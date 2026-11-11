# Tech Challenge Fase 4 — Requisitos e mapa de estudo

## 1. TL;DR

Última atualização: 2026-11-11. Fonte normativa: [enunciado completo](../../POSTECH%20-%20Tech%20Challenge%20-%20Fase%204.pdf), 7 páginas; exigências nas p. 2–6.

O desafio conclui o ToggleMaster com observabilidade e resposta automática a incidentes.
A base funcional das Fases 1, 2 e 3 deve continuar operando: cinco microsserviços, Terraform, CI/CD com DevSecOps e Kubernetes/GitOps.
É preciso ter Prometheus, Loki, Grafana e centralização de métricas, logs e traces por OTel.
Escolha Datadog ou New Relic como APM para exibir o tracing distribuído e o mapa dos cinco serviços; a instrumentação é feita no código ou no Dockerfile, preferencialmente com bibliotecas OpenTelemetry.
Integre alerta, incidente, ChatOps e uma tentativa automática de mitigação (Self-Healing).
Entregue código atualizado, vídeo de até 25 minutos e relatório PDF com prints e justificativas.
Tudo deve ser demonstrado funcionando; ausência de evidência gera desconto.
Este documento contém **42 obrigatórios, 2 bônus (opções/preferências do PDF, sem pontuação extra prometida) e 4 sugestões autorais**. O estado abaixo distingue código implementado, funcionamento evidenciado no ensaio de **2026-11-09** e na gravação de **2026-11-11**, preparação documental e entrega pendente. Material de estudo, teste local e código existente não equivalem a vídeo entregue.
Referências: enunciado, p. 2–6. Páginas 1 e 7 são elementos institucionais, inspecionados visualmente.


### Estado da entrega em 2026-11-11

A cadeia **503 → Grafana Firing → PagerDuty/Slack → Actions → restart → HTTP 200** foi executada no ensaio de 2026-11-09 e de novo na gravação de 2026-11-11 ([execução 42956432177](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42956432177)): da falha à volta do HTTP 200 em 2 min 50 s, sem intervenção humana. [Índice de evidências](../evidencias/README.md). O trace capturado tem 19 spans; o Service Map global foi mostrado no vídeo (relato do usuário). A coleta dos logs dos próprios Collectors entra no cluster com o merge de 2026-11-11.

O vídeo foi gravado em 2026-11-11 pelo [roteiro](../gravacao/README.md); falta publicá-lo e incluir o link. O [relatório v03](../relatorio/README.md) reúne identificação, os quatro prints, a linha do tempo da gravação e as justificativas, e fica pronto para submissão quando o link entrar.

**Leitura dos status:** “Evidenciado” vale para a prova datada indicada; “Implementado” descreve código/configuração; “Preparado” descreve material de entrega; “Pendente” exige ação antes da submissão. Os checkboxes do final seguem esses limites e não estimam nota.

## 2. Contexto do problema

**Em linguagem simples:** num fim de semana, um serviço passou a falhar sem gerar aviso; a equipe só soube pelos usuários 6 horas depois e levou mais 4 horas para achar a causa nos logs espalhados pelos pods (p. 2–3). A meta é enxergar o problema, avisar as pessoas certas e executar uma tentativa automática de correção.

**Tecnicamente:** instrumentar os microsserviços, padronizar coleta/roteamento no OTel, combinar métricas, logs e traces com APM e conectar detecção a resposta ativa. A infraestrutura automatizada anterior continua sendo o substrato do monitoramento (p. 2–4). O evaluation-service falhou silenciosamente e o HPA escalou recursos para compensar (p. 2). O objetivo declarado é “Observabilidade Total e Resposta Ativa”: trace para lentidão, logs centralizados para erro, acionamento por PagerDuty/OpsGenie ao atingir um limite e Self-Healing (p. 3).

## 3. Entregáveis e formato

| Entregável | Conteúdo exigido | Fonte |
|---|---|---|
| Código no repositório | IaC/GitOps com stack/Collector; aplicações instrumentadas; scripts/automações de Self-Healing | p. 5 |
| Vídeo, até 25 min | Cluster EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack (Q-01); Grafana com dashboard, busca no Loki e explicação do roteamento OTel; Service Map, requisição de teste e trace distribuído; falha proposital → Firing → incidente/notificação → execução corretiva | p. 5–6 |
| Relatório PDF | Nomes, RMs, usernames; links do código/vídeo; quatro prints obrigatórios; justificativa OTel/APM/gestão de incidentes | p. 6 |

Não há exigência explícita de entregar um diagrama como arquivo separado. O **Service Map no APM** é obrigatório. Não há no PDF obrigação de README na raiz, formato de nome do vídeo ou relatório, nem plataforma de hospedagem específica.

