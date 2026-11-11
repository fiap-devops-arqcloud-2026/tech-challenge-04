from pathlib import Path
import json, re
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[3]
DATA=json.loads((ROOT/'docs/gravacao/roteiro-conteudo.json').read_text(encoding='utf-8-sig'))
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
NAVY='#0B172A';TEAL='#007F83';INK='#162D45';MUTED='#50647C';BG='#F4F7FA';MINT='#BFF5E2'
def fill(c,col):c.setFillColor(colors.HexColor(col))
def box(c,x,y,w,h,col):fill(c,col);c.rect(x,y,w,h,stroke=0,fill=1)
def text(c,t,x,y,size=12,col=INK,bold=False):fill(c,col);c.setFont('Arial-Bold' if bold else 'Arial',size);c.drawString(x,y,t)
def para(c,t,x,y,w,size=12,col=INK,bold=False):
 st=ParagraphStyle('p',fontName='Arial-Bold' if bold else 'Arial',fontSize=size,leading=size*1.38,textColor=colors.HexColor(col),spaceAfter=0)
 p=Paragraph(escape(t.replace('–','-').replace('—','-')).replace('\n','<br/>'),st);pw,ph=p.wrap(w,10000);p.drawOn(c,x,y-ph);return y-ph
def base(c,title,sub,page,size=A4):
 w,h=size;box(c,0,0,w,h,BG);box(c,0,h-8,w,8,TEAL);text(c,title,38,h-57,25,NAVY,True);para(c,sub,39,h-77,w-78,11,MUTED);box(c,38,38,w-76,0.6,'#D7E1EA');text(c,'TOGGLEMASTER  |  FASE 4  |  2026-11-10',38,23,8,MUTED);text(c,f'{page:02}',w-58,23,10,TEAL,True)
def lines(c,items,x,y,w,size=13):
 for i,t in enumerate(items,1):
  text(c,str(i),x,y-13,size,TEAL,True);y=para(c,t,x+25,y,w-25,size)-15
 return y

out=ROOT/'docs/gravacao/ROTEIRO_GRAVACAO_2026-11-10_v02.pdf'
c=canvas.Canvas(str(out),pagesize=A4);c.setTitle('ToggleMaster - roteiro de gravacao');c.setAuthor('ToggleMaster')
w,h=A4
box(c,0,0,w,h,NAVY);box(c,44,h-150,6,80,MINT)
text(c,'ToggleMaster',70,h-105,37,'#FFFFFF',True);text(c,'Roteiro de gravação',44,h-205,34,'#FFFFFF',True)
para(c,'Observabilidade e recuperação automática',44,h-245,w-88,22,MINT)
para(c,'21 minutos de roteiro\n+ 4 minutos de margem',44,h-349,w-88,28,'#FFFFFF',True)
para(c,'Em cada cena: tela, ações, sua fala e a evidência que precisa aparecer.',44,h-452,w-88,18,'#FFFFFF')
para(c,'Use o PowerPoint como apoio ao apresentador. O vídeo deve demonstrar as ferramentas operando, e não apenas percorrer slides.',44,h-548,w-88,14,MINT)
para(c,'Fonte: enunciado FIAP, páginas 5 e 6.\nLimite oficial: até 25 minutos. Edição: 2026-11-10.',44,114,w-88,11,'#FFFFFF')
c.showPage()
base(c,'Antes de apertar REC','Checklist de preparação - fora do tempo de gravação',2)
y=lines(c,['Brave: GitHub (README, código, Actions e self-healing), ArgoCD, Grafana (dashboard, Explore/Loki e Alert rules), New Relic (Maps e Distributed tracing), PagerDuty (Incidents) e Slack (#incidentes-tech-challenge).','Lens: Nodes e Pods do cluster correto. É uma interface de inspeção; a prova de GitOps fica no ArgoCD. AWS Console é apoio opcional.','Terminais: A para tráfego; B para pods em watch; C para requisição e falha. Mantenha os túneis 8080, 3000 e 8004 e o tráfego contínuo ativos.','Faça login antes. Grave 20 segundos de teste de áudio e reproduza. Feche notificações pessoais e esconda senhas, .env, Secrets, tokens e páginas de chaves.','Ensaie a cadeia completa. Antes de repetir, aguarde o cooldown de 600 segundos, confira HTTP 200 e alerta Normal. Comandos detalhados em COMANDOS.md.'],42,h-139,w-84,13)
box(c,40,100,w-80,70,NAVY);para(c,'As falas são sugestões. Afirme sucesso somente quando a tela mostrar o resultado. Um teste manual não comprova a reação automática.',55,154,w-110,13,'#FFFFFF')
c.showPage()
for i,s in enumerate(DATA['scenes'],3):
 base(c,f"{s['n']}  {s['title']}",f"{s['time'].replace('–',' - ')}  |  {s['tool']}",i)
 text(c,'O QUE MOSTRAR',40,h-142,10,TEAL,True)
 y=lines(c,s['actions'],42,h-160,w-84,13)
 text(c,'SUA FALA',40,y-15,10,TEAL,True)
 y=para(c,s['speech'],40,y-32,w-80,13)
 y-=24;box(c,40,y-78,w-80,78,NAVY);para(c,s['proof'],54,y-13,w-108,12,'#FFFFFF',True)
 if s['command']:para(c,'Operação: '+s['command'].replace('\n',' / '),40,y-96,w-80,10,MUTED)
 para(c,'Fonte: '+s['source'],40,76,w-80,9,MUTED)
 c.showPage()
