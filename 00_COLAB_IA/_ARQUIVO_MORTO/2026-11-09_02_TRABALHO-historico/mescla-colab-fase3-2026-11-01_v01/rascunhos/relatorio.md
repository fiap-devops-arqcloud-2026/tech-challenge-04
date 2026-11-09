# Mescla das pastas 00_COLAB_IA (Fase 3 → Fase 4)

Data: 2026-11-01. Repositório: tech-challenge-04, branch `dev`, HEAD `3b21e65`. Redação: Claude, a partir das rodadas de extração e consolidação.

**TL;DR:** os 39 arquivos de `docs/00_COLAB_IA/` (memória da Fase 3) foram lidos. O conteúdo útil virou 158 itens de conhecimento e 59 decisões com prefixo `F3-`, cada um com destino na pasta vigente `00_COLAB_IA/`. O que não serve mais ficou só no Git (`git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`) e no repositório tech-challenge-03. Este relatório lista o destino de cada tipo de conteúdo, o que foi descartado, onde estavam os dados sensíveis e 26 conflitos. Parte desses conflitos depende de decisão do usuário antes do primeiro apply na conta nova.

## 1. O que foi feito e por quê

- **Pedido (2026-11-01):** o usuário pediu para mesclar a memória da Fase 3 (`docs/00_COLAB_IA/`, 39 arquivos importados com o histórico em 2026-10-20) na colaboração vigente (`00_COLAB_IA/` na raiz). A mescla deve manter as decisões de arquitetura, as boas práticas e toda informação útil para decidir. Depois, a pasta da Fase 3 deve ser descartada.
- **Por quê:** a Fase 4 usa a mesma base da Fase 3 (5 serviços, Terraform em 3 camadas, ArgoCD/Kustomize, CI DevSecOps). As lições de operação, custo e gravação valem para a conta nova. Duas pastas de colaboração causavam colisão de IDs e risco de seguir regras superadas.
- **Método:**
  1. **Extração por lotes:** 11 lotes (G01 a G11), com leitura integral dos arquivos de texto. Os binários (7 PNGs e 1 PDF) foram só inventariados.
  2. **Consolidação cruzada:** 5 grupos (DEC, TEC-A, TEC-B, PROC-A e PROC-B). Cada item foi conferido, quando possível, contra o código atual da árvore de trabalho da `dev` e contra os achados da análise P-015 (`00_COLAB_IA/02_TRABALHO/ANALISE_COMPLETA_FASE4_2026-10-31_v01.md`).
  3. **Redação:** este relatório e os destinos abaixo. Toda consolidação foi somente leitura.
- **Rastreabilidade:** os IDs herdados recebem o prefixo `F3-` (F3-D-017, F3-SN-12, F3-P-124, F3-F-023). Os originais continuam recuperáveis por `git show 3b21e65:docs/00_COLAB_IA/<ARQUIVO>` e no repositório tech-challenge-03. Nas fontes da Fase 3, os caminhos são relativos a `docs/00_COLAB_IA/`.

## 2. Para onde foi cada tipo de conteúdo

| Conteúdo | Destino na pasta vigente | Volume |
|---|---|---|
| Arquitetura herdada, operação AWS (ordem de apply/destroy, armadilhas, sobras), CI/CD e DevSecOps, custos e tempos medidos, gravação e relatório (método), lições de processo | `DOSSIE_CONTEXTO.md` | 122 itens |
| Regras de trabalho do dia a dia: segredos fora do terminal, sem `terraform apply` interativo, shell certo no Windows, cinco estados de evidência, fluxo dev → PR → main, nada de `git add` de tudo, conferir registros contra código e Git, formato do LOG, ritual de sessão, preferências do usuário, comandos que exigem pedido explícito | `LEIA-PRIMEIRO.md` | 14 itens |
| Estrutura do monorepo, nomes e destinos de arquivos, o que nunca se versiona, um fato em um só documento, arquivo morto em commit separado, `git add` só do que foi revisado | `ORGANIZACAO_DE_PASTAS.md` | 6 itens |
| READMEs dos serviços com região us-east-1, gerador do PDF do relatório, regra da Fase 3 sobre documento público sem IA nem códigos internos | `PENDENCIAS_E_PROXIMOS_PASSOS.md` | 3 itens |
| Decisões vigentes ou a revisar (F3-D-003, F3-D-004, F3-D-007 a F3-D-012, F3-D-015 a F3-D-018, F3-D-020 a F3-D-024 e F3-SN-01 a F3-SN-30, exceto F3-SN-03) | `DECISOES.md` | 46 decisões |
| F3-SN-31 (material de aula no repositório) e F3-SN-32 (vídeo Não listado no YouTube) | `PENDENCIAS_E_PROXIMOS_PASSOS.md` | 2 decisões |
| Pendências técnicas ainda abertas no código herdado (por exemplo F3-P-110 a F3-P-115 e F3-P-124) | `PENDENCIAS_E_PROXIMOS_PASSOS.md` | [INCERTO] lista final conforme a gravação |
| Fatos só históricos e decisões superadas ou históricas | Este relatório, seção 4 | 13 itens e 11 decisões |
| De-para e caminho de recuperação dos originais | `LOG_DE_TRABALHO.md` (sugestão dos conflitos) | 1 entrada |
| Contradições entre fases | Este relatório, seção 7, para decisão e registro em `DECISOES`/`PENDENCIAS` | 26 temas (50 registros brutos) |

Vigência das 59 decisões herdadas: 23 vigentes, 26 a revisar, 6 superadas e 4 históricas.

## 3. Arquivo por arquivo

A coluna "bytes" vem do manifesto: é o tamanho do blob no commit `3b21e65`. O valor para a Fase 4 é o da extração.

