from pathlib import Path
from urllib.parse import quote
import json

R=Path(__file__).resolve().parents[2]
W=Path(__file__).parent
# Texto literal e página do enunciado; divisão editorial em itens verificáveis.
rows=[
('Manter toda a base das Fases 1, 2 e 3 funcionando.',2,'é obrigatório que toda a base das Fases 1, 2 e 3 esteja funcionando'),
('Manter os cinco microsserviços conteinerizados.',2,'Os 5 microsserviços conteinerizados.'),
('Provisionar a infraestrutura por Terraform.',2,'A infraestrutura provisionada via código (Terraform).'),
('Manter pipelines CI/CD com DevSecOps (GitHub Actions ou similar).',2,'Pipelines de CI/CD (GitHub Actions ou similar) com DevSecOps.'),
('Implantar em Kubernetes gerenciado via GitOps; alternativas citadas: EKS/GKE/AKS e ArgoCD/Flux. Ver Q-01.',2,'Implantação no Kubernetes (EKS, GKE, AKS) gerenciada via GitOps'),
('Provisionar a stack de observabilidade no cluster e acrescentar Helm charts ao repositório GitOps.',3,'adicionando os Helm charts ao seu repositório GitOps'),
('Usar Prometheus para armazenar e consultar métricas de infraestrutura.',3,'Prometheus: para armazenamento e consulta de métricas de infraestrutura.'),
('Usar Loki para centralizar os logs de todos os contêineres do cluster.',3,'Loki: para centralização e indexação de todos os logs dos contêineres do cluster.'),
('Usar Grafana como visualização principal.',3,'Grafana: como ferramenta principal de visualização.'),
('Criar ao menos um dashboard customizado com recursos do cluster, taxa de requisições dos microsserviços e painel de logs em tempo real.',3,'no mínimo, 1 Dashboard customizado'),
('Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM).',4,'receber, processar e exportar suas métricas, logs e traces'),
('Escolher UMA ferramenta APM: Datadog OU New Relic; o PDF orienta contas gratuitas for education. Ver Q-04.',4,'Datadog OU New Relic - use as contas gratuitas for education'),
('Alterar o código-fonte ou Dockerfile dos microsserviços com bibliotecas de instrumentação.',4,'altere o código-fonte ou o Dockerfile dos microsserviços'),
('Gerar tracing distribuído e mostrar no APM o caminho de uma requisição ao evaluation-service.',4,'Ao fazer uma requisição no evaluation-service, o APM deve mostrar o "caminho"'),
('Exibir no APM o mapa de dependências dos cinco microsserviços.',4,'mapa de dependências dos seus 5 microsserviços'),
('Configurar um alerta inteligente no Grafana ou no APM.',5,'configure um alerta inteligente (no Grafana ou APM)'),
('Criar conta no PagerDuty OU OpsGenie e integrar abertura automática de incidente ao alerta.',5,'integre o alerta para abrir um incidente automaticamente'),
('Enviar notificação detalhada de ChatOps a Slack, Discord ou Teams. Ver Q-02.',5,'notificação detalhada para um canal do Slack, Discord ou Teams'),
('Criar automação de Self-Healing que reaja automaticamente ao alerta e tente mitigar sem intervenção humana.',5,'reaja automaticamente ao alerta criado'),
('Entregar no repositório IaC/GitOps atualizado com stack e OTel Collector.',5,'Código IaC/GitOps atualizado para incluir a stack de monitoramento e o OTel Collector.'),
('Entregar código das aplicações atualizado com instrumentação.',5,'Código fonte das aplicações atualizado com a instrumentação.'),
('Entregar scripts ou automações de Self-Healing.',5,'Scripts ou automações criadas para o Self-Healing.'),
('Evidenciar funcionamento prático de todas as métricas, configurações e requisitos; material apenas configurado não basta.',5,'Não basta configurar; é preciso mostrar operando na prática.'),
('Entregar vídeo com duração de até 25 minutos.',5,'Vídeo de Demonstração (até 25 min)'),
('Mostrar no vídeo EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack. [INCERTO]: divergência com alternativas da p. 2; Q-01.',5,'mostre que o cluster EKS (IaC) e o ArgoCD (GitOps) continuam rodando'),
('No vídeo: abrir Grafana, exibir dashboard/métricas, buscar logs no Loki e explicar o roteamento do Collector.',5,'Busque logs no Loki. Explique rapidamente como o OTel Collector está roteando esses dados.'),
('No vídeo: abrir Datadog/New Relic, mostrar Service Map, fazer requisição de teste e exibir trace distribuído detalhado.',6,'Faça uma requisição de teste e exiba o Trace Distribuído detalhado no APM.'),
('No vídeo: causar um problema proposital no sistema.',6,'Cause um problema proposital no sistema'),
('No vídeo: mostrar o alerta em Firing no Grafana/APM.',6,'Mostre o alerta disparando (Firing) no Grafana/APM.'),
('No vídeo: mostrar incidente aberto no PagerDuty/OpsGenie e notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02.',6,'notificação chegando no Slack/Discord'),
('No vídeo: mostrar a automação de Self-Healing acionada e executando a ação corretiva.',6,'Mostre a automação de Self-Healing sendo acionada e executando a ação corretiva'),
('Entregar relatório no formato PDF.',6,'Relatório de Entrega (.PDF)'),
('Incluir nomes, RMs e usernames no relatório.',6,'Nomes, RMs e usernames.'),
('Incluir links do repositório de código e do vídeo no relatório.',6,'Links do repositório de código e do vídeo.'),
('Incluir print do dashboard do Grafana no relatório.',6,'Print do Dashboard do Grafana.'),
('Incluir print de trace distribuído no APM no relatório.',6,'Print de um Trace distribuído no APM.'),
('Incluir print da notificação de incidente no ChatOps no relatório.',6,'Print da notificação de incidente no ChatOps.'),
('Incluir print de log/execução da automação de Self-Healing no relatório.',6,'Print do log/execução da automação de Self-Healing.'),
('Explicar brevemente a arquitetura OTel implementada no relatório.',6,'breve explicação da arquitetura do OTel implementada'),
('Justificar no relatório escolhas Datadog versus New Relic e OpsGenie versus PagerDuty.',6,'escolha entre Datadog vs New Relic e OpsGenie vs PagerDuty'),
('Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03.',2,'em princípio, deve ser desenvolvida em grupo'),
]
bonus=[('Adotar Grafana Alloy como alternativa ao OTel Collector padrão, mantendo as funções centrais de OTel.',4,'O uso do Grafana Alloy no lugar do OTel Collector padrão é opcional.'),('Preferir bibliotecas OpenTelemetry da linguagem na instrumentação; a instrumentação em si continua obrigatória.',4,'preferencialmente utilizando as bibliotecas do OpenTelemetry')]
suggestions=[('Criar matriz de evidências por requisito e ensaiar a demonstração ponta a ponta.','Evita confundir código configurado com funcionamento comprovado; detalhamento autoral da organização da entrega.','Todos'),('Definir janela, duração e contexto do alerta e usar agrupamento/deduplicação.','Reduz ruído e ajuda o alerta inteligente a ser acionável; valores dependem do cenário.','Observabilidade e Monitoramento; Automação de incidentes'),('Vincular logs e traces por identificadores e padronizar nomes dos serviços.','Facilita navegar da falha ao caminho da requisição; esquema exato não é prescrito.','Monitoramento Opensource; APM'),('Dar escopo mínimo e limite de repetição à automação; validar recuperação após cada ação.','Evita ciclos de reinício e efeitos amplos; política de segurança é decisão do projeto.','Automação de incidentes')]
registry={'required':[dict(id=f'REQ-OBR-{i:02}',requirement=r,page=p,quote=q) for i,(r,p,q) in enumerate(rows,1)],'bonus':[dict(id=f'REQ-BON-{i:02}',requirement=r,page=p,quote=q) for i,(r,p,q) in enumerate(bonus,1)],'suggestions':[dict(id=f'SUG-{i:02}',suggestion=s,why=w,module=m) for i,(s,w,m) in enumerate(suggestions,1)]}
(W/'registro-requisitos-2026-09-16_v01.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf8')
t='''# Tech Challenge Fase 4 — Requisitos e mapa de estudo

## 1. TL;DR

Última atualização: 2026-09-16, Codex. Fonte normativa: [enunciado completo](../../POSTECH%20-%20Tech%20Challenge%20-%20Fase%204.pdf), 7 páginas; exigências nas p. 2–6.

O desafio conclui o ToggleMaster com observabilidade e resposta automática a incidentes.
A base funcional das Fases 1, 2 e 3 deve continuar operando: cinco microsserviços, Terraform, CI/CD com DevSecOps e Kubernetes/GitOps.
É preciso ter Prometheus, Loki, Grafana e centralização de métricas, logs e traces por OTel.
Escolha Datadog ou New Relic para instrumentação, tracing distribuído e mapa dos cinco serviços.
Integre alerta, incidente, ChatOps e uma tentativa automática de mitigação (Self-Healing).
Entregue código atualizado, vídeo de até 25 minutos e relatório PDF com prints e justificativas.
Tudo deve ser demonstrado funcionando; ausência de evidência gera desconto.
Este documento contém **41 obrigatórios, 2 opções/preferências do PDF e 4 sugestões autorais**. Todos os requisitos estão **Pendente**: o material de estudo não comprova implantação.
Referências: enunciado, p. 2–6. Páginas 1 e 7 são elementos institucionais, inspecionados visualmente.

## 2. Contexto do problema

**Em linguagem simples:** o sistema entrega software rapidamente, mas a equipe descobre falhas pelos usuários e demora a localizar a causa. A meta é enxergar o problema, avisar as pessoas certas e executar uma tentativa automática de correção. O caso narrado levou 6 horas para a equipe ser avisada e mais 4 para achar a causa nos logs (p. 2–3).

**Tecnicamente:** instrumentar os microsserviços, padronizar coleta/roteamento no OTel, combinar métricas, logs e traces com APM e conectar detecção a resposta ativa. A infraestrutura automatizada anterior continua sendo o substrato do monitoramento (p. 2–4).

## 3. Entregáveis e formato

| Entregável | Conteúdo exigido | Fonte |
|---|---|---|
| Código no repositório | IaC/GitOps com stack/Collector; aplicações instrumentadas; scripts/automações de Self-Healing | p. 5 |
| Vídeo, até 25 min | Stack e base funcionando; Grafana/Loki/OTel; Service Map/trace; falha proposital → Firing → incidente/notificação → execução corretiva | p. 5–6 |
| Relatório PDF | Nomes, RMs, usernames; links do código/vídeo; quatro prints obrigatórios; justificativa OTel/APM/gestão de incidentes | p. 6 |

Não há exigência explícita de entregar um diagrama como arquivo separado. O **Service Map no APM** é obrigatório. Não há no PDF obrigação de README na raiz, formato de nome do vídeo ou relatório, nem plataforma de hospedagem específica.

## 4. Prazo, submissão, avaliação e penalidades

- Atividade obrigatória, vale **90% da nota de todas as disciplinas da fase** (p. 2).
- O PDF pede atenção ao prazo, mas **não informa data/hora limite** (Q-05).
- Não informa plataforma nem procedimento de submissão (Q-06); Discord aparece apenas como canal para dúvidas (p. 6).
- Requisito sem demonstração clara no vídeo ou documentação no relatório sofre **dedução direta de pontos** (p. 5). O valor por item e a rubrica detalhada não são informados (Q-07).
- Os subitens específicos do vídeo e os prints específicos do relatório continuam exigidos. O “ou” na regra geral de evidência não os torna intercambiáveis (leitura conservadora da p. 5–6).
- “Bônus” abaixo é a categoria solicitada para opções/preferências: **o PDF não promete pontuação extra**.

## 5. 🔴 Requisitos obrigatórios

Toda evidência abaixo se refere ao enunciado. Os trechos são curtos; os subitens completos devem ser lidos na página indicada.

| ID | Requisito | Evidência (página + trecho) | Módulo(s) relacionado(s) | Status |
|---|---|---|---|---|
'''
for x in registry['required']: t+=f'| <a id="{x["id"].lower()}"></a>{x["id"]} | {x["requirement"]} | p. {x["page"]}: “{x["quote"]}” | a mapear | Pendente |\n'
t+='''
## 6. 🟢 Bônus — opções e preferência do PDF

**Sem pontuação adicional estabelecida.** Alloy é alternativa ao Collector padrão. As bibliotecas OTel são preferenciais; isso não torna instrumentação ou centralização opcionais.

| ID | Requisito | Evidência (página + trecho) | Módulo(s) relacionado(s) | Status |
|---|---|---|---|---|
'''
for x in registry['bonus']: t+=f'| <a id="{x["id"].lower()}"></a>{x["id"]} | {x["requirement"]} | p. {x["page"]}: “{x["quote"]}” | a mapear | Pendente |\n'
t+='\n## 7. 🔵 Sugestões — autoria Codex, não são exigências FIAP\n\n| ID | Sugestão | Justificativa | Módulo relacionado |\n|---|---|---|---|\n'
for x in registry['suggestions']: t+=f'| <a id="{x["id"].lower()}"></a>{x["id"]} | {x["suggestion"]} | {x["why"]} | {x["module"]} |\n'
t+='''
## 8. Arquitetura e tecnologias citadas

| Papel | Citações do PDF | Classificação |
|---|---|---|
| Base | Cinco microsserviços conteinerizados; Terraform; GitHub Actions ou similar; Kubernetes EKS/GKE/AKS; ArgoCD/Flux | Obrigatório manter as funções da base (p. 2); Q-01 para alternativas |
| Implantação da stack | Helm charts adicionados ao GitOps | Obrigatório (p. 3) |
| Métricas/logs/visualização | Prometheus; Loki; Grafana | Obrigatórios (p. 3) |
| Transporte/roteamento | OTel Collector; Grafana Alloy como alternativa | Collector central obrigatório; distribuição Alloy opcional (p. 4) |
| APM | Datadog OU New Relic | Escolher uma das duas (p. 4) |
| Incidentes | PagerDuty OU OpsGenie | Escolher uma das duas (p. 5) |
| ChatOps | Slack, Discord ou Teams | Um canal; Q-02 para roteiro do vídeo (p. 5–6) |
| Automação | Runbook Automation, AWS Lambda ou GitHub Action via webhook | Alternativas citadas para cumprir resposta automática (p. 5) |

Fluxo conceitual derivado do enunciado (não é configuração pronta): **serviços → OTel → backends de métricas/logs/APM → visualização e alerta → incidente + ChatOps + automação corretiva**. O requisito exige respeitar cada sinal e demonstrar seu trajeto; não implica que todo backend aceite indistintamente qualquer sinal.

**Exemplos, não prescrições:** HTTP 5xx > 5% no `auth-service`; `kubectl rollout restart deployment/auth-service`; parar banco do `flag-service` ou injetar erro. O PDF os rotula como exemplos (p. 5–6). Reiniciar não garante resolver qualquer causa; a tarefa exige mostrar a tentativa corretiva automática.

## 9. Checklist final de entrega

Os checkboxes medem a implementação/entrega futura, não a produção dos guias.

'''
for x in registry['required']: t+=f'- [ ] **{x["id"]}** — {x["requirement"]}\n'
t+='''
## 10. Dúvidas para professor/tutor

| ID | Dúvida [INCERTO] | Evidência e ação |
|---|---|---|
| Q-01 | EKS/ArgoCD são obrigatórios para o vídeo mesmo se a solução usar GKE/AKS ou Flux? | p. 2 permite alternativas; p. 5 nomeia EKS/ArgoCD. REQ-OBR-25 mantido conservadoramente obrigatório. |
| Q-02 | Teams também é aceito na demonstração de ChatOps? | p. 5 inclui Teams; p. 6 menciona Slack/Discord. |
| Q-03 | Entrega individual é aceita e quantos participantes pode ter o grupo? | p. 2: “em princípio” em grupo; não detalha exceções. REQ-OBR-41 conservador. |
| Q-04 | Como obter as contas educacionais de APM e qual alternativa se o acesso não estiver disponível? | p. 4 orienta conta gratuita, sem explicar elegibilidade/procedimento. Disponibilidade externa não verificada. |
| Q-05 | Qual é a data/hora absoluta de entrega? | p. 2 cita prazo sem data. Não transportar prazo da Fase 3. |
| Q-06 | Qual plataforma/procedimento de submissão e configuração de acesso aos links? | Não especificado nas p. 2–6. Discord é canal para dúvidas. |
| Q-07 | Qual a rubrica detalhada e o valor de cada desconto? | p. 2 informa 90%; p. 5 informa dedução sem valores por item. |

Parâmetros como retenção, amostragem, janela do alerta e nomes de atributos são decisões técnicas não fixadas no enunciado; não foram convertidos em requisitos adicionais. Limitações das aulas serão registradas por módulo nos guias e no relatório de revisão.

## 11. Índice dos guias de estudo

A Fase A foi concluída antes da autoria dos guias. Este índice será preenchido no fechamento da Fase B.
'''
dest=R/'docs/requisitos/README.md'; dest.parent.mkdir(parents=True,exist_ok=True)
if dest.exists(): raise SystemExit('README já existe: preservar e revisar manualmente; não sobrescrever pelo gerador.')
dest.write_text(t,encoding='utf8')
print(f'{dest}: {len(rows)} obrigatórios, {len(bonus)} opções/preferências, {len(suggestions)} sugestões; 7 dúvidas.')
