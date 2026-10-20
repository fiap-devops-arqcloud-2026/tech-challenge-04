# Dossiê — Capítulo de Projeto — Fase 4 (Welcome to Observabilidade e Monitoramento)

Última atualização: 2026-09-16, Claude (Opus 5).

Convenções: “p. N” = página física do PDF, contando a partir de 1. Paráfrase fiel por padrão; citações literais são curtas e vão entre aspas. **[COMPLEMENTO]** = explicação com conhecimento próprio, não está no PDF. **[CONTEXTO DO CURSO]** = informação de outro PDF do curso, conferida apenas no texto extraído (cabeçalho/linha indicados), não neste capítulo. **[ANÁLISE]** = interpretação do autor do dossiê. A marca d'água pessoal do rodapé (nome, RM, e-mail) aparece nas p. 1–4 e não foi transcrita.

---

## 1. Metadados

| Campo | Valor |
|---|---|
| Fonte | `docs/aulas-fiap/00.Welcome to Observabilidade e Monitoramento/POSTECH - Capítulo de Projeto - Fase 4.pdf` (inventário id 1) |
| SHA-256 conferido | `7b2794ae1941c969a9ac510f2fb2b3a476ceac2c0cdd2905556e9b520dc443b8` (igual ao inventário) |
| Páginas totais | 4 (A4, 595 × 842 pt) |
| Páginas lidas (texto PDFium) | 1, 2, 3, 4 — todas |
| Páginas inspecionadas visualmente | 1, 2, 3, 4 — todas (renderizações existentes `qa-fundamentos/01-p01.png` a `01-p04.png`, escala 2, 1191 × 1684 px; recortes ampliados do cabeçalho da p. 2 e do fundo da p. 4 feitos em pasta temporária) |
| Motivo da inspeção | p. 1 e p. 4: páginas de imagem (capa/contracapa), para confirmar ausência de conteúdo informativo; p. 2–3: confirmar ordem do texto, negritos, aspas em 'up/down' e o cabeçalho, que no texto extraído aparece com dois títulos concatenados |
| Código, comandos, tabelas, figuras informativas, fórmulas | Nenhum |
| Nível | **Introdutório** — é uma carta de boas-vindas da fase (8 parágrafos após a saudação), sem definições formais, sem código, sem exercícios, sem referências; apenas anuncia a trilha e a missão do projeto |

Observações de leitura:
- O texto extraído da p. 1 e da p. 4 inclui a linha de cabeçalho “Observabilidade e Monitoramento Welcome to DevOps e Arquitetura Cloud Página N de 4”, que **não aparece visualmente** nas renderizações (fundo escuro). Nas p. 2–3 o cabeçalho é visível, mas os dois títulos estão **sobrepostos** no mesmo ponto (“Observabilidade e Monitoramento” impresso sobre “Welcome to DevOps e Arquitetura Cloud”), à esquerda, e “Página 2 de 4” / “Página 3 de 4” à direita (ver WEL-Q09).
- A ordem do texto extraído coincide com a imagem; não há truncamento. A frase “rotas de acionamento (call rotation)” começa no fim da p. 2 (“rotas de”) e termina no início da p. 3.

## 2. Estrutura da aula

**Não há sumário, “O que vem por aí”, “Hands On”, “Saiba mais”, “Mercado, cases e tendências”, “O que você viu nesta aula” nem referências.** A estrutura física é:

| Página | Conteúdo efetivamente visto |
|---|---|
| p. 1 | Capa: fundo preto com traço de luz; logotipo “POS TECH” no alto à direita; embaixo, “DEVOPS E ARQUITETURA CLOUD” (em magenta), “FASE 4” e o título “OBSERVABILIDADE E MONITORAMENTO”, sublinhado. Não há o termo “Capítulo de Projeto” nem “Welcome” visíveis. |
| p. 2 | Saudação em negrito “Olá, estudante!” e parágrafos 1 a 6 (o 6º continua na p. 3). Marca d'água grande do logotipo FIAP em cinza, em diagonal. |
| p. 3 | Final do parágrafo 6, parágrafos 7 e 8. Mesma marca d'água. Restante da página em branco. |
| p. 4 | Contracapa: fundo escuro com ilustração decorativa (documentos/ícones translúcidos em ciano, linhas verticais, números decorativos como “32.611” e “20.595” sem significado informativo) e logotipo “POS TECH” centralizado. |

