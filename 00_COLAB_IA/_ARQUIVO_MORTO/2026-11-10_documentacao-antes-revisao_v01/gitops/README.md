# GitOps do ToggleMaster — Fase 4

TL;DR: manifests dos cinco serviços (`base/`, `overlays/prod/`) e stack de observabilidade (`observability/`), sincronizados pelo ArgoCD a partir da `main`. O overlay `prod` nasce com marcadores explícitos: o primeiro deploy os troca pelos outputs do Terraform (endpoints e IRSA), e o CI grava as tags das imagens. Não sincronizar antes disso.

Última atualização: 2026-11-09. Fonte: manifests em `base/`, `overlays/prod/`, `observability/` e `terraform/k8s/argocd.tf`.

## Estrutura e destino

```text
gitops/
├── base/                         # deployments, services, configmaps, HPAs e PostgreSQL
├── overlays/prod/
│   ├── kustomization.yaml        # cinco imagens; as tags são gravadas pelo CI
│   └── patches/
│       ├── irsa.yaml             # roles IRSA, preenchidas no primeiro deploy
│       └── endpoints.yaml        # SQS e Redis, preenchidos no primeiro deploy
└── SECRETS-CONTRATO.md            # nomes e chaves esperados, sem segredos
```

O Terraform em `terraform/k8s` declara a Application para `https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04.git`, caminho `gitops/overlays/prod`, branch `main`. Como o repositório é público, o ArgoCD lê sem credencial; a credencial `repo-tech-challenge-04` só é criada se `TF_VAR_github_token` for informado. As mudanças feitas na `dev` chegam ao ArgoCD depois do merge na `main`.

Os Secrets continuam declarados em `terraform/k8s/secrets.tf`; não existem valores secretos neste diretório. Os Services são ClusterIP e não há Ingress; o acesso é por `kubectl port-forward`. A observabilidade fica em `observability/`, com Application própria (`terraform/k8s/observability.tf`).

## Conta nova: o que preencher

| Valor | Local | Fonte real futura |
|---|---|---|
| `newName` das cinco imagens | `overlays/prod/kustomization.yaml` | `ecr_repository_urls` da base da Fase 4 |
| `newTag` das cinco imagens | mesmo arquivo | imagens efetivamente publicadas pelo CI do repositório 04 |
| `AWS_SQS_URL`, em dois ConfigMaps | `patches/endpoints.yaml` | `terraform -chdir=terraform output -raw sqs_queue_url` |
| `REDIS_URL` | mesmo patch | `terraform -chdir=terraform/cluster output -raw redis_url` |
| `eks.amazonaws.com/role-arn`, duas ServiceAccounts | `patches/irsa.yaml` | `terraform -chdir=terraform/cluster output -json irsa_role_arns` |

As imagens/endpoints usam `*.conta-pendente.invalid`, a tag é `conta-pendente` e os ARNs contêm `CONTA_AWS_PENDENTE`. São marcadores intencionais, sem identidade operacional; impedem reutilizar recursos da conta anterior. Renderizar os YAMLs não valida esses valores de runtime.

Antes de sincronizar, substituir **todos** esses marcadores por outputs confirmados e validar conta, região e namespace. Não basta trocar as tags: roles, fila e Redis também dependem da conta/cluster. Se o Redis usar TLS, preservar o esquema `rediss://` emitido pelo output. Os estados Terraform da Fase 3 não entram nessa preparação; consultar [terraform/README.md](../terraform/README.md).

Depois de publicado, o job GitOps do CI atualiza tags na `main`, e o ArgoCD acompanha essa branch. O circuito de desenvolvimento local na `dev` não exige nem executa sincronização do EKS.

## Conferir localmente

```bash
# Renderiza sem usar kubeconfig nem contactar um cluster.
kubectl kustomize gitops/overlays/prod
```

```bash
# Renderiza as 3 pastas do Kustomize e confere dashboards e alertas do Grafana (precisa de Python com PyYAML)
bash scripts/gitops/validate.sh
```

O segundo comando é o mesmo que o workflow GitOps Check roda em todo push na `dev` e na `main` e em todo PR. O Kustomize só embute os arquivos do Grafana como texto. Por isso o script também abre cada JSON e YAML e cruza as referências: painel citado pela regra de alerta, contact point citado pela policy, `alertname` da rota do self-healing e datasources do values.

Em 2026-10-20, a renderização produziu 23 objetos. O `kubectl` não fornece `kustomize edit`; o pipeline instala a ferramenta Kustomize separada para atualizar imagens. A renderização verifica a composição dos manifests; não comprova existência de imagens, autorização IRSA, conectividade com AWS, disponibilidade de banco ou funcionamento da aplicação.

## Referências

- [Contrato dos Secrets](SECRETS-CONTRATO.md)
- [Configuração das três raízes Terraform](../terraform/README.md)
- [Requisitos da Fase 4](../docs/requisitos/README.md)
- [Arquitetura](../docs/ARQUITETURA.md) e [guia de reprodução](../docs/GUIA_DE_REPRODUCAO.md): vieram da base da Fase 3 e não são confirmação da conta atual.
