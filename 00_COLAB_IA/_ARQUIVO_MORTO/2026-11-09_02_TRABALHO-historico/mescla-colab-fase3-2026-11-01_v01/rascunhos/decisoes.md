## Decisões herdadas da Fase 3 (mescladas em 2026-11-01)

Esta seção traz as decisões da memória de trabalho da Fase 3 (`docs/00_COLAB_IA/`, 39 arquivos importados com o histórico em 2026-10-20). Os IDs levam o prefixo `F3-`. `F3-D-0NN` repete o número oficial da Fase 3. `F3-SN-NN` marca decisão que estava espalhada em LOG, runbooks e guias, sem número próprio. A ordem dos `F3-SN` segue o tema, não a data. As fontes usam caminhos relativos a `docs/00_COLAB_IA/`. Os originais ficam no commit 3b21e65 (`git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`) e no repositório `tech-challenge-03`. As referências `arquivo:linha` da Fase 4 valem para a árvore de trabalho da `dev` em 2026-11-01. Essa árvore tem alterações sem commit e difere do HEAD 3b21e65 em alguns pontos.

Vigência na Fase 4:

- **vigente**: continua valendo e já está no código ou no processo atual.
- **revisar**: o princípio é útil, mas a premissa mudou (conta, custo, escopo ou ferramenta). Precisa de decisão ou ADR da Fase 4.
- **superada**: substituída por decisão posterior, da Fase 3 ou da Fase 4.
- **histórica**: explica a origem de algo. Não orienta o trabalho atual.

| ID | Decisão (1 linha) | Vigência na Fase 4 | Relação na Fase 4 |
|---|---|---|---|
| F3-D-001 | `tech-challenge-03` como destino da Fase 3 | superada | Substituída por D-009 e D-014 |
| F3-D-002 | Guias de estudo em Markdown por módulo | superada | Substituída por F3-D-005; a Fase 4 usa guias HTML (D-004) |
| F3-D-003 | Terraform modular, GitHub Actions, ECR, ArgoCD e EKS em conta AWS pessoal | vigente | Base mantida por D-009, D-012 e D-014; TFB-05, TFC-02 |
| F3-D-004 | Não copiar materiais da fase anterior para o repositório novo | revisar | Conflita com F3-SN-31; 34 deleções pendentes (B0); DOC-11 |
| F3-D-005 | Guias de estudo em HTML, um por módulo | vigente | Já coberta por D-003, D-004 e D-005 |
| F3-D-006 | Entrega em grupo com prazo 2026-09-15 | superada | Substituída por D-009 (solo, 2026-11-17); DOC-08 |
| F3-D-007 | Monorepo com serviços, Terraform, GitOps e pipelines | vigente | Preservado por D-014; self-healing no mesmo repositório (CIC-01) |
| F3-D-008 | GitOps com Kustomize (base por serviço, overlay por ambiente) | vigente | GIT-01 e GIT-03: falta decidir como a observabilidade entra |
| F3-D-009 | Tags `project`/`phase` em minúsculas via `default_tags` | revisar | Valor agora é `phase = "4"`; TFC-05, TFB-07 |
| F3-D-010 | Módulos Terraform híbridos (só a VPC da comunidade) | vigente | TFB-11, XCL-15, TFB-05 |
| F3-D-011 | Ambiente único chamado `prod` | vigente | Coerente com D-010 |
| F3-D-012 | Sem Ingress nem Load Balancer; acesso por `port-forward` | revisar | Falta ADR da Fase 4 (XCL-04); TFK-02 |
| F3-D-013 | Segredos via Secrets Manager + ESO | superada | Substituída por F3-D-018; GIT-08 |
| F3-D-014 | Manifestos da Fase 2 como base do GitOps | histórica | Origem dos manifestos estendidos na Fase 4; GIT-15, GIT-05 |
| F3-D-015 | 2 RDS + banco do targeting em StatefulSet no EKS | revisar | Premissa do plano gratuito pode não valer (D-012); TFC-06 |
| F3-D-016 | Node group com 2 x c7i-flex.large | revisar | D-015 cita 3 workers; TFC-01, XCL-10, TFC-04, TFC-06 |
| F3-D-017 | Terraform em 3 camadas com estados separados | vigente | Mantido por D-014 (chaves `phase4/prod`); TFB-01, XCL-03, TFK-05 |
| F3-D-018 | Sem ESO: o Terraform cria os Secrets do Kubernetes | revisar | Não cobre credenciais de terceiros; XCL-09, CMP-02, TFK-04, TFC-09, GIT-08 |
| F3-D-019 | Preferência `dev` -> PR -> `main` | superada | Absorvida por F3-D-020 e F3-D-021 |
| F3-D-020 | Trabalho humano só na `dev`; promoção por PR | vigente | Coerente com D-014 e CLAUDE.md:8; CIC-07, XCL-01 |
| F3-D-021 | Robô do CI comita a tag direto na `main` | revisar | Push/PR/main suspensos (CLAUDE.md:8); CIC-07, CIC-03, TFK-03, GIT-03, TFB-05 |
| F3-D-022 | Provedor OIDC: criar ou reaproveitar (`create_github_oidc_provider`) | revisar | Provedor já criado à mão na conta nova; TFB-03, TFB-01, XCL-03 |
| F3-D-023 | Ordem de subida e destruição, com planos salvos em arquivo | revisar | TFK-03, GIT-03, TFB-01, TFC-05, DOC-02 |
| F3-D-024 | Consolidação da documentação pública (README, guia, arquitetura) | revisar | DOC-02, DOC-07, CMP-03, TFB-04, DOC-12 |
| F3-SN-01 | Região us-east-2 em tudo | vigente | Mantida na conta nova; TFB-07 |
| F3-SN-02 | Bucket de estado criado à mão, versionado e protegido | vigente | Coerente com D-014 (backend parcial); DOC-13 |
| F3-SN-03 | Nome do bucket com ID da conta e região | superada | Substituída por D-014; DOC-12, XCL-14 |
| F3-SN-04 | Lock nativo do S3 (`use_lockfile`) e Terraform >= 1.11 | vigente | Mantido por D-014; TFK-04 |
| F3-SN-05 | NAT por variável, com padrões opostos | vigente | TFB-10, TFC-12 |
| F3-SN-06 | Custo entre sessões: pausa com NAT desligado ou destruir a base | revisar | Nenhuma política escolhida; XCL-10, TFB-01, XCL-03 |
| F3-SN-07 | Exclusão completa com a Application removida antes | revisar | TFC-05, GIT-13, DOC-02 |
| F3-SN-08 | Plano ordenado por custo, cluster no fim | vigente | Sobrepõe D-010 e D-016 |
| F3-SN-09 | Âncora de escopo: entregar o básico que funciona | revisar | A lista de exclusões da Fase 3 não vale; D-002 |
| F3-SN-10 | EKS em suporte padrão (1.34 em vez de 1.31) | revisar | TFC-03, TFK-02 |
| F3-SN-11 | Sem chave estática da AWS: OIDC no CI e IRSA nos pods | vigente | TFB-04, CMP-03, TFB-05, CIC-03, TFC-10 |
| F3-SN-12 | Imagem por nome lógico; URL da fila em ConfigMap | vigente | GIT-03, GIT-06, GIT-02 |
| F3-SN-13 | ArgoCD por chart oficial fixo, com prune e selfHeal | revisar | TFK-02, GIT-04, TFK-06, TFK-09 |
| F3-SN-14 | Bootstrap do ArgoCD em duas etapas (`-target`) | vigente | Mesma armadilha para CRDs novos; TFK-05 |
| F3-SN-15 | Reconciliação do ArgoCD em 30 s | vigente | Afeta o tempo de recuperação nas demos |
| F3-SN-16 | Credencial do repositório para o ArgoCD só com token | revisar | Repositório 04 privado; TFK-11, TFK-04 |
| F3-SN-17 | Senha inicial do ArgoCD fora dos outputs | vigente | Mesmo princípio para Grafana e terceiros; TFK-09 |
| F3-SN-18 | `SERVICE_API_KEY` provisória com `ignore_changes` | vigente | Padrão reutilizável; candidato a automação |
| F3-SN-19 | Schemas do RDS aplicados por pod `psql` descartável | vigente | DOC-02 |
| F3-SN-20 | Trivy estrito com exceções nominais datadas | revisar | Revisão vencida; CIC-08, CIC-10, CIC-14 |
| F3-SN-21 | Scans sem `continue-on-error`; Go 1.25 e lint 2.x em cascata | vigente | D-016 fixou OTel compatível com Go 1.25; CIC-04 |
| F3-SN-22 | Lint e SAST: corrigir o real, `nosec` pontual, estilo em `.pylintrc` | revisar | CIC-02, CIC-11, CIC-17 |
| F3-SN-23 | Gate de imagem por `needs`; CI sem `kubectl apply` | revisar | Self-healing precisa de exceção; CIC-01, XCL-08, TFB-05, TFC-02, GIT-07 |
| F3-SN-24 | Imagem e tag só em push na `main` | revisar | CIC-13, GIT-03 |
| F3-SN-25 | CI de Terraform só com `fmt` e `validate` | revisar | Self-healing dá AWS ao CI; CIC-06, CIC-09, GIT-14 |
| F3-SN-26 | SQS desligado no Compose padrão; Moto no perfil de integração | vigente | Base de D-010 e D-016; CIC-15 |
| F3-SN-27 | Demo só com regras PERCENTAGE 100 ou 0 | vigente | Tráfego controlado para alertas; F-017 |
| F3-SN-28 | Usuário IAM com MFA para o bootstrap; root sem chave | revisar | TFC-02 |
| F3-SN-29 | Estimativa de custo em um único lugar | revisar | XCL-10, TFB-10, TFC-06 |
| F3-SN-30 | Gerador do PDF do relatório | revisar | Nenhum gerador ativo; DOC-01 |
| F3-SN-31 | Material de aula mantido no repositório | revisar | Conflita com F3-D-004; 34 deleções pendentes; DOC-11 |
| F3-SN-32 | Vídeo no YouTube como Não listado | revisar | Etapa B5/B6 do plano P-015 |
| F3-SN-33 | Plano de gravação de 2026-09-15 substitui o guia de 2026-09-11 | histórica | Lição: roteiro para o estado real da conta e um plano C |
| F3-SN-34 | Demo DevSecOps/GitOps com PyYAML no flag-service | histórica | Só se a demo for repetida |
| F3-SN-35 | Caminho C e merge híbrido com `-X theirs` | histórica | Lição: `-X theirs` descartou código em silêncio |

Os códigos TFB, TFC, TFK, GIT, CIC, CMP, DOC e XCL são achados da análise P-015 pelo código.

### F3-D-003 — Terraform modular, GitHub Actions, ECR, ArgoCD e EKS em conta pessoal (vigente; data [INCERTO], registrada entre 2026-07-17 e 2026-07-18)

Contexto: o enunciado da Fase 3 pede IaC, CI/CD, DevSecOps e GitOps para o ToggleMaster.

Decisão: usar Terraform modular, GitHub Actions, ECR, ArgoCD e EKS. Usar conta AWS pessoal, não AWS Academy/LabRole.

Motivo: com AWS Academy/LabRole não é possível criar roles e policies IAM pelo Terraform.

