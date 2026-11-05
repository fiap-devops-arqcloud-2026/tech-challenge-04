# Preparação da implantação (B3) — 2026-11-04

TL;DR: tudo o que dá para validar sem implantar foi validado. As notificações reais funcionam com a nova chave: PagerDuty, Slack e o cartão até Resolved. Os testes dos 5 serviços, o ensaio integrado e o ensaio da falha proposital passaram. O plano real da base mostra **8 imports, 29 criações, 7 alterações no lugar e 0 destruições**. A estimativa oficial é de **US$ 9,82 por dia com tudo ligado**; o período B3–B5 sai por cerca de US$ 45 dos US$ 100. **Atualização 2026-11-05:** os tokens foram validados, o orçamento foi criado e os créditos subiram para US$ 120. Antes de implantar, falta só a autorização dos tópicos 5 (implantação) e 6 (demonstração e entrega).

Última atualização: 2026-11-05, Claude (Opus 5.5): seção 5 com os pré-requisitos fechados e notas datadas nas seções 1, 2, 4, 6 e 7. Versão inicial em 2026-11-04, Claude, continuando a sessão do Codex do mesmo dia. O ID da conta aparece como `<CONTA>`. As evidências brutas ficam em `validacao-local-preimplantacao-2026-11-04/`, ignorada pelo Git.

## 1. Validações feitas (2026-11-04)

| Validação | Resultado | Quem | Evidência |
|---|---|---|---|
| PagerDuty com a nova integração Events API V2 | trigger `HTTP 202` (16:18:25) e resolve `HTTP 202` (16:19:26) | Codex | `notifications-result.json` |
| Slack: webhook direto e cartão do PagerDuty | webhook `HTTP 200 ok`; cartão às 16:18:30; fio "Resolved by Events API V2" às 16:19:33 | Codex | `notificacoes-conferencia-ui.md` |
| Ensaio integrado no Compose (5 serviços, Collector, New Relic) | `test-flow` ok. `test-traces` falhou na 1ª execução e passou na repetição das 16:30: 19 spans, 5 serviços, SQS, PostgreSQL, logs, privacidade e `/health` | Codex | `integration-results.json`, `traces/resultado-traces.json` |
| Exportação ao New Relic no laboratório | 0 falhas nos logs do Collector | Claude | `docker logs` do `tc04-predeploy-otel-collector-1` |
| Falha proposital de ponta a ponta | 11/11 etapas: 503 em JSON nas rotas `/flags`, `/health` 200, controle exige chave, reinício limpa a falha, 13 de 15 spans SERVER com `STATUS_CODE_ERROR` (os 2 restantes são as consultas ao controle) | Claude | `ensaio-falha-resultado.json` |
| Testes unitários | auth e evaluation (`go vet` e `go test`), flag (13 + 6 subtestes), targeting (6), analytics (8) | Claude | saída dos comandos neste LOG |
| Lint do CI no flag-service | `flake8` estrito 0; `pylint` 9,42 (corte 7,0); `bandit` sem achados | Claude | idem |
| Self-healing | `test-restart.sh` 11 cenários; `actionlint` e `shellcheck` limpos | Claude | LOG 2026-11-03 20:52 |
| Charts, Collector e Grafana | `helm template`, `otelcol validate` e Grafana 13.3.0 sem rede | Claude | LOG 2026-11-03 20:52 |
| *Em 2026-11-05:* confiança OIDC no CI | `terraform test` do módulo `iam-ci`, 10/10 local e no Terraform Check; 6 de 6 defeitos introduzidos reprovados | Claude | LOG 2026-11-05 13:52 |

Com o cluster ligado, a notificação do PagerDuty passa a vir do contact point do Grafana. O que se provou aqui é a chave e o caminho; o envio pelo Grafana só é provado no B4.

## 2. Conta AWS e GitHub (consulta somente leitura, 2026-11-04 16:18)

