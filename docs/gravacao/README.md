# 🎬 Roteiro de gravação - Fase 4

**Atualizado em 2026-11-10. Gravação planejada para 2026-11-10.** Guia de fala e operação. A FIAP exige até 25 minutos; a sugestão abaixo usa 21 minutos, deixando 4 de margem. Não é garantia de nota: o funcionamento precisa aparecer. Fonte: enunciado, p. 5–6.

## Materiais prontos para abrir

- [Roteiro em PDF](ROTEIRO_GRAVACAO_2026-11-10_v02.pdf): uma cena por página, ações e fala completa.
- [PowerPoint editável](ROTEIRO_GRAVACAO_2026-11-10_v02.pptx): as mesmas cenas, com notas do apresentador.
- [Relatório com evidências](../relatorio/README.md): participantes e prints do ensaio de 2026-11-09; URL do vídeo pendente.
- [Índice dos prints](../evidencias/README.md): origem, horário e o que cada imagem comprova.

O ensaio integrado de 2026-11-09 foi concluído: falha 503, Firing, PagerDuty/Slack, execução automática e recuperação. [Execução comprovada](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42679005683). A gravação deve mostrar uma execução atual, não apenas reproduzir os prints.

## Antes de apertar REC

Deixe abertos: GitHub (README, código, Actions e self-healing), ArgoCD, Grafana (dashboard, Explore/Loki e Alert rules), New Relic (Maps e Distributed tracing), PagerDuty (Incidents), Slack (#incidentes-tech-challenge), Lens (Nodes e Pods) e três terminais (tráfego, pods e comandos). AWS Console/EKS é apoio opcional; o Prometheus e o Collector podem ser mostrados pelo Grafana/Lens/configuração, sem mais uma interface.

- Teste 20 segundos de áudio e reveja o arquivo. Feche notificações pessoais.
- Prepare login e túneis antes de gravar; não exiba .env, Secrets, tfvars, tokens nem telas de integrações com chaves.
- Faça um ensaio completo. Após um restart, aguarde pelo menos 600 segundos e confira alerta Normal antes de repetir.
- Mantenha o pod de tráfego ligado. Confirme que a flag novo-painel existe e retorna resultado.
- Os comandos operacionais estão em [COMANDOS.md](COMANDOS.md); são executados em Git Bash. A sequência completa, com cada frase ligada a uma tela e a um comando, está em [PASSO_A_PASSO_POR_CENA.md](PASSO_A_PASSO_POR_CENA.md).
- Confirme o enquadramento do **Service Map com os cinco serviços**: a captura existente é do mapa de um trace, não do mapa global. Abra dependências adicionais e ajuste o período no New Relic antes de gravar.
- A fala é sugerida. Só diga que um passo funcionou depois de mostrá-lo na tela.

## 01 · Apresente o problema (00:00–01:00)

**Tela:** GitHub · README

- Mostre o nome ToggleMaster e os cinco serviços.
- Aponte o diagrama de observabilidade.
- Explique o objetivo antes das ferramentas.

**Sua fala:**

> Este é o ToggleMaster, uma plataforma de feature flags com cinco microsserviços. A Fase 4 evolui a base das fases anteriores para responder a três perguntas: o sistema está saudável, onde uma requisição falhou e como reagimos ao incidente? Mantivemos Terraform, CI/CD com verificações de segurança e GitOps. Agora acrescentamos métricas, logs, traces e uma tentativa automática de recuperação. Vou demonstrar o ambiente funcionando e depois provocar uma falha controlada para acompanhar a resposta completa.

**Confira:** O avaliador entende o problema e o que será demonstrado.

**Fonte:** Enunciado FIAP, p. 2–3. Contextualização sugerida.

## 02 · Mostre a base automatizada (01:00–03:00)

**Tela:** GitHub · código + Actions

- Abra terraform/: base, cluster e k8s.
- Abra um CI de serviço concluído na main.
- Mostre testes, lint, SAST/SCA, imagem e publicação.

**Sua fala:**

> A infraestrutura está dividida em três camadas Terraform, com estados separados. O código fica no Git; o state fica no backend S3 e relaciona os recursos declarados aos recursos existentes. Os cinco serviços possuem pipelines que reutilizam verificações por linguagem. Aqui vemos build e testes, análise do código e das dependências. No pull request, a imagem também é construída e verificada. No push da main, o pipeline publica no ECR usando OIDC e atualiza a tag no GitOps. É o ArgoCD que reconcilia essa configuração no cluster.

**Confira:** Abra o run correto; verde de CI não substitui a prova do cluster.

**Fonte:** Enunciado FIAP, p. 2 e 5; .github/workflows; terraform/.

## 03 · Prove EKS + GitOps (03:00–05:00)

**Tela:** Lens · Nodes/Pods + ArgoCD

- Lens: mostre os dois nós Ready e os workloads.
- ArgoCD: mostre as seis Applications Synced/Healthy.
- Abra observability e explique os charts Helm.

**Sua fala:**

> Este é o cluster EKS provisionado por código. No Lens, vemos os nós e os pods das aplicações e da observabilidade. O Lens é apenas uma interface de inspeção. No ArgoCD, as seis aplicações estão sincronizadas com o estado desejado no Git e saudáveis nesta consulta. A aplicação observability organiza os componentes: kube-prometheus-stack, Loki, Collector gateway e Collector agents. Os valores dos charts e as configurações do dashboard e dos alertas estão versionados. Assim, a stack de monitoramento também segue GitOps.

**Confira:** Mostrar Ready, Running e Synced/Healthy; não apenas arquivos YAML.

**Fonte:** Enunciado FIAP, p. 3 e 5.

## 04 · Leia a saúde no Grafana (05:00–08:00)

**Tela:** Grafana · ToggleMaster - Visao geral

- Mostre requisições/s, erros 5xx e latência p95.
- Role para CPU/memória dos nós e dos pods.
- Mostre o painel de logs com dados recentes.

**Sua fala:**

> Este dashboard foi customizado para o ToggleMaster. A taxa de requisições mostra o tráfego recebido pelos serviços HTTP. A proporção de erros indica quantas respostas falharam, e a latência p95 ajuda a observar a experiência nas requisições mais lentas. Mais abaixo, CPU e memória permitem relacionar comportamento da aplicação e recursos do cluster. O painel de logs consulta o Loki. Analytics processa eventos de forma assíncrona, portanto não deve ser apresentado como se tivesse o mesmo tráfego HTTP dos demais serviços. Vou conferir o intervalo de tempo e a atualização para demonstrar dados atuais.

**Confira:** PRINT 01: dashboard com dados; use duas imagens para incluir recursos e logs.

**Fonte:** Enunciado FIAP, p. 3, 5–6; dashboard versionado.

## 05 · Conecte logs, métricas e traces (08:00–10:00)

**Tela:** Grafana Explore · Loki + diagrama OTel

- No Explore, selecione Loki e execute a consulta.
- Aponte serviço, timestamp e trace_id de um log.
- Explique agent → gateway → backends.

**Sua fala:**

> Métricas resumem valores ao longo do tempo; logs registram eventos; traces mostram o caminho de uma execução, dividido em spans. Aqui consulto logs centralizados pelo Loki. O trace_id permite correlacionar um evento ao rastreamento da requisição. Em cada nó, um Collector agent lê os logs dos contêineres e os envia ao gateway. As aplicações enviam seus traces ao mesmo gateway. Ele processa os dados, encaminha logs ao Loki, traces ao New Relic e gera métricas de aplicação pelo spanmetrics para o Prometheus. As métricas de infraestrutura são coletadas diretamente pelo Prometheus nos exporters.

**Confira:** A consulta precisa retornar logs. Explique o caminho real, incluindo o scrape direto.

**Fonte:** Enunciado FIAP, p. 3–5; otel-agent.yaml e otel-gateway.yaml.

## 06 · Siga uma requisição no APM (10:00–13:00)

**Tela:** New Relic · Maps + Distributed tracing

- Mostre o mapa com os cinco serviços e dependências.
- Faça uma requisição /evaluate no terminal.
- Abra o trace correspondente; expanda os spans.

**Sua fala:**

> Escolhemos New Relic como o APM comercial desta entrega. Ele recebe os traces via OpenTelemetry. No mapa, observamos as dependências dos cinco microsserviços. Agora faço uma requisição ao evaluation-service. No trace detalhado, vemos as chamadas aos serviços de flags, segmentação e autenticação, além das dependências de dados. O caminho varia: um acerto no Redis pode encurtar a execução. Para a demonstração completa, seleciono uma requisição sem cache e confiro seu horário. O fluxo de SQS e analytics é assíncrono; a resposta HTTP não espera a persistência analítica. A duração de cada span ajuda a localizar uma operação lenta.

**Confira:** PRINT 02: trace aberto com ID, serviço de entrada, spans e durações; a lista de traces não basta.

**Fonte:** Enunciado FIAP, p. 4 e 6.

## 07 · Provoque a falha controlada (13:00–15:00)

**Tela:** Terminal · tráfego + flag-service

- Mostre HTTP 200 antes da falha.
- Ative /admin/fault usando o comando preparado.
- Mostre HTTP 503; mantenha tráfego contínuo.

**Sua fala:**

> Agora vou provocar uma falha transitória controlada no flag-service. O objetivo é demonstrar detecção e reação automáticas, sem desligar um banco. A rota administrativa exige autenticação e faz as rotas de flags responderem 503. O health check continua saudável; por isso, o Kubernetes não reinicia o processo apenas pela liveness probe. O tráfego contínuo permite medir a proporção de erros. A falha fica na memória do processo e desaparece quando um novo pod assume. Vou observar a cadeia sem clicar em Run workflow nem reiniciar manualmente o serviço.

**Confira:** Grave a causa e o efeito; falha manual → resposta automática.

**Fonte:** Enunciado FIAP, p. 5–6; services/flag-service/app.py.

## 08 · Acompanhe alerta e comunicação (15:00–17:00)

**Tela:** Grafana Alerting → PagerDuty → Slack

- Mostre FlagService5xxAlto em Firing.
- Abra o incidente criado automaticamente no PagerDuty.
- Mostre a mensagem detalhada no canal do Slack.

**Sua fala:**

> A regra avalia a proporção de erros 5xx do flag-service. O limite escolhido é maior que dez por cento durante um minuto; isso evita reagir a um único erro isolado. O exemplo do enunciado usa outro serviço e outro percentual, mas nossa regra atende ao mesmo objetivo. Quando entra em Firing, o Grafana abre um incidente no PagerDuty e envia o contexto ao Slack. PagerDuty organiza o incidente e o acionamento humano; Slack concentra a comunicação. Aqui confiro serviço, horário e descrição para mostrar que as telas correspondem à mesma falha. Um DatasourceError não é a evidência desta regra de erros HTTP.

**Confira:** PRINT 03: notificação do incidente real; capture também Firing e PagerDuty como apoio.

**Fonte:** Enunciado FIAP, p. 5–6; rules.yaml, policies.yaml e contactpoints.yaml.

## 09 · Prove a correção automática (17:00–20:00)

**Tela:** GitHub Actions · Self-healing + terminal

- Abra o run disparado por repository_dispatch.
- Mostre o passo de restart e resultado restarted.
- Mostre pod novo, HTTP 200 e alerta resolvido.

**Sua fala:**

> O mesmo alerta chama o webhook do GitHub e dispara esta execução automaticamente. O workflow assume uma role temporária por OIDC. Antes de agir, o script valida o serviço em uma lista permitida e verifica um intervalo mínimo de dez minutos entre reinícios. Ele executa rollout restart e aguarda o rollout terminar. Aqui vemos o registro da ação e a substituição do pod. O tráfego volta a 200, o alerta retorna ao normal e o incidente é resolvido. Isso é uma tentativa de mitigação, não uma cura universal: um banco indisponível, por exemplo, não seria corrigido apenas reiniciando a aplicação.

**Confira:** PRINT 04: log/execução da automação, com evento automático e reinício concluído.

**Fonte:** Enunciado FIAP, p. 5–6; self-healing.yml e restart.sh.

## 10 · Feche com as evidências (20:00–21:00)

**Tela:** README + relatório PDF

- Recapitule falha → detecção → comunicação → recuperação.
- Mostre onde estão código, relatório e evidências.
- Confirme identificação e link acessível do vídeo na entrega.

**Sua fala:**

> Demonstramos a base automatizada, as métricas e os logs centralizados, o roteamento pelo Collector e o tracing no APM. Na prova do incidente, acompanhamos a falha controlada, o alerta, a comunicação e a tentativa automática de recuperação. O repositório reúne o código de infraestrutura, a instrumentação e a automação. O relatório traz os quatro prints exigidos e justifica a arquitetura e as escolhas de New Relic e PagerDuty. As evidências precisam corresponder ao que foi realmente executado. Obrigado.

**Confira:** Finalize até 25 minutos. Meta do roteiro: 21 minutos + 4 de margem.

**Fonte:** Enunciado FIAP, p. 5–6.

## 📸 Quatro prints obrigatórios

1. Dashboard Grafana com métricas, recursos e logs (pode ser dividido em duas imagens).
2. Trace distribuído detalhado no APM.
3. Notificação do incidente no ChatOps.
4. Log/execução da automação de self-healing.

Salve complementos em `docs/evidencias/entrada-local/`; essa entrada é ignorada pelo Git. Imagens revisadas ficam na pasta datada de evidências. ArgoCD, Lens, Service Map, Loki, Firing e PagerDuty são apoios úteis, além dos quatro prints explicitamente pedidos no relatório.

## ✅ Antes de entregar

- [ ] Todas as cenas obrigatórias foram mostradas funcionando.
- [ ] Vídeo com áudio legível e duração de até 25 minutos.
- [ ] Link do vídeo abre para o avaliador.
- [ ] Relatório identifica nomes, RMs e usernames e contém links do repositório e do vídeo.
- [ ] Os quatro prints estão legíveis e com legenda de contexto/data.
- [ ] Arquitetura OTel e escolhas New Relic/PagerDuty justificadas.
- [ ] Nenhuma credencial aparece no vídeo, nos prints ou no repositório.