base(c,'Feche a entrega com evidências','O relatório PDF exige quatro prints - enunciado, p. 6.',13)
y=lines(c,['Dashboard Grafana: requisições, recursos do cluster e logs com dados. Divida em duas imagens se necessário.','Trace no APM: requisição de entrada, ID, operações e durações. Uma lista de traces não basta.','ChatOps: notificação detalhada do incidente real, com horário e serviço.','Self-healing: execução/log da automação com o disparo automático e a ação corretiva.'],42,h-145,w-84,14)
text(c,'ONDE DEPOSITAR COMPLEMENTOS',40,y-12,10,TEAL,True);y=para(c,'docs/evidencias/entrada-local/\nEntrada local ignorada pelo Git. As capturas só entram na pasta pública datada depois da revisão.',40,y-28,w-80,13)-25
text(c,'ANTES DE SUBMETER',40,y,10,TEAL,True);para(c,'Confirme nomes, RMs, usernames, links do repositório e do vídeo; as justificativas OTel, New Relic e PagerDuty; áudio legível, vídeo até 25 minutos e acesso do avaliador. Não há garantia de nota: qualquer requisito sem demonstração clara pode perder pontos (p. 5).',40,y-20,w-80,13)
c.showPage();c.save()

# Relatório: todas as figuras são capturas autênticas, sem alteração de pixels.
E=ROOT/'docs/evidencias/2026-11-09'
meta=json.loads((ROOT/'docs/relatorio/dados-entrega.json').read_text(encoding='utf-8-sig'))
report=ROOT/'docs/relatorio/RELATORIO_ENTREGA_2026-11-10_v02.pdf'
sz=landscape(A4);w,h=sz;c=canvas.Canvas(str(report),pagesize=sz)
c.setTitle('ToggleMaster - relatório de entrega');c.setAuthor('ToggleMaster')
page=1
repo='https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04'
base(c,'ToggleMaster | Relatório de entrega','Tech Challenge Fase 4 - edição 2026-11-10; evidências de 2026-11-09',page,sz)
y=para(c,meta['status'],40,h-125,w-80,16,TEAL,True)-19
text(c,'PARTICIPANTES',40,y,10,TEAL,True);y-=20
for person in meta['participantes'].split('; '):
 y=para(c,person,40,y,w-80,12)-7
