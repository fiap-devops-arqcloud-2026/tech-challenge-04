# Fatos do B2 (workflow wf_9ab01c7a-69d, 2026-11-03)

Pesquisa em fontes oficiais, 4 frentes. Sem verificacao cetica separada: a verificacao e empirica (validate, render e testes) na implementacao.

## selfhealing
- [confirmado] 1. API repository_dispatch - corpo: `POST /repos/{owner}/{repo}/dispatches | event_type (string, required, <= 100 caracteres) | client_payload (object)` -- O endpoint POST /repos/{owner}/{repo}/dispatches recebe dois campos: event_type (string obrigatória, nome do evento personalizado, com até 100 caracteres) e client_payload (objeto opcional repassado ao workflow). (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] 1. API repository_dispatch - limites do client_payload (REST): `máx. 10 propriedades de 1º nível; tamanho total < 64KB` -- Pela referência REST, o client_payload aceita no máximo 10 propriedades de primeiro nível, e o JSON total precisa ter menos de 64KB. (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] 1. API repository_dispatch - limites (doc do Actions): `máx. 10 top-level properties; máx. 65,535 characters` -- A página de eventos do GitHub Actions repete o limite de 10 propriedades de primeiro nível e expressa o tamanho como no máximo 65.535 caracteres. Há duas formulações oficiais para o tamanho (< 64KB e 65.535 caracteres). (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
- [confirmado] 1. API repository_dispatch - resposta: `204 No Content | 404 | 422` -- Em caso de sucesso, a API devolve 204 No Content, sem corpo. Os erros documentados são 404 (recurso não encontrado) e 422 (validação falhou ou o endpoint foi considerado spam). (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] 1. API repository_dispatch - cabeçalhos: `Authorization: Bearer <TOKEN> | Accept: application/vnd.github+json | X-GitHub-Api-Version: 2026-03-10` -- A referência REST lista os cabeçalhos padrão: Authorization Bearer com o token, Accept application/vnd.github+json e X-GitHub-Api-Version 2026-03-10. Os exemplos em curl omitem esses cabeçalhos. (https://docs.github.com/en/rest/repos/repos)
- [confirmado] 1. Fine-grained PAT - permissão exata: `Repository permissions > Contents: write` -- Com fine-grained personal access token, POST /repos/{owner}/{repo}/dispatches exige a permissão de repositório 'Contents' no nível write, sem permissões adicionais. (https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens#repository-permissions-for-contents)
- [confirmado] 1. PAT clássico / OAuth: `repo` -- Tokens de OAuth app e PAT clássico precisam do escopo repo para usar o endpoint. (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] 1. Fine-grained PAT - alcance de Contents write: `PUT /repos/{owner}/{repo}/contents/{path} | write; DELETE /repos/{owner}/{repo}/contents/{path} | write; POST /repos/{owner}/{repo}/git/refs | write` -- A mesma permissão Contents write também autoriza gravar e apagar arquivos e criar refs pela API. Por isso o token do dispatch é sensível: com ele dá para alterar o código do repositório. (https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens#repository-permissions-for-contents)
- [confirmado] 1. repository_dispatch - só na branch padrão: `GITHUB_SHA: Last commit on default branch | GITHUB_REF: Default branch` -- Confirmado: o evento só dispara um workflow se o arquivo do workflow existir na branch padrão. GITHUB_SHA é o último commit da branch padrão e GITHUB_REF é a própria branch padrão. (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
- [confirmado] 2. Workflow - on.repository_dispatch.types: `on:
  repository_dispatch:
    types: [test_result]` -- Sem filtro, qualquer event_type dispara o workflow. A chave types limita o disparo aos valores de event_type listados. (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
- [confirmado] 2. Workflow - acesso ao client_payload: `if: ${{ !github.event.client_payload.passed }} | env: MESSAGE: ${{ github.event.client_payload.message }} | run: echo $MESSAGE` -- O conteúdo de client_payload fica em github.event.client_payload. O exemplo oficial passa o valor ao shell por env (MESSAGE) e usa a expressão diretamente só no if: do job. (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
- [confirmado] 2. Segurança - script injection: `env:
  TITLE: ${{ github.event.pull_request.title }}
run: ... "$TITLE" ...` -- Para scripts inline, a documentação de segurança do GitHub recomenda colocar o dado não confiável numa variável de ambiente intermediária e usá-la no shell com aspas duplas, em vez de interpolar ${{ }} no run. A primeira opção recomendada é (https://docs.github.com/en/actions/reference/security/secure-use#use-an-intermediate-environment-variable)
- [confirmado] 2. Segurança - pin por SHA: `uses: owner/action@<SHA completo de 40 caracteres> # vX.Y.Z` -- A documentação de segurança do GitHub recomenda fixar actions de terceiros pelo SHA completo do commit e conferir que o SHA vem do repositório original, não de um fork. (https://docs.github.com/en/actions/reference/security/secure-use)
- [confirmado] 2. Workflow - permissão OIDC: `permissions:
  id-token: write` -- Para obter o token OIDC, o workflow ou o job precisa de permissions id-token: write. (https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
- [confirmado] 3. OIDC - sub de branch: `repo:ORG-NAME/REPO-NAME:ref:refs/heads/BRANCH-NAME` -- O sub só inclui a branch quando o job não referencia environment e o evento não é pull request. Formato legado: repo:ORG/REPO:ref:refs/heads/BRANCH. (https://docs.github.com/en/actions/reference/security/oidc#filtering-for-a-specific-branch)
- [confirmado] 3. OIDC - sub com environment: `repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME` -- Quando o job referencia um environment, o sub traz o environment no lugar da ref. (https://docs.github.com/en/actions/reference/security/oidc#filtering-for-a-specific-environment)
- [confirmado] 3. OIDC - sub com IDs imutáveis: `repo:OWNER@OWNER-ID/REPO@REPO-ID:ref:refs/heads/BRANCH (ex.: repo:octo-org@123456/octo-repo@456789:ref:refs/heads/main)` -- Repositórios criados após 15/07/2026 usam por padrão o sub imutável, com o ID do dono e o ID do repositório separados por @. Os mais antigos mantêm o formato anterior, salvo opt-in no nível de organização ou de repositório (UI ou REST). Ren (https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims)
- [confirmado] 3. OIDC - IDs não removíveis: `include_claim_keys não remove @OWNER-ID/@REPO-ID do segmento repo` -- No formato imutável, owner_id e repo_id ficam sempre no segmento repo do sub, mesmo com include_claim_keys. Não há como retirá-los. (https://docs.github.com/en/actions/reference/security/oidc)
- [confirmado] 3. OIDC - condição na trust da AWS: `"token.actions.githubusercontent.com:sub": "repo:octo-org@123456/octo-repo@456789:ref:refs/heads/demo-branch"` -- Exemplo oficial da condição de trust da AWS para o sub imutável. (https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims)
- [provavel] 3. OIDC - sub efetivo de um repository_dispatch: `repo:<OWNER>@<OWNER_ID>/<REPO>@<REPO_ID>:ref:refs/heads/main` -- Inferência a partir de duas páginas oficiais: o repository_dispatch roda com GITHUB_REF igual à branch padrão, então um job sem environment recebe o sub de branch da main. No formato imutável (o usado nos arquivos locais do projeto), o valo (https://docs.github.com/en/actions/reference/security/oidc#filtering-for-a-specific-branch)
- [confirmado] 3. configure-aws-credentials - versão estável: `aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0` -- A release estável mais recente é a v6.3.0 (não é pré-release; publicada em 2026-09-15). O SHA do commit da tag é e1253824e5c10ff9df46874f81ed3ec929e19cfd, o mesmo já fixado em .github/workflows/self-healing.yml. (https://api.github.com/repos/aws-actions/configure-aws-credentials/releases/latest)
- [confirmado] 3. configure-aws-credentials - SHA recomendado?: `uses: aws-actions/configure-aws-credentials@v6.3.0` -- O README não publica um SHA recomendado. Os exemplos usam a tag @v6.3.0 (e @v6 em alguns trechos) com id-token: write, e o texto remete às boas práticas de segurança do GitHub para actions de terceiros, que recomendam fixar pelo SHA complet (https://github.com/aws-actions/configure-aws-credentials/blob/main/README.md)
- [confirmado] 3. configure-aws-credentials - erro com sub legado: `Not authorized to perform sts:AssumeRoleWithWebIdentity` -- O README avisa: se a trust estiver no formato legado e o repositório emitir o sub imutável, o AssumeRoleWithWebIdentity falha. A correção é passar a condição sub para o formato imutável. (https://github.com/aws-actions/configure-aws-credentials/blob/main/README.md#immutable-subject-claims)
- [confirmado] 4. Terraform aws_eks_access_entry: `resource "aws_eks_access_entry" { cluster_name, principal_arn, kubernetes_groups = ["..."], type = "STANDARD" }` -- cluster_name e principal_arn são obrigatórios. kubernetes_groups é opcional. type é opcional e vale STANDARD por padrão; os tipos EC2_LINUX, EC2_WINDOWS e FARGATE_LINUX não aceitam username, grupos nem associações. (https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/eks_access_entry.html.markdown)
- [confirmado] 4. Terraform aws_eks_access_policy_association: `access_scope { type = "namespace"  namespaces = ["togglemaster"] }` -- Exige cluster_name, policy_arn, principal_arn e o bloco access_scope. O type do access_scope aceita namespace ou cluster; namespaces é opcional e define o escopo quando o type é namespace. (https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/eks_access_policy_association.html.markdown)
- [confirmado] 4. EKS - kubernetes_groups exige RBAC próprio: `subjects: [{kind: Group, name: <grupo de kubernetes_groups>}]` -- Num access entry STANDARD com nomes de grupo, é preciso criar um RoleBinding ou ClusterRoleBinding com subject kind: Group. O EKS não confere se o grupo existe em algum binding: aceita a configuração, mas o principal fica sem permissão até  (https://docs.aws.amazon.com/eks/latest/userguide/creating-access-entries.html)
- [confirmado] 4. EKS - access policy em vez de RBAC: `aws_eks_access_policy_association + access_scope type namespace` -- Em vez do RBAC próprio, ou junto com ele, dá para associar access policies da AWS ao access entry, com escopo em namespaces específicos e sem gerenciar objetos RBAC. (https://docs.aws.amazon.com/eks/latest/userguide/creating-access-entries.html)
- [confirmado] 4. EKS - AmazonEKSEditPolicy: `arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy` -- A AmazonEKSEditPolicy dá create, delete, deletecollection, patch e update em deployments e replicasets. Também dá leitura e escrita em secrets, acesso a pods/exec e pods/attach e impersonate de serviceaccounts, o que é muito mais do que um  (https://docs.aws.amazon.com/eks/latest/userguide/access-policy-permissions.html)
- [confirmado] 4. IAM mínimo do aws eks update-kubeconfig: `eks:DescribeCluster` -- O principal IAM precisa de permissão para eks:DescribeCluster no cluster indicado. (https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
- [confirmado] 4. RBAC - kubectl rollout restart: `apiGroups [apps], resources [deployments], verbs [get, patch]` -- O rollout restart busca o objeto no servidor (builder com Latest, ou seja, um GET) e depois aplica um PATCH strategic merge. Precisa dos verbos get e patch em deployments do grupo apps. (https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_restart.go)
- [confirmado] 4. RBAC - kubectl rollout status: `apiGroups [apps], resources [deployments], verbs [get, list, watch]` -- O rollout status faz um GET pelo builder e depois LIST e WATCH do próprio recurso, com field selector metadata.name. Precisa dos verbos get, list e watch em deployments. (https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_status.go)
- [provavel] 4. RBAC - replicasets/pods no rollout status: `replicasets/pods: não exigidos pelo rollout status de Deployment` -- O rollout_status.go só faz list/watch do recurso alvo (o Deployment), então replicasets e pods não parecem necessários para o rollout status de um Deployment. Eles só entram em comandos extras, como kubectl get pods -l app=.... O StatusView (https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_status.go)
- [confirmado] 4. RBAC - resourceNames com list/watch: `resourceNames + verbs [get, list, watch, patch] (list/watch exigem --field-selector=metadata.name=<nome>)` -- list e watch podem ser limitados por resourceNames, desde que o cliente envie o field selector metadata.name com o mesmo nome. O kubectl rollout status faz isso. create e deletecollection não podem ser limitados por nome. (https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [confirmado] 6. Anotação kubectl.kubernetes.io/restartedAt: `kubectl.kubernetes.io/restartedAt: "2024-06-21T17:27:41Z" | jsonpath={.spec.template.metadata.annotations.kubectl\.kubernetes\.io/restartedAt}` -- O kubectl rollout restart faz patch no template dos pods e grava a anotação com o instante do restart. Ela aparece em Deployment, ReplicaSet, StatefulSet, DaemonSet e Pod, e o exemplo oficial está em RFC3339 UTC. (https://kubernetes.io/docs/reference/labels-annotations-taints/)
- [confirmado] 6. Anotação - restart no mesmo segundo: `failed to create patch for <nome>: if restart has already been triggered within the past second, ...` -- Se já houve restart no mesmo segundo, o patch sai vazio e o kubectl recusa com erro 'failed to create patch'. (https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_restart.go)
- [confirmado] 5. Runner - ubuntu-latest: `ubuntu-latest = ubuntu-24.04 (x64)` -- ubuntu-latest aponta para Ubuntu 24.04 x64. O Ubuntu 26.04 existe, mas só com o rótulo ubuntu-26.04. A troca do rótulo -latest acontece aos poucos, em 1 a 2 meses, e fixar a versão evita mudança inesperada. (https://github.com/actions/runner-images/blob/main/README.md)
- [confirmado] 5. Runner - ferramentas já instaladas: `Kubectl 1.37.1 | AWS CLI 2.38.5 | Helm 3.22.1 | Kustomize 5.8.3 | jq 1.7` -- A imagem Ubuntu 24.04 (Image Version 20261026.354.1) já traz kubectl, AWS CLI, Helm, Kustomize e jq. Não é preciso instalar o AWS CLI. O kubectl existe, mas a versão não combina com o EKS 1.34. (https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md)
- [confirmado] 5. kubectl - version skew: `±1 minor: EKS 1.34 -> kubectl 1.33, 1.34 ou 1.35` -- O kubectl pode ter no máximo uma versão minor de diferença do cluster. Para o EKS 1.34, valem as versões 1.33 a 1.35; o 1.37.1 do runner fica fora. (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [confirmado] 5. azure/setup-kubectl - versão estável: `azure/setup-kubectl@bda439f5f36b99b262ebdcd3613869bddb064c8e # v5.2.0` -- A release mais recente é a v5.2.0 (não é pré-release; publicada em 2026-10-06). O SHA do commit da tag é bda439f5f36b99b262ebdcd3613869bddb064c8e. (https://api.github.com/repos/Azure/setup-kubectl/releases/latest)
- [confirmado] 5. azure/setup-kubectl - inputs: `with:
  version: "v1.34.<PATCH>"` -- O input version é obrigatório, vale 'latest' por padrão e aceita latest ou uma versão semver como v1.15.0. Há ainda os inputs opcionais downloadBaseURL (padrão https://dl.k8s.io), checksum e downloadAuthToken, e a saída kubectl-path. A acti (https://github.com/Azure/setup-kubectl/blob/v5.2.0/action.yml)
- [incerto] 5. kubectl 1.34 - patch atual: `[INCERTO] v1.34.<PATCH>` -- O patch mais recente da linha 1.34 não foi verificado por causa do limite de consultas. É preciso escolher a versão exata antes de fixá-la no workflow. (https://kubernetes.io/releases/patch-releases/)
- [confirmado] 6. concurrency - comportamento padrão: `concurrency:
  group: self-healing
  cancel-in-progress: false` -- Dentro do mesmo grupo, só roda um job ou workflow por vez. Um novo disparo fica pendente e, por padrão, substitui o pendente anterior (queue: single). Com cancel-in-progress: true, a execução em andamento também é cancelada. O nome do grupo (https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency)
- [confirmado] 6. concurrency - queue: `queue: single | max` -- queue aceita single (padrão, no máximo 1 pendente) ou max (até 100 pendentes). Combinar queue: max com cancel-in-progress: true gera erro de validação do workflow. (https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency)
- [confirmado] Integração - contact point webhook do Grafana: `Authentication Header Scheme: Bearer | Extra Headers | Custom Payload > Payload Template | Disable resolved message` -- O webhook do Grafana oferece os campos HTTP Method (POST ou PUT), Authentication Header Scheme (Bearer por padrão), Authentication Header Credentials (guardado de forma segura e mascarado), Extra Headers, Custom Payload (Payload Template e  (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/)
- [provavel] Integração - payload padrão do Grafana x API do GitHub: `Custom Payload com coll.Dict ... | data.ToJSON` -- O payload padrão do webhook (receiver, status, orgId, alerts...) não tem event_type, que é obrigatório no dispatch. Por inferência, sem Custom Payload a chamada deve falhar com 422. O Custom Payload oferece coll.Dict, coll.Slice, coll.Appen (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/)

### trechos de configuracao
#### Corpo e cabeçalhos da chamada POST /repos/{owner}/{repo}/dispatches, que o contact point do Grafana precisa reproduzir, mais um teste manual que deve retornar 204 (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
```yaml
# POST https://api.github.com/repos/<OWNER>/<REPO>/dispatches
# Cabecalhos:
#   Authorization: Bearer <fine-grained PAT; Repository permissions > Contents: write>
#   Accept: application/vnd.github+json
#   X-GitHub-Api-Version: 2026-03-10
# Sucesso: 204 No Content (sem corpo). Erros documentados: 404 e 422.
# Corpo (enviar como JSON; mostrado em YAML para leitura):
event_type: self-healing        # obrigatorio; <= 100 caracteres; igual a on.repository_dispatch.types
client_payload:                 # opcional; <= 10 chaves de 1o nivel; JSON total < 64KB
  service: flag-service         # validado por allowlist no workflow
  alertname: <nome-da-regra>    # exemplo
  status: firing                # permite ao workflow ignorar 'resolved'
# Teste manual (token so em variavel da sessao; nunca em arquivo versionado):
teste_manual: |
  curl -sS -o /dev/null -w '%{http_code}\n' -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GITHUB_DISPATCH_TOKEN}" \
    -H "X-GitHub-Api-Version: 2026-03-10" \
    "https://api.github.com/repos/<OWNER>/<REPO>/dispatches" \
    -d '{"event_type":"self-healing","client_payload":{"service":"flag-service","status":"firing"}}'
  # esperado: 204
```
#### Workflow de self-healing com: disparo filtrado por types, client_payload lido por env, concurrency, filtro de status, kubectl dentro do skew do EKS 1.34, OIDC com actions fixadas por SHA e cooldown pela anotação restartedAt (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
```yaml
# .github/workflows/self-healing.yml - precisa estar na branch padrao (main) para o repository_dispatch disparar
name: self-healing
on:
  repository_dispatch:
    types: [self-healing]          # filtra pelo event_type; sem types, qualquer event_type dispara
  workflow_dispatch:
    inputs:
      service:
        type: choice
        required: true
        default: flag-service
        options: [flag-service, auth-service, targeting-service, evaluation-service, analytics-service]
permissions:
  contents: read
  id-token: write                  # necessario para o token OIDC
concurrency:
  group: self-healing              # case-insensitive; uma execucao por vez no repositorio
  cancel-in-progress: false        # queue: single (padrao) = 1 rodando + no maximo 1 pendente
jobs:
  restart:
    # expressao avaliada pelo Actions, nao pelo shell; descarta notificacao 'resolved'
    if: github.event_name == 'workflow_dispatch' || github.event.client_payload.status == 'firing'
    runs-on: ubuntu-24.04          # hoje ubuntu-latest = ubuntu-24.04; fixar evita migracao silenciosa
    timeout-minutes: 10
    env:
      # dado externo entra por variavel de ambiente intermediaria; nunca interpolar dentro de run
      SERVICE: ${{ github.event.client_payload.service || inputs.service }}
      NAMESPACE: togglemaster
      COOLDOWN_SECONDS: "600"
    steps:
      - name: kubectl dentro do skew +-1 do EKS 1.34
        uses: azure/setup-kubectl@bda439f5f36b99b262ebdcd3613869bddb064c8e # v5.2.0
        with:
          version: "v1.34.<PATCH>"   # [INCERTO] patch atual da linha 1.34 nao verificado
      - name: Credenciais AWS por OIDC
        uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
        with:
          role-to-assume: ${{ vars.AWS_SELF_HEALING_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - name: kubeconfig (IAM minimo eks:DescribeCluster)
        env:
          CLUSTER: ${{ vars.EKS_CLUSTER_NAME }}
          REGION: ${{ vars.AWS_REGION }}
        run: aws eks update-kubeconfig --name "$CLUSTER" --region "$REGION"
      - name: allowlist + cooldown + restart + status
        run: |
          case "$SERVICE" in
            auth-service|flag-service|targeting-service|evaluation-service|analytics-service) ;;
            *) echo "servico fora da allowlist"; exit 2 ;;
          esac
          last="$(kubectl get deployment "$SERVICE" -n "$NAMESPACE" \
            -o 'jsonpath={.spec.template.metadata.annotations.kubectl\.kubernetes\.io/restartedAt}')"
          if [[ -n "$last" ]]; then
            elapsed=$(( $(date -u +%s) - $(date -u -d "$last" +%s) ))
            if (( elapsed < COOLDOWN_SECONDS )); then
              echo "cooldown ativo: ultimo restart ha ${elapsed}s"; exit 0
            fi
          fi
          kubectl rollout restart "deployment/$SERVICE" -n "$NAMESPACE"
          kubectl rollout status "deployment/$SERVICE" -n "$NAMESPACE" --timeout=180s
```
#### RBAC mínimo (Role e RoleBinding no namespace togglemaster) para rollout restart, rollout status e cooldown, restrito aos 5 Deployments. Variante mais restrita que a atual; testar antes de adotar (https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
```yaml
# Variante mais restrita do gitops/base/self-healing-rbac.yaml (testar no cluster antes de adotar)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: self-healing
  namespace: togglemaster
rules:
  # rollout restart = GET + PATCH; rollout status = GET + LIST + WATCH com fieldSelector metadata.name;
  # cooldown = GET. Com fieldSelector metadata.name, list/watch aceitam resourceNames.
  - apiGroups: ["apps"]
    resources: ["deployments"]
    resourceNames:
      - auth-service
      - flag-service
      - targeting-service
      - evaluation-service
      - analytics-service
    verbs: ["get", "list", "watch", "patch"]
  # opcional: so para 'kubectl get pods -l app=...' no resumo (LIST por label nao casa com resourceNames)
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: self-healing
  namespace: togglemaster
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: self-healing
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: togglemaster-self-healing   # identico a kubernetes_groups do aws_eks_access_entry
```
#### Terraform: access entry STANDARD com kubernetes_groups (recomendado) comparado à associação da AmazonEKSEditPolicy com escopo de namespace (alternativa ampla demais) (https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/eks_access_policy_association.html.markdown)
```yaml
terraform_hcl: |
  # Opcao A (recomendada, menor privilegio): grupo proprio + Role/RoleBinding do snippet de RBAC
  resource "aws_eks_access_entry" "self_healing" {
    cluster_name      = module.eks.cluster_name
    principal_arn     = aws_iam_role.self_healing.arn
    kubernetes_groups = ["togglemaster-self-healing"]
    type              = "STANDARD"
  }

  # Opcao B (mais simples, ampla demais): access policy da AWS com escopo de namespace.
  # AmazonEKSEditPolicy inclui secrets (leitura e escrita), pods/exec e impersonate de serviceaccounts.
  # resource "aws_eks_access_policy_association" "self_healing_edit" {
  #   cluster_name  = module.eks.cluster_name
  #   policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy"
  #   principal_arn = aws_iam_role.self_healing.arn
  #   access_scope {
  #     type       = "namespace"
  #     namespaces = ["togglemaster"]
  #   }
  #   depends_on = [aws_eks_access_entry.self_healing]  # [provavel] a associacao pressupoe o access entry
  # }
```
#### Terraform IAM: trust OIDC com o sub imutável da main e permissão mínima eks:DescribeCluster para o aws eks update-kubeconfig (https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims)
```yaml
terraform_hcl: |
  data "aws_iam_policy_document" "self_healing_trust" {
    statement {
      effect  = "Allow"
      actions = ["sts:AssumeRoleWithWebIdentity"]
      principals {
        type        = "Federated"
        identifiers = [local.github_oidc_provider_arn]
      }
      condition {
        test     = "StringEquals"
        variable = "token.actions.githubusercontent.com:aud"
        values   = ["sts.amazonaws.com"]
      }
      condition {
        test     = "StringEquals"
        variable = "token.actions.githubusercontent.com:sub"
        # repository_dispatch roda na branch padrao; repo criado apos 2026-07-15 => formato imutavel
        values   = ["repo:<OWNER>@<OWNER_ID>/<REPO>@<REPO_ID>:ref:refs/heads/main"]
        # job com environment: "repo:<OWNER>@<OWNER_ID>/<REPO>@<REPO_ID>:environment:<NOME>" [provavel]
      }
    }
  }

  data "aws_iam_policy_document" "self_healing" {
    statement {
      sid       = "DescribeProjectCluster"
      effect    = "Allow"
      actions   = ["eks:DescribeCluster"]   # minimo para aws eks update-kubeconfig
      resources = [var.eks_cluster_arn]
    }
  }
```
#### Contact point webhook do Grafana chamando a API do GitHub. Usa os rótulos da UI documentada; o template é [provável] e as chaves de provisioning em arquivo não foram verificadas (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/)
```yaml
# Rotulos da UI do contact point Webhook conforme a doc do Grafana; chaves de provisioning em arquivo NAO verificadas aqui
URL: https://api.github.com/repos/<OWNER>/<REPO>/dispatches   # a URL nao e campo seguro: sem token nela
HTTP Method: POST
Authentication Header Scheme: Bearer
Authentication Header Credentials: <fine-grained PAT com Contents write; campo mascarado; nunca no Git>
Extra Headers:
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: "2026-03-10"
Disable resolved message: true    # evita novo dispatch quando o alerta resolve
Custom Payload:
  Payload Template: |
    {{ define "github.dispatch" -}}
    {{ coll.Dict
         "event_type" "self-healing"
         "client_payload" (coll.Dict
            "service" .CommonLabels.service
            "alertname" .CommonLabels.alertname
            "status" .Status)
       | data.ToJSON }}
    {{- end }}
# [provavel] .CommonLabels.service exige o label service=flag-service na regra de alerta
```

### riscos
- Versão do kubectl fora do suportado (teste local, retrato de 2026-11-03): o ubuntu-latest é o Ubuntu 24.04 (imagem 20261026.354.1), que traz Kubectl 1.37.1. A política do Kubernetes só suporta uma versão minor de diferença, e o EKS 1.34 aceita kubectl 1.33 a 1.35. O .github/workflows/self-healing.yml atual usa o kubectl do runner, sem setup-kubectl, e por isso fica fora do suporte. Sugestão: adicionar azure/setup-kubectl@bda439f5f36b99b262ebdcd3613869bddb064c8e (v5.2.0) com uma versão 1.34.x (o patch exato está [INCERTO]) e considerar runs-on: ubuntu-24.04. As versões da imagem mudam toda semana.
- O payload padrão do Grafana (receiver, status, orgId, alerts...) não tem event_type, que o dispatch exige. Por inferência, a API do GitHub responderia 422, então é obrigatório usar o Custom Payload. Não foi verificado se a versão do Grafana entregue pelo kube-prometheus-stack suporta o Custom Payload (versão mínima [INCERTO]); a doc diz apenas que ele ainda não é GA no Grafana Cloud. As chaves de provisioning do contact point em arquivo também não foram verificadas nesta frente.
- Notificação de resolução: se 'Disable resolved message' não for ligado, cada resolução do alerta gera um novo dispatch. O workflow atual não confere client_payload.status, então uma resolução que chegue depois dos 600 s de cooldown reiniciaria o serviço de novo sem necessidade. As repetições do Grafana (repeat interval) também geram dispatches; o cooldown e o concurrency atenuam isso.
- Branch padrão: o repository_dispatch só roda workflows que estão na main e usa o último commit da main (GITHUB_SHA). O self-healing.yml e o scripts/self-healing/restart.sh precisam estar na main. Pela regra do projeto, push e merge na main dependem de autorização explícita do usuário; sem ela, o ensaio da cadeia de incidente não dispara, e mudanças feitas só na dev não são testadas.
- Token sensível: o fine-grained PAT com Contents write também permite gravar arquivos e criar refs pela API. Se ele vazar do Grafana e a main não tiver proteção, alguém pode alterar o scripts/self-healing/restart.sh, que roda com a role do self-healing. Como mitigar: token restrito a este repositório e só com Contents, validade curta, ruleset ou proteção na main exigindo PR, token guardado apenas no campo mascarado do Grafana ou num Secret (nunca no Git) e revogado após a entrega. Se o token expirar, a cadeia para sem aviso; o erro só aparece no log de notificação do Grafana.
- [INCERTO] Repositório de organização: o fine-grained PAT precisa ter a organização como resource owner e pode depender da política de aprovação de PATs da organização. Isso não foi verificado nesta pesquisa.
- OIDC: o projeto já usa o sub imutável (terraform/modules/iam-ci/main.tf:81). Se o job passar a usar environment:, o sub vira ...:environment:<nome> e a condição StringEquals da trust falha com Not authorized to perform sts:AssumeRoleWithWebIdentity. Renomear ou transferir o repositório também muda o trecho do nome no sub. Observação de endurecimento: as roles de ECR e de self-healing confiam no mesmo sub da main, então qualquer workflow da main assume as duas; um environment dedicado, com trust no sub de environment (formato imutável [provável]), separaria as identidades.
- Ordem de implantação: o EKS não confere se o grupo do access entry existe. Até o ArgoCD sincronizar o Role e o RoleBinding no namespace togglemaster, a role recebe Forbidden. O access entry (Terraform) e o RBAC (GitOps) precisam estar aplicados antes do ensaio.
- Associar a AmazonEKSEditPolicy com escopo de namespace daria leitura e escrita de secrets, pods/exec e impersonate de serviceaccounts, o que é demais para um restart. A recomendação é manter o grupo próprio com Role, como em terraform/cluster/self-healing.tf.
- O comentário em gitops/base/self-healing-rbac.yaml diz que list/watch não combinam com resourceNames, o que diverge da doc de RBAC: eles combinam quando o cliente envia field selector metadata.name, e o kubectl rollout status faz isso. Dá para restringir get/list/watch de deployments aos 5 nomes ([provável] que funcione; testar). Também é [provável], por leitura parcial do código, que o rollout status de um Deployment não precise de replicasets nem pods.
- ArgoCD com selfHeal: o restart grava spec.template.metadata.annotations.kubectl.kubernetes.io/restartedAt, que não está no Git. É [provável] que o ArgoCD não reverta essa anotação, porque ela fica fora do estado desejado, mas isso não foi verificado aqui. No ensaio, conferir que a aplicação continua Synced e que não acontece um rollout extra.
- Cooldown pela anotação: o exemplo oficial grava a data em RFC3339 UTC. Um restart manual feito fora do runner pode gravar a data com fuso, como -03:00 ([provável]); o date -u -d aceita os dois formatos. Anotação vazia significa que o serviço nunca foi reiniciado e deve ser tratada como sem cooldown. Dois restarts no mesmo segundo falham com 'failed to create patch'.
- Limites do client_payload: no máximo 10 chaves de primeiro nível, menos de 64KB pela REST ou 65.535 caracteres pela doc de eventos. Não repassar o grupo inteiro de alertas do Grafana. A API também devolve 422 quando considera o endpoint alvo de spam.
- Concurrency: com cancel-in-progress: false e a fila padrão (single), um terceiro disparo durante uma execução cancela o pendente anterior, o que é aceitável aqui. queue: max não pode ser combinado com cancel-in-progress: true, porque gera erro de validação.
- [provável, não verificado] O Grafana dentro do EKS precisa de saída de rede (egress/NAT) até api.github.com.
- Escopo desta pesquisa: foram 25 consultas a fontes oficiais, sem acesso a contas, sem chaves e sem alterar arquivos do repositório. A versão do actions/checkout fixada no workflow atual (v7.0.1) não foi verificada.

## otel
- [confirmado] 6. Distribuição contrib 0.163.2: `version: 0.163.2 | spanmetricsconnector v0.163.0 | prometheusremotewriteexporter v0.163.0 | otlphttpexporter v0.163.0 | otlpexporter v0.163.0 | filelogreceiver v0.163.0 | k8sattributesprocessor v1.2.0 | transformprocessor v0.163.0 | filterprocessor v0.163.0 | memorylimiterprocessor v0.163.0 | batchprocessor v0.163.0` -- O manifest oficial da otelcol-contrib 0.163.2 inclui todos os componentes do desenho. Os módulos estão em v0.163.0, exceto o k8sattributesprocessor, que já está em v1.2.0. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-releases/v0.163.2/distributions/otelcol-contrib/manifest.yaml)
- [confirmado] 6. span_metrics: nome e estabilidade: `type: span_metrics | deprecated_type: spanmetrics | alpha: [traces_to_metrics]` -- O connector foi renomeado. O tipo atual é span_metrics e spanmetrics continua aceito como alias deprecado. Estabilidade: alpha (traces para metrics). (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/metadata.yaml)
- [confirmado] 6. prometheus_remote_write: nome e estabilidade: `type: prometheus_remote_write | deprecated_type: prometheusremotewrite | beta: [metrics]` -- O exporter foi renomeado para prometheus_remote_write. prometheusremotewrite é alias deprecado e registra aviso. Estabilidade: beta. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/exporter/prometheusremotewriteexporter/metadata.yaml)
- [confirmado] 6. otlp_http: nome e estabilidade: `type: otlp_http | deprecated_type: otlphttp | stable: [traces, metrics, logs] | alpha: [profiles]` -- O exporter OTLP/HTTP agora se chama otlp_http. otlphttp é alias deprecado e o README manda trocar. Estabilidade: stable para traces, metrics e logs. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlphttpexporter/metadata.yaml)
- [confirmado] 6. otlp_grpc: exporter gRPC (agente para gateway): `type: otlp_grpc | deprecated_type: otlp | stable: [traces, metrics, logs]` -- O exporter OTLP gRPC agora é otlp_grpc. O nome otlp, como exporter, virou alias deprecado. Estabilidade: stable. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlpexporter/metadata.yaml)
- [confirmado] 6. file_log: nome e estabilidade: `type: file_log | deprecated_type: filelog | beta: [logs]` -- O receiver filelog foi renomeado para file_log; filelog é alias deprecado. Estabilidade: beta para logs. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/receiver/filelogreceiver/metadata.yaml)
- [confirmado] 6. k8s_attributes: nome e estabilidade: `type: k8s_attributes | deprecated_type: k8sattributes | stable: [logs, metrics, traces] | development: [profiles]` -- O processador foi renomeado para k8s_attributes; k8sattributes é alias deprecado. É stable (módulo v1.2.0). (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/processor/k8sattributesprocessor/metadata.yaml)
- [confirmado] 6. transform: estabilidade: `type: transform | beta: [traces, metrics, logs] | development: [profiles]` -- O processador transform manteve o nome. Estabilidade: beta. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/processor/transformprocessor/metadata.yaml)
- [confirmado] 6. filter: estabilidade: `type: filter | alpha: [traces, metrics, logs] | development: [profiles]` -- O processador filter manteve o nome. Estabilidade: alpha. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/processor/filterprocessor/metadata.yaml)
- [confirmado] 6. memory_limiter: estabilidade: `type: memory_limiter | beta: [traces, metrics, logs] | alpha: [profiles]` -- O memory_limiter manteve o nome. Estabilidade: beta. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/processor/memorylimiterprocessor/metadata.yaml)
- [confirmado] 6. batch: estabilidade e padrões: `type: batch | beta: [traces, metrics, logs] | send_batch_size: 8192 | timeout: 200ms | send_batch_max_size: 0 (sem limite)` -- O batch continua beta e o README não traz aviso de depreciação. send_batch_size só dispara o envio e não limita o lote; o teto vem de send_batch_max_size. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/processor/batchprocessor/README.md)
- [provavel] 6. receptor otlp: `receivers: otlp (protocols grpc 4317 e http 4318)` -- O receptor otlp não aparece renomeado: o chart feito para 0.163.2 usa receivers.otlp na config padrão. O metadata.yaml do receptor não foi aberto. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] 1. span_metrics: nomes gerados: `namespace: traces.span.metrics -> traces.span.metrics.calls | traces.span.metrics.duration | traces.span.metrics.events` -- Com o namespace padrão, o connector gera traces.span.metrics.calls (Sum) e traces.span.metrics.duration (Histogram). traces.span.metrics.events só aparece com events.enabled. No código: metricNameCalls = "calls" e metricNameDuration = "dura (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [confirmado] 1. span_metrics: unidade da duração: `histogram.unit: ms (padrão; aceita ms ou s) | connector.spanmetrics.useSecondAsDefaultMetricsUnit: stage alpha` -- Só a duração recebe unidade (SetUnit em histogram.unit; calls fica sem unidade). O padrão continua ms porque o gate connector.spanmetrics.useSecondAsDefaultMetricsUnit está em alpha (desligado). O README avisa que o padrão vai mudar para s. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [confirmado] 1. span_metrics: dimensões padrão: `service.name | span.name | span.kind | status.code | collector.instance.id` -- Em 0.163 as dimensões padrão são service.name, span.name, span.kind e status.code, mais collector.instance.id (gate connector.spanmetrics.includeCollectorInstanceID em beta, ligado). Para remover: exclude_dimensions. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [confirmado] 1. span_metrics: valores de status.code e span.kind: `STATUS_CODE_UNSET | STATUS_CODE_OK | STATUS_CODE_ERROR ; span.kind de servidor = SPAN_KIND_SERVER` -- status.code e span.kind são gravados como texto no formato STATUS_CODE_* e SPAN_KIND_*. O gate spanmetrics.statusCodeConvention.useOtelPrefix (alpha, desligado) trocaria para otel.status_code=ERROR. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/internal/coreinternal/traceutil/traceutil.go)
- [confirmado] 1. span_metrics: dimensão do código HTTP: `dimensions:
  - name: http.response.status_code` -- Para ter o código HTTP, basta listá-lo em dimensions. O valor é buscado nos atributos do span e depois nos do recurso. Se não existir e não houver default, a dimensão é omitida da série. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [confirmado] 1. span_metrics: padrões relevantes: `aggregation_temporality: AGGREGATION_TEMPORALITY_CUMULATIVE | metrics_flush_interval: 60s | metrics_expiration: 0 | explicit.buckets: [2ms, 4ms, 6ms, 8ms, 10ms, 50ms, 100ms, 200ms, 400ms, 800ms, 1s, 1400ms, 2s, 5s, 10s, 15s] | aggregation_cardinality_limit: 0` -- Padrões que afetam o alerta: temporalidade cumulativa, flush a cada 60s e séries sem expiração. dimensions_cache_size está deprecado e foi substituído por aggregation_cardinality_limit. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [confirmado] 1. span_metrics: atributos de recurso: `connector.spanmetrics.excludeResourceMetrics: stage alpha | add_resource_attributes: false (padrão)` -- O gate connector.spanmetrics.excludeResourceMetrics está em alpha (desligado), então os atributos de recurso do span são copiados para as métricas. Por isso o Prometheus gera job (service.name), instance (service.instance.id) e target_info. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/connector.go)
- [confirmado] 1. Nome no Prometheus: contador de chamadas: `traces_span_metrics_calls_total{service_name, span_name, span_kind="SPAN_KIND_SERVER", status_code="STATUS_CODE_ERROR", collector_instance_id, ...}` -- Na estratégia padrão UnderscoreEscapingWithSuffixes (padrão no prometheus_remote_write e no receptor OTLP do Prometheus), calls vira um contador com sufixo _total. O nome final é traces_span_metrics_calls_total, com os rótulos service_name, (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md)
- [provavel] 1. Nome no Prometheus: duração: `traces_span_metrics_duration_milliseconds_bucket | traces_span_metrics_duration_milliseconds_sum | traces_span_metrics_duration_milliseconds_count` -- O histograma de duração, com unidade ms, deve gerar traces_span_metrics_duration_milliseconds_bucket, _sum e _count. Não abri o arquivo do tradutor que converte ms em milliseconds. (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] 1. Flask 0.66b1: 5xx vira STATUS_CODE_ERROR: `if status <= 499 and server_span: return StatusCode.UNSET -> return StatusCode.ERROR` -- Sim. Em span de servidor, a 0.66b1 deixa 1xx–3xx e 4xx como UNSET e marca ERROR em 5xx. _set_status usa server_span=True por padrão. No span_metrics, 5xx aparece como status.code=STATUS_CODE_ERROR e 4xx como STATUS_CODE_UNSET. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-python-contrib/v0.66b1/opentelemetry-instrumentation/src/opentelemetry/instrumentation/utils.py)
- [confirmado] 1. Semantic conventions: status de span HTTP server: `4xx: unset (SpanKind.SERVER) | 5xx: Error` -- A especificação confirma a regra: em span SERVER, 4xx fica sem status e 5xx deve ser Error. (https://opentelemetry.io/docs/specs/semconv/http/http-spans/)
- [confirmado] 1. Flask 0.66b1: nome do atributo do código HTTP: `sem OTEL_SEMCONV_STABILITY_OPT_IN -> _StabilityMode.DEFAULT -> http.status_code ; http -> http.response.status_code ; http/dup -> ambos` -- O repositório não define OTEL_SEMCONV_STABILITY_OPT_IN (grep local em 2026-11-03). Sem ela, o modo é DEFAULT e a biblioteca grava só http.status_code, da convenção antiga. http.response.status_code só aparece com OTEL_SEMCONV_STABILITY_OPT_ (https://raw.githubusercontent.com/open-telemetry/opentelemetry-python-contrib/v0.66b1/opentelemetry-instrumentation/src/opentelemetry/instrumentation/_semconv.py)
- [provavel] 1. Caminho Flask -> WSGI: `_set_status(..., server_span: bool = True)` -- A instrumentação Flask repassa a resposta ao middleware WSGI, que chama _set_status como span de servidor. Não abri os arquivos flask e wsgi da tag; o valor padrão server_span=True está confirmado em _semconv.py. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-python-contrib/v0.66b1/opentelemetry-instrumentation/src/opentelemetry/instrumentation/_semconv.py)
- [confirmado] 2. Receptor OTLP nativo do Prometheus: `--web.enable-otlp-receiver | POST /api/v1/otlp/v1/metrics` -- O receptor vem desligado, como o de remote write. É ligado pela flag --web.enable-otlp-receiver e atende em /api/v1/otlp/v1/metrics. A versão da doc consultada é a 3.15 (latest). (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] 2. Prometheus: estratégias de tradução OTLP: `otlp.translation_strategy: UnderscoreEscapingWithSuffixes (padrão) | UnderscoreEscapingWithoutSuffixes | NoUTF8EscapingWithSuffixes | NoTranslation` -- No bloco otlp da configuração do Prometheus, translation_strategy tem padrão UnderscoreEscapingWithSuffixes. As outras opções são UnderscoreEscapingWithoutSuffixes, NoUTF8EscapingWithSuffixes e NoTranslation (experimental, com riscos de col (https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [confirmado] 2. Prometheus OTLP: target_info, job e instance: `job = service.name | instance = service.instance.id | otlp.promote_resource_attributes | otlp.keep_identifying_resource_attributes: false` -- O Prometheus cria target_info e preenche job com service.name e instance com service.instance.id. Os demais atributos de recurso ficam só em target_info, a menos que sejam promovidos. (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] 2. Prometheus OTLP: recomendações e delta: `tsdb.out_of_order_time_window: 30m | --enable-feature=otlp-deltatocumulative` -- O guia recomenda out_of_order_time_window de 30m. Delta só é aceito com a feature flag experimental otlp-deltatocumulative; o span_metrics já emite cumulativo por padrão. (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] 2. prometheus_remote_write: configuração: `http.endpoint | remote_write_queue.num_consumers: 5 | compressão: snappy` -- O endpoint agora vai preferencialmente em http.endpoint; o endpoint no topo ainda é aceito. Só usa compressão snappy. Não tem sending_queue: a fila é o remote_write_queue (num_consumers padrão 5). (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/exporter/prometheusremotewriteexporter/README.md)
- [confirmado] 2. prometheus_remote_write: tradução e recurso: `translation_strategy: UnderscoreEscapingWithSuffixes (padrão) | UnderscoreEscapingWithoutSuffixes | NoUTF8EscapingWithSuffixes | NoTranslation ; target_info.enabled: true ; resource_constant_labels` -- add_metric_suffixes está deprecado em favor de translation_strategy, que aceita os mesmos quatro modos do Prometheus. target_info vem ligado. resource_to_telemetry_conversion está deprecado em favor de resource_constant_labels. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/exporter/prometheusremotewriteexporter/README.md)
- [confirmado] 2. prometheus_remote_write: temporalidade: `Non-cumulative monotonic, histogram, and summary OTLP metrics are dropped` -- O exporter descarta somas monotônicas, histogramas e summaries que não sejam cumulativos. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/exporter/prometheusremotewriteexporter/README.md)
- [confirmado] 2. kube-prometheus-stack: chaves dos receptores: `enableOTLPReceiver: false | otlp: {} (promoteResourceAttributes, keepIdentifyingResourceAttributes, translationStrategy, convertHistogramsToNHCB) | enableRemoteWriteReceiver: false` -- Os values do kube-prometheus-stack (branch main, chart 92.17.1, operator v0.94.2) têm chaves próprias para ligar os dois receptores; ambas vêm false. (https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml)
- [provavel] 2. kube-prometheus-stack: caminho das chaves: `prometheus.prometheusSpec.enableOTLPReceiver | prometheus.prometheusSpec.otlp | prometheus.prometheusSpec.enableRemoteWriteReceiver` -- Pela indentação, as chaves ficam em prometheus.prometheusSpec. Ainda é preciso conferir na versão do chart que o projeto vai fixar. (https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml)
- [confirmado] 2. otlp_http: endpoints e padrões: `endpoint + /v1/metrics | metrics_endpoint | compression: gzip (padrão) | encoding: proto (padrão) | timeout: 30s` -- No otlp_http, endpoint é a URL base e o exporter acrescenta /v1/traces, /v1/metrics ou /v1/logs; metrics_endpoint recebe a URL completa. Padrões: gzip, proto e timeout de 30s. Com endpoint http://<prometheus>:9090/api/v1/otlp, o envio vai p (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlphttpexporter/README.md)
- [provavel] 2. Comparação: qual usar: `otlp_http -> http://<prometheus>:9090/api/v1/otlp + prometheus.prometheusSpec.enableOTLPReceiver: true` -- Recomendação (análise minha): usar o receptor OTLP nativo com otlp_http. O otlp_http é stable e o prometheus_remote_write é beta. Há menos tradução no Collector, o Prometheus gera target_info, job e instance, e a documentação oficial de OTe (https://prometheus.io/docs/guides/opentelemetry/)
- [provavel] 2. Nomes com outras estratégias: `traces.span.metrics.calls_total (NoUTF8EscapingWithSuffixes) | traces_span_metrics_calls (UnderscoreEscapingWithoutSuffixes) | traces.span.metrics.calls (NoTranslation)` -- Os nomes só mudam se a estratégia for trocada. NoUTF8EscapingWithSuffixes mantém os pontos e os sufixos, e o PromQL passa a exigir aspas. UnderscoreEscapingWithoutSuffixes tira o _total. NoTranslation passa o nome OTel sem alteração. As for (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] 3. Loki: exporter e endpoint: `otlp_http (alias deprecado otlphttp) | endpoint: http://<loki-addr>/otlp -> /otlp/v1/logs` -- O Loki exige o exporter OTLP/HTTP com endpoint http://<loki-addr>/otlp, e o exporter acrescenta /v1/logs. A doc ainda mostra o nome otlphttp; em 0.163 o nome é otlp_http. (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] 3. Loki: structured metadata: `limits_config.allow_structured_metadata: true` -- O Loki precisa de allow_structured_metadata: true; senão rejeita o payload OTLP. Vem ligado a partir do Loki 3.0. (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] 3. Loki: atributos de recurso que viram labels: `cloud.availability_zone, cloud.region, container.name, deployment.environment.name, k8s.cluster.name, k8s.container.name, k8s.cronjob.name, k8s.daemonset.name, k8s.deployment.name, k8s.job.name, k8s.namespace.name, k8s.pod.name, k8s.replicaset.name, k8s.statefulset.name, service.instance.id, service.name, service.namespace` -- Por padrão, 17 atributos de recurso viram index labels. O resto vira structured metadata. (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] 3. Loki: normalização e cardinalidade: `service_name | k8s_namespace_name | limite 15 index labels | distributor.otlp_config.default_resource_attributes_as_index_labels | limits_config.otlp_config` -- Pontos viram sublinhado (service.name vira service_name). O limite padrão é de 15 index labels. A lista é configurável em default_resource_attributes_as_index_labels (otlp_config do distributor) ou em limits_config.otlp_config. A doc desaco (https://grafana.com/docs/loki/latest/send-data/otel/)
- [incerto] 3. Loki: porta 3100: `http://<loki-svc>.observability.svc.cluster.local:3100/otlp` -- A doc mostra o endpoint sem porta. A porta 3100 é a porta HTTP habitual do Loki, mas não foi confirmada nesta pesquisa e depende do Service criado pelo chart do Loki. (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] 4. Chart do Collector para 0.163.2: `0.177.0 (2026-10-22) | 0.178.0 (2026-10-27) | 0.178.1 (2026-10-29) | 0.178.2 (2026-11-02) -> appVersion 0.163.2` -- As versões 0.177.0 a 0.178.2 do chart opentelemetry-collector trazem appVersion 0.163.2. A 0.178.2 é a mais nova (2026-11-02). (https://open-telemetry.github.io/opentelemetry-helm-charts/index.yaml)
- [confirmado] 4. Chart: mode e imagem: `mode: "" (daemonset | deployment | statefulset) | image.repository: "" -> otel/opentelemetry-collector-contrib | image.tag: "" (= appVersion)` -- mode e image.repository vêm vazios e precisam ser definidos. A tag da imagem, por padrão, é a appVersion. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] 4. Chart: nomes gerados pelos presets: `rewriteDeprecatedComponentNames: true` -- rewriteDeprecatedComponentNames vem true, então os presets geram file_log e k8s_attributes, e não os nomes antigos. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] 4. Preset logsCollection: o que gera: `file_log: include: [ /var/log/pods/*/*/*.log ] | start_at: end | retry_on_failure.enabled: true | include_file_path: true | include_file_name: false | operators: [{type: container, id: container-parser, max_log_size: 102400}]` -- O preset logsCollection cria o receiver file_log com o operador container e o coloca no pipeline de logs. Segundo os comentários dos values, também monta os volumes de /var/log/pods. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] 4. Exclusão dos logs do próprio Collector: `exclude: /var/log/pods/<namespace>_<fullname>*_*/opentelemetry-collector/*.log` -- Com includeCollectorLogs: false (padrão), o preset exclui só os logs do próprio release. Logs de outro release, como o gateway, continuam sendo coletados. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [provavel] 4. Como sobrescrever o exclude: `config.receivers.file_log.exclude: [<padrão do agente>, <padrão do gateway>]` -- O preset é mesclado com mustMergeOverwrite e a config do usuário entra por último. Ao definir config.receivers.file_log.exclude, a lista substitui a do preset; por isso é preciso repetir o padrão do agente e acrescentar o do gateway. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] 4. Operador container: `add_metadata_from_filepath: true -> k8s.pod.name, k8s.pod.uid, k8s.container.name, k8s.container.restart_count, k8s.namespace.name` -- O operador container reconhece os formatos docker, crio e containerd. Por padrão, tira do caminho do arquivo os metadados k8s e os grava como atributos de recurso; para isso exige include_file_path: true. Com k8s.pod.uid presente, o k8s_att (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/pkg/stanza/docs/operators/container.md)
- [confirmado] 4. Preset kubernetesAttributes: o que gera: `filter.node_from_env_var: K8S_NODE_NAME (só daemonset) | passthrough: false | pod_association: k8s.pod.ip, k8s.pod.uid, connection | extract.otel_annotations: true | metadata: k8s.namespace.name, k8s.pod.name, k8s.pod.uid, k8s.node.name, k8s.pod.start_time, k8s.deployment.name, k8s.replicaset.name, k8s.replicaset.uid, k8s.daemonset.name, k8s.daemonset.uid, k8s.job.name, k8s.job.uid, k8s.container.name, k8s.cronjob.name, k8s.statefulset.name, k8s.statefulset.uid, container.image.tag, container.image.name, k8s.cluster.uid, service.namespace, service.name, service.version, service.instance.id` -- O preset cria o k8s_attributes e, no modo daemonset, filtra pelo nó. Associa pelo IP e pelo UID do pod ou pela conexão, e extrai uma lista ampla de metadados, incluindo service.*. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] 4. Preset kubernetesAttributes: posição no pipeline: `prepend k8s_attributes, exceto se k8sattributes ou k8s_attributes já estiver em processors` -- O preset insere k8s_attributes no início dos pipelines logs, metrics e traces que existirem. Se o processador já estiver listado, mantém a ordem definida pelo usuário. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] 4. RBAC criado pelo chart: `apiGroups [""]: pods, namespaces [get, watch, list] | apiGroups ["apps"]: replicasets [get, list, watch] | apiGroups ["extensions"]: replicasets [get, list, watch]` -- Com o preset kubernetesAttributes ligado, o chart cria uma ClusterRole com as regras abaixo. A ClusterRoleBinding não foi aberta. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/clusterrole.yaml)
- [confirmado] 4. RBAC exigido pelo processador: `pods, namespaces: get/watch/list | replicasets (condicional) | nodes (condicional) | jobs/cronjobs (condicional)` -- Para atuar entre namespaces, o processador precisa de get, watch e list em pods e namespaces. ReplicaSets entram só para k8s.deployment.uid ou extração from deployment/replicaset; nodes, para k8s.node.uid; jobs, para k8s.cronjob.uid. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/processor/k8sattributesprocessor/README.md)
- [confirmado] 4. Padrões do chart que afetam o desenho: `memory_limiter: check_interval 5s, limit_percentage 80, spike_limit_percentage 25 | batch: {} | resources: {} | useGOMEMLIMIT: true | extraEnvs: [] | receivers: jaeger, otlp, prometheus, zipkin` -- O memory_limiter do chart usa percentual do limite de memória do container, mas resources vem vazio. A config padrão traz receivers jaeger, otlp, prometheus e zipkin, e o exporter debug. Há extraEnvs para injetar variáveis, por exemplo de u (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] 5. New Relic: endpoint OTLP: `https://otlp.nr-data.net (443, 4317, 4318) | EU: https://otlp.eu01.nr-data.net` -- O endpoint US é https://otlp.nr-data.net, nas portas 443, 4317 e 4318, com gRPC e HTTP. Para conta EU, o endpoint é https://otlp.eu01.nr-data.net. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [confirmado] 5. New Relic: autenticação: `api-key: <license key>` -- A autenticação é por um header chamado api-key, com a license key como valor. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [confirmado] 5. New Relic: payload e lote: `payload < 1MB (10^6 bytes) | tamanho do lote controlado pelo batch processor` -- Cada payload precisa ter menos de 1MB (10^6 bytes) e há rate limit. Payloads maiores são rejeitados ou estouram o timeout. No Collector, quem controla o tamanho do lote é o batch processor. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [confirmado] 5. New Relic: compressão: `compression: gzip (padrão do Collector) | zstd (recomendado pelo NR, se suportado)` -- O New Relic aceita gzip e zstd e recomenda zstd quando o exporter suporta. O Collector já usa gzip por padrão. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [confirmado] 5. New Relic: retry e limite de atributo: `retry: recomendado | string de atributo: máx. 4095 caracteres (trunca)` -- O New Relic recomenda retry para erros transitórios. Valores de atributo do tipo string passam de 4095 caracteres e são truncados. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [incerto] 5. New Relic: número de itens por lote: `sem valor numérico oficial` -- A página não fixa um número de itens por lote, só o teto de 1MB. Os valores send_batch_size 256 e send_batch_max_size 512 nos snippets são sugestão minha, coerentes com o laboratório local, e precisam ser validados. (https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/)
- [provavel] 5. otlp_http para New Relic: chave headers: `otlp_http/newrelic: endpoint: https://otlp.nr-data.net | headers: {api-key: ${env:NEW_RELIC_LICENSE_KEY}} | compression: gzip` -- No Collector, o header vai em headers no exporter otlp_http (configuração HTTP do cliente). O README do confighttp não foi aberto; o gzip padrão está confirmado. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlphttpexporter/README.md)

### trechos de configuracao
#### Gateway (Deployment) - values do chart open-telemetry/opentelemetry-collector 0.178.2 (appVersion 0.163.2): OTLP dos 5 serviços, traces para o New Relic, span_metrics para o Prometheus (OTLP nativo), logs para o Loki. Nomes novos dos componentes. <prometheus-svc> e <loki-svc> dependem dos releases das outras frentes. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml | https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md | https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlphttpexporter/README.md)
```yaml
mode: deployment
fullnameOverride: otel-gateway
image:
  repository: otel/opentelemetry-collector-contrib
  tag: "0.163.2"
replicaCount: 1
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    memory: 512Mi   # base do memory_limiter (limit_percentage) e do GOMEMLIMIT
ports:
  jaeger-compact:
    enabled: false
  jaeger-thrift:
    enabled: false
  jaeger-grpc:
    enabled: false
  zipkin:
    enabled: false
extraEnvs:
  - name: NEW_RELIC_LICENSE_KEY
    valueFrom:
      secretKeyRef:
        name: newrelic-otlp   # Secret criado fora do Git
        key: license-key
config:
  receivers:
    jaeger: null
    zipkin: null
    otlp:
      protocols:
        grpc:
          endpoint: ${env:MY_POD_IP}:4317
        http:
          endpoint: ${env:MY_POD_IP}:4318
  processors:
    memory_limiter:
      check_interval: 1s
      limit_percentage: 80
      spike_limit_percentage: 25
    filter/health:
      error_mode: propagate
      traces:
        span:
          - 'attributes["http.route"] == "/health"'
          - 'attributes["url.path"] == "/health"'
          - 'attributes["http.target"] == "/health"'
    transform/sanitize:
      error_mode: propagate
      trace_statements:
        - context: resource
          statements:
            - 'keep_keys(attributes, ["service.name", "service.namespace", "service.version", "deployment.environment.name", "telemetry.sdk.name", "telemetry.sdk.language", "telemetry.sdk.version"])'
        - context: span
          statements:
            - 'keep_keys(attributes, ["http.route", "http.method", "http.request.method", "http.status_code", "http.response.status_code", "http.flavor", "url.scheme", "server.address", "server.port", "network.protocol.version", "net.peer.name", "net.peer.port", "db.system", "db.system.name", "db.name", "db.namespace", "db.operation", "db.operation.name", "messaging.system", "messaging.destination.name", "messaging.operation", "messaging.operation.name", "messaging.operation.type", "error.type", "cache.hit"])'
            - 'set(status.message, "")'
        - context: spanevent
          statements:
            - 'keep_keys(attributes, ["exception.type"])'
    batch:
      timeout: 1s
      send_batch_size: 256
      send_batch_max_size: 512   # teto do lote (NR rejeita payload > 1MB)
  connectors:
    span_metrics:
      namespace: traces.span.metrics   # padrão, explícito para estabilizar nomes
      histogram:
        unit: ms                       # explícito: o README avisa mudança futura para s
        explicit:
          buckets: [5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2500ms, 5s, 10s]
      dimensions:
        - name: http.route
        - name: http.status_code             # gravado pelo Flask 0.66b1 sem OTEL_SEMCONV_STABILITY_OPT_IN
        - name: http.response.status_code    # gravado com OTEL_SEMCONV_STABILITY_OPT_IN=http ou http/dup
      aggregation_temporality: AGGREGATION_TEMPORALITY_CUMULATIVE
      metrics_flush_interval: 15s
      aggregation_cardinality_limit: 5000
  exporters:
    otlp_http/newrelic:
      endpoint: https://otlp.nr-data.net
      headers:
        api-key: ${env:NEW_RELIC_LICENSE_KEY}
      compression: gzip   # NR também aceita zstd
    otlp_http/prometheus:
      endpoint: http://<prometheus-svc>.observability.svc.cluster.local:9090/api/v1/otlp   # o exporter acrescenta /v1/metrics
    otlp_http/loki:
      endpoint: http://<loki-svc>.observability.svc.cluster.local:3100/otlp   # o exporter acrescenta /v1/logs
  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, filter/health, transform/sanitize, batch]
        exporters: [otlp_http/newrelic, span_metrics]
      metrics:
        receivers: [span_metrics]
        processors: [memory_limiter, batch]
        exporters: [otlp_http/prometheus]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp_http/loki]
```
#### Agente (DaemonSet) - values do chart 0.178.2: presets logsCollection e kubernetesAttributes, só pipeline de logs, envio por gRPC ao gateway. O exclude repete o padrão do próprio agente e acrescenta o do gateway, para evitar laço de logs. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl | https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/clusterrole.yaml | https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/v0.163.0/exporter/otlpexporter/metadata.yaml)
```yaml
mode: daemonset
fullnameOverride: otel-agent
image:
  repository: otel/opentelemetry-collector-contrib
  tag: "0.163.2"
presets:
  logsCollection:
    enabled: true
    includeCollectorLogs: false
  kubernetesAttributes:
    enabled: true          # cria ClusterRole: pods/namespaces e replicasets [get, list, watch]
resources:
  requests:
    cpu: 50m
    memory: 128Mi
  limits:
    memory: 256Mi
ports:
  jaeger-compact:
    enabled: false
  jaeger-thrift:
    enabled: false
  jaeger-grpc:
    enabled: false
  zipkin:
    enabled: false
config:
  receivers:
    jaeger: null
    zipkin: null
    file_log:               # nome gerado pelo chart (rewriteDeprecatedComponentNames: true)
      exclude:
        - /var/log/pods/observability_otel-agent*_*/opentelemetry-collector/*.log
        - /var/log/pods/observability_otel-gateway*_*/opentelemetry-collector/*.log
  exporters:
    otlp_grpc/gateway:
      endpoint: otel-gateway.observability.svc.cluster.local:4317
      tls:
        insecure: true
  service:
    pipelines:
      traces: null
      metrics: null
      logs:
        receivers: [file_log]
        processors: [memory_limiter, k8s_attributes, batch]   # listado aqui, o preset não faz prepend
        exporters: [otlp_grpc/gateway]
```
#### kube-prometheus-stack: ligar o receptor OTLP nativo (opção recomendada) ou, como alternativa, o receptor de remote write. Chaves lidas na main (chart 92.17.1); conferir na versão que o projeto fixar. (https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml | https://prometheus.io/docs/guides/opentelemetry/)
```yaml
prometheus:
  prometheusSpec:
    enableOTLPReceiver: true        # --web.enable-otlp-receiver -> /api/v1/otlp/v1/metrics
    otlp: {}                        # padrão do Prometheus: translation_strategy UnderscoreEscapingWithSuffixes
    # otlp:
    #   promoteResourceAttributes: [service.namespace]
    # Alternativa (escolher uma das duas vias):
    # enableRemoteWriteReceiver: true   # --web.enable-remote-write-receiver -> /api/v1/write
```
#### Alternativa ao otlp_http/prometheus: exporter prometheus_remote_write para /api/v1/write. Exige enableRemoteWriteReceiver: true no kube-prometheus-stack. O endpoint agora vai em http.endpoint. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/exporter/prometheusremotewriteexporter/README.md)
```yaml
exporters:
  prometheus_remote_write:
    http:
      endpoint: http://<prometheus-svc>.observability.svc.cluster.local:9090/api/v1/write
    target_info:
      enabled: true
    # translation_strategy: UnderscoreEscapingWithSuffixes   # padrão; add_metric_suffixes está deprecado
service:
  pipelines:
    metrics:
      receivers: [span_metrics]
      processors: [memory_limiter, batch]
      exporters: [prometheus_remote_write]
```
#### Deployment do flag-service e dos demais serviços Flask: fazer a instrumentação 0.66b1 gravar também http.response.status_code. Sem esta variável, só sai http.status_code. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-python-contrib/v0.66b1/opentelemetry-instrumentation/src/opentelemetry/instrumentation/_semconv.py)
```yaml
# trecho de spec.template.spec.containers[].env
env:
  - name: OTEL_SEMCONV_STABILITY_OPT_IN
    value: http/dup   # grava http.status_code (antigo) e http.response.status_code (novo)
```
#### Expressão PromQL da regra de alerta no Grafana (datasource Prometheus): fração de spans SERVER do flag-service com erro (5xx) em 5 minutos. O numerador não existe antes do primeiro erro, por isso o 'or vector(0)'. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/connector/spanmetricsconnector/README.md | https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/v0.163.0/internal/coreinternal/traceutil/traceutil.go)
```yaml
expr: |
  (
    sum(rate(traces_span_metrics_calls_total{service_name="flag-service", span_kind="SPAN_KIND_SERVER", status_code="STATUS_CODE_ERROR"}[5m]))
    or vector(0)
  )
  /
  (
    sum(rate(traces_span_metrics_calls_total{service_name="flag-service", span_kind="SPAN_KIND_SERVER"}[5m])) > 0
  )
# Variante pelo código HTTP:
#   com OTEL_SEMCONV_STABILITY_OPT_IN=http ou http/dup: http_response_status_code=~"5.."
#   sem a variável: http_status_code=~"5.."
# Sem tráfego, o denominador some e o resultado vira No Data: configurar o estado No Data no Grafana.
```

### riscos
- Renomeações em 0.163: span_metrics, otlp_http, otlp_grpc (exporter), file_log, k8s_attributes e prometheus_remote_write. Os nomes antigos ainda funcionam, mas geram aviso de depreciação e serão removidos. O laboratório local e a doc do Loki ainda usam spanmetrics/otlphttp; padronizar tudo nos nomes novos.
- Overrides no chart precisam usar os nomes que o chart gera (rewriteDeprecatedComponentNames: true gera file_log e k8s_attributes). Um override escrito como filelog ou k8sattributes vira outro componente, fora do pipeline, e não tem efeito. [INCERTO] se o Collector aceita os dois nomes juntos ou acusa duplicidade.
- Dimensão HTTP: o repositório não define OTEL_SEMCONV_STABILITY_OPT_IN, então o Flask 0.66b1 grava só http.status_code e a dimensão http.response.status_code fica omitida. Opções: definir http/dup nos Deployments ou alertar por status_code=STATUS_CODE_ERROR, que independe do nome do atributo. [INCERTO] se o opt-in altera nomes de span ou outros atributos; testar antes no laboratório local.
- Fixar histogram.unit: ms. O README avisa que o padrão vai mudar para s; nesse caso, o nome passaria de _milliseconds para _seconds e os painéis quebrariam.
- collector.instance.id agora é dimensão padrão: cada reinício do gateway cria séries novas. Painéis e alertas devem agregar com sum(...). Vale manter a dimensão, porque ela evita conflito de escrita se o gateway tiver mais de uma réplica.
- O flush padrão do span_metrics é a cada 60s e atrasa o alerta e o self-healing; usar 15s com janela de rate de 5m. A série com STATUS_CODE_ERROR só existe depois do primeiro erro, e sem tráfego a razão fica sem dados; tratar o No Data na regra do Grafana.
- Erros 5xx gerados fora do Flask não entram na taxa: timeout ou queda de worker do Gunicorn e 502/504 do ALB ou Ingress não produzem span SERVER do flag-service.
- O prometheus_remote_write descarta métricas que não sejam cumulativas, e o receptor OTLP do Prometheus só aceita delta com otlp-deltatocumulative (experimental). Manter AGGREGATION_TEMPORALITY_CUMULATIVE, que é o padrão.
- Os receptores OTLP e remote write do Prometheus não têm autenticação (a doc os deixa desligados por isso). Manter o Prometheus só como ClusterIP, sem Ingress público.
- As chaves do kube-prometheus-stack foram lidas da branch main (chart 92.17.1, operator v0.94.2); conferir na versão que o projeto fixar. A doc consultada do Prometheus é a 3.15 (latest).
- O chart vem com resources: {}. Sem limits.memory, o memory_limiter por percentual e o GOMEMLIMIT ficam sem o limite do container como referência [provável]. Definir limites; nos m7i-flex.large de 8 GiB, sugiro 512Mi no gateway e 256Mi por nó no agente.
- Laço de logs: o preset exclui só os logs do próprio release. Sem a exclusão manual, o agente coleta os logs do gateway e, com o Loki fora do ar, os erros de exportação viram novos logs. Manter o gateway no file_log.exclude e não usar o exporter debug com verbosity: detailed no pipeline de logs.
- Cardinalidade no Loki: o operador container grava k8s.pod.name e o preset extrai service.instance.id. Os dois viram index labels por padrão, e a doc do Loki desaconselha. Ajustar o otlp_config do Loki (frente do Loki).
- start_at: end com storeCheckpoints: false perde as linhas escritas enquanto o agente reinicia. Ligar storeCheckpoints grava em /var/lib/otelcol no host e faz o Collector rodar como root.
- New Relic: a license key entra por Secret e extraEnvs (secretKeyRef), nunca nos values versionados. O NR responde sucesso após validar só autenticação, tamanho e rate limit; erros de conteúdo aparecem depois como NrIntegrationError. Payload acima de 1MB é rejeitado, por isso o send_batch_max_size.
- O transform/sanitize aplica keep_keys no recurso e apaga k8s.* dos traces. Não ligar o preset kubernetesAttributes no gateway: ele insere k8s_attributes no início dos traces e o sanitize apagaria o resultado. Se quiser k8s.* no New Relic, ampliar a lista permitida.
- Logs duplicados: se algum serviço também exportar logs por OTLP pelo SDK, além do stdout coletado pelo agente, cada linha chega duas vezes. Manter um único caminho.
- Para que os logs tenham o mesmo service.name dos traces, anotar os pods com resource.opentelemetry.io/service.name (o preset usa otel_annotations: true). Não verifiquei a ordem que o k8s_attributes usa para derivar service.name por padrão.
- O chart 0.178.2 saiu em 2026-11-02, há 1 dia; a 0.177.0 (2026-10-22) também usa appVersion 0.163.2. Em qualquer versão, image.repository vem vazio e precisa ser definido. Conferir no helm template se o DaemonSet recebe a variável K8S_NODE_NAME que o preset usa.
- O error_mode: propagate, validado no laboratório, descarta o lote inteiro se uma instrução OTTL falhar. No cluster, avaliar ignore.
- Método: cerca de 33 downloads HTTP em cerca de 20 chamadas, acima do teto de ~25, porque as renomeações obrigaram a conferir cada metadata.yaml. Duas fontes estão fora da lista explícita: docs.newrelic.com (pedida no item 5) e o repositório oficial open-telemetry/opentelemetry-python-contrib (tag v0.66b1). Arquivos baixados em C:\Users\Gabriel\AppData\Local\Temp\claude\C--Users-Gabriel-Documents-GitHub-tech-challenge-04\0c6ae1db-1d45-4b74-9ec0-857241e35810\scratchpad\otel-research\dl. Nenhum arquivo do repositório foi alterado.

## charts
- [confirmado] kube-prometheus-stack: versão: `92.17.1` -- Última versão estável publicada até 2026-11-03 (não é prerelease). Saiu em 2026-11-03 00:04 UTC; a anterior, 92.17.0, saiu em 2026-10-31. (https://artifacthub.io/api/v1/packages/helm/prometheus-community/kube-prometheus-stack)
- [confirmado] kube-prometheus-stack: appVersion: `v0.94.2` -- appVersion do chart 92.17.1, que é a versão do prometheus-operator. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/Chart.yaml)
- [confirmado] kube-prometheus-stack: kubeVersion: `>=1.25.0-0` -- kubeVersion exigido pelo chart. O EKS 1.34 atende. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/Chart.yaml)
- [confirmado] kube-prometheus-stack: versão do Prometheus: `v3.15.1-distroless` -- Imagem padrão do Prometheus em prometheus.prometheusSpec.image: registry quay.io, repository prometheus/prometheus. Ou seja, Prometheus 3.15.1 na variante distroless. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: subcharts: `grafana 14.3.1; kube-state-metrics 8.8.0; prometheus-node-exporter 4.60.1; crds 0.0.0` -- Dependências do chart 92.17.1: grafana 14.3.1 vindo de oci://ghcr.io/grafana-community/helm-charts (condition grafana.enabled); kube-state-metrics 8.8.0 e prometheus-node-exporter 4.60.1 vindos de oci://ghcr.io/prometheus-community/charts;  (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/Chart.yaml)
- [confirmado] kube-prometheus-stack: desligar Alertmanager: `alertmanager.enabled: false (padrão: true)` -- O Alertmanager vem ligado por padrão. Para desligar, usar alertmanager.enabled: false. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: datasource Alertmanager no Grafana: `grafana.sidecar.datasources.alertmanager.enabled: false (padrão: true)` -- A datasource Alertmanager do Grafana depende só de grafana.sidecar.datasources.alertmanager.enabled, que vem true por padrão. O template não olha alertmanager.enabled. Com o Alertmanager desligado, essa chave também precisa ir para false; s (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/templates/grafana/configmaps-datasources.yaml)
- [confirmado] kube-prometheus-stack: receptor de remote write: `prometheus.prometheusSpec.enableRemoteWriteReceiver: false (padrão)` -- Chave dedicada que liga a flag --web.enable-remote-write-receiver do Prometheus. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: receptor OTLP nativo: `prometheus.prometheusSpec.enableOTLPReceiver: false (padrão); prometheus.prometheusSpec.otlp: {}` -- O chart tem uma chave dedicada para o receptor OTLP do Prometheus, além de um bloco otlp para ajustes. O bloco otlp traz como exemplos comentados promoteResourceAttributes e keepIdentifyingResourceAttributes, com referência ao guia oficial. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] Prometheus: endpoint OTLP: `--web.enable-otlp-receiver ; POST /api/v1/otlp/v1/metrics` -- O receptor OTLP nativo é ligado pela flag --web.enable-otlp-receiver e recebe métricas por HTTP no caminho /api/v1/otlp/v1/metrics. (https://prometheus.io/docs/guides/opentelemetry/)
- [confirmado] kube-prometheus-stack: flags extras: `prometheus.prometheusSpec.additionalArgs: []` -- Chave genérica para passar argumentos extras ao container do Prometheus; serve de alternativa às chaves dedicadas. [INCERTO] o formato de cada item (name/value) segue a API do prometheus-operator, que não foi consultada. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: retenção: `prometheus.prometheusSpec.retention: 10d ; prometheus.prometheusSpec.retentionSize: ''` -- Retenção padrão de 10d. retentionSize vem vazio e usa o formato '50GiB'. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: armazenamento persistente: `prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName: gp3` -- storageSpec vem vazio. O exemplo comentado usa volumeClaimTemplate.spec com storageClassName, accessModes [ReadWriteOnce] e resources.requests.storage. Para o projeto, basta trocar storageClassName por gp3. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: recursos: `prometheus.prometheusSpec.resources: {} ; prometheusOperator.resources: {} ; grafana.resources: {}` -- resources vem {} por padrão no Prometheus, no operator e no Grafana. kube-state-metrics e node-exporter têm blocos próprios de subchart (chaves kube-state-metrics: e prometheus-node-exporter:). [INCERTO] o nome exato da chave de resources d (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: componentes a manter: `kubeStateMetrics.enabled: true; nodeExporter.enabled: true; kubelet.enabled: true; kubeApiServer.enabled: true; coreDns.enabled: true` -- Devem ficar ligados (todos já vêm true): kubeStateMetrics, nodeExporter, kubelet, kubeApiServer e coreDns. [provável] O CPU/memória por pod vem do cAdvisor (via kubelet) e do kube-state-metrics. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [provavel] kube-prometheus-stack: componentes a desligar no EKS: `kubeControllerManager.enabled: false; kubeEtcd.enabled: false; kubeScheduler.enabled: false; kubeProxy.enabled: false` -- Candidatos a desligar no EKS: kubeControllerManager, kubeEtcd, kubeScheduler e kubeProxy (todos true por padrão). O plano de controle é gerenciado pela AWS, e os ServiceMonitors padrão costumam gerar alvos inalcançáveis e alertas TargetDown (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [provavel] kube-prometheus-stack: regras padrão: `defaultRules.rules.<grupo>: false` -- Cada grupo de regras tem sua própria chave, todas true por padrão. Para economizar, desligar as de componentes ausentes: alertmanager, etcd, kubeControllerManager, kubeSchedulerAlerting, kubeSchedulerRecording, kubeProxy e windows. Opcional (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: dashboards padrão: `grafana.defaultDashboardsEnabled: true ; prometheus.prometheusSpec.remoteWriteDashboards: false` -- Manter grafana.defaultDashboardsEnabled: true, porque inclui os dashboards de CPU/memória. Os dashboards de remote write já vêm desligados. [INCERTO] Não li os templates para saber se os dashboards de etcd, scheduler, controller-manager e p (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [provavel] kube-prometheus-stack: seleção de ServiceMonitors e regras: `serviceMonitorSelectorNilUsesHelmValues: true; podMonitorSelectorNilUsesHelmValues: true; ruleSelectorNilUsesHelmValues: true (em prometheus.prometheusSpec)` -- Os seletores '*NilUsesHelmValues' vêm true. Com false, o Prometheus passa a selecionar ServiceMonitors, PodMonitors e PrometheusRules criados por outras Applications, sem o label do release. Esse efeito não foi lido no comentário do values. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack: CRDs: `crds.enabled: true ; crds.upgradeJob.enabled: false` -- Os CRDs vêm do subchart local crds. O job de upgrade de CRDs está em preview e vem desligado. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] kube-prometheus-stack + Argo CD: syncOptions: `ServerSideApply=true` -- O README do chart tem uma seção 'Argo CD'. Ela explica que os CRDs passam do limite de 262144 bytes da anotação last-applied-configuration (crd-prometheuses.yaml tem cerca de 840 KiB) e manda sincronizar com ServerSideApply=true. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/README.md)
- [confirmado] kube-prometheus-stack: outros padrões: `windowsMonitoring.enabled: false ; thanosRuler.enabled: false` -- O monitoramento Windows e o Thanos Ruler já vêm desligados. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [provavel] kube-prometheus-stack: webhooks de admissão (opcional): `prometheusOperator.admissionWebhooks.enabled: false` -- O README cita a chave que desliga os hooks do webhook de admissão. Isso reduziria os Jobs de hook no Argo CD, mas o README fala disso no contexto de GKE privado. O uso no projeto é inferência e opcional. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/README.md)
- [confirmado] grafana (subchart): versão e origem: `grafana chart 14.3.1 ; appVersion: 13.3.0 ; kubeVersion: ^1.25.0-0` -- O subchart grafana 14.3.1 é mantido no repositório grafana-community/helm-charts, não mais no grafana/helm-charts. Ele traz o Grafana 13.3.0 e exige kubeVersion ^1.25.0-0, que o EKS 1.34 atende. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/Chart.yaml)
- [confirmado] grafana (subchart): imagem: `grafana.image.registry: docker.io ; grafana.image.repository: grafana/grafana ; grafana.image.tag: '{{ .Chart.AppVersion }}-distroless' ; grafana.image.sha: ''` -- Chaves da imagem. A tag padrão é a appVersion com o sufixo -distroless, ou seja, 13.3.0-distroless. Dentro do kps, as chaves ficam sob grafana.image. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/values.yaml)
- [confirmado] grafana: tag 13.3.0 existe: `13.3.0 (digest sha256:488984b716c0862639f91a698adbe2862677a5a07bad42da5f03f3030883b205); 13.3.0-distroless (sha256:540b8afb775bf34aefce417e4329039daa5d44b6f2fbda6881397b1b247ca7df)` -- A tag grafana/grafana:13.3.0 existe no Docker Hub (push em 2026-10-27, arquiteturas amd64, arm64 e arm). A variante 13.3.0-distroless, padrão do chart, também existe. A release no GitHub grafana/grafana não foi consultada. (https://hub.docker.com/v2/repositories/grafana/grafana/tags?name=13.3.0&page_size=50)
- [confirmado] grafana: senha do admin a partir de Secret: `grafana.admin.existingSecret: '' ; grafana.admin.userKey: admin-user ; grafana.admin.passwordKey: admin-password` -- O admin pode vir de um Secret existente, com as chaves de usuário e senha configuráveis. No kps, adminPassword vem comentado. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] grafana: sidecar de dashboards: `grafana.sidecar.dashboards.enabled: true ; label: grafana_dashboard ; labelValue: '1' ; searchNamespace: ALL` -- O kps sobrescreve o sidecar de dashboards: ligado, label grafana_dashboard, labelValue '1' e busca em todos os namespaces. No chart grafana puro, os padrões são enabled false, labelValue '' e searchNamespace null (linhas 1243, 1267 e 1279). (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] grafana: datasource Prometheus padrão e uid: `grafana.sidecar.datasources.uid: prometheus` -- O uid da datasource Prometheus padrão é fixado por grafana.sidecar.datasources.uid, cujo padrão é prometheus. O template usa esse valor direto. Outros valores do bloco: name Prometheus, isDefaultDatasource true, defaultDatasourceEnabled tru (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/templates/grafana/configmaps-datasources.yaml)
- [confirmado] grafana: sidecar de alertas: `grafana.sidecar.alerts.enabled: false (padrão) ; label: grafana_alert ; labelValue: '' ; searchNamespace: null ; resource: both` -- O sidecar de alertas vem desligado e o kps não sobrescreve. Ele lê ConfigMaps/Secrets com o label configurado, aceita searchNamespace ALL e recarrega via /api/admin/provisioning/alerting/reload. No kps, usar o prefixo grafana. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/values.yaml)
- [confirmado] grafana: datasources adicionais: `grafana.additionalDataSources: [] ; grafana.additionalDataSourcesString: '' ; grafana.deleteDatasources: []` -- Datasources extras entram em additionalDataSources (lista processada por tpl) ou em additionalDataSourcesString. Elas vão para o mesmo ConfigMap da datasource padrão. O exemplo traz name, access, type, url, jsonData e editable. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
- [confirmado] grafana: alerting por values e env a partir de Secret: `grafana.alerting: {} ; grafana.envValueFrom: {} ; grafana.envFromSecret: '' ; grafana.envFromSecrets: []` -- O chart permite provisionar alerting (políticas, contact points) direto pelos values, como alternativa ao sidecar, e injetar variáveis vindas de Secret. envValueFrom recebe <ENV>: <valueFrom em YAML>. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/values.yaml)
- [confirmado] grafana: persistência: `grafana.persistence.enabled: false (type: pvc, size: 10Gi)` -- A persistência do Grafana vem desligada por padrão. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/values.yaml)
- [confirmado] grafana: imagem do sidecar: `quay.io/kiwigrid/k8s-sidecar:2.14.3` -- Imagem padrão dos sidecars de dashboards, datasources e alertas. (https://raw.githubusercontent.com/grafana-community/helm-charts/grafana-14.3.1/charts/grafana/values.yaml)
- [confirmado] loki: versão: `loki 7.5.0 ; appVersion: 3.6.16` -- Última versão estável do chart loki até 2026-11-03: publicada em 2026-10-22 (a anterior na listagem é 7.3.0, de 2026-08-10). O código-fonte fica em grafana/loki (tag helm-loki-7.5.0, production/helm/loki) e o pacote sai nas releases do graf (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/Chart.yaml)
- [confirmado] loki: tag de imagem padrão: `loki.image.registry: docker.io ; loki.image.repository: grafana/loki ; loki.image.tag: 3.6.11` -- O values fixa loki.image.tag em 3.6.11, diferente da appVersion 3.6.16. Como o valor é explícito, o padrão do chart implanta 3.6.11 a menos que seja sobrescrito. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: deploymentMode: `deploymentMode: SingleBinary (padrão: SimpleScalable)` -- O padrão é SimpleScalable. SingleBinary é indicado para instalações pequenas. SimpleScalable e Distributed exigem object storage. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: réplicas no SingleBinary: `singleBinary.replicas: 1 ; read.replicas: 0 ; write.replicas: 0 ; backend.replicas: 0` -- Por padrão, singleBinary.replicas é 0 e read/write/backend têm 3 réplicas. O validate.yaml faz o render falhar se houver réplicas de single binary e simple scalable ao mesmo tempo. Com filesystem, também falha se singleBinary.replicas passa (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/templates/validate.yaml)
- [confirmado] loki: storage filesystem: `loki.storage.type: filesystem ; loki.storage.filesystem.chunks_directory: /var/loki/chunks ; loki.storage.filesystem.rules_directory: /var/loki/rules` -- O tipo de storage padrão é s3. O bloco filesystem define os diretórios de chunks e de rules. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: auth_enabled: `loki.auth_enabled: false (padrão: true)` -- A autenticação (multi-tenant) vem ligada por padrão. Para usar sem tenant, auth_enabled: false. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [provavel] loki: replication_factor: `loki.commonConfig.replication_factor: 1 (padrão: 3)` -- O fator de replicação padrão é 3. Com uma única réplica de single binary, o esperado é 1. A chave está confirmada; a recomendação da doc oficial do monolítico não foi lida nesta pesquisa. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: schemaConfig mínimo: `loki.schemaConfig.configs: [{from: '2024-04-01', store: tsdb, object_store: filesystem, schema: v13, index: {prefix: index_, period: 24h}}]` -- schemaConfig é obrigatório (vem vazio por padrão). O exemplo de teste do próprio chart serve de base: tsdb, v13, índice de 24h. Para o projeto, object_store: filesystem. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/templates/validate.yaml)
- [confirmado] loki: gateway, minio e caches: `gateway.enabled: false ; minio.enabled: false ; chunksCache.enabled: false ; resultsCache.enabled: false ; memcachedExporter.enabled: false` -- Gateway, chunksCache, resultsCache, memcached e memcachedExporter vêm ligados por padrão; minio já vem desligado. Para economizar, desligar gateway, chunksCache, resultsCache e memcachedExporter. [INCERTO] se memcached.enabled também precis (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: lokiCanary e test: `lokiCanary.enabled: false ; test.enabled: false` -- lokiCanary e test vêm ligados. O validate.yaml falha se test estiver ligado com o canary desligado, então os dois precisam ser desligados juntos. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/templates/validate.yaml)
- [confirmado] loki: recursos e persistência do single binary: `singleBinary.resources: {} ; singleBinary.persistence.enabled: true ; size: 10Gi ; storageClass: null (definir gp3) ; whenDeleted: Delete ; enableStatefulSetAutoDeletePVC: true` -- resources vem {}. A persistência vem ligada (10Gi, ReadWriteOnce), sem storageClass definida; o comentário diz que, sem ela, vale o provisionador padrão (gp2 na AWS). Por padrão, o PVC é apagado quando o StatefulSet é apagado. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] loki: endpoint OTLP: `endpoint: http://<loki-addr>/otlp` -- Para enviar logs do OpenTelemetry Collector ao Loki, a doc manda usar o exporter otlphttp com endpoint terminando em /otlp; o exporter completa com /v1/logs. (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] loki: allow_structured_metadata: `loki.limits_config.allow_structured_metadata: true` -- Na ingestão OTLP, allow_structured_metadata precisa ser true, senão o Loki rejeita o payload. Já é o padrão no Loki 3. O chart não define essa chave: limits_config só traz reject_old_samples, reject_old_samples_max_age, max_cache_freshness_ (https://grafana.com/docs/loki/latest/send-data/otel/)
- [confirmado] loki: componentes auxiliares: `sidecar.rules.enabled: true (padrão) ; monitoring.selfMonitoring.enabled: false ; monitoring.dashboards.enabled: false ; monitoring.rules.enabled: false ; monitoring.serviceMonitor.enabled: false ; loki.pattern_ingester.enabled: false ; loki.structuredConfig: {}` -- O sidecar de rules vem ligado e pode ser desligado se o ruler do Loki não for usado. Monitoramento próprio, dashboards, rules, serviceMonitor e pattern_ingester já vêm desligados. Uma chave config no topo é proibida; ajustes extras vão em l (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
- [confirmado] opentelemetry-collector: versão: `opentelemetry-collector 0.178.2 ; appVersion: 0.163.2` -- Última versão estável do chart até 2026-11-03: publicada em 2026-11-02 21:03 UTC. A appVersion é exatamente a contrib usada no projeto. No ArtifactHub, o repositório se chama opentelemetry-helm (URL https://open-telemetry.github.io/opentele (https://artifacthub.io/api/v1/packages/helm/opentelemetry-helm/opentelemetry-collector)
- [confirmado] opentelemetry-collector: mode: `mode: deployment (gateway) | daemonset (agente) — padrão ''` -- mode é obrigatório e vem vazio. Sem um valor válido, o NOTES.txt chama fail e o render falha. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/NOTES.txt)
- [confirmado] opentelemetry-collector: imagem: `image.repository: otel/opentelemetry-collector-contrib ; image.tag: '' (= 0.163.2) ; image.digest: ''` -- image.repository é obrigatório e vem vazio, com fail no NOTES.txt. image.tag vazio usa a appVersion, 0.163.2. image.digest força o pull por digest. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: command: `command.name: '' ; command.extraArgs: []` -- Com command.name vazio, o chart não define command e usa o ENTRYPOINT da imagem, sempre com --config=/conf/relay.yaml. [provável] Na imagem contrib, esse ENTRYPOINT é /otelcol-contrib; se quiser explícito, command.name: otelcol-contrib. Par (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_pod.tpl)
- [confirmado] opentelemetry-collector: aceita contrib 0.163.2: `otel/opentelemetry-collector-contrib:0.163.2 (digest do índice sha256:7f22d2a6748110ffb6a59bc0df448bccbf501cdb667d610ede4c61d3863d5849)` -- O chart aceita a contrib 0.163.2: ela é a appVersion, portanto a tag padrão. A imagem existe no Docker Hub com amd64, que é a arquitetura x86_64 do m7i-flex. (https://hub.docker.com/v2/repositories/otel/opentelemetry-collector-contrib/tags?name=0.163&page_size=50)
- [confirmado] opentelemetry-collector: fullnameOverride: `fullnameOverride: '' ; nameOverride: ''` -- Chaves para fixar os nomes dos recursos; úteis para ter duas Applications do mesmo chart (gateway e agente). (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: presets.logsCollection: `presets.logsCollection.enabled: false ; includeCollectorLogs: false ; storeCheckpoints: false ; maxRecombineLogSize: 102400` -- O preset cria o receiver file_log (filelog se rewriteDeprecatedComponentNames for false) e o adiciona em service.pipelines.logs.receivers. Configuração gerada: include [/var/log/pods/*/*/*.log], exclusão dos logs do próprio collector, start (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] opentelemetry-collector: usuário root com storeCheckpoints: `storeCheckpoints: true + securityContext vazio → runAsUser: 0, runAsGroup: 0` -- Só com storeCheckpoints: true e securityContext vazio o chart roda o container como root. Sem isso, vale o usuário padrão da imagem. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_pod.tpl)
- [confirmado] opentelemetry-collector: presets.kubernetesAttributes: `presets.kubernetesAttributes.enabled: false ; extractAllPodLabels: false ; extractAllPodAnnotations: false` -- O preset coloca o processor k8s_attributes (k8sattributes se a reescrita estiver desligada) no início das pipelines logs, metrics e traces que existirem, e adiciona RBAC mínimo ao ClusterRole. Configuração gerada: em daemonset, filter.node_ (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] opentelemetry-collector: presets.kubeletMetrics: `presets.kubeletMetrics.enabled: false → kubeletstats {collection_interval: 20s, auth_type: serviceAccount, endpoint: ${env:K8S_NODE_IP}:10250}` -- O preset cria o receiver kubeletstats na pipeline metrics e adiciona regras ao ClusterRole; o comentário recomenda daemonset. No projeto pode ficar desligado, porque o kube-prometheus-stack já cobre CPU/memória (inferência). (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
- [confirmado] opentelemetry-collector: nomes novos dos componentes: `rewriteDeprecatedComponentNames: true` -- Por padrão, a config gerada usa os nomes novos dos componentes (ex.: k8s_attributes, file_log). O comentário manda desligar só para imagens antigas. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: como passar a config: `config: {…} (mesclado) ; alternateConfig: {} (não mesclado)` -- A chave config é mesclada com a config padrão. A padrão traz receivers jaeger, otlp, prometheus e zipkin; exporter debug; processors batch e memory_limiter; extensão health_check; e pipelines logs, metrics e traces. config não remove o que  (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: health_check obrigatório: `config.extensions.health_check.endpoint: ${env:MY_POD_IP}:13133` -- A extensão health_check, ou a healthcheckv2, precisa estar na lista de extensões; sem ela o render falha e as probes não passam. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: memory_limiter padrão: `processors.memory_limiter: {check_interval: 5s, limit_percentage: 80, spike_limit_percentage: 25}` -- O chart já define memory_limiter na config padrão, por porcentagem. Na mescla, esses valores convivem com os da config local do projeto. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: env a partir de Secret: `extraEnvs: [] ; extraEnvsFrom: []` -- extraEnvs aceita templates e é renderizado direto em env do container, por isso aceita EnvVar padrão com valueFrom.secretKeyRef. Para carregar um Secret inteiro, existe extraEnvsFrom. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_pod.tpl)
- [confirmado] opentelemetry-collector: portas: `ports.otlp / ports.otlp-http / ports.jaeger-compact / ports.jaeger-thrift / ports.jaeger-grpc / ports.zipkin: enabled: true ; ports.metrics.enabled: false` -- Vêm habilitadas, com hostPort: otlp (4317, appProtocol grpc), otlp-http (4318), jaeger-compact (6831/UDP), jaeger-thrift (14268), jaeger-grpc (14250) e zipkin (9411). A porta metrics (8888) vem desligada e precisa ser ligada para usar Servi (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] opentelemetry-collector: recursos: `resources: {} ; useGOMEMLIMIT: true ; replicaCount: 1` -- resources vem {}, e o próprio chart recomenda definir limites. useGOMEMLIMIT define GOMEMLIMIT como 80% de resources.limits.memory e só funciona se esse limite existir. replicaCount padrão é 1. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
- [confirmado] argo-cd: versão instalada pelo chart 7.7.11: `Argo CD v2.13.2` -- O chart argo-cd 7.7.11, publicado em 2024-12-21, instala o Argo CD v2.13.2 e exige kubeVersion >=1.25.0-0. O pacote vem das releases do argoproj/argo-helm. (https://artifacthub.io/api/v1/packages/helm/argo/argo-cd/7.7.11)
- [confirmado] argo-cd: Applications com várias fontes: `spec.sources[].ref: values ; spec.sources[].helm.valueFiles: [$values/<caminho>/values.yaml]` -- A v2.13.2 suporta spec.sources com uma fonte Git marcada com ref: values, cujos arquivos o chart referencia como $values/<caminho> em helm.valueFiles. O caso exato do projeto aparece na doc dessa versão, inclusive com um exemplo do promethe (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/multiple_sources.md)
- [confirmado] argo-cd: regras das várias fontes: `sources (plural) substitui source ; fonte com ref: sem chart` -- Regras da v2.13.2: quando há sources, o campo source é ignorado. A fonte com ref não pode ter chart. $values só pode aparecer no início do caminho. Se a fonte ref tiver path, o Argo também gera recursos daquele caminho; sem path, o repositó (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/multiple_sources.md)
- [confirmado] argo-cd: ServerSideApply: `spec.syncPolicy.syncOptions: [ServerSideApply=true] ; anotação argocd.argoproj.io/sync-options: ServerSideApply=true` -- ServerSideApply=true faz o Argo usar kubectl apply --server-side. A doc o indica para recursos maiores que os 262144 bytes da anotação. Pode ser ligado na Application inteira ou por recurso, via anotação. Se Replace=true também estiver pres (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/sync-options.md)
- [confirmado] argo-cd: CreateNamespace e SkipDryRun: `syncOptions: [CreateNamespace=true] ; argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true` -- CreateNamespace=true cria o namespace observability. Quando um CR é sincronizado sem que o CRD dele esteja no mesmo sync (ex.: ServiceMonitor em outra Application), a anotação SkipDryRunOnMissingResource=true evita a falha do dry run. Se o  (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/sync-options.md)
- [confirmado] argo-cd: defasagem do chart: `argo-cd 10.11.7 (2026-11-03)` -- O chart argo-cd mais recente na listagem do ArtifactHub é 10.11.7 (2026-11-03), o que deixa o 7.7.11 quase dois anos atrás. [INCERTO] A versão do Argo CD trazida pelo 10.11.7 não foi confirmada. (https://artifacthub.io/api/v1/packages/helm/argo/argo-cd/7.7.11)

### trechos de configuracao
#### Values do kube-prometheus-stack 92.17.1 (Prometheus sem Alertmanager, receptor OTLP nativo, gp3, componentes do plano de controle do EKS desligados). As chaves vêm do values.yaml oficial; CPU, memória, disco e retenção são sugestões para 2 x m7i-flex.large e não vêm da fonte. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
```yaml
# kube-prometheus-stack 92.17.1 — namespace observability
# CPU/memória/disco/retenção abaixo são SUGESTÕES (não vêm da fonte).
crds:
  enabled: true
alertmanager:
  enabled: false
defaultRules:
  rules:
    alertmanager: false
    etcd: false
    kubeControllerManager: false
    kubeSchedulerAlerting: false
    kubeSchedulerRecording: false
    kubeProxy: false
    windows: false
    # opcionais (economia; afetam o dashboard do API server):
    # kubeApiserverAvailability: false
    # kubeApiserverBurnrate: false
    # kubeApiserverHistogram: false
    # kubeApiserverSlos: false
kubeControllerManager:
  enabled: false
kubeEtcd:
  enabled: false
kubeScheduler:
  enabled: false
kubeProxy:
  enabled: false
kubeStateMetrics:
  enabled: true   # manter: estado e requests dos pods
nodeExporter:
  enabled: true   # manter: métricas dos nós
windowsMonitoring:
  enabled: false
prometheusOperator:
  resources:
    requests:
      cpu: 50m
      memory: 128Mi
    limits:
      memory: 256Mi
prometheus:
  prometheusSpec:
    retention: 3d
    retentionSize: 6GiB
    enableOTLPReceiver: true          # recebe em /api/v1/otlp/v1/metrics
    enableRemoteWriteReceiver: false  # alternativa: true + exporter prometheusremotewrite
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
    resources:
      requests:
        cpu: 200m
        memory: 1Gi
      limits:
        memory: 2Gi
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 10Gi
```
#### Bloco grafana dentro dos values do kube-prometheus-stack: imagem fixada, admin vindo de Secret, sidecars de dashboards/datasources/alertas, datasource Alertmanager desligada, Loki com uid fixo e segredos dos contact points em variáveis de ambiente. As chaves vêm do values do kps e do chart grafana-community 14.3.1; nomes de Secret e URL do Loki são exemplos. (https://raw.githubusercontent.com/prometheus-community/helm-charts/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack/values.yaml)
```yaml
grafana:
  enabled: true
  image:
    registry: docker.io
    repository: grafana/grafana
    tag: '13.3.0'        # padrão do chart 14.3.1: '13.3.0-distroless'
  admin:
    existingSecret: grafana-admin   # Secret criado fora do Git
    userKey: admin-user
    passwordKey: admin-password
  defaultDashboardsEnabled: true
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      memory: 512Mi
  sidecar:
    dashboards:
      enabled: true
      label: grafana_dashboard
      labelValue: '1'
      searchNamespace: ALL
    datasources:
      enabled: true
      defaultDatasourceEnabled: true
      isDefaultDatasource: true
      name: Prometheus
      uid: prometheus
      alertmanager:
        enabled: false   # o template não olha alertmanager.enabled
    alerts:
      enabled: true
      label: grafana_alert
      labelValue: '1'
      searchNamespace: ALL
  additionalDataSources:
    - name: Loki
      type: loki
      uid: loki          # [provável] campo uid do provisioning de datasources
      access: proxy
      url: http://loki.observability.svc.cluster.local:3100   # [INCERTO] nome do Service
      editable: false
  envValueFrom:          # formato: <ENV>: <valueFrom em YAML>
    PAGERDUTY_ROUTING_KEY:
      secretKeyRef:
        name: grafana-alerting
        key: pagerduty-routing-key
    SLACK_WEBHOOK_URL:
      secretKeyRef:
        name: grafana-alerting
        key: slack-webhook-url
    GITHUB_DISPATCH_TOKEN:
      secretKeyRef:
        name: grafana-alerting
        key: github-token
```
#### Values do chart loki 7.5.0 em SingleBinary com filesystem, com gateway, caches, canary e test desligados. Esta combinação passa nas validações do templates/validate.yaml: réplicas de read/write/backend zeradas, uma réplica de single binary, schemaConfig presente e test desligado junto com o canary. Recursos são sugestão. (https://raw.githubusercontent.com/grafana/loki/helm-loki-7.5.0/production/helm/loki/values.yaml)
```yaml
# loki 7.5.0 — SingleBinary + filesystem
deploymentMode: SingleBinary
loki:
  auth_enabled: false
  commonConfig:
    replication_factor: 1
  storage:
    type: filesystem
  schemaConfig:
    configs:
      - from: '2024-04-01'
        store: tsdb
        object_store: filesystem
        schema: v13
        index:
          prefix: index_
          period: 24h
  limits_config:
    allow_structured_metadata: true   # padrão no Loki 3; explícito por causa do OTLP
  # image:
  #   tag: 3.6.11   # padrão do values; 3.6.16 (appVersion) só após confirmar a tag
singleBinary:
  replicas: 1
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      memory: 1Gi
  persistence:
    enabled: true
    size: 10Gi
    storageClass: gp3
read:
  replicas: 0
write:
  replicas: 0
backend:
  replicas: 0
gateway:
  enabled: false
minio:
  enabled: false
chunksCache:
  enabled: false
resultsCache:
  enabled: false
memcachedExporter:
  enabled: false
lokiCanary:
  enabled: false
test:
  enabled: false   # precisa desligar junto com lokiCanary
sidecar:
  rules:
    enabled: false
```
#### Values do chart opentelemetry-collector 0.178.2 para o gateway (Deployment): imagem contrib 0.163.2, portas que não serão usadas desligadas, chave do New Relic vinda de Secret e receivers padrão removidos com null. As chaves do chart vêm do values oficial; processors, connectors e exporters devem ser copiados da config local já validada. Os endpoints /otlp do Loki e /api/v1/otlp do Prometheus vêm das docs oficiais; nomes de Service e o endpoint do New Relic são placeholders. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/values.yaml)
```yaml
# opentelemetry-collector 0.178.2 — papel gateway
mode: deployment
fullnameOverride: otel-gateway
replicaCount: 1
image:
  repository: otel/opentelemetry-collector-contrib
  tag: '0.163.2'   # igual ao appVersion do chart
# command.name vazio = ENTRYPOINT da imagem; explícito (provável): otelcol-contrib
presets:
  kubernetesAttributes:
    enabled: true   # k8s_attributes no início das pipelines
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    memory: 512Mi   # ativa GOMEMLIMIT (80%)
ports:
  jaeger-compact:
    enabled: false
  jaeger-thrift:
    enabled: false
  jaeger-grpc:
    enabled: false
  zipkin:
    enabled: false
extraEnvs:
  - name: NEW_RELIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: otel-newrelic   # Secret criado fora do Git
        key: api-key
config:
  receivers:
    jaeger: null
    zipkin: null
    prometheus: null
  # processors (memory_limiter, transform/sanitize, filter/health) e connectors: copiar da config local validada
  connectors:
    spanmetrics: {}   # copiar da config local
  exporters:
    otlp_http/newrelic:
      endpoint: <endpoint da config local>
      headers:
        api-key: ${env:NEW_RELIC_API_KEY}
    otlp_http/loki:
      endpoint: http://<service-do-loki>:3100/otlp
    otlp_http/prometheus:
      endpoint: http://<service-do-prometheus>:9090/api/v1/otlp   # [provável] exporter acrescenta /v1/metrics
  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, filter/health, transform/sanitize, batch]
        exporters: [otlp_http/newrelic, spanmetrics]
      metrics:
        receivers: [otlp, spanmetrics]
        processors: [memory_limiter, batch]
        exporters: [otlp_http/prometheus]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp_http/loki]
```
#### Values do chart opentelemetry-collector 0.178.2 para o agente (DaemonSet), que coleta os logs de todos os pods. O preset logsCollection gera o receiver file_log e os hostPaths; o preset kubernetesAttributes filtra pelo nó. Todas as portas e pipelines que não serão usadas são removidas, e os logs seguem para o gateway. O comportamento dos presets foi conferido em templates/_config.tpl. (https://raw.githubusercontent.com/open-telemetry/opentelemetry-helm-charts/opentelemetry-collector-0.178.2/charts/opentelemetry-collector/templates/_config.tpl)
```yaml
# opentelemetry-collector 0.178.2 — papel agente (logs de todos os pods)
mode: daemonset
fullnameOverride: otel-agent
image:
  repository: otel/opentelemetry-collector-contrib
  tag: '0.163.2'
presets:
  logsCollection:
    enabled: true            # receiver file_log em /var/log/pods/*/*/*.log
    includeCollectorLogs: false
    storeCheckpoints: false  # true => runAsUser: 0 e hostPath /var/lib/otelcol
  kubernetesAttributes:
    enabled: true            # em daemonset filtra por K8S_NODE_NAME
resources:
  requests:
    cpu: 50m
    memory: 128Mi
  limits:
    memory: 256Mi
ports:
  otlp:
    enabled: false
  otlp-http:
    enabled: false
  jaeger-compact:
    enabled: false
  jaeger-thrift:
    enabled: false
  jaeger-grpc:
    enabled: false
  zipkin:
    enabled: false
config:
  receivers:
    otlp: null
    jaeger: null
    zipkin: null
    prometheus: null
  exporters:
    otlp_http/gateway:
      endpoint: http://otel-gateway.observability.svc.cluster.local:4318   # [INCERTO] nome do Service
  service:
    pipelines:
      logs:
        receivers: []          # o preset acrescenta file_log
        processors: [memory_limiter, batch]   # o preset põe k8s_attributes no início
        exporters: [otlp_http/gateway]
      metrics: null
      traces: null
```
#### Application do Argo CD (v2.13.2) para o kube-prometheus-stack, com o chart vindo do repositório Helm e os values vindos do Git (ref: values). Usa ServerSideApply=true, como manda o README do kps, e CreateNamespace=true. Repositório e caminho são placeholders. (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/multiple_sources.md)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kube-prometheus-stack
  namespace: argocd
spec:
  project: default
  destination:
    server: https://kubernetes.default.svc
    namespace: observability
  sources:
    - repoURL: https://prometheus-community.github.io/helm-charts
      chart: kube-prometheus-stack
      targetRevision: 92.17.1
      helm:
        valueFiles:
          - $values/gitops/<caminho>/kube-prometheus-stack/values.yaml
    - repoURL: https://github.com/<owner>/tech-challenge-04.git
      targetRevision: dev
      ref: values        # fonte com ref não pode ter chart
  syncPolicy:
    syncOptions:
      - ServerSideApply=true   # CRDs > 262144 bytes (README do kps)
      - CreateNamespace=true
```
#### Bloco sources das Applications do Loki e do OTel Collector. O OTel precisa de duas Applications (gateway e agente), com nomes e values diferentes. A estrutura segue a doc de várias fontes da v2.13.2; repositório e caminhos são placeholders. (https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/docs/user-guide/multiple_sources.md)
```yaml
# Loki
spec:
  sources:
    - repoURL: https://grafana.github.io/helm-charts
      chart: loki
      targetRevision: 7.5.0
      helm:
        valueFiles:
          - $values/gitops/<caminho>/loki/values.yaml
    - repoURL: https://github.com/<owner>/tech-challenge-04.git
      targetRevision: dev
      ref: values
---
# OTel Collector (uma Application para o gateway e outra para o agente)
spec:
  sources:
    - repoURL: https://open-telemetry.github.io/opentelemetry-helm-charts
      chart: opentelemetry-collector
      targetRevision: 0.178.2
      helm:
        valueFiles:
          - $values/gitops/<caminho>/otel-gateway/values.yaml
    - repoURL: https://github.com/<owner>/tech-challenge-04.git
      targetRevision: dev
      ref: values
```

### riscos
- O kube-prometheus-stack 92.17.1 foi publicado no próprio dia 2026-11-03 (00:04 UTC), e o chart recebe patches quase todo dia. Fixar targetRevision: 92.17.1 exatamente, sem curinga, e registrar a data da escolha.
- O subchart grafana mudou de repositório: o Chart.yaml oficial do kps 92.17.1 aponta para oci://ghcr.io/grafana-community/helm-charts (grafana 14.3.1). Esse repositório não estava na lista de fontes, mas é o que o próprio chart oficial usa; os values de referência devem vir dele, não do grafana/helm-charts.
- [INCERTO] O Argo CD v2.13.2 renderiza o kps a partir do .tgz do repositório HTTP. O esperado é que os subcharts (dependências OCI no ghcr.io) já venham dentro do pacote, mas não abri o .tgz para confirmar.
- Sem ServerSideApply=true, o sync do kps falha com 'metadata.annotations: Too long' (os CRDs passam de 262144 bytes). Atenção: se Replace=true estiver presente, ele prevalece sobre ServerSideApply=true.
- Se ServiceMonitors, PrometheusRules ou ConfigMaps de alerta ficarem numa Application que sincroniza antes dos CRDs do kps, usar sync-waves ou a anotação SkipDryRunOnMissingResource=true.
- Desligar o Alertmanager não remove a datasource 'Alertmanager' do Grafana. Também é preciso definir grafana.sidecar.datasources.alertmanager.enabled: false e defaultRules.rules.alertmanager: false.
- O argo-cd 7.7.11 instala a v2.13.2 (chart de 2024-12-21), enquanto o chart mais recente no ArtifactHub é o 10.11.7 (2026-11-03). [INCERTO] Não verifiquei a compatibilidade oficial da v2.13 com Kubernetes 1.34 nem se essa linha ainda tem suporte. Várias fontes com ref e ServerSideApply estão documentados na v2.13.2.
- Loki: o render falha (validate.yaml) se singleBinary.replicas for maior que 0 e read/write/backend ficarem no padrão 3. Também falha com filesystem e mais de 1 réplica, sem schemaConfig, com test.enabled sem lokiCanary.enabled ou com uma chave config no topo.
- O Loki 7.5.0 declara appVersion 3.6.16, mas o values fixa loki.image.tag: 3.6.11. Sem sobrescrever, roda a 3.6.11. [INCERTO] Não consultei se a imagem grafana/loki:3.6.16 existe.
- Na persistência do Loki, whenDeleted: Delete e enableStatefulSetAutoDeletePVC: true fazem o PVC (e os logs) ser apagado junto com o StatefulSet, por exemplo num prune ou recriação pelo Argo. Com storageClass null vale o padrão do cluster (o comentário cita gp2 na AWS), então definir gp3.
- [INCERTO] Não verifiquei a StorageClass gp3 na documentação da AWS. Em geral o EKS traz só a gp2, e a gp3 depende do add-on EBS CSI e de uma StorageClass 'gp3' criada pelo projeto. Sem ela, os PVCs do Prometheus e do Loki ficam Pending.
- [INCERTO] A retenção do Loki não foi configurada nos snippets, porque não verifiquei as chaves de retenção do compactor. Com filesystem e PVC de 10Gi, o disco pode encher se o ambiente ficar no ar por muito tempo.
- [INCERTO] Os nomes dos Services (Loki SingleBinary sem gateway, Prometheus do kps e Collector gateway) não foram confirmados. Conferir com helm template antes de fixar URLs na datasource e nos exporters.
- OTel: mode e image.repository são obrigatórios; o NOTES.txt chama fail sem eles. [provável] O NOTES.txt também é renderizado no helm template usado pelo Argo CD, então o sync falharia.
- OTel: rewriteDeprecatedComponentNames: true (padrão) faz os presets gerarem file_log e k8s_attributes. Se a config própria usar filelog ou k8sattributes, haverá componentes duplicados. [INCERTO] O nome otlp_http do exporter na 0.163.2: a doc do Loki ainda cita otlphttp. Manter os nomes que já foram validados localmente.
- OTel: a config é mesclada com a padrão (jaeger, zipkin, prometheus, debug, batch e memory_limiter com limit_percentage 80 e spike_limit_percentage 25). Remover o que não for usado com null e redefinir as listas das pipelines. [INCERTO] Se a config local usar limit_mib, as chaves de porcentagem herdadas continuam lá depois da mescla; definir explicitamente ou anular.
- OTel agente: sem storeCheckpoints, o chart não troca o usuário para root. [INCERTO] O usuário padrão da imagem contrib pode não ter leitura em /var/log/pods no EKS. Se aparecer 'permission denied', usar storeCheckpoints: true (o chart define runAsUser: 0) ou um securityContext explícito.
- OTel: as portas otlp, jaeger e zipkin vêm habilitadas com hostPort. Desligar as que não serão usadas, principalmente no DaemonSet. [INCERTO] Não li o template de portas para saber em quais modos o hostPort é aplicado.
- Capacidade: 2 x m7i-flex.large (4 vCPU e 16 GiB no total) para a aplicação, o Argo CD e a observabilidade. kps, Grafana, Loki e OTel vêm com resources: {}; sem requests, o scheduler não reserva capacidade e o useGOMEMLIMIT do OTel fica inativo.
- [provável] Com os seletores *NilUsesHelmValues em true (padrão), o Prometheus pode ignorar ServiceMonitors e regras criados por outras Applications. Definir false ou usar o label do release.
- Prometheus OTLP: escolher um caminho só para as métricas de spanmetrics (OTLP nativo, remote write ou exporter prometheus com ServiceMonitor), para não duplicar séries. O guia oficial sugere ajustes extras (out_of_order_time_window, promote_resource_attributes). [INCERTO] Não verifiquei a chave do chart para out_of_order_time_window.
- Grafana: persistence.enabled vem false. [provável] Reiniciar o pod perde o SQLite com o estado de alertas e silences. [INCERTO] Isso pode fazer notificações serem reenviadas depois de um restart.
- Segredos dos contact points (PagerDuty, Slack, token do GitHub) e do New Relic: criar os Secrets fora do Git e referenciá-los por envValueFrom/envFromSecret no Grafana e por extraEnvs com secretKeyRef no OTel. [INCERTO] Não verifiquei a sintaxe de interpolação de variáveis de ambiente nos arquivos de provisionamento de alerting do Grafana.
- Grafana: fixar a tag 13.3.0 troca a variante padrão do chart (13.3.0-distroless) pela imagem comum; as duas existem, com push em 2026-10-27. Para imutabilidade, dá para fixar por digest (grafana.image.sha e image.digest no OTel) usando os digests anotados.
- O Docker Hub foi usado só para confirmar a existência das tags. Para o Grafana, o pedido permitia isso; para a contrib, a evidência principal é a appVersion 0.163.2 do chart.

## grafana
- [confirmado] Versão e fontes: `v13.3 (latest); appVersion: 13.3.0` -- Em 2026-11-03 a documentação 'latest' do Grafana corresponde à v13.3, mesma linha da imagem padrão do chart grafana 14.3.1 (appVersion 13.3.0), que é o subchart do kube-prometheus-stack atual. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/)
- [confirmado] Versão e fontes: `- name: grafana | version: "14.3.1" | repository: oci://ghcr.io/grafana-community/helm-charts` -- kube-prometheus-stack 92.17.1 (branch main) depende do chart grafana 14.3.1 publicado no OCI da organização grafana-community; o caminho charts/grafana não existe mais na main de grafana/helm-charts. (https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/Chart.yaml#L62-L65)
- [confirmado] Versão e fontes: `image.registry: docker.io; image.repository: grafana/grafana; image.tag: "{{ .Chart.AppVersion }}-distroless"` -- Imagem padrão do chart grafana 14.3.1: docker.io/grafana/grafana com tag <appVersion>-distroless, ou seja 13.3.0-distroless; o bloco grafana: do kube-prometheus-stack não sobrescreve image, env nem alerting. (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/values.yaml#L119-L125)
- [confirmado] Provisionamento de alerting: regras gerais: `provisioning/alerting; POST http://localhost:3000/api/admin/provisioning/alerting/reload` -- Arquivos YAML ou JSON em provisioning/alerting são aplicados na inicialização ou por recarga pela Admin API; o recurso provisionado fica bloqueado para edição na UI (altera-se o arquivo); importar recurso que já existe gera conflito. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/)
- [confirmado] Esquema: groups/rules: `groups[].{orgId,name,folder,interval,rules[].{uid,title,condition,data[].{refId,relativeTimeRange,datasourceUid,model},dashboardUid,panelId,noDataState,execErrState,for,annotations,labels}}; deleteRules[].{orgId,uid}` -- Regras: apiVersion: 1 e groups[] com orgId (padrão 1), name, folder, interval e rules[]; cada regra tem uid (até 40 caracteres: letras, números, - e _), title, condition (refId que decide o alerta), data[] (refId, datasourceUid, model; rela (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-alert-rules)
- [confirmado] Esquema: groups/rules: `noDataState: NoData|Alerting|OK (default NoData); execErrState: Error|Alerting|OK (default Alerting); datasourceUid: '__expr__'` -- noDataState aceita NoData, Alerting ou OK (padrão NoData); execErrState aceita Error, Alerting ou OK (padrão Alerting). No exemplo da v13.3 as expressões usam datasourceUid '__expr__'; o exemplo comentado no values do chart grafana ainda us (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-alert-rules)
- [confirmado] Esquema: contactPoints: `contactPoints[].{orgId,name,receivers[].{uid,type,disableResolveMessage,settings}}; deleteContactPoints[].{orgId,uid}` -- contactPoints[] tem orgId, name e receivers[]; cada receiver (integração) tem uid, type, disableResolveMessage (bool opcional, padrão false: envia a notificação de resolvido) e settings do tipo. Como receivers é lista, um contact point pode (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-contact-points)
- [confirmado] Esquema: policies: `policies[].{orgId,receiver,group_by,matchers,object_matchers,mute_time_intervals,group_wait,group_interval,repeat_interval,routes[]}; resetPolicies: [1]` -- A árvore de políticas é um recurso único: provisionar policies sobrescreve a árvore inteira (sem afetar políticas internas de regras com contact point direto). Campos: receiver, group_by (['...'] desliga o agrupamento), matchers (estilo Pro (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-notification-policies)
- [confirmado] Esquema: templates: `templates[].{orgId,name,template}; deleteTemplates[].{orgId,name}` -- Templates de notificação: templates[] com orgId, name (nome único do grupo) e template (conteúdo com blocos {{ define "nome" }} ... {{ end }}); exclusão via deleteTemplates. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-notification-template-groups)
- [confirmado] Segredos: interpolação de variáveis: `addresses: $EMAIL (exemplo oficial) → integrationKey: $PAGERDUTY_INTEGRATION_KEY` -- O provisionamento de alerting interpola variáveis de ambiente com a sintaxe $VAR; variável inexistente vira string vazia. O exemplo oficial aplica isso dentro de contactPoints[].receivers[].settings. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#template-variable-interpolation)
- [confirmado] Segredos: interpolação de variáveis: `rules[].annotations | rules[].relativeTimeRange | rules[].data.model | muteTimes[].name | muteTimes[].time_intervals[] | templates[].name | templates[].template` -- Não são interpolados: groups[].rules[].annotations, groups[].rules[].relativeTimeRange, groups[].rules[].data.model, muteTimes[].name, muteTimes[].time_intervals[], templates[].name e templates[].template. O restante (settings de contact po (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#template-variable-interpolation)
- [confirmado] Segredos: interpolação de variáveis: `{{ $$labels }}` -- Onde há interpolação, o '$' de template precisa ser escrito '$$': em settings de contact point, {{ $labels }} vira {{ }}, enquanto {{ $$labels }} preserva {{ $labels }}. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#template-variable-interpolation)
- [confirmado] Segredos: interpolação de variáveis: `$ENV_VAR_NAME | ${ENV_VAR_NAME} | 'Pa$$sw0rd' → Pa$sw0rd` -- Regras gerais do provisionamento: aceita $ENV_VAR_NAME ou ${ENV_VAR_NAME}; usar só em valores (não em chaves/estrutura); não vale dentro dos arquivos JSON de dashboard; ${VAR} é resolvido antes de $VAR, então segredo contendo '$' pode sofre (https://grafana.com/docs/grafana/latest/administration/provisioning/#use-environment-variables)
- [provavel] Segredos: $__env/$__file: `interpolateValue: setting.ExpandVar(v) → os.ExpandEnv(v); split em "$$"` -- No código da v13.3.0, cada valor de provisionamento passa por setting.ExpandVar (os expansores do arquivo de configuração, como $__env{VAR} e $__file{caminho}) e depois por os.ExpandEnv. Logo $__file{/etc/secrets/token} tende a funcionar, m (https://github.com/grafana/grafana/blob/v13.3.0/pkg/services/provisioning/values/values.go#L312-L327)
- [confirmado] PagerDuty: campos: `type: pagerduty; settings: integrationKey, severity, class, component, group, summary` -- Settings documentadas do tipo pagerduty: integrationKey (chave de 32 caracteres da Events API, obrigatória), severity (critical, error, warning, info), class, component, group e summary. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#pagerduty)
- [confirmado] PagerDuty: campos: `integrationKey, severity, details, class, component, group, summary, source, client, client_url, url` -- O código da integração (v1) também aceita source, client, client_url, details (mapa) e url. Padrões: severity critical, class default, group default, component Grafana, client Grafana, client_url {{ .ExternalURL }}, url https://events.pager (https://github.com/grafana/alerting/blob/main/receivers/pagerduty/v1/config.go#L18-L107)
- [confirmado] PagerDuty: resolve: `event_action: "resolve"; dedup_key: key.Hash(); SendResolved() = !GetDisableResolveMessage()` -- Sim, o resolve é automático: quando a notificação do grupo fica resolved, o Grafana envia event_action resolve com o mesmo dedup_key (hash da chave do grupo) usado no trigger; só deixa de enviar se o receiver tiver disableResolveMessage: tr (https://github.com/grafana/alerting/blob/main/receivers/pagerduty/v1/pagerduty.go#L118-L149)
- [provavel] PagerDuty: resolve: `Status: firing | resolved` -- O Status da notificação é firing se ao menos um alerta do grupo dispara, senão resolved. Somado ao dedup_key por grupo, o incidente só resolve quando todo o grupo resolve, e o group_by define a granularidade do incidente. (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/reference/)
- [confirmado] Slack: campos: `type: slack; settings: url, recipient, token, username, icon_emoji, icon_url, mentionUsers, mentionGroups, mentionChannel, endpointUrl, color, title, text` -- Settings do tipo slack: url (Incoming Webhook, começa com https://hooks.slack.com/services/; dispensa token), recipient, token, username, icon_emoji, icon_url, mentionUsers, mentionGroups, mentionChannel (here ou channel), endpointUrl (padr (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-slack/#optional-settings)
- [confirmado] Slack: validação: `erro só se Recipient == "" && URL == APIURL (idem Token); url: Secure: true` -- recipient e token só são exigidos na Chat API (url vazio cai no endpointUrl); com url de Incoming Webhook nenhum dos dois é necessário. url e token são campos Secure; username padrão Grafana. (https://github.com/grafana/alerting/blob/main/receivers/slack/v1/config.go#L44-L68)
- [confirmado] Slack: templates: `title: {{ template "slack.default.title" . }}; text: {{ template "slack.default.text" . }}` -- Os textos padrão do Slack vêm dos templates slack.default.title (title) e slack.default.text (text); color aceita template condicional por .Status. (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-slack/#optional-settings)
- [confirmado] Templates de notificação: dados: `.Receiver .Status .Alerts .GroupLabels .CommonLabels .CommonAnnotations .ExternalURL .GroupKey .TruncatedAlerts | .Labels .Annotations .GeneratorURL .DashboardURL .PanelURL .SilenceURL .Values .ValueString` -- No template de notificação, '.' traz Receiver, Status, Alerts (com .Alerts.Firing e .Alerts.Resolved), GroupLabels, CommonLabels, CommonAnnotations, ExternalURL, GroupKey e TruncatedAlerts. Cada alerta tem Status, Labels, Annotations, Start (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/reference/#alert)
- [confirmado] Templates de notificação: links: `dashboardUid + panelId → .DashboardURL / .PanelURL; .SilenceURL` -- DashboardURL e PanelURL só existem quando a regra está ligada a dashboard/painel (dashboardUid e panelId no provisionamento), com janela de 1h antes do início até o fim do alerta; SilenceURL abre a criação de silêncio. (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/reference/#alert)
- [confirmado] Templates de anotação: `{{ $labels.instance }} | {{ $values.A.Value }} | {{ index $values "B" }} | humanizePercentage` -- Em annotations/labels da regra: $labels (só labels da consulta, sem labels configuradas ou reservadas; vazio com classic condition), $values por RefID ($values.A.Value, $values.A.Labels) e $value (string; a doc recomenda $values). Com consu (https://grafana.com/docs/grafana/latest/alerting/alerting-rules/templates/reference/#values)
- [confirmado] Webhook: campos: `url, httpMethod, maxAlerts, authorization_scheme, authorization_credentials, username, password, title, message, tlsConfig, hmacConfig, headers, payload.template, payload.vars` -- Settings do tipo webhook: url (obrigatório), httpMethod (POST ou PUT, padrão POST), username, password, authorization_scheme, authorization_credentials, maxAlerts, title, message, tlsConfig, hmacConfig, headers (mapa, novo na 12.0) e payloa (https://github.com/grafana/alerting/blob/main/receivers/webhook/v1/config.go#L56-L69)
- [confirmado] Webhook: payload customizado: `Payload Template / Payload Variables → .Vars.<variable_name>; {{ coll.Dict ... | data.ToJSON }}` -- Custom Payload troca todo o corpo JSON por um template de notificação e ignora title/message; payload.vars fica acessível como .Vars.<nome>; há funções para montar JSON: coll.Dict, coll.Slice, coll.Append, data.ToJSON e data.JSON (o exemplo (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/#custom-payload)
- [confirmado] Webhook: cabeçalhos: `restrictedHeaders inclui Authorization, User-Agent, Host, Content-Length, Cookie; erro "custom headers %q are not allowed"` -- headers aceita cabeçalhos extras (por exemplo Accept e X-GitHub-Api-Version) e pode trocar o Content-Type padrão application/json; Authorization, User-Agent, Host, Content-Length, Cookie e outros são restritos e geram erro. O Authorization  (https://github.com/grafana/alerting/blob/main/receivers/webhook/v1/config.go#L95-L176)
- [confirmado] Webhook: segurança: `authorization_credentials: Secure: true; url e headers: sem Secure` -- url do webhook não é campo seguro: fica em texto puro e aparece ao ler o contact point; username, password e authorization_credentials passam por decryptFn (campos seguros); headers não é marcado Secure no schema. (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/#optional-settings)
- [confirmado] GitHub: repository dispatch: `POST https://api.github.com/repos/OWNER/REPO/dispatches; {"event_type": "...", "client_payload": {...}}; 204` -- POST /repos/{owner}/{repo}/dispatches com corpo event_type (obrigatório, até 100 caracteres) e client_payload (objeto, até 10 propriedades de topo, menos de 64KB); sucesso = 204 No Content; header accept recomendado application/vnd.github+j (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] GitHub: cabeçalhos: `X-GitHub-Api-Version: 2026-03-10` -- A documentação REST atual indica como cabeçalhos padrão Authorization: Bearer <token>, Accept: application/vnd.github+json e X-GitHub-Api-Version: 2026-03-10. (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [confirmado] GitHub: workflow: `on: repository_dispatch: types: [flag-service-5xx]; github.event.client_payload.<campo>` -- repository_dispatch só dispara workflow cujo arquivo esteja no branch padrão; GITHUB_SHA é o último commit e GITHUB_REF é o branch padrão; filtra-se com on.repository_dispatch.types e os dados chegam em github.event.client_payload. (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
- [incerto] GitHub: token: `[INCERTO] Contents: write (fine-grained); escopo repo para PAT clássico (confirmado)` -- A permissão exata de token fine-grained para criar o dispatch não apareceu no conteúdo obtido; costuma ser Contents com escrita, mas não foi confirmado aqui. (https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [provavel] Webhook para GitHub: mapeamento: `type: webhook; settings.{url, httpMethod, authorization_scheme, authorization_credentials, headers, payload.template, payload.vars}` -- Combinando as fontes: url = https://api.github.com/repos/OWNER/REPO/dispatches, httpMethod POST, authorization_scheme Bearer, authorization_credentials = $GITHUB_DISPATCH_TOKEN, headers com Accept e X-GitHub-Api-Version e payload.template g (https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/)
- [confirmado] Sidecar de alerting (chart grafana): `sidecar.alerts.{enabled: false, label: grafana_alert, labelValue: "", searchNamespace: null, watchMethod: WATCH, resource: both, reloadURL: "http://localhost:3000/api/admin/provisioning/alerting/reload", skipReload: false, initAlerts: false}` -- sidecar.alerts no chart grafana 14.3.1: enabled false (padrão), label grafana_alert, labelValue "", searchNamespace null (só o namespace do pod; aceita lista ou ALL), watchMethod WATCH, resource both (ConfigMap e Secret), resourceName, relo (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/values.yaml#L1146-L1241)
- [confirmado] Sidecar de alerting (chart grafana): `FOLDER=/etc/grafana/provisioning/alerting; REQ_URL={{ .Values.sidecar.alerts.reloadURL }}; REQ_METHOD=POST` -- O sidecar grava cada chave dos ConfigMaps/Secrets rotulados como arquivo em /etc/grafana/provisioning/alerting e faz POST no reloadURL com usuário/senha admin do Secret do chart (REQ_USERNAME/REQ_PASSWORD), injetados só se GF_SECURITY_ADMIN (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/templates/_pod.tpl#L700-L760)
- [confirmado] Sidecar de alerting (kube-prometheus-stack): `grafana.sidecar.alerts.enabled: true` -- O values do kube-prometheus-stack não configura grafana.sidecar.alerts (só dashboards e datasources); vale o padrão desligado do subchart e é preciso definir grafana.sidecar.alerts.enabled: true. (https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml#L1570-L1660)
- [confirmado] Sidecar de alerting (README): `metadata.labels.grafana_alert: "1"; data.<arquivo>.yml com apiVersion: 1` -- O README do chart diz que o sidecar provisiona regras, contact points, políticas, templates e mute timings, em JSON ou YAML, a partir de ConfigMaps com label grafana_alert (exemplo com valor "1"); apagar uma regra exige remover o ConfigMap  (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/README.md#sidecar-for-alerting-resources)
- [confirmado] Alternativa: valor alerting: do chart: `alerting.contactpoints.yaml.secret.{apiVersion: 1, contactPoints: [...]}; summary: {{ `{{ include "default.message" . }}` }}` -- Sem sidecar, o valor alerting: do chart grafana aceita arquivos inline (rules.yaml, contactpoints.yaml, policies.yaml, templates.yaml, mutetimes.yaml); a subchave secret: faz o arquivo virar Secret; templates Go precisam de escape para o He (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/values.yaml#L834-L922)
- [confirmado] Segredos: injeção no container: `envValueFrom: {VAR: {secretKeyRef: {name, key}}}; envFromSecret: "nome"; extraSecretMounts: [{name, mountPath, secretName}]` -- A interpolação roda no processo do Grafana, então a env precisa estar no container grafana (não no sidecar). O chart oferece envFromSecret (Secret inteiro), envFromSecrets (lista), envValueFrom (secretKeyRef por variável), envRenderSecret ( (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/values.yaml#L685-L737)
- [confirmado] Dashboards: sidecar: `grafana.sidecar.dashboards.{enabled: true, label: grafana_dashboard, labelValue: "1", searchNamespace: ALL}` -- No kube-prometheus-stack o sidecar de dashboards vem ligado com label grafana_dashboard, labelValue "1" e searchNamespace ALL; pastas por anotação exigem folderAnnotation (ex.: grafana_folder) e provider.foldersFromFilesStructure: true (com (https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml#L1571-L1603)
- [confirmado] Dashboards: formato do JSON: `{"kind": "Dashboard", "apiVersion": "dashboard.grafana.app/v1", "metadata": {"name": "<uid>"}, "spec": {...}}` -- O arquivo pode ser o JSON do dashboard (a v13.3 mostra também o envelope com dashboard, folderUid e overwrite) ou o formato Kubernetes (kind: Dashboard, apiVersion: dashboard.grafana.app/v1, metadata.name, spec); dashboards v2 exigem o form (https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards)
- [confirmado] Dashboards: uid do datasource: `"datasource": {"type": "prometheus", "uid": "prometheus"}; grafana.sidecar.datasources.uid: prometheus` -- Para fixar o uid: o datasource provisionado aceita uid próprio (o kube-prometheus-stack cria o Prometheus com uid prometheus; extras via grafana.additionalDataSources[].uid) e o JSON do dashboard referencia datasources como objeto {type, ui (https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/view-dashboard-json-model/)
- [confirmado] Datasources: Alertmanager: `grafana.sidecar.datasources.alertmanager.enabled: true (padrão) → definir false` -- O kube-prometheus-stack cria por padrão um datasource Alertmanager (uid alertmanager) apontando para o Service <fullname>-alertmanager; o template testa só grafana.sidecar.datasources.alertmanager.enabled (true por padrão), não alertmanager (https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/templates/grafana/configmaps-datasources.yaml#L79-L92)
- [provavel] Sidecar: labelValue vazio: `{{- with .Values.sidecar.alerts.labelValue }} → - name: LABEL_VALUE` -- Com labelValue "" o chart não define a env LABEL_VALUE no sidecar; o esperado é casar qualquer valor da label grafana_alert, mas a semântica do k8s-sidecar não foi verificada aqui; definir labelValue "1" elimina a dúvida. (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/templates/_pod.tpl#L700-L710)

### trechos de configuracao
#### Values do kube-prometheus-stack (subchart grafana 14.3.1): liga o sidecar de alerting, fixa os uids de datasource, desliga o datasource Alertmanager e leva os segredos como env do container grafana a partir de um Secret criado fora do Git. Chaves conferidas nos values dos dois charts; nome e porta do Service do Loki são placeholder [INCERTO]. (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/values.yaml#L1146-L1241)
```yaml
alertmanager:
  enabled: false
grafana:
  sidecar:
    alerts:
      enabled: true
      label: grafana_alert
      labelValue: "1"
      searchNamespace: null
      resource: both
    datasources:
      uid: prometheus
      alertmanager:
        enabled: false
  additionalDataSources:
    - name: Loki
      type: loki
      uid: loki
      access: proxy
      url: http://LOKI_SERVICE.observability.svc:3100
  envValueFrom:
    PAGERDUTY_INTEGRATION_KEY:
      secretKeyRef:
        name: grafana-alerting-secrets
        key: pagerduty-integration-key
    SLACK_WEBHOOK_URL:
      secretKeyRef:
        name: grafana-alerting-secrets
        key: slack-webhook-url
    GITHUB_DISPATCH_TOKEN:
      secretKeyRef:
        name: grafana-alerting-secrets
        key: github-dispatch-token
```
#### ConfigMap lido pelo sidecar (label grafana_alert) com o grupo de templates: título comum, texto do Slack com links (.GeneratorURL, .DashboardURL, .PanelURL, .SilenceURL) e .ValueString, e o corpo do repository_dispatch montado com coll.Dict + data.ToJSON. templates[].template é isento de interpolação, então '$' não seria problema aqui. Estrutura conforme a seção oficial, conteúdo adaptado ao projeto. [provavel] .Vars chega ao template nomeado quando chamado com '.'. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-notification-template-groups)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-alerting-templates
  namespace: observability
  labels:
    grafana_alert: "1"
data:
  templates.yaml: |-
    apiVersion: 1
    templates:
      - orgId: 1
        name: togglemaster
        template: |
          {{ define "togglemaster.title" -}}
          [{{ .Status }}] {{ .CommonLabels.alertname }} - {{ .CommonLabels.service }}
          {{- end }}
          {{ define "togglemaster.slack.text" -}}
          {{ range .Alerts -}}
          *Resumo:* {{ .Annotations.summary }}
          *Valores:* {{ .ValueString }}
          *Regra:* {{ .GeneratorURL }}
          {{ if .DashboardURL }}*Dashboard:* {{ .DashboardURL }}{{ end }}
          {{ if .PanelURL }}*Painel:* {{ .PanelURL }}{{ end }}
          *Silenciar:* {{ .SilenceURL }}
          {{ end -}}
          {{- end }}
          {{ define "github.dispatch.payload" -}}
          {{ coll.Dict
            "event_type" "flag-service-5xx"
            "client_payload" (coll.Dict
              "status" .Status
              "alertname" .CommonLabels.alertname
              "deployment" .Vars.deployment
              "namespace" .Vars.namespace
              "group_key" .GroupKey)
            | data.ToJSON }}
          {{- end }}
```
#### Três contact points (PagerDuty Events API v2, Slack Incoming Webhook e webhook para o repository_dispatch do GitHub) com segredos por $VAR. Campos conferidos na doc e no código do grafana/alerting; os textos chamam templates nomeados para não ter '$' nos settings, que são interpolados. O webhook não manda resolvido (evita segundo restart). OWNER, REPO e NAMESPACE_DO_APP são placeholders. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#settings)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-alerting-contactpoints
  namespace: observability
  labels:
    grafana_alert: "1"
data:
  contactpoints.yaml: |-
    apiVersion: 1
    contactPoints:
      - orgId: 1
        name: pagerduty-togglemaster
        receivers:
          - uid: pagerduty-togglemaster
            type: pagerduty
            disableResolveMessage: false
            settings:
              integrationKey: $PAGERDUTY_INTEGRATION_KEY
              severity: critical
              class: http-5xx
              component: flag-service
              group: togglemaster
              source: togglemaster-eks
              summary: '{{ template "togglemaster.title" . }}'
      - orgId: 1
        name: slack-togglemaster
        receivers:
          - uid: slack-togglemaster
            type: slack
            settings:
              url: $SLACK_WEBHOOK_URL
              title: '{{ template "togglemaster.title" . }}'
              text: '{{ template "togglemaster.slack.text" . }}'
              color: '{{ if eq .Status "firing" }}#D63232{{ else }}#36a64f{{ end }}'
      - orgId: 1
        name: github-selfheal
        receivers:
          - uid: github-selfheal
            type: webhook
            disableResolveMessage: true
            settings:
              url: https://api.github.com/repos/OWNER/REPO/dispatches
              httpMethod: POST
              authorization_scheme: Bearer
              authorization_credentials: $GITHUB_DISPATCH_TOKEN
              headers:
                Accept: application/vnd.github+json
                X-GitHub-Api-Version: "2026-03-10"
              payload:
                template: '{{ template "github.dispatch.payload" . }}'
                vars:
                  deployment: flag-service
                  namespace: NAMESPACE_DO_APP
```
#### Árvore de políticas completa (substitui a existente): padrão no Slack; alertas critical vão ao PagerDuty e ao Slack com continue: true; só a regra FlagService5xxAlto com selfheal=true aciona o webhook do GitHub, com repeat_interval próprio. Campos da seção oficial; valores adaptados. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-notification-policies)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-alerting-policies
  namespace: observability
  labels:
    grafana_alert: "1"
data:
  policies.yaml: |-
    apiVersion: 1
    policies:
      - orgId: 1
        receiver: slack-togglemaster
        group_by: ['grafana_folder', 'alertname']
        group_wait: 30s
        group_interval: 5m
        repeat_interval: 4h
        routes:
          - receiver: pagerduty-togglemaster
            object_matchers:
              - ['severity', '=', 'critical']
            continue: true
          - receiver: slack-togglemaster
            object_matchers:
              - ['severity', '=', 'critical']
            continue: true
          - receiver: github-selfheal
            object_matchers:
              - ['alertname', '=', 'FlagService5xxAlto']
              - ['selfheal', '=', 'true']
            group_wait: 0s
            repeat_interval: 1h
```
#### Regra de taxa de 5xx do flag-service: A = PromQL instantânea no datasource uid prometheus; C = threshold > 5% sobre A (sem reduce, porque a consulta é instantânea). Esquema da seção oficial; o model de A e C segue o formato de exportação e deve ser validado exportando a regra pela UI. noDataState OK e execErrState Error evitam restart por falha de dados. [INCERTO] nome da métrica e das labels dependem do conector spanmetrics do Collector. (https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/#import-alert-rules)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-alerting-rules
  namespace: observability
  labels:
    grafana_alert: "1"
data:
  rules.yaml: |-
    apiVersion: 1
    groups:
      - orgId: 1
        name: togglemaster-flag-service
        folder: ToggleMaster
        interval: 1m
        rules:
          - uid: flag-service-5xx
            title: FlagService5xxAlto
            condition: C
            data:
              - refId: A
                relativeTimeRange:
                  from: 600
                  to: 0
                datasourceUid: prometheus
                model:
                  refId: A
                  instant: true
                  range: false
                  intervalMs: 1000
                  maxDataPoints: 43200
                  expr: |-
                    (sum(rate(traces_span_metrics_calls_total{service_name="flag-service", http_response_status_code=~"5.."}[5m])) or vector(0))
                    /
                    sum(rate(traces_span_metrics_calls_total{service_name="flag-service"}[5m]))
              - refId: C
                datasourceUid: __expr__
                model:
                  refId: C
                  type: threshold
                  expression: A
                  datasource:
                    type: __expr__
                    uid: __expr__
                  conditions:
                    - evaluator:
                        type: gt
                        params:
                          - 0.05
            dashboardUid: togglemaster-overview
            panelId: 1
            noDataState: OK
            execErrState: Error
            for: 2m
            labels:
              severity: critical
              service: flag-service
              selfheal: "true"
            annotations:
              summary: 'flag-service com {{ humanizePercentage $values.A.Value }} de respostas 5xx (limite 5%)'
```
#### Dashboard pelo sidecar (label grafana_dashboard: "1", que o kube-prometheus-stack observa em todos os namespaces) no modelo Classic, com uid fixo (o mesmo dashboardUid da regra) e datasources referenciados por {type, uid}. As expressões são placeholders; exportar pela UI escolhendo o modelo Classic dá o JSON completo. (https://github.com/grafana-community/helm-charts/blob/grafana-14.3.1/charts/grafana/README.md#sidecar-for-dashboards)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: togglemaster-dashboard
  namespace: observability
  labels:
    grafana_dashboard: "1"
data:
  togglemaster-overview.json: |-
    {
      "id": null,
      "uid": "togglemaster-overview",
      "title": "ToggleMaster - Visao geral",
      "tags": ["togglemaster"],
      "timezone": "browser",
      "schemaVersion": 42,
      "version": 1,
      "refresh": "30s",
      "time": {"from": "now-1h", "to": "now"},
      "panels": [
        {
          "id": 1,
          "type": "timeseries",
          "title": "flag-service - taxa de 5xx",
          "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
          "datasource": {"type": "prometheus", "uid": "prometheus"},
          "targets": [
            {"refId": "A", "datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": "PROMQL_TAXA_5XX"}
          ]
        },
        {
          "id": 2,
          "type": "logs",
          "title": "flag-service - logs",
          "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
          "datasource": {"type": "loki", "uid": "loki"},
          "targets": [
            {"refId": "A", "datasource": {"type": "loki", "uid": "loki"}, "expr": "LOGQL_FLAG_SERVICE"}
          ]
        }
      ]
    }
```
#### Workflow de self-healing acionado por repository_dispatch; o arquivo precisa estar no branch padrão. Gatilho e client_payload conforme a doc do GitHub; os passos AWS/kubectl são esboço com placeholders (versão da action, ARN da role OIDC, cluster e namespace) e alvo fixo, para não interpolar o payload em run:. (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)
```yaml
name: self-healing-flag-service
on:
  repository_dispatch:
    types: [flag-service-5xx]
concurrency:
  group: self-healing-flag-service
  cancel-in-progress: false
permissions:
  contents: read
  id-token: write
jobs:
  restart:
    if: github.event.client_payload.status == 'firing'
    runs-on: ubuntu-latest
    steps:
      - name: Credenciais AWS por OIDC
        uses: aws-actions/configure-aws-credentials@VERSAO_FIXADA
        with:
          role-to-assume: ARN_DO_PAPEL_OIDC
          aws-region: us-east-2
      - name: Kubeconfig do EKS
        run: aws eks update-kubeconfig --region us-east-2 --name NOME_DO_CLUSTER
      - name: Rollout restart com alvo fixo
        run: |
          kubectl -n NAMESPACE_DO_APP rollout restart deployment/flag-service
          kubectl -n NAMESPACE_DO_APP rollout status deployment/flag-service --timeout=180s
```

### riscos
- [BLOQUEIO] repository_dispatch só executa workflow que já esteja no branch padrão (main). Pelo CLAUDE.md, merge na main não está autorizado nesta retomada; sem essa autorização o fluxo Grafana → GitHub → rollout restart não pode ser demonstrado de ponta a ponta.
- Restart duplo: por padrão o webhook também recebe a notificação de resolvido (disableResolveMessage: false). No receiver do GitHub usar disableResolveMessage: true e, no workflow, rodar só quando client_payload.status == 'firing'.
- Restarts repetidos: enquanto o alerta continuar firing, o Grafana reenvia a cada repeat_interval (padrão 4h) e a cada group_interval quando entra alerta novo no grupo. Usar concurrency no workflow e escolher de propósito o repeat_interval da rota do GitHub.
- Falso positivo por erro ou falta de dados: os padrões são noDataState NoData e execErrState Alerting; com Alerting, uma falha do Prometheus vira alerta e pode disparar restart. Usar noDataState: OK (com 'or vector(0)' no numerador), execErrState: Error e casar a rota do GitHub pelo alertname da regra. [INCERTO, não verificado aqui] alertas DatasourceError/DatasourceNoData podem herdar as labels da regra (inclusive selfheal).
- Interpolação de '$' em settings de contact point (title, text, summary, payload.template): {{ $labels }} vira {{ }} sem erro visível. Escapar com $$ ou deixar o texto em templates: (isento) e chamar com {{ template "nome" . }}.
- Env ausente vira string vazia: se o Secret ou a chave não chegar ao container grafana, integrationKey, url ou credenciais ficam vazios; o código do PagerDuty recusa chave vazia. [INCERTO] se um erro de provisionamento impede o Grafana de subir ou afeta só aquele recurso.
- Segredo contendo '$' com a sintaxe ${VAR} sofre dupla expansão; preferir $VAR.
- Segredos fora do Git: o Secret (ex.: grafana-alerting-secrets) precisa ser criado fora do repositório (kubectl manual com autorização, Sealed Secrets ou External Secrets); envRenderSecret colocaria o valor nos values versionados. Regra do projeto: nenhuma chave em arquivo versionado, LOG ou chat.
- Campos não seguros: url e headers do webhook ficam em texto puro e aparecem em leitura/exportação; nunca colocar o token na URL ou em headers. Authorization em headers é rejeitado por ser cabeçalho restrito.
- Datasource Alertmanager quebrado: com alertmanager.enabled: false o kube-prometheus-stack ainda cria o datasource Alertmanager; definir grafana.sidecar.datasources.alertmanager.enabled: false.
- Política única: só um arquivo deve conter policies (ele substitui a árvore inteira) e todo receiver citado precisa existir como contact point. [INCERTO] o sidecar pode gravar os ConfigMaps em momentos diferentes e gerar uma recarga com política apontando para contact point ainda ausente; juntar contact points, templates e policies num só ConfigMap reduz o risco.
- Ciclo de vida: recursos provisionados ficam somente leitura na UI; apagar o ConfigMap não remove nada no Grafana. Usar deleteRules, deleteContactPoints, deleteTemplates ou resetPolicies.
- Sidecar: vem desligado; searchNamespace null restringe ao namespace observability; a recarga usa as credenciais admin do Secret do chart. Se a senha admin vier por GF_SECURITY_ADMIN_PASSWORD em env, REQ_PASSWORD não é injetado e a recarga falha.
- O exemplo oficial do Slack escreve color: {{ if ... }} sem aspas; em YAML um valor que começa com '{' é lido como mapa de fluxo. Usar aspas.
- Token do GitHub: PAT clássico exige o escopo repo (amplo); a permissão fine-grained exata está [INCERTO]; token expirado quebra o self-healing em silêncio (só aparece nos logs do Grafana). Validar antes com um POST de teste esperando 204.
- X-GitHub-Api-Version: a doc atual cita 2026-03-10; [INCERTO] se 2022-11-28 continua aceita. Fixar a versão e testar.
- Limites do GitHub: event_type até 100 caracteres; client_payload até 10 propriedades de topo e menos de 64KB. Não mandar .Alerts inteiro.
- headers e payload foram lidos no código da branch main do grafana/alerting (marcados como novos na 12.0), não na versão exata embutida no Grafana 13.3.0. Validar exportando o contact point no Grafana do cluster antes de versionar.
- Imagem 13.3.0-distroless: sem shell no container grafana para kubectl exec; depurar por logs e API.
- O chart grafana migrou para grafana-community (OCI no ghcr.io); comentários e links do kube-prometheus-stack ainda apontam para grafana/helm-charts. Fixar 14.3.1 e consultar o README da nova organização.
- PagerDuty: o dedup_key é por grupo, então o incidente só resolve quando o grupo todo resolve. O trial vai até 2026-11-11 (contexto do projeto): coletar a evidência antes.
- Métrica do alerta: traces_span_metrics_calls_total e a label http_response_status_code são suposições [INCERTO]; dependem do conector spanmetrics (namespace, dimensions) e de como o Prometheus recebe as métricas do Collector.
- Dashboards: env não funciona dentro do JSON; mudar grafana.sidecar.datasources.uid quebra painéis e regras (datasourceUid: prometheus). [INCERTO, não verificado aqui] ConfigMap grande pode estourar o limite da anotação last-applied do ArgoCD com client-side apply; considerar ServerSideApply.
- Se os arquivos de alerting forem para os values do Helm (grafana.alerting) em vez de ConfigMaps do Kustomize, as chaves {{ }} precisam de escape ({{ `{{ ... }}` }}), como no exemplo do chart.
- Workflow: não interpolar client_payload direto em run: (risco de injeção de comando); manter alvo fixo. A role OIDC do workflow precisa de acesso ao EKS (access entry/RBAC), fora desta pesquisa.