## 4. Prazo, submissão, avaliação e penalidades

- Atividade obrigatória, vale **90% da nota de todas as disciplinas da fase** (p. 2).
- O PDF pede atenção ao prazo, mas **não informa data/hora limite** (Q-05).
- Não informa plataforma nem procedimento de submissão (Q-06). Como canal de contato com a FIAP, o Discord aparece apenas para dúvidas (p. 6); nas p. 5–6 ele também é opção de ChatOps.
- Requisito sem demonstração clara no vídeo ou documentação no relatório sofre **dedução direta de pontos** (p. 5). O valor por item e a rubrica detalhada não são informados (Q-07).
- O PDF lista itens específicos para o vídeo (p. 5–6) e para o relatório (p. 6), e a regra geral fala em demonstração “no vídeo ou” documentação “no relatório” (p. 5). [INCERTO]: por leitura conservadora, este documento trata os dois conjuntos como exigidos; Q-11.
- “Bônus” abaixo é a categoria solicitada para opções/preferências: **o PDF não promete pontuação extra**.

## 5. 🔴 Requisitos obrigatórios

Toda evidência abaixo se refere ao enunciado. Os trechos são curtos; os subitens completos devem ser lidos na página indicada.

O PDF rotula como “(Obrigatório)” apenas o OTel Collector (p. 4), o Self-Healing (p. 5) e as Evidências Visuais (p. 6). Os demais itens também são obrigatórios: usam linguagem imperativa (“deve”, “crie”, “configure”, “escolha”) e a REGRA DE AVALIAÇÃO (p. 5) exige evidenciar todos os requisitos, com dedução direta de pontos.

