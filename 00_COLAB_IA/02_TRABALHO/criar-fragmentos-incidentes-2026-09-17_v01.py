from pathlib import Path
import json
from urllib.parse import quote
import guia_base as g

W=Path(__file__).parent
F=W/'fragmentos/incidentes'
F.mkdir(parents=True,exist_ok=True)
g.AGENTE='Codex'
g.DATA='2026-09-17'
names=[]

def ref(n,pages):
    first=pages.split('–')[0].split(',')[0]
    fn=f'POSTECH - Automacao de Incidentes - Aula {n}.pdf'
    return f'<p class="source">Fonte: <a href="{quote(fn)}#page={first}">Automação de incidentes — Aula {n}, p. {pages}</a>.</p>'

def put(num,ident,title,body):
    name=f'{num:02d}-{ident}.html'
    (F/name).write_text(g.section(ident,title,body),encoding='utf8')
    names.append(name)

def note(ident,text):
    return f'<aside class="note"><strong>{ident} · [INCERTO] no material</strong>{text}</aside>'

def card(n,title,ids,simple,terms,use,case,project):
    return f'<article class="lesson"><div class="lesson-head"><span class="num">{n:02d}</span><div><h3>{title}</h3><span class="badge ok">Essencial no projeto</span></div></div><p>'+''.join(g.badge(i) for i in ids)+'</p><dl class="facets">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in [('Em miúdos',simple),('Siglas e termos',terms),('Para que serve',use),('Caso de uso',case),('Na Fase 4',project)])+'</dl>'

def flow(items):
    return '<ol class="flow">'+''.join(f'<li><div><strong>{a}</strong><span>{b}</span></div></li>' for a,b in items)+'</ol>'

put(0,'visao-geral','Do alerta à recuperação e ao aprendizado', '''<div class="intro"><div class="box"><h3>O que você vai aprender</h3><p>Reconhecer impacto real, reduzir ruído, envolver a equipe certa, comunicar o incidente e automatizar uma tentativa de recuperação. Depois, aprender com a falha para reduzir recorrência.</p></div><div class="box hi"><h3>O que a entrega precisa mostrar</h3><p>Alerta disparando, incidente aberto, mensagem de ChatOps recebida e automação executando uma ação corretiva. Um botão clicado manualmente ou uma função que só imprime uma mensagem não demonstra o Self-Healing exigido.</p></div></div><p>As sete aulas avançam de fundamentos de incidentes até Runbook Automation, GitOps, Engenharia de Caos e pós-incidente. O nível começa introdutório e chega a exemplos intermediários/avançados; os exemplos Python têm simplificações explicitadas neste guia.</p>'''+ref(1,'3–6')+ref(6,'3–13')+ref(7,'3–13')+'''<p class="source">Exigência de demonstração: enunciado da Fase 4, p. 5–6; REQ-OBR-16 a 19, 22, 28 a 31, 37 e 38.</p>'''+g.complement('''<p><strong>Ordem de estudo:</strong> evento e impacto → qualidade do alerta → medição do tempo → gestão de incidentes → comunicação → execução automática → validação e aprendizado. Leia primeiro as fichas; consulte o código junto das notas de fidelidade antes de pensar em adaptação ao ToggleMaster.</p>'''))

terms=[('Evento','Ocorrência ou mudança de estado observável; pode ser rotineira. Aula 1, p.7 e 11.'),('Incidente','Interrupção/degradação de serviço; o enquadramento depende de serviço, risco ou segurança. Aula 1, p.7–12.'),('SLI / SLO','Indicador / objetivo de nível de serviço: observação medida e meta de confiabilidade. SLO: Aula 1, p.8; a sigla SLI aparece no dashboard da p.9.'),('Error budget','Parcela de falha tolerada pela meta e pela janela definida. Aula 1, p.8–9.'),('MTTR / MTTD','Tempo médio para resolução / para detecção. Defina início e fim antes de calcular; há conflito no material. Aula 3, p.5–8 e 17.'),('On-call / escalonamento','Pessoa de plantão e cadeia de encaminhamento quando não há resposta. Aula 3, p.15–16.'),('Deduplicação','Consolidar repetições do mesmo problema usando uma identidade comum. Aula 4, p.7–9.'),('Agrupamento / inibição','Reunir alertas relacionados / suprimir notificações dependentes de um alerta ativo. Aula 2, p.14–16.'),('ChatOps','Interação operacional pelo canal de comunicação, ligando contexto e ações. Aula 5, p.6–10.'),('Webhook','Chamada de integração acionada por um evento para comunicar/solicitar uma ação em outro sistema. Aula 4, p.12–13.'),('Runbook','Procedimento para diagnóstico ou recuperação; automatizado, torna-se código executável. Aula 6, p.3–5.'),('Self-Healing','Recuperação automática diante de falhas, seguida de verificação e escalonamento quando necessário. Aula 7, p.10–11.'),('RCA / post-mortem','Análise de fatores que contribuíram para o incidente e registro de evidências/aprendizados. Aula 7, p.11–13.'),('Blameless','Investigar condições sistêmicas sem buscar culpados individuais. Aula 1, p.6; Aula 7, p.12–13.'),('Idempotência','Repetir a automação deve convergir ao estado esperado; o exemplo simplificado da aula exige cautela com efeitos de reinícios. Aula 7, p.6.'),('AIOps','Uso de análise/IA para correlacionar eventos, detectar anomalias e apoiar prevenção/resposta. Aula 7, p.5–6.')]
put(1,'glossario','Vocabulário para acompanhar as aulas','<div class="glossary">'+''.join(f'<div class="term"><span class="k">{k}</span><span class="d">{d}</span></div>' for k,d in terms)+'</div>')