- **Plano:** `FREE`, ativo, **US$ 100,00 de crédito** e validade até 2027-04-20. *Em 2026-11-05: US$ 120, depois da atividade do Budgets.*
- **Atividades de crédito:** 5 de US$ 20, todas não iniciadas:
  - EC2;
  - Bedrock playground;
  - **AWS Budgets** (concluída em 2026-11-05);
  - Lambda;
  - **RDS**.

  Não é certo que recursos criados pelo Terraform contem para EC2 e RDS. Depois do B3, conferir com `aws freetier list-account-activities`.
- **Cota de vCPU (On-Demand Standard): 5.** Os 2 nós m7i-flex.large usam 4. Por isso o tfvars local tem `node_group_max_size = 2`: um 3º nó estouraria a cota.
- **Região:** m7i-flex.large é `FreeTierEligible` e existe em us-east-2. O EKS 1.34 tem suporte padrão até 2026-12-01, depois da entrega.
- **Recursos:** nenhum cluster, instância, RDS, Redis ou NAT existente. Existem os 5 ECR, a role do CI com a policy e o provedor OIDC.
- **AWS Budgets:** nenhum orçamento em 2026-11-04. *Em 2026-11-05: `togglemaster-creditos` criado; ver a seção 5.*
- **Bucket de estado:** versionado, criptografado (AES256), acesso público bloqueado, sem estado em `phase4/prod/`.
- **GitHub:**
  - repositório privado, branch padrão `main`;
  - Variables `AWS_REGION`, `AWS_ROLE_ARN` e `ECR_REGISTRY`; faltam `AWS_SELF_HEALING_ROLE_ARN` e `EKS_CLUSTER_NAME`, a criar depois do apply da base;
  - subject OIDC imutável (`repo:...@287716251/...@1373159817`), o mesmo da trust das roles;
  - nenhum secret.

## 3. Terraform (planos reais de 2026-11-04 16:30)

Os 3 `terraform.tfvars` locais vêm dos exemplos, com conta, bucket, NAT ligado e 2 nós (máximo 2), e são ignorados pelo Git. `init` e `validate` passaram nas 3 camadas.

**Base: `8 to import, 29 to add, 7 to change, 0 to destroy`.**
- Imports:
  - 5 ECR, alterando só `force_delete`, que é atributo do Terraform e não muda nada na AWS;
  - a policy, ganhando tags;
  - a role do CI, com tags, descrição e o **rótulo `Sid`** da confiança (`GithubOidcMain` → `GithubOidcAssume`). As condições (audiência, subject e provedor) ficam **idênticas**: conferido comparando o documento antes e depois;
  - o anexo da policy, sem mudança.
- Criações:
  - VPC com 4 subnets, IGW, NAT e rotas;
  - SQS e DLQ;
  - DynamoDB;
  - 5 lifecycle policies;
  - a role `togglemaster-self-healing`, com `eks:DescribeCluster` em `arn:aws:eks:us-east-2:<CONTA>:cluster/togglemaster`.

**Cluster e k8s:** os planos não fecham antes do apply da base. A camada cluster lê o estado remoto da base (`Unable to find remote state`), e a k8s precisa do estado do cluster e dos 4 `TF_VAR_*` dos segredos. É uma dependência prevista, não um defeito: esses planos são revisados entre os applies, na ordem do roteiro abaixo.

**Correções do Codex nesta sessão**, validadas e commitadas:
- **Nome do cluster:** o EKS se chama `togglemaster`. `togglemaster-eks-cluster` é o nome da role IAM do cluster. O ARN da permissão do self-healing foi corrigido.
- **Token do ArgoCD:** o `count` do Secret do repositório agora usa `nonsensitive(...)`, porque o Terraform recusa valor sensível em `count`.

## 4. Custos (AWS Price List API, us-east-2, sob demanda, 2026-11-04)