| Arquivo | Blob | Bytes | O que era | Valor | O que foi aproveitado e onde |
|---|---|---|---|---|---|
| DECISOES.md | 9b47cca8d1b6 | 29949 | Registro de decisões D-001 a D-024 da Fase 3, com notas de superação de 2026-09-15 | alto | Decisões F3-D-003 a F3-D-024 → DECISOES. Superadas e históricas (F3-D-001, 002, 005, 006, 013, 014, 019) → seção 4. Conflitos de OIDC, sizing, Ingress e fluxo Git → seção 7 |
| INSTRUCOES_ASSISTENTES.md | 5e6889609121 | 12916 | Instruções vigentes da Fase 3 (2026-09-15): fatos técnicos, regras, mapa de gatilhos de CI, armadilhas, evidências | alto | Regras de trabalho → LEIA-PRIMEIRO. Gatilhos de CI e armadilhas → DOSSIE (gatilhos corrigidos pelos workflows atuais). Runs e PRs → seção 4 |
| LEIA-PRIMEIRO.md | 1dfd4f312558 | 2380 | Porta de entrada da memória da Fase 3 (2026-09-15) | médio | Ritual de sessão e regra de conflito → LEIA-PRIMEIRO. Índice de documentos públicos → seção 4. Ordem de leitura descartada |
| LOG_DE_TRABALHO.md | 6761b5578670 | 73322 | Diário append-only de 2026-07-17 a 2026-09-15 (dois lotes: linhas 1-236 e 237-581) | alto | Ordem de subida e destruição, tempos medidos, armadilhas (OIDC existente, ECR vazio, kubeconfig, PowerShell 5.1), regras do Trivy, lições de gravação e relatório → DOSSIE. Preferências → LEIA-PRIMEIRO. IDs Git e runs → seção 4. Estudos descartados |
| ORGANIZACAO_DE_PASTAS.md | 6b38c87385e2 | 5462 | Estrutura do monorepo e de-para dos movimentos de 2026-09-15 | médio | Regras de destino e lista "nunca versionar" → ORGANIZACAO. De-para descartado |
| PENDENCIAS_E_PROXIMOS_PASSOS.md | ea345566283f | 5012 | Pendências abertas no fim da Fase 3 (P-100 a P-132) | alto | Pendências técnicas ainda abertas no código (conferidas em 2026-11-01: PyYAML==6.0.1, NAT desligado no exemplo, ECR MUTABLE, revisão do .trivyignore vencida) → PENDENCIAS como F3-P-xxx. P-100, P-101 e P-105 descartadas |
| _ARQUIVO_MORTO/ARQUITETURA.md | a50d213230c0 | 3758 | Arquitetura da Fase 3 (2026-09-09): diagrama, três desvios, camadas e controles de segurança | alto | Arquitetura de referência, desvios e controles → DOSSIE. Diagrama Mermaid descartado (refazer com observabilidade) |
| _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md | e3dc8a4df919 | 20188 | Parecer de auditoria da entrega (achados F-042 a F-049) | alto | CRD em duas etapas, schemas idempotentes, dono único da SERVICE_API_KEY, custo do suporte estendido do EKS e política do bot GitOps → DOSSIE. Cinco estados de evidência → LEIA-PRIMEIRO |
| _ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md | 38b35e122e16 | 16587 | Passo a passo do bucket de estado, fora do Terraform | alto | Proteções do bucket e erros comuns → DOSSIE. F3-SN-02 e F3-SN-04 → DECISOES. Nome com ID da conta (F3-SN-03) → seção 4, mascarado |
| _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md | 2d3760c6f3cd | 16999 | Checklist O-01 a O-39, R-01 a R-09 e S-01 a S-09, com estados [x], [~] e [ ] | alto | Legenda de estados, requisitos que não podem regredir e critério literal → DOSSIE. Placar e marcos → seção 4 ou descartados |
| _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md | 26b69912965d | 17397 | Guia de exclusão completa da AWS, revisado mas não executado | alto | Ordem de encerramento, EBS órfão, DependencyViolation, bucket por último, conferência de sobras e flags destrutivas → DOSSIE. Inventário de 2026-09-11 → seção 4 |
| _ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md | 0dca16b4fbcb | 13492 | Snapshot do dossiê da Fase 3 | médio | Decisões estruturais (monorepo, Kustomize, prod, sem Ingress, tags) → DECISOES. Regras de colaboração → LEIA-PRIMEIRO. Glossário e estado vivo descartados |
| _ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md | 67d11a897414 | 1651 | Estimativa no AWS Pricing Calculator (2026-09-11): US$ 281,03/mês | alto | Estimativa oficial e limites → DOSSIE. F3-SN-29 → DECISOES. Link público descartado |
| _ARQUIVO_MORTO/EVIDENCIAS.md | cfea6995acae | 1534 | Checklist do que aparecer na tela (2026-09-09) | médio | Matriz requisito → evidência e separação com ou sem cluster → DOSSIE. Checkboxes descartados |
| _ARQUIVO_MORTO/GUIA_EXECUCAO.md | f9f3490c5796 | 2408 | Índice com três regras mínimas (2026-09-09) | alto | Regras mínimas (OIDC, ordem das camadas, NAT) → DOSSIE. "Um texto por assunto" → ORGANIZACAO |
| _ARQUIVO_MORTO/GUIA_GRAVACAO.md | 77690c012621 | 36061 | Guia de gravação de 2026-09-11, substituído em 2026-09-14 | alto | Matriz de evidências, blocos sem e com cluster, desvios a declarar, print de custo, checklist e comandos explicados → DOSSIE. Cenas de réplicas e de "base permanente" descartadas |
| _ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md | d5b41eefc530 | 10291 | Consolidação dos antigos CLAUDE.md e AGENTS.md da Fase 3 | alto | Fluxo Git (F3-D-019 a F3-D-021) → DECISOES e seção 4. Armadilhas (CRD, SERVICE_API_KEY, Redis, Free Tier) → DOSSIE. Regras → LEIA-PRIMEIRO |
| _ARQUIVO_MORTO/OPERACAO_2026-09-15.md | ac5a528c128d | 69906 | Guia operacional único da Fase 3 | alto | Compose local, provisionamento em 7 passos, schemas por pod psql, teardown, 30 armadilhas, custos e tempos de 2026-09-11, tabela de diagnóstico → DOSSIE. Shell certo → LEIA-PRIMEIRO |
| _ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md | 112b880b68c1 | 3001 | Estrutura do monorepo em 2026-08-27 | médio | Convenções de nome e "nunca versionar" → ORGANIZACAO. Árvore descartada |
| _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md | 1c5439847e8c | 36575 | Snapshot de pendências e achados F-001 a F-051 | alto | Apply parcial, merge de um lado inteiro, laço do job gitops, cadeia de upgrade do Go, continue-on-error, limites do plano gratuito, custos e sizing → DOSSIE. Implementação paralela → seção 4 |
| _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md | 0d5521333157 | 44788 | Runbook de recriação, gravação e destroy de 2026-09-15 | alto | Pré-voo, ordem das camadas, REDIS_URL e IRSA no overlay, run cancelado, Trivy, conferência pós-destroy e método de gravação (áudio, cenas fora de ordem, roteiro) → DOSSIE. F3-SN-33 → seção 4 |
| _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md | 63875156f428 | 15733 | Texto preliminar do relatório da Fase 3 | alto | Estrutura do relatório, desafios e decisões, seção de custos → DOSSIE. Dados pessoais omitidos |
| _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.pdf | 744e82642c8b | 247558 | PDF preliminar renderizado | baixo | Nada; descartado (seção 5) |
| _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md | ff714c6886aa | 13091 | Revalidação após os PRs 4 e 5 | alto | Parâmetros do `/evaluate` e pendências que persistiam → DOSSIE. F3-D-020 → DECISOES. Redirecionamento Bash no PowerShell → LEIA-PRIMEIRO |
| _ARQUIVO_MORTO/ROTEIRO_VIDEO.md | d802dff7f052 | 1103 | Linha do tempo do vídeo da Fase 3 (até 20 min) | médio | Distribuição de tempo por tema como modelo → DOSSIE |
| _ARQUIVO_MORTO/RUNBOOK-SESSAO.md | 4805faa4cc06 | 24121 | Runbook de sessão paga (2026-09-09) | alto | Formato de runbook, NAT antes do cluster, seed, SERVICE_API_KEY, parâmetros do `/evaluate` e disciplina de sessão → DOSSIE. Mapa O-27 a O-32 descartado |
| _ARQUIVO_MORTO/TESTE_COMPOSE.md | fa62fef23e7f | 2020 | Teste integrado local com Moto | médio | Compose Integration como teste integrado → DOSSIE. Menção a AWS Academy descartada |
| _ARQUIVO_MORTO/auditoria-2026-09-09/PLANO_AUDITORIA_2026-09-09_v01.md | 439fd88feee4 | 2382 | Plano e registro da auditoria | baixo | Só o modelo de processo; arquivo descartado |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-fiap-texto-por-pagina-2026-09-09.txt | 111f87c3293a | 6260 | Texto do enunciado da Fase 3, página a página | médio | Requisitos que a base não pode regredir → DOSSIE. Regras gerais de avaliação → seção 4 |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-1.png | 1b869943f0cc | 90285 | Capa do enunciado da Fase 3 | nenhum | Descartado |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-2.png | 46f4f51eef6d | 141567 | Página 2 do enunciado | nenhum | Descartado (coberto pelo .txt) |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-3.png | c5b9061bb980 | 142579 | Página 3 do enunciado | nenhum | Descartado (coberto pelo .txt) |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-4.png | 7d72d86c4917 | 150797 | Página 4 do enunciado | nenhum | Descartado (coberto pelo .txt) |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-5.png | 76c81ce5c6a8 | 150168 | Página 5 do enunciado | nenhum | Descartado (coberto pelo .txt) |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-6.png | bfbfa666a2dd | 36149 | Página 6 do enunciado | nenhum | Descartado (coberto pelo .txt) |
| _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-pagina-7.png | eb240979a403 | 211554 | Página 7, sem texto extraído | nenhum | Descartado. Conteúdo não verificado |
| _ARQUIVO_MORTO/build-report-fase3_2026-09-14.py | 5467b92031bc | 17266 | Gerador ReportLab do PDF preliminar (2026-09-14) | médio | Gerador do PDF → PENDENCIAS. F3-SN-30 → DECISOES. Dados pessoais omitidos |
| _ARQUIVO_MORTO/capturar-estimativa-aws_2026-09-11.cjs | 7bebe4156604 | 1559 | Script Playwright de captura do Pricing Calculator | médio | Captura automatizada → DOSSIE, com a ressalva dos cookies (seção 7, tema 26) |
| _ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py | 1dffb7f62377 | 7058 | Primeiro gerador (Markdown → WeasyPrint) | médio | "Relatório em Markdown versionado e PDF reproduzível" → DOSSIE. Ferramenta em si superada |

