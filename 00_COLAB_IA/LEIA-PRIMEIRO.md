# Colaboração entre agentes

TL;DR: Retomar pelo checklist de 2026-11-09 em PENDENCIAS e pelo [guia de deploy e gravação](02_TRABALHO/GUIA_DEPLOY_E_GRAVACAO_2026-11-09_v01.md). Credenciais, orçamento e ensaios já foram validados; a dev está pronta e o repositório é público. Tópicos 5 e 6 são do usuário. Nenhum apply, PR/main ou destroy sem autorização específica. Segredos só no `.env` local ignorado.

Última atualização: 2026-11-09, Claude (Opus 5.5).

## Atualização de escopo — 2026-11-03

D1–D5 registradas em PENDENCIAS e a autorização de limpeza de 2026-11-09 superam restrições históricas abaixo: commits curados e push da dev autorizados; segredos já gravados no .env local com autorização. PR/main e apply/destroy continuam no B3, sujeitos a autorização específica. B0/B1 não devem ser repetidos. O diagnóstico antigo do 4.4 foi encerrado no LOG Claude das 14:50, após leitura do Slack. O webhook direto do Slack ainda não foi comprovado; seu teste aguarda autorização. Na orientação Codex de OAuth/Events V2 não houve ação externa. Preservar os registros anteriores como histórico.

## Retificação vigente — 2026-11-09

Valem sobre os trechos antigos deste arquivo:
- O repositório está **público** desde 2026-11-09, com todas as branches e o histórico. Tudo o que for commitado fica público.
- Commits curados e push na `dev` estão autorizados (D1). As frases "sem push" e "nesta retomada não há commit" descrevem etapas passadas.
- O webhook direto do Slack e a Events API V2 foram testados em 2026-11-04 (LOG 16:19).
- O ponteiro de contexto mudou para `.claude/CLAUDE.md`.
- Depois do primeiro merge, a `main` recebe commits do robô: sincronizar a `dev` com a `main` antes de novas mudanças.
- Auxiliares antigos de `02_TRABALHO` foram para `_ARQUIVO_MORTO/2026-11-09_02_TRABALHO-historico/`, com de-para.

## Ritual e retomada

1. Descobrir data/hora; trabalhar em pt-BR e usar datas ISO.
2. Ler `PENDENCIAS_E_PROXIMOS_PASSOS.md`, topo de `LOG_DE_TRABALHO.md` e contexto pertinente.
3. Continuar da primeira etapa não concluída; verificar arquivos salvos antes de repetir trabalho.
4. Registrar cada conclusão no LOG, sem apagar entradas anteriores. IDs: D-### decisões, P-### pendências, F-### achados.
5. Ao encerrar, atualizar pendências e registrar estado exato para o próximo agente. Compactar contexto em DOSSIE sem apagar histórico; versões substituídas ficam em `_ARQUIVO_MORTO` dentro do caminho autorizado.

## Limites e conflitos