Mapa dos parágrafos (p. 2–3), na ordem do texto:

| § | Página | Função no texto |
|---|---|---|
| 1 | p. 2 | Parabéns pela Fase 4; o que foi feito até aqui; o trabalho não termina no deploy; pergunta central |
| 2 | p. 2 | Mudança de foco: comportamento do sistema em tempo real; Observabilidade, Monitoramento e Gestão de Incidentes |
| 3 | p. 2 | Bloco 1 — Fundamentos de Monitoramento e Observabilidade |
| 4 | p. 2 | Bloco 2 — Monitoramento OpenSource |
| 5 | p. 2 | Bloco 3 — APM (ferramentas Enterprise) |
| 6 | p. 2–3 | Bloco 4 — Automação de Incidentes |
| 7 | p. 3 | Projeto Integrador da fase |
| 8 | p. 3 | Fechamento motivacional |

## 3. Tópicos em sequência lógica de estudo

### T1. Por que uma fase de observabilidade: o trabalho não termina no deploy (p. 2, § 1)

- O texto parabeniza o estudante por chegar à Fase 4 do Postech em DevOps e Arquitetura Cloud (p. 2).
- Recapitula as fases anteriores com quatro verbos: o estudante **construiu, orquestrou, automatizou e protegeu** sua infraestrutura (p. 2).
- Afirma que, no mundo real, o trabalho **não termina no deploy** (p. 2).
- Apresenta a pergunta que, segundo o texto, separa amadores de profissionais seniores: “Como você sabe que sua aplicação está saudável antes que o cliente reclame?” (p. 2).
- Ideia central a ensinar: a detecção de problemas deve partir do próprio time/sistema, não da reclamação do cliente (p. 2).
- [COMPLEMENTO] Os quatro verbos correspondem, no enunciado, à base obrigatória das fases anteriores: microsserviços conteinerizados, Terraform, CI/CD com DevSecOps e Kubernetes via GitOps (enunciado p. 2). O capítulo não faz essa correspondência explicitamente.

### T2. Mudança de foco: do código ao comportamento do sistema em tempo real (p. 2, § 2)

- Nesta fase o olhar deixa de estar **apenas** no código e passa para o **comportamento do sistema em tempo real** (p. 2).
- O foco declarado da fase tem três partes: **Observabilidade, Monitoramento e Gestão de Incidentes** (p. 2).
- Metáforas usadas: “acender as luzes” e ganhar uma “visão de Raio-X” sobre a arquitetura (p. 2).
- O capítulo **não define** observabilidade nem monitoramento, nem os diferencia formalmente. [CONTEXTO DO CURSO] A distinção é tratada em “Introdução à Observabilidade” (Observabilidade e Monitoramento, Aula 1, título no cabeçalho da p. 1).

### T3. Bloco 1 — Fundamentos de Monitoramento e Observabilidade (p. 2, § 3)

- É o primeiro bloco anunciado (“Começaremos pelos…”, p. 2).
- Promessa: ir **além do simples 'up/down'** (grafado com aspas simples na imagem) para dominar os **três pilares essenciais: Logs, Métricas e Traces** (p. 2).
- Entender como **extrair dados vitais** de três camadas: **infraestrutura, containers e aplicação** (p. 2).
- Configurar **canais de comunicação eficientes via Slack, Teams e Email**, com o objetivo de que **nenhum evento crítico passe despercebido** (p. 2).
- Definições segundo a aula:
  - Três pilares essenciais — Logs, Métricas e Traces (p. 2). O capítulo só os nomeia; não define cada um.