| ID | Requisito | Evidência (página + trecho) | Módulo(s) relacionado(s) | Status |
|---|---|---|---|---|
| <a id="req-obr-01"></a>REQ-OBR-01 | Manter toda a base das Fases 1, 2 e 3 funcionando. | p. 2: “é obrigatório que toda a base das Fases 1, 2 e 3 esteja funcionando” | 00 — Welcome; 02 — Monitoramento Opensource | Evidenciado no ensaio (2026-11-09) e na gravação (2026-11-11): dois nós Ready e seis Applications Synced/Healthy — [evidências](../evidencias/README.md) |
| <a id="req-obr-02"></a>REQ-OBR-02 | Manter os cinco microsserviços conteinerizados. | p. 2: “Os 5 microsserviços conteinerizados.” | 02 — Monitoramento Opensource; 03 — APM | Evidenciado: cinco serviços no EKS e nos spans — [evidências](../evidencias/README.md) |
| <a id="req-obr-03"></a>REQ-OBR-03 | Provisionar a infraestrutura por Terraform. | p. 2: “A infraestrutura provisionada via código (Terraform).” | Fases 1–3 (base anterior) | Implementado: três raízes Terraform; mostrar IaC junto ao EKS no vídeo — [código](../../terraform/README.md) |
| <a id="req-obr-04"></a>REQ-OBR-04 | Manter pipelines CI/CD com DevSecOps (GitHub Actions ou similar). | p. 2: “Pipelines de CI/CD (GitHub Actions ou similar) com DevSecOps.” | Fases 1–3 (base anterior) | Implementado: CI/CD, SAST, SCA e scan de imagem — [workflows](../CI-CD.md); resultado da revisão corrente no PR |
| <a id="req-obr-05"></a>REQ-OBR-05 | Implantar no Kubernetes (EKS, GKE ou AKS), com a implantação gerenciada via GitOps (ArgoCD/Flux). Ver Q-01. | p. 2: “Implantação no Kubernetes (EKS, GKE, AKS) gerenciada via GitOps” | 02 — Monitoramento Opensource; 04 — Automação de incidentes | Evidenciado: EKS e seis Applications Synced/Healthy em 2026-11-09 — [evidências](../evidencias/README.md) |
| <a id="req-obr-06"></a>REQ-OBR-06 | Provisionar a stack de observabilidade no cluster e acrescentar Helm charts ao repositório GitOps. | p. 3: “adicionando os Helm charts ao seu repositório GitOps” | 02 — Monitoramento Opensource | Evidenciado: stack no cluster e Applications Helm versionadas — [GitOps](../../gitops/observability/applications) |
| <a id="req-obr-07"></a>REQ-OBR-07 | Usar Prometheus para armazenar e consultar métricas de infraestrutura. | p. 3: “Prometheus: para armazenamento e consulta de métricas de infraestrutura.” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource | Evidenciado: métricas de recursos no Grafana/Prometheus — [evidências](../evidencias/README.md) |
| <a id="req-obr-08"></a>REQ-OBR-08 | Usar Loki para centralizar e indexar todos os logs dos contêineres do cluster. | p. 3: “Loki: para centralização e indexação de todos os logs dos contêineres do cluster.” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Implementado; a coleta dos logs dos próprios Collectors entra no cluster com o merge de 2026-11-11 e ainda precisa de consulta no Loki — [agent](../../gitops/observability/values/otel-agent.yaml) |
| <a id="req-obr-09"></a>REQ-OBR-09 | Usar Grafana como visualização principal. | p. 3: “Grafana: como ferramenta principal de visualização.” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Evidenciado: Grafana usado para métricas, logs e alertas — [evidências](../evidencias/README.md) |
| <a id="req-obr-10"></a>REQ-OBR-10 | Criar no Grafana ao menos um dashboard customizado que centralize a saúde do ecossistema: (a) uso de recursos do cluster; (b) taxa de requisições dos microsserviços; (c) painel de logs em tempo real. | p. 3: “no mínimo, 1 Dashboard customizado” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Evidenciado: dashboard customizado com recursos, requisições e logs — [evidências](../evidencias/README.md) |
| <a id="req-obr-11"></a>REQ-OBR-11 | Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM). Ver Q-08. | p. 4: “receber, processar e exportar suas métricas, logs e traces” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Evidenciado nos três destinos; métricas de aplicação derivadas dos spans no gateway — [arquitetura](../ARQUITETURA.md) |
| <a id="req-obr-12"></a>REQ-OBR-12 | Escolher UMA ferramenta APM: Datadog OU New Relic; o PDF orienta contas gratuitas for education. Ver Q-04. | p. 4: “Datadog OU New Relic - use as contas gratuitas for education” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | New Relic em uso e com trace; enquadramento da conta education não comprovado (Q-04) |
| <a id="req-obr-13"></a>REQ-OBR-13 | Alterar o código-fonte ou Dockerfile dos microsserviços com bibliotecas de instrumentação. | p. 4: “altere o código-fonte ou o Dockerfile dos microsserviços” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Implementado e evidenciado nos cinco serviços — [instrumentação](../../observability/README.md) |
| <a id="req-obr-14"></a>REQ-OBR-14 | Gerar tracing distribuído e mostrar no APM o caminho de uma requisição ao evaluation-service. | p. 4: “Ao fazer uma requisição no evaluation-service, o APM deve mostrar o "caminho"” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Evidenciado: GET /evaluate, 19 spans, cinco serviços — [evidências](../evidencias/README.md) |
| <a id="req-obr-15"></a>REQ-OBR-15 | Exibir no APM o mapa de dependências dos cinco microsserviços. | p. 4: “mapa de dependências dos seus 5 microsserviços” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Gravado no vídeo de 2026-11-11 (relato do usuário); o relatório traz o mapa de entidades do trace — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-16"></a>REQ-OBR-16 | Configurar um alerta inteligente no Grafana ou no APM. | p. 5: “configure um alerta inteligente (no Grafana ou APM)” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM; 04 — Automação de incidentes | Evidenciado: FlagService5xxAlto entrou em Firing — [evidências](../evidencias/README.md) |
| <a id="req-obr-17"></a>REQ-OBR-17 | Criar conta no PagerDuty OU OpsGenie e integrar o alerta para abrir incidente automaticamente, com a ferramenta acionando o time (objetivo da p. 3). Ver Q-09. | p. 5: “integre o alerta para abrir um incidente automaticamente” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 03 — APM; 04 — Automação de incidentes | Evidenciado: PagerDuty abriu e resolveu incidente #4 — [evidências](../evidencias/README.md) |
| <a id="req-obr-18"></a>REQ-OBR-18 | Enviar notificação detalhada de ChatOps a Slack, Discord ou Teams. Ver Q-02. | p. 5: “notificação detalhada para um canal do Slack, Discord ou Teams” | 01 — Observabilidade e Monitoramento; 03 — APM; 04 — Automação de incidentes | Evidenciado: Slack recebeu Firing/Resolved; correção do texto da annotation preparada — [evidências](../evidencias/README.md) |
| <a id="req-obr-19"></a>REQ-OBR-19 | Criar automação de Self-Healing que reaja automaticamente ao alerta e tente mitigar sem intervenção humana. | p. 5: “reaja automaticamente ao alerta criado” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM; 04 — Automação de incidentes | Evidenciado: dispatch automático, restart e recuperação sem intervenção — [run automático](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42679005683) |
| <a id="req-obr-20"></a>REQ-OBR-20 | Entregar no repositório IaC/GitOps atualizado com stack e OTel Collector. | p. 5: “Código IaC/GitOps atualizado para incluir a stack de monitoramento e o OTel Collector.” | 02 — Monitoramento Opensource | Implementado no repositório — [IaC](../../terraform) e [stack GitOps](../../gitops/observability) |
| <a id="req-obr-21"></a>REQ-OBR-21 | Entregar código das aplicações atualizado com instrumentação. | p. 5: “Código fonte das aplicações atualizado com a instrumentação.” | 03 — APM | Implementado no repositório — [serviços instrumentados](../../services) |
| <a id="req-obr-22"></a>REQ-OBR-22 | Entregar scripts ou automações de Self-Healing. | p. 5: “Scripts ou automações criadas para o Self-Healing.” | 04 — Automação de incidentes | Implementado e executado — [script](../../scripts/self-healing/restart.sh) e [workflow](../../.github/workflows/self-healing.yml) |
| <a id="req-obr-23"></a>REQ-OBR-23 | Evidenciar funcionamento prático de todas as métricas, configurações e requisitos; material apenas configurado não basta. | p. 5: “Não basta configurar; é preciso mostrar operando na prática.” | 00 — Welcome; 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM; 04 — Automação de incidentes | Parcial: evidências reais disponíveis; falta consolidar vídeo, mapa global e cobertura ampliada de logs |
| <a id="req-obr-24"></a>REQ-OBR-24 | Entregar vídeo com duração de até 25 minutos. | p. 5: “Vídeo de Demonstração (até 25 min)” | Entrega (transversal) | Gravado em 2026-11-11 (relato do usuário); falta publicar o vídeo e incluir o link — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-25"></a>REQ-OBR-25 | Mostrar no vídeo EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack. [INCERTO]: divergência com alternativas da p. 2; Q-01. | p. 5: “mostre que o cluster EKS (IaC) e o ArgoCD (GitOps) continuam rodando” | Fases 1–3 (base anterior) | Gravado em 2026-11-11 (relato do usuário) — [roteiro](../gravacao/README.md) |
| <a id="req-obr-26"></a>REQ-OBR-26 | No vídeo: (a) abrir o Grafana; (b) exibir o dashboard customizado com as métricas; (c) buscar logs no Loki; (d) explicar como o Collector roteia esses dados. | p. 5: “Busque logs no Loki. Explique rapidamente como o OTel Collector está roteando esses dados.” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource | Gravado em 2026-11-11 (relato do usuário); dashboard e logs também no relatório — [roteiro](../gravacao/README.md) |
| <a id="req-obr-27"></a>REQ-OBR-27 | No vídeo: (a) abrir o painel do Datadog/New Relic e mostrar o Service Map; (b) fazer uma requisição de teste; (c) exibir o trace distribuído detalhado. | p. 6: “Faça uma requisição de teste e exiba o Trace Distribuído detalhado no APM.” | 03 — APM | Gravado em 2026-11-11 (relato do usuário); trace também no relatório — [roteiro](../gravacao/README.md) |
| <a id="req-obr-28"></a>REQ-OBR-28 | No vídeo: causar um problema proposital no sistema. | p. 6: “Cause um problema proposital no sistema” | 03 — APM; 04 — Automação de incidentes | Evidenciado na gravação: falha ativada às 00:58:48 e 159 respostas 503 nos logs do Loki — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-29"></a>REQ-OBR-29 | No vídeo: mostrar o alerta em Firing no Grafana/APM. | p. 6: “Mostre o alerta disparando (Firing) no Grafana/APM.” | 03 — APM; 04 — Automação de incidentes | Evidenciado na gravação: Firing às 01:00:50, registrado no Slack — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-30"></a>REQ-OBR-30 | No vídeo: (a) mostrar o incidente sendo aberto no PagerDuty/OpsGenie; (b) mostrar a notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02. | p. 6: “notificação chegando no Slack/Discord” | 03 — APM; 04 — Automação de incidentes | Evidenciado na gravação: incidente do PagerDuty e alerta do Grafana no Slack às 01:01 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-31"></a>REQ-OBR-31 | No vídeo: mostrar a automação de Self-Healing acionada e executando a ação corretiva. | p. 6: “Mostre a automação de Self-Healing sendo acionada e executando a ação corretiva” | 02 — Monitoramento Opensource; 04 — Automação de incidentes | Evidenciado na gravação: [execução 42956432177](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42956432177), restart às 01:01:09 e HTTP 200 às 01:01:38 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-32"></a>REQ-OBR-32 | Entregar relatório no formato PDF. | p. 6: “Relatório de Entrega (.PDF)” | Entrega (transversal) | Relatório v03 em PDF pronto; a submissão depende do link do vídeo — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-33"></a>REQ-OBR-33 | Incluir nomes, RMs e usernames no relatório. | p. 6: “Nomes, RMs e usernames.” | Entrega (transversal) | Cinco participantes com nome, RM e username na capa do PDF v03 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-34"></a>REQ-OBR-34 | Incluir links do repositório de código e do vídeo no relatório. | p. 6: “Links do repositório de código e do vídeo.” | Entrega (transversal) | Parcial: link do repositório no PDF v03; URL do vídeo pendente — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-35"></a>REQ-OBR-35 | Incluir print do dashboard do Grafana no relatório. | p. 6: “Print do Dashboard do Grafana.” | 02 — Monitoramento Opensource; 03 — APM | Incluído no relatório v03, p. 6–7 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-36"></a>REQ-OBR-36 | Incluir print de trace distribuído no APM no relatório. | p. 6: “Print de um Trace distribuído no APM.” | 03 — APM | Incluído no relatório v03, p. 8–9 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-37"></a>REQ-OBR-37 | Incluir print da notificação de incidente no ChatOps no relatório. | p. 6: “Print da notificação de incidente no ChatOps.” | 04 — Automação de incidentes | Incluído no relatório v03, p. 10, com as mensagens da gravação — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-38"></a>REQ-OBR-38 | Incluir print de log/execução da automação de Self-Healing no relatório. | p. 6: “Print do log/execução da automação de Self-Healing.” | 04 — Automação de incidentes | Incluído no relatório v03, p. 11–12, com o log da gravação — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-39"></a>REQ-OBR-39 | Explicar brevemente a arquitetura OTel implementada no relatório. | p. 6: “breve explicação da arquitetura do OTel implementada” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Incluído no relatório v03, p. 3 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-40"></a>REQ-OBR-40 | Justificar no relatório escolhas Datadog versus New Relic e OpsGenie versus PagerDuty. | p. 6: “escolha entre Datadog vs New Relic e OpsGenie vs PagerDuty” | 03 — APM; 04 — Automação de incidentes | Incluído no relatório v03, p. 4 — [relatório v03](../relatorio/README.md) |
| <a id="req-obr-41"></a>REQ-OBR-41 | Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03. | p. 2: “em princípio, deve ser desenvolvida em grupo” | Entrega (transversal) | Cinco participantes identificados conforme orientação do usuário; regra de grupo continua dependente do tutor (Q-03) |
| <a id="req-obr-42"></a>REQ-OBR-42 | Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06. | p. 2: “Importante atentar-se ao prazo de entrega” | Entrega (transversal) | Pendente: confirmar prazo/canal oficiais e submeter código, vídeo e relatório (Q-05/Q-06) |

