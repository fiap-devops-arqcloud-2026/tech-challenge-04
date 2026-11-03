"""Gera o catálogo rastreável da revisão, sem modificar fontes operacionais."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import json

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
NOW=datetime.now().astimezone().isoformat(timespec='seconds')
F=[]
def finding(id,title,priority,kind,status,refs,evidence,impact,action,acceptance,requirements,comparison,limits='',links=None):
    F.append(dict(id=id,title=title,priority=priority,kind=kind,status=status,refs=refs,evidence=evidence,impact=impact,action=action,acceptance=acceptance,requirements=requirements,comparison=comparison,limits=limits,official_sources=links or []))

finding('F-019','Observabilidade de cluster e ativação OTel ainda ausentes','Alta','lacuna FIAP','Aberto',
 ['gitops/base/kustomization.yaml:34','gitops/overlays/prod/kustomization.yaml:65','observability/otel-collector-local.yaml:54','terraform/k8s/argocd.tf:94'],
 'O overlay gera 23 objetos da aplicação/base, sem Collector/Prometheus/Loki/Grafana. O único helm_release operacional é ArgoCD. A configuração local tem somente pipeline traces com debug e arquivo; não tem pipelines metrics/logs nem exportador APM. Não há variáveis OTEL nos manifests GitOps dos cinco workloads.',
 'A base pode renderizar e os testes locais passar sem que a observabilidade obrigatória da Fase 4 exista no Kubernetes.',
 'Adicionar charts/values ao GitOps; Collector de logs por nó e gateway conforme arquitetura escolhida; Prometheus, Loki, Grafana, rotas de sinais, configuração dos workloads e dashboard. Definir armazenamento, retenção, recursos e credenciais do exportador.',
 'ArgoCD saudável na conta correta; dados atuais dos cinco serviços e contêineres do cluster consultáveis; dashboard mostra recursos, requisições e logs; trace e mapa aparecem no APM.',
 ['REQ-OBR-06','REQ-OBR-07','REQ-OBR-08','REQ-OBR-09','REQ-OBR-10','REQ-OBR-11','REQ-OBR-14','REQ-OBR-15','REQ-OBR-20'],
 'Reconfirma F-019 e I-01/I-02 da revisão de 2026-10-28. Não é uma regressão causada pelo Claude.',
 'Ausência nos fontes operacionais locais; não foi feito inventário de todo recurso remoto nesta rodada.')

finding('F-020','CI não executa a prova integrada de observabilidade','Média','qualidade de validação','Aberto',
 ['.github/workflows/compose-integration.yml:22','scripts/test-observability.sh:17','scripts/integration/test-traces.py:194','.github/workflows/_ci-go.yml:326','.github/workflows/_ci-python.yml:359'],
 'Compose Integration chama somente test-compose.sh; diagnóstico e limpeza usam dois arquivos Compose. Nenhum dos nove workflows chama test-observability.sh/test-traces.py. A publicação depende de build/lint/SAST/SCA do próprio workflow; a integração fica em outro workflow.',
 'Uma regressão no Collector, correlação HTTP/SQS ou sanitização pode passar no fluxo remoto atual. Não há dependência explícita entre publicação e aprovação do ensaio integrado.',
 'Incluir a prova OTel e seus três overlays no CI; preservar evidência sanitizada. Definir como os checks obrigatórios de PR/publicação impedirão uma entrega com integração falhando.',
 'Uma falha deliberada e controlada no contrato de traces reprova o CI; a limpeza inclui o Collector. Confirmar gates remotos após publicação autorizada.',
 ['REQ-OBR-04','REQ-OBR-13','REQ-OBR-14','REQ-OBR-21','REQ-OBR-23'],
 'Reconfirma F-020/I-06; acrescenta a separação dos workflows como ponto de aceite.',
 'O PDF exige CI/CD e evidência, mas não nomeia esse teste específico. Não foram consultadas regras atuais de proteção de branch.')

finding('F-021','Documentação vigente, backlog e plano não refletem o mesmo estado','Média','documentação/handoff','Aberto',
 ['README.md:5','terraform/README.md:3','observability/README.md:83','SECURITY.md:20','docs/requisitos/README.md:14','gitops/SECRETS-CONTRATO.md:10','docs/ARQUITETURA.md:7','docs/GUIA_DE_REPRODUCAO.md:9'],
 'README/Terraform ainda tratam a conta como não informada; observability/README diz que não há conta New Relic. Registros de 2026-10-28/30 já trazem conta/Variables conferidas, contas externas relatadas e backend.hcl criado. SECURITY afirma trust para qualquer branch/PR, contradizendo StringEquals/main atual. Catálogo normativo segue todo Pendente. Há três âncoras quebradas nos dez Markdown operacionais verificados. Plano v02 preserva cronograma de setembro e instrumentadores planejados diferentes da execução registrada.',
 'O próximo agente pode repetir cadastro ou a correção OIDC, seguir comandos da conta anterior, ou confundir plano com entrega. O guia histórico contém merge/push diretos para main e init sem backend-config; não serve como runbook vigente do 04.',
 'Atualizar README/SECURITY/runbook e produzir nova versão do plano, preservando as anteriores. Usar esta matriz para execução e o catálogo original como fonte normativa. Corrigir os três links e fechar o registro de P-013 sem repetir trabalho.',
 'Um leitor de LOG+PENDENCIAS identifica claramente o ponto atual, inclusive conta verificada em 28, backend criado em 30 e integrações ainda não validadas. Documentos operacionais não mandam refazer F-023.',
 ['REQ-OBR-23','REQ-OBR-39','REQ-OBR-40','REQ-OBR-42'],
 'Reconfirma F-021/DOC-01 a DOC-05; amplia de duas para três âncoras porque incluiu SECRETS-CONTRATO. Estado posterior do Claude incorporado.',
 'Correções desta rodada limitadas ao contexto e às saídas da auditoria; os documentos operacionais ficam como achados, sem edição.')

finding('F-022','Exceções de scanner com revisão vencida','Média','dívida de validação','Aberto',
 ['.trivyignore:58','.github/workflows/_ci-go.yml:309','.github/workflows/_ci-python.yml:342'],
 'As três exceções CVE têm revisão marcada para 2026-10-15; a auditoria é de 2026-10-30. Os quatro scans usam esse arquivo.',
 'O gate pode continuar suprimindo achados com justificativas de imagens de setembro, sem confirmação sobre o artefato final.',
 'Reexecutar os scans das imagens/dependências finais na revisão das aplicações e revisar cada exceção, correção disponível, exposição e prazo.',
 'Cada exceção retida tem evidência recente e justificativa; os scans finais e seu resultado são preservados.',
 ['REQ-OBR-04'],
 'Reconfirma F-022/I-08. Nenhum CVE novo foi atribuído ao projeto.',
 'Código, imagens e dependências dos cinco serviços estão fora do escopo atual. Data vencida não comprova vulnerabilidade explorável.')

finding('F-023','Trust OIDC corrigida localmente; fechamento anterior estava pendente','Informativa','correção confirmada','Resolvido no código local',
 ['terraform/modules/iam-ci/main.tf:80','terraform/modules/iam-ci/main.tf:139','terraform/modules/iam-ci/variables.tf:23','terraform/variables.tf:189','00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/correspondencia-aws-github.json:1'],
 'Subject usa owner/repo e seus IDs imutáveis, branch main e StringEquals para sub/aud. Os três arquivos do módulo são byte a byte idênticos ao harness que registrou 8 testes aprovados em 2026-10-28. Correspondência AWS/GitHub registra 34 checks verdadeiros em 28. Terraform validate atual passou.',
 'Não refazer a correção nem aplicar a versão antiga; a pendência real é documental/publicação futura e validação de OIDC em workflow real.',
 'Usar o subject atual. Atualizar status de P-013/F-023 e, quando autorizado o fluxo remoto, provar autenticação e push ECR.',
 'Relatório da etapa 9 ligado ao contexto; CI remoto autentica apenas no contexto esperado. Consultar configuração novamente se owner/repo/branch/environment mudar.',
 ['REQ-OBR-04'],
 'Concorda com Claude em 2026-10-28 15:11. Contradiz apenas caixas/TL;DR antigos ainda não atualizados.',
 '34/34 e 8/8 são evidências de 2026-10-28, reabertas e comparadas; não foram reexecutadas na AWS em 30.')

finding('F-024','Log de 156 MB não ignorado pode impedir publicação Git','Alta','organização/publicação','Aberto',
 ['00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/test-oidc-offline.py:139','.gitignore:1'],
 'offline-test.jsonl tem 156400265 bytes (149,15 MiB), está não rastreado e git check-ignore retorna 1. O gerador usa terraform test -json -verbose e salva a saída integral. O resumo confirma 8 passed/0 failed; o volume não é necessário para apresentar o resultado.',
 'Um git add indiscriminado inclui arquivo maior que o limite de 100 MiB do GitHub para Git comum.',
 'Antes de qualquer commit, ignorar especificamente o artefato bruto e preservar resumo sanitizado/hashes; decidir retenção/arquivamento do bruto. Remover -verbose quando não necessário para evitar nova geração gigante.',
 'git check-ignore reconhece o bruto e a seleção de arquivos para commit não o contém; resumo dos testes continua acessível.',
 ['REQ-OBR-20','REQ-OBR-21','REQ-OBR-22'],
 'Concorda e mede precisamente o F-024 do Claude; não apagado nem modificado.',
 'Não houve commit/push. Não é pedido para usar LFS para log temporário.',
 ['https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github'])

finding('F-025','Avanços ainda dependem da árvore local; exclusões preexistentes precisam de curadoria','Informativa','preservação/publicação','Aberto',
 ['00_COLAB_IA/02_TRABALHO/auditoria-codex-2026-10-30_v01/git-status-inicial.txt:1','00_COLAB_IA/02_TRABALHO/auditoria-codex-2026-10-30_v01/inventario-inicial.json:1'],
 'Snapshot na dev, HEAD 3b21e65d8b22c454e43ba7dc3b3eb3a039ea061e, main 003a7075a8908011ece83d317d5c700ac2525b58. Instrumentação/Collector/trust e outros avanços estão fora do último commit. Há 34 caminhos rastreados ausentes: as 33 exclusões antigas de aulas Fase 3 e docs/POSTECH - Tech Challenge - Fase 3.pdf.',
 'Outro clone/ArgoCD não recebe esses avanços. Publicar a árvore inteira sem curadoria pode incluir exclusões e artefatos indevidos.',
 'Preservar a árvore e selecionar conscientemente o que comporá um commit quando o usuário autorizar. Não restaurar/apagar as exclusões por suposição; comparar com snapshot da auditoria antes do merge/PR.',
 'Revisão de git diff e da lista do índice, com preservação dos materiais da Fase 4; publicação futura via fluxo autorizado dev → PR → main.',
 ['REQ-OBR-20','REQ-OBR-21','REQ-OBR-22','REQ-OBR-34'],
 'Concorda com F-025, atualiza 33 para 34 ausências já presentes no início desta rodada.',
 'Não commitar é compatível com a instrução do usuário. Isto é risco de preservação e diferença entre local/remoto, não falha disciplinar do agente.')

finding('F-026','Créditos AWS e continuidade do trial PagerDuty permanecem sem prova','Média','incerteza externa','Aberto',
 ['00_COLAB_IA/_ARQUIVO_MORTO/2026-10-30_auditoria-codex/LOG_DE_TRABALHO.md:13','00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/aws/PARECER_AWS_ETAPA8.md:64'],
 'Etapa 8 não consultou Billing/créditos/cotas. Claude registra 12 dias de trial PagerDuty restantes em 2026-10-30, término aproximado 2026-11-11; data exata não conferida na conta. Contas New Relic/Slack/PagerDuty já foram relatadas como criadas. A página pública atual lista Free e integrações/APIs, enquanto a linha de franquia Events da plataforma diz Not included.',
 'Provisionar ou adiar a demonstração apoiado em benefício presumido pode gerar custo ou perda de uma capacidade usada no ensaio.',
 'Conferir plano/créditos/cotas AWS e término/plano efetivo do PagerDuty. Priorizar ensaio completo antes do término informado. Confirmar especificamente Events API/integrador utilizado após trial, sem inferir indisponibilidade absoluta da linha isolada da tabela.',
 'Evidência datada de conta/plano/limites e teste da integração dentro do plano efetivamente disponível; prazo de gravação definido com margem.',
 ['REQ-OBR-03','REQ-OBR-12','REQ-OBR-17','REQ-OBR-30'],
 'Concorda com cautela F-026 e risco de calendário. ⚠️ CONFLITO interpretativo não bloqueante: o registro Claude lê a linha Events como risco de indisponibilidade; Codex não a considera suficiente para afirmar que toda integração Events API do Free termina. Manter [INCERTO] até confirmação da conta/suporte.',
 'Não foi consultada conta SaaS/Billing nesta rodada. Não afirmar elegibilidade nem impossibilidade de usar Free; não propor recriar contas para obter benefícios.',
 ['https://www.pagerduty.com/pricing/'])

finding('F-027','ArgoCD e HPA disputam spec.replicas','Média','defeito de configuração','Aberto',
 ['gitops/base/evaluation-service/deployment.yaml:26','gitops/base/analytics-service/deployment.yaml:24','gitops/base/evaluation-service/hpa.yaml:35','gitops/base/analytics-service/hpa.yaml:31','terraform/k8s/argocd.tf:315'],
 'Os dois Deployments declaram replicas: 1; HPAs podem elevar para 2. A Application ativa automated/selfHeal e não define ignoreDifferences/RespectIgnoreDifferences para réplicas. Render atual confirma os dois pares.',
 'Quando HPA aumentar réplicas, ArgoCD pode identificar desvio e reconciliar para 1, provocando oscilação ou reduzindo capacidade durante carga.',
 'Definir o HPA como responsável por réplicas desses dois Deployments: remover o campo do desejado quando apropriado, ou configurar ignoreDifferences restrito aos dois nomes e RespectIgnoreDifferences=true. Não ignorar réplicas de todos os workloads indiscriminadamente.',
 'Em ensaio de carga no cluster, HPA mantém 2 réplicas durante sincronização ArgoCD, inclusive sync de outra alteração; demais campos seguem reconciliados.',
 ['REQ-OBR-01','REQ-OBR-05'],
 'Novo nesta rodada; não localizado nos relatórios anteriores examinados.',
 'Configuração e comportamento documentado confirmados; oscilação não observada em cluster nesta sessão. HPA não é requisito novo da Fase 4, mas faz parte da base importada.',
 ['https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#respect-ignore-differences-configs'])

finding('F-028','Laboratório publica bancos/cache e APIs sem restringir IP do host','Média','exposição local de configuração','Aberto',
 ['docker-compose.yaml:14','docker-compose.yaml:35','docker-compose.yaml:56','docker-compose.yaml:69','.env.example:22','.env.example:34'],
 'Nove portas publicadas não têm host_ip: PostgreSQL 5433/5434, Redis 6379, DynamoDB 8000 e aplicações 8001–8005. Compose config confirma; somente portas do Collector estão em 127.0.0.1. O ambiente usa credenciais fictícias conhecidas e Redis sem autenticação configurada no Compose.',
 'No padrão do Docker, a publicação alcança interfaces do host além de loopback; outros clientes da rede podem acessar o laboratório quando firewall/roteamento permitirem.',
 'Restringir publicações necessárias a 127.0.0.1 e remover publicações de dados que só precisam de acesso entre contêineres.',
 'Configuração normalizada e inspeção de sockets mostram apenas loopback para portas locais necessárias; testes via localhost continuam funcionando.',
 ['REQ-OBR-04'],
 'Novo nesta rodada; recomendação de segurança do laboratório, não obrigação literal da FIAP.',
 'Não foram iniciados contêineres nem testada exposição real da máquina à rede/internet.',
 ['https://docs.docker.com/engine/network/port-publishing/'])

finding('F-029','CI não renderiza nem valida o conjunto GitOps','Média','lacuna de prevenção de regressão','Aberto',
 ['.github/workflows/compose-integration.yml:22','.github/workflows/terraform-check.yml:30','scripts/validate-all.sh:53','.github/workflows/_ci-go.yml:583','.github/workflows/_ci-python.yml:613'],
 'A renderização kubectl kustomize só existe no script local opcional. Terraform Check é filtrado por terraform/**; o job GitOps usa edit set image, não build/validação do conjunto. Nenhum dos nove workflows chama validate-all.sh ou renderiza o overlay.',
 'Um PR que altera apenas manifests pode passar no Compose e introduzir referência/estrutura GitOps quebrada, descoberta só na sincronização.',
 'Adicionar check local de renderização e validação de schema/contratos de manifests ao CI para mudanças em gitops/** e configuração de charts. Fazer o check requerido no fluxo de revisão.',
 'Um caso controlado com recurso inexistente no kustomization reprova o check; configuração válida renderiza todos os objetos sem acesso ao cluster.',
 ['REQ-OBR-04','REQ-OBR-05','REQ-OBR-20'],
 'Novo nesta rodada; distinto de F-020 (regressão de telemetria).',
 'O estado atual renderizou corretamente; o achado é ausência do gate remoto, não YAML quebrado hoje.')

finding('F-030','Mudanças em políticas compartilhadas não disparam os scans por serviço','Média','lacuna de gatilhos CI','Aberto',
 ['.github/workflows/auth-service.yml:45','.github/workflows/analytics-service.yml:44','.github/workflows/evaluation-service.yml:44','.github/workflows/flag-service.yml:44','.github/workflows/targeting-service.yml:44','.github/workflows/_ci-python.yml:229'],
 'Os filtros push/pull_request listam apenas a pasta do serviço, o workflow chamador e o reutilizável. .trivyignore é consumido por ambos os reutilizáveis e .pylintrc pelo Python, mas nenhum dos dois aparece nesses filtros.',
 'Alterar só exceções Trivy ou configuração Pylint não reexecuta os jobs que consomem a política, reduzindo a evidência de revisão do controle.',
 'Incluir os arquivos compartilhados pertinentes nos filtros ou usar um workflow agregador que determine os serviços afetados; manter build/publicação separados das verificações de política.',
 'PR somente com alteração em .trivyignore roda scans aplicáveis; PR em .pylintrc roda lint dos três serviços Python, sem publicar imagens em PR/dev.',
 ['REQ-OBR-04'],
 'Novo nesta rodada; confirmado pela leitura dos cinco chamadores.',
 'Não foi disparado workflow nem verificada proteção remota da branch.')

finding('F-031','Ensaios Compose herdam variáveis do terminal apesar da promessa de valores fictícios','Média','reprodutibilidade/isolamento','Aberto',
 ['scripts/test-compose.sh:11','scripts/test-observability.sh:12','docker-compose.yaml:82','scripts/integration/test-flow.py:51','scripts/integration/test-traces.py:158'],
 'Scripts limpam SERVICE_API_KEY, mas mantêm MASTER_KEY, DATABASE_URLs, senhas e portas herdadas. Reprodução só com docker compose config e MASTER_KEY sintética no subprocesso confirmou que o valor do terminal sobrepõe .env.example. Os testes usam a chave local fixa.',
 'O ensaio pode falhar com autenticação/portas diferentes e pode colocar parâmetros reais herdados no laboratório. URLs de banco herdadas também podem direcionar conexões fora da composição pretendida.',
 'Isolar o ambiente dos ensaios: sobrescrever explicitamente todas as entradas relevantes com os valores fictícios e validar endpoints/portas; preservar somente variáveis de controle permitidas, como identidade/pasta QA.',
 'Teste de configuração com sentinelas host para MASTER_KEY/URLs/portas confirma que elas não chegam à composição; ensaio continua usando somente dependências locais.',
 ['REQ-OBR-01','REQ-OBR-23'],
 'Novo nesta rodada, com reprodução isolada em validacoes/repro-ambiente-compose.json.',
 'Nenhum segredo real foi exibido/salvo; nenhum contêiner ou conexão a banco foi iniciado. O efeito em configuração foi reproduzido, não um vazamento ocorrido.',
 ['https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/'])

data={'updated':NOW,'agent':'Codex','scope':'Revisao fora dos cinco servicos; nao aplica correcoes de codigo','findings':F,'counts':dict(Counter(f['priority'] for f in F))}
(OUT/'catalogo-achados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Catálogo de achados — auditoria Codex 2026-10-30','',f'TL;DR: {len(F)} registros rastreáveis, dos quais 5 novos (F-027–F-031); F-023 confirmado corrigido no código local. Prioridade Alta significa bloqueio de entrega/publicação, não classificação de vulnerabilidade explorável.','',f'Última atualização: {NOW}, Codex.','', '| ID | Prioridade | Natureza | Estado | Tema |','|---|---|---|---|---|']
for f in F:lines.append(f"| [{f['id']}](#{f['id'].lower()}) | {f['priority']} | {f['kind']} | {f['status']} | {f['title']} |")
for f in F:
    lines += ['',f"<a id=\"{f['id'].lower()}\"></a>",f"## {f['id']} — {f['title']}",'',f"**{f['priority']} · {f['kind']} · {f['status']}**",'',f"**Evidência:** {f['evidence']}",'','**Fontes no snapshot:** '+ '; '.join('`'+x+'`' for x in f['refs'])+'.','',f"**Impacto:** {f['impact']}",'',f"**Correção recomendada:** {f['action']}",'',f"**Aceite:** {f['acceptance']}",'','**Relação FIAP:** '+', '.join(f['requirements'])+'. Não transformar recomendação de implementação em obrigação adicional.', '',f"**Comparação:** {f['comparison']}",'',f"**Limite da conclusão:** {f['limits']}"]
    if f['official_sources']:lines+=['','Documentação primária consultada em 2026-10-30: '+', '.join(f'[fonte {i+1}]({u})' for i,u in enumerate(f['official_sources']))+'.']
(OUT/'CATALOGO_ACHADOS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('catalogo',len(F),data['counts'])
