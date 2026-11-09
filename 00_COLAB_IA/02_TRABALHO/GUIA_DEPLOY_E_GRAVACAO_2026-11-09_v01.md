# Guia de deploy e gravação do vídeo

TL;DR: passo a passo em Git Bash para subir o ambiente, gravar o vídeo da Fase 4, tirar os prints do relatório e encerrar a conta depois. Conta cerca de 2 h até o ambiente ficar pronto; ligado, custa US$ 0,41/h. Detalhe e justificativa de cada passo no [roteiro v02](PREPARACAO_B3_2026-11-05_v02.md).

Última atualização: 2026-11-09, Claude (Opus 5.5). Comandos conferidos contra o código; nada foi executado na AWS.

## Parte 1 — Subir o ambiente

Use uma janela de **Git Bash** na raiz do repositório, na `dev`. Nada desta parte vai para o vídeo. **Não mostre em tela** nenhuma saída de senha.

### 1. Conferir o ponto de partida (1 min)

```bash
cd /c/Users/Gabriel/Documents/GitHub/tech-challenge-04
git switch dev
git pull origin dev
git status --short --branch
aws sts get-caller-identity --query Arn --output text
aws freetier get-account-plan-state --region us-east-1 --query accountPlanRemainingCredits
```

Esperado: `dev` limpa, usuário `fase4` e US$ 120 ou perto disso.

Se um `git push` travar ou abrir login, use a credencial do `gh` só nesse comando:

```bash
git -c credential.helper= -c "credential.helper=!gh auth git-credential" push origin dev
```

### 2. Camada base (5–10 min)

```bash
terraform -chdir=terraform init -backend-config=backend.hcl -input=false
terraform -chdir=terraform plan -input=false -out=base.tfplan
terraform -chdir=terraform show -no-color base.tfplan | grep -E "^Plan:|must be replaced"
```

Esperado, como no plano conferido em 2026-11-09: `Plan: 8 to import, 29 to add, 7 to change, 0 to destroy` e nenhum `must be replaced`. Se houver destroy ou replace, **pare**. Se estiver certo:

```bash
terraform -chdir=terraform apply base.tfplan
```

### 3. Variables do GitHub (1 min)

```bash
gh variable set AWS_SELF_HEALING_ROLE_ARN --body "$(terraform -chdir=terraform output -raw self_healing_role_arn)"
gh variable set EKS_CLUSTER_NAME --body togglemaster
gh variable list
```

Esperado: 5 Variables, somando `AWS_REGION`, `AWS_ROLE_ARN` e `ECR_REGISTRY`, que já existem.

Se o `gh` perguntar `Paste your variable`, o valor veio vazio porque a base não foi aplicada. Não cole nada: aperte `Ctrl+C`, rode o `apply` do passo 2 e repita.

### 4. Camada cluster (15–20 min)

```bash
terraform -chdir=terraform/cluster init -backend-config=backend.hcl -input=false
terraform -chdir=terraform/cluster plan -input=false -out=cluster.tfplan
terraform -chdir=terraform/cluster show -no-color cluster.tfplan | grep -E "^Plan:|must be replaced"
terraform -chdir=terraform/cluster apply cluster.tfplan
aws eks update-kubeconfig --name togglemaster --region us-east-2
kubectl get nodes
```

Esperado: 2 nós `Ready`.

### 5. Preencher o overlay com os valores reais (3 min)

Troca os marcadores por Redis, SQS e as 2 roles IRSA. O ID da conta entra no repositório público; é um identificador, não uma credencial.