b=card(1,'O Que é um Incidente?',['REQ-OBR-16','REQ-OBR-17'],'Uma luz acesa no painel não significa, sozinha, que o serviço parou. É preciso relacionar o sinal ao efeito sobre o usuário e o negócio.','ITIL, SRE, COBIT, NIST, SLO, error budget, blameless.','Declarar, classificar e tratar problemas com critérios compartilhados.','A aula distingue CPU a 70% (informação), 95% por 5 minutos (aviso) e resposta acima do SLA por causa da CPU (incidente). Esses números são exemplos.','O alerta deve representar uma condição relevante; a plataforma de incidentes organiza a resposta à falha demonstrada.')+ref(1,'5–12')
b+='''<h4>Em miúdos: de “quem sabe resolver?” a um processo repetível</h4><p>A aula descreve a evolução de operações dependentes de especialistas para práticas padronizadas e, depois, para engenharia de confiabilidade. SRE emprega software, objetivos de serviço e orçamento de erro. A cultura blameless investiga por que o sistema permitiu o impacto, considerando tecnologia, processos e organização.</p>'''+ref(1,'5–6')
b+='<h4>Tecnicamente: quatro perspectivas para o mesmo sinal</h4>'+g.table(['Perspectiva','Quando o sinal importa','Foco da resposta'],[('ITIL 4','Interrupção não planejada ou redução da qualidade.','Restaurar serviço e minimizar impacto de negócio.'),('SRE','Violação/ameaça à meta de confiabilidade e consumo do error budget.','Resposta sistemática e engenharia para reduzir recorrência.'),('COBIT','Risco para objetivos de negócio, com critérios definidos pela organização.','Governança, registro, classificação e métricas de controle.'),('NIST, conforme referência da aula','Violação ou ameaça iminente às políticas de segurança.','Analisar/validar indicadores; conter, erradicar e recuperar.')])+ref(1,'7–12')
b+='''<p>O fluxo SRE ilustrado na p.9 passa por preparar, detectar, triar, mitigar, resolver, aprender e aplicar melhorias; a comunicação acompanha a resposta. Mitigar reduz o dano, enquanto aprender e corrigir fatores contribuintes ajuda a evitar repetição.</p>'''+ref(1,'9')
b+=g.complement('''<p><strong>No ToggleMaster:</strong> “o pod usa mais CPU” é uma observação; “requisições de avaliação estão falhando e usuários não obtêm resultado” descreve impacto. Use o primeiro dado para investigar o segundo. Registrar incidente e executar mitigação são etapas diferentes.</p>''')
b+=note('INC-A01-01','A revisão da p.14 menciona um modelo de cinco níveis e ISO 20000 sem desenvolvê-los no corpo desta aula. O guia não reconstrói essas partes ausentes. A Figura 5, p.12, representa ciclo de resposta cibernética, embora a legenda anuncie evolução histórica.')
b+='''<p><strong>Para memorizar:</strong> evento → avaliação de impacto → incidente → resposta → aprendizado. Uma correção rápida não encerra o aprendizado.</p></article>'''
put(2,'aula-01','Aula 1 — O Que é um Incidente?',b)

b=card(2,'Monitoramento Ativo e “Alert Fatigue”',['REQ-OBR-16','SUG-02'],'Se o telefone toca o tempo todo sem ação útil, a equipe perde confiança no alerta. A qualidade do sinal protege a atenção do plantão.','Baseline, anomalia, flapping, severidade, agrupamento e inibição.','Detectar degradações e comunicar o que exige resposta.','A aula mostra a falha de um banco gerando alertas em dezenas de serviços dependentes: muitos sintomas podem vir do mesmo problema.','Projetar o alerta inteligente e explicar por que sua condição, janela e encaminhamento fazem sentido.')+ref(2,'5–10')
b+='''<h4>Monitoramento e observabilidade</h4><p><strong>Em miúdos:</strong> uma pergunta pré-definida diz se algo está fora da faixa; explorar telemetria correlacionada ajuda a descobrir por quê. <strong>Tecnicamente:</strong> a aula associa monitoramento a sinais conhecidos e observabilidade a métricas, logs estruturados e traces, com contexto para perguntas novas. A tabela da p.6 compara essas capacidades.</p>'''+ref(2,'5–6')
b+=g.table(['Causa de fadiga','Como aparece na aula','Resposta estudada'],[('Limiar estático fora de contexto','CPU alta em carga de trabalho esperada.','Contextualizar baseline por serviço e padrão temporal.'),('Alerta não acionável','Disco acima de um percentual sem urgência real.','Dashboard/ticket quando não exige ação imediata.'),('Tempestade','Falha de dependência produz muitas notificações.','Agrupar e inibir sintomas relacionados.'),('Falso positivo / flapping','Métrica oscila perto do limiar e alterna estados.','Revisar limiar, persistência e contexto.'),('Falta de contexto','Sinal isolado sem impacto, região ou mudança recente.','Acrescentar serviço, impacto e correlação.'),('Redundância','Duas ferramentas notificam o mesmo problema.','Definir responsabilidade e deduplicar.')])+ref(2,'6–9')
b+='''<h4>Baseline dinâmico, severidade e encaminhamento</h4><p>O baseline aprende padrões históricos. A aula usa média por horário mais três desvios-padrão; no exemplo, 5.000 + 3 × 300 = 5.900 requisições. Ela também apresenta regressão com sazonalidade e modelos como ARIMA/LSTM. A proposta de coletar 2–4 semanas é orientação da aula, não requisito do projeto.</p><p>Os quatro níveis ilustrativos vão de informação registrada, passando por ticket e notificação, até acionamento urgente do plantão. A severidade deve considerar impacto; números de timeout e percentuais apresentados são exemplos, não regras universais.</p>'''+ref(2,'10–14')
b+=g.table(['Mecanismo','O que faz','Cuidado'],[('Agrupamento','Reúne alertas de um serviço/cluster em uma mensagem.','Manter quantidade de instâncias e contexto visíveis.'),('Inibição','Silencia notificações secundárias enquanto a condição principal está ativa.','Dependência errada pode esconder problema independente.'),('Deduplicação','Evita novas notificações para a mesma identidade de problema.','Identidade ampla demais mistura falhas distintas.')])+ref(2,'14–16')+ref(4,'7–9')
b+=note('INC-A02-01','A p.13 afirma que 99,9% de disponibilidade permite aproximadamente “43 segundos” mensais. A unidade está inconsistente; os limiares em segundos derivados dela não devem ser copiados.')
b+=g.complement('<p><strong>Conferência matemática:</strong> assumindo um mês de 30 dias e disponibilidade baseada em tempo, o orçamento de 0,1% é 30 × 24 × 60 × 0,001 = <strong>43,2 minutos</strong> (2.592 segundos). Para uma métrica baseada em requisições, o orçamento é expresso em requisições malsucedidas, e não convertido automaticamente em downtime.</p>')
b+='''<p><strong>Para memorizar:</strong> relevante, acionável e com contexto. Um algoritmo de anomalia também precisa de histórico confiável e revisão após mudanças.</p></article>'''
put(3,'aula-02','Aula 2 — Monitoramento Ativo e “Alert Fatigue”',b)