## 4. O que ficou só no histórico

Estes itens não entram na pasta vigente. Ficam registrados aqui e nos originais no Git.

**Itens de conhecimento (13)**

- **Render do gitops, contagens históricas:** 29 recursos no overlay em 2026-08-27 e 23 na auditoria de 2026-09-09. A fonte não explica a diferença. Fonte F3: LOG_DE_TRABALHO.md (237-581); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md.
- **Inventário da conta da Fase 3 (2026-09-11, 12:53-12:58 -03:00):** contagens de `plan -destroy` por camada. O snapshot do dossiê cita 14/35/36; a camada de cada número não foi conferida [INCERTO]. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md; _ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md.
- **Linha do tempo da pilha AWS:**
  - 2026-09-07: base aplicada com 33 recursos.
  - 2026-09-11: sessão e gravação sem áudio, seguidas de destruição.
  - 2026-09-15: recriação, regravação e destruição total.
  - Fonte F3: LOG_DE_TRABALHO.md (1-236); CHECKLIST.
- **Evidências de CI/CD da Fase 3:** CVE crítico barrado, tags `v1.0.0-<commit>` e commit `chore(gitops)`. Elas não provam nada no repositório 04. Fonte F3: INSTRUCOES_ASSISTENTES.md (140-146); EVIDENCIAS.md.
- **Implementação paralela na main da Fase 3:** foi reconciliada por merge híbrido em 2026-09-09. Só a lição sobre `-X theirs` foi para o DOSSIE. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md.
- **Regras gerais de avaliação da Fase 3:** peso de 90% da nota, opções A e B, vídeo de até 20 min, relatório em .PDF ou .txt. Na Fase 4 valem 25 min e entrega em 2026-11-17. Fonte F3: enunciado-fiap-texto-por-pagina-2026-09-09.txt.
- **Cronograma interno:** marcos M1 a M6 e plano em 4 fases até 2026-09-15. Não eram prazo da FIAP.
- **Demonstração DevSecOps/GitOps da Fase 3:** usou PyYAML no flag-service. `PyYAML==6.0.1` ainda está em `services/flag-service/requirements.txt:8` (lote G06, 2026-11-01).
- **Ausência de testes unitários na Fase 3:** fato superado. A Fase 4 já tem testes Go e Python (P-008 local, 2026-10-27).
- **Documentação oficial consultada, índice de documentos de apoio, execuções e identificadores Git da Fase 3:** só rastreabilidade.
- **Formato preferido para guias de estudo:** HTML, um por módulo (F3-D-005).

