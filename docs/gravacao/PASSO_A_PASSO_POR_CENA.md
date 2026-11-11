# 🎬 Gravação passo a passo, cena por cena

TL;DR: o que abrir, onde clicar e que comando rodar em cada uma das 10 cenas do [roteiro](README.md). As falas estão no roteiro; aqui, cada frase vira uma ação na tela. Conferido no cluster em 2026-11-10, às 23:45:
- tráfego em HTTP 200;
- seis Applications Synced/Healthy;
- chave de serviço válida (71 caracteres);
- nenhum self-healing desde o ensaio de 2026-11-09, então não há cooldown pendente.

Shell: Git Bash. Cada bloco é um comando; copie e cole, sem usar o botão Run.

As seções do README citadas aqui são as da versão **publicada na `main`**, que é a que o GitHub mostra no vídeo. A versão local reorganizada ainda não foi publicada.

## 0. Montar a mesa antes do REC (15 min)

### 0.1 Janelas

| Janela | Para quê | Aparece no vídeo? |
|---|---|---|
| Terminal D | túneis 8080, 3000 e 8004 | não, fica minimizado |
| Terminal A | log do pod `trafego` | sim, cenas 07 a 09 |
| Terminal B | pods do flag-service em watch | sim, cenas 07 a 09 |
| Terminal C | comandos da demonstração | sim, cenas 03, 06 e 07 |
| Lens | Nodes e Pods | sim, cena 03 |
| Brave | 12 abas, na ordem das cenas (0.5) | sim |

**Deixe o Docker Desktop fechado.** Em 2026-11-09, os contêineres locais ocupavam as portas 8001–8005 e responderam no lugar do cluster.

### 0.2 Terminal D: abrir os três túneis

Confira se as portas estão livres:

```bash
for p in 8080 3000 8004; do netstat -ano | grep -q ":$p .*LISTENING" && echo "porta $p OCUPADA" || echo "porta $p livre"; done
```

Esperado: as três `livre`. Depois, abra os túneis. Cada um roda num laço que o reabre sozinho em 2 s se cair:

```bash
(while true; do kubectl -n argocd port-forward svc/argocd-server 8080:80; sleep 2; done) > /tmp/tunel-argocd.log 2>&1 &
```
```bash
(while true; do kubectl -n observability port-forward svc/grafana 3000:80; sleep 2; done) > /tmp/tunel-grafana.log 2>&1 &
```
```bash
(while true; do kubectl -n togglemaster port-forward svc/evaluation-service 8004:8004; sleep 2; done) > /tmp/tunel-evaluation.log 2>&1 &
```

Espere 5 segundos e confira:

```bash
for u in http://127.0.0.1:8080 http://127.0.0.1:3000/api/health http://127.0.0.1:8004/health; do echo "$(curl -s -o /dev/null -w '%{http_code}' -m 5 $u) $u"; done
```

Esperado: três linhas começando com `200`. Se alguma falhar, leia o log dela, por exemplo `tail -5 /tmp/tunel-grafana.log`. Minimize a janela D e não a feche: os túneis morrem junto.

### 0.3 Terminais A e B

Terminal A, tráfego:

```bash
kubectl logs -f trafego -n togglemaster --tail=5
```

Terminal B, pods do flag-service:

```bash
kubectl get pods -n togglemaster -l app=flag-service -w
```

Esperado: A mostra `flag-service /flags -> 200` a cada segundo; B mostra 1 pod `Running`.

### 0.4 Terminal C: logins, sem mostrar senha