b=card(3,'MTTR Baixo com PagerDuty',['REQ-OBR-17','REQ-OBR-19'],'Reduzir o tempo de um incidente exige descobrir em qual etapa a equipe está esperando ou investigando. A ferramenta coordena pessoas e ações.','MTTR, MTTD, reconhecimento, diagnóstico, remediação e verificação.','Medir o ciclo, rotear ao plantão, enriquecer contexto e automatizar procedimentos conhecidos.','A aula compara um cenário ilustrativo de 45 minutos com outro de 12 minutos usando orquestração e contexto; não é resultado deste projeto.','Abrir incidente automaticamente e guardar sua linha do tempo para demonstrar a cadeia de resposta.')+ref(3,'5–18')
b+='<h4>Medir antes de otimizar</h4>'+g.table(['Etapa','Pergunta operacional','Prática estudada'],[('Detecção','Quanto tempo o problema existiu sem ser percebido?','Monitoramento de sintomas, RUM e testes sintéticos.'),('Resposta','Quanto tempo até alguém reconhecer o alerta?','Plantão, multicanal e escalonamento.'),('Diagnóstico','Quanto tempo para entender a falha?','Logs, traces, histórico e mudança recente no mesmo contexto.'),('Remediação','Quanto tempo para aplicar a tentativa de correção?','Runbook parametrizado e automação.'),('Verificação','Como confirmar que o usuário voltou a ser atendido?','Critério de resolução e teste automatizado.')])+ref(3,'6–15')
b+='''<p><strong>Tecnicamente:</strong> registre timestamps de detecção, reconhecimento, investigação, identificação da causa, início/fim da remediação e confirmação da resolução. Separe incidentes por severidade, serviço e tipo antes de comparar. Incidentes não detectados, recorrentes ou parcialmente mitigados podem distorcer a média.</p>'''+ref(3,'6–8')
b+=note('INC-A03-01','A p.5 define MTTR da detecção à resolução, mas a fórmula da p.6 soma também o tempo desde o início da falha até sua detecção. A metodologia da própria p.6 volta a iniciar na detecção. Há duas fronteiras diferentes no material.')
b+=g.complement('<p><strong>Convenção explícita para estudar:</strong> guarde separadamente duração até detectar e duração da detecção à recuperação confirmada. Calcule a média de cada série e publique os marcos usados. Se quiser a duração total do impacto, nomeie-a assim e inclua o período anterior à detecção. Não some a detecção duas vezes.</p>')
b+='''<h4>Como o PagerDuty participa, segundo a aula</h4><p>As p.15–17 descrevem políticas de escalonamento, canais múltiplos, agrupamento/correlação, integração por webhook, runbooks, timeline, histórico e apoio ao pós-incidente. O valor didático está em reduzir espera e reunir contexto, não em substituir os backends de observabilidade.</p><p>A confirmação de recuperação é separada da execução de uma ação. A aula propõe verificar erro, latência e sucesso de uma operação antes de resolver o incidente; se o critério não for atendido, manter aberto e escalar.</p>'''+ref(3,'14–17')
b+=g.complement('<p><strong>Aplicação à entrega:</strong> para o REQ-OBR-19, selecione uma ação que possa ser disparada automaticamente no cenário demonstrado. Uma etapa que aguarda clique humano pode existir em outros runbooks, mas não substitui a tentativa automática exigida pelo enunciado, p.5.</p>')
b+='''<p><strong>Para memorizar:</strong> reconhecer ≠ resolver; script terminou ≠ serviço recuperou. Compare tempos apenas com fronteiras e categorias equivalentes.</p></article>'''
put(4,'aula-03','Aula 3 — MTTR Baixo com PagerDuty',b)

b=card(4,'MTTR Baixo com OpsGenie (Atlassian)',['REQ-OBR-17','REQ-OBR-40','SUG-02'],'Consolidar mensagens repetidas e entregar contexto à equipe certa evita que um incidente pareça dez problemas diferentes.','Fingerprint, enriquecimento, roteamento, supressão e atribuição.','Organizar alto volume de alertas e integração com a gestão de trabalho.','Dez instâncias do mesmo serviço podem virar uma notificação com o total afetado, usando uma identidade por alerta e serviço.','Comparar a plataforma de incidentes escolhida e justificar a escolha no relatório; o enunciado pede PagerDuty OU OpsGenie.')+ref(4,'5–15')
b+='''<h4>Identidade, contexto e destino</h4><p><strong>Em miúdos:</strong> deduplicar decide se a mensagem repete um problema conhecido; enriquecer acrescenta informações úteis; rotear escolhe quem deve agir. <strong>Tecnicamente:</strong> a aula apresenta combinações de campos como fingerprint, correlação e proximidade temporal; metadados de serviço/ambiente ajudam a selecionar time, prioridade e runbook.</p><p>O enriquecimento ilustrado inclui impacto, ticket, histórico, runbook e proprietário. A aula ressalta que integração demais pode atrasar notificação, e que consolidação agressiva pode esconder problemas.</p>'''+ref(4,'7–11')
b+='''<h4>Medir o que a plataforma realmente observa</h4><p>A p.6 distingue criação, notificação, reconhecimento, atribuição, resolução e encerramento. Sua fórmula soma notificação + reconhecimento + atribuição + resolução, deixando fora o período anterior à criação do alerta. Os relatórios descritos na p.7 incluem média, mediana e percentis, por equipe/tipo/período.</p>'''+ref(4,'6–7')
b+=note('INC-A04-01','A enumeração da p.6 mistura um instante (criação) com durações e inclui encerramento, mas a fórmula soma somente quatro durações. Use a fórmula como convenção da aula, não como especificação verificada da API ou do relatório comercial atual.')
b+='''<h4>Supressão e resposta integrada</h4><p>Regras de manutenção, horários e dependências reduzem notificações esperadas. O cenário das p.12–13 cria ticket, adiciona dados, atribui time, notifica Slack, aciona runbook por webhook e escala se a remediação falhar. A análise de padrões nas p.13–14 procura recorrência ligada a deploys e outras mudanças.</p><p>As p.15–16 posicionam PagerDuty para orquestração e OpsGenie para volume de alertas/integração Atlassian. Essas comparações expressam o material do curso; alegações de superioridade, preços e recursos disponíveis precisam de confirmação antes de uma escolha operacional.</p>'''+ref(4,'11–16')
b+=g.complement('<p><strong>Critério de decisão para o projeto:</strong> verifique acesso disponível, integração com o alerta escolhido, abertura automática do incidente e registro da execução. A aula menciona usar ambos em grandes operações; a Fase 4 pede escolher um. Não amplie a entrega por causa desse exemplo.</p>')
b+='''<p><strong>Para memorizar:</strong> consolidar preservando contexto; encaminhar preservando responsabilidade. Acesso comercial e função disponível dependem da situação atual da plataforma.</p></article>'''
put(5,'aula-04','Aula 4 — MTTR Baixo com OpsGenie (Atlassian)',b)