**Decisões (11)**

- F3-D-001 Repositório de destino da Fase 3: superada.
- F3-D-002 Guias em Markdown por módulo: superada (substituída por F3-D-005).
- F3-D-005 Guias HTML, um por módulo: vigente como preferência, mas sem efeito na entrega.
- F3-D-006 Entrega em grupo, prazo 2026-09-15: superada.
- F3-D-013 Secrets Manager + ESO: superada por F3-D-018.
- F3-D-014 Manifestos da Fase 2 como base do GitOps: histórica.
- F3-D-019 Preferência dev → PR → main: superada (absorvida por F3-D-020 e F3-D-021).
- F3-SN-03 Nome do bucket com ID da conta e região: superada. Padrão `togglemaster-tfstate-<CONTA_FASE3>-us-east-2-an`.
- F3-SN-33 Plano de gravação de 2026-09-15 substitui o guia de 2026-09-11: histórica.
- F3-SN-34 Demonstração DevSecOps/GitOps com PyYAML no flag-service: histórica.
- F3-SN-35 Caminho C e merge híbrido dev → main com `-X theirs`: histórica.

## 5. O que foi descartado e por quê

**Arquivos inteiros**

- As 7 PNGs do enunciado: repetem o .txt e o PDF da Fase 3, que continua recuperável. As páginas 1 e 7 não têm requisito.
- O PDF preliminar do relatório: é um artefato renderizado e superado, com dados pessoais. O conteúdo está no .md.
- PLANO_AUDITORIA_2026-09-09_v01.md: é registro de execução da auditoria. O único valor (subagentes independentes e passo de verificação) foi extraído.

**Descartes na consolidação**

- Terraform 1.16.0 baixado fora do PATH: detalhe local de 2026-08-27, com caminho pessoal. A versão do CI foi mantida.
- Mapeamento dos workflows para O-10 a O-20, O-24 e O-26: IDs de requisito da Fase 3 que colidem com a numeração atual (XCL-04).
- Regras de nome de bucket e comandos `get-bucket-*`: já estão em `docs/GUIA_DE_REPRODUCAO.md` (seção 3, 258-283), e o bucket da conta nova foi criado e confirmado em 2026-10-30. Só o resumo das proteções foi mantido.
- "Navegador bloqueia file://": já registrado como F-012 na PENDENCIAS vigente.
- Composição nominal do grupo da Fase 3: é dado pessoal. A Fase 4 é individual (D-009), e DOC-08 recomenda não copiar a tabela. Só a regra genérica ficou: confirmar a composição e registrar a resposta do tutor.
- Detalhes de comandos do roteiro antigo (`[-1]` no `--query` do ECR, `||` do grep): ficou só a lição de preparar um guia de comandos explicados (DOC-02).
- Pendências encerradas ou canceladas da Fase 3 (P-001 a P-017, P-019 a P-023, P-025, P-031, P-032, P-033, P-037): já foram decididas ou superadas pelo apply de 2026-09-07.
- P-026, P-027, P-028, P-030 e P-038: o código existe. O equivalente na conta nova é o plano B3 da P-015.
- P-051 (sincronizar dev e main da Fase 3): resolvida em 2026-09-09.
- P-049 (consolidar documentos antigos): superada por esta mescla.
- P-045/F-042 (`ignore-unfixed`): resolvida. Hoje é `ignore-unfixed: false` em `.github/workflows/_ci-go.yml:304` e `:429` e em `_ci-python.yml:337` e `:460`.
- F-051: estado de ambiente da conta antiga.
- P-007, P-009, P-011, P-013 e P-015 da Fase 3: revisão dos guias HTML da Fase 3.
- P-025: superada pelo apply da base em 2026-09-07.
- P-110 a P-115 como grupo: duplicata, porque cada item foi tratado individualmente.
- Scripts soltos em `tmp/`: a regra vigente já cobre (auxiliares em `00_COLAB_IA/02_TRABALHO`).
- Texto do TESTE_COMPOSE sobre sessão do AWS Academy: desatualizado e contraditório com a própria Fase 3.
- Conflito sobre ler repositórios de fases anteriores: não há contradição de princípio.
- Duplicatas internas foram fundidas: tags (2), checklist de estados (2), fonte óbvia (2), `-X theirs` (2), `git add` (2), nunca versionar (2), plano salvo (2), `phase=3` (6), vídeo de 20 min (5), Ingress (6) e OIDC false (4).

