# Tech Challenge Fase 4 — contexto para assistentes

TL;DR: trabalhar na dev e retomar pelo bloco "Estado em 2026-11-03" de PENDENCIAS. Contas SaaS prontas até o 4.3 do guia PASSO2; B0 e B1 aguardam as decisões D1–D5; trial do PagerDuty até 2026-11-11. Stack e publicação continuam pendentes.

Última atualização: 2026-11-03, Claude (Opus 5.5).

- SaaS (2026-11-03): New Relic, PagerDuty (trial até 2026-11-11, política Default, Events API v2) e Slack (webhook) preparados pelo usuário até o 4.3. Os segredos ficam só com o usuário: não gravar em arquivo versionado, LOG ou chat. Usar o `.env` local (ignorado) apenas com autorização.

- Ler `00_COLAB_IA/LEIA-PRIMEIRO.md` → PENDENCIAS → topo do LOG → DOSSIE/DECISOES. `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo; acervo em `00_COLAB_IA/_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA` (D-017).
- Português do Brasil, explicação simples antes da técnica, datas ISO e fonte. Distinguir relato, configuração, teste local, execução externa e evidência de entrega.
- Código/histórico da Fase 3 importados em 2026-10-20. Enunciado, materiais e cinco guias da Fase 4 preservados. `tech-challenge-03` é somente leitura.
- Branch atual dev; sem commit/push/PR/merge main nesta retomada. A autorização antiga de importação foi cumprida e não é permissão permanente de publicar. Movimentação local da pasta de colaboração autorizada em P-016.
- AWS/GitHub: inventário de 2026-10-28 com 34/34 verificações; trust OIDC corrigido localmente e 8/8 testes offline. Bucket novo completo por relato do usuário em 2026-10-30; backend.hcl nas três raízes ignorado. Faltam tfvars, adoção dos recursos manuais e validação da cobrança. Não reutilizar conta/state/segredos da Fase 3.
- P-008 local concluída em 2026-10-27: 19 spans/5 serviços e ensaio integrado. Laboratório encerrado; não repetir como se faltasse instrumentação. E1 externa (New Relic), stack no EKS, alerta/PagerDuty/Slack e self-healing ainda sem comprovação.
- P-015 tem análise Claude de 44 itens (42 obrigatórios + 2 opções); P-014 tem catálogo Codex e matriz de 42 obrigatórios, fechamento documental pendente. Não somar achados repetidos nem tratar os números como nota.
- D-018: documentos públicos focados no projeto; autoria de agentes e IDs internos ficam no diário. Aplicação pública na revisão B6/P-017, sem apagar histórico. Este arquivo é ponteiro interno.
- Auxiliares em `00_COLAB_IA/02_TRABALHO`; versões em `00_COLAB_IA/_ARQUIVO_MORTO`. Não versionar credenciais, estados, caches ou renderizações; revisar arquivo por arquivo antes de futura publicação. Memória global somente quando pedida diretamente.
- Encerrar com LOG incremental, PENDENCIAS, decisões e teste de handoff. Documento da mescla: `00_COLAB_IA/02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md`.
