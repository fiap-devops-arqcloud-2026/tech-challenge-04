# Retomada da entrega e gravação

TL;DR: ensaio real concluído com sucesso. Os quatro tipos de evidência exigidos no PDF foram capturados. Artefatos são rascunhos em revisão; não publicar antes de finalizar. Última atualização: 2026-11-09 16:13 (America/Sao_Paulo), Codex.

## Autorizações e estado

- Pedido atual autoriza README, workflows, PDF/PPTX, relatório, capturas, push dev, PR main e merge após validação. Não pedir novamente. Nenhum apply/destroy autorizado nesta rodada.
- Usuário autorizou falha real 503, notificações e restart no EKS; confirmou login no PagerDuty; identificação deve vir do README da Fase 3.
- Dev foi sincronizada por fast-forward com main, baseline 484cdcb. Há alterações não commitadas desta rodada. Não descartar. Nenhum novo push/PR/merge desta rodada foi realizado.
- Interrupção: ferramenta de controle do computador não conseguiu confirmar a URL da janela Brave e encerrou o uso do navegador nesta rodada. Não contornar com outra tecnologia de automação. Ao retomar, verificar disponibilidade normal da ferramenta.

## Ensaio comprovado em 2026-11-09

Fonte: kubectl, Grafana, PagerDuty, Slack e execução GitHub, observados durante a sessão.

| Evento | UTC | America/Sao_Paulo |
|---|---|---|
| POST /admin/fault enabled=true confirmado | 18:57:23 | 15:57:23 |
| Grafana Firing | 18:59:20 | 15:59:20 |
| Notificação Grafana/Slack e incidente PD | 18:59:30 | 15:59:30 |
| Restart automático flag-service | 18:59:39 | 15:59:39 |
| Rollout concluído | 19:00:03 | 16:00:03 |
| Tráfego novamente HTTP 200 observado | 19:00:19 | 16:00:19 |
| Notificação Resolved | 19:01:30 | 16:01:30 |

- Execução automática por `repository_dispatch`, sucesso em 43 s: https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42679005683
- Log real: `deployment.apps/flag-service restarted`; `deployment "flag-service" successfully rolled out`; `Self-healing concluido: flag-service reiniciado e com o rollout completo.`
- Pod recuperado: flag-service-6db59df5bb-d59w8. Sem restart manual nem recuperação manual.
- PagerDuty incidente #4, resolvido, duração exibida 2 min. A falha NÃO ficou ativa. Cooldown do restart de 10 min; nova falha não é necessária só para retomar.
- Dois nós Ready e seis Applications Synced/Healthy foram confirmados antes do ensaio.
- Trace New Relic `2ad625552c9917f6aa53c27567f49835`, 18:28:05 UTC: 19 spans, 56,63 ms, cinco serviços presentes nos spans. Service Map global com cinco serviços ainda não teve enquadramento conclusivo; não confundir com o mapa do trace.

## Capturas existentes

Em `docs/evidencias/2026-11-09/`: Grafana requisições e recursos/Loki; trace mapa e spans; ChatOps Resolved; resumo e log do self-healing; ArgoCD; Lens; Firing; PagerDuty resolvido. `04-self-healing-log.png` mostra a ação corretiva real. `03-chatops.png` mostra mensagem Resolved do incidente das 18:59:20 UTC; é evidência ChatOps autêntica, mas uma captura Firing completa seria complementar útil. Lens tem coluna direita cortada; opcional, não usar como única prova de Ready.

## Artefatos em revisão

