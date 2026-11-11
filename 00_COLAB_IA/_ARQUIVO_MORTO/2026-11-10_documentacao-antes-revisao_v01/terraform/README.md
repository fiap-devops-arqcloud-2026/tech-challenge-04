# Terraform do ToggleMaster — Fase 4

TL;DR: infraestrutura da base da Fase 3, adaptada ao repositório `fiap-devops-arqcloud-2026/tech-challenge-04` e a uma conta AWS nova. Nenhum estado, credencial ou recurso da conta anterior foi transportado. Os arquivos `.example` mostram o que preencher localmente antes de cada camada.

Última atualização: 2026-11-09. Fonte: arquivos `.tf`, exemplos e lockfiles deste diretório.

## Camadas e estados separados

| Pasta | O que declara | Chave de estado da Fase 4 | Lê de |
|---|---|---|---|
| `terraform/` (base) | VPC, subnets, NAT, 5 ECR, SQS/DLQ, DynamoDB e OIDC/role do GitHub | `phase4/prod/base.tfstate` | nenhum estado anterior |
| `terraform/cluster/` | EKS, 2 RDS, Redis e IRSA | `phase4/prod/cluster.tfstate` | base da Fase 4 |
| `terraform/k8s/` | ArgoCD, Application, Secrets e StorageClass | `phase4/prod/k8s.tfstate` | base e cluster da Fase 4 |

A ordem de dependências é base → publicação das imagens → cluster → k8s. São raízes independentes: cada uma recebe suas próprias variáveis. O estado guarda valores sensíveis e não deve entrar no Git.

As três raízes usam backend S3 parcial: `backend.tf` fixa a chave, criptografia e lock; bucket/região vêm de um arquivo local `backend.hcl`, preparado a partir de `backend.hcl.example`. O arquivo local é ignorado por `terraform/.gitignore`. Os exemplos têm sentinelas explícitas que precisam ser substituídas pelos dados confirmados da nova conta.

**Não copiar `terraform.tfstate`, planos, `.terraform/` ou o bucket/objetos da Fase 3. Não usar `init -migrate-state` para esta importação.** A base da Fase 4 deve começar com estados próprios e vazios, em um bucket novo. Nenhum bootstrap foi executado nesta etapa.

## Parâmetros da conta

| Parâmetro | Camadas | Origem/condição |
|---|---|---|
| `expected_aws_account_id` | três | ID real da nova conta, obrigatório, 12 dígitos; `allowed_account_ids` recusa credenciais de outra conta |
| bucket/região em `backend.hcl` | três | bucket novo da Fase 4; configuração de backend é separada de variáveis Terraform |
| `state_bucket`, `state_region` | cluster e k8s | mesmos bucket/região dos backends, obrigatórios para ler as camadas anteriores |
| `base_state_key` | cluster e k8s | padrão `phase4/prod/base.tfstate`; coincidir com a base |
| `cluster_state_key` | k8s | padrão `phase4/prod/cluster.tfstate`; coincidir com o cluster |
| `aws_region`, AZs, tipos/tamanhos | conforme raiz | padrões herdados como base de código; revalidar cotas, disponibilidade, suporte e custo da nova conta |
| `create_github_oidc_provider` | base | `true` somente se a nova conta ainda não tiver o emissor do GitHub; não assumir o estado da conta anterior |
| imagens, IRSA, SQS e Redis | overlay GitOps | substituir sentinelas somente pelos outputs/imagens da nova conta |

Para preparar a configuração, preencher os `.example` em arquivos locais, definir o perfil AWS correto e conferir a identidade. A inicialização real usará `terraform -chdir=<camada> init -backend-config=backend.hcl -input=false`, **somente após o bucket e a conta terem sido confirmados**. Não executar esse comando enquanto houver sentinelas. A inicialização com `-backend=false` usada abaixo é outra operação: baixa dependências sem acessar S3.

Há `terraform.tfvars.example` por raiz. Os arquivos reais `terraform.tfvars` são ignorados pelo Git. `expected_aws_account_id` também pode ser passado por `TF_VAR_expected_aws_account_id`; nas raízes cluster/k8s, `TF_VAR_state_bucket` e `TF_VAR_state_region`. Os valores de backend não são preenchidos automaticamente por essas variáveis.

## Destino GitHub e ArgoCD

- OIDC: `github_repository` padrão = `fiap-devops-arqcloud-2026/tech-challenge-04`.
- ArgoCD: `gitops_repo_url` padrão = `https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04.git`; Secret `repo-tech-challenge-04`.
- A branch observada é a `main`, de onde o pipeline publica. O trabalho do dia a dia ocorre na `dev`, e as alterações só chegam ao ArgoCD depois do merge.
- `github_token` precisa de leitura do conteúdo do repositório 04 se ele for privado; passar como variável sensível, nunca versionar token. A visibilidade/acesso remoto atual não foi validada nesta importação.
- Tags AWS: `project=fiap`, `phase=4` nas três raízes. Nomes dos serviços e do namespace permanecem consistentes com os manifests e o código importado.

## Validação local, sem acesso à AWS

```bash
terraform fmt -check -recursive terraform
terraform -chdir=terraform init -backend=false -input=false -lockfile=readonly
terraform -chdir=terraform validate
terraform -chdir=terraform/cluster init -backend=false -input=false -lockfile=readonly
terraform -chdir=terraform/cluster validate
terraform -chdir=terraform/k8s init -backend=false -input=false -lockfile=readonly
terraform -chdir=terraform/k8s validate
terraform -chdir=terraform/modules/iam-ci init -backend=false -input=false -lockfile=readonly
terraform -chdir=terraform/modules/iam-ci test
kubectl kustomize gitops/overlays/prod
```

O `terraform test` do módulo `iam-ci` tem 10 casos e também roda no workflow `Terraform Check`. Ele prova que só a branch `main` deste repositório assume as roles do CI e do self-healing via OIDC, que entradas com curinga são recusadas e que cada role recebe só a permissão do seu trabalho. Os casos usam `command = plan` e um provider sem acesso à AWS; o lock do módulo fixa a mesma versão do provider da camada base.

A inicialização baixa módulos/providers do registro, sem conectar ao backend e sem executar `plan`/`apply`. Os lockfiles originais foram preservados: não atualizar providers apenas para importar o projeto. Validação sintática e renderização local não demonstram acesso à conta, pull de imagens, funcionamento do cluster ou implantação.

## Cuidados operacionais e referências

A stack de observabilidade é entregue por GitOps (`gitops/observability`), com a Application e os Secrets criados em `terraform/k8s/observability.tf`. Não assumir elegibilidade Free Tier nem preços pelos comentários históricos do código.

Qualquer destruição exige inventário/plano e autorização explícita separados. Antes de remover cluster/CSI, confirmar a remoção dos PVCs/PVs/EBS do PostgreSQL targeting; remover o bucket de estado por último. O [guia importado](../docs/GUIA_DE_REPRODUCAO.md) e a [arquitetura importada](../docs/ARQUITETURA.md) documentam a base técnica histórica e precisam ser lidos com o estado/pêndencias atuais. Para a nova conta, prevalecem os parâmetros e limites deste README.

- [Contrato dos Secrets](../gitops/SECRETS-CONTRATO.md)
- [GitOps](../gitops/README.md)
- [Requisitos da Fase 4](../docs/requisitos/README.md)