Alternativas: Jenkins; FluxCD; AWS Academy com LabRole; `kubectl apply` direto no CI.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/main.tf:47-50` e `:94-129` (módulos); `terraform/k8s/argocd.tf:104` (ArgoCD por Helm); `.github/workflows/_ci-go.yml:326-331` (CI com imagem para o ECR); `terraform/providers.tf:14` (`allowed_account_ids` com `expected_aws_account_id`).
- Relação: base mantida por D-009, D-012 e D-014. TFB-05 e TFC-02 pedem identidades novas para o self-healing.
- Ressalva: documentos da Fase 3 (`_ARQUIVO_MORTO/ARQUITETURA.md:42-44`, `_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md:90-92` e `scripts/security-check.sh:70`) chamam a conta pessoal de "D-016". No registro oficial, a conta pessoal é a D-003, e a D-016 é o c7i-flex.large.

Fonte F3: `DECISOES.md:320-328`; `_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md:100`; `_ARQUIVO_MORTO/ARQUITETURA.md:42-44`; `_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md:90-92`.

### F3-D-004 — Não copiar materiais da fase anterior (revisar, 2026-07-18)

Contexto: os materiais da fase anterior ajudam a entender containers, Kubernetes e escalabilidade.

Decisão: usar PDFs e guias da fase anterior como fonte externa. Não copiá-los para o repositório da fase seguinte. Registrar só sínteses próprias.

Motivo: evitar insumos duplicados.

Alternativas: versionar todo o material da fase anterior no repositório novo.

Na Fase 4:
- Vigência: revisar.
- Evidência: no `git status`, 34 arquivos da Fase 3 em `docs/` (PDFs, guias e enunciado) aparecem apagados, sem commit; `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:11` (B0: "decidir as 34 deleções").
- Relação: a importação por merge trouxe esses materiais para o repositório. Conversa com a D-002 (checklist da Fase 3 só como estrutura). Conflita com a F3-SN-31. Achado DOC-11. A remoção depende de decisão do usuário.

Fonte F3: `DECISOES.md:330-338`; `LOG_DE_TRABALHO.md:571-581`; `_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md:98-102`.

### F3-D-005 — Guias de estudo HTML, um por módulo (vigente, 2026-07-18)

Contexto: os guias em Markdown não atenderam, e o usuário decidiu estudar por partes.

Decisão: um guia HTML por vez, salvo na pasta do módulo. Cada guia tem introdução para leigos, glossário, fichas (finalidade, caso de uso, aplicação no ToggleMaster) e resumo. O padrão visual é o do guia de containers da Fase 2.

Motivo: os guias em Markdown não atenderam.

Alternativas: manter Markdown; pasta separada; gerar todos de uma vez.

Na Fase 4:
- Vigência: vigente.
- Evidência: `git ls-files` lista os cinco guias em `docs/aulas-fiap/<módulo>/GUIA-ESTUDO-*.html`; `00_COLAB_IA/DOSSIE_CONTEXTO.md:16`.
- Relação: já coberta por D-003, D-004 e D-005. Não precisa de entrada nova.

Fonte F3: `DECISOES.md:310-318`; `LOG_DE_TRABALHO.md:479`; `LOG_DE_TRABALHO.md:563`.

### F3-D-006 — Entrega em grupo com prazo 2026-09-15 (superada, 2026-07-30)

Contexto: o enunciado diz que o trabalho é "em princípio" em grupo e pede os nomes no relatório, mas não traz prazo.

Decisão: entrega em grupo, prazo final 2026-09-15, repositório público.

Motivo: o prazo veio do usuário, não do enunciado.

Alternativas: entrega individual; seguir sem data.

Na Fase 4:
- Vigência: superada pela D-009 (implementação solo, entrega 2026-11-17).
- Evidência: `00_COLAB_IA/DECISOES.md:73`; `docs/requisitos/README.md:90` (REQ-OBR-41 "em grupo", com [INCERTO]).
- Relação: achado DOC-08, sem confirmação do tutor. Lição útil: o enunciado pode não trazer prazo, e o relatório pede identificação dos participantes. Não copiar a tabela de integrantes da Fase 3.

Fonte F3: `DECISOES.md:280-288`; `INSTRUCOES_ASSISTENTES.md:11`, `:13`; `LOG_DE_TRABALHO.md:453-459`.

### F3-D-007 — Monorepo com serviços, Terraform, GitOps e pipelines (vigente, 2026-08-27)

Contexto: era preciso decidir onde ficariam código, infraestrutura, manifestos e pipelines.

Decisão: os 5 microsserviços ficam em `services/`. A infraestrutura fica em `terraform/`, o Kustomize em `gitops/` e os pipelines em `.github/workflows/`. Os serviços se chamam `<nome>-service`, como no ECR e no Kustomize.

Motivo: o CI dispara em PR e push. O passo de tag vira commit no próprio repositório, sem token cruzado. O enunciado aceita pasta GitOps no monorepo.

Alternativas: código em repositório externo; repositório GitOps separado (opcional no enunciado, não adotado).

Na Fase 4:
- Vigência: vigente.
- Evidência: pastas `services/`, `terraform/`, `gitops/` e `.github/workflows/`; `.github/workflows/auth-service.yml:45-52` (filtro de caminho); `.github/workflows/_ci-go.yml:583` (tag no mesmo repositório).
- Relação: estrutura preservada pela D-014. O self-healing roda no mesmo repositório (CIC-01). Consequência herdada: o robô comita a tag no próprio repositório (F3-D-021).

Fonte F3: `DECISOES.md:268-278`; `INSTRUCOES_ASSISTENTES.md:24`; `ORGANIZACAO_DE_PASTAS.md:3`; `LOG_DE_TRABALHO.md:441-443`.

### F3-D-008 — GitOps com Kustomize (vigente, 2026-08-27)

Contexto: era preciso escolher o formato dos manifestos que o ArgoCD aplica.

Decisão: Kustomize em `gitops/`, com `base/<serviço>` e `overlays/<ambiente>`. Uma Application do ArgoCD (`togglemaster`) gerencia os 5 serviços. O Helm só instala o próprio ArgoCD.

Motivo: Kustomize é nativo do `kubectl` e do ArgoCD, sem templating. O CI muda um único campo do overlay com `kustomize edit set image`, fácil de automatizar e auditar.

Alternativas: YAML puro (duplica manifesto por ambiente); Helm Charts próprios (mais complexidade); cinco Applications (descartado).

Na Fase 4:
- Vigência: vigente.
- Evidência: `gitops/base/kustomization.yaml`; `gitops/overlays/prod/kustomization.yaml:65-80` (bloco `images`); `.github/workflows/_ci-go.yml:583`; `terraform/k8s/argocd.tf:297-301`.
- Relação: GIT-01 (stack de observabilidade ausente do GitOps) e GIT-03 (sentinelas no overlay). Falta decidir como Prometheus, Loki, Grafana e Collector entram (nova Application com Helm ou Kustomize) sem quebrar o fluxo de tag.
- Ressalvas: a tag fica no `kustomization.yaml`, não no `deployment.yaml` citado no enunciado da Fase 3; explicar no vídeo. O CI exige o binário `kustomize` standalone.

Fonte F3: `DECISOES.md:256-266`; `LOG_DE_TRABALHO.md:383`, `:443`; `_ARQUIVO_MORTO/ARQUITETURA.md:23`, `:86`.

### F3-D-009 — Tags `project` e `phase` em minúsculas via `default_tags` (revisar, 2026-08-27)

Contexto: o relatório exige print de custo, e a AWS diferencia maiúsculas nas chaves de tag.

Decisão: todo recurso recebe `project = fiap` e `phase = 3`, em minúsculas, uma vez via `default_tags` no provider. O bucket de estado recebeu as tags à mão. As versões antigas do estado expiram em 30 dias.

Motivo: rastrear custo no Cost Explorer. `Project` e `project` virariam grupos separados. 30 dias bastam porque o estado é pequeno.

Alternativas: tags capitalizadas (registradas às 13:10 e corrigidas às 15:55 de 2026-08-27); tag por recurso; lifecycle de 90 dias (descartado pelo grupo).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/variables.tf:53-59` (`project = fiap`, `phase = "4"`); `terraform/terraform.tfvars.example:28`; `terraform/providers.tf:23-26`, `terraform/cluster/providers.tf:12-13` e `terraform/k8s/providers.tf:22-23` (`default_tags`). `terraform/k8s/storageclass.tf` não define tags para os volumes do CSI.
- Relação: regra mantida pela D-014, agora com `phase = 4`. TFC-05 (volumes EBS do CSI sem tags; guia ainda filtra `phase=3`) e TFB-07 (falta validar a tag `phase`). As consultas de conferência e de sobras precisam usar `phase=4`.

Fonte F3: `DECISOES.md:246-254`; `INSTRUCOES_ASSISTENTES.md:25`; `LOG_DE_TRABALHO.md:395`, `:419`; `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md:176-178`.

### F3-D-010 — Módulos Terraform híbridos (vigente, 2026-08-27; nota de 2026-09-15)

Contexto: construir o EKS do zero é onde projetos perdem dias, e o enunciado cobra autoria.

Decisão: o plano inicial tirava VPC e EKS da comunidade. No estado final, só a VPC vem da comunidade (`terraform-aws-modules/vpc/aws ~> 5.0`). Os outros 7 módulos são próprios: eks, ecr, messaging, iam-ci, rds, elasticache e irsa.

Motivo: os demais recursos são simples e preservam a autoria exigida.

