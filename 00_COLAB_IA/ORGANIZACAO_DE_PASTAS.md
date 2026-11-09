# Organização

TL;DR: Estrutura de código preservada. Em 2026-11-09 saíram redundâncias e caches, e os auxiliares antigos foram para o arquivo morto, com de-para. Pastas ignoradas não são sinônimo de lixo. O repositório é público.

Última atualização: 2026-11-09, Claude (Opus 5.5).

| Área | Uso |
|---|---|
| PDF na raiz | Enunciado, somente leitura |
| `docs/aulas-fiap/<módulo>/` | PDFs originais somente leitura; criar apenas `GUIA-ESTUDO-*.html` |
| `docs/requisitos/` | README de requisitos |
| `00_COLAB_IA/` | Protocolo, contexto, decisões, pendências e log |
| `00_COLAB_IA/02_TRABALHO/` | Scripts, extratos, inventário, análises e verificações |
| `00_COLAB_IA/_ARQUIVO_MORTO/` | Versões anteriores substituídas, se necessário |

Nomes auxiliares: descrição + data ISO + `_v01`; nomes dos entregáveis seguem o pedido. Acentos dos arquivos originais são preservados. HTML deve ser UTF-8 e funcionar por duplo clique, sem servidor/dependências de rede.

Não criar diretórios genéricos vazios. CLAUDE.md já existe como ponteiro interno e é mantido conforme as instruções globais atuais; a regra de 2026-09-16 dizia respeito ao setup inicial de estudos. `tech-challenge-03` é exclusivamente referência de leitura.

## Retificação vigente — 2026-11-09

- A observabilidade e seus Compose/scripts estão versionados; a descrição herdada abaixo sobre estarem fora do Git retrata 2026-11-01.
- A regra de exclusão do JSONL de 156 MB já existe. As proteções de planos JSON e vídeos foram adicionadas nesta limpeza.
- O repositório é público desde 2026-11-09: revisar arquivo por arquivo antes de versionar.
- `CLAUDE.md` agora está em `.claude/CLAUDE.md`.
- O relatório e a apresentação da Fase 3 saíram da árvore, e `docs/evidencias/` recebe os prints da Fase 4, já revisados.
- Auxiliares antigos estão em [`_ARQUIVO_MORTO/2026-11-09_02_TRABALHO-historico`](_ARQUIVO_MORTO/2026-11-09_02_TRABALHO-historico/DE-PARA.md), com de-para.
- Os documentos antigos descritos abaixo como "sem commit" ou "fora do Git" retratam 2026-11-01.
- Consultar o [manifesto de exclusões](02_TRABALHO/limpeza-2026-11-09_v01/manifesto-exclusoes.json) para recuperar as 121 versões removidas; não criar novas cópias desses artefatos sem necessidade.
- Os alvos removidos do arquivo morto não eram consumidos pelo projeto. As demais versões e o acervo local da D-017 continuam disponíveis.
- Históricos abaixo permanecem como fontes datadas; a autorização e o estado atuais estão em PENDENCIAS.

## Regras herdadas da Fase 3

Consolidadas em 2026-11-01 a partir de `docs/00_COLAB_IA/`. Os originais ficam em `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO` e no repositório tech-challenge-03. As fontes F3 são relativas a `docs/00_COLAB_IA/`.

### Estrutura do repositório

- **Monorepo dividido por responsabilidade** (estrutura de 2026-09-15):
  - código em `services/`;
  - infraestrutura em `terraform/` (base na raiz da pasta; `cluster/`, `k8s/` e `modules/`);
  - manifestos em `gitops/base/` e `gitops/overlays/prod/`, com README.md e SECRETS-CONTRATO.md;
  - pipelines em `.github/workflows/`;
  - scripts em `scripts/` (test-compose.sh e integration/ são usados pelo CI);
  - init do Postgres local em `infra/`;
  - documentação em `docs/`.

  Fonte F3: ORGANIZACAO_DE_PASTAS.md (9-29).
- **Artefatos novos de observabilidade seguem essa divisão.** Em 2026-11-01, `observability/`, `docker-compose.otel.yaml` e `scripts/test-observability.sh` existiam na árvore, mas `git ls-files` não os listava: estão fora do Git (OBS-03, DOC-05, XCL-01).

### Destino e nomes

| O quê | Onde | Regra | Fonte F3 |
|---|---|---|---|
| Documento público | `docs/` | Nome em `MAIUSCULAS_COM_UNDERSCORE.md` | ORGANIZACAO_DE_PASTAS.md (37) |
| Evidência datada (captura, estimativa) | `docs/evidencias/` | Data ISO no nome | ORGANIZACAO_DE_PASTAS.md (40) |
| Script | `scripts/` | Só se for executável e estiver em uso; o obsoleto vai para o arquivo morto | ORGANIZACAO_DE_PASTAS.md (43) |
| Saída de gerador e rascunho | `00_COLAB_IA/02_TRABALHO/` | Regra vigente da Fase 4; output/tmp eram convenção histórica. Não linkar artefato ignorado na entrega pública | ORGANIZACAO_DE_PASTAS.md (44) |
| Microsserviço | `services/<nome>-service` | Mesmo nome no ECR e no Kustomize | _ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md (48-68) |