## 6. 🟢 Bônus — opções e preferência do PDF

**Sem pontuação adicional estabelecida.** Alloy é alternativa ao Collector padrão. As bibliotecas OTel são preferenciais; isso não torna instrumentação ou centralização opcionais.

| ID | Requisito | Evidência (página + trecho) | Módulo(s) relacionado(s) | Status |
|---|---|---|---|---|
| <a id="req-bon-01"></a>REQ-BON-01 | Adotar Grafana Alloy como alternativa ao OTel Collector padrão, mantendo as funções centrais de OTel. Ver Q-10. | p. 4: “O uso do Grafana Alloy no lugar do OTel Collector padrão é opcional.” | 00 — Welcome; 02 — Monitoramento Opensource | Não adotado: Collector padrão atende a escolha do projeto |
| <a id="req-bon-02"></a>REQ-BON-02 | Preferir bibliotecas OpenTelemetry da linguagem na instrumentação; a instrumentação em si continua obrigatória. Ver Q-08. | p. 4: “preferencialmente utilizando as bibliotecas do OpenTelemetry” | 01 — Observabilidade e Monitoramento; 02 — Monitoramento Opensource; 03 — APM | Implementado: SDKs OpenTelemetry Go/Python nos cinco serviços |

## 7. 🔵 Sugestões — não são exigências FIAP