Alternativas: tudo da comunidade; tudo à mão.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/main.tf:47-50`; `terraform/modules/`; `terraform/cluster/main.tf:45-47`; `terraform/backend.tf:35` (provider AWS `>= 5.46`, sem teto).
- Relação: TFB-11 (provider sem teto), XCL-15 (lockfiles divergentes), TFB-05 (sugere módulo novo para a role do self-healing).
- Ressalva: o provider ficou sem teto para não conflitar com o módulo de VPC. Na Fase 3, a versão resolvida foi o módulo 5.21.0 com o provider AWS 6.62.0.

Fonte F3: `DECISOES.md:232-244`; `LOG_DE_TRABALHO.md:399`, `:407`.

### F3-D-011 — Ambiente único chamado `prod` (vigente, 2026-08-27)

Contexto: cada ambiente extra multiplica o custo de EKS, RDS e ElastiCache.

Decisão: um só ambiente, com o overlay `gitops/overlays/prod` e estados com prefixo `prod`. Sem overlays `dev` ou `hml`.

Motivo: o enunciado não pede vários ambientes. A estrutura base + overlay permite expandir depois.

Alternativas: dev + prod; dev/staging/prod; overlay único chamado `dev`.

Na Fase 4:
- Vigência: vigente.
- Evidência: `gitops/overlays/` só tem `prod`; `terraform/backend.tf:43`, `terraform/cluster/backend.tf:47` e `terraform/k8s/backend.tf:55` (chaves `phase4/prod/...`).
- Relação: coerente com a D-010 (ambiente único que segue a `main`). A branch `dev` do Git não corresponde a ambiente AWS.

Fonte F3: `DECISOES.md:220-230`; `LOG_DE_TRABALHO.md:381`, `:407`.

### F3-D-012 — Sem Ingress e sem Load Balancer; acesso por `port-forward` (revisar, 2026-08-27)

Contexto: na Fase 2, o Ingress exigia Nginx Ingress Controller e um Load Balancer.

Decisão: Services ClusterIP, sem Ingress nem LB. O ArgoCD (8080:80) e os serviços (8001-8004) são acessados por `port-forward` no vídeo.

Motivo: o LB custaria cerca de US$ 16-20/mês. Em 2026-08-27, a varredura do PDF da Fase 3 (7 páginas) achou zero ocorrências de ingress, load balancer, acesso externo, http, url, endpoint, expor, público, nginx e alb. A escolha também evita LB órfão segurando subnet no destroy.

Alternativas: manter o Ingress/ALB da Fase 2 (melhor demo, cerca de US$ 16-20/mês a mais).

Na Fase 4:
- Vigência: revisar.
- Evidência: `gitops/base/*/service.yaml` com `type: ClusterIP` (auth :23, evaluation :20, flag :20, targeting :17, analytics :18); `gitops/base/kustomization.yaml:73`; `terraform/k8s/outputs.tf:23`; `README.md:129-132` (a Fase 4 só prevê chamadas de saída).
- Relação: XCL-04 (decisão segue valendo, mas sem ADR da Fase 4). TFK-02 usa a falta de Ingress para rebaixar o risco da CVE do ArgoCD. Sem Ingress não há webhook do GitHub, por isso a reconciliação caiu para 30 s (F3-SN-15). Repetir a varredura no enunciado da Fase 4 antes de manter. Se entrar LB, incluí-lo na ordem de destroy.

Fonte F3: `DECISOES.md:208-218`; `INSTRUCOES_ASSISTENTES.md:31-32`; `LOG_DE_TRABALHO.md:383`, `:407`; `_ARQUIVO_MORTO/ARQUITETURA.md:15`, `:33-35`.

### F3-D-013 — Segredos via Secrets Manager + ESO (superada, 2026-08-27)

Contexto: na Fase 2, analytics e evaluation recebiam `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` estáticas num Secret. O enunciado critica credenciais em arquivos sem segurança.

Decisão: o Terraform geraria senhas (`random_password`) no Secrets Manager. O ESO sincronizaria para Secrets do Kubernetes. Chaves estáticas da AWS seriam trocadas por IRSA.

Motivo: tirar credenciais de arquivos.

Alternativas: Secret preenchido à mão; SSM Parameter Store; Secrets criados pelo Terraform (adotado depois).

Na Fase 4:
- Vigência: superada pela F3-D-018 (ESO cortado em 2026-09-01). A parte IRSA continua na F3-SN-11.
- Evidência: não há ExternalSecret nem SecretStore em `gitops/`; `gitops/SECRETS-CONTRATO.md:10`. Ainda há comentários sobre ESO em `gitops/base/auth-service/deployment.yaml:68`, `evaluation-service/deployment.yaml:61` e `flag-service/deployment.yaml:51`.
- Relação: achado GIT-08 (comentários desatualizados). Lição: ao cortar o ESO, o código substituto não foi escrito na hora. Nada criou os 5 Secrets até a correção de 2026-09-09.

Fonte F3: `DECISOES.md:196-206`; `LOG_DE_TRABALHO.md:258`, `:377`.

### F3-D-015 — Dois RDS e banco do targeting em StatefulSet (revisar, 2026-08-27)

Contexto: o enunciado da Fase 3 exige 3 instâncias RDS. O plano gratuito da conta da Fase 3 recusou a terceira ("maximum number of instances available with free plan accounts").

Decisão: `auth_db` e `flags_db` em RDS PostgreSQL 16. `targeting_db` em StatefulSet `postgres-targeting`, com PVC gp3 de 5 GB e os manifestos da Fase 2. A P-031 (migrar para RDS) foi cancelada.

Motivo: em 2026-08-27, o professor confirmou que o arranjo da Fase 2 seguia aceito. Sair do plano gratuito exigiria pagamento e tiraria a proteção contra gasto, com US$ 70,33 de crédito restante.

Alternativas: sair do plano gratuito; 1 RDS com três bancos (não atende "3 instâncias"); 3 RDS literais.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/cluster/variables.tf:127-139` (só auth e flag; a descrição pede revalidar cotas); `gitops/base/postgres-targeting/statefulset.yaml:56`; `terraform/k8s/storageclass.tf:36,61` (StorageClass default, reclaim Delete).
- Relação: a D-012 registra que conta nova de quem já teve conta não ganha Free plan nem crédito. O limite que motivou a decisão pode não existir [INCERTO: plano de cobrança da conta nova não verificado]. TFC-06 aponta comentários que tratam a aprovação e os custos como fato atual.
- Ressalvas: a aprovação do professor valeu para a Fase 3, e não há comprovante escrito localizado. Se a decisão for mantida, o relatório da Fase 4 precisa explicar o desvio. O StatefulSet exige o addon EBS CSI e StorageClass default. O disco de 5 GB fica fora dos estados e precisa sumir antes do destroy do EKS. Os schemas de auth e flag são aplicados à mão (F3-SN-19).

Fonte F3: `DECISOES.md:170-182`; `INSTRUCOES_ASSISTENTES.md:28`, `:32`, `:128`; `LOG_DE_TRABALHO.md:260-261`, `:314`, `:363`, `:383`, `:413`; `_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md:30-31`.

### F3-D-016 — Node group com 2 x c7i-flex.large (revisar, 2026-08-27)

Contexto: a conta da Fase 3 recusou t3.medium ("not eligible for Free Tier"), escolhida no mesmo dia (medida em F-020).

Decisão: c7i-flex.large (2 vCPU / 4 GB), o mesmo tipo da Fase 2. Mínimo 1, desejado 2, máximo 4.

Motivo: c7i-flex.large é equivalente e foi aceito naquele plano. t3.micro comporta cerca de 4 pods e 1 GB. t4g é ARM, e as imagens são x86. m7i-flex.large custava mais sem necessidade.

Alternativas: sair do plano gratuito e usar t3.medium (descartado junto com a F3-D-015).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/cluster/variables.tf:86` (tipo), `:92` (mínimo 1), `:102` (desejado 2), `:108` (máximo 4); `terraform/cluster/main.tf:59` (comentário "F-023, D-016" com IDs da Fase 3).
- Relação: a D-015 da Fase 4 cita três workers como proposta. TFC-01 (2 nós de 4 GiB não comportam com folga a observabilidade), XCL-10 (2 nós no IaC x 3 na documentação), TFC-04 (`max_size` 4 sem autoscaler), TFC-06.
- Ressalvas: cerca de US$ 0,085/h por nó, perto do dobro da t3.medium. Na estimativa da Fase 3, 2 nós custavam US$ 126,99/mês (730 h). O sizing da Fase 3 considerava 450m CPU/512Mi das aplicações mais o ArgoCD, sem observabilidade. A elegibilidade na conta nova não foi verificada.

Fonte F3: `DECISOES.md:156-168`; `LOG_DE_TRABALHO.md:395`, `:407`; `_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md:12-13`.

### F3-D-017 — Terraform em 3 camadas com estados separados (vigente, 2026-08-27; camada k8s desde 2026-09-09)

Contexto: com estado único, o destroy de fim de sessão levaria os ECR e, com `force_delete`, as imagens.

Decisão: três raízes independentes no mesmo bucket.
- `terraform/` (base): VPC, 5 ECR, SQS+DLQ, DynamoDB, role do CI e OIDC.
- `terraform/cluster/`: EKS, node group, 2 RDS, ElastiCache e 2 roles IRSA.
- `terraform/k8s/`: namespaces, 5 Secrets, StorageClass gp3, ArgoCD e Application.

Cada camada lê a anterior por `terraform_remote_state`, e o plan falha se a anterior não existir.

Motivo: o CI não precisa reconstruir as 5 imagens. A camada k8s é separada porque o provider dela depende do cluster criado por outra camada.

Alternativas: estado único com `destroy -target` (frágil); estado único recriando ECR sempre; workspaces (separam ambientes, não ciclo de vida); estrutura antiga `terraform/bootstrap` e `environments/dev` (removida).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/backend.tf:43`, `terraform/cluster/backend.tf:47`, `terraform/k8s/backend.tf:55` (chaves `phase4/prod/<camada>.tfstate`); `terraform/cluster/variables.tf:46`; `terraform/k8s/variables.tf:42,48`.
- Relação: mantida pela D-014. TFB-01/XCL-03 (estado novo vazio e recursos criados à mão: o apply da base colide sem import) e TFK-05.
- Ressalvas: na Fase 3, as chaves eram `prod/<camada>.tfstate`; "prod" é prefixo de chave, não workspace. Custos da Fase 3: base cerca de US$ 0 com NAT desligado; cluster cerca de US$ 0,37/h, depois alinhado em 0,385/h. Em 2026-09-15, "base permanente" virou "preservável": a base foi destruída em 2026-09-11 e em 2026-09-15.

Fonte F3: `DECISOES.md:138-154`; `LOG_DE_TRABALHO.md:257`, `:343-353`; `_ARQUIVO_MORTO/ARQUITETURA.md:46-59`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:39-49`, `:522-549`.

### F3-D-018 — Sem ESO: o Terraform cria os Secrets do Kubernetes (revisar, 2026-09-01; nota de 2026-09-15)

Contexto: o ESO era sugestão das aulas (S-02), não requisito. O prazo na época era de 14 dias.

Decisão: cortar o ESO. A camada `terraform/k8s` (`secrets.tf`) cria os 5 Secrets dos serviços e o do `postgres-targeting`.
- As senhas dos 2 RDS nascem na camada cluster e também vão ao Secrets Manager.
- A senha do targeting, `MASTER_KEY` e `SERVICE_API_KEY` nascem na k8s e ficam só no Secret e no estado.
- O contrato de nomes e chaves fica em `gitops/SECRETS-CONTRATO.md`.

Motivo: o ESO seria peça nova em runtime no caminho crítico da gravação. Falha no chart, na role IRSA ou no ClusterSecretStore derrubaria os 5 serviços.

Alternativas: manter o ESO; Secret versionado no Git (o que o enunciado critica); preencher o Secret à mão após o apply.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/k8s/secrets.tf:92-256`; `terraform/modules/rds/main.tf:178`; `gitops/SECRETS-CONTRATO.md:10`; comentários com ESO em `gitops/base/auth-service/deployment.yaml:68`, `evaluation-service/deployment.yaml:61` e `flag-service/deployment.yaml:51`.
- Relação: XCL-09 e CMP-02 (o contrato não cobre New Relic, PagerDuty, Slack e token de dispatch); TFK-04 (tokens externos em texto no estado; sugere variáveis `ephemeral` e `data_wo`); TFC-09 (senhas RDS repetidas no estado); GIT-08.
- Ressalvas: nenhuma senha vai para o Git. Perdas aceitas: o Secret nasce fora do GitOps, e a rotação não sincroniza sozinha. Os pods não leem o Secrets Manager; não apresentar assim. Os 2 segredos no Secrets Manager da estimativa da Fase 3 são as credenciais dos 2 RDS.

Fonte F3: `DECISOES.md:118-136`; `INSTRUCOES_ASSISTENTES.md:29`, `:32`; `PENDENCIAS_E_PROXIMOS_PASSOS.md:29`; `LOG_DE_TRABALHO.md:249`, `:258`.

### F3-D-020 — Trabalho humano só na `dev`; promoção por PR (vigente, 2026-09-09)

Contexto: uma auditoria achou commits direto na `main` e a `dev` 19 commits atrás (F3-D-019).

Decisão: todo trabalho humano ou de agente parte da `dev`. A `main` recebe só PR `dev` -> `main` e merge. Branches auxiliares não vão direto para a `main`. Depois de cada merge, conferir e sincronizar a `dev` sem descartar trabalho. A regra não é, por si, ordem para publicar ou fazer merge.

Motivo: instrução do usuário. Dá uma origem única ao trabalho, revisão e rastreabilidade. Na `dev` o pipeline só verifica; quem publica imagem e tag é a `main`.

Alternativas: PRs de branches auxiliares direto para a `main` (usados nos PRs 4 e 5); push humano direto na `main`.

Na Fase 4:
- Vigência: vigente.
- Evidência: `CLAUDE.md:8`; `.github/workflows/auth-service.yml:35,58` (gatilhos em `main` e `dev`); `.github/workflows/_ci-go.yml:331,494` (publicação só na `main`).
- Relação: coerente com a D-014. CIC-07 (commits do bot divergem da `dev`; force-push ou `checkout dev -- gitops/` voltam as tags para placeholder) e XCL-01.
- Ressalvas: é disciplina de processo. A proteção de branch não estava disponível no plano do GitHub; não afirmar que é imposta. Em conflito de fast-forward, a Fase 3 usava `git pull --no-rebase origin main`.

Fonte F3: `DECISOES.md:80-94`; `INSTRUCOES_ASSISTENTES.md:53-64`; `LOG_DE_TRABALHO.md:256`, `:265`, `:276-288`.

### F3-D-021 — Robô do CI comita a tag na `main` (revisar, 2026-09-09)

Contexto: a F3-D-020 vale para trabalho humano. Faltava definir o commit automático de tag.

Decisão: o último job de `_ci-go.yml` e `_ci-python.yml` roda `kustomize edit set image` no overlay `prod` e `git push origin HEAD:main`. O commit leva `[skip ci]`, e há laço de 5 tentativas (fetch/reset/edit/commit/push). A `dev` é sincronizada com a `main` no início de cada sessão (`git merge --ff-only origin/main`).

Motivo: a `main` é o estado desejado que o ArgoCD observa. O commit de tag é resultado mecânico de um build que já passou por PR e portões de segurança. Um PR do robô criaria fila de aprovação e quebraria a demo de sincronização automática.

Alternativas: robô comitando na `dev` com PR automático para a `main` (passo manual no caminho crítico); branch `gitops-bot` observada pelo ArgoCD (duas fontes da verdade). Ambas descartadas.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.github/workflows/_ci-go.yml:572` (5 tentativas), `:583`, `:602` (`[skip ci]`), `:606` (`git push origin HEAD:main`); `.github/workflows/_ci-python.yml:602`, `:636`; `terraform/k8s/variables.tf:114-121` e `argocd.tf:301` (a Application observa a `main`). A `main` do 04 ainda não tem `gitops/` (TFK-03).
- Relação: CIC-07, CIC-03 (jobs de build herdam `contents: write` e `id-token: write`), TFK-03, GIT-03, TFB-05. `CLAUDE.md:8` suspende push, PR e `main` nesta etapa.
- Ressalvas: commits do robô não disparam CI, porque levam `[skip ci]` e `gitops/**` não está em filtro. Qualquer merge que dispare o robô na conta nova precisa de role do CI, Variables e autorização do usuário.

Fonte F3: `DECISOES.md:61-77`; `INSTRUCOES_ASSISTENTES.md:30`, `:53`, `:88`; `LOG_DE_TRABALHO.md:265`, `:267`, `:284`.

### F3-D-022 — Provedor OIDC do GitHub: criar ou reaproveitar (revisar, 2026-09-14; registro em 2026-09-15)

Contexto: a conta da Fase 3 já tinha o provedor `token.actions.githubusercontent.com`, criado por outro projeto. A AWS aceita um provedor por URL. O apply falharia com `EntityAlreadyExists`, e o plan não avisa porque compara só com o estado.

Decisão: variável `create_github_oidc_provider`, com padrão `true`. Com `false`, um data source só lê o provedor existente, e o Terraform nunca o destrói; a role do CI confia nele do mesmo jeito. Um bloco `moved` preserva estados antigos. Na conta da Fase 3 o valor era `false`. O plan da base tinha 35 recursos com `false` e 36 com `true`.

Motivo: não quebrar o outro projeto nem falhar no apply.

Alternativas: `terraform import` (o destroy apagaria recurso alheio); apagar e recriar (quebra o outro projeto); criar outro provedor (a AWS recusa URL duplicada).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/variables.tf:237-241` (padrão `true`); `terraform/terraform.tfvars.example:83` (`true`); `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:52` (o usuário criou provedor, policy e role à mão na conta nova, por relato) e `:15` (plano B2: "OIDC false").
- Relação: TFB-03 (o provedor já existe na conta nova, mas o exemplo pede criação; os thumbprints do código diferem dos reais), TFB-01 e XCL-03. A lição da Fase 3 volta a valer.
- Lições e ressalvas: plan limpo não garante apply limpo quando há recurso fora do estado. Com `false` e sem provedor, o plan falha no data source. Usar `tfvars` local por camada, para apply e destroy lerem o mesmo valor. Implementado no commit b78f6bd, PR #15 (merge a4184a2), do repositório da Fase 3.

Fonte F3: `DECISOES.md:45-59`; `INSTRUCOES_ASSISTENTES.md:67`, `:124`, `:145`; `PENDENCIAS_E_PROXIMOS_PASSOS.md:51`; `LOG_DE_TRABALHO.md:51`, `:83-93`.

### F3-D-023 — Ordem de subida e destruição, com planos salvos (revisar, 2026-09-15)

Contexto: a base destruída levou ECR e imagens. Colar um bloco com apply interativo fez a linha seguinte virar a resposta do "yes".

Decisão:
- Subida: base -> imagens publicadas no ECR -> cluster -> `aws eks update-kubeconfig` -> k8s em duas etapas.
- Destruição: k8s -> cluster -> base. O destroy da k8s não é opcional.
- Sempre `plan -out=<camada>.tfplan` e `apply <camada>.tfplan` (no destroy, `plan -destroy -out`). Nunca apply interativo.
- `tfvars` local por camada.

Motivo: aplicar a k8s antes das imagens deixa pods em `ImagePullBackOff`. Ao apagar o PVC, o driver EBS apaga o disco de 5 GB, que não pertence a nenhum estado.

Alternativas: k8s antes das imagens; destruir só o cluster e deixar a k8s (estado órfão e EBS sem dono); valores por `-var` em cada comando (fácil esquecer um no destroy).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/k8s/argocd.tf:247-249` (apply em duas etapas); `terraform/k8s/variables.tf:114-121` (a `main` precisa receber o PR antes); `terraform/cluster/backend.tf` (aviso de preservar o EBS CSI até remover os PVCs, citado na TFC-05); `docs/GUIA_DE_REPRODUCAO.md:46` (`plan -out`; guia marcado como histórico).
- Relação: TFK-03 e GIT-03 (antes da k8s: PR para a `main`, o CI publica as 5 imagens e comita as tags, troca de sentinelas); TFB-01 (imports antes do apply da base); TFC-05 (PVCs da observabilidade fora do Terraform); DOC-02 (falta roteiro vigente).
- Ressalvas: na Fase 3, as imagens foram republicadas com `gh run rerun` dos últimos runs de push na `main`; numa conta nova, isso exige commit na `main`. Os pipelines de imagem podem rodar em paralelo ao apply do cluster (15-30 min). Um rerun antes do fim do apply da base falha com "Could not assume role with OIDC".

Fonte F3: `DECISOES.md:29-43`; `LOG_DE_TRABALHO.md:50-54`, `:76-79`; `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md:219-244`, `:894-908`.

### F3-D-024 — Consolidação da documentação pública da Fase 3 (revisar, 2026-09-15)

Contexto: o projeto foi entregue e o ambiente destruído em 2026-09-15. O mesmo fato estava em até cinco lugares, `docs/OPERACAO.md` tinha 1.636 linhas, e havia links quebrados e rastro de assistente no relatório.

Decisão: três documentos públicos sem sobreposição. O README diz o quê e por quê, `docs/GUIA_DE_REPRODUCAO.md` diz como, e `docs/ARQUITETURA.md` é a referência técnica.
- Cada fato tem detalhe em um único lugar.
- Documentos públicos não citam IA nem códigos internos.
- O arquivo morto não é editado.
- Não editar `services/**` nem `.github/workflows/**`, porque um merge rodaria os jobs de imagem e de GitOps, que falhariam no OIDC sem a role.
- O SECURITY.md foi corrigido: `MASTER_KEY` e `SERVICE_API_KEY` são segredos estáticos de aplicação, e a trust do CI aceitava qualquer branch ou PR do repositório.

Motivo: reduzir duplicação e divergência.

Alternativas: editar `variables.tf` ou `tfvars.example` (violaria "nenhuma mudança de código"); `terraform init -backend-config` como caminho principal; apagar PNGs da auditoria; editar `services/` ou workflows; tirar o sufixo "-an" do bucket.

Na Fase 4:
- Vigência: revisar.
- Evidência: `docs/GUIA_DE_REPRODUCAO.md:1` (marcado como histórico da Fase 3); `README.md:232`. `README.md:5` cita Codex, e `README.md:43` cita D-009, D-012 e D-014. O `git status` mostra `services/**` alterados (OTel). `SECURITY.md:20-23` ainda diz que a trust aceita qualquer branch ou PR, mas `terraform/modules/iam-ci/main.tf:81,141-147` (árvore de trabalho, sem commit) exige `StringEquals` no subject da `main`.
- Relação: DOC-02 e DOC-07 (sem roteiro nem arquitetura vigentes); CMP-03; TFB-04; DOC-12. A D-015 da Fase 4 consolidou explicações no README.
- Ressalvas: a trava sobre `services/` e workflows era circunstancial (role destruída) e não vale na Fase 4. Vira ordem de execução: role do CI e Variables prontas na conta nova antes de levar essas mudanças à `main`. A regra "um fato, um lugar" continua útil.

Fonte F3: `DECISOES.md:3-27`; `INSTRUCOES_ASSISTENTES.md:19`, `:93`; `PENDENCIAS_E_PROXIMOS_PASSOS.md:29`, `:35-36`; `LOG_DE_TRABALHO.md:3-14`, `:40`, `:44`.

### F3-SN-01 — Região us-east-2 (Ohio) em tudo (vigente, 2026-08-27)

Contexto: houve a inferência de us-east-1, tirada de um exemplo errado no README de um serviço.

Decisão: toda a infraestrutura e o bucket de estado ficam em us-east-2, como na Fase 2. Exemplos herdados com us-east-1 estão errados; vale o Terraform.

Motivo: informação do usuário.

Alternativas: us-east-1 (descartada, era erro).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/terraform.tfvars.example:16`; `terraform/cluster/variables.tf:12`; `terraform/k8s/variables.tf:8`; `terraform/cluster/terraform.tfvars.example`.
- Relação: conta nova em us-east-2. TFB-07 (falta validar AZ x região).
- Ressalvas: na CLI, criar bucket em us-east-2 exige `LocationConstraint`. Um bucket não muda de região depois.

Fonte F3: `LOG_DE_TRABALHO.md:429-437`; `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md:33`, `:40-42`, `:107-111`.

### F3-SN-02 — Bucket de estado por bootstrap manual, versionado e protegido (vigente, 2026-08-27)

Contexto: o Terraform precisa do bucket para guardar o próprio estado, e o enunciado exige estado remoto em S3.

Decisão: criar o bucket uma vez, fora do Terraform, pelo console (caminho A), com procedimento documentado. Configuração:
- versionamento ligado;
- SSE-S3 (AES256) com Bucket Key;
- 4 bloqueios de acesso público;
- ACLs desabilitadas e Object Lock desligado;
- policy `DenyInsecureTransport`;
- versões não correntes apagadas após 30 dias.

É a única exceção à regra "se não está no código, não existe".

Motivo: o estado guarda senhas em texto puro. O versionamento recupera estado corrompido. HTTPS obrigatório evita um achado clássico de scanner.

Alternativas: caminho B pela CLI; Apêndice A (criar com Terraform em estado local e migrar com `terraform init -migrate-state`).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/backend.tf:4-6`, `:39-45` (backend parcial via `backend.hcl`); `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:128-130` (bucket da conta nova criado pelo usuário em 2026-10-30, com versionamento e policy só TLS por relato; não verificado).
- Relação: coerente com a D-014. DOC-13 (`backend.hcl.example` repete a key).
- Ressalvas: os destroys não apagam o bucket. Ele é esvaziado e excluído por último, à mão. Com versionamento, `aws s3 rb --force` não apaga as versões antigas.

Fonte F3: `LOG_DE_TRABALHO.md:417`, `:429-437`, `:443`; `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md:3-5`, `:113-176`, `:343-353`; `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md:197`, `:206`.

### F3-SN-03 — Nome do bucket com ID da conta e região (superada, 2026-08-27)

Contexto: o nome de bucket é único no mundo.

Decisão: o grupo usou o nome `togglemaster-tfstate-<CONTA_FASE3>-us-east-2-an`, em vez de sufixo aleatório.

Motivo: identificar conta e região.

Alternativas: sufixo aleatório de 6 caracteres.

Na Fase 4:
- Vigência: superada pela D-014 (backend parcial e `expected_aws_account_id`).
- Evidência: `terraform/backend.tf:39-45`; `terraform/cluster/terraform.tfvars.example` (`state_bucket = NOVO_BUCKET_ESTADO_FASE4`).
- Relação: DOC-12 e XCL-14 (ID da conta antiga em guia versionado; a varredura não bloqueia). Na Fase 3, o ID ficou visível no `backend.tf`, mitigado por repositório privado. Não copiar o nome nem o bloco backend do bootstrap antigo. O nome do bucket novo não foi conferido.

Fonte F3: `LOG_DE_TRABALHO.md:423`; `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md:34`, `:87-105`.

### F3-SN-04 — Lock nativo do S3 e Terraform >= 1.11 (vigente, 2026-08-27)

Contexto: era preciso impedir applies simultâneos.

Decisão: backend S3 com `use_lockfile = true` e `encrypt = true` nas três camadas. Terraform mínimo 1.11.0, sem tabela DynamoDB de lock. O CI usa Terraform 1.16.0.

Motivo: `use_lockfile` só existe a partir da 1.11.0, e a tabela DynamoDB de lock está depreciada. `encrypt` garante criptografia mesmo se o padrão do bucket mudar.

Alternativas: tabela DynamoDB de lock.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/backend.tf:19,44-45`; `terraform/cluster/backend.tf:16,48-49`; `terraform/k8s/backend.tf:16,56-57`; `.github/workflows/terraform-check.yml:65`.
- Relação: mantido pela D-014. TFK-04 usa o `>= 1.11` para viabilizar variáveis write-only.
- Ressalva: um apply travado exige `terraform force-unlock <ID>`, só com certeza de que ninguém está rodando.

Fonte F3: `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md:38`, `:300-322`, `:337-338`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:425`, `:436-438`.

### F3-SN-05 — NAT Gateway por variável, com padrões opostos (vigente, 2026-09-15)

Contexto: o NAT parado custa cerca de US$ 33/mês, mas sem ele o cluster não funciona.

Decisão: `enable_nat_gateway` tem padrão `true` no `variables.tf`, para não derrubar o cluster por esquecimento. No `terraform.tfvars.example` o valor é `false`, para não pagar recurso ocioso.

Motivo: equilibrar não quebrar o cluster e não pagar NAT parado.

Alternativas: padrão único.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/variables.tf:100-110`; `terraform/terraform.tfvars.example:41`.
- Relação: TFB-10 (custo do NAT subestimado: ignora o IPv4 público do EIP e o processamento por GB) e TFC-12 (a camada cluster não verifica se o NAT existe).
- Ressalvas: sem tfvars, o NAT sobe ligado e cobrando. Sem NAT, nós em subnet privada não baixam imagem, e todos os pods ficam em `ImagePullBackOff`. `-var` na linha de comando tem precedência.

Fonte F3: `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:553-555`, `:571-576`, `:606-612`.

### F3-SN-06 — Custo entre sessões: pausa ou destruir também a base (revisar, 2026-09-09 a 2026-09-15)

Contexto: o cluster completo custava cerca de US$ 0,37/h (depois 0,385/h), e o crédito era limitado.

Decisão:
- Opção A, entre sessões: destruir a k8s, conferir o EBS, destruir o cluster e preservar base e bucket. Depois, aplicar `enable_nat_gateway=false` na base; o plano deve remover só NAT, EIP e rota. Religar o NAT antes do cluster.
- Opção B, no encerramento: destruir também a base (ECR e role do CI somem).
- Em 2026-09-11 a base ficou; em 2026-09-15 foi destruída.

Motivo: derrubar ao fim da sessão foi tratado como requisito. A opção A preserva as imagens e acelera a próxima subida.

Alternativas: manter tudo ligado (cerca de US$ 0,385/h); exclusão completa a cada sessão.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/variables.tf:100-110` e `terraform/terraform.tfvars.example:41` (mecanismo do NAT). Nenhuma política escolhida em `00_COLAB_IA/DECISOES.md`.
- Relação: D-010 e D-012 (crédito incerto; desenvolver local primeiro). XCL-10; TFB-01/XCL-03: se ECR, role e OIDC criados à mão forem importados, o destroy da base os apagaria.
- Ressalvas: com a base destruída, merges na `main` que mexam em `services/` ou `_ci-*.yml` ficam vermelhos no job de imagem por falta da role. Os bancos são apagados no destroy do cluster, então seed e schemas são refeitos a cada sessão. Conflito interno da Fase 3: o runbook dizia que ECR/SQS/DynamoDB/IAM não cobram parados, e o guia de destruição dizia que a base pode manter custos de armazenamento.

Fonte F3: `LOG_DE_TRABALHO.md:157`, `:177`; `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:11-19`, `:179-201`, `:592-628`; `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md:210-212`; `_ARQUIVO_MORTO/GUIA_GRAVACAO.md:130-133`; `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md:189-192`, `:749-811`.

### F3-SN-07 — Exclusão completa com a Application removida antes (revisar, 2026-09-11)

Contexto: selfHeal e CreateNamespace do ArgoCD podem disputar com o namespace sendo destruído.

Decisão, nesta ordem:
1. Excluir a Application `togglemaster` com `kubectl`, depois de conferir finalizers (wait 5m).
2. Destruir `terraform/k8s` com EKS, NAT e CSI vivos.
3. Confirmar a remoção do PV/EBS.
4. Destruir `terraform/cluster` e depois `terraform/`.
5. Conferir sobras.
6. Só então esvaziar e excluir o bucket.

Um bloco por vez, sem `-auto-approve`, checando o exit code.

Motivo: evitar a corrida com o ArgoCD. O disco do targeting foi criado pelo CSI e depende do driver vivo para ser apagado. O bucket guarda estado e locks até o fim.

Alternativas: deixar o Terraform remover tudo (risco de corrida); pausa preservando a base (F3-SN-06).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/k8s/storageclass.tf:61` (reclaim Delete); `terraform/k8s/argocd.tf:325,332` (selfHeal e CreateNamespace ligados).
- Relação: TFC-05 (PVCs de Prometheus/Loki/Grafana em namespace fora do Terraform sobrevivem ao destroy da k8s), GIT-13, DOC-02.
- Ressalvas: o guia foi preparado e revisado em 2026-09-11, mas não executado naquele dia. Os comandos antigos usam chaves `prod/` e filtro `phase=3`; refazer para `phase4/prod` e `phase=4`. Com finalizer travado, manter ArgoCD/EKS e diagnosticar, sem forçar. Fazer exports e snapshots antes, se necessários.

Fonte F3: `LOG_DE_TRABALHO.md:157`, `:177`; `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md:3`, `:27-38`, `:77-206`, `:216-218`.

### F3-SN-08 — Plano ordenado por custo, cluster no fim (vigente, 2026-08-27)

Contexto: os workflows de CI dependem só do ECR e da role OIDC (camada base).

Decisão: ordenar o trabalho por custo, não por dependência técnica. O que não consome crédito vem primeiro. O cluster fica para o fim, em sessões de 3 horas, com ensaio 4 dias antes da gravação. A base é aplicada com `enable_nat_gateway = false`.

Motivo: itens de vídeo sem cluster podem ser gravados antes. Se o primeiro apply completo quebrar, há tempo para corrigir com o cluster desligado.

Alternativas: ordem por dependência técnica.

Na Fase 4:
- Vigência: vigente.
- Evidência: `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:11-22` (plano P-015: B1 sem AWS, B3 base antes do cluster, B5 destroy após a gravação); `terraform/terraform.tfvars.example:41`.
- Relação: sobrepõe D-010 e D-016. Calendário da Fase 4: meta interna 2026-11-12, trial do PagerDuty até cerca de 2026-11-11.
- Ressalva: o runbook da Fase 3 declarava 3 h por sessão, mas a soma das etapas dava cerca de 2 h.

Fonte F3: `LOG_DE_TRABALHO.md:357-365`, `:369`; `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:3-4`, `:677`.

### F3-SN-09 — Âncora de escopo: entregar o básico que funciona (revisar, 2026-08-27; reafirmada em 2026-09-09)

Contexto: o usuário avaliou que o assistente estava complicando o projeto, sem requisito que pedisse os extras.

Decisão: priorizar o básico que atende ao enunciado. O README tem três listas: obrigatório, extras com justificativa e o que ficou de fora. Antes de propor algo, conferir se é obrigatório (O-*) ou sugestão (S-*). Na Fase 3 ficaram de fora: múltiplos ambientes, Ingress, charts próprios, ESO, KEDA, DAST e plataformas de observabilidade.

Motivo: nenhum requisito expresso pedia os extras.

Alternativas: ampliar o escopo com extras.

Na Fase 4:
- Vigência: revisar.
- Evidência: `README.md:123-137` (Grafana, Prometheus, Loki, PagerDuty, Slack e self-healing planejados); `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:7-22`.
- Relação: a Fase 4 exige componentes novos em runtime, então a lista de exclusões da Fase 3 não vale. Continua a ideia de não inflar além do enunciado da Fase 4 (a D-002 separa obrigação, opção e sugestão).
- Ressalva: na Fase 3, o assistente gravou a preferência na memória do projeto por iniciativa própria. Na Fase 4, `CLAUDE.md:11` só permite memória global quando o usuário pedir.

Fonte F3: `LOG_DE_TRABALHO.md:314`, `:371-377`; `INSTRUCOES_ASSISTENTES.md:69`; `_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md:86`, `:105`, `:173-175`.

### F3-SN-10 — EKS em versão de suporte padrão: 1.34 em vez de 1.31 (revisar, 2026-09-09)

Contexto: a versão 1.31 saiu do suporte padrão em 2025-11-26.

Decisão: o padrão do EKS em `terraform/cluster/variables.tf` passou de 1.31 para 1.34.

Motivo: no suporte estendido, o control plane vai de US$ 0,10/h para US$ 0,60/h (6x), sem ganho.

Alternativas: manter 1.31 e corrigir o custo.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/cluster/variables.tf:76` (padrão 1.34); sem `upgrade_policy` no `aws_eks_cluster` (TFC-03: `terraform/modules/eks/main.tf:66-109`).
- Relação: TFC-03 (1.34 sem `upgrade_policy STANDARD`; comentários ainda citam 1.31) e TFK-02 (chart do ArgoCD fora da matriz testada da 1.34).
- Ressalvas: as fontes divergem sobre o fim do suporte padrão da 1.34: 2026-12-01 (LOG da Fase 3, por consulta à API em 2026-09), "dezembro de 2026" (relatório da Fase 3) e 2026-12-02 (P-015, não conferido na web). A entrega de 2026-11-17 fica dentro do prazo, com pouca folga. Na estimativa da Fase 3, o control plane custava US$ 73,00/mês.

Fonte F3: `LOG_DE_TRABALHO.md:224`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:427`, `:1589-1592`; `_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md:99-105`; `_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md:167-174`.

### F3-SN-11 — Sem chave estática da AWS: OIDC no CI e IRSA nos pods (vigente, 2026-08-27 a 2026-09-15)

Contexto: na Fase 2, as chaves estáticas num Secret eram "a dor citada no enunciado".

Decisão: os workflows assumem a role `togglemaster-github-actions` pelo provedor OIDC do GitHub, e a role só aceita token deste repositório. Os pods acessam SQS e DynamoDB por IRSA. Nenhum Secret ou GitHub Secret guarda `AWS_ACCESS_KEY_ID`.

Motivo: eliminar o risco de vazamento de credencial.

Alternativas: chaves estáticas nos Secrets do GitHub ou do Kubernetes (guia antigo, considerado o ponto mais grave).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/modules/iam-ci/main.tf:81` e `:128-147` (trust com `StringEquals` no subject imutável da `main`, só na árvore de trabalho; o HEAD ainda tem `StringLike` com curinga em `:136-144`); `terraform/cluster/main.tf:126-133` (IRSA); `gitops/base/evaluation-service/deployment.yaml:68`.
- Relação: TFB-04 (correção F-023 só na árvore de trabalho), CMP-03, TFB-05 (role própria do self-healing), CIC-03, TFC-10.
- Ressalvas: a regra vale para credenciais AWS. New Relic, PagerDuty, Slack e token de dispatch são chaves de terceiros e precisam de caminho próprio (F3-D-018). Ao destruir a base, a role e o OIDC somem, e o CI de publicação falha até serem recriados.

Fonte F3: `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:32-37`, `:1399-1402`; `_ARQUIVO_MORTO/ARQUITETURA.md:96-99`; `_ARQUIVO_MORTO/GUIA_EXECUCAO.md:8-13`, `:32-34`.

### F3-SN-12 — Imagem por nome lógico e URL da fila fora do Secret (vigente, 2026-08-27)

Contexto: o CI precisa trocar a tag sem editar YAML com `sed`.

Decisão: os Deployments citam só o nome lógico da imagem. Registro e tag entram pelo bloco `images:` do overlay. `AWS_SQS_URL` sai do Secret e vai para ConfigMap. O analytics fica sem segredo.

Motivo: `kustomize edit set image` altera um só campo. URL de fila nunca foi segredo.

Alternativas: `sed` em YAML; manter a URL no Secret.

Na Fase 4:
- Vigência: vigente.
- Evidência: `gitops/base/*/deployment.yaml` (image: auth :52, evaluation :47, flag :39, targeting :41, analytics :44); `gitops/overlays/prod/kustomization.yaml:65-80`; `gitops/overlays/prod/patches/endpoints.yaml:39`.
- Relação: GIT-03 (sentinelas a trocar antes do primeiro sync), GIT-06 (ConfigMap via `envFrom` sem hash: mudar `OTEL_*` não reinicia pods), GIT-02 (`OTEL_*` ausentes). As variáveis `OTEL_*` devem seguir o mesmo padrão de ConfigMap, sem segredo.

Fonte F3: `LOG_DE_TRABALHO.md:383`, `:411`.

### F3-SN-13 — ArgoCD por chart oficial fixo, com prune e selfHeal (revisar, 2026-09-09)

Contexto: o enunciado permite instalar por Helm ou Terraform.

Decisão: o ArgoCD é instalado em `terraform/k8s/argocd.tf` pelo provider helm, com o chart oficial 7.7.11 fixo. A Application aponta para `gitops/overlays/prod` na `main`, com sync automático, prune e selfHeal, sem finalizer.

Motivo: instalar por Kustomize exigiria remendar o `install.yaml` (desligar Dex, ajustar réplicas). A versão fixa dá reprodutibilidade.

Alternativas: Kustomize sobre o `install.yaml` oficial; `kubectl apply` de manifesto remoto (guia antigo).

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/k8s/variables.tf:86-95` (7.7.11); `terraform/k8s/argocd.tf:104`, `:297-301`, `:320` (prune), `:325` (selfHeal), `:332` (CreateNamespace).
- Relação: TFK-02 (o chart 7.7.11 instalaria o Argo CD v2.13.2, fora de suporte e com a CVE-2025-55190 crítica; correspondência não conferida localmente), GIT-04 e TFK-06 (selfHeal disputa `spec.replicas` com os HPAs), TFK-09.
- Ressalva: o selfHeal desfaz mudanças manuais. Uma falha de demo provocada por manifesto pode ser revertida antes de gerar alerta.