b=card(5,'Notificação e Interação com Slack e Teams',['REQ-OBR-18','REQ-OBR-30','REQ-OBR-37'],'A mensagem precisa ajudar a agir: dizer o que falhou, quem foi afetado, quando começou e onde investigar.','ChatOps, interação bidirecional, reconhecimento, atribuição e runbook executável.','Reduzir troca de ferramentas e registrar a colaboração durante o incidente.','A aula apresenta uma mensagem de erro do serviço de pagamentos com impacto, horário, taxa de erros, latência, histórico, runbook e ações.','Enviar notificação detalhada, mostrá-la chegando no vídeo e capturar seu print para o relatório.')+ref(5,'6–11')
b+='<h4>As cinco camadas de integração</h4>'+g.table(['Camada','O que acrescenta','Cuidados da aula'],[('1 · Notificação básica','Título, severidade, serviço, impacto, horário e link.','Testar entrega e filtrar ruído.'),('2 · Contexto enriquecido','Métricas/logs, negócio, histórico, runbook, responsável.','Enviar básico rápido e atualizar contexto depois.'),('3 · Interação bidirecional','Reconhecer, atribuir, resolver e escalar pelo canal.','Sincronizar estado entre chat e plataforma.'),('4 · Runbook executável','Acionar procedimentos e receber progresso/resultado.','Aprovação condicional e trilha de execução.'),('5 · Inteligência contextual','Hipóteses causais, recomendações e previsões.','Histórico e análise confiáveis antes de maior complexidade.')])+ref(5,'6–12')
b+='''<h4>O que faz uma mensagem ser acionável</h4><p><strong>Em miúdos:</strong> entregue uma mensagem que a pessoa entenda rapidamente e da qual consiga chegar às evidências. <strong>Tecnicamente:</strong> a aula recomenda formato consistente, segmentação por serviço/equipe/severidade, deduplicação entre produtores e medição do intervalo entre notificação e reconhecimento. Contexto excessivo também atrapalha.</p><p>As integrações descritas incluem notificações, reconhecimento, atribuição, notas e escalonamento no Slack; a p.15 apresenta ações equivalentes no Teams. Os PDFs não fornecem payload de API, configuração de webhook ou código para essas integrações: o conteúdo é um projeto conceitual de interação.</p>'''+ref(5,'12–15')
b+=note('INC-A05-01','A p.13 recomenda quiet hours sem explicar exceções para emergências/plantão. Não conclua que todo alerta crítico deve ficar silencioso à noite. O enunciado p.5 permite Teams, mas o vídeo p.6 cita Slack/Discord: dúvida Q-02 no README.')
b+=g.complement('<p><strong>Para o ToggleMaster:</strong> inclua identidade do incidente, serviço, ambiente, condição que disparou, horário com fuso e links de investigação. Preserve um caminho de escalonamento para falhas críticas. Um botão “Remediate” demonstra interação humana; o Self-Healing precisa também ser acionado pelo evento automaticamente.</p>')
b+='''<p><strong>Para memorizar:</strong> o chat comunica e permite interação; a plataforma precisa manter o estado do incidente consistente. Mensagem enviada não prova mensagem recebida.</p></article>'''
put(6,'aula-05','Aula 5 — Notificação e Interação com Slack e Teams',b)

code1='''import json
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
logs = boto3.client('logs')

def lambda_handler(event, context):
    """Coleta dados de diagnóstico para Taxa de Erro Alta"""
    try:
        incident_data = json.loads(event['body'])
        service_name = incident_data['incident']['service']['summary']

        # Coleta: Métricas de Taxa de Erro
        error_rate = cloudwatch.get_metric_statistics(
            Namespace='PaymentService',
            MetricName='ErrorRate',
            Dimensions=[{'Name': 'ServiceName', 'Value': service_name}],
            StartTime=datetime.utcnow() - timedelta(minutes=5),
            EndTime=datetime.utcnow(),
            Period=60,
            Statistics=['Average']
        )

        # Coleta: Últimos logs de erro
        error_logs = logs.filter_log_events(
            logGroupName=f'/aws/lambda/{service_name}',
            filterPattern='[ERROR]',
            limit=10
        )

        # Consolidar dados
        diagnostic_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': service_name,
            'error_rate': error_rate['Datapoints'],
            'recent_errors': [e['message'] for e in error_logs['events']]
        }

        return {'statusCode': 200, 'body': json.dumps(diagnostic_data)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}'''
code2='''import boto3
import time

autoscaling = boto3.client('autoscaling')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    """Executa mitigação automática: escalar o serviço"""
    try:
        service_name = event['service']

        # Validação: Verificar se é seguro escalar
        if not validate_mitigation(service_name):
            return {'statusCode': 400, 'body': 'Validação falhou'}

        # Executar: Escalar o serviço
        autoscaling.set_desired_capacity(
            AutoScalingGroupName=f'{service_name}-asg',
            DesiredCapacity=5
        )

        # Monitorar: Aguardar 30 segundos
        time.sleep(30)

        # Verificar: Se resolvido, sucesso; senão, rollback
        if is_resolved(service_name):
            return {'statusCode': 200, 'body': 'Resolvido automaticamente'}
        else:
            rollback_mitigation(service_name)
            return {'statusCode': 206, 'body': 'Escalar para humano'}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def validate_mitigation(service_name):
    """Valida se é seguro executar mitigação"""
    # Verificar: múltiplas instâncias, sem manutenção, capacidade disponível
    return True

def is_resolved(service_name):
    """Verifica se taxa de erro voltou ao normal"""
    # Obter métrica atual e comparar com limiar
    return True

def rollback_mitigation(service_name):
    """Desfaz a mitigação se não funcionou"""
    autoscaling.set_desired_capacity(
        AutoScalingGroupName=f'{service_name}-asg',
        DesiredCapacity=3
    )'''
code3='''import json
import time
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Remediação com aprovação: rollback de deployment"""
    try:
        service_name = event['service']

        # Análise: Detectar deployment recente
        deployment = get_recent_deployment(service_name)
        if deployment and deployment['minutes_ago'] < 15:
            # Solicitar aprovação
            request_approval(service_name, deployment)

            # Aguardar aprovação (timeout: 5 minutos)
            if wait_for_approval(timeout_minutes=5):
                execute_rollback(service_name, deployment)
                return {'statusCode': 200, 'body': 'Rollback executado'}

        return {'statusCode': 200, 'body': 'Nenhuma ação necessária'}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def get_recent_deployment(service_name):
    return {'commit': 'abc123', 'minutes_ago': 7}

def request_approval(service_name, deployment):
    print(f"[SLACK] Solicitando aprovação para rollback de {deployment['commit']}")

def wait_for_approval(timeout_minutes=5):
    time.sleep(5)  # Simular espera
    return True

def execute_rollback(service_name, deployment):
    print(f"[AÇÃO] Fazendo rollback para {deployment['commit']}")'''
code4='''import json

def lambda_handler(event, context):
    """Análise de causa raiz após incidente resolvido"""
    try:
        service_name = event['service']

        # Análise 1: Correlação com deployment
        deployment_score = analyze_deployment(service_name)
        # Análise 2: Correlação com mudanças de config
        config_score = analyze_config_changes(service_name)
        # Análise 3: Padrões em logs
        log_score = analyze_log_patterns(service_name)

        # Determinar causa provável
        analyses = [deployment_score, config_score, log_score]
        probable_cause = max(analyses, key=lambda x: x['score'])

        # Criar ticket para correção
        create_jira_ticket(service_name, probable_cause)
        # Notificar team
        notify_team(service_name, probable_cause)

        return {'statusCode': 200, 'body': 'Análise completa'}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def analyze_deployment(service_name):
    return {'type': 'deployment', 'score': 0.95, 'recommendation': 'Rollback'}

def analyze_config_changes(service_name):
    return {'type': 'config', 'score': 0.7, 'recommendation': 'Revisar mudança'}

def analyze_log_patterns(service_name):
    return {'type': 'logs', 'score': 0.8, 'recommendation': 'Otimizar queries'}

def create_jira_ticket(service_name, analysis):
    print(f"[JIRA] Criando ticket: {analysis['recommendation']}")

def notify_team(service_name, analysis):
    print(f"[SLACK] Causa provável: {analysis['recommendation']}")'''