| Item | Preço oficial | Por dia |
|---|---|---|
| Control plane do EKS (suporte padrão) | US$ 0,10/h | US$ 2,40 |
| 2 nós m7i-flex.large | US$ 0,09576/h cada | US$ 4,60 |
| 2 RDS db.t3.micro PostgreSQL Single-AZ | US$ 0,018/h cada | US$ 0,86 |
| ElastiCache cache.t3.micro (Redis) | US$ 0,017/h | US$ 0,41 |
| NAT Gateway | US$ 0,045/h + US$ 0,045/GB | US$ 1,08 + tráfego |
| IPv4 público do NAT | US$ 0,005/h | US$ 0,12 |
| Discos: nós 2 × 20 GiB (gp2 no pior caso, US$ 0,10/GB-mês), PVCs 15 GiB gp3 (US$ 0,08), RDS 2 × 20 GiB gp3 (US$ 0,115) | — | US$ 0,32 |
| Secrets Manager, 2 segredos | US$ 0,40/segredo-mês | US$ 0,03 |
| **Total com tudo ligado** | **US$ 0,409/h** | **US$ 9,82** |

| Cenário | Custo estimado | Sobra dos US$ 100 |
|---|---|---|
| B3 → fim da gravação: 06/11 08h até 10/11 22h (110 h) + 8 GB no NAT | **US$ 45,35** | US$ 54,65 |
| Ligado de 06/11 a 12/11 (7 dias) | US$ 69,08 | US$ 30,92 |
| Limite teórico | 244 h (10,2 dias) | — |
| Base sem cluster, NAT ligado | US$ 1,20/dia | — |
| Base sem cluster, NAT desligado | quase zero | — |

*Em 2026-11-05, com US$ 120 de crédito:*
- o B3–B5 deixa cerca de US$ 74,65;
- os 7 dias deixam US$ 50,92;
- o limite teórico passa a 293 h (12,2 dias).

**Fora da conta por serem desprezíveis:** SQS, DynamoDB sob demanda, ECR, S3 do estado, tráfego entre zonas e saída para a internet, que tem os primeiros 100 GB/mês gratuitos. Não há CloudWatch Logs do control plane ligado.

**Riscos de custo:**
- Se os créditos acabarem, a conta é **suspensa**.
- Ultrapassar o desenho, com 3 nós ou outro tipo de instância, falha por cota ou por restrição do plano.
- Depois do destroy, PVCs órfãos deixam volumes EBS cobrando: conferir `aws ec2 describe-volumes`.

## 5. Pré-requisitos do usuário (antes do tópico 5)

*Atualização 2026-11-05: os itens 1 a 3 estão resolvidos. Falta só a autorização dos tópicos 5 e 6.*

1. **Orçamento no AWS Budgets: criado em 2026-11-05** pelo Claude, a pedido do usuário.
   - Chama-se `togglemaster-creditos`. É um orçamento de custo que soma o gasto de 2026-10-01 a 2027-04-30, o período dos créditos, em vez de recomeçar a cada mês.
   - O limite é de US$ 80, e os créditos ficam fora da conta (filtro `RECORD_TYPE` diferente de `Credit`, métrica `UnblendedCost`). Com eles dentro, o gasto líquido ficaria em zero e nenhum alerta dispararia.
   - São 5 alertas, enviados aos 2 e-mails indicados pelo usuário:
     - gasto real acima de 25%, 50%, 75% e 100% (US$ 20, 40, 60 e 80);
     - previsão acima de 100%.
   - Fica fora do Terraform de propósito, para o `destroy` não apagar o aviso de recursos esquecidos.
   - A atividade de crédito foi concluída às 13:12 UTC: os créditos passaram de US$ 100 para US$ 120.
2. **Tokens do GitHub: salvos e validados em 2026-11-05**, conforme [o guia](TOKENS_GITHUB_PREIMPLANTACAO_2026-11-04_v01.md).
   - Os dois são fine-grained, diferentes e valem até 2027-01-04.
   - Os dois leem o repositório pela API e pelo git via HTTPS, com o usuário `git`, como o ArgoCD.
   - O `GITHUB_DISPATCH_TOKEN` faz `repository_dispatch` (HTTP 204).
   - ⚠️ O `GITHUB_ARGOCD_TOKEN` também tem escrita: o dispatch respondeu 204, e não 403. O usuário decidiu manter assim (D-020).