| ID | Sugestão | Justificativa | Módulo relacionado |
|---|---|---|---|
| <a id="sug-01"></a>SUG-01 | Criar matriz de evidências por requisito e ensaiar a demonstração ponta a ponta. | Evita confundir código configurado com funcionamento comprovado; detalhamento autoral da organização da entrega. | Todos |
| <a id="sug-02"></a>SUG-02 | Definir janela, duração e contexto do alerta e usar agrupamento/deduplicação. | Reduz ruído e ajuda o alerta inteligente a ser acionável; valores dependem do cenário. | Observabilidade e Monitoramento; Automação de incidentes |
| <a id="sug-03"></a>SUG-03 | Vincular logs e traces por identificadores e padronizar nomes dos serviços. | Facilita navegar da falha ao caminho da requisição; esquema exato não é prescrito. | Monitoramento Opensource; APM |
| <a id="sug-04"></a>SUG-04 | Dar escopo mínimo e limite de repetição à automação; validar recuperação após cada ação. | Evita ciclos de reinício e efeitos amplos; política de segurança é decisão do projeto. | Automação de incidentes |

## 8. Arquitetura e tecnologias citadas

| Papel | Citações do PDF | Classificação |
|---|---|---|
| Base | Cinco microsserviços conteinerizados; Terraform; GitHub Actions ou similar; Kubernetes EKS/GKE/AKS; ArgoCD/Flux | Obrigatório manter as funções da base (p. 2); Q-01 para alternativas |
| Implantação da stack | Helm charts adicionados ao GitOps | Obrigatório (p. 3) |
| Métricas/logs/visualização | Prometheus; Loki; Grafana | Obrigatórios (p. 3) |
| Transporte/roteamento | OTel Collector; Grafana Alloy como alternativa | Collector como peça central é obrigatório; Alloy no lugar do Collector padrão é opcional (p. 4) |
| APM | Datadog OU New Relic | Escolher uma das duas (p. 4) |
| Incidentes | PagerDuty OU OpsGenie | Escolher uma das duas (p. 5) |
| ChatOps | Slack, Discord ou Teams | Um canal; Q-02 para roteiro do vídeo (p. 5–6) |
| Automação | Runbook Automation, AWS Lambda ou GitHub Action via webhook | Alternativas citadas para cumprir resposta automática (p. 5) |
| Instrumentação | Código-fonte ou Dockerfile; bibliotecas OpenTelemetry da linguagem | Instrumentação obrigatória; bibliotecas OTel preferenciais (p. 4) |
| Visibilidade no APM | Distributed Tracing (requisição no evaluation-service); Service Map dos 5 microsserviços | Obrigatórios (p. 4) |
| Contexto do incidente narrado | evaluation-service; HPA | Contexto, não requisito (p. 2) |