Fonte F3: `_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md:8`, `:199-202`, `:310-320`; `_ARQUIVO_MORTO/GUIA_EXECUCAO.md:7-8`.

### F3-SN-14 — Bootstrap do ArgoCD em duas etapas (vigente, 2026-09-09)

Contexto: o provider kubernetes valida o tipo Application no plan, antes de o Helm instalar o CRD.

Decisão: em cluster novo, rodar primeiro `terraform -chdir=terraform/k8s apply -target=helm_release.argocd` e depois o apply completo.

Motivo: sem o `-target`, o apply falha com `no matches for kind "Application"`, e `depends_on` não resolve.

Alternativas: apply único (falha em cluster novo); provider de terceiros (descartado); criar a Application fora do Terraform (tiraria do código o objeto que demonstra o GitOps).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/k8s/argocd.tf:247-249`.
- Relação: qualquer CRD novo da Fase 4 (ServiceMonitor, operadores de observabilidade) tem a mesma armadilha. TFK-05.
- Ressalva: em 2026-09-09, o checklist dizia "corrigido e documentado", a revalidação das 17:55 dizia que o erro persistia, e a correção fechou às 22:40 do mesmo dia.

Fonte F3: `LOG_DE_TRABALHO.md:248`, `:271`, `:318`; `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:231-258`; `_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md:42-48`.

### F3-SN-15 — Reconciliação do ArgoCD em 30 s (vigente, 2026-09-11)

Contexto: sem Ingress não há webhook do GitHub (F3-D-012).

Decisão: `timeout.reconciliation` passou de 180 s (padrão) para 30 s, com sync automático.

Motivo: na gravação, 3 minutos de tela parada ou um corte enfraquecem a prova de sincronização automática.

Alternativas: padrão de 180 s; clicar em Refresh (parece provocado); webhook (exige exposição).

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/k8s/argocd.tf:171` (comentário) e `:191` (`"timeout.reconciliation" = "30s"`).
- Relação: afeta o tempo de recuperação nas demos de GitOps e self-healing.
- Ressalvas: gera mais consultas ao Git. Com repositório privado, o ArgoCD precisa de credencial (F3-SN-16). A primeira reconciliação leva de 1 a 2 min.

