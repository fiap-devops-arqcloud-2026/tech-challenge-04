# Contas e acessos para a Fase 4

TL;DR: precisamos de contas configuráveis e de integrações, não de cinco assinaturas pagas. Reutilizar o GitHub existente; começar New Relic, PagerDuty e Slack pelas opções gratuitas. A AWS exige confirmar cobrança, identidade, permissões e cotas antes do Terraform. Criar outra conta não renova automaticamente o Free Tier. Este guia não comprova criação, acesso ou funcionamento das contas.

Última atualização: 2026-10-28, Codex. Fontes oficiais consultadas nessa data; condições efetivas devem ser conferidas no cadastro. Vinculado a P-011/P-003 e ao plano E0–E7. Escolhas D-009/D-014/D-016 preservadas.

## 1. Explicação simples

| Serviço | Papel no projeto | O que precisa estar pronto |
|---|---|---|
| AWS | Hospedar aplicação, cluster, bancos e infraestrutura | Conta ativa, cobrança conhecida e acesso para provisionar |
| GitHub | Guardar código, executar CI e apoiar GitOps/mitigação | Acesso ao repo04 e permissão para configurar Actions |
| New Relic | Exibir APM, traces e relações entre serviços | Conta com acesso à interface APM e chave de ingestão |
| PagerDuty | Abrir incidentes e chamar o responsável | Serviço, integração e política de escalonamento |
| Slack | Mostrar notificações no canal da equipe | Workspace, canal e integração autorizada |

Criar o cadastro é apenas a primeira parte. Depois configuraremos as integrações e produziremos evidência: trace visível, incidente aberto, responsável acionado e mensagem no canal. Essas provas continuam pendentes.

## 2. AWS

### Como preparar

