# Auditoria de organização do repositório — 2026-11-05 a 2026-11-07

TL;DR: o código e a infraestrutura estão organizados. Não há órfão real fora do diário; só o `pyproject.toml` não tem função. O peso está em três lugares:
- o diário `00_COLAB_IA`, com 569 dos 804 arquivos;
- o material da FIAP em `docs/aulas-fiap`, com 19,5 MiB, cerca de 60% dos 33,1 MiB versionados;
- 4,91 GiB de arquivos ignorados no disco.

Nada foi removido. Os pacotes da seção 3 aguardam aprovação do usuário, e a decisão mais urgente é o que a `main` mostra, porque o primeiro merge do tópico 5 publica a `dev` inteira.

Última atualização: 2026-11-07, Claude (Opus 5.5).

*Atualização de 2026-11-09:* aprovados pelo usuário e aplicados. P1, P2 e as cópias, pelo Codex (D-022). ArgoCD (b), P4, P5 e o que o P6 permitia antes do deploy, pelo Claude (D-023). Os PDFs da FIAP ficaram na árvore, por escolha do usuário. Ficam para depois do destroy os `.terraform`, e para o B6 o que depende de evidência do deploy; ver PENDENCIAS.

## 1. Escopo e método

- Três rodadas de agentes **somente leitura** sobre o HEAD `fe7464b`:
  - colaboração ativa e `02_TRABALHO`;
  - arquivo morto;
  - árvore pública;
  - arquivos locais ignorados, com um verificador cético das exclusões, que não têm volta;
  - próximos passos.
- Duas rodadas pararam no limite de uso e uma por falha de DNS. A crítica final foi feita na conversa, a partir dos resultados.
- Detalhe item a item em [ITENS_POR_AREA.md](ITENS_POR_AREA.md); texto integral e evidências em [resultados-brutos.json](resultados-brutos.json).
- O levantamento de próximos passos foi feito antes do roteiro v02 e da D-021, de 2026-11-05. Os itens de Alpine, IRSA, schemas e ordem das Applications já estão resolvidos.

## 2. Diagnóstico

| Área | Situação | Números |
|---|---|---|
| Código, CI, Terraform, GitOps | Organizado. Os 7 módulos Terraform são chamados; Compose `otel`/`newrelic`, `observability/` e `infra/` são usados por script ou Compose. | 235 arquivos fora do diário; único órfão: `pyproject.toml` |
| Material da FIAP | 31 PDFs das aulas e 5 guias de estudo. O avaliador não precisa deles; se o repositório ficar público, há questão de direitos autorais. Os guias têm 39 menções a agentes. | 19,5 MiB, cerca de 60% do repositório |
| Diário ativo (`00_COLAB_IA`) | Os documentos de topo permitem retomar, mas LEIA-PRIMEIRO, DOSSIE (§2–12) e ORGANIZACAO trazem frases desatualizadas. A PENDENCIAS tem 385 de 487 linhas em blocos históricos, que escondem itens ainda abertos. | `02_TRABALHO`: 274 arquivos (80 ficam, 40 precisam de atualização, 7 dependem de decisão, 127 podem ir para o arquivo morto, 20 são lixo) |
| Arquivo morto | 178 dos 289 arquivos têm o mesmo conteúdo em outro ponto do histórico. Nenhum passo do B3, do CI ou do ArgoCD usa a pasta. O DECISOES tem 470 links para o acervo da D-017, que é ignorado e fica só no disco: esses links quebram no GitHub. | 99 podem sair da árvore: 69 antes do merge e 30 depois do B5 ou no B6 |
| Disco local (ignorado) | Nada que deveria ser ignorado está versionado. `.env`, `backend.hcl` e `tfvars` são insubstituíveis. Nunca usar `git clean -X`. | 4,91 GiB: 1,98 GiB confirmados para sair agora; 2,69 GiB de caches `.terraform` só depois do destroy |
| Dados sensíveis | O ID da conta da Fase 3 está em 14 arquivos do arquivo morto (12 em `FASE3_BASE_6100879`) e 13 vezes no `docs/GUIA_DE_REPRODUCAO.md`. RMs aparecem no relatório e na apresentação da Fase 3. Tirar da árvore não limpa o histórico; o repositório é privado. | Só contagens, sem valores |