**Descartes da extração, resumidos por tipo**

- Estado e entrega da Fase 3: placar 24/6/9 e 25/8/6, marcos, links do vídeo, badge e marcador PREENCHER_URL_DO_VIDEO.
- Estado de branches e hashes: sincronização main/dev, PRs #1 a #6, runs, tags de imagem da Fase 3 e retificação de horário.
- Organização antiga: árvores de pastas, de-para de 2026-09-15 (commit 3317204), índices, âncoras e links relativos quebrados, referências aos antigos CLAUDE.md e AGENTS.md.
- Conta da Fase 3: nome do bucket, ID, ARN do contexto kubectl, PV e EBS, perfil local, P-100 e P-101, limpezas feitas em 2026-09-15.
- Gravação da Fase 3: abertura com slides próprios, backup do vídeo mudo, cena de réplicas, "base permanente", transcrição literal do enunciado e opção A (AWS Academy).
- Trilha de estudo da Fase 3 e glossário básico.
- Passo a passo do token fine-grained para o repositório da Fase 3. Ficou só a forma: Contents read-only via `TF_VAR_github_token`, testado com `git ls-remote`.
- Estilos visuais dos geradores e placeholders da Fase 3.

## 6. Dados sensíveis encontrados

O relatório indica só o tipo e o local, sem valores. Os IDs da conta foram mascarados como `<CONTA_FASE3>`. Os dados pessoais foram omitidos. Nenhum segredo real foi encontrado.

| Tipo | Onde (arquivo: linhas) | Tratamento |
|---|---|---|
| ID da conta da Fase 3 (direto ou no nome do bucket) | INSTRUCOES_ASSISTENTES.md: 15; PENDENCIAS_E_PROXIMOS_PASSOS.md: 11; LOG_DE_TRABALHO.md: 251, 423; _ARQUIVO_MORTO/OPERACAO_2026-09-15.md: 436; PLANO_GRAVACAO_2026-09-15.md: 84, 606, 865; GUIA_GRAVACAO.md: 155, 553, 614; PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md: 228, 254, 427; DOSSIE_CONTEXTO_2026-09-11.md: 75; DESTRUIR_AWS_2026-09-11.md: 17, 21, 49, 202; BOOTSTRAP-BACKEND-S3_2026-08-27.md: 5, 34, 275, 295, 309; RUNBOOK-SESSAO.md: 49; INSTRUCOES_ASSISTENTES_2026-09-14.md: 61, 93 | Mascarado como `<CONTA_FASE3>`; nada copiado |
| ARN com ID real | PLANO_GRAVACAO_2026-09-15.md: 217 (role do CI); DESTRUIR_AWS_2026-09-11.md: 51 (cluster EKS) | Não reproduzido |
| ARN só com placeholder | OPERACAO_2026-09-15.md: 604; BOOTSTRAP-BACKEND-S3_2026-08-27.md: 152-153, 222, 261 | Sem risco |
| Dados pessoais (nomes, RMs, usuários de Discord/GitHub, cidade) | RELATORIO_ENTREGA_..._PRELIMINAR.md: 18-24; build-report-fase3_2026-09-14.py: 253-260; gerar-relatorio-pdf_2026-09-11_v00.py: 84-92; PDF preliminar (inferido, não aberto) | Omitidos |
| Caminhos locais com nome de usuário | DECISOES.md: 294; PLANO_GRAVACAO_2026-09-15.md: 30, 81, 102, 121, 123, 125, 1064; DOSSIE_CONTEXTO_2026-09-11.md: 63, 80, 82; DESTRUIR_AWS_2026-09-11.md: 42 | Omitidos |
| Nome de pessoa em nome de branch | LOG_DE_TRABALHO.md: 243; PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md: 356 | Omitido |
| Referências a dados pessoais em outros arquivos (sem o valor) | PENDENCIAS_E_PROXIMOS_PASSOS.md: 15; LOG_DE_TRABALHO.md: 36, 38; PENDENCIAS_..._2026-09-11.md: 32, 424; CHECKLIST: 87; INSTRUCOES_ASSISTENTES_2026-09-14.md: 83-85 | Sem cópia |
| Outro projeto pessoal dono do provedor OIDC na conta antiga | DECISOES.md: 49, 53; INSTRUCOES_ASSISTENTES.md: 67; LOG_DE_TRABALHO.md: 85, 91; PLANO_GRAVACAO_2026-09-15.md: 62, 782 | Descrito só como "outro projeto" |
| Equipamento pessoal (headset) e crédito restante da conta antiga | PLANO_GRAVACAO_2026-09-15.md: 137-140, 858; DECISOES.md: 176 | Equipamento omitido. Crédito (US$ 70,33) citado só como justificativa histórica |
| Endpoints públicos (repositório e organização da Fase 3, runs, PRs, Pricing Calculator, provedor OIDC do GitHub) | INSTRUCOES_ASSISTENTES.md: 11, 140-146; LOG: 87; OPERACAO: 110, 120; PLANO_GRAVACAO: 130; GUIA_GRAVACAO: 181-183, 192; RUNBOOK-SESSAO: 75, 82-88, 148; AUDITORIA: 121, 149-155; REVALIDACAO: 77-79, 91-95; ESTIMATIVA: 6; RELATORIO .md: 30, 250-251; build-report: 267-276, 361, 407 | Não são segredos; não copiados |
| Placeholders de segredo e comandos que imprimem segredos | OPERACAO: 129-130, 218, 232, 239, 262, 287, 970, 976; RUNBOOK-SESSAO: 124, 130, 326, 358-362, 460, 494 | Nenhum valor real. A regra "não expor segredos no terminal" foi para o LEIA-PRIMEIRO |
| Fora da pasta, ainda versionado | `scripts/security-check.sh:10-11` (ID da Fase 3 em comentário); `docs/GUIA_DE_REPRODUCAO.md` (10 linhas com o ID, P-015 DOC-12) | Não reproduzido. Correção sugerida na seção 7, tema 21 |