1. Se já existir uma conta utilizável, conferir sua situação antes de abrir outra. Para novo cadastro, seguir o [guia oficial de criação de conta](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html): e-mail, verificação, senha, dados de contato, escolha de plano, cobrança/identificação exigidas e ativação. O fluxo avançado descrito nessa página pede método de pagamento válido.
2. Para nosso Terraform, priorizar uma conta que permita administrar IAM, rede e recursos diretamente. A AWS diferencia a experiência nova com configurações predefinidas da opção avançada com controle completo. Essa é uma recomendação de compatibilidade com nossa IaC, não uma exigência da FIAP. [Diferenças e serviços suportados](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html).
3. Proteger root com MFA e preparar uma identidade de trabalho com credenciais temporárias para console/CLI; root fica para tarefas da conta. [Boas práticas IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
4. Conferir plano, créditos, orçamento, alertas e cotas. A região hoje configurada no projeto é `us-east-2`; mudar a região exige alinhar variáveis e zonas, não apenas trocar um campo no console.

**Free Tier:** a AWS informa que clientes com conta atual ou anterior não são elegíveis ao novo plano gratuito/créditos. Outra conta ou outro e-mail não resolve essa condição. A disponibilidade de um serviço no plano também não significa que toda configuração ou uso será gratuito. [FAQ oficial](https://aws.amazon.com/free/free-tier-faqs/).

O projeto usa EKS, nós EC2, RDS, Redis/ElastiCache e NAT, além de armazenamento e rede. Precisamos estimar a configuração real antes do apply. Configurar alertas em AWS Budgets ajuda a acompanhar gastos; um alerta comum não é um bloqueio automático garantido. [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

### Permissões e dados que a conta precisa fornecer

- Identidade humana de provisionamento: administrar recursos usados pela IaC — VPC/EC2/EBS, EKS, RDS, ElastiCache, ECR, SQS, DynamoDB, S3 e IAM, incluindo roles/policies/OIDC e PassRole conforme os recursos. A política mínima detalhada ainda precisa ser preparada e validada; esta lista de famílias de serviços não é uma policy pronta.
- Acesso para verificar cobrança/cotas e ajustar limites quando necessário.
- Account ID, região e perfil local de autenticação corretos. O Terraform verifica `expected_aws_account_id` para reduzir o risco de operar na conta errada.
- Bucket S3 próprio para o backend, com controle de acesso e proteção do estado. Preparar esse bootstrap antes do `terraform init` definitivo. Chaves separadas: `phase4/prod/base.tfstate`, `phase4/prod/cluster.tfstate`, `phase4/prod/k8s.tfstate`.
- Role específica do GitHub via OIDC. A role presente no código publica imagens no ECR; ela não é a identidade de provisionamento nem a futura role de mitigação no EKS.

Não é necessário criar EKS, RDS, ECR ou rede manualmente nesta preparação: essas partes já estão declaradas em Terraform. Não reutilizar o estado ou as credenciais da conta anterior. Referência local: [Terraform do projeto](../../terraform/README.md).

**Pronta para o próximo passo:** conta ativa, condições de cobrança compreendidas, perfil local autorizado na conta correta e região/cotas verificadas. A criação do backend e o plan ficam para a etapa de infraestrutura; nenhum apply foi realizado nesta consulta.

## 3. GitHub remoto

### Como preparar

O origin local aponta para [fiap-devops-arqcloud-2026/tech-challenge-04](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04). Isso foi conferido em 2026-10-28, mas a existência, a visibilidade e seus acessos remotos não foram consultados nesta tarefa. Reutilizar sua conta pessoal e o repositório da organização, caso estejam disponíveis; não criar um duplicado.

Você precisa conseguir abrir o repositório e alterar configurações de Actions/variables, diretamente como administrador ou com apoio do administrador da organização. Quem apenas envia código não precisa de todas essas permissões administrativas.

GitHub Free pode atender ao início do projeto. Runners padrão em repositórios públicos são gratuitos; repositórios privados usam a franquia do plano — a documentação consultada indica 2.000 minutos/mês para Free/Free for organizations. Confirmar a política e o consumo da organização. [Cobrança Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [franquias](https://docs.github.com/en/billing/reference/product-usage-included).

### Configuração exigida pelo código atual

Em **Settings → Secrets and variables → Actions → Variables**, após existirem os valores reais da AWS:

| Repository variable | Conteúdo |
|---|---|
| `AWS_REGION` | Região escolhida; padrão atual `us-east-2` |
| `ECR_REGISTRY` | `<account-id>.dkr.ecr.<regiao>.amazonaws.com` |
| `AWS_ROLE_ARN` | ARN da role de publicação criada para GitHub OIDC |

São identificadores de configuração. O fluxo OIDC já previsto obtém credenciais temporárias; não exige cadastrar access key/secret key permanentes da AWS no GitHub. [OIDC GitHub–AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).

O CI usa permissões por job: `id-token: write` para autenticar na AWS e `contents: write` na atualização automatizada de tags GitOps. Não é necessário abrir escrita global indiscriminadamente. A política da organização e as proteções de branch precisam permitir o fluxo aprovado, sem desativar a proteção como atalho.

Hoje os jobs de imagem/GitOps publicam em push na main; dev/PR executam validações. Preparar a conta não publica a dev nem altera esse fluxo. Trabalho humano permanece dev → PR → main, com publicação ainda não autorizada.

Se o repositório for privado, ArgoCD precisa de credencial de leitura: token restrito ao repo04, Contents read-only, respeitando aprovação da organização, passado por `TF_VAR_github_token`. Se público, esse token não é necessário para leitura. A automação futura `repository_dispatch` precisará de autenticação/permissões e payload próprios; não está pronta apenas por criar a conta.

Fontes locais: [workflow Go](../../.github/workflows/_ci-go.yml), [workflow Python](../../.github/workflows/_ci-python.yml), [variáveis Kubernetes](../../terraform/k8s/variables.tf).

**Pronto:** usuário acessa o repo04, administrador permite configurar Actions e integrações, e variáveis podem ser preenchidas com os outputs reais da AWS quando disponíveis.

## 4. New Relic

1. Criar a conta em [New Relic Signup](https://newrelic.com/signup) e confirmar o e-mail.
2. Começar pela oferta gratuita: até 100 GB de ingestão/mês e um full platform user, conforme [documentação de cadastro](https://docs.newrelic.com/docs/accounts/accounts-billing/account-setup/create-your-new-relic-account/). Para nosso teste pequeno, é o ponto de partida recomendado; acompanhar consumo e plano efetivo.
3. Garantir acesso desse usuário ao APM/distributed tracing e permissão para gerenciar a chave de ingestão. Registrar Account ID e região da conta.
4. Obter a **license key/ingest key** na área de API keys. Ela será usada pelo Collector no header `api-key`; não é uma User API key administrativa.

O endpoint OTLP deve corresponder à região New Relic: por exemplo, US `https://otlp.nr-data.net` ou EU `https://otlp.eu01.nr-data.net`, com TLS. A região New Relic é independente da região AWS. O SDK já instrumentado continua enviando ao Collector; configuraremos nele a exportação externa. [Integração OTLP oficial](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/).

**Pronta:** acesso ao APM e chave de ingestão disponível localmente. O aceite seguinte é receber traces e visualizar os cinco serviços, não apenas ter a conta. Podemos validar isso com o Compose antes do cluster AWS. Não houve exportação nesta consulta.

## 5. PagerDuty

Escolher **Incident Management Free**: a página anuncia até cinco usuários, uma escala e uma política de escalonamento, com integrações e notificações básicas. É o ponto de partida para nosso responsável único; não precisamos contratar Runbook Automation para a mitigação planejada no GitHub Actions. [Planos oficiais](https://www.pagerduty.com/pricing/).

1. Usar o cadastro da página oficial, confirmar o usuário e criar a conta com permissão de administrador.
2. Criar um serviço, por exemplo `ToggleMaster Fase 4` — nome sugerido.
3. Vincular uma política de escalonamento ao responsável, diretamente ou por escala. Configurar e-mail/app móvel e regras de notificação.
4. Adicionar uma integração **Events API v2** e guardar a **Integration Key/routing_key**. Essa chave específica envia eventos; não precisamos de uma chave administrativa geral para isso. [Serviços e integrações](https://docs.pagerduty.com/incident-management/services/services-and-integrations), [Events API v2](https://docs.pagerduty.com/developer/events-api-v2-overview).

O cadastro pode iniciar avaliação de 14 dias. Confirmar a seleção/permanência no Free: não presumir migração automática. Se o teste começar em 2026-10-28, 14 dias levam aproximadamente a 2026-11-11, antes do prazo informado para o projeto. [Condições, seção 3.3](https://www.pagerduty.com/terms-of-service/).

**Pronta:** serviço vinculado à política, contato configurado, chave de integração local e plano válido durante a demonstração. Depois validaremos trigger → notificação do responsável → acknowledge → resolve, guardando evidências. Um incidente aberto sozinho não comprova o acionamento humano.

## 6. Slack

1. Criar um workspace no Free seguindo o [guia oficial](https://slack.com/intl/pt-br/help/articles/206845317-Criar-um-workspace-Slack), com e-mail confirmado. Quem cria administra o workspace.
2. Criar um canal, por exemplo `#incidentes-tech-challenge` — nome sugerido.
3. Autorizar um app de integração nesse workspace. Para o caminho simples por webhook: criar o app, ativar **Incoming Webhooks**, clicar em **Add New Webhook to Workspace**, selecionar o canal e autorizar.
4. Guardar a URL gerada como segredo. Para canal privado, o instalador precisa ser membro. [Webhooks oficiais](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/).

Essa opção não exige usar Workflow Builder. O Grafana pode notificar Slack e PagerDuty por contact points, sem depender de uma automação premium do PagerDuty. [Contact points Grafana](https://grafana.com/docs/grafana/latest/alerting/fundamentals/notifications/contact-points/). É uma possibilidade compatível com a arquitetura planejada; configuração/validação ainda pendentes.

**Pronto:** workspace, canal, permissão de instalar app e URL do webhook guardada localmente. Depois comprovar a mensagem real do alerta no canal. O limite exato de apps do Free ficou [INCERTO] por divergência entre páginas oficiais; precisamos de uma integração nesse caminho e devemos conferir a capacidade exibida na conta. [Limites do Free](https://slack.com/help/articles/115002422943-Usage-limits-for-free-workspaces).

## 7. Dados e ordem de execução

| Pode constar na configuração/contexto do projeto | Deve ficar em armazenamento de segredos |
|---|---|
| Região AWS, ID da conta, ARN da role, URL ECR, nome do bucket | Credenciais AWS, se houver; preferir sessão temporária |
| URL do repo04 | Token GitHub para repositório privado ou automação |
| Account ID/região New Relic | License/ingest key New Relic |
| Nome do serviço PagerDuty | Integration/routing key PagerDuty |
| Workspace e nome do canal Slack | URL completa do webhook Slack |

Não enviar chaves, senhas ou URLs de webhook no chat, Git ou prints. Configurá-las localmente ou no mecanismo de Secrets apropriado à etapa. Dados de identificação de contas só precisam ser compartilhados quando necessários à configuração.

Ordem recomendada: conferir GitHub → criar New Relic → preparar Slack/PagerDuty → confirmar cobrança/acessos AWS antes da infraestrutura. Em paralelo podemos continuar o desenvolvimento local; a primeira prova externa recomendada é Compose → Collector → New Relic. A conta AWS pode ser preparada desde já, sem subir recursos imediatamente.

## 8. Verificação e handoff

- [x] Cinco serviços cobertos com cadastro, acesso, integração e critério de prontidão.
- [x] Variáveis, três backends e escopo da role OIDC conferidos com o projeto em 2026-10-28.
- [x] Fontes oficiais datadas e condições incertas separadas das configurações locais confirmadas.
- [x] Nenhuma criação, contratação, credencial, envio de evento/mensagem ou implantação realizada.

[INCERTO] Situação real das cinco contas, permissões da organização, plano efetivo, créditos/cotas e validade das integrações. Confirmar durante a preparação, sem perguntar novamente pelas escolhas de ferramentas já registradas. P-011 documenta orientação concluída; P-003, E1 externa e integrações E2–E7 continuam abertas. Ver [revisão geral](REVISAO_GERAL_FASE4_2026-10-28_v01.md) para a matriz de lacunas; não repetir a importação ou os testes locais já aprovados.