Fluxo conceitual derivado do enunciado (não é configuração pronta): **serviços → OTel → backends de métricas/logs/APM → visualização e alerta → incidente + ChatOps + automação corretiva**. O PDF exige que o Collector roteie os sinais aos backends corretos (p. 4), que o roteamento seja explicado no vídeo (p. 5) e que a arquitetura OTel seja explicada no relatório (p. 6); isso não implica que todo backend aceite indistintamente qualquer sinal.

**Exemplos, não prescrições:** HTTP 5xx > 5% no `auth-service`; `kubectl rollout restart deployment/auth-service`; parar banco do `flag-service` ou injetar erro. O PDF os rotula como exemplos (p. 5–6), assim como “mostrando o pod reiniciando automaticamente via terminal” (p. 6). Reiniciar não garante resolver qualquer causa; a tarefa exige mostrar a tentativa corretiva automática.

Os exemplos não formam, sozinhos, um cenário único: o alerta e a reinicialização citam o `auth-service` (p. 5), e a falha proposital cita o `flag-service` (p. 6). Pela sequência da p. 6 e pelo vínculo da automação “ao alerta criado” (p. 5), a falha escolhida para o vídeo deve acionar o alerta configurado. [INCERTO]; Q-12.

**Disciplinas indicadas pelo PDF:** bloco 1 (p. 3) Prometheus, Grafana, Loki, Observabilidade no Kubernetes; bloco 2 (p. 4) OpenTelemetry (OTel) e Alloy; bloco 3 (p. 4) APM, Instrumentação, Datadog ou New Relic; bloco 4 (p. 4) Alert Fatigue, PagerDuty/OpsGenie, ChatOps, Runbook Automation, Self-Healing.

## 9. Checklist final de entrega

Marcação em 2026-11-11: itens assinalados têm implementação/execução indicada na matriz. Publicação do vídeo, link no PDF, cobertura ampliada de logs e prazo oficial ficam abertos até a prova correspondente; isso não representa uma previsão de nota.