- `docs/gravacao/README.md`: roteiro de 10 cenas, cerca de 21 min, falas completas, telas e critérios.
- `docs/gravacao/COMANDOS.md`: comandos Git Bash, trace sem cache e falha controlada sem revelar CHAVE.
- `docs/gravacao/roteiro-conteudo.json`: fonte compartilhada do roteiro.
- `docs/gravacao/ROTEIRO_GRAVACAO_2026-11-09_v01.pdf`: 13 páginas, gerado/renderizado; revisão visual ainda pendente.
- `docs/gravacao/ROTEIRO_GRAVACAO_2026-11-09_v02.pptx`: 13 slides, validação estrutural/layout/fontes aprovada. Slides 1–7 revisados visualmente; faltam 8–13. v01 tem números quebrados e deve ir para arquivo morto antes de entregar.
- `docs/relatorio/RELATORIO_ENTREGA_2026-11-09_v01.pdf`: rascunho desatualizado, anterior ao ensaio; regenerar v02 com participantes, quatro prints e resultado real. NÃO apresentar como relatório final.
- `docs/relatorio/dados-entrega.json`: identificação dos cinco participantes já preenchida conforme README Fase 3 linhas 445–451. Vídeo ainda pendente, manter explícito.
- `docs/evidencias/entrada-local/LEIA-ME.md`: pasta para prints adicionais, arquivos locais ignorados até revisão.
- README reorganizado; `docs/CI-CD.md` e `docs/CONCEITOS_OBSERVABILIDADE.md` criados. Onze workflows com emojis e comentários; preservar IDs/jobs/triggers/permissões.

## Próximas ações, nesta ordem

1. Corrigir bug real descoberto: `gitops/observability/grafana/alerting/rules.yaml` usa `$$values` na annotation summary. Grafana não interpola env em annotations: usar `$values`. Corrigir comentários em rules/templates e adicionar regressão no checker. Fonte oficial: https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/ (exceções annotations, query models, templates). Bug afetou texto, não detecção/automação. Preservar capturas autênticas, explicar correção no relatório. Não mudar contact point com variáveis de ambiente.
2. Considerar `max: 1` no painel 2 de taxa de erro do dashboard, evitando escala automática 10000% quando zerado. Não alterar queries/limiar.
3. Atualizar README com ensaio comprovado e fontes. Criar índices de evidências/relatório e legendas com horários. Regenerar relatório v02 com todos os prints e identificação, usar `04-self-healing-log.png`. Vídeo é a pendência de submissão restante, além de revisão documental.
4. Revisar slides 8–13 e TODAS as páginas PDF renderizadas. Arquivar v01 do PPTX e relatório (não excluir silenciosamente). Preservar geradores úteis numa pasta de trabalho versionável.
5. Validar links, YAML, equivalência semântica dos workflows (exceto nomes), checker Grafana e regressão, self-healing, security-check e renders GitOps. Revisar segredos no diff/staging; nunca git add -A indiscriminado.
6. Commit curado dev, push, PR main; anexar PR ao chat via attach_artifact. Aguardar CI, corrigir falhas, merge sem bypass e sem excluir dev. Acompanhar publicação e ArgoCD; sincronizar dev com main após tags automáticas. Atualizar LOG/PENDENCIAS/DOSSIE/DECISOES no fechamento.

## Geradores e runtime

Trabalho privado ignorado: `00_COLAB_IA/02_TRABALHO/validacao-local-gravacao-2026-11-09/` contém `build_deck.mjs`, `build_pdf.py`, `conteudo.py`, renders `slides/1.png` a `13.png`, `pdf-roteiro/`, `pdf-relatorio/` e recibo `pptx-validation.json`. NÃO rodar conteudo.py cegamente: JSON recebeu correção posterior para evitar cache por flag, não por user_id. Ajustar gerador antes de preservá-lo.

Runtime: `C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/`; Node em node/bin/node.exe, Python em python/python.exe; módulos em node/node_modules. `RUNTIME_NODE_MODULES` aponta para esses módulos. PPTX foi criado com artifact-tool e validado, não usar python-pptx. Markers das skills PDF (2) e PPTX (1) já executados; não repetir nesta produção. Usar pdftoppm para revisão PDF.

Teste do handoff: este documento + topo do LOG + checklist de PENDENCIAS especificam os arquivos vigentes, evidências, limitações e próximos passos sem nova entrevista.