```bash
REDIS=$(terraform -chdir=terraform/cluster output -raw redis_url)
FILA=$(terraform -chdir=terraform output -raw sqs_queue_url)
ROLES=$(terraform -chdir=terraform/cluster output -json irsa_role_arns)
ROLE_EVAL=$(echo "$ROLES" | py -3.14 -c "import json,sys; print(json.load(sys.stdin)['evaluation'])")
ROLE_ANA=$(echo "$ROLES" | py -3.14 -c "import json,sys; print(json.load(sys.stdin)['analytics'])")
sed -i "s#redis://redis.conta-pendente.invalid:6379#$REDIS#" gitops/overlays/prod/patches/endpoints.yaml
sed -i "s#https://sqs.conta-pendente.invalid/togglemaster-events#$FILA#g" gitops/overlays/prod/patches/endpoints.yaml
sed -i "s#arn:aws:iam::CONTA_AWS_PENDENTE:role/togglemaster-evaluation-irsa#$ROLE_EVAL#" gitops/overlays/prod/patches/irsa.yaml
sed -i "s#arn:aws:iam::CONTA_AWS_PENDENTE:role/togglemaster-analytics-irsa#$ROLE_ANA#" gitops/overlays/prod/patches/irsa.yaml
py -3.14 -B 00_COLAB_IA/02_TRABALHO/preflight-b3-2026-11-05/checar_overlay.py pre-pr
```

Esperado: `OK: SQS, Redis e as duas identidades IRSA conferidos`. Com o OK:

```bash
git add gitops/overlays/prod/patches/endpoints.yaml gitops/overlays/prod/patches/irsa.yaml
git commit -m "chore(gitops): preenche endpoints e roles IRSA da conta"
git push origin dev
```

### 6. Instalar só o ArgoCD (5 min)

Carrega as 4 chaves do `.env` sem imprimir nada. O `TF_VAR_github_token` fica de fora de propósito: com o repositório público, o ArgoCD não precisa de credencial. Assim o token com escrita não vai para o cluster.

```bash
carrega() { grep -E "^$1=" .env | head -1 | cut -d= -f2- | sed -e 's/\r$//' -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//"; }
export TF_VAR_new_relic_license_key="$(carrega NEW_RELIC_LICENSE_KEY)"
export TF_VAR_pagerduty_integration_key="$(carrega PAGERDUTY_INTEGRATION_KEY)"
export TF_VAR_slack_webhook_url="$(carrega SLACK_WEBHOOK_URL)"
export TF_VAR_github_dispatch_token="$(carrega GITHUB_DISPATCH_TOKEN)"
for v in TF_VAR_new_relic_license_key TF_VAR_pagerduty_integration_key TF_VAR_slack_webhook_url TF_VAR_github_dispatch_token; do [ -n "${!v}" ] && echo "$v ok" || echo "$v VAZIA"; done
terraform -chdir=terraform/k8s init -backend-config=backend.hcl -input=false
terraform -chdir=terraform/k8s plan -input=false -target=helm_release.argocd -out=argocd.tfplan
terraform -chdir=terraform/k8s apply argocd.tfplan
kubectl wait --for=condition=Established crd/applications.argoproj.io --timeout=180s
kubectl get pods -n argocd
kubectl get deploy argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
```

Esperado: 4 variáveis ok, pods `Running` e imagem `quay.io/argoproj/argocd:v2.13.9`. Mantenha esta janela aberta: as variáveis só existem nela.

### 7. PR da dev para a main (10–15 min)

O PR constrói e escaneia as 5 imagens, sem publicar.

```bash
gh pr create --base main --head dev --title "Fase 4: observabilidade, resposta a incidentes e self-healing" --body "Stack de observabilidade por GitOps, instrumentacao dos servicos, alerta, PagerDuty, Slack e self-healing."
gh pr checks dev --watch
```

Se o `gh pr checks` disser que ainda não há checks, espere 30 s e repita. **Confira se tudo está verde antes do merge:** o GitHub não bloqueia o botão com check vermelho. Se o `image-scan` reprovar por uma vulnerabilidade CRITICAL nova, pare e me chame. Se estiver verde:

```bash
gh pr merge dev --merge
```

Nunca use `--delete-branch`.

### 8. Acompanhar a publicação (5–10 min)

O merge roda os 5 pipelines: imagem, Trivy, login OIDC real, push no ECR e gravação da tag.

```bash
gh run list --branch main --limit 12 --json workflowName,status,conclusion --jq '.[] | "\(.workflowName): \(.status) \(.conclusion)"'
```

Repita até os 5 serviços ficarem `completed success`. Depois confira tags e imagens numa cópia limpa da `main`:

```bash
SHA=$(gh pr list --state merged --base main --head dev --limit 1 --json mergeCommit --jq '.[0].mergeCommit.oid')
git fetch origin
git worktree add --detach ../tc04-main origin/main
py -3.14 -B 00_COLAB_IA/02_TRABALHO/preflight-b3-2026-11-05/checar_overlay.py pre-sync --checkout ../tc04-main --sha-publicacao "$SHA"
git worktree remove ../tc04-main
```

Esperado: as 2 linhas `OK`. **Só avance com elas:** sem isso, o ArgoCD tentaria subir imagens que não existem.

### 9. Criar as Applications (5 min, mais 10 min de sincronização)

Na mesma janela do passo 6:

```bash
terraform -chdir=terraform/k8s plan -input=false -out=k8s.tfplan
terraform -chdir=terraform/k8s show -no-color k8s.tfplan | grep -E "^Plan:|must be replaced"
terraform -chdir=terraform/k8s apply k8s.tfplan
kubectl get applications -n argocd
kubectl get pods -n togglemaster
kubectl get pods -n observability
```

Repita os 3 últimos até as **6 Applications** ficarem `Synced`/`Healthy` (`togglemaster`, `observability`, `kube-prometheus-stack`, `loki`, `otel-gateway`, `otel-agent`) e os pods, `Running`. Se uma travar: `kubectl describe application <nome> -n argocd | tail -20`.

### 10. Criar as tabelas, a chave real e os dados (5 min)

Os bancos RDS nascem vazios, e a chave do evaluation é provisória.

```bash
AUTH_DB=$(kubectl get secret auth-service-secret -n togglemaster -o jsonpath='{.data.DATABASE_URL}' | base64 -d)
FLAG_DB=$(kubectl get secret flag-service-secret -n togglemaster -o jsonpath='{.data.DATABASE_URL}' | base64 -d)
kubectl run psql-auth --rm -i --restart=Never -n togglemaster --image=postgres:16-alpine -- psql "$AUTH_DB" -v ON_ERROR_STOP=1 < services/auth-service/db/init.sql
kubectl run psql-flag --rm -i --restart=Never -n togglemaster --image=postgres:16-alpine -- psql "$FLAG_DB" -v ON_ERROR_STOP=1 < services/flag-service/db/init.sql
kubectl port-forward svc/auth-service -n togglemaster 8001:8001 >/dev/null 2>&1 &
kubectl port-forward svc/flag-service -n togglemaster 8002:8002 >/dev/null 2>&1 &
kubectl port-forward svc/targeting-service -n togglemaster 8003:8003 >/dev/null 2>&1 &
sleep 3
MASTER=$(kubectl get secret auth-service-secret -n togglemaster -o jsonpath='{.data.MASTER_KEY}' | base64 -d)
CHAVE=$(curl -s -X POST http://localhost:8001/admin/keys -H "Content-Type: application/json" -H "Authorization: Bearer $MASTER" -d '{"name":"demo-fase4"}' | sed -E 's/.*"key":"([^"]+)".*/\1/')
echo "tamanho da chave: ${#CHAVE}"
kubectl create secret generic evaluation-service-secret -n togglemaster --from-literal=SERVICE_API_KEY="$CHAVE" --dry-run=client -o yaml | kubectl apply -f -
kubectl rollout restart deployment/evaluation-service -n togglemaster
kubectl rollout status deployment/evaluation-service -n togglemaster
curl -s -X POST http://localhost:8002/flags -H "Content-Type: application/json" -H "Authorization: Bearer $CHAVE" -d '{"name":"novo-painel","description":"Painel novo","is_enabled":true}'; echo
curl -s -X POST http://localhost:8003/rules -H "Content-Type: application/json" -H "Authorization: Bearer $CHAVE" -d '{"flag_name":"novo-painel","is_enabled":true,"rules":{"type":"PERCENTAGE","value":100}}'; echo
kill %1 %2 %3
```

Esperado: tamanho maior que 0 e 2 JSONs com `novo-painel`.

### 11. Aceite funcional (3 min)

```bash
kubectl port-forward svc/evaluation-service -n togglemaster 8004:8004 >/dev/null 2>&1 &
sleep 3
curl -s "http://localhost:8004/evaluate?flag_name=novo-painel&user_id=user-1"; echo
sleep 20
aws dynamodb scan --table-name ToggleMasterAnalytics --region us-east-2 --select COUNT --query Count
kill %1
```

