# Cobertura de leitura — Monitoramento Opensource

TL;DR: 8/8 PDFs e 118 páginas lidos; guia final gerado e auditado, com validação estática aprovada. QA visual desktop/mobile central ainda pendente nesta passagem.

Última atualização: 2026-09-17 11:45 -03:00, Codex. Complementa e preserva `cobertura-opensource-2026-09-16_v01.md`.

## Fontes lidas integralmente

Pasta dos originais: `docs/aulas-fiap/02.Monitoramento Opensource/`.

| Arquivo | Páginas lidas | Visuais revisados por renderização |
|---|---|---|
| POSTECH - Monitoramento Opensource - Aula 1.pdf | 1–15 | 1–8: capa, sumário, introdução, hands-on, ilustração de infraestrutura, tabela e arquitetura |
| POSTECH - Monitoramento Opensource - Aula 2.pdf | 1–14 | 5–8: ecossistema, arquitetura, ilustração de dashboard |
| POSTECH - Monitoramento Opensource - Aula 3.pdf | 1–13 | 5–8: tabela de componentes e arquitetura |
| POSTECH - Monitoramento Opensource - Aula 4.pdf | 1–14 | 5–9: indexação, LogQL, fluxo, arquitetura e ecossistema |
| POSTECH - Monitoramento Opensource - Aula 5.pdf | 1–16 | 5–12: introdução divergente, tracing, cascata, arquitetura, recomendações |
| POSTECH - Monitoramento Opensource - Aula 6.pdf | 1–16 | 5–8: definições, componentes e pipelines |
| POSTECH - Monitoramento Opensource - Aula 7.pdf | 1–15 | 5–9: evolução, objetos e arquitetura do cluster |
| POSTECH - Monitoramento Opensource - Aula 8.pdf | 1–15 | 5–9: pilares, ecossistema, Prometheus, Zabbix e OTel/Alloy |

Incluídas capas, sumários, texto, tabelas, referências, palavras-chave e finais institucionais. Leitura integral em 2026-09-16; auditoria da síntese em 2026-09-17. Extração layout inicial omitia corpo; texto completo recuperado por PDFium. Nenhuma página permaneceu ilegível. Renderizar não é o mesmo que inspecionar: visuais efetivamente vistos são os da tabela, embora todas as páginas tenham sido renderizadas em `qa-opensource/`.

## Dúvidas distintas e limitações

1. **OS-Q01 [INCERTO]** — Aulas 4 e 5 p. 4 usam Hands On de Zabbix; Aula 5 p. 5 inicia com Zabbix. Roteiro correto precisa de confirmação nas videoaulas/tutor.
2. **OS-Q02 [INCERTO]** — Aula 6 p. 4 usa hosts/itens/triggers para OTel/Alloy, em contraste com o corpo sobre APIs e pipelines.
3. **OS-Q03 [INCERTO]** — Aula 5 p. 8 anuncia cinco papéis de Jaeger e descreve três; figura p. 9 mistura agentes/clientes com texto de v2. Dois papéis ausentes não reconstruídos.
4. **OS-Q04 [INCERTO]** — Aula 7 p. 8–9 simplifica runtime e comunicação; guia delimita o plano de controle sem supor versão/integração Docker.
5. **OS-Q05 [INCERTO]** — Aula 5 p. 10 promete captura ampla na amostragem; Aula 6 p. 10 simplifica head-based. Guia explica limites sem prometer garantia.

**OS-L01:** vídeos/transcrições/scripts/YAML citados não foram fornecidos. **OS-L02:** figuras com auxílio de IA são didáticas, sem comprovar execução. **OS-L03:** cases e ganhos de mercado não verificados externamente. Nenhuma dessas limitações impediu ler os PDFs ou foi preenchida por conteúdo inventado.

## Verificação e estado

- [x] Ler os oito PDFs integralmente e inspecionar figuras pertinentes.
- [x] Mapear referências, requisitos e limitações.
- [x] Finalizar script v02 e gerar HTML.
- [x] Auditar fidelidade das oito fichas.
- [x] Validar estrutura, IDs, âncoras, arquivos e código literal (0 erros/avisos).
- [x] Comparar SHA-256 dos 8 PDFs com inventário (8 intactos).
- [ ] Revisar no navegador em desktop/mobile — coordenado pelo agente principal.

Próxima ação: QA visual central; após eventual troca dos links de requisitos para espelho HTML, regenerar v02 e validar novamente. Auditoria detalhada e de/para: `auditoria-opensource-2026-09-17_v01.md`; evidência estática: `qa-opensource/validacao-estatica-2026-09-17_v01.json`.