- [x] **REQ-OBR-01** — Manter toda a base das Fases 1, 2 e 3 funcionando.
- [x] **REQ-OBR-02** — Manter os cinco microsserviços conteinerizados.
- [ ] **REQ-OBR-03** — Provisionar a infraestrutura por Terraform.
- [ ] **REQ-OBR-04** — Manter pipelines CI/CD com DevSecOps (GitHub Actions ou similar).
- [x] **REQ-OBR-05** — Implantar no Kubernetes (EKS, GKE ou AKS), com a implantação gerenciada via GitOps (ArgoCD/Flux). Ver Q-01.
- [x] **REQ-OBR-06** — Provisionar a stack de observabilidade no cluster e acrescentar Helm charts ao repositório GitOps.
- [x] **REQ-OBR-07** — Usar Prometheus para armazenar e consultar métricas de infraestrutura.
- [ ] **REQ-OBR-08** — Usar Loki para centralizar e indexar todos os logs dos contêineres do cluster.
- [x] **REQ-OBR-09** — Usar Grafana como visualização principal.
- [x] **REQ-OBR-10** — Criar no Grafana ao menos um dashboard customizado que centralize a saúde do ecossistema: (a) uso de recursos do cluster; (b) taxa de requisições dos microsserviços; (c) painel de logs em tempo real.
- [x] **REQ-OBR-11** — Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM). Ver Q-08.
- [ ] **REQ-OBR-12** — Escolher UMA ferramenta APM: Datadog OU New Relic; o PDF orienta contas gratuitas for education. Ver Q-04.
- [x] **REQ-OBR-13** — Alterar o código-fonte ou Dockerfile dos microsserviços com bibliotecas de instrumentação.
- [x] **REQ-OBR-14** — Gerar tracing distribuído e mostrar no APM o caminho de uma requisição ao evaluation-service.
- [x] **REQ-OBR-15** — Exibir no APM o mapa de dependências dos cinco microsserviços.
- [x] **REQ-OBR-16** — Configurar um alerta inteligente no Grafana ou no APM.
- [x] **REQ-OBR-17** — Criar conta no PagerDuty OU OpsGenie e integrar o alerta para abrir incidente automaticamente, com a ferramenta acionando o time (objetivo da p. 3). Ver Q-09.
- [x] **REQ-OBR-18** — Enviar notificação detalhada de ChatOps a Slack, Discord ou Teams. Ver Q-02.
- [x] **REQ-OBR-19** — Criar automação de Self-Healing que reaja automaticamente ao alerta e tente mitigar sem intervenção humana.
- [x] **REQ-OBR-20** — Entregar no repositório IaC/GitOps atualizado com stack e OTel Collector.
- [x] **REQ-OBR-21** — Entregar código das aplicações atualizado com instrumentação.
- [x] **REQ-OBR-22** — Entregar scripts ou automações de Self-Healing.
- [ ] **REQ-OBR-23** — Evidenciar funcionamento prático de todas as métricas, configurações e requisitos; material apenas configurado não basta.
- [ ] **REQ-OBR-24** — Entregar vídeo com duração de até 25 minutos.
- [x] **REQ-OBR-25** — Mostrar no vídeo EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack. [INCERTO]: divergência com alternativas da p. 2; Q-01.
- [x] **REQ-OBR-26** — No vídeo: (a) abrir o Grafana; (b) exibir o dashboard customizado com as métricas; (c) buscar logs no Loki; (d) explicar como o Collector roteia esses dados.
- [x] **REQ-OBR-27** — No vídeo: (a) abrir o painel do Datadog/New Relic e mostrar o Service Map; (b) fazer uma requisição de teste; (c) exibir o trace distribuído detalhado.
- [x] **REQ-OBR-28** — No vídeo: causar um problema proposital no sistema.
- [x] **REQ-OBR-29** — No vídeo: mostrar o alerta em Firing no Grafana/APM.
- [x] **REQ-OBR-30** — No vídeo: (a) mostrar o incidente sendo aberto no PagerDuty/OpsGenie; (b) mostrar a notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02.
- [x] **REQ-OBR-31** — No vídeo: mostrar a automação de Self-Healing acionada e executando a ação corretiva.
- [ ] **REQ-OBR-32** — Entregar relatório no formato PDF.
- [x] **REQ-OBR-33** — Incluir nomes, RMs e usernames no relatório.
- [ ] **REQ-OBR-34** — Incluir links do repositório de código e do vídeo no relatório.
- [x] **REQ-OBR-35** — Incluir print do dashboard do Grafana no relatório.
- [x] **REQ-OBR-36** — Incluir print de trace distribuído no APM no relatório.
- [x] **REQ-OBR-37** — Incluir print da notificação de incidente no ChatOps no relatório.
- [x] **REQ-OBR-38** — Incluir print de log/execução da automação de Self-Healing no relatório.
- [x] **REQ-OBR-39** — Explicar brevemente a arquitetura OTel implementada no relatório.
- [x] **REQ-OBR-40** — Justificar no relatório escolhas Datadog versus New Relic e OpsGenie versus PagerDuty.
- [ ] **REQ-OBR-41** — Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03.
- [ ] **REQ-OBR-42** — Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06.

## 10. Dúvidas para professor/tutor

As ambiguidades do enunciado foram preservadas. As escolhas atuais evitam Q-01/Q-02/Q-08/Q-09/Q-10/Q-12: usamos EKS/ArgoCD, Slack, SDKs OTel, PagerDuty, Collector padrão e falha/alerta/automação no mesmo serviço. Para submissão, confirmar principalmente prazo/canal e acesso aos links; para identificação, os usernames foram reutilizados do GitHub conforme orientação do usuário. Não interpretar todas as perguntas abaixo como bloqueios atuais.