code5='''import math

def lambda_handler(event, context):
    """Monitoramento preditivo: prevenir incidentes"""
    try:
        services = ['payment-service', 'auth-service']

        for service in services:
            # Predição 1: Vazamento de memória?
            memory = predict_memory_issue(service)
            if memory['will_fail']:
                take_preventive_action(service, 'scale_up')

            # Predição 2: Latência aumentando?
            latency = predict_latency_issue(service)
            if latency['will_violate_slo']:
                take_preventive_action(service, 'scale_up')

            # Predição 3: Taxa de erro aumentando?
            errors = predict_error_increase(service)
            if errors['will_exceed']:
                take_preventive_action(service, 'alert')

        return {'statusCode': 200, 'body': 'Monitoramento preditivo completo'}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def predict_memory_issue(service_name):
    """Prediz vazamento de memória usando tendência exponencial"""
    history = [50, 55, 60, 66, 73]  # Exemplo: crescimento exponencial
    growth_rate = calculate_growth_rate(history)
    projected = history[-1] * (1 + growth_rate) ** 5
    return {
        'will_fail': projected > 95,
        'current': history[-1],
        'projected': projected,
        'hours_until_failure': 5 if projected > 95 else None
    }

def predict_latency_issue(service_name):
    """Prediz violação de SLO de latência"""
    history = [100, 110, 120, 130, 140]  # Crescimento linear
    projected = history[-1] + (history[-1] - history[0]) / len(history)
    return {
        'will_violate_slo': projected > 200,
        'current': history[-1],
        'projected': projected,
        'slo_threshold': 200
    }

def predict_error_increase(service_name):
    """Prediz aumento de taxa de erro"""
    history = [1.0, 1.5, 2.0, 2.5, 3.0]
    projected = history[-1] + (history[-1] - history[0]) / len(history)
    return {
        'will_exceed': projected > 5,
        'current': history[-1],
        'projected': projected,
        'threshold': 5
    }

def calculate_growth_rate(history):
    """Calcula taxa de crescimento exponencial"""
    if len(history) < 2:
        return 0
    log_history = [math.log(max(h, 0.1)) for h in history]
    growth = (log_history[-1] - log_history[0]) / (len(history) - 1)
    return math.exp(growth) - 1

def take_preventive_action(service_name, action):
    print(f"[PREVENÇÃO] Executando {action} em {service_name}")'''

b=card(6,'Runbook Automation — Automação com Functions',['REQ-OBR-19','REQ-OBR-22','REQ-OBR-31','REQ-OBR-38','SUG-04'],'Transformar um procedimento em programa permite executá-lo quando um evento acontece. O programa também precisa saber quando parar e como verificar o resultado.','Function, Lambda, boto3, CloudWatch, ASG, rollback, RCA.','Automatizar diagnóstico e ações conhecidas, com evidências de cada execução.','A aula usa um serviço de pagamentos, métricas/logs AWS e um Auto Scaling Group; depois apresenta aprovação, análise e predição simuladas.','Estudar as funções necessárias ao runbook; implementar integração real ao alerta e entregar seus scripts. O exemplo de ASG não equivale ao Deployment Kubernetes do projeto.')+ref(6,'3–13')
b+='<h4>Cinco camadas, com capacidades diferentes</h4>'+g.table(['Camada','Intenção da aula','O que o exemplo efetivamente contém'],[('Diagnóstico','Coletar contexto automaticamente.','Chamadas CloudWatch/Logs e retorno de dados.'),('Mitigação','Agir e verificar recuperação.','Altera capacidade de ASG, mas validação/saúde retornam True fixo.'),('Remediação com aprovação','Decidir e executar ação autorizada.','Simulação por espera e mensagens em print.'),('Causa raiz','Correlacionar dados e encaminhar correções.','Pontuações constantes e mensagens simulando integrações.'),('Predição','Antecipar degradação e agir.','Listas fixas, projeções matemáticas e ação somente impressa.')])+ref(6,'5–13')
b+='''<aside class="warning"><strong>Leitura de código, sem execução</strong> Os cinco blocos abaixo preservam o conteúdo da aula. Quebras causadas pela largura da página foram normalizadas, mantendo tokens e indentação lógica. A presença de chamadas AWS reais e funções simuladas no mesmo exemplo exige distinguir intenção didática de comportamento implementado. Nenhum destes blocos foi executado.</aside>'''
blocks=[(1,'Diagnóstico',code1,'5–6','Lê o corpo do evento, identifica o serviço, consulta média de ErrorRate em janela de cinco minutos e busca até dez eventos de log. Consolida os dados e retorna JSON. O trecho não envia esses dados ao PagerDuty, apesar de a descrição mencionar enriquecimento do incidente.'),(2,'Mitigação automática',code2,'7–8','Solicita capacidade 5 no ASG, aguarda 30 segundos e consulta is_resolved. O rollback definido coloca capacidade 3. Os valores pertencem ao exemplo e não são dimensionamento do ToggleMaster.'),(3,'Remediação com aprovação',code3,'8–9','Procura um deployment recente; no exemplo, a consulta devolve um dicionário constante. A solicitação e o rollback são prints. wait_for_approval simula a espera e sempre retorna True.'),(4,'Análise de causa raiz',code4,'9–11','Compara três escores e escolhe o maior. Os escores são fixos; os nomes das funções descrevem a integração desejada, mas a criação do ticket e a notificação apenas imprimem mensagens.'),(5,'Detecção preditiva',code5,'11–13','Calcula projeções a partir de listas definidas no código. Compara memória, latência e erros com limiares do exemplo e chama uma função que imprime a ação. Não coleta telemetria real nem efetua escalonamento.')]
for n,title,src,pp,expl in blocks:
    b+=f'<h4>Código-fonte {n} — {title}</h4>'
    b+=g.code(src,f'Aula 6, p. {pp} · transcrição conferida nas páginas renderizadas; quebras de linha da diagramação normalizadas; tokens preservados',expl)+ref(6,pp)
    if n==1:
        b+=g.complement('<p><strong>Leitura crítica:</strong> o nome do grupo de logs é de Lambda e o namespace da métrica é PaymentService; eles não se tornam válidos no Kubernetes apenas por copiar o código. A serialização de valores de data nos Datapoints também precisa ser tratada numa adaptação real. O código original foi mantido.</p>')
    if n==2:
        b+=note('INC-A06-01','validate_mitigation e is_resolved não executam as validações prometidas: ambas devolvem True. O bloco usa json.dumps no tratamento de erro sem importar json. O rollback fixa 3, sem consultar a capacidade anterior. Não interpretar o retorno “Resolvido automaticamente” como prova de recuperação.')
    if n==3:
        b+=note('INC-A06-02','O texto da p.8 afirma execução após timeout mesmo sem aprovação, mas o código p.9 só chama rollback se wait_for_approval for verdadeiro; esta função espera cinco segundos e retorna True. Não existe aprovação humana real nem timeout de cinco minutos implementado.')
        b+=g.complement('<p><strong>Regra para uma implementação real:</strong> silêncio ou timeout não é aprovação. Separe ações previamente autorizadas para execução automática das ações que exigem decisão humana. A tentativa automática de mitigação exigida na Fase 4 pode ser limitada a um procedimento específico; a simulação acima não demonstra esse requisito.</p>')
    if n==5:
        b+=note('INC-A06-03','Os códigos 4 e 5 são simulações de análise/integração. No código 5 falta import json no ramo de exceção. Os históricos não documentam a duração entre amostras; “hours_until_failure” não comprova horizonte real. Os percentuais de sucesso/redução apresentados ao lado dos códigos não decorrem de testes exibidos nestes PDFs.')