- [COMPLEMENTO] “Up/down” designa a verificação binária de disponibilidade (o serviço responde ou não). Ir além disso significa entender como e por que o sistema se comporta, não só se está no ar.
- [CONTEXTO DO CURSO] O módulo 01 tem as aulas “Os Três Pilares da Observabilidade: Logs, Métricas e Traces na Prática” (Aula 2), “Coletando Métricas de Infraestrutura a Aplicações em Contêineres” (Aula 4) e “Do Dado à Ação: Configurando Alertas Inteligentes e Notificações” (Aula 5) — títulos nos cabeçalhos das p. 1 desses PDFs.

### T4. Bloco 2 — Monitoramento OpenSource (p. 2, § 4)

- Apresentado como “um padrão de mercado fundamental” (p. 2).
- Proposta prática (“mão na massa”) com uma “stack moderna” (p. 2), com o papel de cada ferramenta segundo o texto:
  - **Prometheus** — para coleta de métricas (p. 2).
  - **Grafana** — para visualização em dashboards (o texto diz “impactantes”) (p. 2).
  - **OpenTelemetry e Jaeger** — para rastreamento distribuído (p. 2).
  - **Zabbix** e **Grafana Alloy** — “além de explorar”; o texto não atribui papel específico a eles (p. 2).
- Objetivo declarado: saber montar uma **central de monitoramento robusta sem depender de licenças proprietárias** (p. 2).
- O capítulo **não cita Loki** nem Kubernetes neste bloco (ver WEL-Q04).
- [CONTEXTO DO CURSO] O módulo 02 contém, pelos cabeçalhos das p. 1: Aula 1 “Métricas com Zabbix”; Aula 2 “Métricas para Sistemas Dinâmicos com Prometheus”; Aula 3 “Visualização e Alertas com Grafana”; Aula 4 “Logs com Loki”; Aula 5 “Tracing com Jaeger”; Aula 6 “OpenTelemetry (OTel) e Alloy”; Aulas 7–8 “Observabilidade no Kubernetes” (partes 1 e 2).

### T5. Bloco 3 — APM com ferramentas Enterprise (p. 2, § 5)

- Justificativa: o **mercado corporativo também exige domínio de ferramentas Enterprise** (p. 2).
- Haverá **uma disciplina dedicada a APM** — expandido no texto como **Application Performance Monitoring** — com “gigantes como Datadog e New Relic” (p. 2). “Como” indica exemplos.
- “O jogo sobe de nível” com três atividades (p. 2):
  1. configurar **alertas inteligentes**;
  2. realizar **troubleshooting avançado para identificar gargalos de código**;
  3. trabalhar na **otimização de performance e custos**, transformando **dados técnicos em decisões de negócio**.
- Definição segundo a aula: APM — Application Performance Monitoring (p. 2). Sem definição adicional.
- [CONTEXTO DO CURSO] O módulo 03 tem Aulas 1–5 sobre Datadog e 6–10 sobre New Relic (cabeçalhos das p. 1).

### T6. Bloco 4 — Automação de Incidentes (p. 2–3, § 6)

- “Fecharemos o ciclo” com a Automação de Incidentes (p. 2).
- Princípio: **“Monitorar não basta; é preciso reagir rápido.”** (p. 2).
- Base: **práticas de SRE**, expandido como **Site Reliability Engineering** (p. 2).
- Conteúdos anunciados (p. 2–3):
  - configurar **monitoramento ativo**;
  - **rotas de acionamento (call rotation)**;
  - **processos de escalation**.
- Ferramentas: “como” **PagerDuty** e **OpsGenie**, **integradas a automações via Functions** (p. 3).
- Objetivos: **reduzir drasticamente o MTTR**, expandido como **Tempo Médio de Recuperação**, e **garantir a disponibilidade do sistema** (p. 3).
- Definições segundo a aula:
  - SRE — Site Reliability Engineering (p. 2).
  - MTTR — Tempo Médio de Recuperação (p. 3). Ver WEL-Q02 sobre variação no curso.
  - Call rotation — apresentado entre parênteses após “rotas de acionamento” (p. 2–3); sem definição. Ver WEL-Q01.
  - Escalation — citado como “processos de escalation” (p. 3); sem definição.
  - Functions — citado como meio de automação integrado a PagerDuty/OpsGenie (p. 3); sem especificar provedor. Ver WEL-Q05.
