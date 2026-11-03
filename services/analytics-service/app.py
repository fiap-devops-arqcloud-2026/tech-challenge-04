import os
import sys
import threading
import json
import uuid
import time
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from flask import Flask, jsonify
from dotenv import load_dotenv
from urllib.parse import urlsplit
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from telemetry import configure_telemetry, instrument_flask, record_error, traced_operation

load_dotenv()

# O Gunicorn atual importa app somente no worker, apos o fork; nao usar --preload.
log = configure_telemetry("analytics-service")

# --- Configuração ---
AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("AWS_SQS_URL")
DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE")
QUEUE_NAME = urlsplit(SQS_QUEUE_URL or "").path.rsplit("/", 1)[-1] or "events"

# SQS_ENABLED é True apenas quando a URL da fila foi realmente informada.
# Em desenvolvimento local, AWS_SQS_URL fica vazia — o worker simplesmente não sobe,
# mas o /health continua respondendo normalmente.
SQS_ENABLED = bool(SQS_QUEUE_URL)

if not AWS_REGION:
    log.critical("Erro: AWS_REGION deve ser definida.")
    sys.exit(1)

# Clientes Boto3 são criados apenas quando SQS está habilitado.
# Em modo local, não precisamos de nenhum cliente AWS.
sqs_client = None
dynamodb_client = None

if SQS_ENABLED:
    # Em produção (EKS), todas as variáveis são obrigatórias
    if not DYNAMODB_TABLE_NAME:
        log.critical("Erro: AWS_DYNAMODB_TABLE deve ser definida quando AWS_SQS_URL está configurada.")
        sys.exit(1)
    try:
        session = boto3.Session(region_name=AWS_REGION)
        # endpoint_url alternativo, para teste local.
        #
        # Em producao as variaveis nao existem, o "or None" faz o boto3
        # receber None e usar o endpoint real da AWS. No compose de
        # integracao elas apontam para simuladores locais, o que permite
        # exercitar o fluxo completo sem tocar na conta.
        sqs_client = session.client("sqs", endpoint_url=os.getenv("SQS_ENDPOINT") or None)
        dynamodb_client = session.client("dynamodb", endpoint_url=os.getenv("DYNAMODB_ENDPOINT") or None)
        log.info("aws.clients.initialized")
    except NoCredentialsError:
        log.critical("Credenciais da AWS não encontradas. Verifique seu ambiente.")
        sys.exit(1)
    except Exception as e:
        log.critical("aws.clients.failed", extra={"error_type": type(e).__name__})
        sys.exit(1)
else:
    # Aviso claro no log para quem inspecionar o container localmente
    log.warning("AWS_SQS_URL não configurada — worker SQS desabilitado (modo local/desenvolvimento).")


# --- SQS Worker ---

def message_context(message):
    """W3C apenas nos MessageAttributes; nunca extrair contexto do corpo de negocio."""
    carrier = {}
    attributes = message.get("MessageAttributes") or {}
    for key in ("traceparent", "tracestate"):
        attribute = attributes.get(key) or {}
        value = attribute.get("StringValue") if isinstance(attribute, dict) else None
        if isinstance(value, str):
            carrier[key] = value
    return TraceContextTextMapPropagator().extract(carrier)


def process_message(message):
    """Preserva o contrato: persistir evento primeiro, confirmar na fila depois."""
    with traced_operation(
        "sqs.process",
        kind=SpanKind.CONSUMER,
        context=message_context(message),
        attributes={
            "messaging.system": "aws_sqs",
            "messaging.destination.name": QUEUE_NAME,
            "messaging.operation.name": "process",
            "messaging.operation.type": "process",
        },
    ) as consumer_span:
        try:
            log.info("analytics.message.processing")
            body = json.loads(message['Body'])
            event_id = str(uuid.uuid4())
            item = {
                'event_id': {'S': event_id},
                'user_id':  {'S': body['user_id']},
                'flag_name':{'S': body['flag_name']},
                'result':   {'BOOL': body['result']},
                'timestamp':{'S': body['timestamp']}
            }

            with traced_operation("dynamodb.PutItem", kind=SpanKind.CLIENT, attributes={
                "db.system.name": "aws.dynamodb",
                "db.operation.name": "PutItem",
                "db.collection.name": DYNAMODB_TABLE_NAME,
            }):
                dynamodb_client.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)
            log.info("analytics.event.persisted")

            # Mesma semantica da base: so confirmar depois de salvar com sucesso.
            with traced_operation("sqs.DeleteMessage", kind=SpanKind.CLIENT, attributes={
                "messaging.system": "aws_sqs",
                "messaging.destination.name": QUEUE_NAME,
                "messaging.operation.name": "DeleteMessage",
                "messaging.operation.type": "settle",
            }):
                sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
            log.info("analytics.message.processed")

        except json.JSONDecodeError as error:
            record_error(consumer_span, error)
            log.error("analytics.message.invalid_json", extra={"error_type": type(error).__name__})
            # Nao deleta: mensagem volta apos o timeout de visibilidade.
        except ClientError as error:
            record_error(consumer_span, error)
            log.error("analytics.message.aws_failed", extra={"error_type": type(error).__name__})
        except Exception as error:
            record_error(consumer_span, error)
            log.error("analytics.message.failed", extra={"error_type": type(error).__name__})


def sqs_worker_loop():
    """Loop infinito que faz long-polling na fila SQS."""
    log.info("Iniciando o worker SQS...")
    while True:
        try:
            # WaitTimeSeconds=20 → long-polling: só retorna quando há mensagem ou após 20s
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                MessageAttributeNames=["traceparent", "tracestate"]
            )

            messages = response.get('Messages', [])
            if not messages:
                continue

            log.info("analytics.batch.received")
            for message in messages:
                process_message(message)

        except ClientError as e:
            log.error("analytics.poll.aws_failed", extra={"error_type": type(e).__name__})
            time.sleep(10)
        except Exception as e:
            log.error("analytics.poll.failed", extra={"error_type": type(e).__name__})
            time.sleep(10)


# --- Servidor Flask (apenas para health check) ---

app = Flask(__name__)
app.config["TELEMETRY_SERVICE_NAME"] = "analytics-service"
instrument_flask(app)

@app.route('/health')
def health():
    """ Verificação de saúde — usada pelos probes do Kubernetes e do docker compose """
    return jsonify({"status": "ok"})


# --- Inicialização ---

def start_worker():
    """Inicia o worker SQS em thread separada — apenas se SQS estiver configurado."""
    if not SQS_ENABLED:
        # Modo local: não inicia o worker, mas o Flask continua rodando normalmente
        return
    worker_thread = threading.Thread(target=sqs_worker_loop, daemon=True)
    worker_thread.start()


start_worker()

if __name__ == '__main__':
    # O default de os.getenv precisa ser str ou None: a funcao devolve
    # sempre uma string quando a variavel existe, e misturar os tipos
    # confunde quem le. O int() externo continua fazendo a conversao.
    port = int(os.getenv("PORT", "8005"))
    # nosec B104 - o bandit alerta sobre ligar em todas as interfaces.
    # Aqui e o comportamento CORRETO e necessario: o processo roda dentro
    # de um container, e ligar apenas em 127.0.0.1 o tornaria inalcancavel
    # pelo kubelet e pelo Service do Kubernetes. Quem restringe o acesso
    # nao e o bind, e o Service ClusterIP (sem Ingress, ver D-012) somado
    # aos security groups da VPC.
    app.run(host='0.0.0.0', port=port, debug=False)  # nosec B104