b+='''<p><strong>Para memorizar:</strong> função com nome de validação precisa validar; print não envia mensagem; escalar capacidade não comprova resolução; código demonstrativo não é evidência de operação.</p></article>'''
put(7,'aula-06','Aula 6 — Runbook Automation: Automação com Functions',b)

b=card(7,'Self-Healing e Pós-Incidente',['REQ-OBR-05','REQ-OBR-19','REQ-OBR-28','REQ-OBR-31','SUG-04'],'Recuperar automaticamente é só parte do trabalho: testar a recuperação e aprender com a falha torna a próxima resposta mais confiável.','AIOps, GitOps, Chaos Engineering, Circuit Breaker, RCA, blameless.','Coordenar ferramentas, executar procedimentos e transformar evidências em melhorias.','O exemplo GitOps reverte a mudança desejada no Git; o controlador reconcilia o cluster. O exemplo de circuit breaker interrompe chamadas falhas e testa a recuperação gradualmente.','Manter coerência com GitOps, demonstrar falha controlada e execução automática, guardar evidências e justificar a solução.')+ref(7,'5–13')
b+='''<h4>Qualidade do runbook como software</h4><p><strong>Em miúdos:</strong> uma automação precisa ser tão revisável quanto a aplicação que ela tenta reparar. <strong>Tecnicamente:</strong> a aula exige, como boas práticas do conteúdo, idempotência, Git/code review, testes e gestão de segredos. Vault, AWS Secrets Manager e Azure Key Vault são exemplos citados; Rundeck aparece como ferramenta de execução com controle de acesso.</p>'''+ref(7,'6–7')
b+=g.complement('<p><strong>Precisão sobre idempotência:</strong> terminar com o serviço “em execução” não torna qualquer reinício repetido inofensivo. Cada reinício pode interromper requisições. Para o runbook, diferencie convergência do estado, repetição de efeitos e controle de execução concorrente.</p>')
b+='''<h4>GitOps e rollback</h4><p>Na explicação da aula, a mudança é registrada no Git e o agente GitOps aplica o estado desejado no Kubernetes. Isso preserva rastreabilidade da intervenção. O comando abaixo está no texto da p.7; o parâmetro entre sinais representa o commit do exemplo, não um valor real deste repositório.</p>'''
b+=g.code('git revert <commit-do-deploy-defeituoso>','Aula 7, p.7 · comando literal conferido visualmente','Cria uma reversão do commit indicado. A aula descreve depois publicar a mudança para o controlador reconciliar; este guia não executou revert, commit nem push.')+ref(7,'7–8')
b+='''<h4>Caos controlado para validar a resposta</h4><p>A sequência estudada é formular hipótese, injetar uma falha delimitada, medir o comportamento e melhorar. O exemplo supõe latência adicional no banco e failover dentro de um tempo esperado; os 200 ms e 30 s são valores ilustrativos. Gremlin é citado como ferramenta, e as tendências também mencionam Steadybit e AWS FIS.</p>'''+ref(7,'8–9')+ref(7,'14')
b+='<h4>Circuit breaker e retorno gradual</h4>'+flow([('Fechado','Chamadas seguem normalmente; aumento de falhas leva à abertura.'),('Aberto','Suspende chamadas ao destino problemático; aguarda período de recuperação.'),('Semiaberto','Envia sondas/parte do tráfego. Sucesso permite fechar; falha mantém proteção e pode levar ao escalonamento.')])+ref(7,'10–11')
b+='''<p>A aula amplia a resposta para desvio de tráfego e estratégias Blue/Green. Isso ilustra opções de arquitetura; a Fase 4 não exige multirregião, circuit breaker nem contratar ferramenta de caos.</p>'''+ref(7,'10')
b+='''<h4>Pós-incidente e cultura blameless</h4><p>A coleta proposta reúne dashboards, logs, traces, conversa do canal e ações executadas. A análise pode sugerir relações com deploys e pausas de GC; itens de ação podem virar tickets ou rascunhos de PR. O foco é melhorar condições do sistema, com segurança para relatar falhas e quase-acidentes.</p>'''+ref(7,'11–13')
b+=g.complement('<p><strong>Hipótese causal:</strong> uma falha começar logo depois do deploy ajuda a investigar, mas não prova que o deploy foi a causa. Use as evidências para testar a hipótese, preservar a linha do tempo e registrar fatores contribuintes. Depois valide se a melhoria reduziu a recorrência.</p>')
b+=note('INC-A07-01','A abertura da p.4 promete código Python, mas o conteúdo desta aula apresenta conceitos, figuras e o comando Git. Nenhum bloco Python foi localizado nas 20 páginas. A Figura 1 da p.6 é um modelo de maturidade de automação, apesar da legenda de painel AIOps.')
b+='''<p><strong>Para memorizar:</strong> detectar → proteger → tentar recuperar → verificar → escalar ou encerrar → aprender. Automatizar a reação não dispensa observação do resultado.</p></article>'''
put(8,'aula-07','Aula 7 — Self-Healing e Pós-Incidente',b)

put(9,'ciclo','O ciclo integrado de resposta',g.complement(flow([('Detectar impacto','Sinais coletados e contextualizados geram uma condição de alerta relevante.'),('Declarar e rotear','A integração abre o incidente, preserva a identidade e escolhe o responsável.'),('Comunicar','O canal recebe contexto e link; a plataforma registra entrega/reconhecimento.'),('Executar o runbook','O alerta dispara a tentativa automática prevista para aquele cenário.'),('Verificar e escalar','Consultar sinais de recuperação; se a ação falhar, manter o incidente e encaminhar ao humano.'),('Aprender','Organizar evidências e fatores contribuintes; transformar ação de melhoria em trabalho rastreável.')])+'<p>Síntese didática das Aulas 2–7. Os componentes podem executar em paralelo; esta ordem facilita a leitura e não impõe uma topologia única.</p>')+ref(2,'10–16')+ref(3,'14–17')+ref(5,'6–10')+ref(7,'11–13'))