- **Versões:** data ISO no nome. Nada de "copia" ou "final-final"; usar `_v01`, `_v02` ou `_VIGENTE`. Fonte F3: _ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md (48-68).
- **Cada fato tem detalhe em um só documento.** Nos demais lugares, basta uma frase com link. Mapa da Fase 3:
  - README: o quê e por quê;
  - GUIA_DE_REPRODUCAO: comandos, tempos medidos, valores a trocar e armadilhas;
  - ARQUITETURA: portas, probes, IRSA, Secrets e versões;
  - RELATORIO_DE_ENTREGA: o relatório;
  - SECURITY.md, terraform/README.md, gitops/README.md e SECRETS-CONTRATO.md: cada um só do seu assunto.

  Na Fase 4, guia, arquitetura e relatório ainda são históricos (com aviso na linha 1) e não têm versão vigente (DOC-01, DOC-02, DOC-07). Fonte F3: INSTRUCOES_ASSISTENTES.md (91-105); DECISOES.md (10-17).

### O que nunca se versiona

- **Lista:** terraform.tfstate e variantes, `*.tfvars`, `*.tfplan`, `.env` (exceto `.env.example`), chaves `.pem`/`.key`, kubeconfig, travas `~$*` do Office e qualquer credencial. Na Fase 4, a lista inclui a license key do New Relic, a routing key do PagerDuty e o webhook do Slack. Fonte F3: ORGANIZACAO_DE_PASTAS.md (46); INSTRUCOES_ASSISTENTES.md (48).
- **Situação em 2026-11-01:** o .gitignore cobre a lista (linhas 4-6, 12, 22-23, 28-32, 38-40 e 88), e terraform/.gitignore:3 ignora backend.hcl. Ainda falta regra para o arquivo de 156 MB (F-024; CMP-01, XCL-02).
- **Adicionar ao Git só os arquivos revisados, um a um, pelo caminho.** Manter `~$*`, `output/` e `tmp/` no .gitignore. A contagem do Git muda com os artefatos; consultar snapshot-retomada-codex.json para o recorte desta sessão. Fonte F3: LOG_DE_TRABALHO.md (36, 74, 202).

### Arquivo morto e movimentos

- **Versão substituída** vai para `_ARQUIVO_MORTO` com sufixo `_AAAA-MM-DD` e de-para no LOG.
- **Mover ou remover em commit próprio,** separado das edições, para preservar o `git log --follow`. Na Fase 3, o commit dos movimentos foi o 3317204.
- **Histórico não se reescreve.** Entradas antigas mantêm os caminhos da época. Para corrigir um estado, criar uma entrada nova datada.

Fonte F3: ORGANIZACAO_DE_PASTAS.md (42, 50); LEIA-PRIMEIRO.md (30-32); DECISOES.md (22).

A remoção de `docs/00_COLAB_IA` foi feita somente na árvore local (sem commit); futura publicação deve separar a movimentação das mudanças funcionais. De-para no LOG e caminho de recuperação registrado (`git show 3b21e65:docs/00_COLAB_IA/<arquivo>` e tech-challenge-03).

### Regras da Fase 3 em conflito

- ⚠️ CONFLITO: na Fase 3, a memória de trabalho ficava em `docs/00_COLAB_IA`, e o arquivo morto era imutável. Na Fase 4, a colaboração fica em `00_COLAB_IA/` na raiz, e o usuário pediu para descartar a pasta da Fase 3. Prevalece o pedido do usuário. Os links relativos da Fase 3 quebram ao mover o conteúdo. Fonte F3: LEIA-PRIMEIRO.md (30-32); ORGANIZACAO_DE_PASTAS.md (41-42).
- ⚠️ CONFLITO: na Fase 3, o usuário decidiu manter o material de aula versionado (2026-09-13). Na árvore da Fase 4, 34 arquivos da Fase 3 em `docs/` estão apagados sem commit, enquanto o README.md:232 diz que foram preservados. O usuário decide o destino deles no B0 (DOC-11). Fonte F3: ORGANIZACAO_DE_PASTAS.md (38); LOG_DE_TRABALHO.md (138-142).
- ⚠️ CONFLITO: pela regra da Fase 3, documento público não cita IA nem códigos internos. O README da Fase 4 não segue essa regra. Além disso, o CLAUDE.md está versionado na raiz, contra a regra deste arquivo de não criá-lo sem autorização. Resolvido em D-018: referências internas no diário; revisão pública no B6/P-017. CLAUDE.md permanece como ponteiro interno, conforme as instruções globais atuais. Fonte F3: ORGANIZACAO_DE_PASTAS.md (37).
Acervo integral da mescla: [_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/). As referências históricas em crases mantêm o caminho da época; novos links ativos usam o destino arquivado.