3. **Senha do PagerDuty:** não será trocada, por decisão do usuário em 2026-11-05 (D-020).
4. **Integração PRTG:** foi preservada como contingência. Removê-la depois do ensaio é opcional.

## 6. Roteiro do tópico 5 (só com autorização específica)

1. **Variáveis de ambiente** a partir do `.env`, no Git Bash:
   ```bash
   set -a; . ./.env; set +a
   export TF_VAR_new_relic_license_key="$NEW_RELIC_LICENSE_KEY"
   export TF_VAR_pagerduty_integration_key="$PAGERDUTY_INTEGRATION_KEY"
   export TF_VAR_slack_webhook_url="$SLACK_WEBHOOK_URL"
   export TF_VAR_github_dispatch_token="$GITHUB_DISPATCH_TOKEN"
   export TF_VAR_github_token="$GITHUB_ARGOCD_TOKEN"
   ```
2. **Base:** `terraform -chdir=terraform plan -out=base.tfplan`. Conferir de novo **8 import, 0 destroy, sem replace**, e só então `apply base.tfplan`.
3. **Variables do GitHub:**
   - `AWS_SELF_HEALING_ROLE_ARN` com o output `self_healing_role_arn`;
   - `EKS_CLUSTER_NAME` = `togglemaster`.
4. **Cluster:** `plan` e `apply`, em cerca de 15–20 min. Depois:
   - `aws eks update-kubeconfig --name togglemaster --region us-east-2`;
   - trocar as sentinelas do overlay (`REDIS_URL`, `AWS_SQS_URL`) pelos outputs reais.
5. **k8s:** primeiro `apply -target=helm_release.argocd`, depois `apply` completo. Isso cria os Secrets, o namespace `observability` e as Applications.
6. **PR dev → main:** o CI publica as 5 imagens e grava as tags no overlay, e o ArgoCD sincroniza. O `self-healing.yml` precisa estar na `main` antes do ensaio. *Em 2026-11-05:* o job `image` faz o primeiro login OIDC real nesta conta; conferir a etapa "Autenticar na AWS via OIDC" antes de seguir.
7. **Aceite:**
   - Applications Synced/Healthy;
   - pods prontos;
   - Grafana com as datasources;
   - traces do cluster no New Relic.

O ensaio da cadeia (tópico 6) vem depois, com gerador de tráfego e a falha ligada por `POST /admin/fault`.

## 7. Limitações

- Nenhum apply, PR, merge ou destroy foi feito.
- Os planos de cluster e k8s não fecham sem a base aplicada.
- O envio de alertas pelo Grafana a PagerDuty, Slack e GitHub só é provado com o cluster no ar.
- Os preços são sob demanda e não contam créditos extras.
- As atividades de crédito podem não reconhecer recursos criados pelo Terraform.
- *Em 2026-11-05:* o AWS Budgets atualiza os números até 3 vezes por dia, em geral a cada 8–12 h, e a previsão depende do histórico de uma conta nova.
  - No B3–B5, o controle de custo é o roteiro, com o destroy no fim.
  - Também conta a conferência dos créditos com `aws freetier get-account-plan-state`.
  - Os alertas são a rede de segurança.

Fontes: AWS Price List API (`aws pricing get-products`, região us-east-2, consultada em 2026-11-04, resposta bruta em `precos-aws-us-east-2.json`); inventário somente leitura da conta (`aws-inventory.json`); planos do Terraform 1.16 (`base-plan.json`, `cluster-plan.log`, `k8s-plan.log`); `gh` (repositório, Variables e customização do subject OIDC). Em 2026-11-05: `aws budgets` e `aws freetier` (`prerequisitos-2026-11-05.txt`) e a documentação do AWS Budgets sobre a frequência de atualização.