y-=9
y=para(c,'Repositório: '+repo,40,y,w-80,12)-15
c.linkURL(repo,(40,y+10,w-40,y+29),relative=0)
y=para(c,'Vídeo: '+meta['video'],40,y,w-80,12)-18
para(c,'Cinco microsserviços no EKS, infraestrutura por Terraform, entrega por GitHub Actions/ArgoCD e observabilidade com OpenTelemetry, Prometheus, Loki, Grafana e New Relic. PagerDuty e Slack recebem o incidente; GitHub Actions executa a mitigação automática.',40,y,w-80,12)
c.showPage();page+=1

base(c,'Arquitetura e escolhas técnicas','Justificativa solicitada no enunciado FIAP, p. 6.',page,sz)
y=para(c,'O Collector separa a produção de telemetria de seus destinos. Agents em DaemonSet leem logs dos contêineres de cada nó e enviam ao gateway. O gateway, em Deployment, também recebe os traces dos SDKs das aplicações, processa e exporta os sinais. O conector spanmetrics deriva métricas de aplicação dos spans; as métricas de infraestrutura são coletadas diretamente pelo Prometheus nos exporters.',40,h-127,w-80,13)-21
for x,title,body in [(40,'APLICAÇÕES + NÓS','Traces dos SDKs\nLogs dos contêineres'),(300,'COLLECTOR','Agents → gateway\nProcessamento e spanmetrics'),(560,'DESTINOS','New Relic: traces\nLoki: logs / Prometheus: métricas')]:
 box(c,x,y-78,240,78,NAVY);text(c,title,x+12,y-21,12,MINT,True);para(c,body,x+12,y-34,215,10,'#FFFFFF')
text(c,'→',282,y-44,18,TEAL,True);text(c,'→',542,y-44,18,TEAL,True);y-=100
y=para(c,'New Relic, em vez de Datadog: a escolha priorizou a integração OTLP configurada no projeto, a investigação por traces distribuídos e a visualização de dependências. O trace capturado contém os cinco serviços. Não foi realizado benchmark comparativo entre fornecedores.',40,y,w-80,12)-16
y=para(c,'PagerDuty, em vez de OpsGenie: a implementação usa Events API V2, abertura/resolução do incidente e comunicação com Slack. O disparo de self-healing parte do Grafana para o GitHub por repository_dispatch; não depende de um clique de um operador no PagerDuty.',40,y,w-80,12)-16
para(c,'Implementação: gitops/observability/values, grafana/alerting e scripts/self-healing. O agent exclui logs dos próprios Collectors para evitar retroalimentação; a cobertura não deve ser descrita como irrestrita. Dois agents e um gateway foram observados no ensaio de 2026-11-09.',40,y,w-80,10,MUTED)
c.showPage();page+=1

base(c,'Ensaio integrado: falha e recuperação','Execução real em 2026-11-09. Horários abaixo em America/Sao_Paulo (UTC-03).',page,sz)
timeline=[('15:57:23','Falha ativada','POST autenticado /admin/fault; rotas de flags passam a responder 503.'),('15:59:20','Alerta Firing','FlagService5xxAlto confirma a condição; notificações às 15:59:30.'),('15:59:39','Ação automática','repository_dispatch → OIDC → rollout restart de flag-service.'),('16:00:03','Rollout completo','Novo pod assume; HTTP 200 observado às 16:00:19.'),('16:01:30','Resolved','Notificação de resolução; incidente PagerDuty #4 resolvido.')]
y=h-137
for time,title,desc in timeline:
 text(c,time,40,y-13,13,TEAL,True);text(c,title,150,y-13,13,INK,True);para(c,desc,150,y-23,w-190,11,MUTED);y-=66
para(c,'Run 42679005683: sucesso em 43 segundos. O log registra restart e rollout, sem recuperação manual. O incidente teve duração exibida de 2 minutos no PagerDuty. Os tempos acima são pontos observados, não uma garantia de tempo de resposta futuro.',40,y,w-80,11)
c.linkURL(meta['run_url'],(40,64,w-40,88),relative=0);text(c,'Abrir a execução automática no GitHub Actions',40,73,11,TEAL,True)
c.showPage();page+=1