Senha do ArgoCD na área de transferência (usuário `admin`, http://localhost:8080):

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d | clip
```

Senha do Grafana (usuário `admin`, http://localhost:3000):

```bash
kubectl -n observability get secret grafana-admin -o jsonpath='{.data.admin-password}' | base64 -d | clip
```

Depois dos dois logins, limpe a tela com `clear`.

### 0.5 Abas do Brave, da esquerda para a direita

| Aba | Endereço ou caminho | Cena |
|---|---|---|
| 1 | GitHub → README do repositório | 01 e 10 |
| 2 | GitHub → pasta `terraform/` | 02 e 03 |
| 3 | GitHub Actions → [run do auth-service no merge](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42656296219) | 02 |
| 4 | ArgoCD → Applications (http://localhost:8080) | 03 |
| 5 | Grafana → Dashboards → ToggleMaster - Visao geral, período **Last 15 minutes**, atualização **10s** | 04 e 07 |
| 6 | Grafana → Explore → Loki | 05 |
| 7 | Grafana → Alerting → Alert rules → FlagService5xxAlto | 08 e 09 |
| 8 | New Relic → APM & Services → evaluation-service → Service map (ou Maps) | 06 |
| 9 | New Relic → Distributed tracing | 06 |
| 10 | PagerDuty → Incidents | 08 e 09 |
| 11 | Slack → `#incidentes-tech-challenge` | 08 e 09 |
| 12 | GitHub Actions → workflow **self-healing** (lista de runs) | 09 |

No Lens, deixe aberto o cluster `togglemaster` na tela **Nodes**.

### 0.6 Última conferência no Terminal C

```bash
kubectl get pods -n togglemaster -l app=flag-service
```

O pod precisa ter mais de 10 minutos (`AGE`). Se você fizer um ensaio, espere 10 minutos depois dele: o self-healing recusa um segundo restart dentro do cooldown de 600 s.

## 1. As cenas

Cada linha diz: quando a fala chegar naquele trecho, faça isso, naquele lugar.

### 01 · Apresente o problema (00:00–01:00) · aba 1

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "Este é o ToggleMaster…" | topo do README | título e "cinco microsserviços" |
| "Mantivemos Terraform, CI/CD… Agora acrescentamos…" | role até **O que foi reaproveitado e o que a Fase 4 acrescentou** | coluna da base ao lado da coluna da Fase 4 |
| "Vou demonstrar o ambiente funcionando…" | role até **Arquitetura de observabilidade e resposta** e, logo abaixo, **Serviços e arquitetura da base** | o diagrama e a tabela dos cinco serviços com as portas |

### 02 · Mostre a base automatizada (01:00–03:00) · abas 2 e 3

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "…três camadas Terraform…" | aba 2: aponte `terraform/` (base), `terraform/cluster` e `terraform/k8s` | as três pastas |
| "…o state fica no backend S3…" | aba 1, seção **Terraform e ArgoCD** do README (ou `backend.tf` de uma camada) | o parágrafo "O backend guarda o state, não o código" |
| "Os cinco serviços possuem pipelines…" | aba 3: o grafo de jobs do run | Build e testes, Linter, SAST, SCA, Imagem e push no ECR, Atualizar tag no GitOps |
| "…análise do código e das dependências" | clique em **SAST (gosec)** e em **SCA (Trivy fs)** | os jobs verdes |
| "No pull request, a imagem também é construída…" | abra o [PR #1 → Checks](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/pull/1/checks) | **Imagem Docker e Trivy (sem push)** verde |
| "No push da main, o pipeline publica no ECR usando OIDC…" | volte à aba 3 → job **Imagem Docker e push no ECR** | passos **Scan da imagem com Trivy**, **Autenticar na AWS via OIDC** e **Push para o ECR** |
| "…e atualiza a tag no GitOps" | job **Atualizar tag no GitOps** | o commit `chore(gitops): auth-service para v1.0.0-…` |

### ★ 03 · Prove EKS + GitOps (03:00–05:00) · Lens, Terminal C, aba 4

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "Este é o cluster EKS…" | Lens → **Nodes** | 2 nós `Ready`, versão v1.34 |
| "…os pods das aplicações e da observabilidade" | Lens → **Workloads → Pods**; filtre o namespace `togglemaster` e depois `observability` | tudo `Running` |
| (opcional, reforça a prova) | Terminal C: os 2 comandos abaixo | nós `Ready` e 6 Applications |
| "No ArgoCD, as seis aplicações…" | aba 4 | 6 cartões `Synced` e `Healthy` |
| "A aplicação observability organiza…" | clique em **observability** | árvore com kube-prometheus-stack, loki, otel-gateway e otel-agent |
| "Os valores dos charts… estão versionados" | aba 2 → `gitops/observability/values` e `gitops/observability/grafana` | os arquivos de values, o dashboard e os alertas |

```bash
kubectl get nodes
```
```bash
kubectl get applications -n argocd
```

### ★ 04 · Leia a saúde no Grafana (05:00–08:00) · aba 5

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "A taxa de requisições…" | painel **Requisicoes por segundo por servico** | uma linha por serviço HTTP |
| "A proporção de erros…" | painéis **flag-service: erros 5xx agora** e **Taxa de erro (5xx) por servico** | 0% antes da falha |
| "…a latência p95…" | painel **Latencia p95 por servico** | milissegundos por serviço |
| "Mais abaixo, CPU e memória…" | role até **CPU/Memoria por no** e **CPU/Memoria por pod** | 2 nós e os pods do togglemaster |
| "O painel de logs consulta o Loki" | role até **Logs da aplicacao (Loki)** | linhas recentes |
| "Analytics processa eventos…" | volte ao painel de requisições | o analytics consome a fila e não tem a mesma linha HTTP |
| "Vou conferir o intervalo…" | canto superior direito: período e atualização | Last 15 minutes e 10s |

📸 **PRINT 01:** o dashboard inteiro; se não couber, use duas imagens (métricas; recursos e logs).

### ★ 05 · Conecte logs, métricas e traces (08:00–10:00) · aba 6 e aba 1

No Explore, escolha a fonte **Loki**, mude para **Code** e rode:

```logql
{k8s_namespace_name="togglemaster", service_name="evaluation-service"} |= "trace_id"
```

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "Aqui consulto logs centralizados pelo Loki" | rode a consulta acima | linhas com `"event":"sqs.published"` |
| "O trace_id permite correlacionar…" | abra uma linha | `service.name`, horário e `trace_id` |
| (para mostrar outro serviço) | troque por `{k8s_namespace_name="togglemaster", service_name="flag-service"}` | linhas `http.request.completed` |
| "Em cada nó, um Collector agent…" | aba 1, diagrama do README; ou `gitops/observability/values/otel-gateway.yaml`, seção `pipelines` | traces → New Relic e spanmetrics; métricas → Prometheus; logs → Loki |
| (opcional) | aba 1, seção **Pods, nós e distribuição do Collector** | "dois agents e um gateway" |
| "As métricas de infraestrutura…" | Lens → Pods → `observability` | `kps-prometheus-node-exporter` e `kps-kube-state-metrics` |

### ★ 06 · Siga uma requisição no APM (10:00–13:00) · abas 8 e 9, Terminal C

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "No mapa, observamos as dependências…" | aba 8 | os cinco serviços ligados; amplie as dependências se precisar |
| "Agora faço uma requisição…" | Terminal C: os 2 comandos abaixo | `Flag criada: video-…` e `"result":true` |
| "No trace detalhado…" | aba 9 → filtre `evaluation-service` → **GET /evaluate** → abra o trace do horário do curl com mais spans | a cascata: evaluation → flag-service e targeting → auth `/validate`, Redis e SQS |
| "O caminho varia: um acerto no Redis…" | aponte o span do Redis | — |
| "O fluxo de SQS e analytics é assíncrono…" | aponte o span de publicação na SQS | a resposta HTTP termina sem esperar o analytics |
| "A duração de cada span…" | clique no span mais longo | duração e atributos |

Crie uma flag exclusiva. O cache é por nome da flag, então só uma flag nova garante o caminho completo. A chave fica dentro do pod e não aparece:

```bash
kubectl exec -n togglemaster trafego -- sh -c 'NOME="video-$(date +%s)"; curl --fail-with-body -s -X POST http://flag-service:8002/flags -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"name\":\"$NOME\",\"description\":\"Demonstracao Fase 4\",\"is_enabled\":true}" >/dev/null && curl --fail-with-body -s -X POST http://targeting-service:8003/rules -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"flag_name\":\"$NOME\",\"is_enabled\":true,\"rules\":{\"type\":\"PERCENTAGE\",\"value\":100}}" >/dev/null && echo "Flag criada: $NOME"'
```

Troque `NOME_DA_FLAG` pelo nome impresso:

```bash
curl -s "http://127.0.0.1:8004/evaluate?flag_name=NOME_DA_FLAG&user_id=video-1"; echo
```

O trace leva de 10 a 60 segundos para aparecer no New Relic. Preencha esse tempo com a fala do mapa.

📸 **PRINT 02:** o trace aberto, com ID, serviço de entrada, spans e durações. A lista de traces não basta.

### ★ 07 · Provoque a falha controlada (13:00–15:00) · Terminais A, B e C, aba 5

Antes, posicione: terminais à esquerda (A em cima, B embaixo, C ao lado) e o Brave à direita.

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "Agora vou provocar uma falha transitória…" | aponte o Terminal A | `-> 200` |
| "A rota administrativa exige autenticação…" | Terminal C: comando de falha abaixo | `{"fault_enabled": true}` ou equivalente |
| "…faz as rotas de flags responderem 503" | Terminal A | passa a `-> 503` |
| "O health check continua saudável…" | Terminal C: comando do `/health` abaixo; aponte o Terminal B | `200`, e o pod `Running` com 0 restarts |
| "O tráfego contínuo permite medir a proporção de erros" | aba 5 | **flag-service: erros 5xx agora** sobe em 30 a 60 s |
| "Vou observar a cadeia sem clicar em Run workflow…" | tire as mãos do teclado | — |

```bash
kubectl exec -n togglemaster trafego -- sh -c 'curl --fail-with-body -s -X POST http://flag-service:8002/admin/fault -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"enabled\":true}"'; echo
```
```bash
kubectl exec -n togglemaster trafego -- curl -s -o /dev/null -w "health: %{http_code}\n" http://flag-service:8002/health
```

### ★ 08 · Acompanhe alerta e comunicação (15:00–17:00) · abas 7, 10 e 11

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "A regra avalia a proporção de erros 5xx…" | aba 7, abra **FlagService5xxAlto** | `Pending` 30 a 60 s depois da falha; `Firing` cerca de 1 min depois |
| "Quando entra em Firing, o Grafana abre um incidente…" | aba 10 | incidente **Triggered** criado sozinho; abra os detalhes |
| "…e envia o contexto ao Slack" | aba 11 | mensagem `[FIRING:1] FlagService5xxAlto - flag-service` e o cartão do PagerDuty |
| "Aqui confiro serviço, horário e descrição…" | aponte **Servico**, **Detalhe** e **Inicio** | o mesmo horário do Firing |

A linha **O que aconteceu** da mensagem do Slack mostra o texto do modelo (`{{ humanizePercentage … }}`) em vez do percentual. A correção não foi publicada no cluster. Leia só serviço, detalhe e horário; a regra e a automação não dependem dessa linha.

📸 **PRINT 03:** a mensagem do incidente no Slack. Como apoio, o Firing da aba 7 e o incidente da aba 10.

### ★ 09 · Prove a correção automática (17:00–20:00) · aba 12, Terminais A e B, abas 7, 10 e 11

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "O mesmo alerta chama o webhook do GitHub…" | aba 12, atualize a página | run novo com evento `repository_dispatch`, segundos depois do Firing |
| "O workflow assume uma role temporária por OIDC" | abra o run → job → passo **Assumir a role do self-healing (OIDC)** | passo verde |
| "…valida o serviço em uma lista permitida…" | expanda **Reiniciar com allowlist e cooldown** | allowlist e cooldown aprovados, `rollout restart` e resultado `restarted` |
| "Aqui vemos o registro da ação e a substituição do pod" | Terminal B | pod antigo `Terminating`, pod novo `Running` |
| "O tráfego volta a 200…" | Terminal A | `-> 200` de novo |
| "…o alerta retorna ao normal…" | aba 7 | `Normal` 1 a 3 min depois |
| "…e o incidente é resolvido" | abas 10 e 11 | `Resolved` no PagerDuty e `[RESOLVED]` no Slack |

A página de resumo do run também mostra **Alerta: FlagService5xxAlto** e **Evento: repository_dispatch**.

📸 **PRINT 04:** o passo **Reiniciar com allowlist e cooldown** expandido e o Terminal B com o pod novo.

Se a automação falhar, não reinicie à mão como se fosse automático. Para encerrar só a falha, use o comando abaixo e diga no vídeo que houve intervenção:

```bash
kubectl exec -n togglemaster trafego -- sh -c 'curl --fail-with-body -s -X POST http://flag-service:8002/admin/fault -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"enabled\":false}"'; echo
```

### 10 · Feche com as evidências (20:00–21:00) · aba 1

| Quando disser… | Faça | O que deve aparecer |
|---|---|---|
| "Demonstramos a base automatizada…" | aba 1, segundo diagrama de **Arquitetura de observabilidade e resposta** | Grafana → PagerDuty, Slack e GitHub Actions → restart |
| "O repositório reúne o código…" | aba 1, **Onde está cada requisito da Fase 4** | cada requisito apontando para o seu arquivo |
| "O relatório traz os quatro prints…" | abra no Brave o PDF local `docs/relatorio/RELATORIO_ENTREGA_2026-11-10_v02.pdf` | os prints e as justificativas |

O relatório e as evidências ainda não estão no GitHub, por isso mostre o PDF local. Revise o PDF inteiro antes de mostrá-lo.

## 2. Depois do STOP

- **Não mostre na tela:** `.env`, Secrets, `kubectl describe pod trafego`, páginas de chave do PagerDuty e do New Relic, nem o webhook do Slack.
- Confira o vídeo e os 4 prints **antes** de qualquer destroy.
- Salve os prints novos em `docs/evidencias/entrada-local/` e cubra chaves e e-mails.
- Feche o Terminal D para encerrar os túneis. Se uma porta continuar presa, rode `taskkill //IM kubectl.exe //F`; só no fim, porque também fecha os Terminais A e B.