Esperado: `"result":true` e contagem maior que 0. Isso prova a cadeia evaluation → SQS → analytics → DynamoDB. Se vier 502, a chave do passo 10 não foi lida: repita o `rollout restart` do evaluation.

### 12. Deixar tudo pronto para gravar

**Tráfego contínuo.** Roda dentro do cluster, então não cai quando o flag-service reinicia. Abra uma janela nova:

```bash
CHAVE=$(kubectl get secret evaluation-service-secret -n togglemaster -o jsonpath='{.data.SERVICE_API_KEY}' | base64 -d)
kubectl run trafego -n togglemaster --image=curlimages/curl:8.11.1 --restart=Never --env="CHAVE=$CHAVE" --command -- sh -c 'while true; do c=$(curl -s -o /dev/null -w "%{http_code}" -m 5 -H "Authorization: Bearer $CHAVE" http://flag-service:8002/flags); curl -s -o /dev/null -m 5 "http://evaluation-service:8004/evaluate?flag_name=novo-painel&user_id=u$(date +%s)"; echo "$(date +%T) flag-service /flags -> $c"; sleep 1; done'
```

**Telas web**, uma janela de Git Bash para cada túnel:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:80
```

```bash
kubectl -n observability port-forward svc/grafana 3000:80
```

```bash
kubectl port-forward svc/evaluation-service -n togglemaster 8004:8004
```

**Senhas, antes de gravar.** Cada comando copia a senha para a área de transferência, sem mostrá-la na tela.

ArgoCD, http://localhost:8080, usuário `admin`:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d | clip
```

Grafana, http://localhost:3000, usuário `admin`:

```bash
kubectl -n observability get secret grafana-admin -o jsonpath='{.data.admin-password}' | base64 -d | clip
```

Entre nas duas telas. Deixe logados também New Relic, PagerDuty, Slack (`#incidentes-tech-challenge`) e GitHub Actions.

### 13. Ensaio obrigatório, antes de gravar

Rode a Cena 6 inteira uma vez, sem gravar. Confira alerta, incidente, Slack, workflow e restart.

**Depois do ensaio, espere pelo menos 10 minutos.** O self-healing tem cooldown de 600 s: dentro desse prazo, o segundo disparo **não reinicia** e a demonstração falha na frente da câmera. Confirme também que o alerta voltou a `Normal` e que o incidente do ensaio foi resolvido.

### Se algo travar

- **Túnel com `address already in use`:** um `port-forward` antigo segue vivo. Encerre todos com `taskkill //IM kubectl.exe //F` e abra de novo.
- **Pod `CrashLoopBackOff` ou `ImagePullBackOff`:** `kubectl describe pod <pod> -n <namespace> | tail -20` e `kubectl logs <pod> -n <namespace>`.
- **Application travada:** `kubectl describe application <nome> -n argocd | tail -20`.
- **Alerta não dispara:** confira no log do `trafego` se há `-> 503`; o `/flags` precisa estar recebendo tráfego.
- **Self-healing termina em `cooldown`:** faz menos de 10 min do último restart. Espere e repita.

## Parte 2 — Guia de gravação

O PDF da FIAP, nas páginas 5 e 6, pede vídeo de **até 25 minutos** e avisa que perde pontos o que não for demonstrado no vídeo ou no relatório. Grave os 4 blocos obrigatórios, marcados com ★.

**Fora de quadro:** senhas e chaves, `kubectl describe pod trafego` (mostra a chave), `.env`, páginas de chave do PagerDuty e do New Relic, webhook do Slack, Secrets e `tfvars`.

### Cena 1 — O projeto (2 min)

- Mostre o README no GitHub, a tabela "Onde está cada requisito" e o diagrama.
- Diga em uma frase: 5 microsserviços, e a Fase 4 acrescenta observabilidade e resposta a incidentes.

### Cena 2 — A base das fases anteriores (2–3 min)

- Pastas `terraform/`, `gitops/` e `services/`.
- GitHub → Actions → o run do `auth-service` do merge: build, lint, SAST, SCA, imagem, Trivy, login OIDC, push no ECR e tag no GitOps.