| ID | Dúvida [INCERTO] | Evidência e ação |
|---|---|---|
| Q-01 | EKS/ArgoCD são obrigatórios para o vídeo mesmo se a solução usar GKE/AKS ou Flux? | p. 2 permite alternativas; p. 5 nomeia EKS/ArgoCD. REQ-OBR-25 mantido conservadoramente obrigatório. |
| Q-02 | Teams também é aceito na demonstração de ChatOps? | p. 5 inclui Teams; p. 6 menciona Slack/Discord. |
| Q-03 | Entrega individual é aceita e quantos participantes pode ter o grupo? | p. 2: “em princípio” em grupo; não detalha exceções. REQ-OBR-41 conservador. |
| Q-04 | Como obter as contas educacionais de APM e qual alternativa se o acesso não estiver disponível? | p. 4 orienta conta gratuita, sem explicar elegibilidade/procedimento. Disponibilidade externa não verificada. |
| Q-05 | Qual é a data/hora absoluta de entrega? | p. 2 cita prazo sem data. Não transportar prazo da Fase 3. |
| Q-06 | Qual plataforma/procedimento de submissão e configuração de acesso aos links? | Não especificado nas p. 2–6. Discord é canal para dúvidas. |
| Q-07 | Qual a rubrica detalhada e o valor de cada desconto? | p. 2 informa 90%; p. 5 informa dedução sem valores por item. |
| Q-08 | O agente ou a biblioteca do fornecedor (Datadog/New Relic), ou a instrumentação feita apenas no Dockerfile, é aceita se a telemetria passar pelo OTel Collector? O envio direto do agente ao APM, sem o Collector, é aceito? | p. 4 torna as bibliotecas OTel preferenciais, mas exige o envio da telemetria ao OTel e o roteamento pelo Collector; p. 5 pede código-fonte atualizado. REQ-OBR-11, 13 e 21 mantidos conservadoramente. |
| Q-09 | Se não for possível criar conta nova em uma das ferramentas de incidentes, a outra passa a ser a única opção aceita, ou existe alternativa? | p. 5 exige conta no PagerDuty OU OpsGenie; a disponibilidade dos planos não é tratada no enunciado. O projeto escolheu PagerDuty, com incidente comprovado em 2026-11-09; a alternativa não bloqueia esta entrega. |
| Q-10 | Com o Grafana Alloy no lugar do OTel Collector, os entregáveis que citam o Collector (REQ-OBR-20 e REQ-OBR-26) ficam atendidos mostrando o Alloy? | p. 4 torna o Alloy opcional; p. 5 nomeia o OTel Collector no código e no vídeo. |
| Q-11 | Um requisito demonstrado só no relatório (ou só no vídeo) evita a dedução, ou os subitens específicos de cada entregável são exigidos separadamente? | p. 5: regra geral com “ou”; p. 5–6: listas específicas de vídeo e de relatório. |
| Q-12 | A falha proposital do vídeo precisa acionar o mesmo alerta e a mesma automação configurados, ou podem ser cenários distintos? | p. 5 vincula a automação “ao alerta criado”; p. 6 usa exemplo de falha em outro serviço. |
| Q-13 | Os usernames do relatório são de qual plataforma (portal FIAP, GitHub, Discord)? | p. 6 não especifica. |
| Q-14 | Que característica torna o alerta “inteligente” para a avaliação? | p. 5 dá apenas um exemplo (taxa de 5xx maior que 5% no auth-service); a disciplina Alert Fatigue consta na p. 4. |

Parâmetros como retenção, amostragem, janela do alerta e nomes de atributos são decisões técnicas não fixadas no enunciado; não foram convertidos em requisitos adicionais. Limitações das aulas serão registradas por módulo nos guias e no relatório de revisão.

## 11. Índice dos guias de estudo

Guias de estudo dos cinco módulos, gerados a partir dos PDFs das aulas e ligados a estes requisitos pelos selos: [00 — Welcome](../aulas-fiap/00.Welcome%20to%20Observabilidade%20e%20Monitoramento/GUIA-ESTUDO-Welcome-to-Observabilidade-e-Monitoramento.html); [01 — Observabilidade e Monitoramento](../aulas-fiap/01.Observabilidade%20e%20Monitoramento/GUIA-ESTUDO-Observabilidade-e-Monitoramento.html); [02 — Monitoramento Opensource](../aulas-fiap/02.Monitoramento%20Opensource/GUIA-ESTUDO-Monitoramento-Opensource.html); [03 — APM](../aulas-fiap/03.APM/GUIA-ESTUDO-APM.html); [04 — Automação de incidentes](../aulas-fiap/04.Automação%20de%20incidentes/GUIA-ESTUDO-Automacao-de-incidentes.html).
