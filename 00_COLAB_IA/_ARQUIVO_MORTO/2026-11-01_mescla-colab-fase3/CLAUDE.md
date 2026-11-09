# Tech Challenge Fase 4 — contexto para assistentes

Última atualização: 2026-10-27, Codex.

- Ler primeiro `00_COLAB_IA/LEIA-PRIMEIRO.md`, PENDENCIAS, topo do LOG e DOSSIE. Essa é a colaboração vigente; `docs/00_COLAB_IA` é histórico importado da Fase 3.
- Português do Brasil, dados com data/fonte; não inventar funcionamento. Manter originais e rastreabilidade.
- Código da Fase 3 importado com histórico; requisitos, cinco guias e materiais da Fase 4 preservados. README/Terraform/GitOps descrevem o destino atual.
- Usuário autorizou branch `import-fase3` e merge local para `dev`. Trabalhar na `dev` após a integração; sem push, PR ou alteração da `main` nesta etapa.
- Nova conta AWS pendente; não usar credenciais, estado, ARNs ou endpoints da conta anterior. Nenhum deploy autorizado nesta etapa.
- `tech-challenge-03` continua somente leitura. Auxiliares locais em `00_COLAB_IA/02_TRABALHO`; não adicionar renderizações, caches, estados ou segredos ao Git.
- Antes de encerrar, atualizar LOG/PENDENCIAS/DECISOES/DOSSIE e registrar verificações e limitações. Memória global somente quando pedida pelo usuário.

- P-008 local concluída em 2026-10-27: integração + OTel/Collector, 19 spans/5 serviços, testes Go/Python, SQL/HTTP/SQS e logs aprovados. Ver relatórios dos passos1/2 e RESULTADO_PASSOS_LOCAIS em 00_COLAB_IA/02_TRABALHO. Laboratório removido; evidências locais ignoradas preservadas.
- E1 externa depende de conta/chave e validação New Relic; métricas, coleta de logs e implantação da stack/alertas/incidentes continuam pendentes. Nenhum commit/push/PR/AWS foi executado nestes passos.