- [COMPLEMENTO] Em uso corrente, *on-call rotation* é a escala/rodízio de quem fica de plantão e é acionado; *escalation* é o encaminhamento do incidente a outro nível/pessoa quando não há resposta ou resolução no prazo; *monitoramento ativo* costuma designar verificações proativas que disparam ação, em contraste com apenas observar painéis.
- [CONTEXTO DO CURSO] O módulo 04 tem: Aula 1 “O Que é um Incidente?”; Aula 2 “Monitoramento Ativo e ‘Alert Fatigue’”; Aula 3 “MTTR Baixo com PagerDuty”; Aula 4 “MTTR Baixo com OpsGenie (Atlassian)”; Aula 5 “Notificação e Interação com Slack e Teams”; Aula 6 “Runbook Automation - Automação com Functions”; Aula 7 “Self-Healing e Pós-Incidente” (cabeçalhos das p. 1).

### T7. Projeto Integrador da fase (p. 3, § 7)

- O capítulo chama a entrega de **Projeto Integrador desta fase** (p. 3). Ver WEL-Q06.
- Missão: **instrumentar a aplicação que você vem desenvolvendo** (p. 3) — ou seja, a mesma aplicação das fases anteriores.
- Deve-se entregar um **ambiente** com três características (p. 3):
  1. **qualquer falha** dispara **um alerta preciso**;
  2. **dashboards que contém** [sic, grafia da aula] **a história do que está acontecendo**;
  3. **automações que ajudem na recuperação do serviço** (a formulação é “ajudem”, não “garantam”).
- O capítulo não detalha ferramentas, prazos, formato de entrega nem critérios de avaliação. Esses itens estão no enunciado (enunciado p. 2–6).

### T8. Fechamento (p. 3, § 8)

- Convida a desenvolver **uma visão analítica e proativa** (p. 3).
- Frase final: “Vamos transformar dados em confiabilidade!” (p. 3).

## 4. Comandos, código e configurações

**Não há nenhum bloco de código, comando, arquivo de configuração, variável de ambiente, caminho de arquivo ou subcomando** nas p. 1–4 (conferido no texto extraído e nas quatro imagens).

Termos técnicos citados em prosa (nomes, não comandos): 'up/down' (p. 2); Logs, Métricas, Traces (p. 2); Slack, Teams, Email (p. 2); Prometheus, Grafana, OpenTelemetry, Jaeger, Zabbix, Grafana Alloy (p. 2); APM, Datadog, New Relic (p. 2); SRE, monitoramento ativo, call rotation, escalation (p. 2–3); PagerDuty, OpsGenie, Functions, MTTR (p. 3).

## 5. Figuras e tabelas

Nenhuma figura informativa, diagrama, tela, gráfico ou tabela.

| Página | Elemento visual | Conteúdo visto |
|---|---|---|
| p. 1 | Capa | Fundo preto com faixa de luz; “POS TECH”; “DEVOPS E ARQUITETURA CLOUD”, “FASE 4”, “OBSERVABILIDADE E MONITORAMENTO”. Decorativa. |
| p. 2–3 | Marca d'água | Logotipo FIAP em contorno cinza, diagonal, atrás do texto. Decorativa. |
| p. 2–3 | Cabeçalho | Dois títulos sobrepostos à esquerda (“Observabilidade e Monitoramento” e “Welcome to DevOps e Arquitetura Cloud”) e “Página N de 4” à direita. |
| p. 4 | Contracapa | Ilustração tecnológica em ciano (documentos translúcidos, pontos, linhas, números soltos) e “POS TECH” no centro. Decorativa. |