Fonte F3: `_ARQUIVO_MORTO/GUIA_GRAVACAO.md:460-470`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:903-905`, `:1198-1201`, `:1389-1391`.

### F3-SN-16 — Credencial do repositório para o ArgoCD só com token (revisar, 2026-09-09 a 2026-09-15)

Contexto: um repositório público clona sem credencial. Num repositório privado sem credencial, a Application fica Unknown com "authentication required".

Decisão: `count = var.github_token != "" ? 1 : 0`. Para repositório privado, usar token fine-grained (Contents read-only, só este repositório, dono = organização) via `TF_VAR_github_token` em variável de ambiente, nunca em arquivo.

Motivo: não pedir credencial desnecessária e não gravar o token em arquivo.

Alternativas: token clássico com escopo `repo` (permissão larga); `terraform.tfvars` (grava o valor); repositório público sem token.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/k8s/argocd.tf:47-54`, `:80`; `terraform/k8s/variables.tf:125-135` (padrão `""`); `00_COLAB_IA/DOSSIE_CONTEXTO.md:9` (repositório 04 privado).
- Relação: TFK-11 (repositório privado, mas token opcional e vazio; sugere torná-lo obrigatório ou usar deploy key) e TFK-04 (o token fica em texto no estado).
- Ressalvas: testar o token com `git ls-remote` antes da sessão paga. Um token fine-grained de organização pode ficar "pending approval". Fazer o token expirar logo após 2026-11-17.