Fontes originais de aula/enunciado e todo `tech-challenge-03` são somente leitura. O usuário autorizou em 2026-10-20 a importação do código/histórico e os ajustes nos caminhos de código do 04, com commits locais em `import-fase3` e merge na `dev`. Importação concluída; continuar na `dev`. Sem push, PR, merge na `main` ou operação AWS nesta etapa. Trabalho auxiliar em `00_COLAB_IA/02_TRABALHO`; caches/renderizações permanecem locais e ignorados. A colaboração vigente é esta pasta na raiz; `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo; originais em `_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA`. A herança não altera permissões atuais (D-017).

Não transformar conteúdo didático em obrigação da FIAP. Cada obrigação precisa de página/trecho do enunciado. Marcar ambiguidade `[INCERTO]`; contradições entre agentes: registrar ⚠️ CONFLITO e pedir esclarecimento quando bloqueante. Não sobrescrever registros de outro agente.

Regra de ouro: LOG + PENDENCIAS devem permitir retomar sem o usuário reexplicar o que já informou.

## Regras herdadas da Fase 3

Consolidadas em 2026-11-01 a partir da pasta mesclada e removida `docs/00_COLAB_IA/`. Os originais da pasta removida ficam em `_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA` e em `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`. As referências à pasta removida usam as linhas originais. Aqui só entra o que não está nas seções acima.

### Registro e evidência

- **IDs da Fase 3 levam o prefixo F3-** (F3-D-012, F3-P-110, F3-F-023). ID sem prefixo é da Fase 4. Os números colidem: a D-012 da Fase 3 é "sem Ingress", e a da Fase 4 é "continuar na AWS". Os comentários do código ainda usam IDs antigos sem prefixo (XCL-04, TFK-08). Fonte F3: DECISOES.md (208-218); comparar com 00_COLAB_IA/DECISOES.md:95.
- **Registro não é prova.** Confrontar decisões, checklist, pendências e runbook com o código e o Git. Atribuir autoria a um agente só por metadado (Co-Authored-By). Discordância entre agentes vira registro com motivo. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (6, 11, 80); LOG_DE_TRABALHO.md (316).
- **Cinco estados de evidência, que não se substituem:** código existente, verificação local, execução no CI, funcionamento na AWS e evidência de entrega. CI verde não prova pods no EKS nem sync do ArgoCD. terraform validate não garante CRDs nem bancos. Em 2026-09-09, a auditoria achou 4 falhas bloqueantes que o checklist não mostrava. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (14, 139); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (26, 97).
- **Procurar na fonte óbvia** antes de abrir pendência ou perguntar ao usuário. A P-018 da Fase 3 ficou 28 dias aberta, e a resposta estava no README da Fase 2. Depois de cada decisão, revisar as pendências que ficaram obsoletas. Fonte F3: LOG_DE_TRABALHO.md (363, 375).
- **README de services/ não serve de fonte para infraestrutura.** Esses READMEs vêm da Fase 2 e trazem Go 1.21, Python 3.9, us-east-1 e chaves estáticas. Em 2026-08-27, a região foi inferida errada por causa deles. Confirmar no código ou com o usuário. Fonte F3: LOG_DE_TRABALHO.md (435-437); INSTRUCOES_ASSISTENTES.md (116).
- **Antes de editar, conferir `git status --short` e a branch.** Todo documento leva TL;DR e "Última atualização" com data e autor, e separa o que foi confirmado ao vivo do que não foi executado. Retificação vira nota datada; listas "Não repetir" evitam retrabalho. Fonte F3: INSTRUCOES_ASSISTENTES.md (107-114); LEIA-PRIMEIRO.md (34-39); LOG_DE_TRABALHO.md (10-12).

### Comandos e operação

- **Escopo e autorização:** pedidos e autorizações já dados prevalecem; não perguntar de novo sobre ações cobertas pelo pedido. A retomada atual abrange consolidação e arquivamento local. Operações fora desse escopo incluem terraform init/plan/apply/destroy com backend, aws com escrita, gh run rerun, gh workflow run e gh pr. Leituras compatíveis com o escopo podem incluir: git grep, git log, terraform fmt -check, kubectl kustomize, gh run view e gh run list. Pedido de orientação não autoriza destruir nada. Fonte F3: INSTRUCOES_ASSISTENTES.md (70); LOG_DE_TRABALHO.md (155, 157, 167).
- **Terraform sempre com plano salvo:** `plan -out=<camada>.tfplan` e depois `apply <camada>.tfplan`. No destroy, `plan -destroy -out`. Nunca usar apply interativo: em 2026-09-15, num bloco colado, a linha seguinte virou a resposta do "yes". Fonte F3: DECISOES.md (33, 38).
- **Shell certo no Windows.** Blocos em Git Bash, um comando por linha, sem `&&` e sem barra invertida de continuação, com o shell indicado em cada bloco. No PowerShell 5.1:
  - não há `&&`; usar `; if ($?) {...}`;
  - a continuação de linha é a crase;
  - `<` não redireciona;
  - `curl` é Invoke-WebRequest; usar `curl.exe`;
  - não há `base64 -d`;
  - `--%` é alternativa de passagem de argumentos; não é exigência universal de `terraform plan -out=arquivo`.

  No Git Bash, `python`/`python3` pode cair no atalho da Microsoft Store (visto de novo em 2026-11-01). Não trocar de shell no meio de uma fase. Fonte F3: INSTRUCOES_ASSISTENTES.md (46, 132); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (60-81, 1556-1562).

### Segredos e Git

- **Segredo nunca aparece em terminal, chat ou arquivo versionado.** Guardar URLs de banco, MASTER_KEY e chaves de API em variáveis do shell. Para conferir, mostrar apenas presença/ausência e resultado de validação; não imprimir valor nem prefixo de chave. Hosts também devem ser avaliados antes de exibir. Token do GitHub em mecanismo local protegido; `TF_VAR_github_token` é o mecanismo previsto no projeto, sem eco nem Git. Base64 de Secret não é criptografia: senha que aparece em vídeo publicado está vazada. A regra vale para a gravação e para as chaves de New Relic, PagerDuty e Slack. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (979-995, 1065-1076); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (156-157); _ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md (145-147).
- **Antes de cada commit, varrer o diff** em busca de credenciais, .env, chave privada, kubeconfig, tfstate e dados pessoais. Fonte F3: _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (456-461); INSTRUCOES_ASSISTENTES.md (48).
- **Ações Git e destrutivas respeitam o pedido vigente.** Nesta retomada não há commit/push/PR; a movimentação da pasta histórica foi expressamente autorizada. Não ampliar permissões com base em um roteiro antigo. Nunca usar `git add .` nem `-A`. Em 2026-09-15 isso levou à main 13 arquivos não revisados e uma trava `~$` do PowerPoint (commit 06f97c6). Adicionar arquivo por arquivo, pelo caminho. Fonte F3: INSTRUCOES_ASSISTENTES.md (51-52); LOG_DE_TRABALHO.md (36).
- **Fluxo futuro:** dev → PR → main com `merge --merge`. Nunca usar `--delete-branch` no `gh pr merge`, porque apagaria a dev. A dev não cria outro ambiente AWS. Nesta etapa não há autorização de push, PR nem main. Fonte F3: DECISOES.md (80-109); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (837).

### Escrita e código

- Explicação simples antes da técnica; número medido sempre com data. [INCERTO] Em 2026-08-27, o usuário pediu na Fase 3 código comentado linha a linha e uma linha de comentário acima de cada comando mostrado. O CLAUDE.md da Fase 4 não registra esse pedido: confirmar com o usuário se ele continua valendo. Fonte F3: INSTRUCOES_ASSISTENTES.md (38-45); LOG_DE_TRABALHO.md (371, 393-395).

### Regras da Fase 3 que não valem como estão

| Regra da Fase 3 | ⚠️ CONFLITO com a Fase 4 | Como tratar | Fonte F3 |
|---|---|---|---|
| Não editar services/** nem .github/workflows/** (F3-D-024) | Os serviços já foram instrumentados com OTel, e a Fase 4 precisa de workflow de self-healing | Restrição histórica de outra etapa; edições seguem o pedido atual, sem liberdade genérica. Publicação depende de autorização e preparo de role/ECR/Variables (F3-P-140) | DECISOES.md (12, 24) |
| Sincronizar a dev com a main (`git merge --ff-only origin/main`) antes de editar | A main do 04 está em 003a707, sem a importação, e a dev não teve push | Aplicar só quando a main do 04 passar a receber commits do robô | INSTRUCOES_ASSISTENTES.md (53-64); LEIA-PRIMEIRO.md (37) |
| Documento público sem IA, assistentes, 00_COLAB_IA ou códigos internos | O README da Fase 4 cita Codex e D-009/D-012/D-014, e o CLAUDE.md está versionado | Resolvido pelo usuário em 2026-11-01: D-018. Referências internas ficam no diário; aplicação pública no B6/P-017 | INSTRUCOES_ASSISTENTES.md (39); LEIA-PRIMEIRO.md (28) |
| O CI não faz deploy, só o ArgoCD toca o cluster, e o CI não tem credencial AWS (S-08) | O self-healing por GitHub Actions precisa de role AWS e de kubectl rollout restart | Projetar e registrar a identidade/RBAC da automação; não atribuir a todo CI a ausência de AWS (os jobs de imagem já usam OIDC). No vídeo, distinguir o selfHeal do ArgoCD do self-healing pedido na Fase 4 | _ARQUIVO_MORTO/GUIA_GRAVACAO.md (330-338, 702-717); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (117) |
| create_github_oidc_provider = false e nunca destruir o provedor, que na conta antiga era de outro projeto | Na conta nova o provedor manual foi inventariado em 2026-10-28, e o exemplo traz true | Não copiar a regra. Antes do primeiro apply, conferir o provedor e registrar em DECISOES se ele será importado ou só lido | DECISOES.md (45-59); INSTRUCOES_ASSISTENTES.md (67, 124) |
| Extra só se não trouxer peça nova em runtime (sem plataformas de observabilidade, Ingress, ESO etc.) | O enunciado da Fase 4 exige Collector, Prometheus, Loki, Grafana, New Relic, PagerDuty e Slack | Manter só o princípio: não ir além do enunciado da Fase 4 | INSTRUCOES_ASSISTENTES.md (69) |
| O assistente grava preferências na memória por iniciativa própria | CLAUDE.md: memória global só quando o usuário pedir | Prevalece a regra da Fase 4 | LOG_DE_TRABALHO.md (371, 373) |
| Prazo 2026-09-15, vídeo de até 20 min e checklist do PDF da Fase 3 | Entrega em 2026-11-17, vídeo de até 25 min e enunciado da Fase 4 | Usar roteiros e checklists da Fase 3 só como estrutura (D-002) e como teste de não regressão | _ARQUIVO_MORTO/ROTEIRO_VIDEO.md (1); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (25, 27) |