## 6. Ferramentas, tecnologias e arquitetura

O capítulo não apresenta arquitetura (nenhum fluxo entre componentes). Organização do dossiê — papel **segundo o capítulo**; a coluna do enunciado serve só para a seção 12:

| Ferramenta/conceito | Bloco (capítulo) | Papel segundo o capítulo | Página | Situação no enunciado (referência) |
|---|---|---|---|---|
| Logs, Métricas, Traces | Fundamentos | Três pilares essenciais | p. 2 | Métricas, logs e traces passam pelo OTel Collector (enunciado p. 4) |
| Slack, Teams, Email | Fundamentos | Canais de comunicação eficientes para que nenhum evento crítico passe despercebido | p. 2 | ChatOps exigido em Slack, Discord **ou** Teams; Email não é citado (enunciado p. 5) |
| Prometheus | OpenSource | Coleta de métricas | p. 2 | Armazenamento e consulta de métricas de infraestrutura (enunciado p. 3) |
| Grafana | OpenSource | Visualização em dashboards | p. 2 | Ferramenta principal de visualização; ≥1 dashboard customizado (enunciado p. 3) |
| OpenTelemetry | OpenSource | Com Jaeger, rastreamento distribuído | p. 2 | OTel Collector central para métricas, logs e traces (enunciado p. 4) |
| Jaeger | OpenSource | Com OpenTelemetry, rastreamento distribuído | p. 2 | Não citado |
| Zabbix | OpenSource | “Explorar”; papel não especificado | p. 2 | Não citado |
| Grafana Alloy | OpenSource | “Explorar”; papel não especificado | p. 2 | Opcional no lugar do OTel Collector (enunciado p. 4) |
| Loki | — | **Não citado no capítulo** | — | Obrigatório para logs (enunciado p. 3) |
| APM | APM | Application Performance Monitoring; alertas inteligentes, troubleshooting de gargalos de código, otimização de performance e custos | p. 2 | Escolher UMA ferramenta APM (enunciado p. 4) |
| Datadog, New Relic | APM | “Gigantes” citados como exemplos de APM Enterprise | p. 2 | Datadog OU New Relic, contas for education (enunciado p. 4) |
| SRE | Automação | Base das práticas de automação de incidentes | p. 2 | Não citado |
| Monitoramento ativo | Automação | Conteúdo a configurar | p. 2 | Não citado com esse nome |
| Call rotation / escalation | Automação | “Rotas de acionamento” e “processos de escalation” | p. 2–3 | Não citados |
| PagerDuty, OpsGenie | Automação | Ferramentas de incidentes integradas a automações via Functions | p. 3 | PagerDuty OU OpsGenie abrindo incidente automaticamente (enunciado p. 5) |
| Functions | Automação | Meio de automação integrado às ferramentas de incidente | p. 3 | Automação via Runbook Automation, AWS Lambda ou GitHub Action (enunciado p. 5) |
| MTTR | Automação | Tempo Médio de Recuperação, a reduzir drasticamente | p. 3 | Não citado |
| Self-Healing | — | **Não citado com esse nome**; aparece como “automações que ajudem na recuperação do serviço” | p. 3 | Obrigatório (enunciado p. 5) |

## 7. Boas práticas e erros comuns (como a aula formula)

Boas práticas / atitudes recomendadas:
- Não considerar o trabalho encerrado no deploy (p. 2).
- Saber que a aplicação está saudável **antes** que o cliente reclame (p. 2).
- Observar o comportamento do sistema em tempo real, não só o código (p. 2).
- Ir além do simples 'up/down' (p. 2).
- Extrair dados de infraestrutura, containers e aplicação (p. 2).
- Configurar canais de comunicação eficientes para que nenhum evento crítico passe despercebido (p. 2).
- Conseguir montar uma central de monitoramento robusta sem depender de licenças proprietárias (p. 2).
- Transformar dados técnicos em decisões de negócio (p. 2).
- Monitorar não basta; é preciso reagir rápido (p. 2).
- Reduzir drasticamente o MTTR e garantir a disponibilidade (p. 3).
- Alertas precisos, dashboards que contem a história do que acontece e automações que ajudem na recuperação (p. 3).
- Visão analítica e proativa (p. 3).

