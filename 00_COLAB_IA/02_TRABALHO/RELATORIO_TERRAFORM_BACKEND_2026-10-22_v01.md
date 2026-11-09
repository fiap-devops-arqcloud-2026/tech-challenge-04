# Terraform e backend da Fase 4 — leitura explicada e estado verificado

TL;DR: o projeto possui o código de infraestrutura importado da Fase 3, organizado em três camadas, mas a nova conta e o bucket do estado ainda não estão configurados. Código, estado, backend e infraestrutura real são coisas diferentes. As três camadas já têm chaves próprias da Fase 4; não devemos transportar o estado da conta anterior. Há validação local registrada, sem comprovação de infraestrutura ativa. Esta análise explica e inventaria; não executa os passos de integração Docker/instrumentação, AWS ou implantação.

Última atualização: 2026-10-22, Codex. Conferência local iniciada às 11:50 (America/Sao_Paulo, UTC-03:00). Escopo: arquivos Terraform, workflows relacionados, documentação vigente e documentação primária HashiCorp. Nenhum segredo foi lido ou incluído.

## 1. Explicação simples: o projeto, a memória e o lugar da memória

Imagine que vamos construir uma casa:

| Elemento | Analogia | Aqui no projeto |
|---|---|---|
| Código `.tf` | Planta e especificações da casa | Declara rede, cluster, bancos, permissões e objetos Kubernetes |
| Valores de entrada | Endereço, tamanho e opções da construção | Região, conta esperada, tamanho dos nós e nomes fornecidos às variáveis |
| Provider | Profissional que conversa com o sistema responsável pela obra | Plugin que usa as APIs AWS, Kubernetes ou Helm |
| State | Cadastro que associa cada item da planta ao objeto efetivamente gerenciado | Snapshot com endereços Terraform, IDs, atributos e outputs |
| Backend | Local e mecanismo para guardar e coordenar esse cadastro | Backend S3, com um objeto de estado para cada camada |
| Plan | Proposta das alterações a realizar | Diferenças entre configuração, estado e leitura dos objetos remotos |
| Apply | Execução das alterações aprovadas | Criar, atualizar ou remover objetos e registrar os resultados no estado |