figs=[
 ('01-grafana-requisicoes.png','01 | Grafana: requisições e latência','Dashboard customizado com dados reais de 2026-11-09. O gráfico de erros estava com escala automática inadequada quando zerado; a captura histórica foi preservada. Analytics tem fluxo assíncrono, diferente dos serviços HTTP.'),
 ('01-grafana-recursos-logs.png','01 | Grafana: recursos e logs','Continuação do mesmo dashboard: CPU/memória dos pods e logs consultados no Loki. A imagem complementa a visão das requisições e documenta os itens do dashboard solicitados na p. 3.'),
 ('02-trace-spans.png','02 | Trace distribuído no New Relic','GET /evaluate em 2026-11-09 18:28:05 UTC (15:28:05 UTC-03). Trace 2ad625552c9917f6aa53c27567f49835: 19 spans; operações expandidas para análise das chamadas e durações.'),
 ('02-trace-mapa.png','02 | Dependências da execução','A mesma execução apresenta 19 spans, 10 entidades e duração total de 56,63 ms. Este é o mapa associado ao trace; não substitui o enquadramento do Service Map global exigido na demonstração em vídeo.'),
 ('03-chatops.png','03 | Notificação no ChatOps',meta['chatops']),
 ('04-self-healing.png','04 | Disparo automático e resultado','GitHub Actions: evento repository_dispatch, execução 42679005683 concluída com sucesso em 43 segundos. A próxima imagem mostra a ação corretiva, além do resultado geral.'),
 ('04-self-healing-log.png','04 | Log da ação corretiva',meta['selfhealing']),
 ('05-argocd.png','Apoio | GitOps em operação','Seis Applications Synced/Healthy na consulta de 2026-11-09: togglemaster, observability, kube-prometheus-stack, Loki, otel-gateway e otel-agent. Evidência adicional; não substitui o ensaio do incidente.')
]
for fn,title,caption in figs:
 base(c,title,'Captura autêntica de 2026-11-09 - fonte: ferramenta indicada na imagem.',page,sz)
 f=E/fn
 if not f.exists(): raise FileNotFoundError(f)
 im=ImageReader(str(f));iw,ih=im.getSize();scale=min((w-80)/iw,345/ih)
 dw,dh=iw*scale,ih*scale;c.drawImage(im,(w-dw)/2,h-121-dh,width=dw,height=dh,mask='auto')
 para(c,caption,40,112,w-80,11,MUTED)
 c.showPage();page+=1

base(c,'Cobertura e fechamento da entrega','Base documental: enunciado FIAP, páginas 2 a 6.',page,sz)
items=[
 'Base e observabilidade: cinco serviços, Terraform, pipelines, GitOps, dashboard e traces foram documentados com fontes de código e capturas do ambiente. O vídeo ainda deve mostrar esses elementos funcionando.',
 'Incidente: a falha proposital gerou Firing, PagerDuty/Slack, repository_dispatch e restart automático; houve recuperação HTTP 200 e resolução. Não foi necessário executar recuperação manual.',
 'Limites das capturas: o ChatOps mostra Resolved, com erro de formatação do resumo preservado. O ajuste do template e da escala do gráfico é rastreável no GitOps. A imagem do mapa é do trace, não do Service Map global.',
 'Antes de gravar: confirmar Service Map com os cinco serviços, estado atual saudável, tráfego, logins e cooldown de 600 s. Não mostrar tokens, Secrets ou variáveis com valores sensíveis.',
 'Antes de submeter: gravar vídeo até 25 minutos, testar áudio e acesso do avaliador, inserir sua URL neste relatório e no README. Os nomes, RMs, usernames, repositório, prints e justificativas já estão incluídos.'
]
lines(c,items,40,h-132,w-80,12)
para(c,'A FIAP exige evidência clara do funcionamento; este relatório não garante nota nem substitui o vídeo (enunciado, p. 5-6).',40,80,w-80,10,MUTED)
c.showPage();c.save()
print(json.dumps({'roteiro':str(out),'relatorio':str(report),'paginas_relatorio':page},ensure_ascii=True))