Erros comuns (implícitos no texto, não listados como tal):
- Descobrir problemas pela reclamação do cliente — associado, pela pergunta central, a um comportamento de “amadores” (p. 2).
- Ficar no “simples 'up/down'” (p. 2).
- Apenas monitorar sem capacidade de reação (p. 2).

## 8. Hands On

Não há seção Hands On, laboratório, comando, código ou referência a vídeo no capítulo (p. 1–4). A única proposta prática é a missão do Projeto Integrador (p. 3) e a menção genérica de que no bloco OpenSource o estudante colocará “a mão na massa” (p. 2).

## 9. Mercado, cases e tendências

Não há seção dedicada, cases ou números. Menções de mercado: o Monitoramento OpenSource é chamado de padrão de mercado fundamental (p. 2); o mercado corporativo também exige ferramentas Enterprise (p. 2); Datadog e New Relic são chamados de “gigantes” (p. 2). Nada foi validado externamente.

## 10. “O que você viu nesta aula” e referências bibliográficas

Não existem no PDF. O fechamento é o § 8 (p. 3). A p. 4 é contracapa sem texto além do logotipo.

## 11. Pontos prováveis de prova/projeto — [ANÁLISE]

1. A pergunta central da fase (saber da saúde da aplicação antes do cliente) e a ideia de que o trabalho não termina no deploy (p. 2).
2. O foco triplo da fase: Observabilidade, Monitoramento e Gestão de Incidentes (p. 2).
3. Os **três pilares** — Logs, Métricas e Traces — e as três camadas de dados: infraestrutura, containers, aplicação (p. 2).
4. Associação ferramenta → papel: Prometheus/coleta de métricas; Grafana/dashboards; OpenTelemetry + Jaeger/rastreamento distribuído (p. 2).
5. OpenSource (sem licenças proprietárias) vs. Enterprise (Datadog, New Relic) (p. 2).
6. Expansões de siglas: APM, SRE, MTTR — com a ressalva de WEL-Q02 (p. 2–3).
7. A sequência dos quatro blocos (Fundamentos → OpenSource → APM → Automação de Incidentes) e a frase “monitorar não basta; é preciso reagir rápido” (p. 2–3).
8. Para o projeto: a missão resume o fluxo **falha → alerta preciso → dashboard que conta a história → automação que ajuda a recuperar** (p. 3), que é o mesmo encadeamento da “Prova Real” do vídeo no enunciado (enunciado p. 6).

## 12. Relação com o Tech Challenge

Vínculos reais apenas; estudar o capítulo não comprova atendimento. Exigências vêm do enunciado.

