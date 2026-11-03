# Análise completa do projeto — Tech Challenge Fase 4

TL;DR: dos 44 requisitos do enunciado (42 obrigatórios e 2 bônus), 1 está concluído com evidência, 3 estão implementados sem demonstração, 15 parciais, 23 ausentes e 2 dependem de confirmação da FIAP. A base herdada da Fase 3 é sólida e passa nas validações locais. Falta quase toda a parte nova da Fase 4 no cluster: stack de observabilidade, dashboard, alerta, PagerDuty, Slack, self-healing, vídeo e relatório. A auditoria manteve 112 achados (6 altos, 39 médios, 67 baixos), que se reduzem a 10 causas-raiz. O primeiro bloqueio não é técnico: **o `origin/main` tem um único arquivo, o PDF do enunciado**. Todo o trabalho da Fase 4 existe só na sua pasta local, e o ArgoCD e o CI leem o remoto. O prazo que manda no calendário é o fim do trial do PagerDuty, por volta de 2026-11-11.

Última atualização: 2026-10-31, Claude (Opus 5.5). Auditoria somente leitura: nenhum comando na AWS, nenhum `init`/`plan`/`apply`, nenhum arquivo do projeto alterado. Os IDs de conta AWS aparecem como `<CONTA>`.

## 1. Situação geral

| Indicador | Valor | Fonte |
|---|---|---|
| Requisitos concluídos com evidência | 1 de 44 (REQ-OBR-02) | Seção 2 |
| Implementados, sem demonstração | 3 (REQ-OBR-04, REQ-OBR-13, REQ-BON-02) | Seção 2 |
| Parciais / ausentes / a confirmar | 15 / 23 / 2 | Seção 2 |
| Achados mantidos após verificação | 112: 6 altos, 39 médios, 67 baixos | Apêndice A |
| Achados descartados na verificação | 2 | Apêndice C |
| `terraform fmt -check` e `validate` | aprovados nas 3 camadas (2026-10-30) | frentes Terraform e CI/CD |
| `kubectl kustomize gitops/overlays/prod` | renderiza 23 objetos sem aviso; imagens ainda em sentinela | frente GitOps |
| Conteúdo de `origin/main` | 1 arquivo (`POSTECH - Tech Challenge - Fase 4.pdf`) | `git ls-tree origin/main`, conferido em 2026-10-31 |
| Commits locais fora do remoto | `dev` 103 commits à frente de `origin/dev`; último commit 3b21e65, de 2026-10-20 | `git rev-list`, `git log` |
| Arquivos não comitados | 40 modificados, 73 não rastreados, 34 apagados | `git status --porcelain` |

**Os 5 maiores riscos, em ordem:**

1. **Nada da Fase 4 está no remoto (XCL-01).** O CI só publica imagens a partir da `main`, e o ArgoCD observa a `main`. Um commit parcial também quebraria o build: o `app.py` versionado importa um `telemetry.py` que não está no Git.
2. **Trial do PagerDuty até cerca de 2026-11-11.** A página oficial de preços mostra *Events: Not included* no plano Free, então a demonstração alerta → incidente → Slack precisa ser gravada antes dessa data.
3. **O primeiro `apply` da base colide com os recursos criados à mão** (TFB-01, TFB-02, TFB-03). Não há blocos `import`, e o exemplo de tfvars ainda manda criar o provedor OIDC que já existe.
4. **A stack de observabilidade não existe no GitOps** (GIT-01, TFK-01, OBS-01), e os Deployments não têm as variáveis `OTEL_*` (GIT-02). Sem elas, a instrumentação fica desligada no cluster.
5. **O CI deve falhar na primeira execução** (CIC-02). O lint Python roda o pylint sem instalar as dependências, a nota deve cair abaixo de 7,0 e o job de imagem é pulado. É uma estimativa: o pylint não foi executado.

## 2. Situação dos requisitos

Legenda: ✅ concluído com evidência · 🟦 implementado, falta demonstrar · 🟨 parcial · ⬜ ausente · ❔ a confirmar. A lista completa do que falta em cada requisito, na ordem de execução, está no Apêndice B.

### 2.1 Base das Fases 1–3

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-01 Base funcionando | 🟨 | Hoje só funciona no laboratório local (Compose com Moto). Falta comitar, publicar e implantar na conta nova. |
| REQ-OBR-02 5 serviços conteinerizados | ✅ | Dockerfiles multi-stage e não-root, com execução conjunta comprovada no Compose. Falta versionar as mudanças dos Dockerfiles Python. |
| REQ-OBR-03 Infraestrutura por Terraform | 🟨 | tfvars das 3 camadas, import dos recursos manuais, `plan`/`apply` e capacidade para a stack (3 nós). |
| REQ-OBR-04 CI/CD com DevSecOps | 🟦 | Push da `dev` com CI verde (corrigir o lint Python), revisar o `.trivyignore` e fazer o merge `dev` → `main` para publicar as 5 imagens. |
| REQ-OBR-05 Kubernetes + GitOps | 🟨 | Publicar a base na `main`, trocar as sentinelas do overlay e criar o `ignoreDifferences` do HPA. Depois, o `apply` cluster/k8s e a Application em *Synced/Healthy*. |

### 2.2 Stack open source e OTel Collector

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-06 Stack no cluster via Helm no GitOps | ⬜ | Criar `gitops/observability/` (kube-prometheus-stack, Loki, Collector agent+gateway) e a Application `observability`. |
| REQ-OBR-07 Prometheus (métricas de infra) | ⬜ | Values com o remote write receiver ligado, retenção curta, PVC gp3 e Alertmanager desligado. |
| REQ-OBR-08 Loki (todos os logs) | ⬜ | Loki SingleBinary; agent DaemonSet com `filelog` em todos os namespaces; pipeline de logs até o Loki em `/otlp`. |
| REQ-OBR-09 Grafana | ⬜ | Datasources Prometheus e Loki provisionados e senha de admin vinda de um Secret. |
| REQ-OBR-10 Dashboard (recursos, taxa, logs) | ⬜ | JSON versionado com os 3 painéis. Plano B para a taxa de requisições, caso o `spanmetrics` (alpha) falhe. |
| REQ-OBR-11 Collector central (métricas, logs, traces) | 🟨 | Hoje só há o pipeline local de traces (saída em arquivo). Faltam o gateway com `spanmetrics` e os exporters para Prometheus, Loki e New Relic. |
| REQ-OBR-20 IaC/GitOps com stack e Collector | ⬜ | Consequência dos 6 itens acima, mais a documentação. A auditoria rebaixou o status de parcial para ausente. |
| REQ-BON-01 Grafana Alloy (opcional) | ⬜ | Nenhuma tarefa obrigatória. |

### 2.3 APM e instrumentação

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-12 Escolher Datadog ou New Relic | 🟨 | New Relic escolhido (DECISOES.md:73) e conta criada na região US. Faltam a license key e a primeira ingestão. |
| REQ-OBR-13 Instrumentar código/Dockerfile | 🟦 | Instrumentação pronta (19 spans, 5 serviços, testada em 2026-10-27), mas sem commit e sem as variáveis `OTEL_*` nos manifests. |
| REQ-OBR-14 Trace distribuído no APM | 🟨 | Exporter para `otlp.nr-data.net` no Collector local e um `GET /evaluate` com cache vazio. Dá para fazer **sem AWS**. |
| REQ-OBR-15 Service Map dos 5 serviços | 🟨 | Gerar tráfego e conferir se a aresta assíncrona via SQS (evaluation → analytics) aparece; isso ainda não foi verificado. |
| REQ-OBR-21 Código instrumentado entregue | 🟨 | Commit de `services/**`, incluindo `telemetry.*`, testes e `go.sum`. |
| REQ-BON-02 Bibliotecas OpenTelemetry (preferência) | 🟦 | Já usa só SDKs OTel. Falta mencionar no relatório e no vídeo. |

### 2.4 Alerta, incidente, ChatOps e self-healing

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-16 Alerta inteligente | ⬜ | Regra de proporção de 5xx por serviço, com `for` e agrupamento, versionada no provisioning do Grafana. |
| REQ-OBR-17 PagerDuty abrindo incidente | 🟨 | A conta existe. Serviço, integração Events API v2, escala e regra de notificação **não dependem do cluster: fazer já**. |
| REQ-OBR-18 Notificação detalhada no Slack | ⬜ | Canal, Incoming Webhook e contact point com template (serviço, valor medido, links). |
| REQ-OBR-19 Self-healing automático | ⬜ | Workflow `repository_dispatch`, role OIDC e access entry no EKS, token de escopo mínimo e falha proposital que o restart cura. |
| REQ-OBR-22 Scripts de self-healing entregues | ⬜ | Versionar o workflow, o script (allowlist, cooldown) e as peças do Grafana. |

### 2.5 Vídeo (até 25 min)

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-23 Evidenciar o funcionamento na prática | 🟨 | Concluir E1–E5 e montar a matriz de evidências (requisito → tela → minuto do vídeo). |
| REQ-OBR-24 Vídeo de até 25 min | ⬜ | Roteiro da Fase 4, ensaio cronometrado, gravação e link acessível. |
| REQ-OBR-25 EKS e ArgoCD com a nova stack | 🟨 | Implantação completa e Applications *Synced/Healthy*. |
| REQ-OBR-26 Grafana, dashboard, Loki e roteamento do Collector | ⬜ | Depende da E3/E4. A auditoria rebaixou de parcial para ausente. |
| REQ-OBR-27 New Relic: Service Map, requisição e trace | 🟨 | E1 externa local, depois a mesma exportação no gateway do cluster. |
| REQ-OBR-28 Problema proposital | ⬜ | Escolher uma falha que o `rollout restart` cure, como um estado de erro em memória no flag-service. |
| REQ-OBR-29 Alerta em *Firing* | ⬜ | Ensaiar falha → *Pending* → *Firing* e medir o tempo, para caber no vídeo. |
| REQ-OBR-30 Incidente no PagerDuty e mensagem no Slack | ⬜ | Rebaixado de parcial: nenhuma das duas integrações existe. **Gravar até cerca de 2026-11-10.** |
| REQ-OBR-31 Self-healing executando | ⬜ | Depende do REQ-OBR-19; mostrar o run no GitHub e `kubectl get pods -w`. |

### 2.6 Relatório PDF e entrega

| Requisito | Status | O que falta (resumo) |
|---|---|---|
| REQ-OBR-32 Relatório em PDF | ⬜ | Escrever o Markdown-fonte da Fase 4 sem sobrescrever o da Fase 3 e gerar o PDF (reportlab já está disponível). |
| REQ-OBR-33 Nomes, RMs e usernames | ⬜ | Rebaixado de "a confirmar": o relatório não existe. Antes, confirmar com o tutor se a entrega é individual. |
| REQ-OBR-34 Links do repositório e do vídeo | 🟨 | O repositório é privado e o remoto está vazio. Decidir o acesso do avaliador. |
| REQ-OBR-35 Print do dashboard | ⬜ | Depende da E3/E4. |
| REQ-OBR-36 Print do trace no APM | ⬜ | Pode sair da E1 externa, sem AWS. |
| REQ-OBR-37 Print da notificação no ChatOps | ⬜ | Depende da E4; capturar dentro do trial do PagerDuty. |
| REQ-OBR-38 Print do self-healing | ⬜ | Depende da E5. |
| REQ-OBR-39 Arquitetura OTel explicada | 🟨 | Há bom material planejado. O texto final precisa descrever o que foi implantado. |
| REQ-OBR-40 Justificar New Relic e PagerDuty | 🟨 | As razões estão em DECISOES. Reconfirmar as fontes perto da redação e declarar a limitação do trial. |
| REQ-OBR-41 Desenvolver em grupo | ❔ | O PDF diz "em princípio". Perguntar ao tutor se a entrega individual é aceita (Q-03). |
| REQ-OBR-42 Submeter no prazo | ❔ | Confirmar data, horário e canal de submissão (Q-05/Q-06). |

## 3. Achados por causa raiz

Os 112 achados vêm de 9 frentes. Vários são o mesmo problema visto de camadas diferentes, por isso estão agrupados por causa raiz. Severidade é a que ficou depois da verificação. A tabela completa, com arquivo, linha e recomendação, está no Apêndice A.

### T1 — O trabalho da Fase 4 não está no Git (bloqueia tudo)

- **XCL-01 (alta):** todo o trabalho desde 2026-10-20 existe numa única cópia local: instrumentação, testes, Collector, correção F-023 e documentação. Arquivos versionados dependem de arquivos não versionados; o `services/flag-service/app.py:10` importa `telemetry.py`, que está como `??`. O `origin/main` contém só o PDF.
- **CMP-01 / XCL-02 (média):** `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/offline-test.jsonl` tem 156 MB e não é ignorado. O GitHub recusa arquivos acima de 100 MB, então um `git add -A` quebraria o push.
- **OBS-03 / DOC-05 (média):** `observability/`, `docker-compose.otel.yaml` e os scripts de teste não estão no Git, e o README aponta para eles.
- **TFB-04 (média):** a correção F-023 da trust OIDC só existe na árvore de trabalho; o HEAD da `dev` ainda tem o curinga.
- **34 deleções** de materiais de aula da Fase 3, sem decisão registrada.

**Correção:** ignorar o arquivo de 156 MB; decidir as 34 deleções; fazer commits curados na `dev` com `git add` explícito (serviços + `telemetry.*` + testes, depois observabilidade, Terraform e documentação); validar num clone limpo; push da `dev`; PR para a `main`. Tudo isso só com a sua autorização.

### T2 — O primeiro `apply` da base colide com os recursos criados à mão

- **TFB-01 / XCL-03 / DOC-03 (média):** não há bloco `import` nem roteiro. Com o estado vazio, o `apply` tenta criar os 5 ECR, a role e a policy, falha com *AlreadyExists* e deixa a VPC e o NAT já criados (estado parcial). O verificador rebaixou de alta para média: não há perda de dados e a correção é rápida.
- **TFB-02 (média):** em `terraform/modules/iam-ci/main.tf:212`, a `description` da `aws_iam_policy` força recriação. Se a policy criada no console ficou sem descrição, o `plan` depois do import vai propor destruir e recriar a policy e o attachment. O valor real não foi consultado.
- **TFB-03 (média):** `create_github_oidc_provider = true` (`terraform/variables.tf:241`, `terraform/terraform.tfvars.example:83`) mandaria criar o provedor que já existe, e os thumbprints do código diferem dos reais.

**Correção:** criar `terraform/imports.tf` (5 ECR, role, policy, attachment); usar `create_github_oidc_provider = false` no tfvars local; ajustar a `description`. Aceitar o `plan` só se mostrar **0 destroy/replace**.

### T3 — O GitOps ainda é o da Fase 3

- **GIT-01 (alta, era crítica):** nenhuma peça da stack de observabilidade no GitOps (Collector, Prometheus, Loki, Grafana).
- **GIT-02 (alta):** os ConfigMaps e Deployments não têm `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_ENDPOINT` nem as demais variáveis; o SDK, que só liga quando o endpoint é definido, fica desligado no cluster.
- **TFK-01 (alta):** a camada k8s não tem nada da E2/E3: namespace `observability`, Secrets do New Relic, PagerDuty, Slack e GitHub, e a Application de observabilidade.
- **GIT-03 / TFK-03 (média):** o overlay prod está todo em sentinelas, e a Application acompanha a `main`, que hoje não tem `gitops/`.
- **TFK-11 (média):** o repositório é privado, mas o token de leitura do ArgoCD é opcional e vem vazio por padrão (`terraform/k8s/variables.tf:125`).
- **GIT-04 / TFK-06 (média):** `selfHeal` sem `ignoreDifferences` em `/spec/replicas` disputa com os HPAs; isso também pode desfazer o efeito do self-healing.
- **Endurecimento (baixa):** sem `securityContext` (GIT-05), sem NetworkPolicy (GIT-12), Postgres com tag móvel (GIT-09) e ConfigMaps via `envFrom` sem hash (GIT-06).

### T4 — O Collector ainda é só local

- **OBS-01 (alta):** o Collector tem só o pipeline de traces com saída em arquivo; faltam métricas, logs e os exporters reais.
- **OBS-02 (média):** a sanitização provada localmente não está no desenho do gateway. Se o `keep_keys` for copiado sem ajuste, apaga os atributos `k8s.*` de que Loki e Grafana precisam.
- **OBS-09 (baixa):** o caminho `spanmetrics` → Prometheus, que alimenta o painel de taxa e a regra de alerta, nunca foi validado. O nome real da métrica é incerto.

### T5 — O CI deve falhar na primeira execução da Fase 4

- **CIC-02 (média):** `.github/workflows/_ci-python.yml:180` instala só flake8 e pylint, sem o `requirements.txt`. Os imports de terceiros viram erros E0401, a nota deve ficar abaixo de `fail-under=7.0` (`.pylintrc:37`) e o job `image` é pulado nos 3 serviços Python. Isso é estimativa: o pylint não foi executado.
- **CIC-09 / GIT-14 (média):** nenhum workflow renderiza ou valida o GitOps, embora `scripts/validate-all.sh:57` diga que sim.
- **CIC-03, CIC-04, CIC-05, CIC-08 (média):**
  - jobs de build e lint herdam `id-token: write` e `contents: write`;
  - actions de terceiros estão fixadas por tag móvel (só o Trivy está por SHA);
  - não há varredura de segredos;
  - as exceções do `.trivyignore` tinham revisão marcada para 2026-10-15, já vencida.

### T6 — Capacidade e custo do cluster

- **TFC-01 / XCL-10 (média):** o node group padrão é 2 × c7i-flex.large (4 GiB cada). Não comporta com folga a stack de observabilidade mais o ArgoCD, e o plano pede 3 nós.
- **TFB-10 (baixa):** os comentários subestimam o custo do NAT: não contam o IPv4 público do EIP nem o processamento por GB.
- **TFC-03 (baixa):** o EKS 1.34 fica em suporte padrão até 2026-12-02, depois da entrega; não há urgência.
- **TFC-05 (baixa):** o `destroy` pode deixar volumes EBS órfãos dos PVCs da stack.

**Estimativa de custo:** o projeto estimou cerca de US$ 0,47/h com 3 nós (Fase 3, `09-plano-fontes.html`), sem contar os volumes de Prometheus e Loki. Ligado 24 h, isso dá cerca de US$ 11 por dia. Os créditos da conta nova **continuam não confirmados**.

### T7 — Self-healing: faltam todas as peças

- **CIC-01 (alta):** não existe workflow com `repository_dispatch`. O verificador lembrou dois pontos:
  - o GitHub só dispara `repository_dispatch` para workflows que estão na branch padrão (`main`);
  - interpolar `client_payload` dentro de `run:` abre script injection. O payload deve ir por `env` e ser validado contra uma allowlist.
- **TFC-02 / XCL-08 (média):** o EKS não tem access entry para a role do self-healing nem para um admin explícito; só o criador do cluster recebe acesso.
- **TFB-05 (média):** a role OIDC do self-healing não está declarada na base.
- **GIT-07 (baixa):** falta RBAC mínimo para o self-healing agir sobre os Deployments.

### T8 — Prazo do PagerDuty e confirmações da FIAP

- **DOC-04 (média):** o trial termina antes da meta interna e da entrega, e isso não aparece no README nem no plano.
- **DOC-08 (média):** o trabalho individual contradiz o REQ-OBR-41 (grupo), e não há registro de confirmação do tutor.
- A configuração do PagerDuty, do Slack e do New Relic do lado SaaS **não depende do cluster** e pode começar hoje.

### T9 — Documentação e entrega desatualizadas

- **DOC-01 (média):** não existe relatório da Fase 4. O `docs/RELATORIO_DE_ENTREGA.md` é o da Fase 3 (Grupo 203).
- **DOC-02 (média):** não há roteiro de implantação para a conta nova. O único roteiro, o `GUIA_DE_REPRODUCAO`, é histórico, da Fase 3.
- **DOC-06 / TFB-06, XCL-05 (média):**
  - o README raiz, o `terraform/README.md` e o `CLAUDE.md` ainda dizem que a conta e o bucket estão pendentes;
  - o `CLAUDE.md:9` diz "Nova conta AWS pendente".
- **CMP-03 / CMP-02 (média/baixa):** o `SECURITY.md` descreve a trust OIDC antiga (qualquer branch ou PR) e não cobre os segredos novos.
- **DOC-07 (baixa):** o `docs/ARQUITETURA.md` é histórico e contradiz o código atual.
- **DOC-09 (baixa):** o catálogo de requisitos mostra tudo como "Pendente", com data de 2026-09-20.
- **Âncoras quebradas e resquícios da Fase 3:** DOC-10, DOC-12, TFC-06, TFK-08, XCL-04, CIC-16.

### T10 — Higiene e melhorias menores

Itens de baixa severidade que não bloqueiam a entrega, mas melhoram a qualidade:
- Compose: portas publicadas em todas as interfaces (CMP-04) e imagens de dados com tag flutuante (CMP-08).
- `.gitattributes` só normaliza `*.sh` (CMP-10).
- Validações de variáveis incompletas (TFB-07) e permissões IRSA um pouco acima do uso (TFC-10).
- Redis sem TLS e sem AUTH (TFC-08) e senhas repetidas no state (TFC-09).
- ArgoCD v2.13.2 fora de suporte e afetado pela CVE-2025-55190 (TFK-02). O risco é baixo aqui, porque o acesso é só por port-forward.
- Lockfiles com versões diferentes do provider AWS entre as camadas (XCL-15).
- Detalhes dos scripts de teste (OBS-04, OBS-06, OBS-07, OBS-10).

## 4. O que já está bem feito

- **Terraform:**
  - `fmt -check` e `validate` aprovados nas 3 camadas;
  - backend S3 parcial com `use_lockfile`;
  - `allowed_account_ids` com validação de 12 dígitos, que protege contra operar na conta errada;
  - trust OIDC corrigida com `StringEquals` e subject imutável, idêntica à da conta (etapa 8);
  - policy de push restrita aos 5 ARNs de ECR.
- **CI/CD:**
  - OIDC sem chave estática;
  - só os jobs de imagem e de GitOps, em push na `main`, assumem a role;
  - scan Trivy da imagem antes do push;
  - tag imutável `v1.0.0-<sha7>` usada pelo GitOps;
  - as 3 Variables usadas são exatamente as configuradas no GitHub.
- **GitOps:**
  - nenhum Secret versionado;
  - os nomes dos `secretKeyRef` batem com `terraform/k8s/secrets.tf` e com o contrato;
  - sem campos depreciados do Kustomize;
  - requests, limits e probes nos 6 containers;
  - IRSA com duas ServiceAccounts de menor privilégio.
- **Observabilidade local:**
  - Collector fixado por versão e digest;
  - `memory_limiter` como primeiro processador;
  - portas publicadas só em `127.0.0.1`;
  - teste que consulta o `health_check` real.
- **Consistência entre camadas:** nomes coerentes entre ECR, Kustomize e CI; mesmos nomes de fila, tabela, roles, ServiceAccounts, Secrets e bancos em todas as camadas; nenhum ID da conta da Fase 3 em arquivos operacionais.

## 5. Enunciado × catálogo de requisitos

O PDF foi lido por inteiro e comparado com `docs/requisitos/README.md`. Duas divergências se confirmaram, ambas de baixo impacto:

| Requisito | Tipo | Divergência |
|---|---|---|
| REQ-OBR-19 | detalhe faltante | O PDF (p. 5) aceita três mecanismos de self-healing: Runbook Automation, AWS Lambda ou GitHub Action disparada via webhook. A linha do requisito no catálogo não os cita; eles aparecem só em outra seção. |
| REQ-OBR-41 | exagerado | O PDF (p. 2) diz que a atividade "em princípio" deve ser feita em grupo, mas o catálogo a lista entre os obrigatórios. Já era conhecido (Q-03). |

**Roteiro mínimo do vídeo, na ordem do PDF (p. 5–6):**
1. EKS e ArgoCD rodando com a nova stack.
2. Grafana: dashboard customizado, busca de logs no Loki e explicação do roteamento do Collector.
3. New Relic: Service Map, uma requisição de teste e o trace distribuído.
4. Problema proposital: alerta em *Firing* → incidente no PagerDuty → mensagem no Slack → self-healing executando.

**Prints obrigatórios no relatório (p. 6):** dashboard do Grafana, trace no APM, notificação no ChatOps e log ou execução do self-healing.

## 6. O que falta para concluir: plano com datas

O calendário tem duas âncoras:
- **o fim do trial do PagerDuty, por volta de 2026-11-11 (quarta-feira):** a cadeia de incidente precisa estar gravada antes;
- **a entrega em 2026-11-17 (terça-feira).**

O princípio é fazer **tudo o que não precisa de cluster antes de ligar o cluster**, para reduzir as horas pagas.

| Bloco | Datas-alvo | Entregáveis | Requisitos | Custo AWS |
|---|---|---|---|---|
| **B0 — Git e contas SaaS** | 31/10–01/11 | Ignorar o arquivo de 156 MB; decidir as 34 deleções; commits curados e push da `dev`, que deve rodar o CI sem publicar; corrigir o lint Python (CIC-02). No PagerDuty, criar serviço, integração Events API v2 e escala, e testar com um evento manual. No Slack, criar canal e webhook e testar com uma mensagem. No New Relic, gerar a license key. | 01, 04, 17, 18, 21 | nenhum |
| **B1 — E1 externa (APM sem AWS)** | 01/11–02/11 | Exporter New Relic no Collector local; trace distribuído e Service Map dos 5 serviços no New Relic; prints e trace_id guardados. | 12, 14, 15, 27, 36 | nenhum |
| **B2 — Escrever o que falta (local)** | 02/11–04/11 | **Terraform:** `imports.tf`, OIDC `false`, `description` da policy, tfvars das 3 camadas (phase 4, 3 nós), role e access entry do self-healing, Secrets e namespace `observability`, token do ArgoCD. **GitOps:** `OTEL_*`, `ignoreDifferences`, `gitops/observability/` (charts, values, dashboard, regra de alerta, contact points). **Aplicação e workflow:** falha proposital no flag-service, `self-healing.yml` e script com allowlist e cooldown. Validar com `terraform validate` e `kubectl kustomize`. | 03, 05, 06–11, 16, 19, 20, 22 | nenhum |
| **B3 — Subir a plataforma** | 05/11–06/11 | `plan` da base (aceitar só 0 destroy/replace) e `apply`; merge `dev` → `main`, quando o CI publica as 5 imagens; `apply` do cluster, endpoints reais no overlay e `apply` do k8s; ArgoCD *Synced/Healthy*; stack no ar; dashboard com dados; traces do cluster no New Relic. | 01–11, 13, 25 | começa a cobrança |
| **B4 — Cadeia de incidente** | 07/11–09/11 | Falha → *Firing* → PagerDuty → Slack → self-healing, de ponta a ponta. Ensaiar, capturar os prints e **gravar este trecho até 10/11**, com 1 dia de folga antes do fim do trial. | 16–19, 28–31, 37, 38 | cluster ligado |
| **B5 — Vídeo** | 10/11–12/11 | Roteiro de no máximo 25 minutos, ensaio cronometrado e gravação completa. Depois, `destroy` do cluster e da base (o bucket fica). | 23–26, 35 | encerra a cobrança |
| **B6 — Relatório e submissão** | 13/11–16/11 | Relatório PDF (identificação, links, 4 prints, arquitetura OTel, justificativas); README, ARQUITETURA e GUIA atualizados; merge final; acesso do avaliador ao repositório; submissão até 17/11. | 32–42 | nenhum |

**Riscos do plano:**
- **Capacidade:** pods em *Pending* se o cluster ficar com 2 nós.
- **Métrica do dashboard:** o `spanmetrics` é alpha e o nome da métrica é incerto; o plano B são métricas OTLP direto dos serviços.
- **Cache:** o cache de 30 s do evaluation esconde chamadas, então é preciso um gerador de carga variando flags e usuários.
- **Datas:** não há folga para mais de um dia perdido entre B3 e B4.

`✶ Ponto de atenção:` como o `repository_dispatch` só dispara workflows que estão na `main`, o `self-healing.yml` precisa estar na `main` **antes** do ensaio do B4.

## 7. Decisões que dependem de você

1. **Créditos e plano de cobrança da conta nova** (Billing → Credits; *Free* ou *Paid*). Ainda não confirmados; isso define quantas horas de cluster cabem.
2. **Autorização de Git:** commits curados na `dev`, push e PR/merge `dev` → `main`. Sem isso, nada chega ao CI nem ao ArgoCD.
3. **As 34 deleções** de materiais de aula da Fase 3: restaurar ou comitar a remoção?
4. **O arquivo de 156 MB:** ignorar (recomendado) ou mover.
5. **Provedor OIDC:** deixar fora do Terraform (`create_github_oidc_provider = false`, recomendado) ou importar.
6. **Falha proposital e serviço que o self-healing reinicia:** a recomendação é um estado de erro em memória no flag-service.
7. **Tamanho do cluster:** 3 × c7i-flex.large (como no plano) ou um tipo maior.
8. **Ensaiar Grafana, Prometheus e Loki no Compose** antes do cluster, para economizar horas: sim ou não.
9. **Perguntas à FIAP (Discord):** a entrega individual é aceita (REQ-OBR-41/33)? Qual a data, o horário e o canal de submissão (REQ-OBR-42)? A conta Free do New Relic substitui a conta "for education" (Q-04)?
10. **Acesso do avaliador:** tornar o repositório público após a varredura de segredos, ou conceder acesso.

## 8. Método, verificação e limitações

**Como foi feita a auditoria (2026-10-30 a 2026-10-31):**
- 9 frentes de boas práticas: as 3 camadas de Terraform e seus módulos, CI/CD, GitOps, Collector local, Compose e scripts, documentação, e consistência entre camadas com a higiene do Git;
- 6 frentes de requisitos;
- a conferência do PDF.

Ficaram fora a pasta `services/` (só lida para checar requisitos), as pastas de colaboração e os materiais de aula. Os 116 arquivos do escopo foram declarados lidos por pelo menos uma frente.

**Verificação:**
- os achados altos e críticos foram conferidos individualmente (prova e impacto);
- os demais foram conferidos em lote por um verificador cético;
- os status dos requisitos passaram por auditores que procuraram exagero e omissão.

Resultado: 84 achados confirmados, 20 parciais (mantidos com a severidade ajustada) e 2 descartados. Na frente de consistência entre camadas (15 achados), o limite de uso interrompeu o verificador. Conferi pessoalmente 7 deles: os 3 graves e mais 4. Os outros 8 estão marcados como **não verificados** no Apêndice A.

**Limitações:**
- Docker estava parado, então nenhum contêiner foi executado nesta auditoria; vale a evidência registrada em 2026-10-27.
- O pylint não foi executado (CIC-02 é estimativa).
- Não houve consulta à AWS. Ficaram sem verificação a descrição real da policy (TFB-02), os créditos e a cota de vCPU.
- O GitHub não foi consultado ao vivo; vale a evidência de 2026-10-28.
- Algumas frentes rodaram duas vezes por causa de interrupções. Os achados equivalentes foram unificados, com a rodada mais recente como base e os achados exclusivos da anterior acrescentados.

## Apêndice A — Todos os achados mantidos (112)

Ordem: severidade final, depois id. Prefixos: TFB/TFC/TFK = Terraform base/cluster/k8s; CIC = CI/CD; GIT = GitOps; OBS = observabilidade local; CMP = Compose e configuração da raiz; DOC = documentação; XCL = consistência entre camadas. "Severidade original" aparece quando a verificação a ajustou.

### Alta (6)

- **CIC-01 — Workflow de self-healing (repository_dispatch) inexistente**  
  `.github/workflows:0` · verificação: confirmado · bloqueia a entrega · esforço G · já conhecido: REVISAO_GERAL_FASE4_2026-10-28_v01.md (REQ-OBR-19/22 pendentes) e REVISAO_GERAL_ · requisitos: REQ-OBR-19, REQ-OBR-22, REQ-OBR-31, REQ-OBR-38, REQ-OBR-23  
  **Problema:** REQ-OBR-19/22/31/38 exigem uma automação que reaja ao alerta, junto com o print da execução e a demonstração em vídeo. O plano (07-resposta.html) descreve self-healing.yml, mas ainda faltam o arquivo, a credencial para o EKS e o token de disparo. Também há restrições que afetam o prazo: um repository_dispatch só roda o workflow que está na branch padrão (main), e hoje a origin/main só contém o PDF.  
  **Recomendação:** Criar .github/workflows/self-healing.yml com estes pontos: (1) gatilho 'on: repository_dispatch: types: [self-heal]', com o arquivo publicado na main antes do ensaio; (2) passar client_payload ao job por env, sem interpolar ${{ github.event.client_payload.* }} dentro de run (isso abre script injection), sair sem ação quando status != firing e validar o serviço com regex e allowlist fixa (por exemplo, flag-service e evaluation-service) e namespace fixo togglemaster; (3) 'concurrency: group: self-heal-<serviço>, cancel-in-progress: false', cooldown pela anotação de última tentativa no Deployment (ex.: 10 min), uma tentativa só e timeout-minutes curto; (4) 'permissions: id-token: write, contents: read' e uma role própria, separada da role do CI. Usar 'environment: self-healing' no job para o sub do token ficar diferente do sub do CI (…:environment:self-healing; conferir o formato exato com o mesmo GET do subject imutável). A role precisa só de eks:DescribeCluster, mais aws_eks_access_entry e RBAC limitado ao namespace (get/patch em deployments, get/list/watch em replicasets/pods), já que o modo de autenticação API_AND_CONFIG_MAP aceita access entries; (5) passos aws eks update-kubeconfig, kubectl rollout restart e rollout status --timeout, depois publicar o resultado no Slack com o webhook guardado em GitHub Secret; (6) para o Grafana chamar POST /repos/{owner}/{repo}/dispatches, usar um fine-grained PAT ou GitHub App limitado a este repositório, com expiração curta, guardado só em Secret do cluster ou do Grafana, nunca no Git. Conferir na documentação oficial a permissão mínima do endpoint e se a organização exige aprovação de PAT.  
  **Verificação:** confirmado; impacto procede — A evidência confere: o workflow não existe e a role do CI não tem permissão no EKS. Também não há access entry nem token de disparo. Sem isso, REQ-OBR-19/31 (automação reagindo ao alerta, com demonstração no vídeo) fica sem atendimento, então o achado bloqueia a entrega. A ausência em si é uma etapa prevista no plano (07-resposta) e um ponto já conhecido (I-05). O plano já trazia filtro de status, allowlist, cooldown e role própria. Os pontos novos de fato são quatr…

- **GIT-01 — Stack de observabilidade (Collector, Prometheus, Loki, Grafana) ausente do GitOps**  
  `gitops/base/kustomization.yaml:0` · verificação: parcial · severidade original: crítica · bloqueia a entrega · esforço G · já conhecido: F-019; REVISAO_GERAL_INFRA I-01 · requisitos: REQ-OBR-06, REQ-OBR-07, REQ-OBR-08, REQ-OBR-09, REQ-OBR-10, REQ-OBR-11, REQ-OBR-20, REQ-OBR-25  
  **Problema:** O enunciado exige Helm charts da stack no repositório GitOps e o IaC/GitOps atualizado com o OTel Collector. Hoje a única Application do ArgoCD aponta para gitops/overlays/prod, que não tem nada da stack. Não há onde declarar charts: o helmCharts do Kustomize exige --enable-helm no ArgoCD, que não está configurado. Faltam também no contrato de Secrets as credenciais que a stack vai precisar (license key do New Relic para o Collector, routing key do PagerDuty, webhook do Slack e token do repository_dispatch).  
  **Recomendação:** Criar gitops/platform/ (ou gitops/observability/) com Applications do ArgoCD multi-source (chart oficial + values versionados no repo) para opentelemetry-collector, kube-prometheus-stack (ou só Prometheus + Grafana), Loki e o agente de logs (Alloy ou Promtail). Aplicar o padrão app-of-apps a partir de uma Application raiz declarada em terraform/k8s/argocd.tf. Fixar as versões dos charts, limitar retenção e réplicas (1) e usar storage gp3 pequeno. Estender o SECRETS-CONTRATO.md com os Secrets da stack, criados pelo Terraform e nunca versionados. Dimensionar os nós junto com a stack (ver I-07).  
  **Verificação:** parcial; impacto procede — A lacuna existe e bloqueia a entrega: o enunciado pede os Helm charts no repositório GitOps (REQ-OBR-06 e seguintes), e hoje nada da stack está declarado. Mesmo assim o achado está exagerado em dois pontos. Primeiro, a frase "não há onde declarar charts" está errada. Uma Application do ArgoCD com source Helm (chart + targetRevision + values, single ou multi-source) funciona nativamente, sem --enable-helm. Essa flag só é necessária para usar helmCharts dentro do Kustomi…

- **GIT-02 — Variáveis OTEL_* ausentes nos ConfigMaps e Deployments: o SDK não liga no cluster**  
  `gitops/base/evaluation-service/configmap.yaml:0` · verificação: confirmado · bloqueia a entrega · esforço P · já conhecido: F-019; REVISAO_GERAL_INFRA I-02 · requisitos: REQ-OBR-11, REQ-OBR-14, REQ-OBR-15, REQ-OBR-20, REQ-OBR-27, REQ-OBR-36  
  **Problema:** As imagens instrumentadas sobem sem endpoint e não exportam nada. Sem traces no APM não há trace distribuído nem Service Map no vídeo e no relatório.  
  **Recomendação:** Acrescentar aos 5 ConfigMaps OTEL_EXPORTER_OTLP_ENDPOINT=http://<collector>.<ns-observabilidade>.svc:4318, OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf e OTEL_SERVICE_NAME=<svc>, além de OTEL_RESOURCE_ATTRIBUTES (deployment.environment.name=prod e k8s.namespace.name). Usar a downward API para k8s.pod.name no env do Deployment. Espelhar o docker-compose.otel.yaml. Garantir que o rollout ocorra depois da mudança (ver G-06).  
  **Verificação:** confirmado; impacto procede — A evidência existe e o efeito é real: com o render atual do prod, os 5 serviços sobem no EKS com o tracer noop e não mandam traces ao Collector nem ao New Relic. Sem isso não há trace distribuído, Service Map nem métricas de APM para o vídeo e o relatório (REQ-OBR-11/14/15/20). Há uma imprecisão pequena: OTEL_SERVICE_NAME não é obrigatória. Os serviços Go (telemetry.go:30-33) e Python (telemetry.py:59) caem num nome padrão quando ela falta. O bloqueio vem só da ausê…