## 7. Conflitos e pontos para o usuário decidir

Os 50 registros brutos foram agrupados em 26 temas. "Decidir" marca os pontos que precisam do usuário.

1. **Provedor OIDC na conta nova (decidir antes do primeiro apply).**
   - O provedor foi criado à mão na conta nova (por relato). O padrão e o exemplo ainda pedem criação: `terraform/variables.tf:237-241` e `terraform.tfvars.example:83` têm `true`. O plano B2 fala em "OIDC false".
   - A Fase 3 mandava manter `false` e nunca destruir o provedor (F3-D-022).
   - Sugestão: ADR da Fase 4 sobre a posse do provedor. O caminho simples é `false` no tfvars local, sem import. Se importar com `true`, alinhar `thumbprint_list` e ajustar o exemplo e o README. P-015 TFB-03, TFB-01 e XCL-03.
2. **Bancos e tipo de nó (decidir).**
   - F3-D-015 (2 RDS + pod) e F3-D-016 (c7i-flex.large) dependem do plano gratuito e do crédito de US$ 70,33 da conta antiga. A conta nova não ganha Free plan nem crédito (D-012 da Fase 4; PENDENCIAS:62).
   - Os comentários do Terraform tratam isso como fato atual (`terraform/cluster/main.tf:59`; `variables.tf:127-139`).
   - Sugestão: confirmar o plano de cobrança (P-003), decidir em ADR e reescrever os comentários como "conta da Fase 3". TFC-06.
3. **Dimensionamento e custo com observabilidade (decidir).**
   - O código tem 2 nós de 4 GiB (`terraform/cluster/variables.tf:86`, `:95`, `:102`). A D-015 da Fase 4 cita 3 workers.
   - O custo da Fase 3 (US$ 281,03/mês, cerca de US$ 0,385/h) foi calculado sem Prometheus, Loki, Grafana e Collector.
   - Há três valores por hora na Fase 3: US$ 0,385, US$ 0,37 (camada cluster) e US$ 0,368. O oficial é US$ 281,03/mês, cerca de US$ 0,385/h.
   - Conflitos internos da Fase 3 também pedem cuidado: 3 RDS contra 2 RDS no bootstrap, custo parado da base, 2 segredos no Secrets Manager sem dizer quais [ambíguo].
   - Sugestão: somar requests e limits dos charts, escolher entre 3 × c7i-flex.large ou um tipo com 8 GiB, e fazer estimativa nova com data. TFC-01, XCL-10.
4. **Ingress e acesso externo (decidir).**
   - F3-D-012 (sem Ingress e sem LB, economia de US$ 16-20/mês) foi validada contra o enunciado da Fase 3. Os manifests citam "D-012" no sentido da Fase 3 (`gitops/base/kustomization.yaml:73`).
   - Se as integrações forem só de saída, o port-forward pode bastar [INCERTO]. Um LB traz de volta o risco de DependencyViolation no destroy.
   - Sugestão: varrer o enunciado da Fase 4 e registrar ADR própria.
   - A regra de escopo da Fase 3 ("sem peça nova em runtime") não vale contra o enunciado da Fase 4. Fica só o princípio de não inflar.
5. **Colisão de IDs.**
   - Exemplos: F-023 (F3: recusa de t3.medium e bloqueio do plano gratuito; F4: trust OIDC). D-016 (F3: c7i-flex.large; F4: instrumentação local). D-012 (F3: sem Ingress; F4: continuar na AWS).
   - A Fase 3 também rotulava "conta pessoal" como D-016, quando no registro é a D-003.
   - Locais no código: `terraform/cluster/main.tf:15`, `:59`, `:74`; `terraform/modules/eks/main.tf:14`; `scripts/security-check.sh:70`.
   - Sugestão: prefixo `F3-` em toda referência herdada, regra no LEIA-PRIMEIRO e correção dos comentários em TFK-08/XCL-04.
6. **Fluxo Git e robô do CI na main (decidir quando liberar).**
   - F3-D-020 e F3-D-021 pressupõem push e merge na main. O CLAUDE.md proíbe push, PR e alteração da main nesta etapa.
   - A main do 04 está em `003a707`, sem `gitops/`, e a Application observa a main. O ritual `git merge --ff-only origin/main` não se aplica agora.
   - Sugestão: ADR com a ordem PR → CI publica 5 imagens e tags → troca de sentinelas → apply da k8s. Proibir force-push e `checkout dev -- gitops/`. Executar só com autorização (B0, B3). TFK-03, GIT-03, CIC-07.
7. **Self-healing por GitHub Actions contra "o CI não toca o cluster" (decidir o escopo da exceção).**
   - A Fase 3 evitou dar credencial AWS ao CI (S-08). O `selfHeal` do ArgoCD (`terraform/k8s/argocd.tf:325`) desfaz mudanças fora do Git.
   - O guia de 2026-09-11 chamava de self-heal do ArgoCD a recriação de um pod apagado, que na verdade é feita pelo controlador do Deployment (observação do analista).
   - Sugestão: role própria com trust de environment, `eks:DescribeCluster`, access entry e RBAC só no namespace `togglemaster`, com allowlist de Deployments. No vídeo, explicar que `rollout restart` não muda o manifesto. CIC-01, XCL-08, TFB-05, TFC-02, GIT-07.