| ID | Vínculo com o capítulo | Força |
|---|---|---|
| REQ-OBR-01 | O capítulo situa a fase como continuação do que foi construído, orquestrado, automatizado e protegido (p. 2) e manda instrumentar a aplicação que “você vem desenvolvendo” (p. 3). Não detalha a base. | Fraca/contextual |
| REQ-OBR-07 | Prometheus apresentado para coleta de métricas (p. 2). O enunciado pede armazenamento e consulta de métricas de infraestrutura (enunciado p. 3). | Média |
| REQ-OBR-09 | Grafana para visualização em dashboards (p. 2). | Média |
| REQ-OBR-10 | Dashboards “que contém a história do que está acontecendo” (p. 3) e extração de dados de infraestrutura, containers e aplicação (p. 2) orientam o conteúdo do dashboard; o capítulo não fala de taxa de requisições nem de painel de logs. | Fraca/média |
| REQ-OBR-11 | OpenTelemetry é anunciado, mas **só** no contexto de rastreamento distribuído com Jaeger (p. 2); o papel de Collector central para métricas, logs e traces vem do enunciado (p. 4). | Fraca |
| REQ-OBR-12 | Datadog e New Relic citados como APM Enterprise (p. 2). | Média |
| REQ-OBR-13 / REQ-OBR-21 | A missão do Projeto Integrador é instrumentar a aplicação (p. 3). O capítulo não diz como. | Média |
| REQ-OBR-14 | Rastreamento distribuído anunciado com OpenTelemetry e Jaeger (p. 2); o enunciado exige vê-lo no APM (enunciado p. 4), não no Jaeger. | Fraca/média |
| REQ-OBR-16 | “Configurar alertas inteligentes” no bloco APM (p. 2) e “alerta preciso” na missão (p. 3). | Média |
| REQ-OBR-17 | PagerDuty e OpsGenie no bloco de Automação de Incidentes (p. 3). | Média |
| REQ-OBR-18 | Canais de comunicação via Slack, Teams e Email (p. 2). Slack e Teams são opções válidas do enunciado; Email não; Discord não aparece no capítulo (enunciado p. 5). | Média |
| REQ-OBR-19 / REQ-OBR-22 | “Automações via Functions” (p. 3) e “automações que ajudem na recuperação do serviço” (p. 3). O termo Self-Healing não aparece. | Média (19) / fraca (22) |
| REQ-OBR-40 | O capítulo apresenta as duas duplas a comparar (Datadog/New Relic, p. 2; PagerDuty/OpsGenie, p. 3), sem critérios de escolha. | Fraca |
| REQ-OBR-28, 29, 31 | A missão (falha → alerta → recuperação, p. 3) antecipa o roteiro da demonstração; não trata de vídeo/evidência. | Fraca/narrativa |
| REQ-BON-01 | Grafana Alloy será explorado (p. 2); o enunciado o torna opcional no lugar do OTel Collector (enunciado p. 4). | Fraca |

Sem vínculo real (não forçar): REQ-OBR-02 a 06, 08 (Loki não é citado), 15, 20, 23 (o capítulo não trata de evidenciar funcionamento), 24–27, 30, 32–39, 41; REQ-BON-02; SUG-01 a SUG-04 (sugestões autorais do Codex; o capítulo não as menciona — no máximo, “alerta preciso” e “nenhum evento crítico passe despercebido” tangenciam SUG-02).

## 13. Incertezas [INCERTO]