- **OBS-01 — Collector só tem pipeline de traces com saída local; faltam métricas, logs, exporters reais e versão para o cluster**  
  `observability/otel-collector-local.yaml:56` · verificação: confirmado · bloqueia a entrega · esforço G · já conhecido: F-019; REVISAO_GERAL_FASE4_2026-10-28_v01.md:93 (REQ-OBR-11 Parcial); REVISAO_GE · requisitos: REQ-OBR-06, REQ-OBR-07, REQ-OBR-08, REQ-OBR-10, REQ-OBR-11, REQ-OBR-14, REQ-OBR-15, REQ-OBR-20  
  **Problema:** O REQ-OBR-11 exige que o Collector receba, processe e exporte métricas, logs e traces para Prometheus, Loki e APM. A configuração atual prova apenas o recebimento e o tratamento de traces, com destino de arquivo/debug. Como os serviços não emitem métricas OTLP, a taxa de requisições do dashboard (REQ-OBR-10b) depende inteiramente do conector spanmetrics no gateway, e os logs dependem do filelog no agent. Nenhum desses componentes existe ainda em código. Também não há exporter New Relic (otlp.nr-data.net com header api-key), por isso REQ-OBR-14/15 continuam sem prova.  
  **Recomendação:** Criar os values do chart opentelemetry-collector em gitops/, com duas releases. (1) Agent DaemonSet com os presets logsCollection (filelog em /var/log/pods) e kubernetesAttributes, transform que extrai trace_id/span_id do JSON e exporter otlp para o gateway. (2) Gateway Deployment com 1 réplica e receiver otlp 4317/4318. Na ordem: memory_limiter, filter/health, transform/sanitize ajustado (ver OBS-02), k8sattributes e batch. Exporters: otlphttp/newrelic (endpoint https://otlp.nr-data.net, headers api-key lido de Secret via env), conector spanmetrics → pipeline metrics → prometheusremotewrite (habilitar enableRemoteWriteReceiver no kube-prometheus-stack) e logs → otlphttp para http://<loki>/otlp. Antes do cluster, validar a parte New Relic pelo Compose, acrescentando o exporter a um arquivo de override não versionado ou a uma chave lida de variável de ambiente. Reaproveitar a mesma imagem contrib fixada por digest.

- **TFK-01 — Camada k8s ainda nao tem nada das etapas E2/E3: namespace observability, Secrets de New Relic/PagerDuty/Slack/GitHub e Application de observabilidade**  
  `terraform/k8s/secrets.tf:0` · verificação: confirmado · bloqueia a entrega · esforço M · já conhecido: F-019 (stack/OTel ausentes no Kubernetes) e plano-fase4 04-plataforma.html/08-ex · requisitos: REQ-OBR-06, REQ-OBR-11, REQ-OBR-12, REQ-OBR-16, REQ-OBR-17, REQ-OBR-18, REQ-OBR-19, REQ-OBR-20, REQ-OBR-22  
  **Problema:** Sem esses objetos o Collector nao tem a license key do New Relic, o Grafana nao tem routing key do PagerDuty, webhook do Slack nem token do GitHub para o repository_dispatch, e o ArgoCD nao instala a stack a partir de gitops/observability/. Com isso a demonstracao de stack no cluster, APM, alerta, incidente, ChatOps e self-healing fica bloqueada. Prazo interno 2026-11-12.  
  **Recomendação:** Em terraform/k8s: (1) kubernetes_namespace_v1.observability; (2) variaveis sensitive (de preferencia ephemeral, ver K8S-04) com validation de valor nao vazio: newrelic_license_key, pagerduty_routing_key, slack_webhook_url, github_dispatch_token e grafana_admin_password; (3) Secrets em observability com nomes e chaves fixados em gitops/SECRETS-CONTRATO.md e consumidos pelos values dos charts (extraEnvs/secretKeyRef no Collector; grafana.admin.existingSecret, para nao ficar a senha padrao do chart); (4) kubernetes_manifest 'observability' (app of apps) com source.path gitops/observability, destination.namespace argocd, automated prune/selfHeal e syncOptions ['CreateNamespace=true','ServerSideApply=true'] desde o inicio, porque os CRDs do kube-prometheus-stack costumam falhar no apply client-side por limite de tamanho de anotacao (o plano ja cita isso como algo a testar); (5) depends_on nos Secrets e no namespace (ver K8S-05). Atualizar outputs.tf (secrets_criados) e o contrato.  
  **Verificação:** confirmado; impacto procede — A evidência existe e está descrita com precisão. A camada k8s não tem namespace observability, Secrets de New Relic/PagerDuty/Slack/GitHub nem a Application observability. Sem esses objetos não dá para demonstrar a stack no cluster, o alerta, o incidente, o ChatOps e o self-healing, que são o núcleo da Fase 4. Isso justifica severidade alta e o bloqueio da entrega. Mas não é um defeito no código existente: é trabalho pendente que já era conhecido (F-019 e etapas E2/…

- **XCL-01 — 11 dias de trabalho só na árvore local, com arquivos rastreados dependendo de arquivos não rastreados**  
  `services/flag-service/app.py:10` · verificação: confirmado (Claude) · bloqueia a entrega · esforço M · já conhecido: F-025 (Claude 2026-10-28; Codex 2026-10-30 corrigiu de 33 para 34 deleções). Nov · requisitos: REQ-OBR-20, REQ-OBR-21, REQ-OBR-22  
  **Problema:** Toda a instrumentação, os testes, a correção da trust OIDC e a documentação existem numa única cópia em disco, sem backup remoto. Um `git commit -a` ou um commit só dos arquivos modificados publicaria app.py e main.go sem telemetry.*. Isso quebraria o build das imagens e o CI, e o README ficaria com links mortos no GitHub. Um `git add -A` também levaria as 34 deleções e os artefatos grandes (T-02). REQ-OBR-20/21/22 exigem o código no repositório entregue, e o ArgoCD/CI leem o remoto.  
  **Recomendação:** Antes de 2026-11-05, com autorização do usuário: (1) resolver T-02; (2) decidir as 34 deleções (restaurar com `git restore` ou comitar a remoção com justificativa no LOG); (3) comitar na dev em lotes coesos com `git add` explícito: serviços (código + telemetry.* + tests/ + go.sum/requirements), depois observability/ + docker-compose.otel.yaml + scripts, depois terraform/modules/iam-ci, depois a documentação; (4) validar num clone limpo (`git worktree add`) rodando scripts/validate-all.sh e test-observability.sh; (5) fazer push para origin/dev, que é fast-forward (0 commits atrás).  
  **Verificação:** Conferido: app.py versionado importa telemetry.py não rastreado; origin/main tem 1 arquivo (o PDF); dev 103 commits à frente de origin/dev; último commit 3b21e65 de 2026-10-20.

### Média (39)

- **CIC-02 — Lint Python roda pylint sem as dependências e deve reprovar o código OTel (fail-under 7.0)**  
  `.github/workflows/_ci-python.yml:180` · verificação: confirmado · severidade original: alta · bloqueia a entrega · esforço P · já conhecido: Parcial: F-022 (reexecutar DevSecOps sobre os artefatos finais). O mecanismo E04 · requisitos: REQ-OBR-04, REQ-OBR-05, REQ-OBR-21  
  **Problema:** Sem os pacotes instalados, cada import de terceiro gera E0401 (import-error), e a nota do pylint pesa erro 5 vezes. As notas da Fase 3 (8,26/8,08/7,59) batem com cerca de 5 imports com erro por serviço. Com telemetry.py e tests/ versionados, ficam cerca de 20 a 28 imports com erro por serviço. Pela minha estimativa (não executei o pylint), a nota fica abaixo de 7,0. Nesse caso o job lint falha, o 'image' (needs: [build, lint, sast, sca]) é pulado e os 3 serviços Python não publicam imagem. O ArgoCD continuaria com os placeholders registry.conta-pendente.invalid. golangci-lint v2, gosec e Trivy também não rodaram sobre o código e as dependências da Fase 4.  
  **Recomendação:** No job lint, instalar as dependências do serviço antes do pylint (setup-python com cache pip e 'pip install -r requirements.txt'). Rodar antes, localmente, exatamente o comando do CI em cada serviço. Exercitar todos os gates com push em dev, que só verifica e não publica nem toca a AWS, antes do primeiro push na main. Corrigir o comentário de :226-228.  
  **Verificação:** confirmado; impacto procede — O mecanismo procede. O runner do job lint tem só flake8 e pylint, então cada import de terceiro gera E0401 (erro, peso 5 na fórmula do pylint). São cerca de 25-29 erros contra algumas centenas de statements, uma penalidade estimada de 3 a 5 pontos antes dos demais avisos. Isso torna muito provável a nota abaixo de 7,0 nos 3 serviços. Também não executei o pylint: o runtime permitido não o tem, e rodá-lo foge da lista do que é permitido. O resultado é falha do lint, …

- **CIC-03 — Jobs de build/lint/SAST/SCA herdam id-token: write e contents: write**  
  `.github/workflows/auth-service.yml:77` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** Num workflow reutilizável, job sem permissions recebe as do chamador. Assim, os jobs que rodam código de terceiros (pip install -r requirements.txt, go test, linters baixados sem versão fixa) recebem token de escrita no repositório e podem pedir token OIDC. Num push na main, o sub desse token satisfaz a trust da role. Uma dependência comprometida poderia então dar push na main, que o ArgoCD aplica, ou publicar no ECR. O comentário de _ci-go.yml:499 ('única permissão de escrita em todo o pipeline') não corresponde ao comportamento real.  
  **Recomendação:** Acrescentar 'permissions: contents: read' no topo de _ci-go.yml e _ci-python.yml, mantendo os overrides dos jobs image e gitops. Opcionalmente, mover o bloco dos chamadores para o nível do job 'ci'.  
  **Verificação:** auth-service.yml:77-83 (e os outros 4 chamadores, :76-82) declaram id-token: write e contents: write no nível do workflow. Em _ci-go.yml/_ci-python.yml só image (:335/:368) e gitops (:497/:527) têm permissions; build/lint/sast/sca (_ci-go.yml:75,127,190,246) não têm, então herdam as do chamador. Nenhum checkout usa persist-credentials: false (grep sem resultado), então o token de escrita fica em .git/config durante pip install -r requirements.txt (_ci-python.yml:116) e go test. ACTIONS_ID_TOKEN_…

- **CIC-04 — Actions de terceiros fixadas por tag móvel; só o Trivy está por SHA**  
  `.github/workflows/_ci-go.yml:88` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** O próprio comentário de _ci-go.yml:264-268 explica que tag pode ser movida e que SHA é a forma segura. A regra, porém, só foi aplicada a uma action. As actions configure-aws-credentials e amazon-ecr-login rodam no job que tem a credencial AWS, e o checkout roda no job que tem contents: write.  
  **Recomendação:** Fixar todas as actions por SHA de commit com a versão em comentário, conferindo cada SHA na página oficial de releases. Opcionalmente, ativar o Dependabot para github-actions, que gera PRs de atualização.  
  **Verificação:** A contagem de 'uses:' bate: checkout@v4 14x, setup-go@v5 3x, setup-python@v5 3x, golangci-lint-action@v9, configure-aws-credentials@v4 2x, amazon-ecr-login@v2 2x, setup-terraform@v3. Só a trivy-action está presa por SHA (_ci-go.yml:274, justificativa em :264-268). Uma ressalva: o binário do golangci-lint tem versão fixada (version: v2.13.2, _ci-go.yml:174) e o gosec também (@v2.29.0, :230); só a action em si está por tag. A maioria das actions é de mantenedor oficial, mas fixar por SHA continua …

- **CIC-05 — Sem varredura de segredos no CI; security-check.sh não cobre os segredos novos da Fase 4**  
  `scripts/security-check.sh:63` · verificação: parcial · esforço P · já conhecido: Parcial: F-029 registra que nenhum workflow chama validate-all.sh. A falta de pa · requisitos: REQ-OBR-04, REQ-OBR-17, REQ-OBR-18  
  **Problema:** A Fase 4 traz segredos que ainda não existiam: license key e API key do New Relic, URL de webhook e token do Slack, routing key do PagerDuty e o PAT ou token de App do GitHub para o repository_dispatch. Esses valores tendem a aparecer em values de charts, contact points do Grafana ou no Collector dentro de gitops/, que fica numa área versionada lida pelo ArgoCD. Hoje nada barra esse commit no pipeline. É um risco real de vazamento num repositório com várias contas SaaS.  
  **Recomendação:** Criar um job de segredos no repositório inteiro, por exemplo trivy-action (mesmo SHA) com scan-type fs, scan-ref '.', scanners secret e exit-code 1, ou gitleaks com versão fixada, disparado em PR e push. Acrescentar ao security-check.sh padrões para 'hooks.slack.com/services/', 'xox[abprs]-', 'github_pat_|ghp_', 'NRAK-' e chave de ingestão do New Relic. Para valores sem formato estável, como a routing key do PagerDuty, documentar que só entram por Secret do Kubernetes ou do GitHub.  
  **Verificação:** Conferido: nenhum workflow chama security-check.sh nem validate-all.sh (grep vazio), e as regras de scripts/security-check.sh:63-82 cobrem só AKIA, chave privada, o ID da conta da Fase 2 (<CONTA>) e três variáveis. Mas a afirmação 'nenhum outro scanner de segredos' é imprecisa. Os passos do Trivy (_ci-go.yml:274-309, :418-434 e equivalentes no Python) não definem 'scanners', então o Trivy usa o padrão vuln,secret e já procura segredos em services/<svc> e na imagem. Essa varredura só barra achado…

- **CIC-08 — Exceções do Trivy com revisão vencida (2026-10-15) e sem expiração automática**  
  `.trivyignore:58` · verificação: confirmado · esforço P · já conhecido: F-022 · requisitos: REQ-OBR-04  
  **Problema:** A data de revisão já passou, e a justificativa vale para uma versão de perl-base de setembro. Se a base mudou, as exceções podem estar inúteis ou podem esconder outra coisa. Se apareceu CRITICAL novo, o scan da imagem bloqueia a publicação no primeiro push na main.  
  **Recomendação:** Rodar o Trivy nas imagens finais antes do push na main (pode ser via CI na dev, que não publica). Remover as linhas que não se aplicam mais. Usar a sintaxe de expiração do Trivy na mesma linha ('CVE-… exp:2026-11-20'), que reativa o bloqueio sozinha depois da entrega.  
  **Verificação:** .trivyignore:58 diz 'Revisar em: 2026-10-15.' As linhas :63, :68 e :73 trazem só o ID do CVE, sem exp:. A medição de 2026-09-09 na tag v1.0.0-122174a está em :56-57. Os Dockerfiles usam python:3.12-slim sem digest (services/*/Dockerfile:6,43). Já era conhecido: F-022 (PENDENCIAS_E_PROXIMOS_PASSOS.md:68 e LOG_DE_TRABALHO.md:160). A sugestão nova é usar a expiração do Trivy na própria linha.

- **CIC-09 — CI não renderiza nem valida o GitOps (onde entrará a stack de observabilidade)**  
  `scripts/validate-all.sh:55` · verificação: confirmado · esforço P · já conhecido: F-029 · requisitos: REQ-OBR-05, REQ-OBR-20  
  **Problema:** A Fase 4 vai acrescentar charts, Collector, Prometheus/Loki/Grafana e uma nova Application em gitops/. Um erro de estrutura só apareceria no sync do ArgoCD, com o cluster ligado e cobrando cerca de US$ 0,47/h.  
  **Recomendação:** Criar um workflow leve com paths gitops/**, rodando kustomize build (e helm template, se houver charts), com permissions contents: read.  
  **Verificação:** 'kubectl kustomize gitops/overlays/prod' só aparece em scripts/validate-all.sh:55, que nenhum workflow chama. terraform-check.yml:32-33/:39-40 filtra por terraform/**, e o job gitops só roda 'kustomize edit set image' (_ci-go.yml:583). Já era conhecido: é o F-029 (auditoria-codex-2026-10-30_v01/CATALOGO_ACHADOS.md:242), com a mesma evidência e a mesma correção.

- **CMP-01 — Evidências não ignoradas: arquivo de 156 MB e ID real da conta prontos para entrar no Git**  
  `.gitignore:98` · verificação: parcial · severidade original: alta · esforço P · já conhecido: F-024 (só o jsonl de 156 MB); a exposição do ID da conta nos outros cinco arquiv · requisitos: REQ-OBR-20, REQ-OBR-42  
  **Problema:** O bloco de 00_COLAB_IA em .gitignore (linhas 98-106) ignora pastas específicas (qa-*, extracoes*, validacao-*), mas não a etapas8-9-2026-10-28_v01 nem as demais pastas novas. Todo o trabalho desde 3b21e65 está sem commit (F-025). Com o commit em vista, um 'git add -A' ou 'git add 00_COLAB_IA' inclui (1) um arquivo de 156 MB, e o GitHub recusa arquivos acima de 100 MB, o que trava o push de toda a entrega; (2) cinco arquivos com o ID da conta nova em ARNs de role/policy/OIDC e no registry. O CLAUDE.md proíbe levar estado e ARNs ao Git. Remover arquivo grande do histórico depois exige reescrever o histórico. A gravação do vídeo (REQ-OBR-24) pode criar outro arquivo grande dentro do repositório.  
  **Recomendação:** Antes de qualquer commit, ignorar a pasta inteira de evidências locais (por exemplo, '00_COLAB_IA/02_TRABALHO/etapas*/' e '*.jsonl') ou mover o jsonl para fora do repositório. Acrescentar '*.mp4', '*.mkv' e '*.mov' para a gravação do vídeo. Mascarar <CONTA> nos arquivos de evidência que forem versionados. Validar com 'git status --porcelain --untracked-files=all' e 'git ls-files -o --exclude-standard | xargs du -b | sort -n | tail'. Fazer staging só arquivo a arquivo, como o próprio GUIA recomenda.  
  **Verificação:** parcial; impacto procede — A evidência existe e o risco é real enquanto o trabalho estiver sem commit (F-025): um `git add -A` levaria junto o arquivo de 156 MB, e o GitHub recusa arquivos acima de 100 MB. O achado exagera em três pontos. (1) Atribui ao CLAUDE.md uma proibição de levar ARNs ao Git, mas a regra da linha 9 vale para a conta anterior. A regra geral proíbe 'estados ou segredos', e o ID de conta AWS não é segredo para a própria AWS. Expor o ID num repositório público é um vazamento d…

- **CMP-03 — SECURITY.md descreve a trust OIDC antiga (qualquer branch/PR)**  
  `SECURITY.md:21` · verificação: confirmado · esforço P · já conhecido: Decorre de F-023 (correção da trust); o impacto no SECURITY.md não estava regist · requisitos: REQ-OBR-04  
  **Problema:** Com a correção do F-023 (árvore de trabalho), a trust aceita só o subject imutável da branch main via StringEquals. PRs e outras branches passam a ser recusados pela própria AWS. O documento de segurança, que o avaliador lê, afirma o contrário e subestima um controle que existe. Também omite que a role e a policy foram criadas à mão na conta nova e só depois serão importadas.  
  **Recomendação:** Reescrever o parágrafo: a trust exige aud sts.amazonaws.com e o sub 'repo:<owner>@<owner_id>/<repo>@<repo_id>:ref:refs/heads/main' (IDs imutáveis); jobs de PR/dev que não publicam não assumem a role. Citar terraform/modules/iam-ci/main.tf como fonte.  
  **Verificação:** SECURITY.md:20-23 diz que a trust 'aceita qualquer branch ou pull request'. Já terraform/modules/iam-ci/main.tf na árvore de trabalho (alterado e não comitado, segundo o git status) monta na linha 81 o sub com IDs imutáveis e 'ref:refs/heads/${var.github_deploy_branch}', e as linhas 139-148 exigem StringEquals no sub e no aud. Era conhecido em parte: PENDENCIAS_E_PROXIMOS_PASSOS.md:21 pede 'documentação coerente' na etapa 9, mas não cita o SECURITY.md. O documento erra para o lado conservador, m…

- **DOC-01 — Não existe relatório da Fase 4; docs/RELATORIO_DE_ENTREGA.md é o da Fase 3 (Grupo 203)**  
  `docs/RELATORIO_DE_ENTREGA.md:3` · verificação: parcial · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: REVISAO_GERAL_FASE4_2026-10-28_v01.md (REQ-OBR-32/34 'relatório PDF final da Fas · requisitos: REQ-OBR-32, REQ-OBR-33, REQ-OBR-34, REQ-OBR-35, REQ-OBR-36, REQ-OBR-37, REQ-OBR-38, REQ-OBR-39, REQ-OBR-40  
  **Problema:** O enunciado exige relatório PDF com nomes/RMs/usernames, links de código e vídeo, 4 prints (dashboard Grafana, trace no APM, notificação ChatOps, log do Self-Healing), explicação da arquitetura OTel e justificativa Datadog x New Relic e OpsGenie x PagerDuty. Nenhum documento do escopo tem essa estrutura nem rascunho das justificativas. A única decisão registrada é uma linha em 00_COLAB_IA/DECISOES.md:73. Faltando 17 dias e com trabalho individual, deixar o relatório inteiro para depois da demonstração aumenta o risco de perder itens que descontam nota.  
  **Recomendação:** Criar já um esqueleto versionado (por exemplo docs/RELATORIO_ENTREGA_FASE4.md, para exportar em PDF), preservando o da Fase 3. Ele deve ter: identificação individual (nome, RM e usuário GitHub, depois de resolver a Q-13 sobre a plataforma do username), links do repo 04 e do vídeo, 4 seções de print com legenda e data, uma seção OTel (agents/gateway, receivers→processors→exporters, spanmetrics, o que vai a Prometheus/Loki/New Relic) e uma seção de justificativas (New Relic: conta gratuita e OTLP nativo; PagerDuty: OpsGenie fora de venda desde 2025-06-04, F-008). Incluir um checklist REQ-OBR-32..40 e preencher os prints durante o ensaio.  
  **Verificação:** parcial; impacto procede — O fato central se confirma: não existe relatório nem esqueleto da Fase 4, e REQ-OBR-32..40 estão todos pendentes. O achado, porém, exagera em três pontos. (1) Insinua que docs/RELATORIO_DE_ENTREGA.md pode ser tomado como relatório atual, mas a linha 1 o marca como referência histórica da Fase 3, ou seja, a preservação já é deliberada. (2) Diz que as justificativas não têm rascunho, mas DECISOES.md:72-74 já traz a justificativa de PagerDuty x OpsGenie (venda encerrada e…

- **DOC-02 — Não há roteiro de implantação vigente para a conta nova; o único roteiro (GUIA) é da Fase 3 e tem comandos incompatíveis com o código atual**  
  `docs/GUIA_DE_REPRODUCAO.md:291` · verificação: parcial · severidade original: alta · bloqueia a entrega · esforço G · já conhecido: REVISAO_GERAL_INFRA_2026-10-28_v01.md:68 ('produzir/adaptar um runbook vigente d · requisitos: REQ-OBR-01, REQ-OBR-03, REQ-OBR-05, REQ-OBR-23, REQ-OBR-25  
  **Problema:** O GUIA se declara histórico (linha 1), mas é o único lugar com os passos que o deploy da Fase 4 ainda precisa: k8s em duas etapas (-target=helm_release.argocd), schemas do RDS, troca do SERVICE_API_KEY, REDIS_URL no overlay, checagem de sobras e ordem de destroy. Quem seguir esses passos na conta nova vai falhar no init (falta o bucket no backend), apontar para chaves de estado erradas ou criar o bucket fora do namespace regional (-an) que o usuário já criou. O marcador [INCERTO] do -an continua, embora o sufixo identifique o namespace regional da conta (lançado pela AWS em 2026-03, segundo o contexto da tarefa; não reconferido na documentação oficial nesta revisão). terraform/README.md:65 remete o leitor a esse guia como 'base técnica'.  
  **Recomendação:** Escrever um runbook da Fase 4 (docs/RUNBOOK_FASE4.md ou nova versão do guia, preservando o original) com estes passos: (1) backend.hcl por camada e 'init -backend-config=backend.hcl'; (2) terraform.tfvars com expected_aws_account_id, state_bucket, state_region e as variáveis OIDC; (3) reconciliação ou import dos recursos criados à mão (ver DOC-A03); (4) a ordem base → imagens → cluster → k8s A/B; (5) schemas e chave de serviço; (6) instalação da stack de observabilidade; (7) destroy e checagem de sobras com phase=4. Explicar o sufixo -an como namespace regional da conta, citando a fonte oficial com data, e trocar todo ID antigo por <CONTA>.  
  **Verificação:** parcial; impacto procede — A evidência confere, mas o risco descrito está exagerado. O GUIA se declara histórico já na linha 1 e proíbe executar os comandos antigos. Os parâmetros que o achado diz faltar já estão em terraform/README.md: init com -backend-config, chaves phase4/prod/*, as variáveis expected_aws_account_id e state_*, e a tag phase=4. Por isso, quem seguir a documentação vigente não falha no init nem usa a chave errada, e 'quem seguir esses passos vai falhar' só vale para quem ignor…

- **DOC-03 — terraform/README.md não orienta a reconciliação com ECR, OIDC, role e policy criados à mão: o apply da base vai colidir**  
  `terraform/README.md:31` · verificação: confirmado · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: F-023; PENDENCIAS_E_PROXIMOS_PASSOS.md:36 e :61 ('Inventariar/importar recursos  · requisitos: REQ-OBR-03, REQ-OBR-04, REQ-OBR-05  
  **Problema:** O usuário já criou à mão os 5 repositórios ECR, o provedor OIDC, a role togglemaster-github-actions e a policy togglemaster-ci-ecr-push, com os mesmos nomes que a camada base declara. Sem import ou parametrização, o primeiro apply para com RepositoryAlreadyExists/EntityAlreadyExists, o que a própria Tabela de armadilhas do GUIA (:695) descreve. Se o operador resolver apagando os recursos, perde a trust OIDC que já funciona. O README também não documenta github_repository_owner_id, github_repository_id e github_deploy_branch (variables.tf:189-219), que agora definem o subject da trust. A linha :40 cita só github_repository.  
  **Recomendação:** Acrescentar ao terraform/README.md uma seção 'Recursos criados manualmente na conta nova' com o inventário (5 ECR, OIDC, role, policy e attachment) e a estratégia escolhida: blocos import {} versionados com IDs vindos de variáveis/tfvars (sem ID de conta no Git), ou import manual com terraform plan conferindo '0 to destroy' e nenhuma substituição da trust. Instruir create_github_oidc_provider=false. Documentar as três variáveis OIDC e dizer que o subject deve coincidir com o da role manual (F-023).  
  **Verificação:** confirmado; impacto procede — A evidência existe como descrita. O terraform/README.md é anterior aos recursos manuais e não dá orientação de reconciliação. O exemplo de tfvars ainda manda criar o provedor OIDC. As três variáveis que formam o subject da trust não aparecem no README. Os nomes da role e da policy coincidem com os recursos criados à mão. Não há blocos import. Então um apply ingênuo colidiria com EntityAlreadyExists. Para os 5 ECR, a colisão depende de os nomes manuais coincidirem co…

- **DOC-04 — Trial do PagerDuty termina antes da meta interna e da entrega, e isso não aparece no README nem no plano**  
  `README.md:25` · verificação: parcial · severidade original: alta · esforço P · já conhecido: PENDENCIAS_E_PROXIMOS_PASSOS.md:113 (risco registrado só no backlog, não nos doc · requisitos: REQ-OBR-17, REQ-OBR-30, REQ-OBR-37, REQ-OBR-24  
  **Problema:** A integração Grafana → PagerDuty depende da recepção de eventos. Se o plano Free não incluir Events depois do trial, a abertura automática do incidente pode deixar de funcionar depois de cerca de 2026-11-11, antes da meta interna de 2026-11-12. REQ-OBR-17/30/37 dependem disso. O documento de situação (README) diz que vídeo e relatório virão 'após a demonstração', sem esse prazo duro.  
  **Recomendação:** No README (seção de situação) e no plano, registrar a data limite de cerca de 2026-11-10 para gravar alerta → PagerDuty → Slack → Self-Healing e capturar os prints 3 e 4, citando a fonte (página de preços consultada, com data). Antecipar no cronograma a etapa de incidentes, ou gravar esse trecho do vídeo separadamente. Conferir na conta a data exata do fim do trial.  
  **Verificação:** parcial; impacto procede — A evidência existe e o risco de agenda é real. A partir de cerca de 2026-11-11, a prova de alerta → PagerDuty (REQ-OBR-17/30/37) e os prints dependentes podem ficar impossíveis de produzir, antes da meta interna e da entrega. Hoje nada no plano ou no cronograma antecipa E4 para dentro do trial, e E4 depende de E2/E3 (cluster, stack), que ainda não começaram. O achado, porém, exagera em dois pontos. Primeiro, o risco já é conhecido e foi analisado com fonte e data no LO…

- **DOC-05 — README raiz aponta para artefatos da Fase 4 que não estão no Git (observability/, docker-compose.otel.yaml, test-observability.sh e relatórios)**  
  `README.md:183` · verificação: confirmado · esforço P · já conhecido: F-025 (trabalho desde 3b21e65 não comitado) e F-024 (arquivo de 156 MB) · requisitos: REQ-OBR-20, REQ-OBR-21  
  **Problema:** O README descreve como aprovada a instrumentação local (README.md:5, :181), mas o runbook, o Compose do Collector e o script de teste existem só na árvore de trabalho. Para quem clonar o repositório, e para o avaliador, esses links quebram, e REQ-OBR-20/21 dependem de o código estar no repositório. Uma perda local apagaria a evidência. Existe ainda o arquivo de 156 MB não ignorado (F-024): um 'git add -A' faria o push ser recusado.  
  **Recomendação:** Quando o usuário autorizar o commit, adicionar ao .gitignore o diretório etapas8-9-*/terraform/offline-test.jsonl (ou o padrão *.jsonl de trabalho) e comitar na dev, por caminho explícito, observability/, docker-compose.otel.yaml, scripts/test-observability.sh e scripts/integration/test-traces.py. Decidir quais relatórios de 02_TRABALHO serão versionados. Os que ficarem locais não devem ser linkados do README público; nesse caso, citar só o nome e a data.  
  **Verificação:** README.md:183-186 linka observability/README.md e relatórios de 00_COLAB_IA/02_TRABALHO, e README.md:178 cita scripts/test-observability.sh. git status mostra '?? observability/', '?? docker-compose.otel.yaml', '?? scripts/test-observability.sh' e '?? scripts/integration/test-traces.py'. git ls-files não lista nenhum desses itens, e os relatórios PASSO1/PASSO2/RESULTADO aparecem como '??'. git check-ignore no offline-test.jsonl retornou 1 (o arquivo não está ignorado). Também estão fora do Git o…

- **DOC-06 — README raiz e terraform/README.md descrevem um estado da conta AWS já superado**  
  `terraform/README.md:19` · verificação: confirmado · esforço P · já conhecido: LOG_DE_TRABALHO.md:8 aponta backlog desatualizado sobre F-023; a defasagem dos R · requisitos: REQ-OBR-03, REQ-OBR-23  
  **Problema:** Bucket de estado (namespace -an, versionado, só TLS), ECR, OIDC, role/policy e repository variables já existem, por relato do usuário. Os dois documentos de destino continuam dizendo que nada foi feito. A contradição com o backlog faz o operador repetir passos, como recriar o bucket, ou ignorar a reconciliação necessária. O README também deixa de citar a escolha do PagerDuty em :39 ('As escolhas New Relic, Slack e GitHub Actions').  
  **Recomendação:** Atualizar a data e o TL;DR dos dois arquivos para: conta nova existe (sem ID); bucket criado à mão no namespace regional; recursos IAM/ECR manuais a reconciliar; Variables configuradas por relato e CI remoto ainda não testado; terraform.tfvars ainda inexistentes; nenhum init com backend, plan ou apply. Marcar o que é relato do usuário e o que foi verificado. Incluir PagerDuty em README.md:39.  
  **Verificação:** terraform/README.md:3 diz 'A nova conta AWS ainda não foi informada'. Em :5 a data é 2026-10-20 e :19 diz 'em um bucket novo. Nenhum bootstrap foi executado'. README.md:210 diz 'Quando a conta estiver pronta, configurar estas repository variables'. Isso contradiz PENDENCIAS:36 (provedor, policy, role e Variables feitos, segundo relato do usuário) e PENDENCIAS:113-114 (bucket confirmado, backend.hcl criados). Um ajuste: README.md:39 omite o PagerDuty, mas o README o cita em :37, :55, :60 e :123, …

- **DOC-08 — Trabalho individual contradiz REQ-OBR-41 (grupo), e não há registro da confirmação do tutor**  
  `docs/requisitos/README.md:90` · verificação: confirmado · esforço P · já conhecido: REVISAO_GERAL_FASE4_2026-10-28_v01.md:123 e REVISAO_GERAL_DOCUMENTACAO_2026-10-2 · requisitos: REQ-OBR-41, REQ-OBR-33  
  **Problema:** O relatório herdado sugere um grupo de cinco pessoas, enquanto a Fase 4 é feita só pelo usuário. Sem a resposta do tutor à Q-03 registrada, o relatório pode sair com a composição errada ou sofrer desconto por não ser em grupo.  
  **Recomendação:** Pedir ao tutor/FIAP a confirmação da entrega individual e registrar a resposta com data em DECISOES e no relatório da Fase 4. Não copiar a tabela de participantes da Fase 3.  
  **Verificação:** docs/requisitos/README.md:90 tem REQ-OBR-41 'Desenvolver em grupo' com o marcador [INCERTO]. :188 mantém a Q-03 aberta. DECISOES.md:73 e :79 registram 'Implementação solo'. RELATORIO_DE_ENTREGA.md:9-15 lista cinco integrantes da Fase 3. Não há registro da resposta do tutor. O ponto já era conhecido (REVISAO_GERAL_FASE4 e REVISAO_GERAL_DOCUMENTACAO, Q-03).

- **GIT-03 — Overlay prod inteiro em sentinelas, main sem gitops/ e bootstrap das 5 imagens sem procedimento**  
  `gitops/overlays/prod/kustomization.yaml:65` · verificação: parcial · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: REVISAO_GERAL_INFRA I-03 (sentinelas); main sem gitops citado em gitops/README.m · requisitos: REQ-OBR-05, REQ-OBR-23, REQ-OBR-25  
  **Problema:** As sentinelas são intencionais, mas qualquer sync antes da troca deixa todos os pods em ImagePullBackOff, e o analytics e o evaluation falham no IRSA. Além disso: (1) a Application tem sync automático e observa a main, que ainda não tem gitops/, então o primeiro apply da camada k8s antes da publicação deixa a Application em erro de path; (2) cada pipeline só atualiza a própria imagem, e os outros 4 serviços continuam com a sentinela até que cada pipeline rode na main. O comentário proíbe a edição manual, que é justamente o caminho óbvio para o bootstrap.  
  **Recomendação:** Antes do apply da camada k8s: publicar as 5 imagens (workflow_dispatch dos 5 pipelines ou um push que toque nos 5) e substituir de uma vez imagens, ARNs IRSA, SQS e Redis pelos outputs do Terraform. Validar com 'kubectl kustomize ... | grep -c conta-pendente' igual a 0 como check de CI ou pré-sync. Documentar no gitops/README que a primeira carga das tags pode ser feita à mão (ou por um script) e ajustar o comentário das linhas 56-57. Avaliar começar a Application com sync manual até a primeira sincronização limpa.  
  **Verificação:** parcial; impacto procede — A evidência confere, mas o essencial já era conhecido. As sentinelas são uma decisão consciente (DECISOES:121). O ImagePullBackOff e a falha de IRSA só aparecem se alguém sincronizar antes da troca, e o gitops/README:3 proíbe isso. A troca de todos os marcadores também já é pendência registrada (I-03, PENDENCIAS:202). Pontos novos e válidos: - Não existe procedimento nem check automático que confirme zero 'conta-pendente' no render antes do primeiro sync. - O comentári…

- **GIT-04 — ArgoCD (selfHeal) e HPA disputam spec.replicas do evaluation e do analytics**  
  `gitops/base/evaluation-service/deployment.yaml:26` · verificação: confirmado · esforço P · já conhecido: F-027 · requisitos: REQ-OBR-01, REQ-OBR-05  
  **Problema:** Quando o HPA sobe para 2, o ArgoCD vê drift e volta para 1. A réplica oscila durante a demonstração de carga ou o self-healing, e o card do ArgoCD fica OutOfSync no vídeo.  
  **Recomendação:** Remover 'replicas' dos dois Deployments com HPA (o HPA passa a ser o dono) ou configurar ignoreDifferences em /spec/replicas só para esses dois Deployments, com syncOptions RespectIgnoreDifferences=true.  
  **Verificação:** Já conhecido (F-027 em 00_COLAB_IA/02_TRABALHO/auditoria-codex-2026-10-30_v01/CATALOGO_ACHADOS.md:17,196). Conferido: gitops/base/evaluation-service/deployment.yaml:26 e analytics-service/deployment.yaml:24 com 'replicas: 1', HPA nos dois; terraform/k8s/argocd.tf:316-333 com automated prune=true/selfHeal=true e só 'CreateNamespace=true' em syncOptions, sem ignoreDifferences. Quando o HPA escalar para 2, o diff de spec.replicas deixa a Application OutOfSync e o selfHeal reverte. Média está bem ca…

- **GIT-14 — Manifests GitOps não são validados em nenhum workflow, embora o script diga que são**  
  `scripts/validate-all.sh:57` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04, REQ-OBR-05, REQ-OBR-20  
  **Problema:** Uma alteração em gitops/ (OTEL_*, charts e values da stack, patches com outputs reais) chega à main sem render nem validação de schema, e o primeiro a descobrir um YAML inválido é o ArgoCD no cluster, com custo por hora ligado e prazo curto. O próprio job GitOps comita a tag sem renderizar o overlay depois do edit.  
  **Recomendação:** Criar um workflow leve (on: push/pull_request, paths: gitops/**) que rode kustomize build gitops/overlays/prod, valide com kubeconform -strict -ignore-missing-schemas (versão fixa), renderize os charts da stack (helm template com versões fixas) e falhe se houver sentinelas quando a branch for main. Acrescentar o mesmo render ao job GitOps antes do commit. Corrigir a mensagem do validate-all.sh.  
  **Verificação:** Já conhecido (F-029 em CATALOGO_ACHADOS.md:19). Conferido: scripts/validate-all.sh:57 promete 'render do Kustomize sera feito no CI', mas nos workflows o kustomize aparece só como 'kustomize edit set image' (_ci-go.yml:583), seguido de git diff e commit sem build (_ci-go.yml:575-600). O terraform-check.yml é filtrado por paths. A mensagem enganosa do script é a parte nova.

- **OBS-02 — Sanitização provada localmente não está no desenho do gateway e, se copiada sem ajuste, apaga os atributos k8s.***  
  `observability/otel-collector-local.yaml:33` · verificação: confirmado · esforço M · já conhecido: Parcial: aviso genérico em observability/README.md:63; a omissão no plano 06-tel · requisitos: REQ-OBR-11, REQ-OBR-14, REQ-OBR-15  
  **Problema:** O plano do gateway omite filter/health e transform/sanitize. A própria suíte local trata como vazamento a presença de user_id, flag e chave nos spans (test-traces.py:216), e o README:63 avisa que o destino futuro não fica seguro automaticamente. Sem o processor, URL/query (flag_name e user_id de /evaluate), mensagens de exceção e eventuais atributos de header podem chegar ao New Relic. Se o mesmo transform for copiado depois de k8sattributes, o keep_keys de resource remove k8s.namespace.name, k8s.pod.name e outros atributos, e o Grafana/New Relic perdem o contexto de pod e namespace. Também remove service.instance.id. A conclusão de que haveria vazamento é inferida das asserções do teste e não foi medida sem o processor.  
  **Recomendação:** No values do gateway, incluir filter/health e transform/sanitize antes do batch, com error_mode: ignore. Acrescentar à allowlist de resource os atributos k8s.namespace.name, k8s.pod.name, k8s.deployment.name, k8s.node.name e service.instance.id, ou executar k8sattributes depois do transform. Registrar a ordem no plano v03. Repetir a sonda assert_privacy_processor contra o gateway (por port-forward em 4318) antes de ligar o exporter New Relic. Para logs enviados ao Loki/New Relic, avaliar um transform equivalente com log_statements.

- **OBS-03 — Toda a observabilidade local (overlay, Collector, README e testes) está fora do Git**  
  `docker-compose.otel.yaml:0` · verificação: confirmado · severidade original: alta · bloqueia a entrega · esforço P · já conhecido: F-025 · requisitos: REQ-OBR-13, REQ-OBR-20  
  **Problema:** O único trabalho de OTel concluído, que comprova REQ-OBR-13 e prepara REQ-OBR-11/20, existe apenas no disco local. Uma limpeza do working tree, um checkout errado ou a perda da máquina apagariam o trabalho. Além disso, a entrega exige que o código esteja no repositório.  
  **Recomendação:** Fazer um commit na dev, com autorização do usuário, agrupando overlay, Collector, README e testes junto com a instrumentação dos serviços. Antes, conferir que nada de qa-otel/ entra (já coberto por .gitignore:101).

- **TFB-01 — Sem blocos import nem procedimento documentado para os recursos criados à mão: o primeiro apply com estado vazio falha no meio**  
  `terraform/main.tf:0` · verificação: confirmado · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: Necessidade de importar já registrada (LOG 2026-10-28, handoff P-013; PARECER_AW · requisitos: REQ-OBR-03, REQ-OBR-04, REQ-OBR-05  
  **Problema:** Os nomes batem, mas o estado novo está vazio e não há blocos import nem roteiro no README. Um plan sem import propõe criar os 5 aws_ecr_repository, a role, a policy, o attachment e, com create_github_oidc_provider=true, o provedor OIDC. No apply, a VPC (e o NAT, se ligado) seria criada e a execução pararia com RepositoryAlreadyExistsException ou EntityAlreadyExists, deixando um estado parcial que cobra enquanto o problema não é resolvido. Nada seria destruído, porque o Terraform não conhece esses recursos. A implantação fica bloqueada até a reconciliação.  
  **Recomendação:** Criar terraform/imports.tf com: import { for_each = toset(var.services); to = module.ecr.aws_ecr_repository.this[each.key]; id = "${each.key}-service" }; import da role (id = "togglemaster-github-actions"); da policy (id = "arn:aws:iam::${var.expected_aws_account_id}:policy/togglemaster-ci-ecr-push"); do attachment (id no formato "<role>/<policy-arn>", conferir na doc do provider 6.62); e do provedor OIDC só se a decisão for ser dono dele (ver TF-BASE-03). Rodar o plan e aceitar somente '0 to destroy' e nenhum 'forces replacement'. As 5 aws_ecr_lifecycle_policy aparecerão como criações, o que é esperado porque estão ausentes na conta. Ajustes in-place esperados: tags de default_tags, force_delete e Sid da trust. Documentar o passo no terraform/README.md.  
  **Verificação:** confirmado; impacto procede — A evidência existe e está correta. O estado é novo e vazio, e os nomes coincidem com os recursos criados à mão. Por isso, um apply sem import falharia com RepositoryAlreadyExists ou EntityAlreadyExists depois de criar outros recursos, como a VPC e o NAT se estiver ligado. Ficaria um estado parcial a reconciliar. O próprio achado reconhece que nada seria destruído. Rebaixo de alta para média por três motivos. Primeiro, a necessidade de importar já está registrada nos…

- **TFB-02 — A description da aws_iam_policy força recriação: depois do import, o plan provavelmente destrói e recria a policy e o attachment**  
  `terraform/modules/iam-ci/main.tf:212` · verificação: confirmado · severidade original: alta · esforço P · requisitos: REQ-OBR-03, REQ-OBR-04  
  **Problema:** A policy togglemaster-ci-ecr-push foi criada no console seguindo um guia que não pede description, então provavelmente está vazia ou diferente. Depois do import, essa diferença aparece como 'forces replacement'. A policy_arn passa a 'known after apply' e o attachment também é substituído. O CI perde a permissão de push durante o apply, e o resultado contraria a regra de não recriar o que já existe. A role não tem esse problema, porque a description dela é atualizada in-place.  
  **Recomendação:** Antes do plan, o usuário lê a description real com uma consulta somente leitura (aws iam get-policy --policy-arn <arn> --query Policy.Description). Se vier vazia, remover o atributo description do recurso; se vier preenchida, copiar o texto exato. Outra opção é lifecycle { ignore_changes = [description] } em aws_iam_policy.ecr_push. Rejeitar qualquer plan que mostre 'must be replaced' nos recursos importados.  
  **Verificação:** confirmado; impacto procede — A evidência existe e o mecanismo está correto. Uma policy criada no console seguindo o guia quase certamente ficou com a descrição vazia. Depois do import, o plan marcaria a policy como "forces replacement" e o attachment também seria substituído, porque o policy_arn passa a "known after apply". Isso contraria o próprio plano de reconciliar sem recriar, que o guia expressa como "sem apagar/recriar por atalho". O efeito real, porém, é limitado. O problema aparece no …

- **TFB-03 — Provedor OIDC já existe na conta, mas o padrão e o exemplo pedem criação; thumbprints do código diferem dos reais**  
  `terraform/variables.tf:241` · verificação: confirmado · esforço P · já conhecido: Diferença de thumbprints já registrada em PARECER_AWS_ETAPA8.md (etapa 8). A dec · requisitos: REQ-OBR-03, REQ-OBR-04  
  **Problema:** O usuário criou o provedor à mão na conta nova. Com o valor de exemplo (true) e sem import, o apply falha com EntityAlreadyExists. Se o provedor for importado, o plan troca in-place os thumbprints reais pelos dois valores herdados da Fase 3. A AWS valida o GitHub pela cadeia de CA, então isso não deve quebrar a federação, mas gera drift sem motivo. Também falta uma decisão registrada sobre quem é dono do provedor nesta conta.  
  **Recomendação:** Na conta dedicada, a opção mais simples é create_github_oidc_provider = false no terraform.tfvars local. O data source lê o provedor, o destroy da base não o remove (ele não tem custo) e não é preciso importá-lo. Se a escolha for importar (true), remover thumbprint_list, que é Optional no provider, ou alinhá-lo ao valor real. Ajustar terraform.tfvars.example e o README para refletir o caso desta conta.  
  **Verificação:** Conferido: terraform/variables.tf:241 default = true e terraform.tfvars.example:83 create_github_oidc_provider = true; modules/iam-ci/main.tf:56-59 fixa os thumbprints 6938fd4d... e 1c58a3a8...; inventario-aws-sanitizado.json:663-671 (oidc_thumbprints) mostra aws=[ab9d0263...], equal=false. O provedor foi criado à mão (LOG:78; PENDENCIAS:36), e a propriedade ainda não foi decidida (PENDENCIAS:115 'definindo propriedade/reutilização do OIDC'). Com true e sem import, o apply falha com EntityAlread…

- **TFB-04 — Correção F-023 da trust só existe na árvore de trabalho; o HEAD da dev ainda tem StringLike com curinga e o subject antigo**  
  `terraform/modules/iam-ci/main.tf:139` · verificação: confirmado · esforço P · já conhecido: F-025 (trabalho não comitado desde 3b21e65) e F-023 · requisitos: REQ-OBR-03, REQ-OBR-04  
  **Problema:** Na árvore de trabalho, o subject e o StringEquals estão corretos e idênticos à trust real. A versão comitada, porém, aceita qualquer contexto do repositório e usa o formato sem IDs, que não corresponde ao token real. Um plan/apply feito a partir de um checkout limpo, de outra máquina ou de um agente que descarte as mudanças sobrescreveria a trust correta da role importada. O CI então passaria a receber AccessDenied no AssumeRoleWithWebIdentity e, além disso, a trust ficaria mais permissiva.  
  **Recomendação:** Comitar na dev (com autorização do usuário) as mudanças de terraform/ antes de qualquer init com backend, import ou plan. Versionar junto o teste de trust (ver TF-BASE-09).  
  **Verificação:** git show HEAD:terraform/modules/iam-ci/main.tf: linha 136 test = "StringLike" e linha 144 values = ["repo:${var.github_repository}:*"]. Na árvore de trabalho, main.tf:81 monta o subject com @287716251/@1373159817 e :147 usa StringEquals. git diff --stat HEAD -- terraform/ mostra 5 arquivos modificados (104+/11-). O risco de um checkout limpo sobrescrever a trust correta é real. Já era conhecido como F-023 (corrigido só no disco) e F-025 (trabalho não comitado), mas o reforço de que o commit prec…

- **TFB-05 — A base ainda não declara a role OIDC do self-healing prevista no plano**  
  `terraform/main.tf:0` · verificação: confirmado · bloqueia a entrega · esforço M · já conhecido: Planejado no plano E5 (plano-fase4/partes/04-plataforma.html e 07-resposta.html) · requisitos: REQ-OBR-19, REQ-OBR-22, REQ-OBR-31, REQ-OBR-38  
  **Problema:** O desenho escolhido (repository_dispatch -> workflow -> kubectl rollout restart no EKS) precisa de uma identidade AWS com eks:DescribeCluster e de uma access entry no cluster. A única role existente só tem permissões de ECR. Sem a nova role, o workflow de self-healing não acessa o cluster, e REQ-OBR-19/22/31/38 ficam bloqueados. Há ainda um ponto de isolamento: a trust do CI aceita qualquer workflow que rode em refs/heads/main, inclusive repository_dispatch. Se o self-healing usar o mesmo subject, os dois workflows poderiam assumir as duas roles.  
  **Recomendação:** Criar um módulo (por exemplo modules/iam-selfhealing) com trust StringEquals em um subject de environment (repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:environment:self-healing), com o job do workflow usando 'environment: self-healing', e uma policy mínima (eks:DescribeCluster no ARN do cluster). Expor o ARN como output e fazer a access entry na camada cluster, conforme o plano. Isso separa a trust do CI (branch) da trust do self-healing (environment).  
  **Verificação:** terraform/main.tf chama apenas vpc, ecr, messaging e iam_ci, e terraform/modules/ só tem ecr, eks, elasticache, iam-ci, irsa, messaging e rds. grep por self-heal em terraform/ e .github/ não retorna nada. A única role tem só ECR (iam-ci/main.tf, policy ecr_push). O ponto de isolamento procede: a trust aceita ref:refs/heads/main, e um workflow repository_dispatch roda na branch padrão com esse mesmo subject. A role já estava prevista no plano E5 (04-plataforma.html/07-resposta.html), então é trab…

- **TFC-01 — Node group 2 x c7i-flex.large (4 GiB) não comporta com folga a stack de observabilidade + ArgoCD**  
  `terraform/cluster/variables.tf:86` · verificação: parcial · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: REVISAO_GERAL_INFRA_2026-10-28 I-07 e plano 09-plano-fontes (terceiro nó). A con · requisitos: REQ-OBR-05, REQ-OBR-06, REQ-OBR-07, REQ-OBR-08, REQ-OBR-09, REQ-OBR-11, REQ-OBR-23, REQ-OBR-25, REQ-OBR-26  
  **Problema:** Pela fórmula do VPC CNI (ENIs x (IPs-1) + 2), cada nó comporta 3x9+2 = 29 pods, ou 58 nos dois nós. Pods não são o gargalo. A memória é: cada nó tem 4 GiB brutos. Pela minha estimativa, que não foi medida, sobram cerca de 3,2 GiB alocáveis depois do kube-reserved e do limite de eviction, ou seja, uns 6,4 GiB no total. Esse espaço tem de acomodar: addons do sistema (aws-node, kube-proxy, coredns, ebs-csi controller+node, metrics-server, cerca de 12 pods), ArgoCD reduzido (4 pods, terraform/k8s/argocd.tf:134-147), as 5 aplicações + postgres-targeting + até 2 réplicas de HPA (requests de 64-128Mi cada) e a stack planejada: Prometheus, kube-state-metrics, node-exporter x2, Loki, Grafana, Collector agent x2 + gateway. Prometheus e Loki costumam passar de algumas centenas de MiB de working set. Com max_unavailable=1 (main.tf:213), uma atualização deixa um só nó, de 4 GiB. O risco concreto é OOMKilled/evictions ou pods Pending na hora da gravação (REQ-OBR-23/25/26). O disco raiz não está declarado e fica no padrão do recurso: 20 GiB, segundo a documentação do aws_eks_node_group, o que precisa ser reconfirmado.  
  **Recomendação:** Antes do primeiro apply, decidir o dimensionamento com números. (a) Avaliar m7i-flex.large: mesmos 2 vCPU e 29 pods, com 8 GiB. Conferir na página oficial o preço em us-east-2 e se ele é elegível ao plano da conta nova. (b) Ou passar para 3 nós c7i-flex.large, como já propõe o plano (cerca de US$ 0,47/h no total). Também: declarar requests/limits explícitos em todos os charts de observabilidade (retenção curta no Prometheus e no Loki, Loki em modo single binary, sem Alertmanager se o alerta ficar no Grafana/APM) e somar os requests numa planilha antes de subir; definir disk_size = 30 no node group; depois do deploy, medir com kubectl top nodes/pods e registrar como evidência.  
  **Verificação:** parcial; impacto procede — A evidência confere: o código está em 2 x c7i-flex.large, o node group não declara disk_size e a própria variável admite que o sizing está pendente. O risco de faltar memória com a stack de observabilidade é real, e não há conta de requests registrada. Mas o achado exagera em dois pontos. (1) O problema já era conhecido. O plano prevê um terceiro nó em E2 (desired = 3), Alertmanager desligado e requests revisados, e a revisão I-07 pede exatamente esse dimensionamento. …

- **TFC-02 — Sem access entry para a role do self-healing (nem para um admin explícito); só o criador do cluster recebe acesso**  
  `terraform/modules/eks/main.tf:93` · verificação: parcial · severidade original: alta · bloqueia a entrega · esforço M · requisitos: REQ-OBR-19, REQ-OBR-22, REQ-OBR-31, REQ-OBR-38, REQ-OBR-03  
  **Problema:** O plano faz o self-healing num runner do GitHub Actions: o workflow assume uma role IAM por OIDC e roda kubectl rollout restart. No modo de autenticação atual, só o principal IAM que executou o apply vira admin do cluster. Qualquer outra role precisa de aws_eks_access_entry e aws_eks_access_policy_association, e nada disso está declarado, nem a própria role do self-healing. Sem isso o workflow recebe 'Unauthorized' do API server e a automação exigida em REQ-OBR-19/22/31 não executa. O acesso administrativo também fica atrelado a quem rodou o apply (perfil da CLI, SSO etc.), sem estar declarado em código. Trocar bootstrap_cluster_creator_admin_permissions depois força a recriação do cluster.  
  **Recomendação:** Na camada cluster, ou numa camada nova do self-healing: criar a role IAM com trust OIDC do GitHub restrita ao repositório/workflow com o mesmo subject imutável do F-023 e permissão só de eks:DescribeCluster no ARN do cluster. Adicionar aws_eks_access_entry para ela e aws_eks_access_policy_association com AmazonEKSEditPolicy (ou uma policy/RBAC mínima que permita patch em deployments) com access_scope type = "namespace", namespaces = ["togglemaster"]. Opcionalmente, adicionar access entry explícito para o ARN do admin humano, via variável. Avaliar authentication_mode = "API", porque o aws-auth ConfigMap não é usado.  
  **Verificação:** parcial; impacto procede — A evidência existe: hoje não há access entry nem role do self-healing no Terraform, e sem isso o workflow do GitHub Actions receberia Unauthorized ao rodar o rollout restart. Mas o achado trata isso como lacuna não percebida, e o plano de arquitetura já tem exatamente a correção recomendada: access entry + AmazonEKSEditPolicy limitada ao namespace togglemaster, na camada cluster, nas etapas E2/E5. A recomendação só repete o plano. O self-healing nem foi implementado ai…

- **TFK-03 — Application acompanha a main, que ainda nao contem gitops/overlays/prod nem as tags reais de imagem**  
  `terraform/k8s/variables.tf:121` · verificação: confirmado · esforço P · já conhecido: Parcial: comentario em terraform/k8s/variables.tf:115-119 e REVISAO_GERAL_INFRA_ · requisitos: REQ-OBR-05, REQ-OBR-25  
  **Problema:** Se a camada k8s for aplicada antes do PR dev->main e do primeiro CI na main, que publica as imagens no ECR novo e comita as tags, a Application fica em ComparisonError (o caminho nao existe) ou sincroniza pods em ImagePullBackOff. Com cluster pago por hora, essa ordem errada custa dinheiro e tempo de gravacao.  
  **Recomendação:** Registrar no runbook da Fase 4 a ordem obrigatoria: PR para a main, CI publica imagens e comita tags, depois patches de endpoints e so entao 'terraform -chdir=terraform/k8s apply'. Incluir no terraform.tfvars.example as linhas gitops_repo_branch e gitops_repo_path com comentario. Para ensaios antes do merge, aceitar targetRevision=dev apenas com imagens/tag ja publicadas. Opcional: adicionar uma precondition/check que falhe quando gitops_repo_branch != "main" sem confirmacao explicita.  
  **Verificação:** variables.tf:121 usa default "main", e argocd.tf:301 o usa em targetRevision. 'git ls-tree main gitops/overlays/prod' saiu vazio e 'git ls-tree -r --name-only main | grep -c gitops' deu 0. gitops/overlays/prod/kustomization.yaml:67-71 ainda tem registry.conta-pendente.invalid e a tag conta-pendente. Já era conhecido em parte: variables.tf:115-119 diz que a main precisa receber o PR, mas nenhuma pré-condição no código nem ordem formal no runbook impede aplicar antes. Severidade média está adequad…

- **TFK-05 — Application sem dependencia explicita do namespace, dos Secrets e da StorageClass (ordem de criacao e de destruicao)**  
  `terraform/k8s/argocd.tf:352` · verificação: confirmado · esforço P · já conhecido: Parcial: docs/00_COLAB_IA/LOG_DE_TRABALHO.md 2026-09-11 ('Encerrar primeiro a Ap · requisitos: REQ-OBR-03, REQ-OBR-05  
  **Problema:** Na criacao, o ArgoCD pode sincronizar antes dos Secrets e da StorageClass existirem, deixando pods em CreateContainerConfigError e PVC Pending por algum tempo. Se o ArgoCD criar o namespace primeiro, o kubernetes_namespace_v1.app pode falhar com 'already exists'. No destroy, o Terraform apaga o namespace e a StorageClass em paralelo com a Application, enquanto o selfHeal/CreateNamespace pode recriar recursos. Na Fase 3 a sequencia funcionou (guia secao 10: 13 recursos em 1m04s), mas com a Application de observabilidade e os PVCs de Prometheus/Loki o risco de corrida e de EBS orfao (custo) aumenta.  
  **Recomendação:** Adicionar ao kubernetes_manifest.app_togglemaster depends_on = [kubernetes_namespace_v1.app, kubernetes_secret_v1.auth, .flag, .targeting, .evaluation, .postgres_targeting, kubernetes_storage_class_v1.gp3], e fazer o mesmo na futura Application observability. No destroy, a Application sai primeiro e so depois o namespace e os PVCs. Manter no guia a verificacao de volumes EBS 'available' apos o destroy.  
  **Verificação:** argocd.tf:352 tem só depends_on = [helm_release.argocd]. destination.namespace = var.app_namespace (argocd.tf:311) não referencia kubernetes_namespace_v1.app (secrets.tf:38), e CreateNamespace=true está em argocd.tf:332. Nenhum Secret (secrets.tf:92-211) nem a StorageClass (storageclass.tf:27) tem relação com a Application. Na etapa B do procedimento em duas etapas (argocd.tf:249-252) o helm já existe, então a Application é criada em paralelo com namespace, Secrets e StorageClass. No destroy não…

- **TFK-06 — selfHeal sem ignoreDifferences de /spec/replicas disputa com os HPAs de evaluation e analytics**  
  `terraform/k8s/argocd.tf:315` · verificação: confirmado · esforço P · já conhecido: F-027 (auditoria-codex-2026-10-30_v01/CATALOGO_ACHADOS.md) e plano 04-plataforma · requisitos: REQ-OBR-01, REQ-OBR-05, REQ-OBR-28, REQ-OBR-31  
  **Problema:** Quando o HPA escala para 2, o ArgoCD ve diferenca com o Git e tende a voltar para 1. Isso causa oscilacao justamente no cenario de carga e de incidente que o video precisa mostrar e confunde a leitura do self-healing.  
  **Recomendação:** Preferencia: remover 'replicas' dos Deployments que tem HPA (o HPA passa a ser o dono). Alternativa: ignoreDifferences = [{ group = "apps", kind = "Deployment", jsonPointers = ["/spec/replicas"] }] e syncOptions + "RespectIgnoreDifferences=true". Testar no primeiro cluster de ensaio com carga.  
  **Verificação:** argocd.tf:315-326 tem automated prune/selfHeal e nenhum ignoreDifferences (grep em terraform/ e gitops/ sem resultado). gitops/base/evaluation-service/deployment.yaml:26 e analytics-service/deployment.yaml:24 têm 'replicas: 1', e existem hpa.yaml nos dois serviços. É o conflito clássico entre HPA e selfHeal. Já era conhecido como F-027 e na nota 'A conferir na E3' do plano 04-plataforma; o achado não traz novidade além da recomendação.

- **TFK-11 — Repositório 04 é PRIVADO, mas o token de leitura do ArgoCD é opcional e vazio por padrão**  
  `terraform/k8s/variables.tf:125` · verificação: confirmado · severidade original: alta · bloqueia a entrega · esforço P · requisitos: REQ-OBR-05, REQ-OBR-25  
  **Problema:** O repositório fiap-devops-arqcloud-2026/tech-challenge-04 é privado. Do jeito que está, um apply sem TF_VAR_github_token conclui sem erro, mas não cria o Secret de repositório. A Application fica em Unknown com 'authentication required', e o único aviso é o output credencial_do_repo_criada = false (outputs.tf:59-73). O terraform.tfvars.example só traz um comentário. O output sugere 'ghp_xxxx' (token clássico, outputs.tf:67), enquanto a descrição da variável pede um fine-grained token. Num repositório de organização, o fine-grained PAT ainda pode depender de a organização permitir e aprovar esse tipo de token.  
  **Recomendação:** Tornar o token obrigatório enquanto o repositório for privado: tirar o default "" e adicionar uma validation length(var.github_token) > 0, ou criar uma variável repo_is_private = true com um bloco check/precondition. Alternativa preferível: deploy key SSH somente leitura do repositório 04, com sshPrivateKey no Secret e repoURL git@github.com:..., sem dono pessoal nem escopo de organização. Se ficar o PAT: fine-grained com Contents: Read-only só no 04, expirando logo depois de 2026-11-17, e aprovação da organização confirmada antes da sessão paga. Corrigir 'ghp_xxxx' no output e incluir a orientação no tfvars.example.  
  **Verificação:** confirmado; impacto procede — A evidência existe e está correta. O repositório é privado (isso já se sabia desde F-023), mas a variável ainda trata a visibilidade como desconhecida, e o token continua opcional. Um apply sem TF_VAR_github_token termina sem erro e deixa a Application do ArgoCD sem conseguir clonar, o que quebra o GitOps (REQ-OBR-05/25) e tudo o que depende dele, inclusive o self-healing. A inconsistência ghp_ vs fine-grained também é real. O risco de a organização exigir aprovação…

- **XCL-02 — Artefatos de trabalho não curados (156 MB) seriam incluídos por um git add amplo**  
  `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/offline-test.jsonl:0` · verificação: confirmado (Claude) · severidade original: alta · bloqueia a entrega · esforço P · já conhecido: F-024 (Claude 2026-10-28, Codex 2026-10-30). Novos: o volume total de 161 MB e o · requisitos: REQ-OBR-20  
  **Problema:** O GitHub recusa arquivos acima de 100 MB, então um push com esse log falha e obriga a reescrever o histórico local perto do prazo. O restante do volume (cópias de serviços, inventários com ID/ARNs da conta, que é privada mas não precisa ir para o repositório da entrega) poluiria o repositório que será avaliado.  
  **Recomendação:** Acrescentar ao .gitignore regras específicas: `00_COLAB_IA/02_TRABALHO/**/offline-test.jsonl` (ou `*.jsonl` em 02_TRABALHO) e decidir se `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-2*/` entra no Git. Guardar só o resumo dos testes (8 passed) e os hashes. Remover `-verbose` do gerador. Conferir com `git check-ignore -v` e `git add -n .` antes do commit.  
  **Verificação:** Conferido com find + git check-ignore: só offline-test.jsonl (>50 MB) não é ignorado. Mesmo problema de CMP-01.

- **XCL-03 — Primeiro apply da base colide com recursos criados à mão: nenhum import preparado e exemplo ainda manda criar o OIDC**  
  `terraform/terraform.tfvars.example:83` · verificação: confirmado (Claude) · severidade original: alta · bloqueia a entrega · esforço M · já conhecido: P-003 (itens 'Inicializar base e incorporar os recursos manuais') e PARECER_AWS_ · requisitos: REQ-OBR-01, REQ-OBR-03, REQ-OBR-05  
  **Problema:** O apply da base, como o código está hoje, falha com RepositoryAlreadyExists/EntityAlreadyExists depois de já ter criado VPC/NAT (cobrança de cerca de US$ 0,045/h). Se o OIDC for importado com create=true, um destroy futuro o apagaria. Sem decidir a propriedade, plan e apply ficam imprevisíveis, e esse é o primeiro passo do caminho crítico até a E2.  
  **Recomendação:** Criar terraform/imports.tf com blocos `import` para module.ecr (5 repositórios), module.iam_ci (role, policy, attachment) e, se o projeto for dono, o provedor OIDC. Do contrário, usar create_github_oidc_provider=false no tfvars local. Rodar o plan da base com enable_nat_gateway=false e aceitar só se mostrar 0 destroy/replace, a criação das 5 lifecycle policies e a reconciliação dos thumbprints. Registrar a decisão em DECISOES.  
  **Verificação:** Conferido: nenhum bloco import em terraform/; terraform.tfvars.example:83 com create_github_oidc_provider = true. Mesmo problema de TFB-01/TFB-03.

- **XCL-04 — IDs de rastreabilidade da Fase 3 no código colidem com IDs da Fase 4 de significado diferente**  
  `terraform/outputs.tf:29` · verificação: nao_verificado · esforço P · requisitos: REQ-OBR-39, REQ-OBR-40  
  **Problema:** Quem segue um ID de um comentário de IaC/GitOps (agente, avaliador ou o próprio autor ao escrever as justificativas do PDF) cai numa decisão ou achado diferente. Isso mina a rastreabilidade que o projeto adota como regra. A decisão 'sem Ingress/port-forward', vigente na Fase 4, nem existe no registro da Fase 4.  
  **Recomendação:** Opção mínima (P): em 00_COLAB_IA/DECISOES.md e no README, uma nota de que IDs em comentários de código sem prefixo referem-se a docs/00_COLAB_IA (Fase 3), e criar uma ADR da Fase 4 para 'sem Ingress, acesso por port-forward' que cite a D-012 da Fase 3. Opção completa (M): prefixar as referências da Fase 3 no código (ex.: `F3/D-012`) com sed controlado e revisão do diff.

- **XCL-05 — Documentos de estado e CLAUDE.md contradizem o estado real (conta, backend, P-003/P-013/F-023, datas, contagens)**  
  `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:109` · verificação: confirmado (Claude) · esforço P · já conhecido: F-021 (Codex 2026-10-30 cobre README, SECURITY, observability/README e o backlog  
  **Problema:** A regra de ouro do protocolo ('LOG + PENDENCIAS permitem retomar') não vale hoje. O próximo agente pode tratar a conta como inexistente, refazer o inventário ou a correção F-023, esperar Variables já configuradas ou planejar o PagerDuty com a data errada, num prazo de 17 dias.  
  **Recomendação:** Uma passada de fechamento (P-013 e P-014): marcar as caixas concluídas com data/evidência (correspondencia-aws-github.json, backend.hcl de 10-30); reescrever os TL;DRs de LEIA, PENDENCIAS, DOSSIE, LOG e CLAUDE.md para 'conta verificada em 2026-10-28; bucket/backend.hcl em 2026-10-30; tfvars, imports e init pendentes'; unificar o trial em 2026-11-11 (a fonte mais recente); corrigir 33→34; transferir F-027..F-031 para LOG/PENDENCIAS; mover o TL;DR do LOG para o topo. Preservar as versões antigas em _ARQUIVO_MORTO, como o protocolo exige.  
  **Verificação:** Conferido: CLAUDE.md:9 ainda diz "Nova conta AWS pendente".

- **XCL-06 — Autorizações de sessão acumuladas sem validade no protocolo contradizem CLAUDE.md**  
  `00_COLAB_IA/LEIA-PRIMEIRO.md:34` · verificação: nao_verificado · esforço P  
  **Problema:** As autorizações valem por sessão, mas o arquivo as registra como permanentes e 'prevalecentes', em conflito com CLAUDE.md. Um agente pode executar chamadas autenticadas na AWS (e, por extensão, init/plan com backend real) achando que a permissão de 28/10 ainda vale, ou deixar de comitar por seguir a instrução mais antiga.  
  **Recomendação:** Trocar as seções 'Escopo autorizado em <data>' por uma única 'Escopo vigente' com data e validade explícita ('válida somente na sessão de 2026-10-28; expirada'), deixando o histórico só no LOG. Alinhar CLAUDE.md:9 a esse texto. Registrar que init com backend, import, plan, apply e push exigem pedido novo do usuário.

- **XCL-08 — Pré-requisitos do self-healing não estão modelados: role do CI só tem ECR, EKS sem access entry, workflow precisa estar na main**  
  `terraform/modules/eks/main.tf:97` · verificação: nao_verificado · bloqueia a entrega · esforço M · já conhecido: Lacuna geral já conhecida (I-05 da REVISAO_GERAL_INFRA, plano E5). Novos: a ausê · requisitos: REQ-OBR-19, REQ-OBR-22, REQ-OBR-38  
  **Problema:** O caminho Grafana → repository_dispatch → Actions → `kubectl rollout restart` depende de três camadas que hoje não se encaixam. Pela documentação do GitHub, repository_dispatch só dispara workflow que esteja na branch padrão (main, ainda vazia). A role do CI não pode chamar eks:DescribeCluster nem tem acesso RBAC. Sem isso, REQ-OBR-19/22/38 não fecham e a falha só aparece no ensaio final.  
  **Recomendação:** Na camada cluster: aws_iam_role togglemaster-self-healing (trust StringEquals no mesmo subject imutável de main, permissão eks:DescribeCluster no cluster) + aws_eks_access_entry + aws_eks_access_policy_association com escopo de namespace togglemaster (ou um Role RBAC mínimo que permita patch em deployments). Criar .github/workflows/self-healing.yml e levá-lo à main antes do ensaio da E5. Ensaiar com `gh api repos/:owner/:repo/dispatches` antes de ligar o Grafana.

- **XCL-09 — Contrato de segredos não cobre as credenciais externas da Fase 4**  
  `gitops/SECRETS-CONTRATO.md:38` · verificação: nao_verificado · esforço P · já conhecido: Parcial: plano 09-plano-fontes (token GitHub no Grafana). · requisitos: REQ-OBR-16, REQ-OBR-17, REQ-OBR-18, REQ-OBR-19  
  **Problema:** A E3/E4 vai precisar de 4 credenciais novas (license key New Relic no Collector, integration/routing key PagerDuty, webhook Slack, token GitHub para repository_dispatch) sem definição de origem, Secret, namespace, rotação ou exposição no state. É o ponto com mais risco de vazamento em screenshot ou no Git durante a gravação, e o trial do PagerDuty não deixa margem para retrabalho.  
  **Recomendação:** Antes da E3, estender SECRETS-CONTRATO com uma linha por credencial: nome do Secret, namespace (ex.: observability), chave, origem (TF_VAR_* ou `kubectl create secret` manual), se fica no state, escopo mínimo (fine-grained PAT só neste repositório com Contents: write) e revogação após a entrega. Acrescentar ao scripts/security-check.sh padrões para NRAK-/license key e hooks.slack.com/services.

- **XCL-10 — Dimensionamento divergente entre IaC (2 nós), documentação (3 workers) e custo estimado**  
  `terraform/cluster/variables.tf:102` · verificação: nao_verificado · esforço P · já conhecido: I-07 (REVISAO_GERAL_INFRA_2026-10-28) e nota em PENDENCIAS:70 ('dimensionamento  · requisitos: REQ-OBR-05, REQ-OBR-06  
  **Problema:** A stack Prometheus/Loki/Grafana/Collector (DaemonSet + gateway) mais 5 serviços, o Postgres do targeting e o ArgoCD em 2 nós de 4 GiB podem não caber (pods Pending durante a gravação). Se for usar 3 nós, o orçamento e o tempo ligado precisam ser calculados com o número real. Sem créditos confirmados, a divergência afeta diretamente o custo.  
  **Recomendação:** Decidir em uma ADR (ver T-07) com uma soma de requests/limits de todos os charts. Fixar o valor no terraform.tfvars local da camada cluster e alinhar README, PENDENCIAS e a estimativa de US$/h com a mesma premissa.

### Baixa (67)

- **CIC-06 — Infraestrutura (Terraform/manifests) sem scan de segurança no pipeline**  
  `.github/workflows/terraform-check.yml:73` · verificação: confirmado · severidade original: média · esforço M · requisitos: REQ-OBR-03, REQ-OBR-04  
  **Problema:** O pipeline cobre SAST, SCA e imagem, mas não a configuração da infraestrutura. Problemas de IAM, security group ou endpoint só são vistos em revisão manual. Para um DevSecOps defensável na banca é uma lacuna barata de fechar. Não é exigência literal do enunciado.  
  **Recomendação:** Adicionar um passo com trivy-action (mesmo SHA): scan-type config, scan-ref terraform/ (e gitops/), severity HIGH,CRITICAL. Começar com exit-code 0, triar os achados (por exemplo, o endpoint público do EKS, que é decisão documentada) e passar para exit-code 1 com exceções nominais.  
  **Verificação:** terraform-check.yml:73-97 só faz fmt -recursive -check e init -backend=false + validate nas 3 camadas. Não há tfsec, checkov nem trivy config, e não existe *.tftest.hcl em terraform/ (find vazio). O próprio achado reconhece que isso não é exigência literal do enunciado, e o DevSecOps de aplicação (SAST, SCA, imagem) já existe. Por isso a severidade baixa, como melhoria para defender na banca. Não é achado conhecido.

- **CIC-07 — Commits do bot na main divergem da dev; um force-push ou merge errado volta as tags para placeholder**  
  `.github/workflows/_ci-go.yml:606` · verificação: confirmado · severidade original: média · esforço P · requisitos: REQ-OBR-05, REQ-OBR-23  
  **Problema:** Depois do primeiro pipeline na main, ela passa a ter commits do bot que a dev não tem. Um push do usuário para main é rejeitado (non-fast-forward) enquanto os 5 bots gravam. Se o usuário resolver com force-push ou com 'git checkout dev -- gitops/', as 5 tags voltam para o placeholder. Com selfHeal ligado, o ArgoCD aplicaria isso e os pods iriam para ImagePullBackOff, um risco direto para a gravação. A corrida entre os 5 pipelines está bem tratada pelo laço fetch/reset/edit/push; o risco aqui é o fluxo humano dev↔main.  
  **Recomendação:** Documentar no runbook: depois de cada pipeline na main, fazer 'git pull origin main' na dev, sem force-push na main. Se o plano da organização permitir, ativar um ruleset que bloqueie force-push na main sem bloquear o bot. Antes da gravação, conferir que o kustomization.yaml da main tem as 5 tags v1.0.0-<sha>.  
  **Verificação:** _ci-go.yml:606 e _ci-python.yml:636 fazem 'git push origin HEAD:main'. gitops/overlays/prod/kustomization.yaml:67-80 traz os placeholders registry.conta-pendente.invalid/conta-pendente. A Application observa var.gitops_repo_branch (terraform/k8s/argocd.tf:301) com selfHeal = true (:325), e origin/main = 003a707 (git log). A divergência dev/main é real. Um merge comum de dev em main preservaria as tags do bot, porque a dev não altera essas linhas. O dano só acontece com force-push ou com 'checkou…

- **CIC-10 — Relatório do Trivy omite HIGH, ao contrário do que diz o comentário**  
  `.github/workflows/_ci-go.yml:281` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** O parâmetro severity do Trivy filtra o que é exibido, então HIGH não aparece no log. A banca e o próprio autor ficam sem visibilidade das vulnerabilidades altas, e o comentário induz a erro.  
  **Recomendação:** Acrescentar um passo não bloqueante (severity HIGH,CRITICAL, exit-code 0, format table) antes do passo bloqueante, ou corrigir o comentário. O scanOnPush do ECR também registra os achados.  
  **Verificação:** _ci-go.yml:281-283 traz o comentário 'HIGH e abaixo aparecem no relatório' com 'severity: CRITICAL'. O mesmo filtro aparece em _ci-go.yml:423 e _ci-python.yml:316/:454. No Trivy, severity filtra o que é reportado, então HIGH não aparece no log e o comentário induz a erro. O impacto é só de visibilidade. Não é achado conhecido.

- **CIC-11 — Ferramentas do CI sem versão fixada (pylint, flake8, bandit, pytest) e kustomize sem checksum**  
  `.github/workflows/_ci-python.yml:180` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** Uma release nova do pylint ou do bandit pode mudar nota ou regras e quebrar o pipeline perto da entrega sem nenhum commit. O binário baixado sem checksum roda no job que tem contents: write. O próprio arquivo defende versão fixa para o kustomize (:64-67), mas não aplica a mesma regra aos linters.  
  **Recomendação:** Fixar as versões (por exemplo, um requirements-ci.txt com hashes), validar o sha256 do tarball do kustomize contra o checksums.txt da release e usar '-lockfile=readonly' no terraform-check.  
  **Verificação:** Conferido: 'pip install pytest' (_ci-python.yml:141), 'pip install flake8 pylint' (:180) e 'pip install bandit' (:263), todos sem versão. O curl do kustomize v5.4.3 + sudo mv não confere sha256 (_ci-go.yml:534-539, _ci-python.yml:565). terraform-check.yml faz init sem -lockfile=readonly, ao contrário de validate-all.sh:41, e os três .terraform.lock.hcl estão versionados. Ressalva: no Go, o golangci-lint (v2.13.2) e o gosec (v2.29.0) estão fixados, então a falta de versão vale só para o Python. N…

- **CIC-12 — Compose Integration roda em qualquer push/PR (sem paths nem concurrency); jobs sem timeout**  
  `.github/workflows/compose-integration.yml:3` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** Em repositório privado, os minutos do Actions são cobrados da cota do plano. Cada commit que só mexe em documentação ou 00_COLAB_IA reconstrói as 5 imagens e sobe o Compose, e um job travado (por exemplo, download da base do Trivy ou docker build) pode consumir até 6 h.  
  **Recomendação:** Acrescentar paths-ignore (00_COLAB_IA/**, docs/**, '**/*.md'), 'concurrency: group: compose-${{ github.ref }}, cancel-in-progress: true' e timeout-minutes de 15 a 30 em todos os jobs. Conferir a cota do plano da organização.  
  **Verificação:** compose-integration.yml:4-6 dispara em pull_request sem filtro e em push para main/dev sem paths, e não tem concurrency (grep vazio). Só esse workflow tem timeout-minutes (:16, 20 min). Os jobs de _ci-go/_ci-python ficam no padrão de 360 min, mas esses workflows já são filtrados por paths. O repositório consta como private (02_TRABALHO/etapas8-9-2026-10-28_v01/github/configuracao.json:11). O impacto é só de cota de minutos. Não é achado conhecido.

- **CIC-13 — workflow_dispatch não publica imagem: sem forma de republicar sem commit**  
  `.github/workflows/_ci-go.yml:331` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04, REQ-OBR-05  
  **Problema:** Um disparo manual na main só roda as verificações. Se um serviço falhar no primeiro push (ver CI-02 e CI-08) ou se for preciso republicar depois de limpar o ECR, a única saída é um commit artificial na pasta do serviço. O comentário promete uma função que o workflow não tem.  
  **Recomendação:** Aceitar também "github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'" nos jobs image e gitops. O sub do token continua ref:refs/heads/main, compatível com a trust atual.  
  **Verificação:** Os jobs image/gitops exigem github.event_name == 'push' && ref main (_ci-go.yml:331/:494, _ci-python.yml:364/:524). auth-service.yml:65-68 apresenta o workflow_dispatch como útil na gravação e para reexecutar. Ressalva: para reexecutar uma rodada de push que falhou, o 'Re-run jobs' do GitHub mantém o evento push e publica. O caso realmente sem saída é republicar sem commit novo, por exemplo depois de limpar o ECR. Não é achado conhecido.

- **CIC-14 — Filtros de paths não incluem .trivyignore nem .pylintrc**  
  `.github/workflows/auth-service.yml:45` · verificação: confirmado · esforço P · já conhecido: F-030 · requisitos: REQ-OBR-04  
  **Problema:** Uma mudança só na política de exceções ou no lint não reexecuta os scans que dependem dela, e a revisão da exceção fica sem evidência no CI.  
  **Recomendação:** Incluir '.trivyignore' nos 5 chamadores e '.pylintrc' nos 3 chamadores Python.  
  **Verificação:** auth-service.yml:45-52 e :60-63 listam só services/<svc>/**, o próprio arquivo e o reutilizável. Os dois reutilizáveis usam 'trivyignores: .trivyignore' (_ci-go.yml:309, _ci-python.yml:342) e o Python usa .pylintrc (:229). Já era conhecido: é o F-030 (auditoria-codex-2026-10-30_v01/CATALOGO_ACHADOS.md:263), que o Codex classificou como Média; baixa parece mais adequada porque o efeito é só de evidência.

- **CIC-15 — Compose Integration não roda a prova OTel e não condiciona a publicação**  
  `.github/workflows/compose-integration.yml:22` · verificação: confirmado · esforço M · já conhecido: F-020 · requisitos: REQ-OBR-21, REQ-OBR-04  
  **Problema:** Uma regressão na instrumentação (REQ-OBR-21) passaria pelo CI. Além disso, a imagem é publicada pelo workflow do serviço mesmo com a integração vermelha.  
  **Recomendação:** Acrescentar um job ou passo com o overlay OTel e o test-observability.sh, só em PR ou com paths services/**. Recomendação de qualidade, não exigência da FIAP.  
  **Verificação:** Conferido em compose-integration.yml:22 ('bash scripts/test-compose.sh'). Os passos :25, :28 e :31 usam só docker-compose.yaml e docker-compose.integration.yaml, e o grep por 'otel|observab' em scripts/test-compose.sh e .github/workflows/*.yml não encontrou nada. O workflow é independente (on: pull_request/push, :3-7) e não é pré-requisito de _ci-go/_ci-python. Assim, uma regressão de OTel passa pelo CI e a publicação não depende da integração. O achado já era conhecido (F-020), como o próprio a…

- **CIC-16 — Resquícios da Fase 3 em comentários, no verificador e no guia de reprodução**  
  `scripts/security-check.sh:11` · verificação: confirmado · esforço P · já conhecido: Parcial: F-021 (documentação vigente desatualizada) · requisitos: REQ-OBR-04  
  **Problema:** Não há risco operacional: o git grep não acha a conta antiga em .github, terraform, gitops nem services. Porém o verificador não impede que ARN ou endpoint da conta da Fase 3 voltem a arquivos operacionais, que é a regra do CLAUDE.md, e o guia ensina um procedimento que não corresponde mais aos workflows.  
  **Recomendação:** Trocar o ID literal na linha 11 por uma descrição. Acrescentar uma regra para a conta da Fase 3 restrita a arquivos operacionais (.github, terraform, gitops, services, scripts). Atualizar as referências ao enunciado e às datas para a Fase 4 e corrigir a tabela do GUIA_DE_REPRODUCAO para apontar para as Variables do repositório.  
  **Verificação:** Todos os pontos foram conferidos. security-check.sh:11 tem um ID literal de 12 dígitos (<CONTA>) num comentário versionado. Os comentários de :69-73 falam da Fase 3 em conta pessoal, e a regra :78 cobre só a conta da Fase 2. _ci-go.yml:294 e _ci-python.yml:327 citam 'o enunciado da Fase 3'. .trivyignore:6 também cita a Fase 3, e :53-54 diz 'a 6 dias da entrega'. GUIA_DE_REPRODUCAO.md:186-187 manda editar ECR_REGISTRY/AWS_ROLE_ARN nos workflows, e o bloco sed de ~:205 troca a conta neles, mas _ci…

- **CIC-17 — pyproject.toml configura ruff, que nenhum pipeline executa**  
  `pyproject.toml:1` · verificação: parcial · esforço P  
  **Problema:** A configuração sugere um gate que não existe e duplica, com outra ferramenta, a decisão já registrada em .pylintrc:68-74 (broad-exception-caught).  
  **Recomendação:** Remover o arquivo ou documentar que serve só para uso local no editor.  
  **Verificação:** Os fatos conferem. pyproject.toml:1-4 tem só [tool.ruff.lint] ignore=['BLE001']. Nenhum .yml ou .sh chama ruff. .pylintrc:68-74 já trata broad-exception-caught. Porém docs/ARQUITETURA.md:308 já registra 'O pyproject.toml configura só o ruff, que nenhum workflow executa', ou seja, o desalinhamento é conhecido e documentado. Por isso o campo 'ja_conhecido' vazio está errado e a alternativa 'documentar' já está em parte atendida. Falta só dizer que o arquivo serve para uso no editor, ou removê-lo. …

- **CMP-02 — SECURITY.md não cobre os segredos novos da Fase 4**  
  `SECURITY.md:3` · verificação: parcial · severidade original: média · esforço P · requisitos: REQ-OBR-11, REQ-OBR-12, REQ-OBR-17, REQ-OBR-18, REQ-OBR-19, REQ-OBR-22  
  **Problema:** A Fase 4 traz credenciais de terceiros: license/ingest key do New Relic usada pelo Collector, chave de integração/routing key do PagerDuty, webhook do Slack e o token do GitHub que o self-healing usa para chamar repository_dispatch. O documento não diz onde ficam (Secret do Kubernetes via Terraform? GitHub Secrets? cofre do PagerDuty?) nem proíbe versioná-las. Também não cita backend.hcl, que contém o nome do bucket com o ID da conta. Sem regra escrita, o caminho mais curto ao montar values do Helm, a Application do ArgoCD ou o webhook é colar a chave em YAML versionado. O GitOps sincroniza tudo do Git, o que torna esse vazamento provável e difícil de desfazer.  
  **Recomendação:** Acrescentar uma tabela para a Fase 4: chave do New Relic como Secret do Kubernetes (criado por Terraform ou por 'kubectl create secret' fora do Git) e referenciado pelo Collector via env; token do repository_dispatch como fine-grained PAT de escopo mínimo (só o repositório, Actions/Contents) guardado na ferramenta que dispara; webhook do Slack e chave do PagerDuty só nas UIs. Incluir backend.hcl e essas chaves na lista 'Nunca versionar'. Ajustar a frase das linhas 3-6 assim que algum segredo existir no GitHub. Se der, estender scripts/security-check.sh com padrões de chave do New Relic e URL hooks.slack.com.  
  **Verificação:** Conferi SECURITY.md:3-6 e 25-30: a lista 'Nunca versionar' não cita as chaves do New Relic, do PagerDuty, do Slack nem o token do repository_dispatch, então a lacuna existe. Duas ressalvas. (1) O backend.hcl já está tratado: terraform/.gitignore:2-3 tem 'backend.hcl' e '**/backend.hcl', e o git check-ignore confirmou que os três arquivos locais estão ignorados. (2) Esses segredos ainda não existem no repositório, e o risco já aparece de forma genérica em PENDENCIAS_E_PROXIMOS_PASSOS.md:46 ('segr…

- **CMP-04 — Portas de Postgres, Redis e DynamoDB Local publicadas em todas as interfaces**  
  `docker-compose.yaml:14` · verificação: confirmado · esforço P  
  **Problema:** Sem IP explícito, o Docker publica em 0.0.0.0. Assim, em rede compartilhada (Wi-Fi da faculdade), Postgres com senha conhecida do .env.example e Redis sem autenticação ficam acessíveis a terceiros. Nenhum teste usa as portas 5433/5434/6379/8000: test-flow.py acessa o Redis por 'compose exec'. Os dados são fictícios, por isso o risco é baixo, mas o overlay OTel já segue o padrão correto e o base não.  
  **Recomendação:** Prefixar todas as portas com '127.0.0.1:' (por exemplo "127.0.0.1:${AUTH_PORT}:8001"). Remover a publicação de 5433/5434/6379/8000, ou movê-la para um profile 'debug', se ninguém consulta os bancos pelo host.  
  **Verificação:** Conferi docker-compose.yaml:14 ('5433:5432'), :35, :56 ('6379:6379', Redis sem senha), :69 ('8000:8000') e as portas dos apps em :85/109/134/163/197, todas sem IP de bind. A única dependência dessas portas pelo host é documental: docs/GUIA_DE_REPRODUCAO.md:705 lista as portas que precisam estar livres. Nenhum script ou teste fora de services/ usa 5433, 5434, 6379 ou 8000; test-flow.py só acessa as portas 8001-8005 em 127.0.0.1. Como os dados são fictícios, baixa está correta.

- **CMP-06 — Scripts de integração: sem limpeza local, valores duplicados e chamada sem timeout**  
  `scripts/integration/test-flow.py:55` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04, REQ-OBR-23  
  **Problema:** (1) Fora do CI, a stack de 9-10 contêineres e os volumes ficam ligados após o teste, passe ele ou falhe. O README:188 admite isso. (2) Portas e MASTER_KEY estão fixos no Python e duplicam o .env.example, o que gera divergência silenciosa se o .env.example mudar. (3) O 'up --wait' interno não tem limite e pode ficar preso até o timeout de 20 min do job. (4) Rodado sozinho, test-flow.py recria o evaluation-service sem o overlay de integração. (5) Variáveis já exportadas no shell (por exemplo AWS_REGION, que o GUIA seção 0 exporta) têm precedência sobre --env-file. (6) No Windows o GUIA manda usar WSL por causa do python3.  
  **Recomendação:** Em test-compose.sh, adicionar 'trap' opcional (KEEP_STACK=1 para manter) que execute 'docker compose --env-file .env.example down -v --remove-orphans'. Em test-flow.py, ler portas/MASTER_KEY do .env.example (ou de variáveis passadas pelo script), passar '--wait-timeout 120' no up interno e falhar cedo se COMPOSE_FILE não estiver definido. Opcionalmente, usar 'python3 || python' no script.  
  **Verificação:** Conferi cada ponto. scripts/test-compose.sh:9-14 não tem trap nem down, e o README.md:188 admite 'O script não remove o ambiente'. test-flow.py:11 chama o compose sem -f nem -p e depende do COMPOSE_FILE exportado em test-compose.sh:7. test-flow.py:44 fixa range(8001, 8006) e :52 fixa 'local-master-key-change-me'. test-flow.py:55 roda 'up --wait' sem --wait-timeout. O GUIA:735 manda usar o WSL por causa do python3. No CI a limpeza já existe (compose-integration.yml:31 com down -v), então o efeito…

- **CMP-07 — GUIA manda limpar o projeto Compose tc03-integration; o script cria tc04-integration**  
  `docs/GUIA_DE_REPRODUCAO.md:741` · verificação: confirmado · esforço P  
  **Problema:** Quem seguir o Apêndice A executa um 'down -v' que não encontra nada e acha que limpou. Os contêineres e volumes do teste continuam ocupando a máquina. Sobrou da renomeação Fase 3 para Fase 4.  
  **Recomendação:** Trocar para '-p tc04-integration' (ou usar COMPOSE_PROJECT_NAME) na linha 741, igual ao README.  
  **Verificação:** docs/GUIA_DE_REPRODUCAO.md:741 usa '-p tc03-integration', mas scripts/test-compose.sh:6 define 'tc04-integration', igual a compose-integration.yml:18 e ao README.md:192. O down do GUIA não remove nada do projeto criado pelo script. É inconsistência de documentação, baixa.

- **CMP-08 — Imagens de dados com tag flutuante e DynamoDB Local sem healthcheck**  
  `docker-compose.yaml:7` · verificação: confirmado · esforço P · requisitos: REQ-OBR-02  
  **Problema:** Tags flutuantes fazem o CI baixar versões diferentes a cada execução, enquanto Moto e Collector já estão fixados por digest. O comentário da linha 200 está errado: dá para configurar healthcheck, só a imagem não traz curl. No overlay de integração o dynamodb-local sobe sem uso, porque o analytics aponta para o Moto, e consome recursos à toa.  
  **Recomendação:** Fixar 'postgres:16.x-alpine@sha256:...' e 'redis:7.x-alpine@sha256:...'. Corrigir o comentário. No overlay de integração, pôr dynamodb-local em 'profiles: [local]' ou 'scale: 0'.  
  **Verificação:** docker-compose.yaml:7 e :26 usam 'postgres:16-alpine' e :53 usa 'redis:7-alpine', tags flutuantes, enquanto docker-compose.integration.yaml:4 fixa o Moto por digest. No overlay de integração, o analytics aponta DYNAMODB_ENDPOINT para o aws-local (integration.yaml:45), e mesmo assim o dynamodb-local (docker-compose.yaml:64-70) continua subindo sem uso. O comentário em :200 ('não tem healthcheck configurável') é impreciso, mas não verifiquei quais ferramentas a imagem amazon/dynamodb-local:3.3.0 t…

- **CMP-09 — .env.example com variáveis mortas e Compose sem exigir as obrigatórias**  
  `.env.example:49` · verificação: confirmado · esforço P  
  **Problema:** Variáveis que não têm efeito confundem quem edita o .env achando que liga SQS ou muda credenciais. Se a pessoa rodar 'docker compose up' sem criar o .env, o Compose só avisa e passa valores vazios: o Postgres falha com mensagem pouco clara e as portas viram vazias.  
  **Recomendação:** Remover as três variáveis mortas, ou usá-las de fato via ${...} no compose, e documentar. Trocar as interpolações obrigatórias por '${POSTGRES_PASSWORD:?defina .env a partir de .env.example}'.  
  **Verificação:** .env.example:49 (AWS_SQS_URL) e :52-53 (as chaves 'test') não são interpoladas: docker-compose.yaml:160, 191-192 e 195 usam literais, e o overlay também (integration.yaml:21-22, 32-35 e 43). O comentário em .env.example:47-48 até explica que o compose injeta a URL vazia, o que atenua a confusão, mas as variáveis continuam sem efeito. As interpolações em docker-compose.yaml:10-12 e :29-33 não usam ':?'. Baixa.

- **CMP-10 — .gitattributes só normaliza *.sh; com autocrlf=true, YAML/.env/Python/Dockerfile ficam CRLF no Windows**  
  `.gitattributes:1` · verificação: confirmado · esforço P  
  **Problema:** Hoje nada quebra: o teste local passou e o CI Linux faz checkout em LF. Mas arquivos montados em contêiner (scripts/integration/*.py, configs do Collector e, depois, values/dashboards da stack) ficam CRLF no Windows, e o resultado depende da configuração de cada máquina. Também falta marcar binários (PDF/PNG) para evitar diffs/normalização.  
  **Recomendação:** Acrescentar '* text=auto eol=lf', '*.ps1 text eol=crlf' (se houver) e '*.pdf binary', '*.png binary'; depois 'git add --renormalize .' num commit separado.  
  **Verificação:** O .gitattributes só tem '*.sh text eol=lf' e o core.autocrlf está true. O git ls-files --eol mostra 'i/lf w/crlf attr/' para .env.example, docker-compose.yaml, scripts/integration/test-flow.py e services/auth-service/Dockerfile, e 327 arquivos no total com w/crlf. Hoje nada quebra, porque o CI é Linux e o teste local passou, então o impacto é preventivo. Baixa.

- **DOC-07 — Não há documento de arquitetura vigente da Fase 4; docs/ARQUITETURA.md é histórico e contradiz o código atual**  
  `docs/ARQUITETURA.md:79` · verificação: parcial · severidade original: média · esforço M · requisitos: REQ-OBR-39, REQ-OBR-26, REQ-OBR-11  
  **Problema:** O banner da linha 1 avisa que o documento é histórico, mas ele é a única referência técnica detalhada (portas, Secrets, IRSA, pipeline). Para a Fase 4 não existe documento equivalente da arquitetura implementada (OTel SDK, Collector agent/gateway, exporters, alerta, incidentes). REQ-OBR-39 pede essa explicação no relatório, e o README só traz a arquitetura 'planejada'.  
  **Recomendação:** Criar docs/ARQUITETURA_FASE4.md, ou nova versão preservando a original, com o que realmente estiver implantado: fluxo de telemetria por sinal, configuração do Collector, endpoints OTLP/New Relic (sem chave), regra de alerta, contact points e o workflow repository_dispatch. Atualizar as tabelas herdadas que mudaram (chaves de estado, trust OIDC, gatilhos). Reaproveitar o texto como seção OTel do relatório.  
  **Verificação:** As divergências de docs/ARQUITETURA.md são reais. :79 usa as chaves 'prod/*.tfstate'. :242 mostra terraform-check só na main, mas o workflow tem branches [main, dev]. :321 usa StringLike, mas terraform/modules/iam-ci/main.tf:141 usa StringEquals com subject por IDs e branch (:81). O caminho correto é modules/iam-ci, não iam-ci. :380 diz 'Sem testes unitários Python'. Porém o banner da linha 1 marca o documento como histórico e remete ao README. O README.md vigente já cobre a arquitetura da Fase …

- **DOC-09 — Catálogo de requisitos (e espelho HTML) mostra todos os itens como Pendente, com data 2026-09-20, e não remete à matriz atual**  
  `docs/requisitos/README.md:14` · verificação: confirmado · esforço P · já conhecido: DOC-01 (REVISAO_GERAL_DOCUMENTACAO_2026-10-27_v01.md:59) · requisitos: REQ-OBR-12, REQ-OBR-13, REQ-OBR-21  
  **Problema:** O catálogo funciona como referência normativa, mas um leitor (ou o próprio usuário, na reta final) não enxerga o progresso nem onde está a evidência de cada requisito. A matriz MATRIZ_REQUISITOS_FASE4_2026-10-28_v01.json existe só localmente e não é versionada.  
  **Recomendação:** Manter o catálogo normativo e acrescentar uma linha no TL;DR apontando para uma matriz de status versionada, ou adicionar uma coluna 'Evidência atual' e regenerar o HTML pelo script, sem editar o HTML à mão. Não marcar como concluído o que só foi provado localmente.  
  **Verificação:** docs/requisitos/README.md:5 traz 'Última atualização: 2026-09-20' e :14 diz 'Todos os requisitos estão **Pendente**'. A MATRIZ_REQUISITOS_FASE4_2026-10-28_v01.json aparece como '??' no git status. O impacto é baixo porque o catálogo é normativo e o status vive no backlog. O ponto já era conhecido (DOC-01 da revisão de 2026-10-27).

- **DOC-10 — Duas âncoras quebradas para seções que não existem mais no README**  
  `docs/GUIA_DE_REPRODUCAO.md:9` · verificação: confirmado · esforço P · já conhecido: DOC-05 (REVISAO_GERAL_DOCUMENTACAO_2026-10-27_v01.md:91); F-021  
  **Problema:** A navegação dos documentos históricos leva a seções do README da Fase 3 que foram substituídas. O impacto é baixo.  
  **Recomendação:** Apontar para a cópia histórica do README em 00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879/ (se existir lá) ou trocar por um texto que explique que a seção não existe mais.  
  **Verificação:** docs/GUIA_DE_REPRODUCAO.md:9 aponta para ../README.md#8-custo e docs/ARQUITETURA.md:7 aponta para ../README.md#5-decisões-e-o-porquê. Os títulos atuais do README (grep '^## ') não têm essas seções. A recomendação é viável: 00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879/README.md contém '## 5. Decisões e o porquê' (:219) e '## 8. Custo' (:353). O ponto já era conhecido (F-021 e DOC-05 da revisão anterior).

- **DOC-11 — Relatório histórico cita o PDF da Fase 3, que está apagado na árvore, e o README diz que os materiais da Fase 3 foram preservados**  
  `docs/RELATORIO_DE_ENTREGA.md:100` · verificação: confirmado · esforço P · já conhecido: LOG_DE_TRABALHO.md:182 ('33 exclusões preexistentes observadas, não executadas')  
  **Problema:** Se essas exclusões forem comitadas, a referência do relatório histórico quebra e a afirmação do README deixa de ser verdadeira na árvore do repositório 04 (o material continua no histórico Git e no repositório 03).  
  **Recomendação:** Decidir as 33-34 exclusões preexistentes: restaurar com 'git restore' ou confirmar a remoção. No segundo caso, ajustar README.md:232 para 'preservados no histórico Git e no repositório 03' e a linha 100 do relatório para o commit/caminho histórico.  
  **Verificação:** RELATORIO_DE_ENTREGA.md:100 cita 'docs/POSTECH - Tech Challenge - Fase 3.pdf'. git status mostra 34 linhas ' D', entre elas esse PDF e os guias/aulas da Fase 3 em docs/aulas-fiap. Hoje docs/aulas-fiap só contém as pastas 00 a 04 da Fase 4. README.md:232 afirma que os 'materiais da Fase 3 foram preservados'. As exclusões já eram conhecidas pelo LOG. A contradição com README:232 é nova.

- **DOC-12 — Guia histórico versionado publica o ID da conta AWS antiga e o endpoint do Redis antigo**  
  `docs/GUIA_DE_REPRODUCAO.md:177` · verificação: confirmado · esforço P  
  **Problema:** O ID de conta não é credencial, mas facilita reconhecimento e engenharia social, e a regra do projeto é não usar identificadores da conta anterior. O comando :203 também ensina um sed que depende desse ID. O dado já está no histórico Git e no _ARQUIVO_MORTO, então o ganho de removê-lo é só reduzir a exposição em documentos ativos.  
  **Recomendação:** Na nova versão do guia, trocar por <CONTA_ANTIGA>/<CONTA> e remover o endpoint Redis literal. Não reescrever o histórico Git, porque não compensa o custo no prazo.  
  **Verificação:** git grep -c com o padrão de 12 dígitos encontra 10 linhas em docs/GUIA_DE_REPRODUCAO.md. Um exemplo é :203, com o sed sobre togglemaster-tfstate-<CONTA>-us-east-2-an. :191 contém o endpoint literal do Redis antigo (hostname de um recurso da conta anterior, não credencial). A severidade baixa está bem calibrada: o dado já está no histórico Git e no _ARQUIVO_MORTO.

- **DOC-13 — backend.hcl.example repete a key que o README diz estar fixa no backend.tf**  
  `terraform/README.md:17` · verificação: confirmado · esforço P · requisitos: REQ-OBR-03  
  **Problema:** Hoje os valores coincidem, mas há duas fontes da chave de estado. O valor de -backend-config prevalece, então um backend.hcl local copiado de outra camada pode apontar a camada para o estado errado sem que o backend.tf indique nada.  
  **Recomendação:** Remover key dos .example (deixar só bucket/region) ou documentar no README que a key do .hcl deve coincidir com a do backend.tf e conferir isso antes do init.  
  **Verificação:** terraform/README.md:17 diz que backend.tf 'fixa a chave'. terraform/backend.tf:43, cluster/backend.tf:47 e k8s/backend.tf:55 definem a key. Os três backend.hcl.example repetem key = "phase4/prod/<camada>.tfstate". Em configuração parcial, -backend-config sobrepõe o bloco, então há duas fontes da mesma chave. Hoje os valores coincidem, por isso o risco é baixo. Não li os backend.hcl locais (ignorados) para confirmar o que eles contêm.

- **GIT-05 — Nenhum securityContext nos 6 pods; runAsNonRoot exigirá UID numérico**  
  `gitops/base/auth-service/deployment.yaml:0` · verificação: confirmado · severidade original: média · esforço M · requisitos: REQ-OBR-04, REQ-OBR-05  
  **Problema:** Os containers não declaram allowPrivilegeEscalation=false, capabilities drop ALL, seccompProfile RuntimeDefault nem readOnlyRootFilesystem. Os pods sem IRSA (auth, flag, targeting e postgres) montam o token da SA default sem precisar dele. Isso é DevSecOps básico, e a ausência fica visível num relatório de projeto que se apresenta como DevSecOps. Ao corrigir, há uma armadilha: runAsNonRoot=true com USER não numérico faz o kubelet recusar o container ('non-numeric user ... cannot verify user is non-root'), e os Gunicorn precisam de /tmp gravável se o root ficar read-only.  
  **Recomendação:** Nos 5 Deployments: pod securityContext {runAsNonRoot: true, runAsUser/runAsGroup: <UID fixo, ex. 10001 também fixado no Dockerfile>, seccompProfile: RuntimeDefault}; container {allowPrivilegeEscalation: false, capabilities.drop: [ALL], readOnlyRootFilesystem: true} com emptyDir em /tmp nos serviços Python; automountServiceAccountToken: false em auth, flag, targeting e postgres. Postgres: só seccomp, drop ALL com as capabilities mínimas ou fsGroup 70; testar antes. Opcional: rótulo pod-security.kubernetes.io/warn=restricted no namespace (nos dois lados, Terraform e GitOps).  
  **Verificação:** No render de gitops/overlays/prod, securityContext=0 e automountServiceAccountToken=0. Os Dockerfiles usam 'USER app' não numérico (services/auth-service/Dockerfile:49-50,59; flag-service/Dockerfile:57-58,73). Então a armadilha do runAsNonRoot existe. Baixei a severidade porque nenhum requisito da Fase 4 (REQ-OBR-04/05, docs/requisitos/README.md:53-54) exige endurecimento de pod, e a falta não bloqueia a entrega, que é focada em observabilidade.

- **GIT-06 — ConfigMaps via envFrom sem hash: mudar endpoint ou OTEL não reinicia os pods**  
  `gitops/base/evaluation-service/deployment.yaml:54` · verificação: confirmado · severidade original: média · esforço M · requisitos: REQ-OBR-05, REQ-OBR-11  
  **Problema:** Variáveis de ambiente só são lidas na criação do pod. Quando o ArgoCD atualizar um ConfigMap (troca das sentinelas, inclusão das OTEL_*, ajuste de endpoint do Collector), o Deployment não muda e os pods seguem com os valores antigos. O ArgoCD mostra Synced e o comportamento não muda, o que é fácil de confundir com um bug durante a preparação do vídeo.  
  **Recomendação:** Migrar os 5 ConfigMaps para configMapGenerator na base (com o patch do overlay via behavior: merge), para que o sufixo de hash force o rollout automático. Alternativa mínima: documentar 'kubectl rollout restart' após toda mudança de ConfigMap.  
  **Verificação:** envFrom configMapRef em gitops/base/evaluation-service/deployment.yaml:54-56. Os ConfigMaps entram como resources estáticos (base/kustomization.yaml:34-70) e o overlay só tem patches (overlays/prod/kustomization.yaml:39-41), sem configMapGenerator. Então mudar um ConfigMap não reinicia os pods. Baixei para baixa: o cluster é efêmero e recriado a cada sessão (D-017, argocd.tf:255-256), e na maioria das sessões os pods já nascem com o ConfigMap vigente. O problema só aparece quando o ConfigMap mud…

- **GIT-07 — Falta RBAC mínimo para o self-healing agir sobre os Deployments**  
  `gitops/base/kustomization.yaml:0` · verificação: parcial · severidade original: média · bloqueia a entrega · esforço M · já conhecido: REVISAO_GERAL_INFRA I-05 (automação ausente, sem detalhar RBAC) · requisitos: REQ-OBR-19, REQ-OBR-22, REQ-OBR-31  
  **Problema:** Sem uma identidade no cluster com permissão de patch em deployments no namespace togglemaster, a ação corretiva do workflow falha com Forbidden, e o REQ de self-healing não se demonstra.  
  **Recomendação:** Declarar em gitops/base um Role (apps/deployments: get, list, patch; namespace togglemaster) e um RoleBinding para um grupo dedicado (ex.: togglemaster-selfheal). No Terraform, criar o access entry da role do GitHub mapeado a esse grupo, ou usar AmazonEKSEditPolicy com escopo de namespace. Restringir o allowlist de Deployments no workflow.  
  **Verificação:** É verdade que o código ainda não tem Role/RoleBinding em gitops/ nem aws_eks_access_entry (só authentication_mode em terraform/modules/eks/main.tf:97). Mas o plano já trata disso: 00_COLAB_IA/02_TRABALHO/plano-fase4/partes/04-plataforma.html prevê um 'aws_eks_access_entry' com 'AmazonEKSEditPolicy restrita ao namespace togglemaster' na camada cluster, e 09-plano-fontes.html e 08-exibicao-mudancas.html repetem isso. Portanto não falta RBAC no desenho; falta implementar uma etapa já planejada (E5)…

- **GIT-08 — Comentários dos manifests contradizem o contrato de Secrets (ESO, Secrets Manager, camada errada)**  
  `gitops/base/auth-service/deployment.yaml:67` · verificação: confirmado · esforço P · já conhecido: F-021 (só a âncora de SECRETS-CONTRATO.md:10) · requisitos: REQ-OBR-20, REQ-OBR-23  
  **Problema:** Quem depurar CreateContainerConfigError seguindo os comentários vai procurar ESO, externalsecret.yaml e Secrets Manager inexistentes, e não secrets.tf. Os manifests são didáticos e entram na avaliação. O gitops/README.md (data 2026-10-20, linha 22) também ficou para trás.  
  **Recomendação:** Reescrever os comentários para 'Secret criado por terraform/k8s/secrets.tf (D-018)', remover as menções a ESO e externalsecret, corrigir a âncora do README e trocar as referências ao guia histórico pelo runbook vigente quando ele existir. Atualizar o gitops/README após incluir a stack.  
  **Verificação:** Conferido em gitops/base/auth-service/deployment.yaml:66-68 (cita ESO e um externalsecret.yaml que não existe; a pasta tem só configmap, deployment e service), evaluation-service/deployment.yaml:61 ('via ESO') e flag-service/deployment.yaml:51 ('injetado pelo ESO'). Já gitops/SECRETS-CONTRATO.md:10 e overlays/prod/kustomization.yaml:26 dizem que o ESO foi descartado. postgres-targeting/service.yaml:5 diz que o DATABASE_URL fica no Secrets Manager, mas SECRETS-CONTRATO.md:19-22 diz que os valores…

- **GIT-09 — Imagem do Postgres com tag móvel, fora do scan e comentário afirmando imutabilidade**  
  `gitops/base/postgres-targeting/statefulset.yaml:56` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** 16-alpine é uma tag flutuante (muda a cada minor ou rebuild do Alpine). Nós diferentes podem rodar builds diferentes, e a imagem nunca é verificada pela Trivy. O comentário ensina o contrário do que acontece. Puxar anonimamente do Docker Hub pelo NAT também está sujeito ao limite de pulls (não verificado nesta revisão).  
  **Recomendação:** Fixar versão completa ou digest (postgres:16.x-alpine3.yy@sha256:...), corrigir o comentário e incluir essa imagem num scan Trivy (job agendado ou de config). Opcional: espelhá-la no ECR.  
  **Verificação:** gitops/base/postgres-targeting/statefulset.yaml:56 usa 'postgres:16-alpine', uma tag móvel, e os comentários das linhas 52 ('versao fixa') e 58-59 ('a tag e imutavel') estão errados. A Trivy só varre services/<svc> e <svc>:scan (_ci-go.yml:280,421; _ci-python.yml:314,452), então a imagem do Postgres nunca é escaneada. O limite de pulls do Docker Hub continua não verificado, como o próprio achado ressalva.

- **GIT-10 — Namespace com dois donos (Terraform e ArgoCD) e rótulos divergentes**  
  `gitops/base/namespace.yaml:21` · verificação: confirmado · esforço P · requisitos: REQ-OBR-03, REQ-OBR-05  
  **Problema:** A afirmação de rótulos idênticos é falsa no render. O ArgoCD vai acrescentar managed-by e a anotação de tracking num objeto que o Terraform também gerencia. Provavelmente aparece drift no próximo plan da camada k8s (o comportamento do provider kubernetes 3.2.1 não foi verificado). Se namespace.yaml sair do Git, o prune apaga o namespace junto com os Secrets criados pelo Terraform.  
  **Recomendação:** Deixar o namespace só com o Terraform: remover namespace.yaml da base e manter CreateNamespace=true como rede de proteção. Outra saída é igualar os rótulos e usar lifecycle ignore_changes em metadata[0].labels/annotations, além da anotação argocd.argoproj.io/sync-options: Prune=false no Namespace.  
  **Verificação:** No render, o Namespace traz os rótulos part-of e managed-by: argocd (managed-by vem de base/kustomization.yaml:30). Já terraform/k8s/secrets.tf:38-46 declara só part-of, e o comentário das linhas 33-35 afirma que os rótulos são idênticos, o que é falso. Com prune=true (argocd.tf:320), tirar namespace.yaml do Git levaria o ArgoCD a apagar o namespace junto com os Secrets do Terraform. O drift no plan do provider kubernetes 3.2.1 não foi verificado, como o achado reconhece.

- **GIT-11 — Labels recomendados incompletos e ausentes nos pods (afeta filtros de Loki/Grafana)**  
  `gitops/base/kustomization.yaml:26` · verificação: confirmado · esforço P · requisitos: REQ-OBR-08, REQ-OBR-10  
  **Problema:** Os pods não carregam app.kubernetes.io/name, part-of nem component. Para o dashboard e as consultas do Loki por serviço ou sistema (e para o service.name nos logs), será preciso depender do rótulo informal 'app'. O inventário 'kubectl get all -l app.kubernetes.io/part-of=togglemaster' citado nos comentários não lista os pods.  
  **Recomendação:** Acrescentar includeTemplates: true ao bloco labels e definir app.kubernetes.io/name e app.kubernetes.io/component por serviço, mantendo os selectors 'app' (que são imutáveis em Deployments já criados). Usar esses rótulos nas relabel rules do agente de logs.  
  **Verificação:** base/kustomization.yaml:26-30 tem includeSelectors: false e não tem includeTemplates. No render, os 5 templates de pod só têm 'app: <svc>' e app.kubernetes.io/name tem 0 ocorrências, então o inventário citado na linha 25 não lista pods. O impacto é limitado: a descoberta de logs do Kubernetes já fornece namespace, pod e container, e o service.name vem das variáveis OTEL. Por isso, baixa.

- **GIT-12 — Sem NetworkPolicies, e o CNI não as aplicaria**  
  `gitops/base/kustomization.yaml:0` · verificação: confirmado · esforço M  
  **Problema:** Qualquer pod do cluster (inclusive os charts de terceiros da stack que serão instalados) alcança o postgres-targeting:5432 e os serviços. Num projeto acadêmico só com ClusterIP o risco é baixo, mas incluir NetworkPolicy sem habilitar o enforcement no VPC CNI daria falsa sensação de proteção.  
  **Recomendação:** Se houver tempo: habilitar enableNetworkPolicy no addon vpc-cni e criar default-deny de ingress no namespace togglemaster com liberações explícitas (evaluation→flag/targeting, flag/targeting→auth, targeting→postgres, Collector/Prometheus→serviços). Caso contrário, registrar como limitação no relatório.  
  **Verificação:** NetworkPolicy tem 0 ocorrências no render, e terraform/modules/eks/main.tf:282-287 declara o addon vpc-cni sem configuration_values (sem enableNetworkPolicy). Nenhum requisito da Fase 4 exige NetworkPolicy, e o achado já propõe só registrar como limitação. Baixa está correta.

- **GIT-15 — Probes rasas e idênticas para readiness e liveness, sem timeoutSeconds nem startupProbe**  
  `gitops/base/flag-service/deployment.yaml:68` · verificação: parcial · esforço P · requisitos: REQ-OBR-16, REQ-OBR-28  
  **Problema:** Readiness nunca reflete banco/Redis/serviços dependentes indisponíveis, então o pod continua recebendo tráfego durante a falha proposital, o que pode ser bom para o alerta mas impede o Kubernetes de isolar o problema. Nos serviços Python com um único worker sync, uma requisição lenta bloqueia o /health e, com timeout de 1 s, pode gerar reinícios por liveness sob carga (efeito colateral durante testes de carga ou do incidente).  
  **Recomendação:** Definir timeoutSeconds: 2-3 explicitamente; considerar startupProbe nos Python em vez de initialDelaySeconds longos; se quiser readiness significativa, criar /ready que verifique a dependência principal (sem tocar o /health da liveness). Registrar no roteiro do vídeo qual sinal o alerta usa, para não depender da readiness.  
  **Verificação:** Os fatos conferem: gitops/base/flag-service/deployment.yaml:68-83 usa /health em readiness e liveness, o render tem 0 timeoutSeconds e 0 startupProbe, e services/flag-service/app.py:71-74 e evaluation-service/handlers.go:18-27 retornam 200 fixo. O risco está exagerado: a liveness exige 3 falhas a cada 30 s (cerca de 90 s) para reiniciar, então o timeout de 1 s raramente causa restart. Com 1 réplica, uma readiness que checasse dependências tiraria o único endpoint e poderia gerar falha em cascata…

- **OBS-04 — test-observability.sh sem trap de limpeza/diagnóstico e fora do CI**  
  `scripts/test-observability.sh:18` · verificação: confirmado · severidade original: média · esforço P · já conhecido: F-020 (parte CI); a ausência de trap e de diagnóstico é nova · requisitos: REQ-OBR-04, REQ-OBR-13  
  **Problema:** Quando o teste falha ou passa, o laboratório continua rodando: portas 8001-8005, 4318 e 13133, além de volumes. O projeto tc04-integration é o mesmo de test-compose.sh, que usa COMPOSE_FILE sem o overlay OTel. Uma execução seguinte desse script recria os serviços sem OTel e deixa o otel-collector órfão. Em caso de falha, nenhum log do Collector ou dos serviços é impresso, e o operador precisa repetir os comandos do README à mão. A prova de traces também não protege o CI contra regressões.  
  **Recomendação:** Adicionar 'trap cleanup EXIT', em que cleanup imprime 'docker compose logs --tail=100 otel-collector evaluation-service analytics-service' quando o status é diferente de zero e executa 'down -v --remove-orphans', exceto com KEEP_LAB=1 para inspeção. Envolver os passos Python com 'timeout 600' quando disponível e incluir um job ou passo em compose-integration.yml que rode este script com upload de resultado-traces.json como artefato.

- **OBS-05 — Exporters e Collector sem fila, retry e telemetria própria para detectar falha de envio no cluster**  
  `observability/otel-collector-local.yaml:45` · verificação: parcial · severidade original: média · esforço P · requisitos: REQ-OBR-11, REQ-OBR-10  
  **Problema:** Para o arquivo local isso basta. Ao reaproveitar o arquivo no cluster, porém, uma chave New Relic errada (401/403) ou um Loki ou Prometheus indisponível só aparecem nos logs do pod do Collector, e não há métrica otelcol_exporter_send_failed_* coletada para mostrar no Grafana ou alertar. Com isso, a demonstração pode falhar em silêncio. Com error_mode: propagate, um erro de OTTL descarta o lote inteiro: é útil como fail-fast no teste e perigoso no gateway. Um limit_mib absoluto não acompanha o limite do pod.  
  **Recomendação:** Nos values do cluster: sending_queue e retry_on_failure explícitos nos exporters otlphttp/newrelic, loki e prometheusremotewrite; service.telemetry.metrics com leitor Prometheus em :8888 e um ServiceMonitor ou PodMonitor; painel ou alerta com otelcol_exporter_send_failed_spans; error_mode: ignore em filter e transform; memory_limiter com limit_percentage/spike_limit_percentage e GOMEMLIMIT. Manter o exporter debug desligado ou em basic.

- **OBS-06 — test-traces.py depende do ambiente exportado pelo wrapper e duplica a chave mestra**  
  `scripts/integration/test-traces.py:14` · verificação: confirmado · esforço P  
  **Problema:** Executado fora de test-observability.sh, sem COMPOSE_FILE e COMPOSE_PROJECT_NAME, o 'compose up --force-recreate evaluation-service' (linha 161) atua em outro projeto ou sem o overlay OTel. O resultado é um conflito de porta ou um timeout de trace com mensagem enganosa. A chave mestra fixa diverge se .env.example mudar. A mensagem de status HTTP omite a rota e o corpo, o que dificulta o diagnóstico. Chamadas compose sem timeout podem travar. Os valores são fictícios, então não há risco de credencial.  
  **Recomendação:** No início de main(), validar que COMPOSE_FILE contém docker-compose.otel.yaml e que COMPOSE_PROJECT_NAME está definido, abortando com mensagem clara. Ler MASTER_KEY de .env.example (ou de os.environ) em vez de literal. Incluir path e os primeiros 200 caracteres do corpo na mensagem de erro e usar timeout=300 em subprocess.run.

- **OBS-07 — Arquivo de traces cresce sem limite e é relido inteiro a cada segundo**  
  `observability/otel-collector-local.yaml:51` · verificação: confirmado · esforço P  
  **Problema:** Execuções repetidas na mesma OTEL_TRACE_DIR acumulam traces sem limite. Cada sondagem relê e decodifica o arquivo inteiro, o que deixa os testes lentos e aproxima o timeout de 40 s com o tempo. A pasta é ignorada pelo Git, então o problema não chega a vazar para o repositório.  
  **Recomendação:** Truncar ou rotacionar o arquivo no início de test-observability.sh (por exemplo, mover traces.jsonl para traces-<data>.jsonl) ou usar append: false com uma pasta por execução. Em test-traces.py, guardar o offset já lido e processar só as linhas novas.

- **OBS-08 — observability/README.md desatualizado quanto à conta New Relic e ao destino OTLP**  
  `observability/README.md:83` · verificação: confirmado · esforço P · requisitos: REQ-OBR-26, REQ-OBR-39  
  **Problema:** O usuário já criou a conta New Relic (região US, endpoint otlp.nr-data.net), mas o runbook ainda trata essa conta como inexistente e não diz qual endpoint e header usar. O README também descreve apenas o laboratório. Falta indicar o que será reaproveitado no cluster (imagem/digest, processors) e o que muda (agent/gateway, spanmetrics, Loki /otlp), o que é necessário para o relatório (REQ-OBR-39) e para o vídeo (REQ-OBR-26d).  
  **Recomendação:** Atualizar a data e a seção 'Próxima validação externa' com região US, https://otlp.nr-data.net (4318) e header api-key lido de variável ou Secret, sem valor. Acrescentar uma seção curta 'Do laboratório ao cluster' que aponte para os values GitOps quando existirem.

- **OBS-09 — Caminho spanmetrics → Prometheus (taxa de requisições e alerta) não é validado localmente; réplicas do gateway podem duplicar séries**  
  `observability/otel-collector-local.yaml:54` · verificação: parcial · severidade original: média · esforço M · já conhecido: Parcial: risco do nome da métrica em plano-fase4/partes/09-plano-fontes.html:162 · requisitos: REQ-OBR-07, REQ-OBR-10, REQ-OBR-11, REQ-OBR-16  
  **Problema:** O painel REQ-OBR-10b e a regra de alerta REQ-OBR-16, que aciona PagerDuty e self-healing, dependem do nome e dos rótulos da métrica do spanmetrics. Descobrir isso só no EKS consome horas de cluster pagas (cerca de US$ 0,47/h estimados). Além disso, com 2 ou mais réplicas do gateway, cada uma gera séries spanmetrics com os mesmos rótulos, sem rótulo de instância, e o remote write pode registrar conflito ou subcontagem.  
  **Recomendação:** Acrescentar ao laboratório local o conector spanmetrics, com as dimensões http.route e http.response.status_code e a saída do pipeline traces ligada ao conector, e um pipeline metrics → exporter prometheus em 127.0.0.1:8889 ou debug detailed. Registrar o nome real da métrica, por exemplo traces_span_metrics_calls_total, e escrever a PromQL do painel e do alerta antes do cluster. No gateway, usar 1 réplica sem HPA ou adicionar um atributo de instância do Collector às métricas geradas.  
  **Verificação:** Conferido em observability/otel-collector-local.yaml:54-60: só existe o pipeline traces, sem conector spanmetrics nem pipeline metrics. Isso é coerente com o escopo declarado na linha 1 (laboratório local só de traces). A pendência do nome da métrica já era conhecida: 09-plano-fontes.html:55 e :162 e 08-exibicao-mudancas.html:21 (placeholder <calls>) deixam a conferência para a E3. A sugestão de validar localmente antes do EKS é boa e barata, mas não corrige um defeito existente. A parte sobre r…

- **OBS-10 — Filtro filter/health do Collector não é exercitado pelo teste**  
  `scripts/integration/test-traces.py:241` · verificação: confirmado · esforço P · requisitos: REQ-OBR-11  
  **Problema:** Como o SDK já não cria spans de /health, a asserção passa mesmo que filter/health esteja errado ou seja removido. A configuração do filtro (otel-collector-local.yaml:19-25) fica sem prova, e ela será reaproveitada no gateway, onde as probes do kubelet chamam /health.  
  **Recomendação:** Na sonda OTLP sintética, enviar também um span com http.route='/health' (e outro com url.path='/health') num trace_id próprio e verificar que não aparece em traces.jsonl, enquanto o span de controle aparece.  
  **Verificação:** Conferido em scripts/integration/test-traces.py:154-156 (envio de /health), :241 (asserção 'not read_trace(health_id)') e :112-120 (a sonda usa http.route '/privacy-probe'). O SDK já descarta /health: services/*/telemetry.py:128 usa excluded_urls e services/*-service/telemetry.go:125 usa WithFilter. Portanto a asserção passa mesmo sem o filter/health de otel-collector-local.yaml:19-25. observability/README.md:59 afirma 'filtrado no Collector' sem teste que prove isso. A severidade baixa está cor…

- **TFB-06 — Documentação da base desatualizada: diz que conta e bucket estão pendentes e cita a conta anterior**  
  `terraform/README.md:3` · verificação: confirmado · esforço P · requisitos: REQ-OBR-20  
  **Problema:** Em 2026-10-30, a conta, o bucket e o backend.hcl existem, e ECR, role, policy e OIDC foram criados à mão. Os comentários e o README induzem o próximo passo errado (por exemplo, create_github_oidc_provider=true 'somente se a nova conta ainda não tiver o emissor'), não citam a reconciliação por import e trazem um prefixo e um evento da conta anterior. Como o README faz parte do repositório entregue (REQ-OBR-20), isso também prejudica a avaliação.  
  **Recomendação:** Atualizar o README com o estado em 2026-10-30, a lista de recursos pré-existentes, o passo de import/plan sem destroy (TF-BASE-01) e a decisão sobre o OIDC (TF-BASE-03). Trocar o comentário de iam-ci/main.tf:31-34 por um texto neutro e substituir '891...' por '<conta>'.  
  **Verificação:** Conferido: terraform/README.md:3 'A nova conta AWS ainda não foi informada' e :5 'Última atualização: 2026-10-20'; backend.tf:4 'a conta e o bucket novos ainda estao pendentes'; variables.tf:55 'Ainda nao ha bucket confirmado'; iam-ci/main.tf:31-32 'como aconteceu nesta conta em 2026-09-14' (evento da conta anterior); outputs.tf:40 e ecr/outputs.tf:13 '891...amazonaws.com'. O README.md:19 ('Nenhum bootstrap foi executado nesta etapa') refere-se à etapa de importação e é o ponto mais fraco. Os de…

- **TFB-07 — Validações de variáveis incompletas (AZ x região, tamanho das listas, CIDR, tag phase, contagem de imagens)**  
  `terraform/variables.tf:72` · verificação: confirmado · esforço P · requisitos: REQ-OBR-03  
  **Problema:** Trocar aws_region sem trocar as AZs fixas us-east-2a/b, ou passar listas de tamanhos diferentes, só falha na API ou gera subnets incoerentes. Sobrescrever default_tags no tfvars sem a chave phase apaga 'phase = 4' de todos os recursos e prejudica o rastreio de custo exigido no relatório. ecr_images_to_keep igual a 0 gera uma lifecycle policy recusada pela API.  
  **Recomendação:** Adicionar validations: length(var.availability_zones) >= 2 e igual ao tamanho das duas listas de CIDR; alltrue([for c in ... : can(cidrhost(c, 0))]); alltrue([for az in var.availability_zones : startswith(az, var.aws_region)]); lookup(var.default_tags, "phase", "") == "4"; ecr_images_to_keep >= 1; length(var.services) == length(distinct(var.services)). Também é possível usar merge() de tags fixas com var.default_tags em providers.tf.  
  **Verificação:** Conferido em variables.tf: availability_zones (:72-81), private_subnet_cidrs e public_subnet_cidrs (:83-98), default_tags (:47-60), services (:118-125) e ecr_images_to_keep (:156-164) não têm bloco validation. Só ecr_image_tag_mutability tem (:139-145). Em modules/ecr/variables.tf, image_tag_mutability não tem validation no módulo, mas a raiz já valida, então esse item é quase irrelevante. Os riscos descritos (AZ x região, default_tags sem phase sobrescrito no tfvars) são plausíveis e de baixo i…

- **TFB-08 — A policy de push concede 4 ações de leitura que o CI não usa, e o comentário justifica com um uso inexistente**  
  `terraform/modules/iam-ci/main.tf:195` · verificação: confirmado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** Viola levemente o menor privilégio, embora restrito aos 5 ARNs e só para leitura. O comentário afirma um uso que os workflows não fazem, o que confunde quem audita. O risco é baixo neste projeto.  
  **Recomendação:** Manter apenas as 5 ações de push mais GetAuthorizationToken. Isso atualiza a policy real in-place, com nova versão e sem recriação, depois do import. Se a decisão for manter a leitura, corrigir o comentário (por exemplo, 'reserva para cache/inspeção futura').  
  **Verificação:** iam-ci/main.tf:195-201: o comentário diz 'necessario para o cache de build e para o Trivy escanear a imagem publicada' e concede BatchGetImage, GetDownloadUrlForLayer, DescribeImages e DescribeRepositories. Em _ci-go.yml:399, o build é local (:scan), e :415-421 roda o Trivy com image-ref ${{ inputs.service }}:scan antes do login e do push (:456-461). grep por cache-from, type=registry, docker pull, describe-images e batch-get-image em .github/workflows não retorna nada. A linha citada no achado …

- **TFB-09 — O teste de regressão da trust OIDC fica fora de terraform/ e não está versionado**  
  `terraform/modules/iam-ci/main.tf:0` · verificação: confirmado · esforço P · já conhecido: Testes citados no LOG (P-013, 8/8 offline). Não estava registrado que ficaram fo · requisitos: REQ-OBR-03, REQ-OBR-04  
  **Problema:** Os 8 testes que garantem o subject imutável e o StringEquals (F-023) não acompanham o código. Uma regressão no módulo não seria detectada nem no CI nem por outro agente.  
  **Recomendação:** Mover o teste para terraform/modules/iam-ci/tests/trust.tftest.hcl com mock_provider/override_data, para rodar offline, e executar 'terraform test' no workflow de IaC, se houver.  
  **Verificação:** find mostra que o único *.tftest.hcl é 00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/harness/tests/trust.tftest.hcl, com 8 blocos run. git ls-files | grep tftest não retorna nada, e git check-ignore retorna rc=1 (não ignorado, apenas não rastreado). .github/workflows/terraform-check.yml:51-91 roda só fmt e validate, sem terraform test. O LOG:60 cita os testes 8/8, mas não registra que estão fora de terraform/. Relacionado ao TFB-04 (trabalho fora do versionamento), mas é outro probl…

- **TFB-10 — Custo do NAT subestimado nos comentários (ignora a cobrança do IPv4 público do EIP e o processamento por GB)**  
  `terraform/variables.tf:102` · verificação: confirmado · esforço P · já conhecido: F-026 trata de créditos/plano da conta (relacionado, não igual) · requisitos: REQ-OBR-03  
  **Problema:** US$ 33/mês corresponde só à hora do NAT (cerca de US$ 0,045/h). Pelo meu conhecimento, a AWS também cobra o IPv4 público do EIP (cerca de US$ 0,005/h) e o processamento de dados (cerca de US$ 0,045/GB), mas não conferi esses valores na página oficial nesta revisão. O NAT é o único custo horário relevante da base, então vale registrar o valor completo para a decisão de ligar e desligar e para o print de custo do relatório.  
  **Recomendação:** Conferir na página oficial de preços da VPC (NAT Gateway e Public IPv4, us-east-2) e atualizar os comentários com o valor por hora completo (cerca de US$ 0,05/h, mais o tráfego). Manter enable_nat_gateway=false enquanto não houver cluster e destruir ou desligar o NAT entre sessões.  
  **Verificação:** variables.tf:102, main.tf:72 e terraform.tfvars.example:35 citam US$ 33/mês. Isso equivale a cerca de US$ 0,045/h x 730 h, ou seja, só a hora do NAT. main.tf:74 single_nat_gateway = true cria 1 EIP. A cobrança do IPv4 público (cerca de US$ 0,005/h desde fev/2024) e o processamento por GB são preços públicos da AWS que conheço, mas não conferi a página oficial nesta verificação. Para confirmar, ver aws.amazon.com/vpc/pricing (NAT Gateway e Public IPv4, us-east-2). O impacto fica só nos comentário…

- **TFB-11 — Restrição de versão do provider AWS sem teto**  
  `terraform/backend.tf:35` · verificação: parcial · esforço P · requisitos: REQ-OBR-03  
  **Problema:** O lockfile versionado fixa a 6.62.0, mas um 'init -upgrade' acidental, durante a correria antes da entrega, poderia trazer uma major futura (7.x) com mudanças incompatíveis para o módulo VPC 5.x.  
  **Recomendação:** Usar ">= 5.79, < 7.0" (ou "~> 6.62"), que é compatível com o módulo VPC 5.21.0 (>= 5.79), e manter '-lockfile=readonly' no init, como o README já orienta.  
  **Verificação:** backend.tf:35 version = ">= 5.46", e .terraform.lock.hcl:5-6 fixa 6.62.0 (o lockfile é versionado, conforme git ls-files). Porém backend.tf:27-33 documenta a escolha deliberada de não pôr teto (evitar conflito com a restrição do módulo VPC), e o lockfile versionado já mitiga o risco. Só um 'init -upgrade' explícito traria uma 7.x. A sugestão (< 7.0) é razoável como endurecimento, mas não corrige um defeito; é uma decisão já registrada e com contrapartida.

- **TFC-03 — Kubernetes 1.34 sem upgrade_policy STANDARD: fim do suporte padrão em 2026-12-02 e comentários ainda citando 1.31**  
  `terraform/cluster/variables.tf:76` · verificação: confirmado · severidade original: média · esforço P · já conhecido: Plano 09-plano-fontes ('Conferir ... o fim do suporte padrão do EKS 1.34'); a fa · requisitos: REQ-OBR-03, REQ-OBR-05  
  **Problema:** A entrega é em 2026-11-17, 15 dias antes do fim do suporte padrão da 1.34, então o prazo é cumprido. Mas a política padrão é EXTENDED: se o cluster for recriado ou continuar ligado depois de 2026-12-02 (correção, reapresentação, reaproveitamento na fase seguinte), o plano de controle passa a cobrar 6x mais sem aviso no código. Os comentários que citam a 1.31 induzem a escolher uma versão que já está em suporte estendido. O plano registra 'até 2026-12-01'; a data oficial é 2026-12-02.  
  **Recomendação:** Adicionar ao aws_eks_cluster o bloco upgrade_policy { support_type = "STANDARD" } (com isso, ao fim do suporte o cluster é atualizado em vez de passar a cobrar o estendido). Avaliar subir o default para 1.35 ou 1.36, ambas em suporte padrão até 2027, depois de conferir com aws eks describe-addon-versions a compatibilidade dos addons vpc-cni/coredns/kube-proxy/ebs-csi/metrics-server. Atualizar os três comentários que mencionam 1.31 e registrar a fonte com data.  
  **Verificação:** Conferido: terraform/cluster/variables.tf:76 tem default "1.34", aws_eks_cluster (modules/eks/main.tf:66-109) não tem upgrade_policy (o grep por upgrade_policy/support_type no .tf não acha nada) e os comentários sobre 1.31 estão em modules/eks/main.tf:73-74, cluster/main.tf:55-56 e eks/variables.tf:24. Não conferi na web a data de 2026-12-02 nem os preços padrão/estendido; a data bate com o ciclo de 14 meses da 1.34, mas falta confirmar na página oficial de versões do EKS. Rebaixo para baixa: a …

- **TFC-04 — max_size = 4 sem Cluster Autoscaler/Karpenter: o node group nunca escala sozinho**  
  `terraform/cluster/variables.tf:108` · verificação: confirmado · severidade original: média · esforço P · requisitos: REQ-OBR-05, REQ-OBR-23  
  **Problema:** Sem um autoscaler de nós, o tamanho do managed node group fica em desired_size. min/max só limitam ajustes manuais. Se o HPA (até 2 réplicas) ou a stack nova não couberem nos 2 nós, os pods ficam Pending e nenhum nó novo aparece. O comentário dá a falsa impressão de elasticidade, e isso pode aparecer no vídeo ou no relatório como funcionalidade que não existe.  
  **Recomendação:** Uma de duas: (a) assumir capacidade fixa, dimensionando desired_size para o pico (ver TF-CL-01), e corrigir os comentários/descrições para 'limite para ajuste manual'; ou (b) instalar o Cluster Autoscaler via GitOps, com role IRSA mínima e tags k8s.io/cluster-autoscaler/*, e acrescentar lifecycle { ignore_changes = [scaling_config[0].desired_size] } ao node group. Para o prazo e o orçamento, (a) é a mais simples.  
  **Verificação:** modules/eks/main.tf:207 diz 'Maximo, teto do auto scaling' e cluster/variables.tf:105-109 diz 'para o auto scaling do node group'. O grep por autoscaler/karpenter em terraform/gitops/.github só acha o binário do provider e os HPA de pods. Sem autoscaler, o node group fica em desired_size=2. Rebaixo para baixa: os dois HPA têm maxReplicas 2 (gitops/base/*/hpa.yaml:31/35), o que cabe em 2 nós. O impacto real é o comentário enganoso e o sizing da stack nova, que se sobrepõe ao TF-CL-01 citado.

- **TFC-05 — Destroy pode deixar volumes EBS órfãos dos PVCs da stack de observabilidade**  
  `terraform/modules/eks/main.tf:306` · verificação: parcial · severidade original: média · esforço P · já conhecido: Parcial: aviso em terraform/cluster/backend.tf:9-11; o caso dos PVCs criados pel · requisitos: REQ-OBR-03, REQ-OBR-06  
  **Problema:** Hoje o único PVC (postgres-targeting) fica no namespace togglemaster, que é recurso Terraform da camada k8s. O destroy da k8s apaga esse namespace, e o driver CSI, ainda ativo, apaga o disco. Prometheus, Loki e talvez Grafana vão pedir PVCs num namespace criado pelo ArgoCD (fora do Terraform). Esses PVCs sobrevivem ao destroy da camada k8s, e o destroy do cluster remove o driver CSI e os nós sem apagar os volumes. Como o projeto prevê destroy no fim de cada sessão, cada ciclo deixa novos volumes gp3 'available' cobrando, e esses volumes não carregam as default_tags do Terraform.  
  **Recomendação:** Uma de duas: (a) criar o namespace de observabilidade como kubernetes_namespace_v1 na camada k8s, como o namespace app; ou (b) acrescentar ao runbook de destroy, antes do destroy da k8s, a remoção da Application/ns de monitoramento com cascade e a confirmação com kubectl get pvc -A vazio. Na StorageClass, acrescentar tags nos volumes do CSI (parâmetros tagSpecification_N com project=fiap e phase=4) para a checagem de sobras encontrar os discos. Atualizar o filtro de tags do guia, que ainda usa phase=3.  
  **Verificação:** cluster/backend.tf:9-11 já avisa para preservar o EBS CSI até confirmar a remoção dos PVCs/PVs, e o addon ebs_csi está em modules/eks/main.tf:306-313. Hoje o único PVC está em gitops/base/postgres-targeting/statefulset.yaml. A stack de observabilidade ainda não existe, então o cenário de PVCs fora do Terraform é hipotético e depende de como ela for desenhada (namespace, finalizer cascade da Application do ArgoCD). Vale como checklist para o desenho da E-observabilidade e do runbook de destroy, n…

- **TFC-06 — Comentários herdados da conta da Fase 3 com custos, créditos, aprovações e IDs que colidem com o registro da Fase 4**  
  `terraform/cluster/main.tf:19` · verificação: confirmado · esforço P · já conhecido: Parcial: REVISAO_GERAL_INFRA_2026-10-28 I-07 (rds/variables.tf:31, eks/variables · requisitos: REQ-OBR-32  
  **Problema:** Os IDs F-023, D-015 e D-016 nos comentários Terraform apontam para achados/decisões da Fase 3, mas os mesmos números existem em 00_COLAB_IA com outro significado. Quem segue a rastreabilidade cai no item errado. Custo/crédito e 'esta conta recusa' tratam como fato da conta nova algo que não foi verificado nela: o plano de cobrança da conta nova ainda não foi confirmado. Isso pode passar para o relatório PDF como afirmação falsa.  
  **Recomendação:** Prefixar as referências históricas (por exemplo 'F3/F-023', 'F3/D-015'). Reescrever o bloco de custo com a data/fonte da estimativa e marcá-lo como a revalidar na conta nova. Trocar 'esta conta' por 'a conta da Fase 3'. Manter o texto original no histórico do Git.  
  **Verificação:** Conferido em cluster/main.tf:19-22 (US$ 0,385/h; 'restavam US$ 70 de credito'), :72-74 ('aprovado pelo professor'), modules/eks/main.tf:11-14 e eks/variables.tf:30-31 ('Esta conta RECUSA t3.medium (F-023)... (D-016)'), modules/rds/main.tf:4-9 e rds/variables.tf:31-33. Os mesmos IDs têm outro significado no registro atual: F-023 é o subject OIDC (PENDENCIAS:61), D-015 é o README e D-016 é a instrumentação local (DECISOES.md:127,139). Parte já era conhecida (I-07); a colisão de IDs e o bloco de cu…

- **TFC-07 — Endpoint público da API do EKS aberto a 0.0.0.0/0 e sem logs do control plane**  
  `terraform/modules/eks/main.tf:90` · verificação: confirmado · esforço P · requisitos: REQ-OBR-19, REQ-OBR-38  
  **Problema:** A exposição pública é deliberada (comentário em :85-89) e protegida por IAM, o que é aceitável aqui. Mas o default 0.0.0.0/0 expõe a API a varredura de qualquer origem, e sem logs de audit/authenticator não há como provar quem executou o rollout restart do self-healing nem investigar um 'Unauthorized' (ver TF-CL-02). Restringir a um /32 bloquearia os runners hospedados do GitHub, que o self-healing planejado usa.  
  **Recomendação:** Expor public_access_cidrs como variável (default 0.0.0.0/0, documentando o motivo: runners do GitHub com IPs dinâmicos) para poder restringir quando o self-healing não estiver em uso. Opcionalmente, ligar enabled_cluster_log_types = ["audit", "authenticator"] com um aws_cloudwatch_log_group /aws/eks/<nome>/cluster de retenção de 1 a 3 dias criado pelo Terraform, para limitar o custo e o destroy apagar o grupo. Serve de evidência do self-healing (REQ-OBR-38).  
  **Verificação:** modules/eks/main.tf:90 tem endpoint_public_access = true sem public_access_cidrs, e não há enabled_cluster_log_types no recurso (o grep no .tf não acha nenhum dos dois). A exposição é deliberada e está justificada em :85-89, então a severidade baixa está correta. Os logs de audit/authenticator são melhoria opcional e geram custo no CloudWatch.

- **TFC-08 — Redis sem TLS e sem AUTH; o tráfego de banco e cache só é protegido pelo SG**  
  `terraform/modules/elasticache/main.tf:97` · verificação: confirmado · esforço M · já conhecido: Decisão deliberada documentada em terraform/cluster/variables.tf:151-170 · requisitos: REQ-OBR-01  
  **Problema:** Qualquer pod em qualquer nó pode ler e escrever no cache sem credencial, porque o SG de origem é o cluster SG, comum a todos os nós e, portanto, a toda a stack nova (Grafana, Collector, ArgoCD). A decisão está documentada e justificada pelo risco de CrashLoop no boot. Para um projeto acadêmico com dados não sensíveis, o risco é baixo.  
  **Recomendação:** Manter como está até a entrega, mas citar no relatório como trade-off consciente. Se sobrar tempo: ligar o TLS e trocar o REDIS_URL para rediss:// na mesma mudança (o output redis_url já acompanha o esquema). auth_token exige TLS e mudança no cliente, então deixar como melhoria futura.  
  **Verificação:** modules/elasticache/main.tf:97 usa var.transit_encryption_enabled (default false) e não há auth_token no replication group (main.tf:66-105). A decisão já está documentada em cluster/variables.tf:151-170, como o próprio achado reconhece. Na prática, o achado só recomenda registrar o trade-off no relatório.

- **TFC-09 — Senhas RDS repetidas no state (random_password, aws_db_instance, Secrets Manager e output database_urls)**  
  `terraform/modules/rds/main.tf:131` · verificação: confirmado · esforço P · requisitos: REQ-OBR-03  
  **Problema:** sensitive=true só oculta o valor no terminal: a senha fica em texto puro no cluster.tfstate. Quem tiver s3:GetObject no bucket de estado lê as duas senhas, sem registro no Secrets Manager/CloudTrail data events. O desenho é coerente com D-018 (a camada k8s cria o Secret), e o bucket é cifrado e só aceita TLS, por isso a severidade é baixa.  
  **Recomendação:** Garantir que só o usuário/role de administração tenha s3:GetObject no prefixo phase4/ do bucket e que o bucket bloqueie acesso público. Não colar `terraform output -json database_urls` em logs/vídeo. Alternativa futura: a camada k8s ler a URL do Secrets Manager (data aws_secretsmanager_secret_version) em vez do output do remote state, ou usar manage_master_user_password junto com um mecanismo de sincronização.  
  **Verificação:** modules/rds/main.tf:131 usa random_password como senha, e o secret_string com password e DATABASE_URL está em :201-215. A senha fica no state, como é inerente ao Terraform e o próprio comentário em :128-129 admite ('so no estado, que vive cifrado no S3'). A recomendação de restringir s3:GetObject no prefixo do estado faz sentido; baixa está bem calibrada.

- **TFC-10 — Permissões IRSA um pouco acima do uso real**  
  `terraform/modules/irsa/main.tf:101` · verificação: confirmado · esforço P · requisitos: REQ-OBR-01  
  **Problema:** As ações sobram, mas estão limitadas aos ARNs da fila e da tabela do projeto, sem curinga. O impacto é mínimo, porém o menor privilégio é argumento explícito do relatório.  
  **Recomendação:** Remover GetQueueUrl/GetQueueAttributes das duas policies e BatchWriteItem da do analytics, ou registrar no comentário que foram mantidas para uso futuro. Testar com o fluxo real depois do deploy (eventos chegando ao DynamoDB).  
  **Verificação:** modules/irsa/main.tf:95-103 dá ao evaluation SendMessage, GetQueueUrl e GetQueueAttributes; :141-154 dá ao analytics também GetQueueUrl, GetQueueAttributes e BatchWriteItem. Os serviços usam a URL vinda do ambiente: services/evaluation-service/sqs.go:68 chama só SendMessage com QueueUrl, e analytics-service/app.py:23-25,112,123,147 usa receive/delete/put_item. Não achei chamada a GetQueueUrl, GetQueueAttributes nem batch_write. As ações extras estão limitadas aos ARNs do projeto; o impacto é mín…

- **TFC-11 — Security groups de RDS e Redis com egress 0.0.0.0/0 desnecessário**  
  `terraform/modules/rds/main.tf:74` · verificação: confirmado · esforço P  
  **Problema:** RDS e ElastiCache não abrem conexões de saída pela ENI do cliente para funcionar, e o SG é stateful para as respostas. O egress total contradiz o comentário de menor privilégio. O impacto prático é baixo.  
  **Recomendação:** Remover os blocos egress, já que no aws_security_group a ausência de egress em bloco inline remove a regra padrão, ou restringir ao cluster SG. Validar com plan.  
  **Verificação:** Há egress protocol -1 para 0.0.0.0/0 em modules/rds/main.tf:74-81 e modules/elasticache/main.tf:45-51, e os comentários justificam com 'precisa falar com servicos da AWS'. Isso não vale para a ENI do cliente, porque o SG é stateful. O impacto é baixo. Remover exige plan, porque o aws_security_group com egress inline vazio remove a regra padrão.

- **TFC-12 — Camada cluster não verifica se a base criou o NAT Gateway**  
  `terraform/cluster/data.tf:41` · verificação: parcial · esforço P · requisitos: REQ-OBR-03  
  **Problema:** Se o apply da base tiver sido feito com enable_nat_gateway = false, os nós em subnets privadas não conseguem baixar imagens do ECR nem falar com STS. O node group fica cerca de 20 minutos criando e termina em CREATE_FAILED (NodeCreationFailure), consumindo crédito e tempo de sessão.  
  **Recomendação:** Exportar da base um output (por exemplo nat_gateway_ids ou um booleano) e adicionar na camada cluster um bloco check/precondition que falhe no plan quando não houver NAT.  
  **Verificação:** cluster/data.tf:41 lê apenas private_subnet_ids; terraform/variables.tf:100-111 tem enable_nat_gateway com default true e manda usar false só na Etapa 1. O grep não acha output de NAT nem VPC endpoints nos .tf do projeto (as ocorrências estão só em .terraform/modules). O cenário depende de o usuário esquecer o false no tfvars da base. A proteção sugerida (check/precondition) é útil, mas tem pouco peso: o default seguro já existe.

- **TFK-02 — Chart argo-cd 7.7.11 instala Argo CD v2.13.2, fora de suporte e afetado pela CVE-2025-55190 (crítica)**  
  `terraform/k8s/variables.tf:95` · verificação: confirmado · severidade original: média · esforço M · requisitos: REQ-OBR-04, REQ-OBR-05  
  **Problema:** A versão está fixada (bom), mas numa linha sem patches há cerca de um ano e com CVE crítica conhecida. Neste projeto o risco efetivo é baixo: sem Ingress, Service ClusterIP, acesso só por port-forward e sem tokens de projeto. Mesmo assim, a versão aparece no vídeo e no relatório como base de DevSecOps. A combinação com EKS 1.34 funcionou na Fase 3 (LOG da Fase 3: Synced/Healthy), mas o 1.34 não está na matriz testada da 2.13.  
  **Recomendação:** Antes da sessão paga, avaliar um chart com Argo CD 3.x suportado (confirmar a versão exata com 'helm search repo argo/argo-cd --versions'). Revisar as mudanças da 3.0: tracking por anotação como padrão, chaves de configs.params/cm e RBAC de logs. Testar no ensaio. Se o risco de regressão no prazo for alto, subir pelo menos para um chart com appVersion >= v2.13.9 e registrar a decisão e a CVE no relatório.  
  **Verificação:** terraform/k8s/variables.tf:95 fixa default "7.7.11" (também citado no plano 04-plataforma.html:40). A correspondência chart 7.7.11 -> appVersion v2.13.2 e a correção da CVE-2025-55190 na v2.13.9 batem com o que conheço, mas não conferi localmente (não há Chart.yaml no repositório); para confirmar, rode 'helm show chart argo/argo-cd --version 7.7.11'. A linha 2.13 está fora de suporte, mas a exploração exige token de API com permissão de projeto. Aqui não há tokens, não há Ingress e o acesso é só…

- **TFK-04 — Tokens externos (GitHub hoje; New Relic/PagerDuty/Slack/GitHub-dispatch na E2) ficam em texto no state, e o output sugere digitar o token na linha de comando**  
  `terraform/k8s/argocd.tf:81` · verificação: confirmado · severidade original: média · esforço P · já conhecido: Parcial: plano 09-plano-fontes.html linha 164 ('Token do GitHub no Grafana... es · requisitos: REQ-OBR-05, REQ-OBR-17, REQ-OBR-18, REQ-OBR-19  
  **Problema:** 'sensitive = true' so oculta o valor na saida; o state em S3 guarda o conteudo dos Secrets. O bucket e privado, criptografado e versionado, entao cada versao antiga do state tambem guarda o token. Na E2/E5 entra um token do GitHub com permissao de escrita para o repository_dispatch e a chave de ingestao do New Relic, que tem impacto maior se vazar. O exemplo do output deixa o token no historico do PowerShell, enquanto o guia usa 'read -rs'.  
  **Recomendação:** Para os segredos vindos de fora, declarar variable { ephemeral = true; sensitive = true } e usar kubernetes_secret_v1 com data_wo e data_wo_revision. A rotacao passa a ser feita incrementando a revisao. Manter 'data' so para valores gerados aqui (random_password). Trocar o exemplo do output por 'read -rs TF_VAR_github_token; export TF_VAR_github_token' ou por Read-Host -AsSecureString. Usar tokens fine-grained com escopo minimo e prazo de expiracao proximo de 2026-11-17, e registrar a revogacao apos a entrega.  
  **Verificação:** argocd.tf:81 grava password = var.github_token em kubernetes_secret_v1.data, então o valor vai para o state. outputs.tf (output credencial_do_repo_criada, linhas 43-44 do trecho) sugere '$env:TF_VAR_github_token = "ghp_xxxx"' na linha de comando, enquanto docs/GUIA_DE_REPRODUCAO.md:436 usa 'read -rs'. O binário do provider kubernetes 3.2.1 contém 'data_wo_revision' (grep deu 2 ocorrências), e required_version >= 1.11.0 (backend.tf:106) permite write-only. Rebaixo porque o bucket é privado, cript…

- **TFK-07 — Provider AWS sem uso, com guarda de conta ineficaz, e locals mortos (sqs_queue_url, redis_url) com comentarios enganosos**  
  `terraform/k8s/providers.tf:16` · verificação: confirmado · esforço P · já conhecido: Parcial: REVISAO_GERAL_INFRA_2026-10-28_v01.md linha 58 (guard do provider nao c · requisitos: REQ-OBR-03  
  **Problema:** allowed_account_ids (providers.tf:18) passa a impressao de proteger a camada contra a conta errada. Porem o S3 do terraform_remote_state e o 'aws eks get-token' do exec usam as credenciais do ambiente, e um provider sem dependentes normalmente e podado do grafo pelo Terraform (inferencia, nao testada). Ler o state da base so para um local morto cria uma dependencia desnecessaria do output sqs_queue_url. Os comentarios falsos atrapalham quem for manter o codigo.  
  **Recomendação:** Opcao 1: adicionar data "aws_caller_identity" "current" {} com um check/precondition comparando account_id com var.expected_aws_account_id, para tornar a guarda efetiva. Opcao 2: remover o provider AWS e as variaveis associadas. Em ambos os casos, remover os locals sqs_queue_url/redis_url (ou usa-los para gerar ou validar os endpoints) e corrigir os comentarios de providers.tf:4 e backend.tf:19. Avaliar fixar AWS_PROFILE no 'env' do exec.  
  **Verificação:** providers.tf:4 e backend.tf:109 dizem que a camada lê o Secrets Manager, mas o grep por 'aws_' em terraform/k8s/*.tf não acha nenhum recurso nem data source aws_*. Só aparecem o provider (providers.tf:16-25) e o exec 'aws eks get-token'. Os locals sqs_queue_url (data.tf:51) e redis_url (data.tf:69) só aparecem em data.tf. O comentário de data.tf:50 ('Vai para o ConfigMap') é falso. Que allowed_account_ids não tenha efeito porque o provider sem dependentes é podado do grafo é inferência plausível…

- **TFK-08 — Comentarios citam IDs da Fase 3 (F-019, F-020, F-025, F-043, F-046, O-23..O-32) que colidem com a numeracao da Fase 4**  
  `terraform/k8s/argocd.tf:196` · verificação: confirmado · esforço P · requisitos: REQ-OBR-20  
  **Problema:** A rastreabilidade exigida pelo CLAUDE.md fica ambigua: um avaliador ou assistente que procure F-019 no LOG atual encontra outro assunto. O comentario de '2 nos' tambem diverge do plano de 3 nos.  
  **Recomendação:** Prefixar as referencias historicas (por exemplo 'F3-F-020', 'F3-O-23') ou mapea-las para REQ-OBR-xx e D-xxx atuais; atualizar o comentario de dimensionamento quando o terceiro no for decidido.  
  **Verificação:** argocd.tf:196 '(F-020)' e '2 nós c7i-flex.large', secrets.tf:160/188 '(F-019)', variables.tf:70 '(F-019)', storageclass.tf:14 '(F-025)', argocd.tf:2 '(O-23, O-25)'. Em 00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:65-66, F-019 é Collector/OTel no Kubernetes e F-020 é a prova OTel no CI; na linha 25, F-025 é trabalho não comitado. A colisão de numeração existe. O comentário de 2 nós em argocd.tf:135/196 também destoa do plano de 3 nós. É problema só de documentação.

- **TFK-09 — Release do ArgoCD sem requests/limits, sem atomic/cleanup_on_fail e com o Secret de senha inicial mantido**  
  `terraform/k8s/argocd.tf:197` · verificação: confirmado · esforço P · requisitos: REQ-OBR-05  
  **Problema:** Quando kube-prometheus-stack, Loki e os dois Collectors forem para os mesmos nos, componentes sem requests sao os primeiros a sofrer com falta de memoria e podem ser despejados durante a gravacao. Se o wait de 600 s estourar, a release fica 'failed' e o proximo apply exige intervencao manual. Manter o Secret de senha inicial e boa pratica ausente, de baixo risco porque o acesso e so por port-forward.  
  **Recomendação:** Definir requests modestos (por exemplo controller/repoServer/server/redis) nos values; adicionar atomic = true (ou cleanup_on_fail = true). Depois do primeiro login, trocar a senha e apagar argocd-initial-admin-secret, ou definir configs.secret.argocdServerAdminPassword (bcrypt) a partir de variavel sensivel.  
  **Verificação:** argocd.tf:197-207 define só replicas = 1, sem 'resources'. O helm_release (argocd.tf:94-214) tem wait/timeout, mas não tem atomic nem cleanup_on_fail. O output argocd_senha_inicial manda ler argocd-initial-admin-secret e não diz para apagá-lo depois. O risco de despejo cresce com a stack de observabilidade nos mesmos nós, mas continua baixo. Severidade baixa adequada.

- **TFK-10 — Higiene: lock com restricoes antigas, variavel project_name sem uso, providers random/aws sem teto e tfvars.example desalinhado**  
  `terraform/k8s/.terraform.lock.hcl:30` · verificação: confirmado · esforço P · requisitos: REQ-OBR-03  
  **Problema:** Nao quebra o validate, mas o lock nao reflete as restricoes declaradas, o que gera diff no proximo init e dificulta revisao. Variavel morta e restricoes abertas destoam do cuidado aplicado a kubernetes/helm.  
  **Recomendação:** Rodar 'terraform -chdir=terraform/k8s providers lock -platform=windows_amd64 -platform=linux_amd64' na proxima janela autorizada de init e comitar o lock; remover project_name ou usa-lo; usar '~> 6.0' (aws) e '~> 3.5' (random); alinhar o tfvars.example manualmente.  
  **Verificação:** No .terraform.lock.hcl, a linha 30 (helm) tem constraints ">= 2.13.0" e a linha 51 (kubernetes) tem ">= 2.30.0", enquanto backend.tf:122/131 exige "~> 3.0". backend.tf:112 (aws ">= 5.46") e :137 (random ">= 3.5") não têm teto. variables.tf:51 project_name não é referenciado em nenhum outro .tf (grep). terraform.tfvars.example:8-9 tem o '=' desalinhado. Tudo confirmado; é só higiene, sem efeito no validate.

- **XCL-07 — DECISOES não registra as decisões vigentes da Fase 4 e mantém status vencidos**  
  `00_COLAB_IA/DECISOES.md:93` · verificação: parcial (Claude) · severidade original: média · esforço P · requisitos: REQ-OBR-39, REQ-OBR-40  
  **Problema:** O relatório PDF precisa de justificativas (REQ-OBR-40 e arquitetura em REQ-OBR-39), e a decisão de segurança mais importante desde a importação (trust OIDC) só existe no LOG e no código. Status abertos em decisões já superadas confundem quem lê o registro.  
  **Recomendação:** Acrescentar D-017..D-02x curtos (contexto, decisão, alternativas, data, fonte) para os itens listados; marcar D-010, D-011 e D-013 como 'substituída por D-012/D-014' sem apagar o texto; atualizar o cabeçalho e o índice do DOSSIE §6.  
  **Verificação:** Exagerado: DECISOES.md:73 registra New Relic, Slack, self-healing por repository_dispatch e PagerDuty; faltam só decisões mais recentes (bucket -an, trial do PagerDuty).

- **XCL-11 — Namespace togglemaster definido em três fontes com donos diferentes**  
  `terraform/k8s/variables.tf:73` · verificação: nao_verificado · esforço P  
  **Problema:** Se app_namespace mudar só na camada k8s, a IRSA continua amarrada a togglemaster e os pods recebem AccessDenied em tempo de execução, sem erro de deploy (o próprio cluster/outputs.tf:84 alerta para isso). O Namespace com dois donos (Terraform e ArgoCD) complica a remoção e a reconciliação, e a mesma ambiguidade vai se repetir no namespace da stack de observabilidade.  
  **Recomendação:** Tornar a camada cluster a fonte (variável + output app_namespace), fazer a k8s ler via remote_state e retirar namespace.yaml do GitOps (CreateNamespace já está na Application) ou anotá-lo com `argocd.argoproj.io/sync-options: Prune=false`. Para a stack, definir já o nome do namespace (ex.: observability) num único lugar.

- **XCL-12 — Configuração ativa remete ao guia histórico, que ensina a trocar o ID da conta antiga em arquivos que já usam sentinelas e vars**  
  `gitops/overlays/prod/patches/endpoints.yaml:12` · verificação: confirmado (Claude) · esforço M · já conhecido: I-04 (REVISAO_GERAL_INFRA) e F-021 (runbook vigente ausente). Novo: a remissão e · requisitos: REQ-OBR-23  
  **Problema:** Para a conta nova, o arquivo operacional manda o leitor a um procedimento que se declara não executável e cujos comandos não fazem mais nada ou induzem ao erro. O roteiro vigente de troca das sentinelas, seed e bootstrap em duas etapas não existe.  
  **Recomendação:** Criar docs/RUNBOOK_FASE4.md (ou uma seção no terraform/README) com: outputs → endpoints.yaml/irsa.yaml, bootstrap do ArgoCD em duas etapas, schemas/seed e SERVICE_API_KEY. Atualizar as 5 remissões para apontar para ele.  
  **Verificação:** Conferido: gitops/overlays/prod/patches/endpoints.yaml:12 remete ao GUIA histórico, seções 2 e 6.

- **XCL-13 — Teste de regressão da trust OIDC vive numa cópia do módulo fora do CI**  
  `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/harness/tests/trust.tftest.hcl:0` · verificação: nao_verificado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** A garantia de que só main e o subject imutável assumem a role (8/8 testes) não acompanha o módulo. Qualquer edição futura em iam-ci (por exemplo, para a role de self-healing do T-08) pode afrouxar a trust sem teste nenhum falhar, e a cópia vai divergir em silêncio.  
  **Recomendação:** Mover o teste para terraform/modules/iam-ci/tests/ (com mock_provider/override_data para rodar offline) e acrescentar um passo `terraform -chdir=terraform/modules/iam-ci init -backend=false && terraform test` ao terraform-check.yml. Apagar a cópia do harness depois de conferida, com autorização.

- **XCL-14 — Varredura de segredos não protege contra o retorno da conta da Fase 3 aos arquivos operacionais**  
  `scripts/security-check.sh:78` · verificação: nao_verificado · esforço P · requisitos: REQ-OBR-04  
  **Problema:** Copiar um trecho do guia histórico ou do _ARQUIVO_MORTO/FASE3_BASE_6100879 (rastreado, com workflows e overlay da conta antiga) para um arquivo operacional passaria pelo validate-all e pelo CI. O provider Terraform barra a conta errada (allowed_account_ids), mas o GitOps e os workflows não.  
  **Recomendação:** Acrescentar uma regra restrita aos caminhos operacionais: `git grep -InE '<ID Fase 3>' -- '*.tf' '*.yml' '*.yaml' ':!00_COLAB_IA' ':!docs'`, ou, de forma genérica, recusar `arn:aws:iam::[0-9]{12}` e `[0-9]{12}\.dkr\.ecr` em gitops/ e .github/ (onde só deveriam existir sentinelas ou `vars`).

- **XCL-15 — Lockfiles do provider AWS divergem entre camadas**  
  `terraform/.terraform.lock.hcl:0` · verificação: confirmado (Claude) · esforço P  
  **Problema:** As três camadas do mesmo ambiente rodam versões diferentes do provider. A diferença é pequena, mas complica reproduzir um bug ou comparar plans entre camadas e cria uma segunda atualização de lock quando a base for inicializada.  
  **Recomendação:** Na próxima inicialização autorizada da base, alinhar com `terraform -chdir=terraform init -upgrade -backend-config=backend.hcl` (ou fixar `version = "~> 6.63"` nas três raízes) e comitar as três locks juntas.  
  **Verificação:** Conferido: lock da base com aws 6.62.0; cluster e k8s com 6.63.0.

## Apêndice B — Requisitos: o que falta em detalhe

Lista completa das tarefas, na ordem de execução, com dependências e riscos. Quando a auditoria mudou o status, a justificativa aparece como "Ajuste da auditoria".

### REQ-OBR-01 — 🟨 parcial

Manter toda a base das Fases 1, 2 e 3 funcionando (pré-condição da Fase 4, p. 2). Hoje ela funciona só no laboratório local: Compose com Moto no lugar de SQS/DynamoDB. Não há nada implantado na conta nova nem código no repositório remoto.

**Ajuste da auditoria** (era 🟨 parcial): Status e evidências conferem: git branch -avv mostra 'dev 3b21e65 [origin/dev: ahead 103]'; git status tem 40 M, 34 D e 73 entradas ??; offline-test.jsonl tem 156400265 bytes e `git check-ignore` retorna rc 1; o log passo2-compose-sql-final.log:392 e :405 traz as linhas PASS. Nenhum arquivo de services/, scripts/ ou compose foi alterado depois do log de 2026-10-27 11:03, exceto scripts/security-check.sh (find -newer), então a prova local continua representativa do código atual. A lista 'falta' cita a curadoria só para 'instrumentação, testes, ajustes de Terraform' e omite as 34 exclusões, que um `git add -A` comitaria.

**Falta:**

1. Resolver F-024 antes de qualquer commit: ignorar 00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/offline-test.jsonl (156 MB). Aceite: `git check-ignore` reconhece o arquivo.
2. Fazer a curadoria e o commit do trabalho local (instrumentação, testes, ajustes de Terraform) e, com autorização, enviar a dev ao remoto. Aceite: origin/dev contém .github/workflows, gitops/, terraform/ e services/.
3. Concluir REQ-OBR-03: tfvars, reconciliação dos recursos manuais, init/plan/apply da base.
4. Concluir REQ-OBR-04: CI verde na dev e publicação das cinco imagens a partir da main.
5. Concluir REQ-OBR-05: cluster, endpoints do overlay, ArgoCD Synced/Healthy.
6. Seguir a seção 8 de docs/GUIA_DE_REPRODUCAO.md: schemas do auth e do flag via psql, chave de serviço gravada no Secret, flag e regra de exemplo.
7. Seguir a seção 9 do guia (verificação ponta a ponta no cluster): pods 1/1, HPA com TARGETS, /evaluate true, Cache MISS→HIT, Count>0 no DynamoDB e fila perto de 0. Salvar a saída em 00_COLAB_IA/02_TRABALHO como evidência.
8. Corrigir F-027 (HPA × selfHeal) antes de demonstrar o escalonamento.
9. Na curadoria do commit, decidir explicitamente sobre as 34 exclusões rastreadas (git status ' D': docs/POSTECH - Tech Challenge - Fase 3.pdf e docs/aulas-fiap/**). Fazer commit delas sem decisão contraria a regra 'Manter originais' do CLAUDE.md (F-025).

**Depende de:** REQ-OBR-02; REQ-OBR-03; REQ-OBR-04; REQ-OBR-05; Autorização do usuário para commit/push/PR/merge e para operações AWS; Confirmação de créditos e cobrança da conta nova (F-026)

**Etapa do plano:** E0 e E2 (09-plano-fontes.html: "E0 e E2 cobrem 01–05") · **Esforço:** G

**Risco:** Prazo: a base precisa estar rodando no cluster cedo, porque E3–E5 dependem dela e o trial do PagerDuty acaba por volta de 2026-11-11. Custo: estimativa da Fase 3 de cerca de US$ 0,47/h com 3 nós, e créditos não confirmados (F-026). Publicação: o arquivo de 156 MB não ignorado pode barrar o push (F-024).

### REQ-OBR-02 — ✅ concluído com evidência

Os cinco microsserviços estão conteinerizados: Dockerfiles multi-stage com usuário não-root, e build e execução conjunta via Compose comprovados localmente em 2026-10-27.

**Falta:**

1. Versionar as alterações dos três Dockerfiles Python e os demais arquivos de serviço, junto com o commit de REQ-OBR-01.
2. Publicar as cinco imagens no ECR pelo CI da main e conferir as tags. Isso se cumpre em REQ-OBR-04.
3. Mostrar os cinco pods Running com as imagens do ECR no EKS. Isso se cumpre em REQ-OBR-05 e no vídeo (REQ-OBR-25).

**Depende de:** Commit das alterações locais (F-025)

**Etapa do plano:** E0/E2 · **Esforço:** P

**Risco:** Baixo para a conteinerização em si. O risco residual é de publicação: as alterações não versionadas não chegam ao CI nem ao ArgoCD, e os scans de imagem das dependências OTel novas ainda não rodaram no CI, com exceções Trivy vencidas (F-022).

### REQ-OBR-03 — 🟨 parcial

A infraestrutura por Terraform está organizada em três camadas (base: VPC/ECR/SQS/DynamoDB/IAM CI; cluster: EKS/RDS/ElastiCache/IRSA; k8s: ArgoCD/Secrets/StorageClass) e passa em fmt/validate. Faltam os parâmetros da conta nova, a reconciliação dos recursos criados à mão e o dimensionamento para a Fase 4. Nada foi aplicado.

**Falta:**

1. Confirmar créditos, cobrança, orçamento e a cota de vCPU On-Demand (guia, seção 1, linha 113: 8 ou mais), além do suporte do EKS 1.34 em us-east-2 (F-026).
2. Criar terraform.tfvars nas três camadas, fora do Git: expected_aws_account_id, state_bucket, create_github_oidc_provider = false (o provedor já existe), enable_nat_gateway conforme o custo.
3. Definir o tratamento dos recursos manuais: blocos `import` ou `terraform import` com autorização para os cinco aws_ecr_repository, aws_iam_role, aws_iam_policy, attachment e o OIDC lido via data. Revisar thumbprints e lifecycle para não haver drift destrutivo.
4. Ajustar a capacidade para a stack da Fase 4 (node_group_desired_size 3 ou tipo maior) e, se o plano mantiver, o namespace observability e os Secrets novos na camada k8s.
5. Com autorização: init da base, depois plan revisado (zero destroy/replace nos recursos importados) e apply. Em seguida cluster e k8s em duas etapas (guia, seção 7). Salvar plan/apply resumidos e `terraform output` como evidência.

**Depende de:** Autorização do usuário para init/import/plan/apply; Créditos e cotas da conta nova (F-026); Inventário da etapa 8 (já existe)

**Etapa do plano:** E0 (parâmetros, inventário) e E2 (apply das três camadas) · **Esforço:** M

**Risco:** Custo por hora do EKS, RDS, ElastiCache e NAT (estimativa da Fase 3: cerca de US$ 0,47/h com 3 nós), com créditos não confirmados. Um apply sem import falha por recurso já existente (ECR/IAM). Com create_github_oidc_provider=true, tentaria criar um provedor duplicado. Trocar thumbprints ou lifecycle sem querer pode quebrar o CI. Prazo: toda a cadeia E3–E5 depende deste apply.

### REQ-OBR-04 — 🟦 implementado, falta demonstrar

Pipelines GitHub Actions com DevSecOps: build, testes, lint, SAST (gosec/bandit), SCA (Trivy fs), scan de imagem (Trivy image), OIDC sem chave estática, push ECR e atualização da tag no GitOps. Tudo declarado, mas nunca executado no repositório 04, porque o remoto não tem os workflows.

**Falta:**

1. Resolver F-024 e fazer a curadoria do commit (F-025). Com autorização, push da dev. Aceite: os cinco workflows de serviço, Terraform Check e Compose Integration rodam verdes na dev do repo 04.
2. Revisar as exceções do .trivyignore com scan das imagens finais com OTel (F-022). Recomendado: incluir .trivyignore/.pylintrc nos paths (F-030) e renderizar gitops no CI (F-029).
3. Com autorização, abrir PR dev → main e fazer o merge. Aceite: os cinco runs da main completam com os jobs image e gitops verdes, as tags aparecem no ECR e o robô comita v1.0.0-<sha7> no overlay.
4. Registrar a evidência (gh run list/view, prints) para o relatório. Opcional para o vídeo: demonstração do gate barrando CVE (guia, Apêndice B).

**Depende de:** Autorização do usuário para commit/push/PR/merge na main; REQ-OBR-03 não é pré-requisito para o CI na dev; para o push no ECR bastam os repositórios e a role que já existem; Política de proteção da main permitir o push do job gitops (não verificado)

**Etapa do plano:** E0 (CI verde na dev) e E2 (merge dev → main para publicar as imagens instrumentadas) · **Esforço:** M

**Risco:** Sem nenhuma execução remota até hoje, falhas de ambiente (Actions, OIDC, thumbprints, permissões de push na main) aparecem só agora. O repositório é privado de organização: a cota de minutos do GitHub Actions depende do plano da organização, não verificado. Gates CRITICAL do Trivy podem barrar as imagens com dependências OTel novas e consumir prazo.

### REQ-OBR-05 — 🟨 parcial

Implantação no EKS gerenciada por ArgoCD: Application (automated, prune, selfHeal) criada pelo Terraform, apontando para gitops/overlays/prod no repo 04/main. O overlay renderiza 23 objetos, mas imagens, REDIS_URL, URL do SQS e ARNs IRSA ainda são sentinelas, o remoto não tem gitops/ e há conflito entre HPA e selfHeal.

**Ajuste da auditoria** (era 🟨 parcial): O status parcial se confirma. Reexecutei `kubectl kustomize gitops/overlays/prod` com rc 0 e 23 objetos; há seis `replicas: 1` no render e não há ignoreDifferences em terraform/k8s/argocd.tf (só prune e selfHeal em :320 e :325). Os sentinelas estão em kustomization.yaml:67-80 e em endpoints.yaml:31/39/49. A citação de irsa.yaml, porém, está errada: `wc -l` dá 43 linhas, e o grep mostra CONTA_AWS_PENDENTE nas linhas 31 e 43. Confirmei também que o job gitops (_ci-go.yml, passo 'Atualizar a tag e enviar') usa `kustomize edit set image <svc>=${ECR_REGISTRY}/<svc>:<tag>`, ou seja, troca o registry e a tag, o que sustenta a afirmação de que o CI corrige as imagens sozinho.

**Falta:**

1. Publicar a base no remoto: dev → PR → main, com autorização (depende de REQ-OBR-04).
2. Corrigir F-027: ignoreDifferences em /spec/replicas restrito a evaluation-service e analytics-service, com RespectIgnoreDifferences=true, ou remover replicas desses Deployments.
3. Depois do apply da base: substituir AWS_SQS_URL e os ARNs IRSA, que já são previsíveis pelo ID da conta. As tags das imagens o CI grava sozinho.
4. Apply da camada cluster, depois REDIS_URL real no endpoints.yaml, com commit e merge na main (guia, seção 6). `aws eks update-kubeconfig`; nós Ready.
5. Apply da camada k8s em duas etapas (só helm_release.argocd, depois o restante), com TF_VAR_github_token de escopo mínimo (guia, seção 7).
6. Aceite: Application Synced/Healthy; cinco pods e postgres-targeting-0 1/1; inicializar schemas e chave (seção 8) e rodar o teste funcional (seção 9), não só Running/Synced. Fazer prints da UI do ArgoCD via port-forward para o vídeo (REQ-OBR-25).
7. Corrigir a evidência: os ARNs IRSA sentinela estão em gitops/overlays/prod/patches/irsa.yaml:31 e :43 (o arquivo tem 43 linhas), não em :80 e :92.

**Depende de:** REQ-OBR-03 (cluster e k8s aplicados); REQ-OBR-04 (imagens no ECR e tags no overlay); Push da dev para o remoto e merge na main (autorização do usuário); Token GitHub com leitura do repo privado

**Etapa do plano:** E2 (a stack de observabilidade por GitOps vem depois, em E3) · **Esforço:** M

**Risco:** F-027 pode desfazer o escalonamento do HPA durante a demonstração. A primeira aplicação da Application exige o CRD (aplicar em duas etapas). Com só 2 nós (default), a stack da E3 pode deixar pods em Pending. O token do GitHub no cluster precisa ser revogado depois da entrega. O cluster ligado custa por hora, então convém sincronizar e testar em sessões curtas.

### REQ-OBR-06 — ⬜ ausente

Provisionar no cluster a stack de observabilidade (Prometheus, Loki, Grafana e Collector) declarada como Helm charts no repositório GitOps.

**Ajuste da auditoria** (era ⬜ ausente): O status 'ausente' está correto: o render 'kubectl kustomize gitops/overlays/prod' dá 23 objetos, nenhum da stack, e o rg no repositório inteiro (com arquivos ignorados, fora de docs/ e 00_COLAB_IA/) não acha prometheus, loki, grafana nem Application de observabilidade. Os ajustes tratam de omissões na lista 'falta'. (1) O namespace com Secrets precisa vir do Terraform, como o plano já define (09-plano-fontes.html:40). (2) O terceiro nó está fora de ordem: é uma mudança de tfvars da E2 e sai mais barata agora, porque os tfvars ainda não existem. (3) O risco considerou só a meta de 2026-11-12, não o trial do PagerDuty (~2026-11-11), que depende desta stack. O registro do Codex na matriz já marcava o requisito como pendente; esses três pontos não estavam na avaliação.

**Falta:**

1. Decidir e registrar as versões fixas dos charts (kube-prometheus-stack, loki, opentelemetry-collector e Grafana embutido) reconsultando a documentação oficial: as versões do plano (91.5.0 e 0.173.1) são de 2026-09-23
2. Criar gitops/observability/ com uma Application Helm por chart (targetRevision fixo, values versionados, ServerSideApply=true para os CRDs do kube-prometheus-stack) e o namespace observability
3. Acrescentar em terraform/k8s/argocd.tf a Application 'observability' (app of apps) apontando para gitops/observability/, ou incluir as Applications por outro caminho declarado no Git
4. Dimensionar o cluster: hoje node_group_desired_size = 2 (terraform/cluster/variables.tf:95-103); o plano pede 3 nós. Definir requests/limits e retenção/PVC de Prometheus e Loki
5. Validar localmente: kubectl kustomize/helm template dos values e terraform validate
6. Depois da E2 (cluster no ar), sincronizar e registrar print/saída das Applications Synced/Healthy e dos pods Running no namespace observability
7. Criar o namespace 'observability' pelo Terraform k8s, no mesmo padrão de kubernetes_namespace_v1.app (terraform/k8s/secrets.tf:27-38). Os Secrets novos (admin do Grafana e license key do New Relic) nascem no Terraform antes do sync, então o namespace precisa existir antes deles. O plano já prevê isso (09-plano-fontes.html:40, 'Terraform: terceiro nó, namespace observability, Secrets novos'), mas a lista 'falta' coloca o namespace só em gitops/observability/.
8. Trazer o dimensionamento para o começo da lista: gravar node_group_desired_size = 3 no terraform.tfvars da camada cluster na hora de criá-lo (o arquivo ainda não existe), antes do apply da E2. O default continua 2 (terraform/cluster/variables.tf:95-103) e o plano pede 3 (04-plataforma.html:118; 08-exibicao-mudancas.html:53).
9. Conferir na documentação do ArgoCD se a versão instalada pelo chart argo-cd 7.7.11 (terraform/k8s/variables.tf:95) aceita Application com várias fontes (chart Helm externo mais values no Git). Se não aceitar, usar values inline ou um chart wrapper. O project 'default' não tem restrições (argocd.tf:277-278), então os repositórios Helm externos são aceitos.
10. Prazo real: a stack (Prometheus e Grafana) precisa estar sincronizada antes de o trial do PagerDuty acabar, por volta de 2026-11-11. A regra de alerta fica no Grafana (02-alto-nivel.html:139), e a evidência alerta -> PagerDuty -> Slack tem de ser gravada dentro do trial (PENDENCIAS_E_PROXIMOS_PASSOS.md:113, 'Events' 'Not included' no Free). Hoje o risco cita só a meta de 2026-11-12.

**Depende de:** E2: cluster EKS e camada k8s aplicados na conta nova (reconciliação P-003 e correção F-023 antes do apply); Confirmação de créditos/plano de cobrança da conta AWS (F-026); Autorização de deploy (CLAUDE.md: nenhum deploy autorizado nesta etapa); Publicação na branch observada pelo ArgoCD (gitops_repo_branch = main): exige commit/push/merge, hoje não autorizados

**Etapa do plano:** E3 · **Esforço:** G

**Risco:** Prazo: faltam 13 dias para a meta interna (2026-11-12) e nada da E2 foi aplicado. Custo: cerca de US$ 0,47/h com 3 nós (estimativa da Fase 3, 09-plano-fontes.html), sem incluir os volumes EBS de Prometheus e Loki (09-plano-fontes.html:146); créditos da conta nova não confirmados. Capacidade: c7i-flex.large com 2 nós por padrão; a stack (Prometheus, node-exporter por nó, kube-state-metrics, Grafana, Loki, 2 releases do Collector) pode deixar pods em Pending. O limite de pods por nó desse tipo de instância precisa ser conferido na documentação da AWS. CRDs grandes do kube-prometheus-stack podem falhar no apply client-side do ArgoCD.

### REQ-OBR-07 — ⬜ ausente

Prometheus no cluster para armazenar e consultar métricas de infraestrutura.

**Ajuste da auditoria** (era ⬜ ausente): O status está certo. O grep não acha 'prometheus' em gitops/, terraform/ nem .github/, e o único coletor de métricas é o addon metrics-server (terraform/modules/eks/main.tf:317), que serve ao HPA. A omissão é na configuração: a lista cobre remote write, retenção, PVC e Alertmanager desligado, mas não o ajuste dos scrapes de control plane para EKS. Esse ponto não estava na avaliação nem no plano: o grep por kubeControllerManager/kubeScheduler em plano-fase4/partes não acha nada. É uma recomendação a confirmar na documentação oficial do kube-prometheus-stack.

**Falta:**

1. Values do kube-prometheus-stack com prometheus.prometheusSpec.enableRemoteWriteReceiver: true (ou enableOTLPReceiver), retenção curta, PVC gp3 dimensionado, alertmanager.enabled: false se a regra ficar no Grafana, e node-exporter e kube-state-metrics habilitados
2. Conferir se os seletores de ServiceMonitor/PodMonitor atendem ao que será coletado
3. Depois de implantado: consultar no Prometheus (port-forward) uma métrica de nó/pod, por exemplo node_cpu_seconds_total ou container_memory_working_set_bytes, e registrar a saída ou o print
4. Conferir o nome real das métricas do spanmetrics que chegam por remote write (o plano deixa marcado como <calls>, 08-exibicao-mudancas.html)
5. Nos values do kube-prometheus-stack, desligar os alvos de plano de controle que o EKS gerenciado não expõe para scrape direto: kubeControllerManager, kubeScheduler, kubeEtcd, e conferir o kubeProxy. Revisar também as defaultRules. Sem isso, o Prometheus pode ficar com alvos down e alertas como TargetDown disparando sem parar, o que é ruído na gravação e contradiz o tema de alert fatigue. Isto vem da documentação do chart e da AWS e precisa ser conferido para a versão escolhida.

**Depende de:** REQ-OBR-06 (Application e chart); E2: cluster no ar; REQ-OBR-11 para as métricas de aplicação (spanmetrics -> remote write)

**Etapa do plano:** E3 · **Esforço:** M

**Risco:** Consumo de memória e disco do Prometheus num cluster de 2 a 3 nós pequenos; volume EBS fora da estimativa de custo; o nome das métricas do spanmetrics após a conversão é incerto e o conector é alpha (06-telemetria.html:95).

### REQ-OBR-08 — ⬜ ausente

Loki no cluster para centralizar e indexar os logs de todos os contêineres do cluster.

**Ajuste da auditoria** (era ⬜ ausente): O status 'ausente' está confirmado: grep 'loki' em gitops/, terraform/ e .github/ sem resultado, e observability/README.md:21 diz 'Ainda não há ... coleta de logs pelo Collector, Loki'. A lista 'falta' não cobre dois riscos de capacidade e configuração do chart do Loki: os caches e o canary ligados por padrão, e a retenção, que depende do compactor. São justamente os que fariam o Loki não subir no cluster de 2 a 3 nós pequenos. Os padrões do chart precisam ser confirmados na documentação da versão fixada.

**Falta:**

1. Values do chart do Loki em modo SingleBinary, com PVC gp3, retenção curta e allow_structured_metadata (padrão a partir do Loki 3.0, segundo o plano)
2. Release 'agent' do opentelemetry-collector como DaemonSet com os presets logsCollection e kubernetesAttributes, cobrindo todos os namespaces (o PDF pede 'todos os logs dos contêineres do cluster', não só o togglemaster)
3. Pipeline de logs no gateway exportando para o Loki em /otlp
4. Depois de implantado: consultar no Grafana Explore logs de pelo menos um pod de cada namespace (togglemaster, argocd, observability, kube-system) e uma busca por trace_id; registrar print
5. Conferir no values.yaml da versão escolhida do chart do Loki os componentes que vêm ligados por padrão: chunksCache e resultsCache (memcached), lokiCanary (um por nó), gateway e pod de teste. Desligar ou dimensionar cada um. Em versões 6.x o chunksCache reserva vários GiB, o que deixaria pods em Pending em nós c7i-flex.large (terraform/cluster/variables.tf:86). Confirmar na documentação.
6. Para a 'retenção curta' valer de fato, ligar o compactor com retention_enabled e um armazenamento de delete requests (conferir na documentação do Loki). Configurar só o PVC não apaga dados.
7. Passar para a lista 'falta' (hoje está só em observações) a decisão de sanitizar logs: a config local só tem trace_statements (observability/otel-collector-local.yaml:26-40). Se os logs forem também ao New Relic, criar log_statements equivalentes.

**Depende de:** REQ-OBR-06; REQ-OBR-11 (pipeline de logs do Collector); E2: cluster no ar

**Etapa do plano:** E3 · **Esforço:** M

**Risco:** Volume de logs (ArgoCD, kube-system) aumenta disco e memória do Loki; a falta de filtro pode encher o PVC. Se o filtro for restrito ao togglemaster, o requisito 'todos os contêineres' deixa de ser atendido. Logs do Gunicorn e do SDK não seguem o JSON (observability/README.md:63).

### REQ-OBR-09 — ⬜ ausente

Grafana como ferramenta principal de visualização, com fontes de dados Prometheus e Loki.

**Falta:**

1. Habilitar o Grafana no values do kube-prometheus-stack (ou um chart próprio) com datasources provisionados: Prometheus (o do chart) e Loki (URL do serviço do Loki), com correlação de trace_id para o New Relic, se desejada
2. Senha de admin vinda de Secret criado fora do Git (Terraform k8s ou existingSecret), sem valor versionado
3. Sidecar de dashboards e de alertas habilitado com o rótulo combinado
4. Depois de implantado: port-forward, testar os datasources ('Data source is working') e registrar print

**Depende de:** REQ-OBR-06; REQ-OBR-07 e REQ-OBR-08 (datasources); E2: cluster no ar

**Etapa do plano:** E3 · **Esforço:** P

**Risco:** Baixo isoladamente. Um Secret de admin mal tratado violaria a regra de não versionar segredos (D-013, gitops/base/kustomization.yaml:76-84).

### REQ-OBR-10 — ⬜ ausente

Pelo menos um dashboard customizado no Grafana com (a) recursos do cluster, (b) taxa de requisições dos microsserviços e (c) logs em tempo real.

**Ajuste da auditoria** (era ⬜ ausente): O status está certo: nenhum JSON de dashboard ou rótulo grafana_dashboard no repositório (rg por '"panels"' e 'grafana_dashboard' só acha planos). A omissão é de mitigação. Hoje o painel (b) depende só do spanmetrics alpha, e a avaliação deixou o MeterProvider como observação em REQ-OBR-11 em vez de colocá-lo como alternativa concreta na lista deste requisito, que é o mais afetado. Os itens de uid fixo e de logs ao vivo são detalhes de implementação que evitam painéis vazios ou quebrados na gravação; precisam ser confirmados na documentação oficial.

**Falta:**

1. Implantar o spanmetrics (REQ-OBR-11) e ler no Prometheus o nome real da métrica de chamadas e dos rótulos (service_name, span_kind, status_code)
2. Escrever o dashboard JSON versionado em ConfigMap com rótulo grafana_dashboard em gitops/observability/: painel (a) CPU e memória por nó e por pod (node-exporter, cAdvisor, kube-state-metrics); painel (b) rate por serviço, só spans SERVER; painel (c) tipo Logs com consulta LogQL ao namespace togglemaster e refresh curto ou live
3. Gerar carga (requisições de avaliação) e registrar print do dashboard com os três painéis com dados, que é evidência obrigatória do relatório (Print do Dashboard do Grafana, p. 6)
4. Plano B para o painel (b), para não depender só do conector spanmetrics, que é alpha (06-telemetria.html:95): registrar um MeterProvider OTLP nos serviços. otelhttp (Go) e FlaskInstrumentor (Python) já emitem métricas HTTP quando há MeterProvider global; hoje go.opentelemetry.io/otel/metric é só dependência indireta (services/auth-service/go.mod:28; services/evaluation-service/go.mod:33) e não há MeterProvider (grep sem resultado). Isso também reduz o risco da leitura estrita de Q-08. Conferir os nomes das métricas nas versões fixadas.
5. Provisionar os datasources Prometheus e Loki com uid fixo e referenciar esse uid no JSON do dashboard, para o ConfigMap carregado pelo sidecar não quebrar.
6. Conferir na documentação do Grafana como mostrar 'logs em tempo real': o painel Logs de um dashboard trabalha por refresh, e o Live tailing é do Explore. Decidir se o vídeo mostra refresh curto no painel e o Live no Explore.

**Depende de:** REQ-OBR-07, REQ-OBR-08, REQ-OBR-09; REQ-OBR-11 (spanmetrics para o painel b); Imagens instrumentadas publicadas no ECR e variáveis OTEL_* nos ConfigMaps (o overlay ainda usa sentinelas: gitops/overlays/prod/kustomization.yaml:147-164)

**Etapa do plano:** E4 · **Esforço:** M

**Risco:** O spanmetrics é alpha e o nome da métrica é incerto, o que pode deixar painéis vazios na gravação. O cache de 30 s do evaluation reduz chamadas a flag/targeting/auth, então a taxa desses serviços aparece baixa sem um gerador de carga (risco listado no plano). O prazo depende do cluster ligado para desenhar o dashboard; uma alternativa é ensaiar Grafana, Prometheus e Loki no Compose (pergunta em aberto em PENDENCIAS:76 e 163).

### REQ-OBR-11 — 🟨 parcial

OTel Collector como peça central: receber, processar e exportar métricas, logs e traces dos microsserviços para Prometheus, Loki e APM.

**Ajuste da auditoria** (era 🟨 parcial): O status 'parcial' está confirmado: só existe o pipeline local de traces (otel-collector-local.yaml:54-60, exporters debug e file/traces), não versionado ('??' no git status), e nada de Collector em gitops/ ou terraform/ (rg 'otel|collector' sem resultado). O que é novo nesta auditoria e não estava nem na avaliação nem no plano: a allowlist de recurso da sanitização, reaproveitada como pede a lista 'falta', apagaria os atributos k8s.*. Além disso, o pipeline de traces do gateway no plano não tem sanitize nem filtro de /health, o que contradiz o README da observabilidade.

**Falta:**

1. Criar values das duas releases do chart opentelemetry-collector (agent DaemonSet e gateway Deployment, imagem contrib fixada) em gitops/observability/
2. Gateway: pipeline traces com k8sattributes, o mesmo transform/sanitize da config local (observability/README.md:63 exige reaproveitá-lo antes de exportar para fora), exporter otlp/otlphttp para otlp.nr-data.net com header api-key vindo de Secret, e conector spanmetrics
3. Gateway: pipeline metrics (spanmetrics -> prometheusremotewrite para /api/v1/write) e pipeline logs (otlp do agent -> otlphttp para o Loki em /otlp)
4. Agent: filelog em /var/log/pods com kubernetesAttributes e export OTLP ao gateway
5. Secret da license key do New Relic criado pelo Terraform (terraform/k8s/secrets.tf hoje não o tem) e documentado em gitops/SECRETS-CONTRATO.md
6. OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_SERVICE_NAME e OTEL_RESOURCE_ATTRIBUTES nos ConfigMaps de gitops/base/*/configmap.yaml apontando para o gateway
7. Validar a config com 'otelcol-contrib validate' localmente (como já feito em scripts/test-observability.sh:17)
8. Ensaio local opcional: estender docker-compose.otel.yaml com Prometheus e Loki para provar os três roteamentos sem cluster
9. Depois de implantado: provar os três sinais (métrica do spanmetrics no Prometheus, log no Loki, trace no New Relic) e registrar
10. Resolver o conflito entre transform/sanitize e k8sattributes. A allowlist de recurso da config local só mantém service.*, deployment.environment.name e telemetry.sdk.* (observability/otel-collector-local.yaml:33). Reaproveitada no gateway depois do k8sattributes, ela apaga k8s.namespace.name, k8s.pod.name e k8s.deployment.name, que os logs, o Loki, o filtro por namespace e a identificação do trace vindo do EKS usam. Ampliar a lista ou ordenar os processadores de propósito.
11. Atualizar o plano: o pipeline de traces do gateway em 06-telemetria.html:88 (memory_limiter, k8sattributes, batch) não tem filter/health nem transform/sanitize, embora observability/README.md:63 exija reaproveitar a sanitização antes de exportar para fora. Definir se o spanmetrics recebe os spans depois do filtro de /health.
12. Ordem: o Secret da license key e o namespace 'observability' (Terraform) precisam existir antes do sync da Application do Collector. Senão o pod do gateway não sobe por falta de variável de ambiente ou Secret.

**Depende de:** E1 externa: conta e license key do New Relic e validação de ingestão; REQ-OBR-06 (charts no cluster); REQ-OBR-07 e REQ-OBR-08 (destinos); Imagens instrumentadas publicadas (overlay com sentinelas conta-pendente); Interpretação Q-08: as métricas de aplicação são derivadas de traces (spanmetrics) e os logs coletados do stdout pelo agent, não enviados por SDK

**Etapa do plano:** E3 · **Esforço:** G

**Risco:** Cota gratuita do New Relic (o plano cita 100 GB/mês, 06-telemetria.html:98) com risco de bloqueio se métricas e logs forem enviados também. O conector spanmetrics é alpha. Pela redação 'Os microsserviços devem enviar os dados de telemetria para o OTel', um avaliador pode esperar métricas e logs saindo dos serviços via OTLP; hoje os serviços só emitem traces (Q-08). O vazamento de dados sensíveis ao exportar para fora depende de reaplicar a sanitização. Prazo e custo seguem os de REQ-OBR-06.

### REQ-OBR-12 — 🟨 parcial

Escolher UMA ferramenta APM (Datadog OU New Relic), usando conta gratuita 'for education' (PDF p. 4).

**Ajuste da auditoria** (era 🟨 parcial): O status 'parcial' é defensável: a escolha está em DECISOES.md:73 e a conta foi relatada pelo usuário, mas não há chave nem ingestão registradas, e Q-04 continua aberta. Há um exagero na lista 'falta' e nas evidências: a avaliação diz que a região US 'vem do contexto da tarefa, sem registro', mas o LOG:36 e PENDENCIAS:113 já a registram (relato do usuário de 2026-10-30).

**Falta:**

1. Na conta New Relic: confirmar a região US, o plano efetivo (Free, 100 GB/mês) e o acesso do usuário ao APM/Distributed Tracing. Registrar a data da conferência e o Account ID mascarado no LOG
2. Gerar a license key (ingest), guardada só localmente ou em gerenciador de segredos, nunca no Git nem no chat
3. Primeira ingestão de prova (ver REQ-OBR-14): um trace chegando ao New Relic encerra o aceite técnico da escolha
4. Perguntar ao tutor (Q-04) se a conta Free comum substitui a conta 'for education', ou procurar o programa educacional oficial, e registrar a resposta
5. Redigir no relatório a justificativa New Relic x Datadog (REQ-OBR-40), com a data da verificação de preços/planos
6. Tirar da lista 'falta' a confirmação da região US: ela já está registrada em 00_COLAB_IA/LOG_DE_TRABALHO.md:36 ('a conta abre em one.newrelic.com, região US') e em PENDENCIAS_E_PROXIMOS_PASSOS.md:113 (2026-10-30). Continuam pendentes o plano efetivo, o acesso ao APM e a license key.

**Depende de:** Conta New Relic ativa com license key (relato do usuário, ainda não conferido em registro); Resposta da FIAP sobre 'contas gratuitas for education' (Q-04)

**Etapa do plano:** E0 (contas) / E1 (validação de ingestão) · **Esforço:** P

**Risco:** Baixo para prazo. O plano Free tem limite de 100 GB/mês e 1 usuário full: o volume do projeto é pequeno, mas mandar também métricas do spanmetrics ao NR gastaria cota (plano 06-telemetria.html ~l.98 já recomenda enviar só traces). Q-04 sem resposta pode gerar dedução se a FIAP exigir a conta educacional. A retenção de spans no plano Free não foi verificada nesta rodada (confira na documentação 'data retention' da New Relic); se for curta, prints e gravação precisam sair logo após a prova.

### REQ-OBR-13 — 🟦 implementado, falta demonstrar

Alterar o código-fonte ou o Dockerfile dos cinco microsserviços com bibliotecas de instrumentação (PDF p. 4).

**Ajuste da auditoria** (era 🟦 implementado, falta demonstrar): O status está confirmado: a instrumentação existe no código (evaluation main.go:42/94/104; flag/targeting app.py:16,19; analytics app.py:19,173; telemetry.py:77-125), mas não está versionada (git ls-files services | grep telemetry = 0) e o render do overlay tem 0 ocorrências de OTEL. A omissão está na ativação: só incluir as variáveis nos ConfigMaps (item da lista 'falta') não basta para pods já criados, por causa do envFrom sem hash. Isto não aparecia na avaliação nem nos achados F-019 citados.

**Falta:**

1. Versionar a instrumentação (ver REQ-OBR-21): sem isso, as imagens do CI e do cluster não a contêm
2. Ativar o SDK nos workloads: incluir OTEL_SERVICE_NAME, OTEL_EXPORTER_OTLP_ENDPOINT (Collector do cluster), OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf e OTEL_RESOURCE_ATTRIBUTES nos gitops/base/*/configmap.yaml. Hoje 'kubectl kustomize gitops/overlays/prod' gera 23 objetos com 0 ocorrências de 'OTEL'
3. Publicar as imagens instrumentadas (merge dev para main, CI) e trocar os placeholders 'registry.conta-pendente.invalid' (gitops/overlays/prod/kustomization.yaml:65-80)
4. Demonstrar no APM (REQ-OBR-14/15/27) e citar a instrumentação no relatório (REQ-OBR-39)
5. Garantir o rollout depois da mudança de ConfigMap. Os Deployments leem as variáveis por envFrom de ConfigMaps simples (gitops/base/*/deployment.yaml, envFrom/configMapRef; gitops/base/kustomization.yaml:41-64, sem configMapGenerator), e o Kubernetes não reinicia pods quando o ConfigMap muda. Levar as OTEL_* no mesmo sync da troca de imagem, ou usar configMapGenerator com hash ou annotation de checksum. Senão o SDK continua no-op (services/auth-service/telemetry.go:39-42) em pods já rodando.

**Depende de:** REQ-OBR-21 (commit/publicação autorizados pelo usuário); E2: conta AWS, ECR e CI para publicar as imagens; E3: Collector no cluster e variáveis OTEL nos manifests (F-019)

**Etapa do plano:** E1 (implementação local concluída) / E2-E3 (publicação e ativação) · **Esforço:** P

**Risco:** O risco técnico é baixo, porque o código está testado. O risco de entrega vem do código não versionado (F-025): a perda da árvore de trabalho apagaria toda a instrumentação. Quando os testes forem para o Git, o CI Python passa a rodar pytest em tests/ (.github/workflows/_ci-python.yml:136-143) e o Trivy/SCA vai examinar as novas dependências OTel. Pode haver falha de pipeline não prevista, já que o CI remoto nunca rodou com este código.

### REQ-OBR-14 — 🟨 parcial

Gerar tracing distribuído e mostrar no APM o 'caminho' de uma requisição ao evaluation-service (PDF p. 4; vídeo p. 6; print p. 6).

**Falta:**

1. E1 externa (sem AWS): criar uma variante local do Collector com exporter otlphttp para https://otlp.nr-data.net, header api-key lido de variável de ambiente local (nunca versionada), mantendo memory_limiter, filter/health, transform/sanitize e batch. A variante pode ficar em arquivo ignorado ou usar ${env:NEW_RELIC_LICENSE_KEY}
2. Subir o Compose (docker-compose.yaml + integration + otel) e fazer um GET /evaluate com o cache vazio. CACHE_TTL é 30 s (evaluator.go:24): com cache quente, flag, targeting e auth não aparecem no trace
3. No New Relic, abrir Distributed Tracing, localizar o trace pelo trace_id e conferir os 5 serviços e a cadeia HTTP + SQS. Guardar print e trace_id (evidência sanitizada)
4. Verificar no NR o efeito do transform/sanitize: atributos como url.full e http.url são descartados. Conferir se as chamadas externas e de banco continuam identificadas (server.address, db.system / db.system.name)
5. E3: implantar o Collector no cluster (Application ArgoCD + Helm) com pipeline de traces exportando ao NR e a license key num Secret criado fora do Git; acrescentar as variáveis OTEL aos ConfigMaps dos 5 serviços
6. Repetir a requisição de teste no cluster via kubectl port-forward e confirmar o trace vindo do EKS (por exemplo, com deployment.environment.name diferente de 'local')
7. E6/E7: ensaiar e gravar (REQ-OBR-27b/c) e incluir o print do trace no relatório (REQ-OBR-36)

**Depende de:** REQ-OBR-12 (license key disponível); REQ-OBR-21 e E2 (imagens instrumentadas publicadas); REQ-OBR-11/E3 (Collector no cluster roteando traces para o APM); Conta AWS com crédito/cobrança confirmados (F-026) para a demonstração no EKS

**Etapa do plano:** E1 (externa, pendente) / E3 (cluster) / E6-E7 (ensaio, vídeo e relatório) · **Esforço:** M

**Risco:** Prazo: meta interna 2026-11-12. A prova Compose para NR pode ser feita já, sem AWS e sem custo, e reduz bastante o risco. A demonstração no EKS custa cerca de US$ 0,47/h (estimativa da Fase 3) e depende de créditos não confirmados. O alerta e o PagerDuty (trial até cerca de 2026-11-11) competem pela mesma janela de cluster ligado. O SDK em lote e o encerramento de pods podem perder spans (RELATORIO_PASSO2:75). Sem flag/targeting no trace por causa do cache, o 'caminho' fica incompleto na gravação.

### REQ-OBR-15 — 🟨 parcial

O painel do APM deve exibir o mapa de dependências (Service Map) dos 5 microsserviços (PDF p. 4; vídeo p. 6).

**Falta:**

1. Depois da ingestão (REQ-OBR-14), gerar tráfego repetido em GET /evaluate, com cache vazio e com o worker analytics consumindo a fila
2. No NR, abrir Service Map / Distributed Tracing e conferir os 5 serviços como entidades (service.name) e as arestas HTTP evaluation->flag, evaluation->targeting, flag->auth e targeting->auth
3. Verificar se o NR desenha a aresta assíncrona evaluation->analytics (PRODUCER/CONSUMER via SQS). O plano (05-requisicao.html ~l.102) supõe que sim, mas isso não foi verificado. Se não desenhar, avaliar span link ou atributos de messaging reconhecidos pelo NR, ou explicar no vídeo pelo trace, e registrar a limitação
4. Conferir se Redis, PostgreSQL, SQS e DynamoDB aparecem como dependências. Os spans Go usam só db.system.name (telemetry.go:168-170) e o analytics usa db.system.name='aws.dynamodb' (app.py:108); se o NR exigir db.system, acrescentar o atributo legado
5. Repetir com tráfego vindo do cluster (E3), fazer print do mapa e incluir no vídeo (REQ-OBR-27a)

**Depende de:** REQ-OBR-14 (traces chegando ao New Relic); REQ-OBR-12 (conta/license key); E3 (Collector no cluster) para a demonstração final

**Etapa do plano:** E1 (externa) / E3 / E6-E7 · **Esforço:** M

**Risco:** Técnico: o reconhecimento das relações assíncronas (SQS) e das dependências de banco pelo New Relic não foi testado. Se o analytics aparecer desconectado, o mapa 'dos 5 microsserviços' fica incompleto, e corrigir isso depois de 2026-11-12 aperta o prazo. Mapas costumam precisar de alguns minutos de tráfego para se formar: reserve tempo antes da gravação.

### REQ-OBR-16 — ⬜ ausente

Configurar um alerta inteligente no Grafana ou no APM (exemplo do PDF: 5xx do auth-service acima de 5%).

**Ajuste da auditoria** (era ⬜ ausente): O status ausente está confirmado: o grep por alert|PrometheusRule|contact point|alertmanager fora de 00_COLAB_IA e docs não encontra nenhuma regra, só comentários de bandit e o README. A lista 'falta', porém, põe a decisão e a implementação da falha depois da E2/E3. Pelo plano, a falha exige código (07-resposta.html: 'a falha provocada precisa ser do tipo que um reinício cura'; 09-plano-fontes.html, opção (a), 'endpoint administrativo no flag'), e o ArgoCD e o CI dependem da main (terraform/k8s/argocd.tf:298-300). Essa ordem gera retrabalho com o cluster ligado, em conflito com o risco de custo e trial já apontado.

**Falta:**

1. Concluir a E2 (cluster) e a E3 (Prometheus, Grafana e Collector gateway com o conector spanmetrics exportando para o Prometheus, conforme REQ-OBR-06/07/09/11).
2. Ler no Prometheus o nome real da métrica do spanmetrics e dos rótulos service_name e status_code. O plano deixa isso explícito como pendente (06-telemetria.html:95; 09-plano-fontes.html:162).
3. Decidir o cenário da falha e o serviço que o alerta vai observar (perguntas abertas em 09-plano-fontes.html:179-180). Levar em conta o F-018: o auth devolve 401 em qualquer erro SQL (services/auth-service/handlers.go:55-59). Por isso o exemplo de '5xx do auth-service' do PDF NÃO dispara se o banco do auth cair. Levar em conta também o F-017 (falhas do targeting viram 200).
4. Versionar a regra no Grafana (provisioning em ConfigMap carregado pelo sidecar, ou em values do chart) dentro de gitops/observability/, com proporção de erro por serviço, janela, `for` contra flapping e rótulo service. Isso cobre a parte 'inteligente' (SUG-02, Q-14).
5. Sincronizar pelo ArgoCD e confirmar que a regra aparece em Alerting > Alert rules.
6. Provocar a falha e registrar a transição Normal → Pending → Firing → Normal (print e horário) para a E6/E7 (REQ-OBR-29).
7. Mudar a ordem: decidir e implementar o mecanismo de falha (item 3) ANTES da E2. Ele é código novo no flag-service, precisa passar pelo CI/DevSecOps na main e estar na imagem publicada; deixá-lo para depois de E2/E3 obriga a um novo ciclo de imagem com o cluster ligado.
8. Definir na regra o tratamento de No Data/Error e garantir tráfego contínuo durante ensaio e gravação. A expressão é uma razão de rate() (08-exibicao-mudancas.html:27-31) e, sem requisições, fica sem dados.
9. Avaliar prototipar a regra e conferir o nome real da métrica spanmetrics num Prometheus/Grafana local no Compose (pergunta aberta em 09-plano-fontes.html). Isso adianta o item 2 sem custo de cluster.

**Depende de:** REQ-OBR-06; REQ-OBR-07; REQ-OBR-09; REQ-OBR-11; E2 (cluster no ar, nada implantado hoje); E3 (stack de observabilidade por GitOps, inexistente); Decisão do mecanismo de falha (Q-12; pergunta aberta do plano); Correção ou contorno de F-017/F-018 conforme o serviço escolhido

**Etapa do plano:** E4 · **Esforço:** M

**Risco:** Prazo: a regra só pode ser validada com cluster e stack no ar, e hoje nada está implantado. A entrega é em 2026-11-17, com meta interna em 2026-11-12. Custo: ~US$ 0,47/h com 3 nós (estimativa da Fase 3), e os créditos da conta nova não foram confirmados (F-026). Risco técnico: se o nome da métrica do spanmetrics divergir, painel e alerta ficam sem dados. O conector está marcado como alpha (06-telemetria.html:95). O cache de 30 s do evaluation (services/evaluation-service/evaluator.go:24) atrasa os erros no evaluation, embora não afete os 500 do próprio flag.

### REQ-OBR-17 — 🟨 parcial

Criar conta no PagerDuty (escolhido; OpsGenie descontinuado) e integrar o alerta para abrir incidente automaticamente, acionando o responsável (p. 3: 'o time deve ser acordado').

**Ajuste da auditoria** (era 🟨 parcial): O status parcial se mantém (conta relatada pelo usuário; nenhuma integração no repositório, conforme o grep). A ordem da lista, porém, deixa toda a configuração no PagerDuty para depois da E2/E3. Isso ignora que a parte SaaS não depende do cluster e que o plano já a previa na E0 (09-plano-fontes.html:13). Com o trial perto do fim e 'Events: Not included' no Free (PENDENCIAS:113), a verificação precisa ser feita primeiro. O risco de prazo foi tratado, mas a mitigação proposta ('repetir depois') não protege a entrega.

**Falta:**

1. Conferir na conta a data exata de fim do trial e o que o plano Free mantém depois dele, sobretudo a ingestão por Events API v2 (F-026). Verificação prática: enviar um evento de teste à routing key ainda no trial e repetir depois; em caso de dúvida, consultar o suporte ou as condições do plano.
2. No PagerDuty: criar o serviço 'togglemaster', a escala com o usuário responsável, a política de escalonamento e a regra de notificação do usuário (push/SMS/e-mail), para atender ao 'acordar o time'. Criar a integração Events API v2 e guardar a routing key fora do Git.
3. Acrescentar no Terraform k8s (ou outro mecanismo de Secrets) um Secret no namespace observability para a routing key, entrando por TF_VAR_*. Documentar o Secret em gitops/SECRETS-CONTRATO.md.
4. Criar o contact point PagerDuty no Grafana, provisionado no Git e lendo a chave do Secret, com dedup/agrupamento por serviço na notification policy.
5. Usar 'Test' do contact point e depois a falha real: comprovar incidente Triggered → Resolved e o acionamento do responsável (print com horário), tudo antes do fim do trial.
6. Registrar a justificativa PagerDuty versus OpsGenie para o relatório (REQ-OBR-40).
7. Antecipar para agora, sem depender do cluster, a criação do serviço, da escala, da política de escalonamento e da integração Events API v2, além de um evento de teste por curl à routing key. A E0 do plano já pedia isso (09-plano-fontes.html:13). O item 1 da lista ('repetir depois' do trial) não serve como mitigação: quando o resultado sair, já é tarde para trocar de caminho. É preciso confirmar agora, na página de billing/plano da própria conta ou com o suporte, o que acontece no fim do trial.
8. Avaliar validar o contact point Grafana -> PagerDuty com um Grafana local no Compose (pergunta aberta do plano em 09-plano-fontes.html) antes de cerca de 2026-11-11. Isso desacopla do cluster o risco do trial.
9. Conferir a data exata do fim do trial: PENDENCIAS:112 diz 'cerca de 2026-11-12' e :113 diz 'cerca de 2026-11-11'.

**Depende de:** REQ-OBR-16; E2/E3 (Grafana no cluster com saída para a internet; NAT habilitado por padrão em terraform/variables.tf:100-111); Secret da routing key (inexistente); Confirmação do plano PagerDuty depois do trial (F-026)

**Etapa do plano:** E0 (conta) e E4 (integração) · **Esforço:** M

**Risco:** Risco ALTO de prazo e plano. O trial do PagerDuty termina por volta de 2026-11-11, antes da meta interna de 2026-11-12 e da entrega em 2026-11-17. A página de preços mostra 'Events: Not included' no Free. Se a integração Events API v2 parar depois do trial, o contact point do Grafana deixa de abrir incidentes e a gravação teria de acontecer até ~11-11. Isso pressiona E2, E3, E4 e E5 em cerca de 12 dias, ainda com créditos AWS não confirmados (F-026). Outro risco: a chave vazar em print ou vídeo.

### REQ-OBR-18 — ⬜ ausente

Configurar notificação detalhada (ChatOps) para um canal do Slack (escolhido; evita a dúvida Q-02 sobre Teams).

**Falta:**

1. No workspace Slack: criar o canal (ex.: #togglemaster-incidentes), criar o app com Incoming Webhooks, autorizar e guardar a URL fora do Git. Conferir o limite de apps do plano Free na própria conta.
2. Criar um Secret com a URL do webhook (Terraform k8s via TF_VAR_* ou mecanismo equivalente) e documentá-lo em gitops/SECRETS-CONTRATO.md.
3. Criar o contact point Slack no Grafana, provisionado no Git, com template de mensagem 'detalhada': serviço, valor medido versus limite, severidade, início, links para painel e trace, e status firing/resolved.
4. Criar no workflow de self-healing (REQ-OBR-19) uma etapa que publique o resultado da ação no mesmo canal, como o plano prevê (07-resposta.html:120).
5. Testar com 'Test' do contact point e depois com a falha real; capturar o print obrigatório (REQ-OBR-37) sem mostrar a URL do webhook.

**Depende de:** REQ-OBR-16; E3 (Grafana no cluster); Secret do webhook Slack (inexistente)

**Etapa do plano:** E4 · **Esforço:** P

**Risco:** Risco baixo de custo, porque o Slack Free basta para um webhook. O limite de apps do Free ficou [INCERTO] no guia (linha 109). Há risco de vazar a URL do webhook em print ou vídeo. O prazo depende do encadeamento E2→E4.

### REQ-OBR-19 — ⬜ ausente

Automação de self-healing (GitHub Action por webhook/repository_dispatch) que reaja sozinha ao alerta e tente mitigar (ex.: kubectl rollout restart).

**Ajuste da auditoria** (era ⬜ ausente): O status ausente está confirmado: .github/workflows não tem self-healing nem repository_dispatch, e não há access_entry nem eks:* no Terraform (o grep só encontra ecr:* em terraform/modules/iam-ci/main.tf:175-200). Uma correção na justificativa: a observação global da avaliação diz que o token de dispatch e os Secrets de PagerDuty/Slack/GitHub 'não estão previstos'. Eles estão previstos no plano, mas não implementados: 04-plataforma.html:45 ('Secrets: New Relic, PagerDuty, Slack e token do GitHub'), 08-exibicao-mudancas.html:54 e :58 ('4 Secrets novos' em terraform/k8s/secrets.tf e no SECRETS-CONTRATO), 09-plano-fontes.html:13 (criar o token do GitHub na E0) e :164. A nuance válida é que o github_token atual (terraform/k8s/variables.tf:125-131) é Contents: Read-only, para o ArgoCD, e não serve ao dispatch. Os pontos novos que procedem: não achei menção a 'branch padrão' em 00_COLAB_IA, e o endpoint público do EKS não tem public_access_cidrs (modules/eks/main.tf:90), o que permite runners hospedados.

**Falta:**

1. Decidir o mecanismo da falha proposital que o reinício cura (opção (a) do plano: estado de erro só em memória no flag, ativado por endpoint ou sinal protegido) e implementá-lo com teste. Decidir também quais Deployments a allowlist reinicia (flag e/ou evaluation), já que a regra por serviço dispara para os dois (09-plano-fontes.html:179-180).
2. Terraform: criar uma role IAM própria do self-healing com trust OIDC restrita ao repositório e à ref main, usando o subject efetivo com IDs imutáveis do F-023, mais eks:DescribeCluster. Criar também a aws_eks_access_entry + access policy AmazonEKSEditPolicy limitada ao namespace togglemaster.
3. Criar um token GitHub fine-grained com acesso só ao repo 04 e permissão de escrita em Contents, exigida por POST /repos/{owner}/{repo}/dispatches. Guardá-lo em um Secret do namespace observability, criado pelo Terraform via TF_VAR_*, e revogá-lo após a entrega (09-plano-fontes.html:164).
4. Criar no Grafana um contact point webhook para https://api.github.com/repos/fiap-devops-arqcloud-2026/tech-challenge-04/dispatches, com header Authorization e corpo customizado no formato {event_type:'self-heal', client_payload:{service, status, ...}}. Confirmar que a versão do Grafana do chart escolhido aceita payload customizado no webhook. O payload padrão do Grafana não tem event_type, e o GitHub o recusaria.
5. Criar .github/workflows/self-healing.yml (on: repository_dispatch, types [self-heal]; permissions id-token: write, contents: read) com estas etapas: ignorar status resolved, validar a allowlist, verificar o cooldown por anotação no Deployment, configure-aws-credentials por OIDC, aws eks update-kubeconfig, kubectl rollout restart, kubectl rollout status --timeout e publicação do resultado no Slack.
6. Fazer merge na main (branch padrão; origin/HEAD -> origin/main), que hoje NÃO está autorizado (CLAUDE.md: 'sem push, PR ou alteração da main nesta etapa'). Pela documentação do GitHub, repository_dispatch só dispara workflows presentes no branch padrão. Conferir em docs.github.com, 'Events that trigger workflows' > repository_dispatch.
7. Ensaiar o ciclo no cluster: falha → Firing → dispatch → restart → Resolved, 3 vezes seguidas, com uma recusa dentro do cooldown (critério da E5). Confirmar também que o ArgoCD continua Synced depois do restart.
8. Cadastrar nos Secrets/Variables do repositório GitHub o ARN da role do self-healing e a URL do webhook Slack que o workflow usará para relatar o resultado (o Secret do cluster não chega ao runner). Isso é uma alteração de configuração do repositório e precisa de autorização do usuário.
9. Conferir se a organização fiap-devops-arqcloud-2026 permite tokens fine-grained com acesso ao repo e se exige aprovação do owner. O repositório é privado (LOG_DE_TRABALHO.md:100), e isso pode atrasar a obtenção do token.

**Depende de:** REQ-OBR-16; REQ-OBR-18 (relato no Slack); E2 (cluster, role, access entry; F-023 trust OIDC); E3/E4 (Grafana com contact point webhook); Autorização do usuário para push/merge na main; Decisão do mecanismo de falha (Q-12)

**Etapa do plano:** E5 · **Esforço:** G

**Risco:** É o item mais longo da cadeia e o último antes da gravação. Depende de cluster no ar (custo ~US$ 0,47/h; créditos não confirmados, F-026), de merge na main (ainda não autorizado) e de um token com escrita no repositório guardado no cluster (risco de segurança). Se a falha escolhida não for curável por reinício (ex.: banco parado, exemplo da p. 6), o vídeo mostra a tentativa mas não a recuperação. Sem filtro de resolved e cooldown, pode entrar em laço de reinícios. O cache de 30 s do evaluation atrasa a manifestação e a recuperação na gravação. Se a gravação ficar depois de ~2026-11-11, a cadeia completa pode perder o elo PagerDuty.

### REQ-OBR-20 — ⬜ ausente

Entregar no repositório o código IaC/GitOps atualizado com a stack de monitoramento e o OTel Collector.

**Ajuste da auditoria** (era 🟨 parcial): O requisito (p. 5) pede 'Código IaC/GitOps atualizado para incluir a stack de monitoramento e o OTel Collector'. A própria avaliação admite que o incremento 'está, na prática, ausente': nenhum chart, values, Application ou Collector em terraform/ ou gitops/ (rg no repositório inteiro sem ocorrência; o render do overlay dá 23 objetos de Fase 3; gitops/README.md:22 e terraform/README.md:63 dizem que a observabilidade não foi implementada). A base IaC/GitOps da Fase 3 é pré-requisito, não entrega deste item. A única config de Collector é local e fora do Git. Manter 'parcial' superestima o estado. O Codex marcou 'Parcial'; divirjo pelo mesmo motivo.

**Falta:**

1. Concluir os artefatos de REQ-OBR-06, 07, 08, 09, 10 e 11 em gitops/observability/ e terraform/k8s (Application observability, namespace e Secrets novos)
2. Atualizar gitops/README.md, terraform/README.md e gitops/SECRETS-CONTRATO.md descrevendo a stack
3. Antes de qualquer commit: incluir no .gitignore o arquivo de 156 MB (F-024; 'git check-ignore' confirma que não está ignorado) e decidir o que do trabalho não comitado entra (F-025)
4. Com autorização do usuário: commit na dev, merge na main (a branch observada pelo ArgoCD) e push
5. Demonstrar que a stack implantada veio dessa versão do Git (ArgoCD Synced no commit correspondente)
6. Registrar no relatório e na matriz que docker-compose.otel.yaml e observability/otel-collector-local.yaml são laboratório local e não versionado ('??' no git status). Não são IaC/GitOps do cluster e não contam como entrega deste requisito.

**Depende de:** REQ-OBR-06 a REQ-OBR-11; Autorização de commit, push e merge (CLAUDE.md: sem push/PR/main nesta etapa); Repositório acessível ao avaliador (hoje privado, segundo argocd.tf:39-49 e PENDENCIAS F-023)

**Etapa do plano:** E3 · **Esforço:** M

**Risco:** Um 'git add -A' incluiria o arquivo de 156 MB e o GitHub recusaria o push (F-024). Todo o trabalho desde 3b21e65 existe só na árvore local (F-025): uma perda local apagaria a instrumentação e o Collector. Prazo de 2026-11-12/17.

### REQ-OBR-21 — 🟨 parcial

Entregar no repositório o código-fonte das aplicações atualizado com a instrumentação (PDF p. 5).

**Falta:**

1. Com autorização do usuário: resolver F-024 antes de qualquer add (ignorar 00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/offline-test.jsonl)
2. Selecionar e commitar na dev os arquivos de services/** (incluindo telemetry.*, testes e go.sum), docker-compose.otel.yaml, observability/ e scripts/ de prova, sem segredos, evidências brutas ou .exe
3. Push da dev, CI verde (pytest passa a rodar tests/; Go 'go test ./...'; Trivy/SCA nas novas dependências) e merge para main para publicar as imagens (E2)
4. Garantir acesso do avaliador ao repositório fiap-devops-arqcloud-2026/tech-challenge-04 (privado) e citar o link no relatório (REQ-OBR-34)
5. Atualizar os services/*/README.md e o observability/README.md (hoje diz que não há conta NR) para a versão final

**Depende de:** Autorização do usuário para commit/push/PR (CLAUDE.md: 'sem push, PR ou alteração da main nesta etapa'); Correção de F-024; CI remoto funcionando com a role OIDC (F-023 / P-013)

**Etapa do plano:** E1 (código pronto) / E2 (merge para main e publicação) / E7 (link no relatório) · **Esforço:** P

**Risco:** Alto impacto e baixo esforço: enquanto nada for commitado, uma limpeza ou perda local apaga toda a instrumentação, e o 'código entregue' não a contém. O primeiro push vai disparar o CI com dependências e testes novos; falhas de SCA/Trivy nas libs OTel podem exigir ajuste de versão perto do prazo. O repositório privado exige confirmar o acesso do avaliador.

### REQ-OBR-22 — ⬜ ausente

Entregar no repositório os scripts/automações criados para o self-healing.

**Falta:**

1. Versionar .github/workflows/self-healing.yml e scripts/self-healing/ (script de ação com allowlist, cooldown, filtro de status e validação pós-restart) como descrito no REQ-OBR-19.
2. Versionar no Git, junto, as peças que fazem a automação reagir ao alerta: contact point webhook e template no provisioning do Grafana (gitops/observability/), role e access entry no Terraform, e o contrato dos Secrets.
3. Acrescentar um teste local do script (ex.: modo dry-run com payload firing/resolved e serviço fora da allowlist) e o lint do workflow no CI (actionlint/zizmor, se já usado no projeto).
4. Commitar e publicar no repositório entregue. Hoje há trabalho não commitado desde 3b21e65 (F-025). Fazer commit/push só com autorização do usuário.
5. Citar os caminhos no relatório PDF (REQ-OBR-34) e mostrar o log de execução (REQ-OBR-38).

**Depende de:** REQ-OBR-19; Autorização de commit/push e merge na main (F-025; restrição do CLAUDE.md)

**Etapa do plano:** E5 · **Esforço:** M

**Risco:** O risco é baixo isoladamente, mas o requisito herda todo o risco do REQ-OBR-19. Há ainda o risco de ficar com código no repositório que não corresponde ao demonstrado no vídeo, se ajustes de última hora não forem commitados. Não versionar tokens, URLs de webhook nem a routing key.

### REQ-OBR-23 — 🟨 parcial

Regra de avaliação (p. 5): evidenciar na prática o funcionamento de todas as métricas, configurações e requisitos; só configurar não basta.

**Falta:**

1. Concluir E1 externa: exporter OTLP para otlp.nr-data.net no Collector, com a chave fora do Git, e trace + Service Map no New Relic
2. Concluir E2: apply nas 3 camadas, imagens instrumentadas publicadas e 5 pods Running/Synced
3. Concluir E3/E4/E5: stack, dashboard, alerta, PagerDuty, Slack e self-healing funcionando no cluster
4. Montar a matriz de evidências (SUG-01): para cada REQ-OBR, a tela, o print, o minuto do vídeo e o commit/imagem implantada
5. Ensaio cronometrado (E6) sem lacunas na matriz e gravação/relatório (E7)

**Depende de:** REQ-OBR-24; REQ-OBR-25; REQ-OBR-26; REQ-OBR-27; REQ-OBR-28; REQ-OBR-29; REQ-OBR-30; REQ-OBR-31; REQ-OBR-32 a 38 (relatório); E1 externa (New Relic); E2-E5 na AWS

**Etapa do plano:** E6 · **Esforço:** G

**Risco:** Alto. É o requisito-guarda-chuva: cada item sem evidência gera 'dedução direta de pontos' (p. 5). O calendário do plano (09-plano-fontes.html:124-131) previa E4 até 10-25 e E5 até 11-01; em 2026-10-30 nem a E1 externa nem a E2 foram feitas. Custo do cluster (~US$ 0,47/h, créditos da conta nova não confirmados, F-026).

### REQ-OBR-24 — ⬜ ausente

Entregar vídeo de demonstração com no máximo 25 minutos.

**Ajuste da auditoria** (era ⬜ ausente): O status ausente está confirmado: não há *.mp4/*.mkv/*.mov nem roteiro da Fase 4, e docs/00_COLAB_IA/_ARQUIVO_MORTO/ROTEIRO_VIDEO.md:1 é da Fase 3 ('máximo 20 minutos'). A lista 'falta' omite a etapa de custo pós-gravação que o próprio plano prevê. Além disso, PENDENCIAS:163 registra 'crédito AWS esgotado declarado em 2026-10-13 (Billing não consultado)', o que reforça o risco de custo de uma regravação.

**Falta:**

1. Escrever o roteiro da Fase 4 na ordem das p. 5-6: visão geral EKS/ArgoCD → Grafana/Loki/Collector → New Relic → incidente/self-healing, com tempo por bloco e somando menos de 25 min
2. Ensaio cronometrado completo (E6) com o cluster ligado
3. Gravar, conferir duração (≤ 25:00) e legibilidade das telas
4. Hospedar com link acessível ao avaliador (plataforma não definida no PDF, Q-06) e testar o acesso numa sessão anônima
5. Registrar o link para o relatório (REQ-OBR-34)
6. Logo depois que a gravação for aprovada, destruir as camadas caras (tarefa da E7 em 09-plano-fontes.html, 'Destruir as camadas caras assim que a gravação for aprovada') e registrar o custo real. Uma regravação exige religar o cluster, a cerca de US$ 0,47/h, sem créditos confirmados.

**Depende de:** REQ-OBR-25 a 31 (conteúdo obrigatório do vídeo); E2-E5 concluídas; Q-06 (plataforma/procedimento de submissão)

**Etapa do plano:** E7 · **Esforço:** M

**Risco:** Prazo: entrega em 2026-11-17 (data informada pelo usuário, não pelo PDF; Q-05), meta interna 2026-11-12. Uma regravação exige religar o cluster (custo) e, depois de cerca de 2026-11-11, pode ficar sem a integração do PagerDuty (fim do trial). Risco de passar de 25 min se a espera do alerta (janela/for + cache de 30 s) não for cortada na edição.

### REQ-OBR-25 — 🟨 parcial

No vídeo, mostrar o cluster EKS (IaC) e o ArgoCD (GitOps) rodando com a nova stack.

**Falta:**

1. E0/E2: criar terraform.tfvars (default_tags phase=4, node_group_desired_size=3), reconciliar/importar os recursos criados à mão (ECR, OIDC, role, F-023) antes de qualquer apply
2. Integrar o trabalho local (F-025) e, com autorização do usuário, fazer push/merge dev→main, porque o ArgoCD observa a branch main (argocd.tf:300) e o CI publica as imagens a partir dela
3. Substituir as sentinelas de imagem do overlay pelas tags publicadas no ECR
4. Criar gitops/observability/ (Applications Helm de kube-prometheus-stack, Loki, Grafana e Collector agent/gateway) e a Application 'observability' (Terraform ou app-of-apps)
5. Adicionar as variáveis OTEL_* aos ConfigMaps dos 5 serviços (F-019)
6. Apply nas 3 camadas e conferência: kubectl get nodes, pods Running nos namespaces togglemaster e observability, ArgoCD com as duas Applications Synced/Healthy
7. No vídeo: mostrar o console/kubectl do EKS, o código Terraform e a UI do ArgoCD (port-forward, sem Ingress)

**Depende de:** E0 (conta, tfvars, reconciliação IAM/ECR, F-023); Autorização de push/merge para main; REQ-OBR-06/20 (stack em GitOps); Q-01 (EKS/ArgoCD conservador)

**Etapa do plano:** E2 + E3 (gravação na E7) · **Esforço:** G

**Risco:** Custo: cluster de 3 nós a ~US$ 0,47/h (estimativa da Fase 3), sem créditos confirmados na conta nova (F-026). Prazo: a E2 nem começou. Cota de vCPU On-Demand (o plano pede 8 ou mais). Conflito HPA × selfHeal sem ignoreDifferences (grep não encontrou ignoreDifferences; 04-plataforma.html:127). CRDs grandes do kube-prometheus-stack podem exigir ServerSideApply.

### REQ-OBR-26 — ⬜ ausente

No vídeo: (a) abrir o Grafana; (b) mostrar o dashboard customizado com métricas; (c) buscar logs no Loki; (d) explicar como o OTel Collector roteia os dados.

**Ajuste da auditoria** (era 🟨 parcial): A classificação 'parcial' exagera. O próprio avaliador escreve que (a), (b) e (c) 'não têm nenhum artefato no repositório'. Para o item (d), só há documento de arquitetura planejada (README.md:121) e o Collector local, cujo único pipeline é traces -> [debug, file/traces] (observability/otel-collector-local.yaml:56-60). Esse Collector não encaminha 'esses dados' (métricas e logs exibidos no Grafana) para lugar nenhum, e observability/README.md:21 confirma que não há métricas, logs, Loki, Prometheus nem Grafana. Pelo grep fora de 00_COLAB_IA e docs, não existe gitops/observability/ nem qualquer chart ou values. O Codex classificou como Pendente (auditoria-codex-2026-10-30_v01/MATRIZ_REQUISITOS.md:36). Pelo mesmo critério com que o REQ-OBR-18 foi marcado ausente (pré-condição não é entrega), o status correto é ausente.

**Falta:**

1. Valores Helm e Applications para Prometheus (remote write receiver habilitado), Loki e Grafana, com datasources Prometheus/Loki provisionados
2. Collector no cluster: agent (filelog dos pods → Loki) e gateway (OTLP; spanmetrics → Prometheus; traces → New Relic), com pipelines de metrics/logs/traces
3. Conferir no Prometheus o nome real da métrica do spanmetrics e os rótulos de status antes de escrever as consultas
4. Dashboard versionado (ConfigMap com label de sidecar) com os 3 painéis de REQ-OBR-10
5. Testar no Grafana Explore a consulta LogQL por service_name e por trace_id
6. Preparar o trecho falado/diagrama do roteamento a partir da configuração efetivamente implantada (não da planejada)
7. Gravar o bloco no vídeo e capturar o print do dashboard (REQ-OBR-35)
8. Antes de gravar, decidir com o usuário se Grafana/Prometheus/Loki sobem também no Compose (pergunta aberta em 09-plano-fontes.html, 'Grafana, Prometheus e Loki também no Compose?'). Isso permite desenhar dashboard e consultas sem cluster ligado e reduz horas de custo.

**Depende de:** REQ-OBR-25 (cluster e ArgoCD no ar); REQ-OBR-06 a 11 e 20 (stack e Collector); Q-10 (só se trocar o Collector pelo Alloy)

**Etapa do plano:** E3 + E4 (gravação na E7) · **Esforço:** G

**Risco:** Capacidade do cluster (Prometheus + Loki + Grafana + 2 releases do Collector em 3 nós pequenos; o plano desliga o Alertmanager). Volumes EBS novos não entram na estimativa de custo. O conector spanmetrics é alpha (06-telemetria.html:95). Cota de 100 GB/mês do New Relic, se os logs também forem enviados para lá.

### REQ-OBR-27 — 🟨 parcial

No vídeo: abrir o New Relic, mostrar o Service Map, fazer uma requisição de teste e exibir o trace distribuído detalhado.

**Falta:**

1. E1 externa: acrescentar exporter otlphttp (endpoint https://otlp.nr-data.net, header api-key vindo de variável/arquivo local ignorado) ao Collector do Compose e provar trace + Service Map no New Relic sem cluster
2. Conferir no New Relic que os 5 serviços aparecem conectados (incluindo o caminho SQS evaluation → analytics) e que o filtro transform/sanitize não removeu atributos de que o Service Map precisa
3. Levar a mesma exportação ao gateway do Collector no cluster (Secret com a license key criado pelo Terraform, TF_VAR_*)
4. Preparar a requisição de teste (curl via port-forward para o evaluation-service com uma flag existente) e anotar o trace_id para localizar na UI
5. Gravar o bloco e capturar o print do trace (REQ-OBR-36)

**Depende de:** Chave de ingestão do New Relic (externa); REQ-OBR-25 (para demonstrar a partir do cluster); REQ-OBR-11, 14, 15

**Etapa do plano:** E1 (externa) + E3; gravação na E7 · **Esforço:** M

**Risco:** Médio. Limite gratuito do New Relic (100 GB/mês e usuários do plano Free); o modo de exibição do Service Map para serviços OpenTelemetry deve ser conferido na própria conta. Instrumentação ainda não comitada (F-025), então as imagens do ECR não a contêm.

### REQ-OBR-28 — ⬜ ausente

No vídeo: causar um problema proposital no sistema.

**Ajuste da auditoria** (era ⬜ ausente): O status ausente está confirmado: no grep fora de 00_COLAB_IA e docs, 'fault/inject/chaos/simulat' só encontra a propagação OTel (services/evaluation-service/sqs.go:60) e o /admin/keys do auth. A lista 'falta' não traz a premissa de processo único, que decide se a opção (a) do plano funciona. O /health raso (services/flag-service/app.py:71-74) e a livenessProbe em /health (deployment.yaml:77-83) confirmam que a falha na rota /flags não faz o kubelet reiniciar o pod, o que é favorável e já foi notado pelo avaliador.

**Falta:**

1. Decidir o mecanismo: falha que o rollout restart de fato cura, por exemplo um estado de erro só em memória no flag-service, ativado por endpoint protegido ou por variável e não pelo Git (o plano recomenda a opção a)
2. Implementar e testar localmente (Compose) que a falha gera 5xx no flag e 502 no evaluation e que o restart a remove
3. Evitar a falha via targeting (F-017) ou via banco do auth (F-018), cujo efeito não é 5xx
4. Criar o gerador de carga variando flags/usuários para contornar o cache de 30 s
5. Ensaiar no cluster junto com o alerta (REQ-OBR-29) e documentar o comando exato do vídeo
6. Se a falha escolhida for um estado em memória, garantir que ela vale para o pod inteiro. Hoje o flag-service roda gunicorn sem --workers (services/flag-service/Dockerfile:77, um worker por padrão), com replicas: 1 e sem HPA (gitops/base/flag-service/deployment.yaml:23; só analytics e evaluation têm HPA). Se workers ou réplicas aumentarem, o toggle atinge só um processo e a taxa de erro fica imprevisível. Registrar essa premissa e cobri-la com teste.
7. Implementar o mecanismo antes da E2, para entrar na imagem publicada pelo CI na main (ver REQ-OBR-16).

**Depende de:** Decisão do usuário (pergunta em aberto do plano); REQ-OBR-25 (cluster); REQ-OBR-29 (o alerta precisa detectar a falha escolhida); Q-12

**Etapa do plano:** E5 (mecanismo) e E6 (ensaio) · **Esforço:** M

**Risco:** Parar o banco do flag (exemplo da p. 6) significa parar um RDS: a operação leva minutos, depende da AWS durante a gravação, e o restart não cura, então mostra a tentativa sem a recuperação. Um endpoint de injeção de erro é código novo que precisa passar pelo CI/DevSecOps e ser protegido.

### REQ-OBR-29 — ⬜ ausente

No vídeo: mostrar o alerta disparando (Firing) no Grafana ou no APM.

**Falta:**

1. Com a stack no ar, conferir o nome da métrica spanmetrics e o rótulo status_code no Prometheus
2. Escrever a regra (provisionada como ConfigMap/arquivo versionado): taxa de 5xx por serviço acima de 5%, com janela e 'for' definidos e rótulo com o nome do serviço
3. Definir a política de notificação (agrupamento por serviço) e os 3 contact points (PagerDuty, Slack, webhook)
4. Ensaiar falha → Pending → Firing e medir o tempo total para caber no vídeo
5. Gravar a tela do Grafana Alerting em Firing

**Depende de:** REQ-OBR-16; REQ-OBR-26 (Prometheus/Grafana); REQ-OBR-28 (falha que gere 5xx); Q-14

**Etapa do plano:** E4 (gravação na E7) · **Esforço:** M

**Risco:** Janela de 5 min + 'for' + cache de 30 s podem alongar o vídeo. Rótulos do spanmetrics podem não ser os previstos. Se o alerta for criado no New Relic em vez do Grafana, muda toda a cadeia de notificação já planejada.

### REQ-OBR-30 — ⬜ ausente

No vídeo: mostrar o incidente aberto no PagerDuty e a notificação chegando ao Slack.

**Ajuste da auditoria** (era 🟨 parcial): Há incoerência com a avaliação de incidentes. O REQ-OBR-18 foi marcado ausente com o argumento de que a conta é só pré-condição. O REQ-OBR-30 é um requisito de vídeo ('mostrar o incidente sendo aberto ... e a notificação chegando') e não tem nenhuma das duas partes: o grep por pagerduty|slack fora de 00_COLAB_IA e docs só encontra texto do README (37, 55-56, 129-134) e o comentário de terraform/k8s/argocd.tf:146 que desliga as notificações do ArgoCD. Também não há Secret em terraform/k8s/secrets.tf (só auth, flag, targeting, postgres_targeting e evaluation, linhas 92-211). As contas existem apenas por relato do usuário (PENDENCIAS:112-113), e o próprio PENDENCIAS diverge sobre a data do trial: cerca de 11-12 na linha 112 e cerca de 11-11 na linha 113. O Codex marcou Pendente (MATRIZ_REQUISITOS.md:40). Contas e plano não demonstram nada operando.

**Falta:**

1. No PagerDuty: serviço com integração Events API v2, guardar a routing key fora do Git, política de escalonamento com o usuário como responsável e notificação no celular/e-mail
2. No Slack: canal e Incoming Webhook (ou app) e URL guardada fora do Git
3. Terraform: Secrets no namespace observability (TF_VAR_*) e contrato atualizado em gitops/SECRETS-CONTRATO.md
4. Grafana: contact points PagerDuty (com dedup) e Slack (template com serviço, valor medido e links) na política de notificação
5. Teste de ponta a ponta, primeiro com 'Test' do contact point e depois com a falha real; gravar ainda dentro do trial do PagerDuty
6. Capturar o print da notificação no Slack (REQ-OBR-37)
7. Criar já (sem cluster) o serviço PagerDuty e a integração Events API v2 e enviar um evento de teste por curl dentro do trial. A E0 do plano já previa isso (09-plano-fontes.html:13: 'PagerDuty (serviço com integração Events API v2)'). Assim, a dúvida do plano Free fica resolvida enquanto ainda dá para trocar de caminho.
8. Fixar uma data-limite de gravação da cadeia completa (cerca de 2026-11-10) e encaixar nela o calendário das etapas E2 a E5.

**Depende de:** REQ-OBR-17; REQ-OBR-18; REQ-OBR-29; Trial do PagerDuty (externo); Q-02 (Slack evita a dúvida sobre Teams); Q-09

**Etapa do plano:** E4 (gravação na E7) · **Esforço:** M

**Risco:** Crítico de prazo: o trial do PagerDuty termina por volta de 2026-11-11, antes da meta interna (11-12) e do prazo (11-17). Se a ingestão via Events API deixar de funcionar no plano Free, a gravação e qualquer regravação precisam acontecer antes disso. O calendário original previa esta etapa até 2026-10-25 (09-plano-fontes.html:128) e está atrasado. Limites do plano Free do Slack (número de apps/integrações) não conferidos ([INCERTO]).

### REQ-OBR-31 — ⬜ ausente

No vídeo: mostrar a automação de Self-Healing acionada automaticamente e executando a ação corretiva (ex.: pod reiniciando no terminal).

**Falta:**

1. Terraform: role do self-healing com trust OIDC restrita ao repositório (subject com IDs imutáveis, F-023) e permissão eks:DescribeCluster; access entry com AmazonEKSEditPolicy limitada ao namespace togglemaster (E5)
2. Workflow .github/workflows/self-healing.yml (on: repository_dispatch types [self-heal]) com filtro firing/resolved, allowlist, cooldown por anotação, rollout restart, rollout status --timeout e envio do resultado ao Slack
3. Script versionado em scripts/self-healing/ testável localmente (allowlist/cooldown)
4. Token do GitHub com escopo mínimo guardado como Secret do Grafana; contact point de webhook com header Authorization e corpo no formato do /dispatches
5. O workflow precisa estar na branch padrão do repositório para repository_dispatch disparar, o que exige push/merge autorizado
6. Ensaio: o ciclo 3 vezes seguidas e um segundo disparo recusado pelo cooldown (critério da E5), com kubectl get pods -w no terminal
7. Gravar o acionamento e a execução e capturar o print do log do workflow (REQ-OBR-38)

**Depende de:** REQ-OBR-19; REQ-OBR-22; REQ-OBR-29 (alerta); REQ-OBR-28 (falha curável pelo restart); REQ-OBR-25 (cluster); Autorização de push/merge; F-023 (trust OIDC)

**Etapa do plano:** E5 (gravação na E7) · **Esforço:** G

**Risco:** Alto. Segurança: um token no Grafana dá escrita ao repositório (o plano pede escopo mínimo e revogação após a entrega). Sem o filtro de 'resolved' ocorre um segundo restart. Latência do runner do GitHub (fila) durante a gravação. Workflows de repository_dispatch só rodam a partir da branch padrão. Calendário previa E5 até 11-01 (09-plano-fontes.html:129) e ela não começou.

### REQ-OBR-32 — ⬜ ausente

Entregar o relatório da Fase 4 em PDF. Não existe PDF nem rascunho da Fase 4. O que há é o relatório da Fase 3 em Markdown e PDF, mais os geradores arquivados da Fase 3.

**Ajuste da auditoria** (era ⬜ ausente): O status ausente se confirma: só existem o relatório e o PDF da Fase 3. Os geradores estão em docs/00_COLAB_IA/_ARQUIVO_MORTO (versionados), e o runtime tem reportlab, pypdf e pypdfium2, mas não weasyprint nem markdown (reverifiquei com find_spec). A lista 'falta', porém, cobre só os quatro prints da p. 6. A regra de avaliação da p. 5 (extração do enunciado, linhas 205-208) faz o relatório valer como prova alternativa para qualquer requisito, e isso não está planejado. Também falta a sanitização dos prints, um risco concreto porque os prints de 37 e 38 virão de telas com segredos.

**Falta:**

1. Criar um Markdown-fonte novo para a Fase 4, por exemplo docs/RELATORIO_DE_ENTREGA_FASE4.md, sem sobrescrever o relatório histórico da Fase 3. Seções: identificação, links, quatro prints e justificativa técnica
2. Adaptar uma cópia de build-report-fase3_2026-09-14.py (reportlab já está disponível; weasyprint e markdown não estão) para a Fase 4, com outro nome de saída e sem a seção de custos obrigatória da Fase 3
3. Gerar o PDF depois de 32–40 estarem preenchidos. Conferir com pypdf/pypdfium2 o número de páginas, o texto extraível, as imagens legíveis e os links clicáveis
4. Decidir se o PDF final é versionado ou só submetido. O PDF não exige isso; registrar a decisão em DECISOES
5. Incluir no relatório uma matriz de evidências REQ → print/link para os demais requisitos demonstráveis (Loki, Service Map, alerta Firing, incidente aberto no PagerDuty, ArgoCD Synced, HPA), além dos quatro prints obrigatórios. A regra da p. 5 (extração :205-208) desconta 'qualquer requisito que não for claramente demonstrado no vídeo ou documentado no relatório', e Q-11 continua aberta. O relatório é a rede de segurança caso algum trecho do vídeo falhe.
6. Revisar todos os prints antes de inseri-los e mascarar URL do webhook do Slack, chave de ingestão do New Relic, tokens do GitHub, routing key do PagerDuty e o ID da conta AWS, se a decisão de REQ-OBR-34 for não expô-lo. Os logs de run do GitHub Actions e as telas de contact point do Grafana são as fontes mais prováveis de vazamento.

**Depende de:** REQ-OBR-33; REQ-OBR-34; REQ-OBR-35; REQ-OBR-36; REQ-OBR-37; REQ-OBR-38; REQ-OBR-39; REQ-OBR-40

**Etapa do plano:** E7 · **Esforço:** M

**Risco:** Prazo: o PDF é o último item da cadeia. Depende do vídeo, dos prints e, portanto, do cluster (custo de cerca de US$ 0,47/h com 3 nós, créditos não confirmados) e do trial do PagerDuty, que termina por volta de 2026-11-11. O calendário do plano (semanas 7–8) está desatualizado (F-021).

### REQ-OBR-33 — ⬜ ausente

Incluir nomes, RMs e usernames no relatório. Não há relatório da Fase 4. A única tabela de participantes é a do Grupo 203 da Fase 3, enquanto a decisão vigente é implementação solo. A plataforma dos usernames também não está definida (Q-13).

**Ajuste da auditoria** (era ❔ a confirmar): O entregável é a tabela de identificação no relatório da Fase 4, que não existe (o próprio texto da avaliação diz que 'O relatório em si está ausente'). Procurei com find por *RELATORIO_DE_ENTREGA* e *relatorio*fase*4*, e só aparecem docs/RELATORIO_DE_ENTREGA.md (Fase 3) e a cópia dele em 00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879. A composição do grupo é uma dependência externa (Q-03/Q-13) e não o estado do requisito; usar a_confirmar esconde que nada foi produzido. Fica incoerente com REQ-OBR-32, que é ausente pelo mesmo motivo. A linha do usuário já existe e está verificada: docs/RELATORIO_DE_ENTREGA.md:12 tem a linha com o GitHub Tocaccelli (RMs não exibidos aqui).

**Falta:**

1. Confirmar com o tutor/FIAP (Discord, p. 6) a composição da entrega da Fase 4: individual ou Grupo 203 (Q-03)
2. Confirmar a plataforma dos usernames (Q-13). Na falta de resposta, incluir GitHub e, se aplicável, Discord, deixando a plataforma explícita
3. Preencher a tabela de identificação no Markdown da Fase 4 só com os participantes efetivos. Não copiar a tabela da Fase 3 sem confirmação
4. Registrar a resposta em DECISOES e atualizar Q-03/Q-13 no docs/requisitos/README.md
5. Fazer a pergunta Q-03/Q-13 já, sem esperar a E7, junto com Q-05/Q-06. A linha do próprio usuário (nome, RM e GitHub) já está em docs/RELATORIO_DE_ENTREGA.md:12 e pode ser reaproveitada sem consulta externa; só a dos demais integrantes depende da resposta.

**Depende de:** REQ-OBR-41; Resposta da FIAP/tutor a Q-03 e Q-13

**Etapa do plano:** E7 · **Esforço:** P

**Risco:** Se a FIAP considerar a entrega como do Grupo 203 e o relatório trouxer só um nome, ou o contrário, pode haver dedução ou problema de autoria. Perguntar cedo, sem esperar a E7.

### REQ-OBR-34 — 🟨 parcial

Incluir no relatório os links do repositório e do vídeo. A URL do repositório existe, mas o repositório estava privado em 2026-10-28 e o remoto não tem nenhum código da Fase 4. O vídeo não existe.

**Ajuste da auditoria** (era 🟨 parcial): Mantenho o status parcial, mas a lista 'falta' não cobre o risco de publicar o histórico. Verifiquei que scripts/security-check.sh:51 executa `git grep -InE "$pattern" -- ...`, que examina só a árvore rastreada e não o histórico. Também verifiquei que cinco arquivos não rastreados em etapas8-9 contêm o ID da conta nova (o grep comparou o conjunto de IDs sem exibi-los: um ID, diferente do ID antigo de docs/GUIA_DE_REPRODUCAO.md). A avaliação original cita 'varredura de segredos (scripts/security-check.sh)' como suficiente, e isso não é. O estado do remoto foi reconfirmado nas refs locais: origin/main=003a707 só com o PDF do desafio e origin/dev com 32 arquivos (FETCH_HEAD de 2026-10-30 10:29).

**Falta:**

1. Com autorização do usuário: curar e comitar o trabalho local (F-025), excluindo antes o offline-test.jsonl de 156 MB (F-024, não ignorado; o GitHub recusa arquivos acima de 100 MB) e decidindo sobre as 34 exclusões preexistentes
2. Com autorização: push da dev e PR/merge para a main, para que o link aponte para o código final (o ArgoCD também segue a main)
3. Decidir o acesso do avaliador: tornar o repositório público após varredura de segredos (scripts/security-check.sh) ou conceder acesso explícito. Testar o link numa janela anônima ou com conta sem acesso
4. Gravar o vídeo (REQ-OBR-23/24), publicar em plataforma com link acessível (não listado, sem login) e testar fora da conta
5. Colocar os dois links no relatório e no README.md:25, e testar os links do PDF final
6. Antes de tornar o repositório público, varrer também o HISTÓRICO (por exemplo gitleaks ou git log -p com os mesmos padrões). scripts/security-check.sh:51 usa só `git grep` na árvore rastreada e não examina commits antigos nem arquivos não rastreados. Tornar público publica os 103 commits locais, que incluem a importação da Fase 3.
7. Na curadoria, decidir conscientemente sobre os arquivos não rastreados de 00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01 (aws/PARECER_AWS_ETAPA8.md, aws/inventario-aws-sanitizado.json, github/configuracao.json, terraform/harness/tests/trust.tftest.hcl, terraform/test-oidc-offline.py). Eles contêm o ID de 12 dígitos da conta nova em ARNs. O GUIA_CONTAS_E_ACESSOS_FASE4_2026-10-28_v01.md:113-115 classifica esse dado como configuração, não como segredo, mas o security-check só barra IDs de contas antigas (linhas 70-78) e não pegaria esse. Registrar a decisão em DECISOES.
8. Registrar que a escolha de visibilidade muda outros requisitos. Se o repositório ficar público, o Secret de repositório do ArgoCD deixa de ser necessário (terraform/k8s/argocd.tf:52-53, count condicionado a github_token) e os minutos do Actions passam a ser gratuitos (GUIA_CONTAS:52). Se ficar privado, o avaliador precisa de acesso explícito, e os links de runs de REQ-OBR-38 só abrem para quem tem acesso.

**Depende de:** REQ-OBR-23; REQ-OBR-24; Autorização do usuário para commit/push/PR/merge e mudança de visibilidade; F-024; F-025

**Etapa do plano:** E7 · **Esforço:** M

**Risco:** Com o repositório privado, o avaliador pode não conseguir abrir o código. Um push sem curadoria pode falhar pelo arquivo de 156 MB ou incluir as exclusões/artefatos. Se o vídeo for gravado só no fim, sobra pouco tempo para resolver problemas de publicação.

### REQ-OBR-35 — ⬜ ausente

Incluir no relatório o print do dashboard do Grafana. Não existe Grafana, Prometheus ou Loki no repositório, nem dashboard versionado ou captura.

**Falta:**

1. E2/E3: subir o cluster e instalar a stack por GitOps (gitops/observability/ e a Application observability)
2. E4: versionar o dashboard como ConfigMap com os três painéis (recursos do cluster, taxa de requisições, logs)
3. Gerar carga e capturar um print legível do dashboard com dados reais, com horário e intervalo visíveis, e salvar a captura numa pasta de evidências
4. Inserir o print no PDF com legenda (data, cluster, origem dos dados)

**Depende de:** REQ-OBR-06; REQ-OBR-07; REQ-OBR-08; REQ-OBR-09; REQ-OBR-10; Cluster EKS ligado (E2)

**Etapa do plano:** E4 · **Esforço:** P

**Risco:** O print é rápido, mas exige o cluster ligado com a stack: custo de cerca de US$ 0,47/h, créditos não confirmados (F-026) e cota de nós para a stack. Capturar na mesma sessão da gravação para economizar horas de cluster.

### REQ-OBR-36 — ⬜ ausente

Incluir no relatório o print de um trace distribuído no APM. A instrumentação OTel dos cinco serviços funciona localmente (19 spans gravados em arquivo), mas não há exportação ao New Relic nem captura do APM.

**Falta:**

1. E1 externa: adicionar ao Collector um exporter OTLP para otlp.nr-data.net com o header api-key vindo de variável ou Secret, nunca versionado, reaplicando a sanitização
2. Provar a ingestão localmente (Compose) e depois no cluster (E3)
3. Fazer uma requisição de teste com cache vazio (evaluation → flag/targeting → auth + SQS → analytics) e localizar o trace no New Relic pelo trace_id
4. Capturar a visão detalhada do trace (waterfall com os cinco serviços) e, opcionalmente, o Service Map. Inserir no PDF com legenda

**Depende de:** REQ-OBR-12; REQ-OBR-13; REQ-OBR-14; REQ-OBR-15; Chave de ingestão New Relic

**Etapa do plano:** E1 · **Esforço:** P

**Risco:** Baixo custo: dá para capturar o trace a partir do Compose local, sem cluster. O plano gratuito do New Relic tem 100 GB/mês, uma limitação que o próprio plano registra. Se o vídeo exigir o trace vindo do cluster, a captura do PDF deve vir da mesma origem para manter a coerência.

### REQ-OBR-37 — ⬜ ausente

Incluir no relatório o print da notificação de incidente no ChatOps (Slack). Não há regra de alerta, contact point, integração PagerDuty/Slack nem captura. Existem só a conta Slack, informada pelo usuário, e o plano.

**Ajuste da auditoria** (era ⬜ ausente): Confirmei que não há nenhuma configuração de PagerDuty, Slack ou Grafana: find e grep no repositório inteiro, incluindo não rastreados, só encontram documentação e plano, e terraform/k8s/argocd.tf:146-148 desliga as notificações do ArgoCD. O status ausente está correto. Faltam, porém, dois controles de risco. O primeiro é a dependência de integração no Slack Free, que o próprio guia de contas marcou como [INCERTO] (linha 108). O segundo é uma data-limite operacional antes do fim do trial, porque o LOG:38 dá 'por volta de 2026-11-11' com base em informação do usuário, não da conta.

**Falta:**

1. E4: criar a regra de alerta e os contact points PagerDuty (Events API v2) e Slack (webhook de entrada), com segredos via Terraform/TF_VAR_*
2. Definir de onde vem a notificação 'de incidente': do contact point Slack do Grafana ou da integração PagerDuty → Slack. Garantir que a mensagem tenha detalhes (serviço, métrica, valor, link)
3. Provocar a falha, confirmar Firing → incidente no PagerDuty → mensagem no Slack, e capturar o print com o canal, o horário e o conteúdo da mensagem
4. Inserir no PDF com legenda que ligue o print ao incidente do PagerDuty
5. Confirmar o limite de apps e integrações do plano Free do Slack para o caminho escolhido (app do PagerDuty e/ou incoming webhook do Grafana). O guia de contas deixou o limite como [INCERTO] por divergência entre páginas oficiais (GUIA_CONTAS_E_ACESSOS_FASE4_2026-10-28_v01.md:108).
6. Fixar uma data-limite interna para o print e o trecho de incidente do vídeo (por exemplo 2026-11-09 ou 2026-11-10), com folga em relação ao término aproximado do trial (cerca de 2026-11-11, data não conferida na conta). Conferir a data exata no painel do PagerDuty.

**Depende de:** REQ-OBR-16; REQ-OBR-17; REQ-OBR-18; Trial do PagerDuty ativo

**Etapa do plano:** E4 · **Esforço:** P

**Risco:** Alto. Depois do trial (por volta de 2026-11-11, data não conferida na conta), o envio de eventos ao PagerDuty no plano Free não é garantido ('Events: Not included'). Se a notificação depender do PagerDuty, o print precisa ser capturado antes de 2026-11-11, junto com a gravação do vídeo. Isso adianta E2–E4, que dependem de conta e créditos AWS ainda não confirmados.

### REQ-OBR-38 — ⬜ ausente

Incluir no relatório o print do log ou da execução da automação de Self-Healing. Não existe workflow, script, role nem access entry de self-healing. Só o projeto no plano.

**Falta:**

1. E5: role OIDC própria e access entry EKS limitada ao namespace togglemaster (Terraform)
2. E5: workflow .github/workflows/self-heal.yml com repository_dispatch, filtro firing/resolved, allowlist, cooldown e kubectl rollout restart
3. E4/E5: contact point webhook no Grafana com token GitHub de escopo mínimo
4. Executar o ciclo e capturar o print do run no GitHub Actions (passos e log do rollout) e/ou do terminal 'kubectl get pods -w'. Inserir no PDF com o link do run, lembrando que o repositório é privado

**Depende de:** REQ-OBR-19; REQ-OBR-22; REQ-OBR-16; Cluster EKS ligado

**Etapa do plano:** E5 · **Esforço:** P

**Risco:** Exige cluster ligado (custo e créditos), token GitHub e role nova. O link do run só abre para quem tem acesso ao repositório privado, por isso o print é indispensável. Minutos de Actions em repositório privado consomem a franquia do plano (GUIA_CONTAS_E_ACESSOS_FASE4_2026-10-28_v01.md:52).

### REQ-OBR-39 — 🟨 parcial

Explicar brevemente no relatório a arquitetura OTel implementada. Há bom material: a arquitetura planejada no README e no plano, e o pipeline local efetivamente implementado em observability/README.md. Mas não há relatório, e a arquitetura do cluster (agents/gateway, spanmetrics, Loki, Prometheus) ainda não existe.

**Falta:**

1. Implantar a arquitetura no cluster (E3) e registrar o que de fato operou: versões dos charts, réplicas do gateway, nome real da métrica do spanmetrics
2. Escrever de meia página a uma página com um diagrama simples: SDKs → gateway (traces) / agents filelog → gateway (logs) → Prometheus/Loki/New Relic; spanmetrics; sanitização
3. Garantir que o texto descreva o implantado, não o planejado, e marcar diferenças em relação ao plano v02 (F-021)
4. Inserir no PDF e, se útil, reaproveitar o mesmo diagrama no vídeo (REQ-OBR-26)

**Depende de:** REQ-OBR-06; REQ-OBR-07; REQ-OBR-08; REQ-OBR-11; REQ-OBR-20

**Etapa do plano:** E7 · **Esforço:** M

**Risco:** Baixo para o texto. O risco é descrever no PDF uma arquitetura que não foi implantada ou que mudou durante a E3, criando incoerência com o vídeo.

### REQ-OBR-40 — 🟨 parcial

Justificar no relatório New Relic em vez de Datadog e PagerDuty em vez de OpsGenie. As razões estão registradas em decisões e no plano, com fontes de 2026-09. Falta redigi-las no relatório e reconfirmar as condições comerciais perto da entrega.

**Falta:**

1. Reconfirmar em fonte oficial, perto da redação, as condições usadas: plano gratuito do New Relic, APM fora do free do Datadog e situação do OpsGenie. Registrar a data da consulta
2. Redigir dois parágrafos curtos com critérios técnicos e de custo: OTLP nativo do New Relic e Service Map; disponibilidade e continuidade do OpsGenie; integrações PagerDuty–Grafana–Slack
3. Declarar honestamente a limitação de Events no plano Free do PagerDuty, que obrigou a demonstração dentro do trial
4. Inserir no PDF, coerente com o que aparece no vídeo

**Depende de:** REQ-OBR-12; REQ-OBR-17

**Etapa do plano:** E7 · **Esforço:** P

**Risco:** Baixo. A informação comercial de 2026-09 pode mudar. Afirmar 'APM fora do plano gratuito' sem reconfirmar pode ser contestado.

### REQ-OBR-41 — ❔ a confirmar

Desenvolver em grupo, pela interpretação conservadora de 'em princípio'. O usuário decidiu implementar sozinho, e não há confirmação da FIAP de que a entrega individual é aceita. O relatório da Fase 3 indica o Grupo 203 com cinco integrantes.

**Falta:**

1. Perguntar ao tutor no Discord (canal indicado na p. 6) se a entrega individual é aceita na Fase 4 ou se a entrega continua vinculada ao Grupo 203
2. Guardar a resposta (print ou texto com data) como evidência e registrar em DECISOES
3. Se a resposta for 'grupo': combinar com os integrantes a participação e a autoria, e ajustar REQ-OBR-33
4. Atualizar Q-03 em docs/requisitos/README.md

**Depende de:** Resposta da FIAP/tutor (Q-03)

**Etapa do plano:** E7 · **Esforço:** P

**Risco:** Perguntar tarde (na E7) deixa pouco tempo para ajustar a composição ou a autoria antes de 2026-11-17. O custo de perguntar já é baixo.

### REQ-OBR-42 — ❔ a confirmar

Submeter código, vídeo e relatório dentro do prazo oficial. O prazo de 2026-11-17 foi informado pelo usuário; o PDF não traz data, horário nem canal. Hoje nenhum dos três entregáveis está pronto e o código não chegou ao remoto.

**Falta:**

1. Confirmar com a FIAP data, horário, plataforma e procedimento de submissão (Q-05/Q-06), e registrar a fonte
2. Replanejar o calendário (F-021) com o caminho crítico E2→E5 e gravação do trecho de incidente antes de 2026-11-11 (trial do PagerDuty)
3. Com autorização: ignorar ou remover do índice o arquivo de 156 MB, curar e comitar, push, PR dev→main e merge
4. Garantir o acesso do avaliador ao repositório e ao vídeo (ver REQ-OBR-34)
5. Gerar o PDF final (REQ-OBR-32), submeter os três itens até a meta interna de 2026-11-12, guardar o comprovante e registrar em LOG/PENDENCIAS

**Depende de:** REQ-OBR-23; REQ-OBR-24; REQ-OBR-32; REQ-OBR-34; Resposta da FIAP a Q-05/Q-06; Autorização do usuário para commit/push/PR

**Etapa do plano:** E7 · **Esforço:** M

**Risco:** Alto quanto ao prazo. Faltam 18 dias para 2026-11-17 e 13 para a meta de 11-12. Nada foi implantado na AWS (sem tfvars, init, plan ou apply). Os créditos e o plano da conta AWS não foram confirmados (F-026). O trial do PagerDuty termina por volta de 11-11. O código não está no remoto. O prazo vem do usuário, não do PDF.

### REQ-BON-01 — ⬜ ausente

Opcional: usar o Grafana Alloy no lugar do OTel Collector padrão, mantendo as funções centrais de OTel.

**Falta:**

1. Nenhuma tarefa obrigatória. Se o usuário quiser o bônus: obter resposta à Q-10 no Discord da FIAP antes de trocar o Collector
2. Caso adote: config River/Alloy equivalente (otelcol.receiver.otlp, processors, exporters Prometheus/Loki/New Relic, coleta de logs dos pods), chart grafana/alloy em gitops/observability/ e explicação no vídeo e no relatório

**Depende de:** Resposta da FIAP à Q-10; Decisão do usuário (o plano recomenda o Collector padrão)

**Etapa do plano:** nenhuma (fora do plano; E3 só se o usuário mudar a decisão) · **Esforço:** P

**Risco:** Adotar o Alloy agora gasta prazo e pode criar dúvida na avaliação dos itens que nomeiam o 'OTel Collector' (REQ-OBR-20 e 26). O PDF não promete pontos extras pelo Alloy (auditoria-codex-2026-10-30_v01/MATRIZ_REQUISITOS.md:7).

### REQ-BON-02 — 🟦 implementado, falta demonstrar

Preferir bibliotecas OpenTelemetry da linguagem na instrumentação (preferência do PDF p. 4; a instrumentação continua obrigatória).

**Falta:**

1. Versionar o código (REQ-OBR-21)
2. Mencionar explicitamente no relatório (REQ-OBR-39) que a instrumentação usa só SDKs e instrumentadores OpenTelemetry, com OTLP para o Collector e daí para o New Relic, sem agente do fornecedor
3. Mostrar no vídeo, de forma breve, os arquivos telemetry.* / dependências e o atributo telemetry.sdk.name no trace do NR (a allowlist o mantém, otel-collector-local.yaml:33)

**Depende de:** REQ-OBR-21 (commit/publicação); REQ-OBR-14 (demonstração no APM)

**Etapa do plano:** E1 · **Esforço:** P

**Risco:** Baixo. Só existe o risco comum de o código não ser entregue se o commit não acontecer (F-025). As bibliotecas Python de instrumentação são beta (0.66b1); no Go, otelhttp é contrib v0.x. Ambas foram testadas localmente.

## Apêndice C — Achados descartados na verificação (2)

- **CMP-05 — Script de init do Postgres não é executável no Git e acaba 'sourced' pelo entrypoint** (`infra/postgres-app/01-init-multi-db.sh`): O modo 100644 se confirma (git ls-files -s), e o arquivo é o mesmo blob 891e063 em tech-challenge-03. Só que o mesmo arquivo 644 rodou no CI Linux da Fase 3: tech-challenge-03/docs/00_COLAB_IA/LOG_DE_TRABALHO.md:216 registra 'Compose Integration - todos success' e a linha 320 confirma o Compose Integration no HEAD. O script (infra/postgres-app/01-init-multi-db.sh:1-12) só chama psql com variáveis definidas no compose (linhas 29-33). A falha descrita fica sem evidência, e o próprio achado admite isso. Dar o bit de execução seria só um ajuste estético.
- **GIT-13 — PVC do Postgres pode ficar órfão no destroy do cluster efêmero** (`gitops/base/postgres-targeting/statefulset.yaml`): Já tratado: docs/GUIA_DE_REPRODUCAO.md:600-616 manda destruir na ordem k8s, cluster, base, e a linha 643 já traz a verificação 'aws ec2 describe-volumes --filters Name=status,Values=available'. Destruir a camada k8s apaga kubernetes_namespace_v1.app, o que remove o PVC, e a StorageClass com reclaim Delete (terraform/k8s/storageclass.tf:56-61) apaga o EBS. Além disso, persistentVolumeClaimRetentionPolicy só age quando o StatefulSet é apagado e não evitaria o órfão no cenário descrito (cluster destruído direto). Resta no máximo um reforço opcional.
