# GitOps do ToggleMaster — Fase 4

TL;DR: manifests importados preservam os cinco serviços e passam a ser publicados pelo repositório `tech-challenge-04`. O overlay `prod` contém sentinelas explícitas porque a nova conta AWS ainda não foi fornecida. Não sincronizar esse overlay antes de configurar e revisar os valores reais.

Última atualização: 2026-10-20, Codex. Fonte: manifests em `base/`, `overlays/prod/` e `terraform/k8s/argocd.tf`; somente validação local, sem implantação.

## Estrutura e destino

```text
gitops/
├── base/                         # deployments, services, configmaps, HPAs e PostgreSQL
├── overlays/prod/
│   ├── kustomization.yaml        # cinco imagens da nova conta, ainda pendentes
│   └── patches/
│       ├── irsa.yaml             # roles novas, ainda pendentes
│       └── endpoints.yaml        # SQS e Redis novos, ainda pendentes
└── SECRETS-CONTRATO.md            # nomes e chaves esperados, sem segredos
```

O Terraform em `terraform/k8s` declara a Application para `https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04.git`, caminho `gitops/overlays/prod`, branch `main`. A credencial de repositório se chama `repo-tech-challenge-04`. A `main` é o destino futuro de publicação: o usuário autorizou trabalhar agora somente na `dev`, sem PR/push/main. Logo, estas mudanças locais ainda não estão disponíveis ao ArgoCD remoto.

Os Secrets continuam declarados em `terraform/k8s/secrets.tf`; não existem valores secretos neste diretório. Os Services são ClusterIP e a base ainda não possui Ingress. Não foi acrescentada observabilidade nesta importação.

## Conta nova: o que preencher

| Valor | Local | Fonte real futura |
|---|---|---|
| `newName` das cinco imagens | `overlays/prod/kustomization.yaml` | `ecr_repository_urls` da base da Fase 4 |
| `newTag` das cinco imagens | mesmo arquivo | imagens efetivamente publicadas pelo CI do repositório 04 |
| `AWS_SQS_URL`, em dois ConfigMaps | `patches/endpoints.yaml` | `terraform -chdir=terraform output -raw sqs_queue_url` |
| `REDIS_URL` | mesmo patch | `terraform -chdir=terraform/cluster output -raw redis_url` |
| `eks.amazonaws.com/role-arn`, duas ServiceAccounts | `patches/irsa.yaml` | `terraform -chdir=terraform/cluster output -json irsa_role_arns` |

As imagens/endpoints usam `*.conta-pendente.invalid`, a tag é `conta-pendente` e os ARNs contêm `CONTA_AWS_PENDENTE`. São marcadores intencionais, sem identidade operacional; foram usados para impedir reutilizar recursos da conta anterior enquanto se aguarda a nova. Renderizar os YAMLs não valida esses valores de runtime.

Antes de habilitar implantação, substituir **todos** esses marcadores por outputs confirmados, validar conta/região/namespace e publicar pelo fluxo de revisão autorizado. Não basta trocar as tags: roles, fila e Redis também dependem da conta/cluster. Se o Redis usar TLS, preservar o esquema `rediss://` emitido pelo output. Os estados Terraform da Fase 3 não entram nessa preparação; consultar [terraform/README.md](../terraform/README.md).

Depois de publicado, o job GitOps do CI atualiza tags na `main`, e o ArgoCD acompanha essa branch. O circuito de desenvolvimento local na `dev` não exige nem executa sincronização do EKS.

## Conferir localmente

```bash
# Renderiza sem usar kubeconfig nem contactar um cluster.
kubectl kustomize gitops/overlays/prod
```

Em 2026-10-20, a renderização produziu 23 objetos. O `kubectl` não fornece `kustomize edit`; o pipeline instala a ferramenta Kustomize separada para atualizar imagens. A renderização verifica a composição dos manifests; não comprova existência de imagens, autorização IRSA, conectividade com AWS, disponibilidade de banco ou funcionamento da aplicação.

## Referências

- [Contrato dos Secrets](SECRETS-CONTRATO.md)
- [Configuração das três raízes Terraform](../terraform/README.md)
- [Requisitos da Fase 4](../docs/requisitos/README.md)
- [Pendências e retomada](../00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md)
- [Arquitetura importada](../docs/ARQUITETURA.md) e [guia de reprodução importado](../docs/GUIA_DE_REPRODUCAO.md): contexto histórico da base; não são confirmação da nova conta.
