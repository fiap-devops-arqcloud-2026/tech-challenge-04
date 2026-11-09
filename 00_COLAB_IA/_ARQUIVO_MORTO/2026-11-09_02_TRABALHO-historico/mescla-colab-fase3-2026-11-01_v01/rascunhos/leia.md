## Regras herdadas da Fase 3

Consolidadas em 2026-11-01 a partir de `docs/00_COLAB_IA/`. Os originais ficam em `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO` e no repositório tech-challenge-03. As fontes F3 são relativas a `docs/00_COLAB_IA/`. Aqui só entra o que não está nas seções acima.

### Registro e evidência

- **IDs da Fase 3 levam o prefixo F3-** (F3-D-012, F3-P-110, F3-F-023). ID sem prefixo é da Fase 4. Os números colidem: a D-012 da Fase 3 é "sem Ingress", e a da Fase 4 é "continuar na AWS". Os comentários do código ainda usam IDs antigos sem prefixo (XCL-04, TFK-08). Fonte F3: DECISOES.md (208-218); comparar com 00_COLAB_IA/DECISOES.md:95.
- **Registro não é prova.** Confrontar decisões, checklist, pendências e runbook com o código e o Git. Atribuir autoria a um agente só por metadado (Co-Authored-By). Discordância entre agentes vira registro com motivo. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (6, 11, 80); LOG_DE_TRABALHO.md (316).
- **Cinco estados de evidência, que não se substituem:** código existente, verificação local, execução no CI, funcionamento na AWS e evidência de entrega. CI verde não prova pods no EKS nem sync do ArgoCD. terraform validate não garante CRDs nem bancos. Em 2026-09-09, a auditoria achou 4 falhas bloqueantes que o checklist não mostrava. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (14, 139); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (26, 97).
- **Procurar na fonte óbvia** antes de abrir pendência ou perguntar ao usuário. A P-018 da Fase 3 ficou 28 dias aberta, e a resposta estava no README da Fase 2. Depois de cada decisão, revisar as pendências que ficaram obsoletas. Fonte F3: LOG_DE_TRABALHO.md (363, 375).
- **README de services/ não serve de fonte para infraestrutura.** Esses READMEs vêm da Fase 2 e trazem Go 1.21, Python 3.9, us-east-1 e chaves estáticas. Em 2026-08-27, a região foi inferida errada por causa deles. Confirmar no código ou com o usuário. Fonte F3: LOG_DE_TRABALHO.md (435-437); INSTRUCOES_ASSISTENTES.md (116).
- **Antes de editar, conferir `git status --short` e a branch.** Todo documento leva TL;DR e "Última atualização" com data e autor, e separa o que foi confirmado ao vivo do que não foi executado. Retificação vira nota datada; listas "Não repetir" evitam retrabalho. Fonte F3: INSTRUCOES_ASSISTENTES.md (107-114); LEIA-PRIMEIRO.md (34-39); LOG_DE_TRABALHO.md (10-12).

### Comandos e operação

- **Só com pedido explícito do usuário:** terraform init/plan/apply/destroy com backend, aws com escrita, gh run rerun, gh workflow run e gh pr. A leitura é livre: git grep, git log, terraform fmt -check, kubectl kustomize, gh run view e gh run list. Pedido de orientação não autoriza destruir nada. Fonte F3: INSTRUCOES_ASSISTENTES.md (70); LOG_DE_TRABALHO.md (155, 157, 167).
- **Terraform sempre com plano salvo:** `plan -out=<camada>.tfplan` e depois `apply <camada>.tfplan`. No destroy, `plan -destroy -out`. Nunca usar apply interativo: em 2026-09-15, num bloco colado, a linha seguinte virou a resposta do "yes". Fonte F3: DECISOES.md (33, 38).
- **Shell certo no Windows.** Blocos em Git Bash, um comando por linha, sem `&&` e sem barra invertida de continuação, com o shell indicado em cada bloco. No PowerShell 5.1:
  - não há `&&`; usar `; if ($?) {...}`;
  - a continuação de linha é a crase;
  - `<` não redireciona;
  - `curl` é Invoke-WebRequest; usar `curl.exe`;
  - não há `base64 -d`;
  - `terraform plan -out=arquivo` exige `--%`.

  No Git Bash, `python`/`python3` pode cair no atalho da Microsoft Store (visto de novo em 2026-11-01). Não trocar de shell no meio de uma fase. Fonte F3: INSTRUCOES_ASSISTENTES.md (46, 132); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (60-81, 1556-1562).

### Segredos e Git