8. **Trava F3-D-024 em `services/**` e workflows.** A Fase 4 já instrumentou os serviços e precisa de um workflow novo. Sugestão: tratar a trava como superada e manter só a ordem: role, ECR e Variables prontos na conta nova antes de levar as mudanças à main.
9. **Documento público sem IA nem códigos internos (decidir).**
   - Regra da Fase 3 (INSTRUCOES_ASSISTENTES.md:5, :39; LEIA-PRIMEIRO.md:28).
   - Na Fase 4: `README.md:5` cita Codex; `README.md:14-16`, `:43`, `:184-186`, `:226` citam 00_COLAB_IA e D-0xx. Os READMEs de terraform, gitops e observability também citam esses termos.
   - O `CLAUDE.md` é versionado, embora a D-001 da Fase 4 e `ORGANIZACAO_DE_PASTAS.md:18` digam para não criá-lo na raiz.
   - Sugestão: o usuário decide se a regra vale para o README final e o PDF (B6).
10. **SECURITY.md desatualizado.**
    - `SECURITY.md:20-23` diz que a trust aceita qualquer branch.
    - Na árvore de trabalho, a trust virou `StringEquals` no subject da main (`terraform/modules/iam-ci/main.tf:81`, `:141-147`). O HEAD ainda tem `StringLike` com curinga.
    - Sugestão: comitar a correção F-023 da Fase 4 com autorização e reescrever o parágrafo. CMP-03, TFB-04.
11. **Segredos de terceiros.**
    - "Nenhuma chave estática" (Fase 3) não cobre New Relic, PagerDuty, Slack nem o token de dispatch.
    - O `gitops/SECRETS-CONTRATO.md` e o `SECURITY.md` não os citam (busca de 2026-11-01). Os manifests ainda citam ESO e Secrets Manager.
    - Sugestão: estender o contrato com uma linha por credencial e limitar "sem chave estática" a credenciais AWS. XCL-09, TFK-04, CMP-02, GIT-08.
12. **Tag `phase` e valores fixos da Fase 3.**
    - O código já usa `phase = "4"` (`terraform/variables.tf:58`). Os volumes do CSI não recebem tags (`terraform/k8s/storageclass.tf`), e os guias herdados filtram por `phase=3`.
    - Outros valores mudaram: chaves `phase4/prod/*.tfstate`, `tc04-integration`, `expected_aws_account_id` obrigatório, 25 min e 2026-11-17.
    - Sugestão: tags nos volumes do CSI, `phase=4` nas consultas de sobras e runbook novo (DOC-02). TFC-05, TFB-07, CMP-07, XCL-12.
13. **Fim do suporte padrão do EKS 1.34.**
    - As datas divergem: 2026-12-01 (Fase 3: LOG:155, :224; `docs/GUIA_DE_REPRODUCAO.md:101`; `docs/ARQUITETURA.md:133`), "dezembro de 2026" (relatório preliminar) e 2026-12-02 (P-015 TFC-03, não conferido na web).
    - Não há `upgrade_policy` no código.
    - Sugestão: conferir com `aws eks describe-cluster-versions` na conta nova, registrar com fonte e avaliar `upgrade_policy STANDARD`. As duas datas caem depois da entrega.
14. **Chart do ArgoCD 7.7.11 e selfHeal contra HPA.**
    - Segundo a P-015, a versão fixada na Fase 3 (F3-SN-13) instala ArgoCD fora de suporte, com CVE crítica.
    - O selfHeal disputa réplicas com os HPAs.
    - Sugestão: conferir com `helm show chart`, tirar `replicas` dos Deployments com HPA ou usar `ignoreDifferences`, e provocar a falha da demo sem alterar o manifesto. TFK-02, GIT-04, TFK-06.
15. **`.trivyignore` vencido.** A data "Revisar em: 2026-10-15" (`.trivyignore:58`, `:63`, `:68`, `:73`) já passou. Sugestão: remedir as imagens finais, remover linhas sem efeito e usar `exp:` na linha. CIC-08.
16. **Token do ArgoCD e visibilidade do repositório.**
    - As fontes da Fase 3 divergem: repositório privado em 2026-08-27, público em 2026-09-15.
    - O repositório 04 é privado, e o `github_token` é opcional e vazio por padrão (`terraform/k8s/variables.tf:125-135`).
    - Sugestão: tornar a credencial obrigatória enquanto o repositório for privado, ou usar deploy key somente leitura. TFK-11.
17. **Política de custo entre sessões (decidir).**
    - A Fase 3 passou de "base com NAT desligado" (2026-09-11) para "destruir tudo" (2026-09-15). Com a base destruída, merges em `services/` falham por falta da role.
    - Na Fase 4, ECR, role, policy e OIDC foram criados à mão. Se forem importados, o destroy da base os apagaria.
    - Sugestão: ADR conjunta com a posse dos recursos manuais (import ou data source). TFB-01, XCL-03.
18. **Material de aula e arquivo morto (decidir).**
    - A Fase 3 decidiu manter o material versionado (2026-09-13). Na árvore atual, 34 arquivos da Fase 3 em `docs/` estão apagados sem commit, e `README.md:232` diz que foram preservados.
    - A regra de "arquivo morto imutável" cede ao pedido explícito do usuário.
    - Sugestão: confirmar as 34 deleções no B0 e registrar o de-para no LOG. DOC-11.