Fonte F3: `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:65-164`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:925-997`.

### F3-SN-17 — Senha inicial do ArgoCD fora dos outputs (vigente, 2026-09-15)

Contexto: um output fica gravado em texto no arquivo de estado.

Decisão: ler a senha do Secret `argocd-initial-admin-secret` por `kubectl` e base64. Não expor como output do Terraform.

Motivo: não gravar segredo no estado.

Alternativas: output sensível do Terraform.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/k8s/outputs.tf:26-36` (o output só traz o comando de leitura).
- Relação: o mesmo princípio vale para credenciais de Grafana, New Relic, PagerDuty e Slack: nenhum segredo em output. TFK-09.

Fonte F3: `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:1177-1196`.

### F3-SN-18 — `SERVICE_API_KEY` provisória e `ignore_changes` (vigente, 2026-09-09)

Contexto: o banco nasce depois do Secret, então a chave real só existe depois do seed.

Decisão: o Terraform cria `evaluation-service-secret` com valor provisório. O seed troca pela chave real. O recurso declara `lifecycle { ignore_changes = [data] }`.

Motivo: sem `ignore_changes`, o Terraform restauraria a chave provisória.

Alternativas: o Terraform gerenciar o valor sempre; seed gravando fora do Terraform sem `ignore_changes`.

Na Fase 4:
- Vigência: vigente.
- Evidência: `terraform/k8s/secrets.tf:211-256` (`ignore_changes` em `:255-256`).
- Relação: padrão reutilizável para segredos preenchidos fora do Terraform. É passo manual, candidato a automação.
- Ressalvas: o seed é obrigatório a cada sessão. Sem a troca, `/evaluate` responde 502 e o pod loga 401. Mudanças posteriores no valor não são revertidas pelo Terraform.

Fonte F3: `LOG_DE_TRABALHO.md:249`, `:318`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:1270-1302`, `:1553`.

### F3-SN-19 — Schemas do RDS aplicados por pod `psql` descartável (vigente, 2026-09-09)

Contexto: o Terraform cria instâncias e bancos vazios, e o RDS fica em subnet privada.

Decisão: ler `DATABASE_URL` dos Secrets `auth-service-secret` e `flag-service-secret` para variáveis do shell. Depois, rodar `kubectl run ... --rm -i --restart=Never --image=postgres:16-alpine -- psql "$VAR" < services/<svc>/db/init.sql` e conferir com `\dt`.

Motivo: a senha não deve aparecer na tela da gravação.

Alternativas: digitar senhas e endereços (descartado por expor a senha).

Na Fase 4:
- Vigência: vigente.
- Evidência: existem `services/auth-service/db/init.sql`, `services/flag-service/db/init.sql` e `services/targeting-service/db/init.sql`; nenhum recurso Terraform cria tabelas.
- Relação: DOC-02 (sem roteiro vigente para a conta nova). O targeting carrega o schema sozinho na primeira subida.
- Ressalvas: exige Git Bash ou WSL (redirecionamento `<`). Os schemas são idempotentes (`CREATE TABLE IF NOT EXISTS`).

Fonte F3: `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:331-461`; `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:1005-1015`.

### F3-SN-20 — Trivy estrito com exceções nominais datadas (revisar, 2026-09-09; validada no pipeline em 2026-09-10)

Contexto: o enunciado da Fase 3 (p. 4) exige falha em vulnerabilidade crítica, sem prever exceção. `ignore-unfixed` escondia vulnerabilidades.

Decisão: `ignore-unfixed: false` nos 4 scans Trivy CRITICAL (2 em `_ci-go.yml`, 2 em `_ci-python.yml`). Exceções sem correção publicada ficam uma a uma no `.trivyignore`, com justificativa e data de revisão.

Motivo: a exceção vira linha revisável no diff do PR, em vez de flag silenciosa.

Alternativas: `ignore-unfixed: true`; desligar a regra; `continue-on-error`.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.github/workflows/_ci-go.yml:283,304,429` e `_ci-python.yml:337,460`; `.trivyignore:58` ("Revisar em: 2026-10-15"), `:63`, `:68`, `:73` (3 CVEs, sem `exp:`).
- Relação: CIC-08 (revisão vencida em 2026-10-15; sugere `exp:` na linha), CIC-10, CIC-14. Dependências OTel novas podem trazer CVEs.
- Medição de 2026-09-09 (Trivy 0.74, tag v1.0.0-122174a): 3 CRITICAL em perl-base do `python:3.12-slim`, sem correção; `alpine:3.20` (Go) com zero; scan fs dos 5 serviços com zero.
- Ressalvas: o rerun usa o `.trivyignore` do commit antigo, então exceção nova entra por merge. Os jobs de imagem só rodam em push na `main`.

Fonte F3: `LOG_DE_TRABALHO.md:195`, `:217`, `:247`, `:269`; `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md:910-943`; `_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md:34-40`.

### F3-SN-21 — Scans sem `continue-on-error` e correção de CVE em cascata (vigente, 2026-09-11, por relato)

Contexto: o Trivy acusou o CVE-2026-56854 (crítico), mas os pipelines passavam verdes porque os scans usavam `continue-on-error`.

Decisão: atualizar `golang.org/x/crypto` de v0.20.0 para v0.55.0. Em cascata: Go 1.25 nos Dockerfiles e no SAST, golangci-lint da linha 1.x para a 2.x e três tratamentos de erro corrigidos. Os scans deixaram de usar `continue-on-error`.

Motivo: fazer o pipeline bloquear de verdade.

Alternativas: não registradas na fonte.

Na Fase 4:
- Vigência: vigente.
- Evidência: nenhum `continue-on-error` em `.github/workflows/`; `services/auth-service/go.mod:3` e `services/evaluation-service/go.mod:3` (go 1.25.0); `services/*/Dockerfile:10`; `.github/workflows/_ci-go.yml:161`, `:217`.
- Relação: a D-016 fixou dependências OTel compatíveis com Go 1.25 e Python 3.12. CIC-04 (actions de terceiros por tag móvel).

Fonte F3: `_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md:176-190`; `_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md:111-113`.

### F3-SN-22 — Lint e SAST: corrigir o achado real (revisar, 2026-09-09)

Contexto: as notas iniciais do pylint (4.84 a 5.66) estavam abaixo do corte.

Decisão:
- errcheck: corrigido no código.
- bandit B608 e B104: marcados como falso positivo com `# nosec` pontual e justificativa.
- pylint: achados reais corrigidos; regras de estilo desligadas no `.pylintrc` com justificativa por regra; nenhuma regra da família E tocada; corte `--fail-under=7.0` mantido.
- gosec e bandit falham só em severidade alta.

Motivo: achado real deve ser corrigido, não afrouxado.

Alternativas: baixar o corte do pylint; afrouxar o SAST.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.pylintrc:37`; `.github/workflows/_ci-go.yml:241` (`gosec -severity high -confidence medium`); `.github/workflows/_ci-python.yml:180`.
- Relação: CIC-02 (o pylint roda sem as dependências e deve reprovar o código OTel), CIC-11, CIC-17. O código OTel passa pelos mesmos cortes.
- Notas finais em 2026-09-09: flag 8.26, targeting 8.08, analytics 7.59.

Fonte F3: `_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md:179-182`, `:335-352`.

### F3-SN-23 — Gate de imagem por `needs`; CI sem `kubectl apply` (revisar, 2026-09-11, por relato)

Contexto: o enunciado pede para "falhar e não prosseguir" e critica deploy manual e deriva do cluster.

Decisão: o job de imagem declara `needs: [build, lint, sast, sca]`. Se algum falhar, a imagem não é construída. O último job grava a tag no overlay e comita. Nenhum workflow faz `kubectl apply`; quem aplica é o ArgoCD.

Motivo: leitura literal do enunciado.

Alternativas: não registradas.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.github/workflows/_ci-go.yml:326` (`needs`) e `:481` ("O CI NAO faz kubectl apply"); `.github/workflows/_ci-python.yml:359`, `:511`.
- Relação: a D-009 escolheu self-healing via GitHub Actions com `repository_dispatch`, e `README.md:132-137` prevê ação corretiva (reinício). CIC-01, XCL-08, TFB-05, TFC-02, GIT-07 (workflow, role, access entry e RBAC para `kubectl rollout restart`).
- Ressalva: o gate continua. A regra "CI nunca toca o cluster" precisa de exceção explícita e restrita para o self-healing. `rollout restart` não altera o manifesto, então o selfHeal do ArgoCD não o reverte.

Fonte F3: `_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md:107-112`, `:129-146`; `_ARQUIVO_MORTO/GUIA_GRAVACAO.md:330-338`, `:702-717`.

### F3-SN-24 — Imagem e tag GitOps só em push na `main` (revisar, 2026-09-15)

Contexto: era preciso controlar o que chega à produção.

Decisão: os jobs "Imagem Docker e push no ECR" e "Atualizar tag no GitOps" só rodam com `github.event_name == 'push'` e `github.ref == 'refs/heads/main'`. `workflow_dispatch` roda os testes e não publica.

Motivo: [INCERTO] não declarado na fonte; implícito o controle de promoção para produção.