- **Segredo nunca aparece em terminal, chat ou arquivo versionado.** Guardar URLs de banco, MASTER_KEY e chaves de API em variáveis do shell. Para conferir, mostrar só um prefixo (`${CHAVE:0:12}...`) ou o protocolo e o host. Token do GitHub só em variável `TF_VAR_`. Base64 de Secret não é criptografia: senha que aparece em vídeo publicado está vazada. A regra vale para a gravação e para as chaves de New Relic, PagerDuty e Slack. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (979-995, 1065-1076); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (156-157); _ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md (145-147).
- **Antes de cada commit, varrer o diff** em busca de credenciais, .env, chave privada, kubeconfig, tfstate e dados pessoais. Fonte F3: _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (456-461); INSTRUCOES_ASSISTENTES.md (48).
- **O assistente não faz add, commit, push, mv, rm, stash ou checkout sem pedido explícito.** Nunca usar `git add .` nem `-A`. Em 2026-09-15 isso levou à main 13 arquivos não revisados e uma trava `~$` do PowerPoint (commit 06f97c6). Adicionar arquivo por arquivo, pelo caminho. Fonte F3: INSTRUCOES_ASSISTENTES.md (51-52); LOG_DE_TRABALHO.md (36).
- **Fluxo futuro:** dev → PR → main com `merge --merge`. Nunca usar `--delete-branch` no `gh pr merge`, porque apagaria a dev. A dev não cria outro ambiente AWS. Nesta etapa não há autorização de push, PR nem main. Fonte F3: DECISOES.md (80-109); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (837).

### Escrita e código

- Explicação simples antes da técnica; número medido sempre com data. [INCERTO] Em 2026-08-27, o usuário pediu na Fase 3 código comentado linha a linha e uma linha de comentário acima de cada comando mostrado. O CLAUDE.md da Fase 4 não registra esse pedido: confirmar com o usuário se ele continua valendo. Fonte F3: INSTRUCOES_ASSISTENTES.md (38-45); LOG_DE_TRABALHO.md (371, 393-395).

### Regras da Fase 3 que não valem como estão

| Regra da Fase 3 | ⚠️ CONFLITO com a Fase 4 | Como tratar | Fonte F3 |
|---|---|---|---|
| Não editar services/** nem .github/workflows/** (F3-D-024) | Os serviços já foram instrumentados com OTel, e a Fase 4 precisa de workflow de self-healing | Regra superada. Vira ordem de execução: editar na dev é livre; a main só recebe as mudanças com role, ECR e Variables prontos (F3-P-140) | DECISOES.md (12, 24) |
| Sincronizar a dev com a main (`git merge --ff-only origin/main`) antes de editar | A main do 04 está em 003a707, sem a importação, e a dev não teve push | Aplicar só quando a main do 04 passar a receber commits do robô | INSTRUCOES_ASSISTENTES.md (53-64); LEIA-PRIMEIRO.md (37) |
| Documento público sem IA, assistentes, 00_COLAB_IA ou códigos internos | O README da Fase 4 cita Codex e D-009/D-012/D-014, e o CLAUDE.md está versionado | O usuário decide (P-016) | INSTRUCOES_ASSISTENTES.md (39); LEIA-PRIMEIRO.md (28) |
| O CI não faz deploy, só o ArgoCD toca o cluster, e o CI não tem credencial AWS (S-08) | O self-healing por GitHub Actions precisa de role AWS e de kubectl rollout restart | Registrar em DECISOES uma exceção explícita e restrita. No vídeo, distinguir o selfHeal do ArgoCD do self-healing pedido na Fase 4 | _ARQUIVO_MORTO/GUIA_GRAVACAO.md (330-338, 702-717); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (117) |
| create_github_oidc_provider = false e nunca destruir o provedor, que na conta antiga era de outro projeto | Na conta nova o provedor foi criado à mão (por relato), e o exemplo traz true | Não copiar a regra. Antes do primeiro apply, conferir o provedor e registrar em DECISOES se ele será importado ou só lido | DECISOES.md (45-59); INSTRUCOES_ASSISTENTES.md (67, 124) |
| Extra só se não trouxer peça nova em runtime (sem plataformas de observabilidade, Ingress, ESO etc.) | O enunciado da Fase 4 exige Collector, Prometheus, Loki, Grafana, New Relic, PagerDuty e Slack | Manter só o princípio: não ir além do enunciado da Fase 4 | INSTRUCOES_ASSISTENTES.md (69) |
| O assistente grava preferências na memória por iniciativa própria | CLAUDE.md: memória global só quando o usuário pedir | Prevalece a regra da Fase 4 | LOG_DE_TRABALHO.md (371, 373) |
| Prazo 2026-09-15, vídeo de até 20 min e checklist do PDF da Fase 3 | Entrega em 2026-11-17, vídeo de até 25 min e enunciado da Fase 4 | Usar roteiros e checklists da Fase 3 só como estrutura (D-002) e como teste de não regressão | _ARQUIVO_MORTO/ROTEIRO_VIDEO.md (1); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (25, 27) |