comp=g.table(['Dimensão','PagerDuty conforme Aula 3','OpsGenie conforme Aula 4'],[('Ênfase didática','Orquestração da resposta e runbooks.','Gestão de alertas, deduplicação e enriquecimento.'),('Responsabilidade','Política de escalonamento e plantão.','Roteamento e atribuição por contexto.'),('Contexto','Timeline, histórico e integração com observabilidade.','Metadados, histórico e integração com gestão de trabalho.'),('Medição','Necessita definir marcos do MTTR.','Distingue tempos após criação do alerta.'),('Limite da comparação','Recursos dependem da integração/plano disponível.','Novos cadastros foram encerrados; veja complemento abaixo.')])+ref(3,'15–17')+ref(4,'5–15')
comp+=g.complement('''<p><strong>Disponibilidade verificada em 2026-09-17:</strong> a Atlassian informa que novos cadastros/compras do OpsGenie terminaram em <strong>2025-06-04</strong> e que o acesso será encerrado em <strong>2027-04-05</strong>, com exclusão de dados não migrados. Fontes oficiais: <a href="https://www.atlassian.com/software/opsgenie/pricing" rel="noopener">OpsGenie — preços e encerramento de novas vendas</a> e <a href="https://www.atlassian.com/software/opsgenie/migration" rel="noopener">OpsGenie — migração e encerramento</a>.</p><p>O enunciado continua oferecendo PagerDuty OU OpsGenie. Registre a restrição de acesso na justificativa e confirme a orientação com a FIAP (Q-08 no documento de requisitos). A migração comercial para outro produto não torna esse produto automaticamente aceito no desafio.</p>''')
comp+='<h3>Slack e Teams no conteúdo</h3>'+g.table(['Ponto','Slack','Teams'],[('Conteúdo da aula','Notificação, botões, atribuição, notas, escalonamento e runbooks.','Notificação e ações no canal; a aula também cita calendário Outlook.'),('Papel na entrega','Canal aceito no enunciado e citado no roteiro do vídeo.','Canal aceito na p.5; não citado na lista do vídeo da p.6 (Q-02).'),('O que comprovar','Recebimento da mensagem detalhada e print.','Mesmo objetivo; confirmar a divergência do roteiro antes da entrega.')])+ref(5,'13–15')+'<p class="source">Aceitação de canais: enunciado, p.5–6. Discord é opção do enunciado, mas não recebe uma implementação detalhada nestas aulas.</p>'
put(10,'comparativo','Comparando papéis e opções',comp)

app=g.complement('<p><strong>Roteiro de estudo para uma demonstração rastreável:</strong> os passos abaixo organizam os requisitos, sem afirmar que o projeto já foi implantado.</p>'+flow([('Definir o cenário','Escolher serviço, falha, critério do alerta e ação corretiva que possa ser observada.'),('Ligar toda a cadeia','Configurar alerta → incidente → ChatOps e alerta → runbook; registrar qual componente dispara cada integração.'),('Provocar a falha no ambiente preparado','Gravar o problema, o estado Firing e a abertura do incidente.'),('Demonstrar a execução','Mostrar o evento acionando a automação e a ação corretiva. Registrar resultado, inclusive eventual necessidade de escalonamento.'),('Guardar evidências','Capturar ChatOps e log/execução do runbook para o relatório; registrar arquivos de configuração e justificativas.')]))
app+=g.table(['Evidência','Requisito','Contribuição do módulo'],[('Regra e alerta disparando',g.badge('REQ-OBR-16')+g.badge('REQ-OBR-29'),'Severidade, contexto, janela e ação esperada.'),('Incidente e mensagem chegando',g.badge('REQ-OBR-17')+g.badge('REQ-OBR-18')+g.badge('REQ-OBR-30'),'Integração, identidade e conteúdo detalhado.'),('Falha provocada e correção executando',g.badge('REQ-OBR-28')+g.badge('REQ-OBR-31'),'Teste controlado e observação do runbook.'),('Scripts no repositório',g.badge('REQ-OBR-22'),'Código real e parâmetros documentados.'),('Prints e justificativa',g.badge('REQ-OBR-37')+g.badge('REQ-OBR-38')+g.badge('REQ-OBR-40'),'Notificação, execução e motivo da plataforma escolhida.')])
app+='<p class="source">Fonte normativa: enunciado, p.5–6. A forma de organizar a demonstração é Complemento; os entregáveis e evidências da tabela são exigidos.</p>'
put(11,'aplicacao','Aplicação ao ToggleMaster e à demonstração',app)

bp=g.table(['Prática estudada','Erro comum','Fonte'],[('Alertar de acordo com impacto e ação','Copiar um percentual global para todo serviço.','Aula 2, p.6–13.'),('Agrupar sem perder identidade','Consolidar falhas independentes como se fossem uma só.','Aula 4, p.7–9.'),('Validar após remediar','Encerrar apenas porque a função retornou sucesso.','Aula 3, p.14–15.'),('Usar código versionado, revisado e testado','Runbook fora do Git ou sem ensaio de falha.','Aula 7, p.6–7.'),('Manter segredos fora do código','Publicar token de integração no repositório.','Aula 7, p.7.'),('Rastrear ações e resultados','Mensagem no chat sem identidade da execução.','Aula 5, p.9–10.'),('Aprender com fatores contribuintes','Encerrar o pós-incidente ao apontar uma pessoa.','Aula 7, p.12–13.')])
bp+=g.complement('<p>'+g.badge('SUG-04')+' <strong>Limites para uma automação real:</strong> selecionar apenas os recursos necessários, impedir disparos concorrentes/repetidos, limitar tentativas, definir tempo de espera e registrar saída. Observar recuperação antes de tentar novamente. Esses parâmetros não estão fixados no PDF; precisam ser definidos e testados no cenário do projeto.</p><p>Reinício, rollback, failover e aumento de capacidade têm riscos diferentes conforme dependências e estado. As classificações de baixo/médio/alto risco dos exemplos não devem ser tomadas como universais.</p>')
put(12,'boas-praticas','Boas práticas e erros que comprometem a resposta',bp)

put(13,'outros-modulos','Relação com os outros módulos',g.complement(g.table(['Módulo','O que oferece à automação','Pergunta para integrar'],[('Welcome to Observabilidade e Monitoramento','Contexto evolutivo do projeto e visão da jornada.','Qual comportamento da base será observado?'),('Observabilidade e Monitoramento','Sinais, objetivos de serviço e leitura de confiabilidade.','A condição traduz impacto relevante?'),('Monitoramento Opensource','Métricas, logs, dashboards e transporte de telemetria.','É possível ir do alerta aos sinais que o explicam?'),('APM','Traces, serviços e dependências para diagnóstico.','Qual chamada ou dependência está ligada à falha?'),('Automação de incidentes','Roteamento, comunicação, execução e aprendizado.','A reação foi acionada e seu resultado foi observado?')])+'<p>O vínculo é um mapa didático. A coleta de métricas/logs/traces e o APM vêm do enunciado p.3–4; a resposta ativa e suas evidências vêm das p.5–6.</p>'))

