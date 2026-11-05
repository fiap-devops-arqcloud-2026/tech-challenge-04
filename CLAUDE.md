# Tech Challenge Fase 4 — contexto para assistentes

TL;DR: trabalhar na dev e retomar pela "Execução vigente" de PENDENCIAS (2026-11-05). B0/B1/B2 e a preparação do B3 concluídos (notificações reais, testes, plano da base com 0 destroy e US$ 9,82/dia em 02_TRABALHO/PREPARACAO_B3_2026-11-04_v01.md). Pré-requisitos fechados em 2026-11-05: tokens validados, orçamento `togglemaster-creditos` e créditos em US$ 120; teste da confiança OIDC no Terraform Check (b2c5bdf); painel dos nós no dashboard (46d0a18); GitOps Check e scan da imagem no PR (793384e). O cluster EKS se chama `togglemaster`. Falta só a autorização dos tópicos 5 e 6. Commits e push na dev autorizados; main, apply e destroy exigem autorização específica.

Última atualização: 2026-11-05, Claude (Opus 5.5).

- SaaS (atualização 2026-11-05): New Relic conferido; nova chave Events API V2 e webhook direto do Slack testados em 2026-11-04 (LOG 16:19), com PRTG mantido. Senha do PagerDuty mantida pelo usuário, risco aceito (D-020); agentes não a usam. D5 autorizou segredos no .env local ignorado; não gravar valores em arquivos versionados, LOG ou chat. Guia: `00_COLAB_IA/02_TRABALHO/PAGERDUTY_OAUTH_EVENTS_API_2026-11-03_v01.md`.

- Ler `00_COLAB_IA/LEIA-PRIMEIRO.md` → PENDENCIAS → topo do LOG → DOSSIE/DECISOES. `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo; acervo em `00_COLAB_IA/_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA` (D-017).
- Português do Brasil, explicação simples antes da técnica, datas ISO e fonte. Distinguir relato, configuração, teste local, execução externa e evidência de entrega.
- Código/histórico da Fase 3 importados em 2026-10-20. Enunciado, materiais e cinco guias da Fase 4 preservados. `tech-challenge-03` é somente leitura.
- Branch atual dev. D1 de 2026-11-03 autoriza commits curados e push origin/dev, já realizados pelo Claude; PR/merge main continuam no B3 com autorização específica. Nesta orientação Codex não houve commit/push. Movimentação local da pasta de colaboração concluída em P-016.
- AWS/GitHub: inventário de 2026-10-28 com 34/34 verificações; trust OIDC corrigido localmente e 8/8 testes offline. Bucket novo completo por relato do usuário em 2026-10-30; backend.hcl nas três raízes ignorado. tfvars locais (ignorados) e imports prontos no plano da base; a adoção efetiva acontece no apply do B3. Orçamento criado em 2026-11-05, fora do Terraform. Não reutilizar conta/state/segredos da Fase 3.
- P-008 local concluída em 2026-10-27: 19 spans/5 serviços e ensaio integrado. B1 New Relic e teste isolado PagerDuty → Slack concluídos em 2026-11-03. Stack no EKS e cadeia completa alerta → self-healing ainda sem comprovação; não confundir o teste isolado com a entrega integrada.
- P-015 tem análise Claude de 44 itens (42 obrigatórios + 2 opções); P-014 tem catálogo Codex e matriz de 42 obrigatórios, fechamento documental pendente. Não somar achados repetidos nem tratar os números como nota.
- D-018: documentos públicos focados no projeto; autoria de agentes e IDs internos ficam no diário. Aplicação pública na revisão B6/P-017, sem apagar histórico. Este arquivo é ponteiro interno.
- Auxiliares em `00_COLAB_IA/02_TRABALHO`; versões em `00_COLAB_IA/_ARQUIVO_MORTO`. Não versionar credenciais, estados, caches ou renderizações; revisar arquivo por arquivo antes de futura publicação. Memória global somente quando pedida diretamente.
- Encerrar com LOG incremental, PENDENCIAS, decisões e teste de handoff. Documento da mescla: `00_COLAB_IA/02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md`.