Alternativas: `workflow_dispatch` publicando.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.github/workflows/_ci-go.yml:331`, `:494`; `.github/workflows/_ci-python.yml:364`, `:524`; `terraform/modules/iam-ci/main.tf:81` (trust só da `main`, na árvore de trabalho).
- Relação: CIC-13 (não há como republicar sem commit; sugere aceitar `workflow_dispatch` na `main`, compatível com a trust). Bootstrap das 5 imagens na conta nova (GIT-03).
- Ressalvas: republicar exige re-run de um run de push na `main` (até 30 dias) ou commit novo. Não editar tags à mão no fluxo normal.

Fonte F3: `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:637-640`, `:842-843`, `:879-898`, `:1539`.

### F3-SN-25 — CI de Terraform só com `fmt` e `validate` (revisar, 2026-09-09)

Contexto: um plan no CI exigiria credencial AWS e acesso ao estado remoto.

Decisão: `terraform-check.yml` roda `fmt` e `validate` nas três camadas, com `-backend=false`, em PR e push. Não roda plan.

Motivo: o ganho não compensava expor a conta. O plan era feito à mão no início de cada sessão.

Alternativas: plan automatizado com credencial no CI.

Na Fase 4:
- Vigência: revisar.
- Evidência: `.github/workflows/terraform-check.yml:11-23`, `:37-38`, `:84-85`.
- Relação: o self-healing dará ao CI acesso à AWS e ao cluster por OIDC (TFB-05, XCL-08). CIC-06 (sem scan de IaC), CIC-09 e GIT-14 (GitOps não renderizado nem validado no CI).
- Ressalva: o checklist antigo dizia que o plan era automatizado; isso foi corrigido na Fase 3.

Fonte F3: `_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md:117`; `_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md:43`, `:71`.

### F3-SN-26 — SQS desligado no Compose padrão; Moto no perfil de integração (vigente, 2026-09-15)

Contexto: testar localmente não deve exigir conta AWS.

Decisão: no Compose padrão, `AWS_SQS_URL` fica vazio em evaluation e analytics, e o worker do analytics não inicia. `docker-compose.integration.yaml` acrescenta o Moto (SQS e DynamoDB) e um inicializador de fila e tabela.

Motivo: ninguém precisa de conta ou credencial AWS para testar flags, regras, avaliação e cache.

Alternativas: exigir AWS real localmente.

Na Fase 4:
- Vigência: vigente.
- Evidência: `docker-compose.yaml:160`, `:195`; `docker-compose.integration.yaml:4` (Moto 5.2.2 por digest), `:32`, `:43`.
- Relação: base de D-010 e D-016 (19 spans em 5 serviços, com SQS e DynamoDB). CIC-15 (o Compose Integration não roda a prova OTel).
- Ressalva: o caminho evaluation -> SQS -> analytics -> DynamoDB só é exercitado no perfil integrado ou na AWS.

Fonte F3: `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md:329-343`, `:351-354`.

### F3-SN-27 — Demo só com regras PERCENTAGE de 100 ou 0 (vigente, 2026-09-09)

Contexto: o evaluation-service só implementa PERCENTAGE. Uma regra com `user_ids` seria aceita pelo targeting e ignorada na avaliação.

Decisão: a flag "novo-painel" usa `{type: PERCENTAGE, value: 100}` (sempre true). Outra flag usa `value 0` (sempre false) para o caso oposto.

Motivo: 100 e 0 são determinísticos.

Alternativas: trocar `user_id` na mesma flag (não funciona com 100%).

Na Fase 4:
- Vigência: vigente.
- Evidência: `services/evaluation-service/evaluator.go:262-264`.
- Relação: útil para tráfego controlado no cenário de alerta. Relaciona-se ao F-017 (targeting indisponível pode virar HTTP 200/`result=true`; `00_COLAB_IA/DOSSIE_CONTEXTO.md:117`).
- Ressalva: mudar a regra e reavaliar o mesmo par flag/usuário pode devolver o valor do cache Redis (TTL).

Fonte F3: `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:520-557`.

### F3-SN-28 — Usuário IAM com MFA para o bootstrap; root sem chave (revisar, 2026-08-27)

Contexto: a AWS desaconselha chaves do root.

Decisão: conta pessoal, com MFA no root, usado só em emergência e sem chaves. Cada integrante tem usuário IAM próprio (AdministratorAccess e MFA) para bootstrap e uso diário. As roles criadas pelo Terraform seguem menor privilégio real. A access key é pessoal, fica em gerenciador de senhas e nunca vai ao repositório nem é compartilhada.

Motivo: AdministratorAccess foi aceito para o bootstrap de uma conta de estudo.

Alternativas: não registradas.

Na Fase 4:
- Vigência: revisar.
- Evidência: `terraform/providers.tf:14` e `terraform/cluster/providers.tf:10` (`allowed_account_ids`). Identidades humanas não estão no código.
- Relação: TFC-02 (só o criador do cluster recebe acesso; não há access entry explícito para admin nem para o self-healing).
- Ressalvas: usuários IAM manuais não são removidos pelos destroys; desativá-los é passo manual. A identidade usada na conta nova não foi verificada.

Fonte F3: `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md:44-81`, `:293-298`; `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md:208`; `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md:227-229`.

### F3-SN-29 — Estimativa de custo com fonte única (revisar, 2026-09-11)

Contexto: dois lugares com o mesmo número divergem. Já havia 0,37 e 0,385 em arquivos diferentes.

Decisão: a estimativa fica num só lugar (seção 8 do relatório), com números oficiais do AWS Pricing Calculator, sem arquivo próprio.

Motivo: evitar divergência.

Alternativas: arquivo separado de estimativa (descartado).

Na Fase 4:
- Vigência: revisar.
- Evidência: o README da Fase 4 não tem seção de custo; `docs/GUIA_DE_REPRODUCAO.md:13` aponta para `README#8-custo`, que não existe mais.
- Relação: XCL-10 (custo sem premissa única de nós), TFB-10, TFC-06.
- Números da Fase 3 (sem observabilidade; não valem para a Fase 4): US$ 281,03/mês (soma de 7 itens), US$ 3.372,36/ano, US$ 0,385/h (281,03/730) e cerca de US$ 1,15 por sessão de 3 h.

Fonte F3: `LOG_DE_TRABALHO.md:130`, `:135`, `:200`.

### F3-SN-30 — Gerador do PDF do relatório (revisar, 2026-09-11 a 2026-09-15)

Contexto: havia dois geradores, e as fontes divergem sobre qual era o canônico.

Decisão (sequência):
- Em 2026-09-11, `scripts/gerar-relatorio-pdf.py` (Markdown para PDF, com capa e captura de custos) foi declarado canônico.
- Em 2026-09-14, o docstring do `build-report-fase3.py` (ReportLab) se declara canônico, com o texto dentro do script.
- Em 2026-09-15, a F3-D-024 arquivou o `build-report` e o `capturar-estimativa-aws.cjs`.

Motivo: o gerador ReportLab não rodava na máquina (reportlab ausente), escrevia em `output/pdf/` (ignorado) e divergia do formato da Fase 2. Em troca, acrescentava desafios, decisões e captura de custos.

Alternativas: um ou outro gerador. A identidade visual ficou a cargo do usuário.

Na Fase 4:
- Vigência: revisar.
- Evidência: `git ls-files` só mostra `docs/00_COLAB_IA/_ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py` e `build-report-fase3_2026-09-14.py`; nenhum gerador ativo em `scripts/`.
- Relação: DOC-01 (não existe relatório da Fase 4; `docs/RELATORIO_DE_ENTREGA.md` é o da Fase 3). Lição: escolher uma única fonte de texto para o PDF.
- Ressalvas: resultado de 2026-09-11: 9 páginas, 242 KB. O script de captura aceitava o banner de cookies quando não achava a opção de recusa; não reutilizar sem corrigir.

Fonte F3: `LOG_DE_TRABALHO.md:23`, `:196`, `:201`; `_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py:1-10`, `:32-34`; `_ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py:22-28`; `_ARQUIVO_MORTO/capturar-estimativa-aws_2026-09-11.cjs:35-41`.

### F3-SN-31 — Material de aula da FIAP mantido no repositório (revisar, 2026-09-13)

Contexto: o material foi retirado do versionamento em 2026-09-11 e depois devolvido.

Decisão: os 33 arquivos de aula (18 MB, 87% do peso do repositório) voltaram ao controle de versão, e o bloco saiu do `.gitignore`. Em 2026-09-15, foram movidos para `docs/aulas-fiap/`.

Motivo: decisão do usuário. A preocupação de publicar material da instituição em repositório aberto ficou como ressalva.

Alternativas: retirar do versionamento (feito em 2026-09-11 e revertido).

Na Fase 4:
- Vigência: revisar.
- Evidência: no `git status`, 34 arquivos da Fase 3 em `docs/` aparecem apagados, sem commit; `README.md:232`; `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:11` (B0).
- Relação: conflita com a F3-D-004. DOC-11. A decisão do usuário está pendente; os originais seguem no Git e no `tech-challenge-03`.

Fonte F3: `LOG_DE_TRABALHO.md:20`, `:138-142`; `ORGANIZACAO_DE_PASTAS.md:21-24`, `:38-39`.

### F3-SN-32 — Vídeo no YouTube como Não listado (revisar, 2026-09-11 e 2026-09-15)

Contexto: o avaliador não abre vídeo privado.

Decisão: publicar como Não listado e testar o link numa aba anônima. O link entra no README e no relatório.

Motivo: garantir acesso do avaliador.

Alternativas: vídeo privado.

Na Fase 4:
- Vigência: revisar.
- Evidência: sem artefato no código. Vídeo da Fase 4 com até 25 min (`00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:20`).
- Relação: etapa B5/B6 do plano P-015. Confirmar a forma de entrega no enunciado da Fase 4. O limite da Fase 3 era 20 min.

Fonte F3: `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md:744-745`; `_ARQUIVO_MORTO/GUIA_GRAVACAO.md:929-931`, `:978`.

### Conflitos com a Fase 4

- ⚠️ CONFLITO — Provedor OIDC na conta nova. O usuário relatou ter criado o provedor à mão na conta nova, mas o padrão e o exemplo ainda pedem criação. É o mesmo cenário da F3-D-022.
  - Evidência: `terraform/variables.tf:237-241` (padrão `true`); `terraform/terraform.tfvars.example:83` (`true`); `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:52` e `:15` (plano "OIDC false"); TFB-03, TFB-01, XCL-03.
  - Sugestão: ADR da Fase 4 sobre quem é dono do provedor. Caminho simples: `false` no `terraform.tfvars` local, sem import. Se importar com `true`, alinhar ou remover `thumbprint_list`. Ajustar o exemplo e o README.

- ⚠️ CONFLITO — Premissas de conta em F3-D-015 e F3-D-016. As justificativas vêm do plano gratuito e do crédito de US$ 70,33 da conta da Fase 3. A D-012 registra que a conta nova não ganha Free plan nem crédito. A aprovação do professor valeu para a Fase 3, mas os comentários do Terraform tratam tudo isso como fato atual.
  - Evidência: `00_COLAB_IA/DECISOES.md:99`; `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:62`; `terraform/cluster/main.tf:59`; `terraform/cluster/variables.tf:127-139`; TFC-06.
  - Sugestão: confirmar o plano de cobrança da conta nova. Decidir em ADR a topologia de bancos e o tipo de nó, por custo e pelo enunciado da Fase 4. Reescrever os comentários como "conta da Fase 3", com prefixo F3-.

- ⚠️ CONFLITO — Dimensionamento do cluster. O código mantém 2 nós de 4 GiB, a D-015 cita três workers como proposta, e o sizing da Fase 3 não incluía Prometheus, Loki, Grafana e Collector.
  - Evidência: `terraform/cluster/variables.tf:86,102`; `00_COLAB_IA/DECISOES.md:133`; TFC-01, XCL-10.
  - Sugestão: somar requests/limits dos charts e escolher entre 3 x c7i-flex.large ou um tipo com 8 GiB. Fixar a escolha no tfvars local e alinhar README, PENDENCIAS e a estimativa de custo.

- ⚠️ CONFLITO — Sem Ingress. A F3-D-012 foi validada contra o enunciado da Fase 3. A Fase 4 não tem ADR própria nem nova varredura. Os comentários "D-012" nos manifests apontam para a Fase 3, mas a D-012 da Fase 4 é "continuar na AWS".
  - Evidência: `gitops/base/kustomization.yaml:73`; `gitops/base/auth-service/service.yaml:21`; `00_COLAB_IA/DECISOES.md:95`; `README.md:129-132`; XCL-04.
  - Sugestão: repetir a varredura no enunciado da Fase 4 e registrar ADR citando a F3-D-012. Se entrar LB ou Ingress, incluí-lo na ordem de destroy.