| ID | Páginas | Trecho curto | Por que é duvidoso | Como tratar no guia |
|---|---|---|---|---|
| WEL-Q01 | p. 2–3 | “rotas de acionamento (call rotation)” | “Rota” sugere roteamento de alertas; “rotation” significa rodízio/escala de plantão. A tradução mistura os dois sentidos e não é definida. Aulas posteriores usam “on-call” e “escalonamento” (Automação de Incidentes, Aula 2 e Aula 3, texto extraído). | Citar o termo da FIAP literalmente; explicar como [COMPLEMENTO] que *call rotation* costuma designar escala de plantão, distinta de regras de roteamento; remeter ao módulo 04. |
| WEL-Q02 | p. 3 | “MTTR (Tempo Médio de Recuperação)” | No próprio curso a sigla aparece com outras expansões: “Mean Time To Resolution, ou Tempo Médio para Resolução” (Automação de Incidentes, Aula 3, p. 3); “tempo médio de resolução” (Observabilidade e Monitoramento, Aula 1, p. 13); “Mean Time to Resolution” (Monitoramento Opensource, Aula 8, p. 9); “tempo médio de recuperação” (Observabilidade e Monitoramento, Aula 5, p. 4). | Registrar a variação; não tratar uma expansão como a única correta; em prova, reconhecer ambas. |
| WEL-Q03 | p. 2 | “OpenTelemetry e Jaeger para rastreamento distribuído” | Escopo mais estreito que o do enunciado, que usa o OTel Collector para métricas, logs e traces (enunciado p. 4), e que o título da aula “OpenTelemetry (OTel) e Alloy” (Monitoramento Opensource, Aula 6). Não é erro, mas pode induzir a ver OTel só como tracing. | Não reduzir OTel a tracing no guia; indicar que o papel completo vem do enunciado e do módulo 02. |
| WEL-Q04 | p. 2–3 | Lista de ferramentas dos blocos | A lista é panorâmica e não exaustiva: não cita Loki (obrigatório, enunciado p. 3), Kubernetes, Self-Healing (obrigatório, enunciado p. 5) nem Discord; o curso tem “Logs com Loki” (Monitoramento Opensource, Aula 4) e “Self-Healing e Pós-Incidente” (Automação de Incidentes, Aula 7). Também coloca “alertas inteligentes” só no APM, enquanto o enunciado aceita alerta no Grafana ou APM (enunciado p. 5). | Dizer que o capítulo é visão geral, não inventário; apontar onde Loki e Self-Healing são estudados. |
| WEL-Q05 | p. 3 | “automações via Functions” | Termo genérico, sem provedor (AWS Lambda, Azure Functions etc.). A aula do módulo 04 “Runbook Automation - Automação com Functions” usa exemplo com Lambda (Automação de Incidentes, Aula 6, p. 5, texto extraído); o enunciado lista Runbook Automation, AWS Lambda ou GitHub Action (enunciado p. 5). | Não inferir provedor a partir do capítulo; citar as opções do enunciado. |
| WEL-Q06 | p. 3 | “Projeto Integrador desta fase” | O enunciado chama a entrega de Tech Challenge (enunciado p. 2). Muito provavelmente é a mesma atividade, mas o capítulo não usa esse nome. | Escrever “o capítulo chama de Projeto Integrador; o enunciado, de Tech Challenge”. |
| WEL-Q07 | p. 3 | “qualquer falha dispare um alerta preciso” | Formulação absoluta/aspiracional. O enunciado exige configurar um alerta inteligente e demonstrar uma falha proposital (enunciado p. 5–6), não cobertura de “qualquer falha”. | Não transformar em exigência de cobertura total; tratar como meta de qualidade. |
| WEL-Q08 | p. 2 | “Prometheus para coleta de métricas” | O enunciado atribui ao Prometheus armazenamento e consulta de métricas de infraestrutura e ao OTel Collector o recebimento/roteamento (enunciado p. 3–4). Papéis compatíveis, mas a palavra “coleta” pode confundir quem desenha o fluxo OTel → Prometheus. | Apresentar ambos os papéis com suas fontes; o desenho do fluxo segue o enunciado. |
| WEL-Q09 | p. 1–4 | Cabeçalho “Observabilidade e Monitoramento” + “Welcome to DevOps e Arquitetura Cloud”; arquivo “Capítulo de Projeto - Fase 4” | Dois títulos sobrepostos (falha de diagramação visível nas p. 2–3) e nome de arquivo diferente do nome da pasta; o título do material é ambíguo. | Referir o material pelo nome do arquivo e da pasta; não citar o cabeçalho como título. |

## 14. Limitações

- O PDF não cita vídeos, links externos, referências bibliográficas, exercícios ou Hands On; nada disso precisou ser aberto.
- As referências a outras aulas (seções 3, 12 e 13, rótulo [CONTEXTO DO CURSO]) foram conferidas apenas nos textos extraídos por PDFium (cabeçalhos e linhas indicadas), sem inspeção visual daqueles PDFs.
- As renderizações usadas foram as existentes (`qa-fundamentos/01-p01.png` a `01-p04.png`, escala 2); o hash do PDF confere com o inventário e o conteúdo coincide com o texto extraído, por isso não foi necessário renderizar de novo. Recortes ampliados do cabeçalho (p. 2) e do fundo (p. 4) foram gerados só em pasta temporária.
- O cabeçalho das p. 1 e 4 existe na camada de texto, mas não é visível na imagem.
- Nenhuma afirmação de mercado foi validada externamente (não há números no capítulo).