## 3. Pacotes para aprovação

| Pacote | O que entra | Quando | Reversível |
|---|---|---|---|
| **P1 — Disco** | Os 7 itens confirmados: `.terraform` do harness, caches Go da `qa-otel-go`, 6 executáveis Go (inclusive 2 no arquivo morto), `.venv` de 2026-10-22 e `__pycache__`. Ficam as evidências dentro das pastas `qa-*`. | agora | Não, mas tudo é regenerável |
| **P2 — Proteções** | `.gitignore` com regras para o JSON de plano do Terraform e para vídeos, antes do B4/B5; corrigir o comentário que chama todas as `qa-*` de reconstruíveis. | agora | Sim |
| **P3 — O que a `main` mostra** | Decisão do usuário antes do PR. Ver a seção 4. | antes do merge | Sim, pelo Git |
| **P4 — `services/**` e `.github/**`** | READMEs dos 5 serviços (Python 3.9, `us-east-1`, chaves estáticas da Fase 2), PyYAML sem uso no flag-service (remover ou manter para a demonstração de CVE) e IDs internos nos comentários dos workflows. | antes do merge, porque depois esses caminhos disparam `image` e `gitops` na `main` | Sim |
| **P5 — Retomada** | Retificações datadas em LEIA-PRIMEIRO, DOSSIE e ORGANIZACAO. Levar os blocos históricos da PENDENCIAS para o arquivo morto, depois de trazer para o topo D1–D5, o calendário e os itens abertos. | agora ou B6 | Sim |
| **P6 — B6** | Revisão D-018 dos documentos públicos (README, `terraform/`, `gitops/`, `observability/`, ARQUITETURA e requisitos). Relatório e apresentação da Fase 3 saem do caminho. Decidir o destino do GUIA da Fase 3. Também entram: `pyproject.toml`, comentários velhos do Terraform (EKS 1.31, `GUIA-AWS.md`), os 116 arquivos de `02_TRABALHO`, os 30 redundantes do arquivo morto, os `.terraform` e os `.tfplan`. | depois do destroy do B5 | Sim, exceto os caches, que são regeneráveis |

Imagens das pastas `qa-apm`, `qa-opensource`, `qa-fundamentos` e `qa-incidentes` (231 MB): o verificador pediu **AJUSTAR**. São regeneráveis a partir dos PDFs, mas o `pypdfium2` só existe no runtime do Codex, e o PDF da aula 5 de CI/CD só está no tech-challenge-03. Manter até o B6.

**Já feito em 2026-11-07, sem remoção:**
- `SECURITY.md` dizia que a role do CI aceitava qualquer branch ou pull request. Agora descreve a regra real: o `sub` exato da `main` com IDs imutáveis, provado pelos 10 testes do Terraform Check.
- `gitops/SECRETS-CONTRATO.md` ganhou os 3 Secrets da observabilidade (`grafana-admin`, `newrelic-license` e `grafana-notificacoes`).

## 4. Decisão P3: o que a `main` mostra

| Opção | Como | Prós | Contras |
|---|---|---|---|
| **(a) Publicar a `dev` como está** | Nada a fazer | Zero trabalho e transparência total do processo | O avaliador vê 569 arquivos internos antes do README. Entram também a conta da Fase 3, os RMs e os 19,5 MiB da FIAP |
| **(b) Publicar enxuta (recomendada)** | Antes do PR, em commit só de remoção: os 69 arquivos do arquivo morto (`FASE3_BASE_6100879`, as cópias de código de 2026-10-22, os 2 HTML duplicados e `2026-11-04_preimplantacao_v01`) e os 20 de lixo do `02_TRABALHO`. Decidir junto o material da FIAP e o CLAUDE.md | Tira da árvore as cópias com dado sensível e o ruído; o diário continua funcionando | O histórico continua com tudo; exige um commit cuidadoso |
| **(c) Tirar `00_COLAB_IA` da `main`** | Manter o diário fora da `dev` ou numa branch própria | `main` só com o projeto | Quebra o handoff entre agentes, 9 links do README e 4 caminhos de saída de QA em scripts e Compose. Não recomendada antes da entrega |