limits=[('INC-A01-01','Aula 1 p.14 anuncia tópicos não desenvolvidos no corpo.','Não inventar níveis/métodos ausentes.'),('INC-A02-01','Aula 2 p.13: orçamento mensal em segundos com unidade errada.','Conferência explícita: 43,2 min para 30 dias a 99,9%.'),('INC-A03-01','Aula 3 p.5–6: MTTR tem fronteiras incompatíveis.','Definir início/fim e separar detecção.'),('INC-A04-01','Aula 4 p.6: enumeração de marcos difere da fórmula.','Não misturar instante de criação com duração.'),('INC-A05-01','Aula 5 p.13: quiet hours sem exceção explícita de plantão.','Preservar caminho de escalonamento de críticos.'),('INC-A06-01','Aula 6 p.7–8: validações constantes, capacidade fixa e import ausente.','Código preservado; não presumir validação real.'),('INC-A06-02','Aula 6 p.8–9: aprovação/timeout inconsistentes e simulados.','Não confundir espera com autorização.'),('INC-A06-03','Aula 6 p.9–13: escores/listas fixas, prints e resultados sem ensaio exibido.','Não alegar integração ou desempenho comprovados.'),('INC-A07-01','Aula 7 p.4 anuncia Python, ausente do restante do PDF.','Preservar conceitos e comando realmente presentes.'),('INC-VIS-01','Legendas divergentes: A1 p.11–12, A2 p.6, A4 p.5 e A7 p.6.','Usar conteúdo visível e texto, sem deduzir pela legenda.'),('INC-EXT-01','Cases, estatísticas, preços, recursos e recomendações comerciais dos PDFs.','Atribuir ao material; não tratar como verificação externa atual.')]
lim='<p>A leitura cobriu os sete PDFs, incluindo introduções, exemplos, figuras, revisão e referências. Não há vídeos ou áudios locais neste módulo. A extração inicial por layout perdeu o corpo; a leitura usou extração completa e páginas renderizadas.</p>'+g.table(['ID [INCERTO]','Limite da fonte','Tratamento no guia'],limits)
lim+='<p>Os resultados de empresas citados nas seções de mercado foram lidos como alegações dos materiais: Aula 1 p.13; Aula 2 p.17–18; Aula 3 p.19; Aula 4 p.16–17; Aula 5 p.16–17; Aula 6 p.14; Aula 7 p.14–16. Este guia não transporta esses percentuais para o ToggleMaster nem promete resultado semelhante.</p><p>O encerramento de novos cadastros do OpsGenie é um fato externo verificado, separado de INC-EXT-01 no <a href="#comparativo">complemento de disponibilidade</a>. Os problemas no texto/código dos PDFs foram mantidos rastreáveis, sem modificar originais.</p>'
put(14,'limites','Fidelidade, incertezas e limites de uso',lim)

qas=[('Todo evento é um incidente?','Não. A Aula 1, p.7–12, distingue ocorrência observável de impacto em serviço, negócio ou segurança.'),('Agrupar e inibir são a mesma coisa?','Não. Agrupar reúne alertas relacionados; inibir suprime notificações secundárias sob uma condição principal ativa. Aula 2, p.14–16.'),('99,9% em 30 dias permite 43 segundos de falha?','Não. A conta correta para disponibilidade por tempo é 43,2 minutos. O exemplo da Aula 2, p.13, contém erro de unidade; confira o complemento matemático.'),('Como comparar dois valores de MTTR?','Definindo os mesmos marcos inicial/final e categorias equivalentes. A Aula 3, p.5–8, tem um conflito de fronteiras que precisa ser explicitado.'),('O que uma notificação detalhada precisa comunicar?','Título/condição, severidade, serviço, impacto, horário e link; contexto e runbook podem enriquecer. Aula 5, p.6–8.'),('O código de mitigação comprova que a taxa de erro normalizou?','Não: is_resolved retorna True constante. Aula 6, p.8. Uma adaptação real precisa consultar o sinal de saúde.'),('O código de aprovação da aula manda mensagem real ao Slack?','Não. request_approval usa print e wait_for_approval simula espera. Aula 6, p.9.'),('Por que GitOps importa ao reverter um deploy?','A mudança de estado desejado fica rastreável no Git e o controlador reconcilia o cluster. Aula 7, p.7–8.'),('O que fazer se a tentativa automática não recuperar o serviço?','A aula orienta verificar critérios, manter o incidente e escalar quando necessário. Aula 3, p.14–15; Aula 7, p.10.'),('Qual evidência evita confundir configuração com funcionamento?','Mostrar falha, alerta Firing, incidente, notificação e execução corretiva, além dos prints e scripts exigidos. Enunciado, p.5–6.'),('O que deve sair de um pós-incidente blameless?','Fatores contribuintes e ações concretas que fortaleçam o sistema, com evidências e acompanhamento. Aula 7, p.11–13.')]
put(15,'revisao','Revisão rápida e autoavaliação','<p>Responda antes de abrir cada item. As perguntas organizam a revisão dos conceitos e das evidências; não representam questões oficiais de prova.</p>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in qas))

connections=[('REQ-OBR-05','Aula 7 relaciona rollback ao estado desejado e à reconciliação GitOps.'),('REQ-OBR-16','Aulas 1–2 ligam condição, impacto, contexto e ação ao alerta inteligente.'),('REQ-OBR-17','Aulas 3–4 estudam abertura/roteamento de incidentes; conferir restrição atual do OpsGenie.'),('REQ-OBR-18','Aula 5 organiza conteúdo e recebimento da notificação detalhada.'),('REQ-OBR-19','Aulas 6–7 explicam reação automática, tentativa corretiva e verificação; simulações devem virar integração real.'),('REQ-OBR-22','Runbooks versionados sustentam a entrega dos scripts/automações.'),('REQ-OBR-23','A cadeia de resposta gera evidência de operação, distinta de configuração.'),('REQ-OBR-28','Engenharia de Caos ajuda a planejar a falha proposital e observar seu efeito.'),('REQ-OBR-29','Qualidade do alerta ajuda a demonstrar a condição Firing no cenário escolhido.'),('REQ-OBR-30','Gestão de incidentes e ChatOps permitem mostrar abertura e notificação chegando.'),('REQ-OBR-31','O runbook precisa mostrar acionamento automático e ação corretiva executada.'),('REQ-OBR-37','A notificação detalhada fornece a evidência visual de ChatOps para o relatório.'),('REQ-OBR-38','Registro da execução oferece log/print da automação de Self-Healing.'),('REQ-OBR-40','Comparar papéis e disponibilidade sustenta a justificativa PagerDuty versus OpsGenie; a parte APM é estudada no módulo APM.'),('SUG-01','Organizar timeline e evidências por requisito e ensaiar a demonstração completa.'),('SUG-02','Escolher contexto/janela, agrupamento e deduplicação para reduzir ruído.'),('SUG-04','Limitar escopo/repetições e verificar recuperação da automação.')]
(F/'conexoes.json').write_text(json.dumps(connections,ensure_ascii=False,indent=2),encoding='utf8')
(F/'config.json').write_text(json.dumps({'pasta':'04.Automação de incidentes','titulo':'Automação de incidentes','subtitulo':'Do sinal acionável ao Self-Healing: contexto, comunicação, execução e aprendizado.','nivel':'Introdutório a avançado, com exemplos Python comentados','agente':'Codex','data':'2026-09-17','revisao':'Leitura integral e conferência visual dos exemplos','fragmentos':names,'conexoes':'conexoes.json'},ensure_ascii=False,indent=2),encoding='utf8')
print(f'{len(names)} fragmentos e configuração salvos em {F}')
