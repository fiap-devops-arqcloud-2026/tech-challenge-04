# Cobertura do módulo APM

TL;DR: leitura/autoria em andamento; o corpo dos PDFs foi recuperado com PDFium após a falha da extração inicial em modo layout. Não é correto chamar os PDFs inteiramente rasterizados.

Última atualização: 2026-09-16 15:41 -03:00, Codex (agente APM).

## Progresso incremental

- Aulas 1–5: leitura integral do texto recuperado, incluindo capas, referências e páginas institucionais. Falta conferir novamente pequena região truncada das p. 12–13 da Aula 4.
- Aula 1 p. 4: renderização Poppler e inspeção visual concluída, corpo legível.
- Aulas 6–10: leitura pendente.
- Figuras com tabelas/código, autoria do HTML e verificação final: pendentes.

## Notas para continuidade

A1: fundamentos p5–9, componentes Agent p9–13, Linux p14–17, Docker/rede/mounts/Autodiscovery p18–26, métricas e USE p27–30. Código textual p15,19–25; confirmar imagens antes de transcrever.

A2: trace/span p5–12, cardinalidade de recurso p12–14, erro/contexto p14–15, instrumentação .NET p16–19, UST env/service/version p20–23. Figuras p6,10–12 a revisar. A2 p16–27 já lidas no primeiro lote.

A3: ciclo de logs p5–12, JSON/Serilog p12–20 (código em figuras), correlação p20–22, pipelines/facets p23–26, índices/retenção p26–29, sampling p30–35, archive/reidratação/custos p35–39. Figuras p10–18,25,29,32 contêm informação não inteiramente textual.

A4: dashboard p5–14, SLI/SLO/budget/burn rate p14–20, monitores p20–26, Error Tracking p26–31, notificações/Slack/templates p31–37. Fórmulas e exemplos de queries p13–14; não tratar alvos de exemplos como exigência.

A5: AIOps/Watchdog p5–13, RUM/APM p13–18, replay/privacidade p18–24, sintéticos p24–31, AAP p31–38 e SAST/SCA p38–41. Essas extensões não são requisitos do enunciado.

## Incertezas identificadas (numeração provisória)

- APM-I01: A1 p27 descreve `system.cpu.idle` como tempo roubado pelo hypervisor. Não adotar essa equivalência; confirmar com tutor.
- APM-I02: A2 p10 generaliza Trace ID de 64bits; p12 cita W3C128bits. Usar definição por função, registrar contraste.
- APM-I03: A3 p31–32/38 atribui tail sampling ao Agent/Observability Pipelines e garante100% dos erros mesmo em estratégia combinada. Compatibilidade e preservação real não comprovadas; não fornecer configuração inventada.
- APM-I04: A5 p17–18/42 apresenta LCP,FID,CLS como CWV; tratar como vocabulário do material, não lista atual validada.
- APM-I05: A5 p5–7 promete análise100% dos sinais pelo Watchdog. Não transformar alegação abrangente em garantia operacional.