19. **Gerador do PDF (decidir).** Há dois geradores arquivados (WeasyPrint de 2026-09-11 e ReportLab de 2026-09-14) e nenhum ativo. Sugestão: escolher um gerador e uma única fonte de texto. DOC-01.
20. **Grupo ou individual (decidir com o tutor).** F3-D-006 e REQ-OBR-41 dizem "em grupo" [INCERTO], mas a implementação da Fase 4 é solo. Sugestão: pedir confirmação ao tutor e registrar a resposta com data. DOC-08.
21. **`security-check.sh` com lógica invertida.**
    - O script só bloqueia a conta da Fase 2 (`:68-78`), diz que a Fase 3 "roda em conta pessoal", traz o ID da Fase 3 em comentário (`:10-11`) e se exclui da varredura (`:51`).
    - Sugestão: proibir `<CONTA_FASE3>` e ARNs ou registries literais em `gitops/` e `.github/`, sem escrever o ID em claro (F3-P-124). Trocar o ID por marcador no guia histórico. XCL-14, CIC-05.
22. **Parâmetros de entrega da Fase 3.** Prazo 2026-09-15, até 20 min e checklist das páginas 2 a 6 não valem. Usar só como estrutura (D-002 da Fase 4) e como não regressão.
23. **Teto do provider AWS.**
    - A Fase 3 diz que `~> 6.0` conflitava com o módulo VPC (LOG:399; F3-F-021). Mas a versão resolvida, 6.62.0, satisfaz `~> 6.0`, o que torna a justificativa duvidosa.
    - Sugestão: tratar como [INCERTO] e testar `>= 5.79, < 7.0` ou `~> 6.62` com `init -backend=false` e `validate`. TFB-11.
24. **Gatilhos do CI na documentação histórica.** `docs/ARQUITETURA.md:242-243` e o mapa da Fase 3 dizem push só na main. Os workflows `terraform-check.yml` e `compose-integration.yml` têm `[main, dev]`. Sugestão: no DOSSIE, usar os workflows atuais como fonte e corrigir em DOC-07.
25. **Memória do assistente.** Na Fase 3, preferências foram gravadas por iniciativa do assistente (LOG:371, :373, :395). Na Fase 4 prevalece o CLAUDE.md: memória global só quando pedida.
26. **Cookies no script de captura.** `capturar-estimativa-aws_2026-09-11.cjs:35-41` aceita o banner se não achar a recusa. Sugestão: se o script for reaproveitado, recusar sempre os cookies não essenciais e falhar quando a recusa não existir.

## 8. Limitações

- **Rodadas:** a rodada 1 foi interrompida por limite de uso. A rodada 2 reaproveitou a extração já feita nos lotes G01 a G11. Falhas de consolidação: `[]` (nenhuma).
- **Escopo da leitura:**
  - Os arquivos de texto foram lidos inteiros na extração. As 7 PNGs e o PDF não foram abertos, só inventariados.
  - Na consolidação, os originais foram reabertos só nos pontos ambíguos: gerador de PDF, rótulo D-016, data do EKS, LOG 391-402 e PENDENCIAS_2026-09-11 428-432, mais amostras do PROC-A.
  - Os demais itens dependem da fidelidade da extração.
- **Base de comparação:** a conferência com o código usou a árvore de trabalho da `dev` em 2026-11-01, que tinha 149 entradas no `git status` (por exemplo, trust OIDC, `terraform.tfvars.example` e serviços com OTel). Ela difere do HEAD `3b21e65`, e os números de linha podem mudar quando o trabalho for comitado.
- **O que não foi feito:**
  - Nenhum `terraform plan`, `kubectl kustomize`, consulta AWS ou GitHub remoto, nem preço atual.
  - Não foram verificados: plano de cobrança da conta nova, data oficial do EKS 1.34, appVersion e CVE do chart 7.7.11, existência do provedor OIDC e do bucket novo (só por relato), proteção de branch remota.
  - O enunciado da Fase 4 não foi varrido para Ingress, webhooks e opcionais (fica [INCERTO]).
  - Não foram conferidos a versão do Go nos Dockerfiles, o desfecho do F3-F-046 (SERVICE_API_KEY) nem se as 3 exceções de perl-base continuam no `.trivyignore`.
  - Dos achados P-015, só cerca de 30 foram lidos em detalhe.
- **Lotes com ambiguidades:**
  - G04: render 29 contra 23.
  - G06: o "35 to add" é atribuído ao cluster por uma fonte e à base pela outra. Os tempos do PLANO e do GUIA são estimativas.
  - G08: o alvo de 3 h não bate com a soma de cerca de 2 h, nem 30-40 com 35-45 min.
  - G09: F3-F-043 aparece como corrigido no checklist e como persistente na revalidação. O-34 cita 7 workflows e R-09 cita 9.
  - G11: não se sabe qual gerador produziu o PDF v00.
- **Mapeamento por arquivo:** a entrada consolidada não traz o arquivo de origem de cada item. A coluna "o que foi aproveitado e onde" da seção 3 associa arquivos a temas pelos resumos da extração.
- **Tamanhos:** os bytes da seção 3 são do blob no commit. A extração citou tamanhos maiores em alguns arquivos (por exemplo, RELATORIO .md com 16.058 contra 15.733 e build-report com 17.688 contra 17.266). A causa provável é a quebra de linha CRLF na árvore de trabalho [INCERTO].
- **Estado da gravação:** ao redigir este relatório (2026-11-01), os arquivos vigentes de `00_COLAB_IA/` ainda não tinham entradas `F3-` (grep com 0 ocorrências). A gravação dos destinos e o descarte da pasta são etapas posteriores.
- **Lista de pendências:** a lista final de pendências F3-P-xxx levadas à PENDENCIAS não está detalhada nesta entrada [INCERTO].
- **Mascaramento:** os IDs de conta foram contados sem serem impressos. Nenhum dado pessoal ou segredo foi reproduzido.

## 9. Verificação

PREENCHER_VERIFICACAO