Subdecisões da opção (b):
- **Material da FIAP.** Manter versionado, ou tirar da árvore e guardar só no disco: um `.gitignore` em `docs/aulas-fiap/`, e o estudo continua acessível na sua máquina. Recomendação: tirar da árvore antes do merge.
- **CLAUDE.md.** Manter na raiz, ou mover para `.claude/CLAUDE.md`, que o Claude Code também lê sozinho e fica menos visível ao avaliador. Recomendação: mover.

## 5. Ordem sugerida

1. **Hoje:**
   - decidir o ArgoCD (seção 6) e o P3;
   - aplicar P1, P2 e P5;
   - P4 antes do PR.
2. **Antes do PR do tópico 5:**
   - P3 em commit só de remoção, com de-para no LOG (`git show <commit>:<caminho>`);
   - corrigir no mesmo PR os links que apontarem para o que saiu;
   - rodar o verificador no modo `pre-pr`.
3. **Tópico 5**, depois **tópico 6**.
4. **Depois do destroy confirmado nas 3 camadas:** apagar os `.terraform` e os `.tfplan`.
5. **B6:** P6.

Regras de execução:
- adicionar ao Git arquivo por arquivo;
- remoções em commit próprio;
- no Git Bash, usar `go clean -modcache` ou `rm -rf` para caminhos longos;
- depois de cada remoção local, conferir `git status --porcelain`;
- nunca apagar uma pasta `qa-*` inteira.

## 6. Pendências abertas encontradas fora da limpeza

- **ArgoCD com CVE crítica.** O chart `7.7.11` instala a v2.13.2. A falha `CVE-2025-55190` (GHSA-786q-9hcg-v9ff) permite que um token de projeto leia as credenciais de repositório. Foi corrigida em v2.13.9, v2.14.16, v3.0.14 e v3.1.2; nenhum chart da linha 7.7 traz a correção (o `7.7.23` instala v2.13.4). O chart atual é o `10.14.0`, com v3.6.1. Opções:
  - **(a)** manter, como risco aceito: sem Ingress, sem token de projeto e com o cluster vivo por poucos dias;
  - **(b)** chart `7.7.23` com a imagem v2.13.9 forçada nos values;
  - **(c)** subir para uma linha suportada, num salto 2.x→3.x com mudanças incompatíveis, que pede novo ensaio.

  Decidir antes do apply da camada k8s. Fontes: `terraform/k8s/variables.tf:95`, aviso oficial do argo-cd e a tag do argo-helm.
- **Gerador de tráfego para o tópico 6.** Não existe em `scripts/`. Sem tráfego contínuo direto no flag-service, a regra `FlagService5xxAlto` (5xx acima de 10% por 1 min) não dispara, porque o cache do evaluation esconde as chamadas.
- **Entrega:**
  - confirmar com o tutor se é individual ou em grupo, e o horário e o canal de envio (Q-03, Q-05 e Q-06);
  - dar acesso ao avaliador, porque o repositório é privado;
  - o relatório PDF não tem gerador vigente.
- **Aplicação**, fora do escopo exigido:
  - F-017: falha do targeting libera a flag no evaluation;
  - F-018: o auth responde 401 a qualquer erro de banco;
  - F-022: a revisão das exceções do `.trivyignore`, marcada para 2026-10-15, venceu.
- **Cronograma:** o B3 estava previsto para 2026-11-06 e não começou. O trial do PagerDuty termina em 2026-11-11, por relato.