- ⚠️ CONFLITO — Colisão de IDs. Comentários de código e scripts usam D-0xx/F-0xx da Fase 3, que existem na Fase 4 com outro significado. A Fase 3 também rotulava a conta pessoal como "D-016", quando no registro oficial ela é a D-003.
  - Evidência: `terraform/cluster/main.tf:59` ("F-023, D-016"); `scripts/security-check.sh:70`; `gitops/base/kustomization.yaml:73`; `00_COLAB_IA/DECISOES.md:127,139`; XCL-04, TFC-06, TFK-08.
  - Sugestão: usar o prefixo F3- em toda referência herdada (DECISOES, PENDENCIAS e comentários), com uma nota no README sobre IDs sem prefixo.

- ⚠️ CONFLITO — Robô do CI e fluxo para a `main`. F3-D-020 e F3-D-021 pressupõem push e merge na `main`, mas `CLAUDE.md` proíbe push, PR e alteração da `main` nesta etapa. A `main` do 04 não tem `gitops/`, e a Application observa a `main`. O ritual `git merge --ff-only origin/main` da Fase 3 não se aplica sem adaptação.
  - Evidência: `CLAUDE.md:8`; `.github/workflows/_ci-go.yml:606`; `.github/workflows/_ci-python.yml:636`; `terraform/k8s/variables.tf:114-121`; `terraform/k8s/argocd.tf:301`; TFK-03, GIT-03, CIC-07.
  - Sugestão: ADR da Fase 4 mantendo o push do robô na `main`, com a ordem PR -> CI publica as 5 imagens e as tags -> troca de sentinelas -> apply da k8s. Proibir force-push na `main` e `checkout dev -- gitops/`. Executar só com autorização do usuário.

- ⚠️ CONFLITO — CI sem acesso ao cluster x self-healing. A Fase 3 definiu que o CI não faz `kubectl apply` e não tem credencial AWS para plan. O self-healing da Fase 4 por GitHub Actions precisa assumir uma role AWS e rodar `kubectl rollout restart`.
  - Evidência: `.github/workflows/_ci-go.yml:481`; `.github/workflows/terraform-check.yml:11-23`; `00_COLAB_IA/DECISOES.md:73`; `README.md:132-137`; CIC-01, XCL-08, TFB-05, TFC-02, GIT-07.
  - Sugestão: registrar uma exceção explícita e restrita: role própria com trust de environment, `eks:DescribeCluster`, access entry e RBAC só no namespace `togglemaster`, com allowlist de Deployments. Explicar no vídeo que `rollout restart` não muda o manifesto.

- ⚠️ CONFLITO — Trava de edição da F3-D-024. A regra manda não editar `services/**` nem workflows, mas a Fase 4 já alterou os serviços (OTel) e precisa de um workflow de self-healing.
  - Evidência: `git status` (`services/*/app.py`, `main.go` e `handlers.go` modificados); `00_COLAB_IA/DECISOES.md:139-149`.
  - Sugestão: tratar a trava como superada e manter só a ordem de execução: role do CI e Variables prontas na conta nova antes de levar essas mudanças à `main`.

- ⚠️ CONFLITO — IA e códigos internos em documentos públicos. A F3-D-024 proíbe essas menções, mas o README da Fase 4 cita Codex e D-009/D-012/D-014. O `CLAUDE.md` está versionado na raiz, embora a D-001 dissesse para não criá-lo ali.
  - Evidência: `README.md:5`, `:43`; `git ls-files CLAUDE.md`; `00_COLAB_IA/DECISOES.md:11`.
  - Sugestão: decidir com o usuário se a regra vale para o README e o relatório PDF da Fase 4 e como tratar o `CLAUDE.md` versionado.

- ⚠️ CONFLITO — SECURITY.md desatualizado. O texto da Fase 3 diz que a trust aceita qualquer branch ou PR. Na árvore de trabalho, a trust passou a `StringEquals` no subject imutável da `main`, mas o HEAD ainda tem `StringLike` com curinga.
  - Evidência: `SECURITY.md:20-23`; `terraform/modules/iam-ci/main.tf:81,141-147` (árvore de trabalho); `git show HEAD:terraform/modules/iam-ci/main.tf:136-144`; CMP-03, TFB-04.
  - Sugestão: comitar a correção F-023 da Fase 4, com autorização, e reescrever o parágrafo do SECURITY.md.

- ⚠️ CONFLITO — Credenciais de terceiros. O padrão da F3-D-018 e a frase "nenhuma chave estática no projeto" não cobrem as credenciais de terceiros da Fase 4, e os manifests ainda citam ESO e Secrets Manager.
  - Evidência: `gitops/SECRETS-CONTRATO.md` (sem New Relic, PagerDuty, Slack e token de dispatch); `terraform/k8s/argocd.tf:80`; `gitops/base/auth-service/deployment.yaml:68`; `evaluation-service/deployment.yaml:61`; `flag-service/deployment.yaml:51`; XCL-09, TFK-04, CMP-02, GIT-08.
  - Sugestão: estender o contrato com uma linha por credencial (Secret, namespace, origem, estado, escopo, revogação). Avaliar variáveis `ephemeral`/`data_wo`. Limitar a frase "sem chave estática" às credenciais AWS e corrigir os comentários.

- ⚠️ CONFLITO — Tag `phase`. O código já usa `phase = "4"`, mas os volumes criados pelo CSI não recebem tags, e os guias herdados filtram por `phase=3`.
  - Evidência: `terraform/variables.tf:58`; `terraform/k8s/storageclass.tf` (sem `tagSpecification`); TFC-05, TFB-07.
  - Sugestão: manter minúsculas e `default_tags`, adicionar as tags `project`/`phase` nos volumes do CSI e usar `phase=4` nas consultas de sobras.

- ⚠️ CONFLITO — Fim do suporte padrão do EKS 1.34. As fontes divergem: 2026-12-01 (LOG da Fase 3), "dezembro de 2026" (relatório da Fase 3) e 2026-12-02 (P-015, não conferido na web). O código não tem `upgrade_policy`.
  - Evidência: `docs/00_COLAB_IA/LOG_DE_TRABALHO.md:224`; `docs/00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md:167-174`; `terraform/cluster/variables.tf:76`; TFC-03.
  - Sugestão: confirmar a data na página oficial do EKS antes do apply, adicionar `upgrade_policy STANDARD` e avaliar 1.35/1.36, conferindo os addons.

- ⚠️ CONFLITO — Chart do ArgoCD e selfHeal. Segundo a P-015, o chart 7.7.11 (F3-SN-13) instala uma versão fora de suporte com CVE crítica. O selfHeal disputa réplicas com os HPAs e pode desfazer falhas de demonstração.
  - Evidência: `terraform/k8s/variables.tf:95`; `terraform/k8s/argocd.tf:320-332`; `gitops/base/evaluation-service/deployment.yaml:26`; `gitops/base/analytics-service/deployment.yaml:24`; TFK-02, GIT-04, TFK-06.
  - Sugestão: confirmar com `helm show chart` e avaliar um chart suportado. Remover `replicas` dos Deployments com HPA ou usar `ignoreDifferences`. Provocar a falha da demo sem alterar manifesto.

- ⚠️ CONFLITO — Exceções do Trivy vencidas. A F3-SN-20 exigia data de revisão, e a data registrada já venceu.
  - Evidência: `.trivyignore:58` ("Revisar em: 2026-10-15"), `:63`, `:68`, `:73`; CIC-08.
  - Sugestão: remedir as imagens finais antes do push na `main`, remover linhas sem efeito e usar `exp:` na própria linha.

- ⚠️ CONFLITO — Token do ArgoCD em repositório privado. A F3-SN-16 tratou o token como opcional, pensando em repositório público. O repositório da Fase 4 é privado, e o token continua opcional e vazio por padrão.
  - Evidência: `terraform/k8s/argocd.tf:54`; `terraform/k8s/variables.tf:125-135`; `00_COLAB_IA/DOSSIE_CONTEXTO.md:9`; TFK-11.
  - Sugestão: tornar a credencial obrigatória enquanto o repositório for privado (`validation` ou `precondition`) ou usar deploy key somente leitura.

- ⚠️ CONFLITO — Política de custo entre sessões. A Fase 3 passou de "base preservada com NAT desligado" (2026-09-11) para "destruir tudo" (2026-09-15). Na Fase 4, nenhuma política foi escolhida. Se ECR, role e OIDC criados à mão forem importados, o destroy da base os apagaria.
  - Evidência: `docs/00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md:130-133`; `docs/00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md:189-192`; `00_COLAB_IA/DECISOES.md` (sem ADR); TFB-01, XCL-03, XCL-10.
  - Sugestão: decidir em ADR, junto com a posse dos recursos manuais (import ou data source), qual opção vale entre sessões e no encerramento.

- ⚠️ CONFLITO — Material de aula. A Fase 3 decidiu mantê-lo versionado (2026-09-13). Na árvore da Fase 4, 34 arquivos da Fase 3 em `docs/` estão apagados sem commit, e o README diz que foram preservados.
  - Evidência: `git status`; `README.md:232`; `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:11`; DOC-11.
  - Sugestão: o usuário decide o destino das 34 deleções no B0; depois, ajustar o README e o relatório histórico.

- ⚠️ CONFLITO — Gerador do PDF. As fontes da Fase 3 divergem sobre o canônico (`gerar-relatorio-pdf.py` em 2026-09-11; `build-report` ReportLab em 2026-09-14), e os dois estão arquivados. Não há gerador ativo.
  - Evidência: `docs/00_COLAB_IA/LOG_DE_TRABALHO.md:23`, `:196`, `:201`; `docs/00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py:1-10`; `git ls-files`; DOC-01.
  - Sugestão: escolher um gerador e uma única fonte de texto para o relatório da Fase 4.

- ⚠️ CONFLITO — Entrega em grupo. A F3-D-006 previa grupo. A Fase 4 é implementação solo, e o REQ-OBR-41 diz "em grupo" ([INCERTO]). Falta confirmação do tutor.
  - Evidência: `00_COLAB_IA/DECISOES.md:73`; `docs/requisitos/README.md:90`; DOC-08.
  - Sugestão: pedir confirmação ao tutor e registrar a resposta com data. Não copiar a tabela de integrantes da Fase 3.

- ⚠️ CONFLITO — Varredura de segredos. `security-check.sh` só bloqueia o ID da conta da Fase 2. A conta da Fase 3 também é legado na Fase 4, e o guia histórico versionado traz o ID dela.
  - Evidência: `scripts/security-check.sh:68-77`; `docs/GUIA_DE_REPRODUCAO.md` (DOC-12: 10 linhas com o ID); XCL-14.
  - Sugestão: acrescentar uma regra para `<CONTA_FASE3>` e para ARNs/registries literais em `gitops/` e `.github/`. Trocar o ID por marcador no guia histórico.

- ⚠️ CONFLITO — Organização da memória de trabalho. A Fase 3 mantinha a memória em `docs/00_COLAB_IA`, tratava o arquivo morto como imutável e deixava o assistente gravar preferências por iniciativa própria. A Fase 4 usa `00_COLAB_IA/` na raiz, o usuário pediu o descarte da pasta da Fase 3, e a memória global só é usada quando pedida.
  - Evidência: `docs/00_COLAB_IA/LEIA-PRIMEIRO.md:30-32`; `docs/00_COLAB_IA/LOG_DE_TRABALHO.md:40`, `:371-373`; `CLAUDE.md:5`, `:11`.
  - Sugestão: o pedido do usuário prevalece. Registrar no LOG o de-para e o caminho de recuperação (`git show 3b21e65:docs/00_COLAB_IA/<arquivo>` e `tech-challenge-03`).

- ⚠️ CONFLITO — Parâmetros de entrega. O prazo 2026-09-15, o vídeo de até 20 min e o checklist das páginas 2 a 6 do PDF da Fase 3 não valem para a Fase 4 (2026-11-17, até 25 min, enunciado da Fase 4).
  - Evidência: `docs/00_COLAB_IA/_ARQUIVO_MORTO/ROTEIRO_VIDEO.md:1`; `docs/00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md:25,27`; `00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md:20-21`.
  - Sugestão: usar os roteiros e checklists da Fase 3 só como estrutura (D-002) e como teste de não regressão.