O estado permite, por exemplo, associar o endereço Terraform `module.eks.aws_eks_cluster.this` a um cluster específico. Ele não contém uma cópia de todos os dados de bancos ou discos e não substitui seus backups. Perder o estado não apaga imediatamente a infraestrutura; perde-se o vínculo que permite gerenciá-la com segurança. Fonte conceitual consultada em 2026-10-22: [finalidade do state](https://developer.hashicorp.com/terraform/language/state/purpose).

**Trazer código da Fase 3 não trouxe a infraestrutura da conta anterior.** A importação preservou as definições e o histórico Git. Para a nova conta, a política vigente é criar backend e estados próprios, sem copiar `.tfstate`, `.terraform/` ou planos antigos. Fonte: [terraform/README.md:19](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:19) e [D-014](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/00_COLAB_IA/DECISOES.md:113), conferidos em 2026-10-22.

## 2. O que existe no computador em 2026-10-22

Inspeção de existência, sem abrir arquivos de credenciais ou snapshots sensíveis:

| Raiz independente | Código `.tf` | `.terraform.lock.hcl` versionado | Pasta `.terraform/` local | `backend.hcl` local | `terraform.tfvars` local | `terraform.tfstate` na raiz | Arquivo literal `tfplan` |
|---|---|---|---|---|---|---|---|
| `terraform/` | Sim | Sim | Sim | Não | Não | Não | Não |
| `terraform/cluster/` | Sim | Sim | Sim | Não | Não | Não | Não |
| `terraform/k8s/` | Sim | Sim | Sim | Não | Não | Não | Não |

Os resultados acima só descrevem esses nomes locais. A presença de `.terraform/` é compatível com a inicialização para validação; não demonstra conexão com um backend. A ausência de um estado na raiz não prova ausência de estado remoto. Não houve inventário AWS, `state pull/list`, inspeção do conteúdo das pastas de cache ou leitura da conta.

Inventário do código próprio, excluindo os downloads de `.terraform/`: **40 arquivos `.tf`, sete diretórios de módulos locais, oito chamadas `module`, 51 blocos `resource` e 13 blocos `data`**. Bloco não equivale a objeto implantado: `for_each`/`count` expandem ou eliminam instâncias, e o módulo externo de VPC possui seus próprios recursos. Esses números não são uma previsão de `plan` nem um inventário de recursos ativos. Fonte: enumeração local e busca de declarações em `terraform/**`, em 2026-10-22.

## 3. Por que há três pastas de execução

São três **root modules**, cada qual com configuração, providers, entradas e estado próprios. São camadas do ambiente chamado `prod`; não são os ambientes dev/homologação/produção. A branch Git `dev` também não cria um ambiente AWS. Não há seleção explícita por `terraform.workspace` no código lido; nenhum workspace real foi consultado.

| Camada/raiz | Responsabilidade declarada | Chave própria de estado S3 | Depende de |
|---|---|---|---|
| Base: `terraform/` | Rede, registros de imagens, mensageria e identidade CI | `phase4/prod/base.tfstate` | Bucket do backend e identidade prontos |
| Cluster: `terraform/cluster/` | EKS, bancos RDS, Redis e identidades de pods | `phase4/prod/cluster.tfstate` | Outputs do estado da base |
| Kubernetes: `terraform/k8s/` | Namespaces, Secrets, StorageClass, ArgoCD e Application | `phase4/prod/k8s.tfstate` | Outputs da base e do cluster; API Kubernetes acessível |

Fontes locais: [base/backend.tf:42](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/backend.tf:42), [cluster/backend.tf:46](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/backend.tf:46), [k8s/backend.tf:54](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/backend.tf:54), [README Terraform:9](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:9).

O texto `phase4/prod/` é um prefixo da chave de um objeto S3, não uma pasta de código ou um isolamento de conta por si só. A vantagem é poder operar camadas em momentos diferentes sem obrigar tudo a compartilhar o mesmo estado. A responsabilidade adicional é coordenar suas dependências e não destruir uma camada de que outra ainda depende.

Ordem operacional registrada: **base → publicar imagens → cluster → k8s**. A publicação é dependência para os pods funcionarem, embora a API do EKS possa ser criada antes das imagens. Fontes: [README Terraform:15](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:15) e [outputs ECR:37](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/outputs.tf:37).

## 4. Como as camadas e os módulos trocam dados

Um módulo local agrupa uma peça reutilizável. Ele declara entradas em `variables.tf`, usa-as nos recursos e publica saídas em `outputs.tf`. A raiz chama o módulo e liga entradas e saídas. A raiz base, por exemplo, passa `module.ecr.repository_arns` a `module.iam_ci.ecr_repository_arns`: a policy do CI recebe os ARNs dos repositórios criados. Fonte: [main.tf:128](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/main.tf:128).

Isso é diferente de ler outro **estado**. Cada execução na raiz cluster usa `data.terraform_remote_state.base`; a raiz k8s lê base e cluster. Esses data sources leem snapshots existentes e disponibilizam os outputs da raiz produtora; não aplicam automaticamente a configuração anterior nem criam um pipeline entre pastas. Se recriarmos uma subnet na base, precisamos aplicar a base e depois planejar/aplicar seus consumidores para propagarem a mudança.

| Origem | Saídas efetivamente usadas na próxima raiz | Onde a leitura ocorre |
|---|---|---|
| Base → cluster | ID da VPC, subnets privadas/públicas, ARN SQS, ARN DynamoDB | [cluster/data.tf:17](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/data.tf:17), atalhos a partir da linha 36 |
| Base → k8s | URL SQS armazenada no atalho local | [k8s/data.tf:16](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/data.tf:16), atalho na linha 51; não foi localizado consumidor desse atalho em outros `.tf` |
| Cluster → k8s | Nome/endpoint/CA do EKS, URLs com senhas dos bancos e URL Redis | [k8s/data.tf:34](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/data.tf:34), atalhos a partir da linha 55 |

**Atenção ao acesso:** embora a interface de `terraform_remote_state` exponha outputs, quem consegue ler o objeto de estado no S3 consegue acessar o snapshot inteiro. Neste projeto, o estado do cluster conterá senhas/URLs dos bancos, e a camada k8s também as utilizará. Marcar um output `sensitive` reduz exibição comum no terminal; não torna o estado sem segredos. Fonte oficial: [remote state e sensibilidade](https://developer.hashicorp.com/terraform/language/state/remote-state-data); evidência local: [cluster/outputs.tf:95](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/outputs.tf:95), [k8s/secrets.tf:105](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/secrets.tf:105).

## 5. Inventário funcional do que o código declara

Nada nesta tabela afirma criação ou funcionamento na AWS em 2026-10-22. Quantidades citadas decorrem dos valores padrão atuais, não de um plano remoto.

| Raiz | Módulo ou arquivo | Recursos e função | Fonte local |
|---|---|---|---|
| Base | `vpc` externo | VPC, duas subnets privadas e duas públicas pelos padrões; DNS; configuração de IGW/rotas/NAT pelo módulo. `single_nat_gateway=true`; `enable_nat_gateway` é variável | [main.tf:45](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/main.tf:45), [variables.tf:66](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/variables.tf:66) |
| Base | `modules/ecr` | Cinco repositórios ECR para auth, flag, targeting, evaluation e analytics; policy de ciclo de vida em cada repositório | [ecr/main.tf:12](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/ecr/main.tf:12), [ecr/main.tf:58](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/ecr/main.tf:58), [variables.tf:118](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/variables.tf:118) |
| Base | `modules/messaging` | Uma fila de eventos, uma DLQ e a tabela DynamoDB `ToggleMasterAnalytics`, com chave `event_id` | [messaging/main.tf:22](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/messaging/main.tf:22), linhas 40 e 79 |
| Base | `modules/iam-ci` | Cria ou lê emissor OIDC do GitHub conforme flag; role, policy ECR e associação; confiança aponta para repo04 | [iam-ci/main.tf:41](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/iam-ci/main.tf:41), linhas 65, 144, 150, 207 e 214 |
| Cluster | `modules/eks` | Cluster EKS, node group gerenciado, roles/policies de control plane/nós/EBS CSI, emissor OIDC do cluster; cinco add-ons: VPC CNI, CoreDNS, kube-proxy, EBS CSI e metrics-server | [eks/main.tf:48](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/eks/main.tf:48), linhas 66, 129, 159, 186, 259 e 282 |
| Cluster | `modules/rds` | Dois RDS PostgreSQL pelo mapa auth/flag; subnet group e security group compartilhados; uma senha e um segredo/versão Secrets Manager por banco | [rds/main.tf:26](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/rds/main.tf:26), linhas 47, 58, 92, 178 e 193; [cluster/variables.tf:127](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/variables.tf:127) |
| Cluster | `modules/elasticache` | Subnet group, security group e replication group Redis com um nó e sem réplica | [elasticache/main.tf:22](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/elasticache/main.tf:22), linhas 29 e 66 |
| Cluster | `modules/irsa` | Duas roles de ServiceAccounts: evaluation publica em SQS; analytics consome SQS e escreve DynamoDB; policies e associações próprias | [cluster/main.tf:133](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/main.tf:133), [irsa/main.tf:74](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/irsa/main.tf:74), linhas 111, 117, 162 e 168 |
| k8s | `secrets.tf` | Namespace da aplicação; três valores aleatórios; cinco Secrets de auth, flag, targeting, banco targeting e evaluation | [secrets.tf:38](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/secrets.tf:38), linhas 61, 70, 83, 92, 121, 148, 177 e 211 |
| k8s | `storageclass.tf` | StorageClass `gp3`, provisioner EBS CSI, `WaitForFirstConsumer`, volume criptografado e política `Delete` | [storageclass.tf:27](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/storageclass.tf:27) |
| k8s | `argocd.tf` | Namespace ArgoCD, credencial de leitura opcional para repo privado, release Helm do ArgoCD e Application observando o overlay prod do repo04 | [argocd.tf:30](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/argocd.tf:30), linhas 52, 94 e 270 |

Os Deployments da aplicação e o StatefulSet PostgreSQL targeting são conteúdo GitOps aplicado pelo ArgoCD. O disco EBS gerado a partir de um PVC é provisionado pelo CSI; não aparece como um `aws_ebs_volume` diretamente gerenciado nestas raízes. O estado Terraform não inventaria automaticamente todos os objetos filhos criados por Kubernetes, Helm ou serviços AWS.

**Limite de escopo:** o Terraform atual ainda é a base importada. Não há declaração aqui que implante a stack planejada de OTel Collector, Prometheus, Loki e Grafana ou configure New Relic, Slack, PagerDuty e o self-healing da Fase 4. Esses itens continuam como trabalho de implementação, conforme o backlog vigente.

## 6. Backend parcial: o que já está pronto e o que falta

Cada `backend.tf` já informa `key`, `encrypt=true` e `use_lockfile=true`. O bucket e a região foram retirados do código operacional fixo; serão fornecidos em um `backend.hcl` local. Existem três exemplos, cada um com a chave da respectiva camada e a sentinela `NOVO_BUCKET_ESTADO_FASE4`.

Há **duas configurações separadas**, que precisam concordar:

| Configuração | Uso | Arquivo/entrada |
|---|---|---|
| Backend de cada raiz | Onde ler/gravar o próprio state dessa raiz | `backend.hcl`, passado ao `init` |
| Leitura dos estados anteriores | De onde cluster/k8s extraem outputs de base/cluster | `state_bucket`, `state_region`, `base_state_key` e `cluster_state_key` |

`terraform.tfvars`/`TF_VAR_...` alimentam variáveis da configuração. Não preenchem automaticamente o bloco backend, inicializado separadamente. `expected_aws_account_id` também não configura automaticamente a conta de acesso do backend. Referência local: [README Terraform:23](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:23); explicação oficial: [configuração parcial de backend](https://developer.hashicorp.com/terraform/language/backend).

O nome do bucket não basta: ele precisa existir antes da inicialização real e estar acessível à identidade correta. O código atual não contém um módulo de bootstrap S3; o procedimento histórico é criá-lo fora destas três raízes. A propriedade de ser “manual” é uma escolha do projeto; tecnicamente poderia haver uma raiz bootstrap independente, mas ela não foi implementada. Fonte: [README Terraform:19](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:19) e [guia histórico:258](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/docs/GUIA_DE_REPRODUCAO.md:258).

Para esse bootstrap, o guia histórico descreve privacidade/bloqueio público, versionamento, criptografia e política de TLS. São propriedades a conferir no futuro bucket; `encrypt=true` no backend não configura sozinho todas essas proteções. Versionamento permite recuperar versões do arquivo; não transforma state em backup dos bancos. O guia antigo usa conta/chaves antigas em outras seções: seus comandos não devem ser copiados literalmente para o 04. As chaves vigentes são `phase4/prod/*`, e o README Terraform atual prevalece.

### Três coisas diferentes chamadas “lock”

| Nome | Função | Versionar no Git? |
|---|---|---|
| Lock S3 do estado, normalmente objeto `<chave>.tflock` | Coordena operações concorrentes que precisam bloquear aquele state | Não |
| `.terraform.lock.hcl` | Registra versões e checksums selecionados dos providers | Sim |
| Versionamento do bucket | Mantém versões dos objetos para recuperação | É configuração do bucket, não arquivo Git |

O backend S3 usa lock quando `use_lockfile=true`; precisa de permissões para criar, ler e apagar o objeto de lock. Esse desenho não usa uma tabela DynamoDB para travar state. A tabela DynamoDB de analytics é um dado da aplicação e tem outra finalidade. Lock não substitui backups, revisão do plano ou coordenação entre estados diferentes. Fonte oficial consultada em 2026-10-22: [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3); configuração local em cada `backend.tf`.

## 7. Providers, versões e proteção de conta

Provider é um plugin; backend S3 faz parte do Terraform. Ambos podem acessar AWS, mas possuem configurações de autenticação separadas. Portanto o guard do provider não deve ser interpretado como proteção universal de backend, remote state ou comandos AWS externos.

| Raiz | Providers declarados/selecionados no lockfile atual | Fonte |
|---|---|---|
| Base | AWS `6.62.0`; exigência configurada `>=5.46` | [backend.tf:22](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/backend.tf:22), [lockfile:4](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/.terraform.lock.hcl:4) |
| Cluster | AWS `6.63.0`, Random `3.9.0`, TLS `4.4.0` | [backend.tf:18](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/backend.tf:18), [lockfile:4](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/.terraform.lock.hcl:4) |
| k8s | AWS `6.63.0`, Helm `3.3.0`, Kubernetes `3.2.1`, Random `3.9.0`; Helm/Kubernetes restringidos à série 3.x nos `.tf` | [backend.tf:18](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/backend.tf:18), [lockfile:4](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/.terraform.lock.hcl:4) |

As raízes independentes podem ter seleções diferentes do provider AWS. Não foi feita atualização de dependências nesta leitura. Nos lockfiles k8s, o texto `constraints` registra restrições anteriores mais amplas, enquanto as versões selecionadas continuam dentro da série 3.x exigida atualmente. A validação registrada usou `-lockfile=readonly`; uma futura normalização do metadado exigiria revisão, sem implicar que se deve atualizar o provider para a versão mais nova.

O lockfile fixa providers e seus checksums; não fixa o binário Terraform, recursos ativos ou módulos remotos. A chamada VPC é `version="~>5.0"`, portanto admite atualizações dentro da série 5.x. O comentário que cita a versão histórica 5.21.0 não a fixa. Fonte: [main.tf:45](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/main.tf:45) e [lockfile de dependências](https://developer.hashicorp.com/terraform/language/files/dependency-lock), consultado em 2026-10-22.

As três raízes exigem `expected_aws_account_id` sem valor padrão e validam 12 dígitos. O provider AWS usa `allowed_account_ids=[var.expected_aws_account_id]`. A sentinela dos exemplos não passa essa validação. Isso ajuda a recusar credenciais de outra conta ao configurar o provider; não confirma existência de conta, saldo, permissões ou a propriedade do bucket. Fontes: [variables.tf:24](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/variables.tf:24), [providers.tf:9](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/providers.tf:9), [cluster/providers.tf:8](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/providers.tf:8), [k8s/providers.tf:16](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/providers.tf:16).

Os backends/data sources atuais não contêm `allowed_account_ids`. O backend S3 também oferece essa opção, mas ela deve ser configurada especificamente para ele. Nesta análise, isso é observação da separação de responsabilidades, não alteração autorizada. Fonte oficial: [opções de autenticação S3](https://developer.hashicorp.com/terraform/language/backend/s3#credentials-and-shared-configuration).

Kubernetes e Helm obtêm endpoint/CA do estado do cluster e usam `aws eks get-token` por `exec`. Além de credenciais AWS, será necessário que a identidade tenha acesso à API EKS e à rede do endpoint. Não assumir que um perfil correto para o bucket já possui essas permissões. Na raiz k8s, não foi encontrado recurso/data source AWS que consuma o provider AWS declarado: as leituras de estado usam o provider embutido do Terraform e o token é obtido pela AWS CLI. Por isso, não confiar no `allowed_account_ids` desse provider como proteção da operação Kubernetes/Helm ou da leitura dos estados; a identidade efetiva precisa ser conferida separadamente. Esta conclusão deriva da leitura estática, sem teste de autenticação. Fonte: [k8s/providers.tf:30](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/providers.tf:30) e [k8s/data.tf:16](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/data.tf:16).

## 8. `.terraform/`, lockfile, state e plan não são a mesma coisa

`.terraform/` guarda material de trabalho, como módulos/providers baixados, além de metadados da inicialização. Quando há backend inicializado, `.terraform/terraform.tfstate` pode guardar a **configuração local do backend**; não deve ser confundido com o snapshot da infraestrutura armazenado no backend remoto. Pode conter informação sensível, por isso não deve ser compartilhado como se fosse código. Fonte: [backend e dados locais](https://developer.hashicorp.com/terraform/language/backend#initialize-the-backend), consultado em 2026-10-22.

Um plano salvo é um arquivo de execução, não uma receita portátil para outra conta. Ele pode incorporar valores sensíveis e está ligado à configuração e ao estado/destino que o produziram. O comando `plan` normalmente consulta objetos remotos, compara-os à configuração/estado e propõe alterações; ele não executa as alterações propostas, mas tampouco é um teste totalmente offline. `apply` executa a proposta e atualiza o estado conforme o resultado. Fonte: [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan), consultado em 2026-10-22.

A política Git atual ignora `.tfstate*`, `.terraform/`, arquivos reais `.tfvars`, `.tfplan`, `tfplan` e credenciais; preserva os exemplos e lockfiles. `terraform/.gitignore` ignora os três `backend.hcl` locais. Não foi identificado arquivo desses tipos rastreado por esta inspeção dos lockfiles e configurações. Essas regras ajudam a evitar inclusão acidental; não saneiam um arquivo já rastreado nem autorizam publicar segredos. Fontes: [.gitignore:2](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/.gitignore:2), [terraform/.gitignore:1](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/.gitignore:1).

## 9. O que os testes anteriores demonstraram

Em 2026-10-20, o relatório da importação registrou sucesso em `fmt`, `init -backend=false -input=false -lockfile=readonly` e `validate` nas três raízes. Esses comandos não foram repetidos nesta análise. Fonte: [RESULTADO_IMPORTACAO:34](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/00_COLAB_IA/02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md:34).

| Verificação | O que ajuda a provar | O que não prova |
|---|---|---|
| `fmt -check` | Formatação conforme a ferramenta | Correção da arquitetura ou disponibilidade de recursos |
| `init -backend=false` | Resolução/instalação de dependências sem inicializar o backend | Acesso ao S3 ou identidade da conta |
| `validate` | Coerência sintática e estrutural da configuração com os schemas dos providers | Plano real, cotas, orçamento, conectividade e sucesso da aplicação |
| Renderização GitOps/Compose config | Estrutura local dos manifests/configuração | Execução de contêineres ou funcionamento do serviço |

“Sem AWS” não significa necessariamente “sem internet”: `init` pode baixar módulos e providers. Fonte: [terraform init](https://developer.hashicorp.com/terraform/cli/commands/init).

O workflow [Terraform Check:28](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/.github/workflows/terraform-check.yml:28) está configurado para PR, push em `main`/`dev` com filtros de caminho e disparo manual. Instala Terraform `1.16.0`, faz `fmt`, inicializa sem backend e executa `validate` nas três raízes. Não contém `plan`/`apply`, credenciais AWS ou provisionamento. Sua execução no GitHub depende de publicação/disparo e não foi comprovada nesta análise. Fontes: linhas 65, 74, 84–97 desse arquivo.

Os workflows de serviço têm outra finalidade: build/análise de aplicação e publicação ECR nas condições configuradas. Agora recebem `AWS_REGION`, `ECR_REGISTRY` e `AWS_ROLE_ARN` de repository variables; possuem verificação de consistência de conta/região antes de publicar. Não são um pipeline Terraform completo. Fontes: [_ci-go.yml:55](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/.github/workflows/_ci-go.yml:55), linha 356; [_ci-python.yml:49](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/.github/workflows/_ci-python.yml:49), linha 387.

## 10. Pontos de atenção reais para a retomada

1. **Conta/backend ainda pendentes.** Não há `backend.hcl` nem `terraform.tfvars` reais nestas raízes. Bucket, conta, permissões e cobrança atuais permanecem `[INCERTO]` até a conferência apropriada. O guard do provider não dispensa validar separadamente backend, remotes e perfil.
2. **NAT tem padrões diferentes.** A variável tem padrão `true`, mas o exemplo da base define `enable_nat_gateway=false`. `.example` não é carregado automaticamente. Na futura implantação do cluster privado, a saída de rede deve estar disponível. Não interpretar a base como “sempre barata”: há componentes potencialmente cobrados e os preços nos comentários são históricos. Fontes: [variables.tf:100](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/variables.tf:100), [tfvars.example:41](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/terraform.tfvars.example:41).
3. **Topologia final ainda precisa sizing.** O código herdado usa desejado de dois workers, Kubernetes `1.34`, `c7i-flex.large`, dois RDS e cache `cache.t3.micro`; o plano da Fase 4 propõe três workers. Isso é diferença entre base implementada e plano futuro, não implantação de três nós. As restrições Free Tier/aprovação acadêmica citadas em comentários referem-se ao contexto anterior. Fonte: [cluster/variables.tf:68](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/variables.tf:68) e backlog E2.
4. **Primeira execução k8s exige tratamento do CRD.** A Application do ArgoCD usa `kubernetes_manifest`, que precisa conhecer seu schema no planejamento. O próprio arquivo documenta primeiro instalar ArgoCD/CRD e depois planejar o restante; `depends_on` não faz o CRD aparecer durante o primeiro plan. Esse é procedimento futuro, não comando executado aqui. Fonte: [argocd.tf:226](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/argocd.tf:226).
5. **Infraestrutura pronta não implica aplicação pronta.** Os bancos RDS precisam dos schemas; a chave de serviço nasce provisória e precisa ser criada no auth/atualizada no Secret. O Secret evaluation tem `ignore_changes=[data]`, preservando esse valor após seed, com a limitação de que recriação exige seed novamente. Fonte: [secrets.tf:75](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/secrets.tf:75), linha 255; [guia histórico:484](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/docs/GUIA_DE_REPRODUCAO.md:484).
6. **Segredos ficam em estado apesar de existirem no Secrets Manager.** O código gera senhas e as publica no Secrets Manager, outputs sensíveis e Secrets Kubernetes. Não dizer que “nunca passam por arquivo de texto”: o state persiste esses valores. Tratar estados, backups e planos como sensíveis. Fontes: [rds/main.tf:193](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/rds/main.tf:193), [cluster/outputs.tf:95](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/cluster/outputs.tf:95).
7. **Destruição não tem proteção automática de dados.** RDS está com `skip_final_snapshot=true` e `deletion_protection=false`; Secrets Manager com `recovery_window_in_days=0`; StorageClass usa `Delete`. Isso favorece descarte de laboratório, mas exige preservar o que for necessário antes de uma destruição expressamente autorizada. Preservar CSI até confirmar remoção de PVC/PV/EBS; bucket de estado por último. Fonte: [rds/main.tf:147](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/modules/rds/main.tf:147), linha 190; [storageclass.tf:57](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/k8s/storageclass.tf:57); [README Terraform:65](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/README.md:65).
8. **Há comentários históricos imprecisos.** `use_lockfile` já aparece como experimental no Terraform 1.10; dizer que surgiu somente no 1.11 é incorreto. Manter mínimo `>=1.11` continua sendo uma restrição válida do repositório, sem precisar alterar IaC por causa da explicação. Fonte: [documentação oficial 1.10](https://developer.hashicorp.com/terraform/language/v1.10.x/backend/s3#state-locking), contraposta ao comentário em [backend.tf:17](C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/terraform/backend.tf:17). Cabeçalhos também falam em Secrets Manager no provider AWS de k8s, mas o código k8s atual recebe URLs pelo remote state; não há data source de leitura Secrets Manager nessa raiz. O código executável prevalece sobre os comentários.

Esses pontos foram documentados, sem correção da IaC, sem mudança de decisão e sem confirmação de recursos ativos.

## 11. Verificação desta análise e estado para o próximo agente

- [x] Ler backend, providers, entradas/saídas e exemplos das três raízes.
- [x] Inventariar sete módulos locais e distinguir o módulo VPC externo.
- [x] Conferir chamadas, data sources, dependências e recursos declarados.
- [x] Conferir workflow Terraform e separação dos workflows de serviço.
- [x] Conferir metadados de existência local e regras de Git, sem ler segredos/state.
- [x] Conferir conceitos em documentação primária HashiCorp, inclusive lock S3/lockfile e limites de remote state.
- [x] Registrar diferenças entre código importado, planejamento e evidência de execução; 64 links locais com arquivos e linhas existentes conferidos, sem falhas.
- [x] Conferir lista Git: zero arquivos de estado, planos, `.terraform/`, `backend.hcl` reais ou `.tfvars` reais rastreados. Lockfiles e exemplos permanecem versionados.

Este relatório é o único arquivo criado por este agente. Nenhum `.tf`, workflow, estado, configuração real, branch, commit, recurso AWS ou contexto de outro agente foi alterado. A análise não executou `terraform init`, `plan`, `apply`, comandos de state ou comandos AWS. O teste Compose e a instrumentação seguem pendentes conforme a condução do agente principal; conta/backend podem ser preparados em paralelo quando os dados/autorização aplicáveis estiverem disponíveis.

Fontes e datas: leituras locais e documentação oficial consultadas em **2026-10-22**; a validação de importação foi executada/documentada em **2026-10-20**, e está explicitamente citada como evidência anterior. Valores/preços/limitações da conta antiga nos documentos históricos não foram reutilizados como fatos atuais.