### ★ Cena 3 — EKS e ArgoCD com a stack nova (3 min)

```bash
kubectl get nodes
kubectl get pods -n togglemaster
kubectl get pods -n observability
kubectl get applications -n argocd
```

- ArgoCD (http://localhost:8080): as 6 Applications `Synced`/`Healthy`; abra a árvore de `observability`.
- Repositório: mostre `gitops/observability/applications` e `values`. Explique que Prometheus, Loki e Grafana são charts Helm entregues por GitOps.

### ★ Cena 4 — Grafana, Loki e OpenTelemetry (4–5 min)

- Dashboard **ToggleMaster - Visao geral**: uso de CPU e memória dos nós e pods (recursos do cluster), requisições por segundo por serviço, erros, latência e o painel de logs em tempo real.
- Explore → Loki, para a busca de logs:

```text
{k8s_namespace_name="togglemaster"} |= "flag-service"
```

- Explique a rota do OTel, com o diagrama do README e `gitops/observability/values/otel-gateway.yaml`:
  - os serviços enviam traces ao **gateway**;
  - os **agents** (DaemonSet) leem os logs dos contêineres em cada nó e os mandam ao gateway;
  - o gateway envia traces ao New Relic, logs ao Loki e, pelo conector `spanmetrics`, métricas ao Prometheus.

### ★ Cena 5 — New Relic: Service Map e trace (4 min)

Crie uma flag nova para garantir uma requisição sem cache, com o caminho completo. Use a janela do passo 12 onde a variável `CHAVE` existe; o túnel 8004 segue aberto na outra janela:

```bash
kubectl run nova-flag -n togglemaster --rm -i --restart=Never --image=curlimages/curl:8.11.1 --env="CHAVE=$CHAVE" --command -- sh -c 'curl -s -X POST http://flag-service:8002/flags -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"name\":\"video-trace\",\"is_enabled\":true}"; curl -s -X POST http://targeting-service:8003/rules -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"flag_name\":\"video-trace\",\"is_enabled\":true,\"rules\":{\"type\":\"PERCENTAGE\",\"value\":100}}"'
curl -s "http://localhost:8004/evaluate?flag_name=video-trace&user_id=video-1"; echo
```

- New Relic → **APM & Services** → `evaluation-service` → **Service map**: os 5 serviços.
- **Distributed tracing** → filtre por `evaluation-service` e abra o trace mais recente de `/evaluate`, com mais spans. Mostre o caminho entre os serviços, a chamada ao Redis, a publicação no SQS e a duração de cada etapa.

### ★ Cena 6 — A prova do incidente (6–7 min)

Tudo visível: à esquerda, o terminal; à direita, as abas do navegador. Em 2 janelas de terminal:

```bash
kubectl logs -f trafego -n togglemaster
```

```bash
kubectl get pods -n togglemaster -l app=flag-service -w
```

Abas: Grafana → **Alerting → Alert rules** (`FlagService5xxAlto`), PagerDuty → **Incidents**, Slack → `#incidentes-tech-challenge`, GitHub → **Actions → self-healing**.

1. **Mostre o normal:** o log do tráfego em `-> 200`.
2. **Cause a falha,** e explique que o `/health` continua saudável, então o Kubernetes sozinho não resolveria:

```bash
kubectl run falha -n togglemaster --rm -i --restart=Never --image=curlimages/curl:8.11.1 --env="CHAVE=$CHAVE" --command -- sh -c 'curl -s -X POST http://flag-service:8002/admin/fault -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"enabled\": true}"'
```

3. **O log passa a `-> 503`.** No dashboard, o painel de erros 5xx sobe.
4. **Em 1 a 3 min:** alerta `Pending` e depois **Firing**.
5. **PagerDuty:** incidente aberto sozinho. Abra e mostre os detalhes.
6. **Slack:** a mensagem detalhada do Grafana e o cartão do PagerDuty.
7. **GitHub Actions:** o run do `self-healing`, disparado por `repository_dispatch`. Abra o passo **Reiniciar com allowlist e cooldown**.
8. **Terminal:** o pod antigo `Terminating` e o novo `Running`. **Esse é o momento que a FIAP pede.**
9. **Recuperação:** o log volta a `-> 200`; em 1 a 2 min, o alerta volta a `Normal`, o incidente fica `Resolved` e o Slack avisa.

Se o tempo sobrar, feche com uma frase sobre o caminho: falha → métrica → alerta → incidente → comunicação → correção automática → recuperação.

## Parte 3 — Prints para o relatório

Tire **durante a gravação ou logo depois, antes do destroy**: sem o cluster, não dá para refazer. Salve em `docs/evidencias/`, confira cada imagem antes de versionar e cubra chaves e e-mails, porque o repositório é público.

### Obrigatórios pelo PDF (p. 6)

| # | Print | Onde |
|---|---|---|
| 1 | **Dashboard do Grafana** | http://localhost:3000 → Dashboards → ToggleMaster - Visao geral, com dados e, de preferência, com o pico de erros |
| 2 | **Trace do APM** | New Relic → Distributed tracing → o trace do `/evaluate` aberto, com os spans dos serviços |
| 3 | **Notificação no ChatOps** | Slack → `#incidentes-tech-challenge` → a mensagem do alerta, e o cartão do PagerDuty se couber |
| 4 | **Execução do self-healing** | GitHub → Actions → self-healing → o run, com o passo **Reiniciar com allowlist e cooldown** aberto; e o terminal com o pod novo |

### Recomendados, para sustentar o que o PDF pede

| # | Print | Onde |
|---|---|---|
| 5 | Service Map com os 5 serviços | New Relic → APM & Services → evaluation-service → Service map |
| 6 | Alerta em Firing | Grafana → Alerting → Alert rules → FlagService5xxAlto |
| 7 | Incidente aberto e depois resolvido | PagerDuty → Incidents → o incidente |
| 8 | Busca de logs no Loki | Grafana → Explore → Loki |
| 9 | ArgoCD com as 6 Applications Synced/Healthy | http://localhost:8080 → Applications |
| 10 | Pods e nós | Terminal: `kubectl get nodes` e `kubectl get pods -A` |
| 11 | CI/CD com publicação | GitHub → Actions → run do merge → jobs `image` e `gitops`, e o passo do OIDC |

### O que mais o relatório precisa ter (p. 6)

- Nomes, RMs e usernames.
- Links do repositório e do vídeo.
- Justificativa técnica da arquitetura OTel.
- Justificativa das escolhas de **New Relic em vez de Datadog** e de **PagerDuty em vez de OpsGenie**.

## Parte 4 — Encerrar, depois de gravar

**Só depois** de conferir que vídeo e prints estão bons. Dá para fazer em 30 min, e cada hora ligada custa US$ 0,41.

```bash
terraform -chdir=terraform/k8s plan -destroy -input=false -out=k8s-destroy.tfplan
terraform -chdir=terraform/k8s apply k8s-destroy.tfplan
terraform -chdir=terraform/cluster plan -destroy -input=false -out=cluster-destroy.tfplan
terraform -chdir=terraform/cluster apply cluster-destroy.tfplan
aws ec2 describe-volumes --region us-east-2 --filters Name=status,Values=available --query 'Volumes[].[VolumeId,Size]' --output table
```

- Use plano salvo no destroy, nunca o `destroy` interativo: num bloco colado, a linha seguinte pode virar a resposta do `yes`.
- A janela do destroy da k8s precisa das variáveis do passo 6.
- Se o destroy da k8s demorar, é o ArgoCD removendo os recursos: espere.
- Apague os volumes EBS que sobrarem, depois de conferir: `aws ec2 delete-volume --volume-id <id> --region us-east-2`.
- **A base fica de fora por enquanto:** ela guarda os 5 ECR e a identidade do CI. Para zerar quase todo o custo, desligue o NAT com plano próprio: `terraform -chdir=terraform plan -var enable_nat_gateway=false -out=sem-nat.tfplan`, confira e aplique. O destroy da base é uma decisão à parte, depois da entrega.
- Depois do destroy confirmado nas 2 camadas, apague os caches `.terraform` e os `*.tfplan`.
- Sincronize a `dev` com os commits do robô na `main`, antes de novas mudanças: `git switch dev`, `git pull origin main` e `git push origin dev`.
