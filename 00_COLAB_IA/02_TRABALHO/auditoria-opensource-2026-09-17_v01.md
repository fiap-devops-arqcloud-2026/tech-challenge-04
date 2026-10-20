# Auditoria do guia — Monitoramento Opensource

TL;DR: B3 auditado contra os oito PDFs locais (118 páginas); HTML regenerado com metadados de 2026-09-17 e validação estática sem erros. Cinco incertezas documentais mantidas. Revisão visual desktop/mobile será feita pelo agente principal no lote final.

Última atualização: 2026-09-17 11:45 -03:00, Codex.

## Escopo e evidência

Retomada conforme LEIA-PRIMEIRO, LOG, PENDENCIAS e decisões D-003/D-005. O guia existente, gerado em 2026-09-16 pelo fluxo de Claude a partir do script Codex v01, não tinha registro de auditoria. Esta passagem confrontou a síntese, os exemplos, a classificação documental e as referências com as fontes já lidas integralmente em 2026-09-16; conferência em 2026-09-17.

Fontes: `docs/aulas-fiap/02.Monitoramento Opensource/POSTECH - Monitoramento Opensource - Aula N.pdf`, N=1–8. Contagens: 15+14+13+14+16+16+15+15 = 118 páginas. Extrações recuperadas por PDFium, IDs 07–14 em `extracoes-pdfium`. O problema inicial estava no modo layout do extrator, não na inexistência de texto das aulas.

## Resultado por aula

| Aula | Conteúdo conferido | Páginas principais | Resultado |
|---|---|---|---|
| 1 — Zabbix | Host/item/trigger/event/action/template; Server, Agent, Proxy, banco; retenção, histerese, segurança | 5–10 | Fiel. V02 acrescenta distinção polling/trapping já presente na p. 7. Zabbix não apresentado como exigência do desafio. |
| 2 — Prometheus | Scrape, séries temporais, exporters, Pushgateway, Alertmanager; PromQL, tipos, cardinalidade | 5–9 | Fiel. Range query separado de range vector; nenhuma query PromQL inventada. |
| 3 — Grafana | Fontes, painéis, consultas, transformações, variáveis, alertas, organização | 5–8 | Fiel. Distinção entre visualização e armazenamento e proposta de dashboard estão rotuladas como Complemento. |
| 4 — Loki | Labels, streams, chunks, LogQL, caminhos de escrita/leitura e correlação | 5–9 | Fiel. Consulta LogQL preservada exatamente; incoerência do Hands On p. 4 mantida como OS-Q01. |
| 5 — Jaeger | Trace/span, contexto, arquitetura, papéis descritos, sampling, privacidade | 5–11 | Fiel. Exemplo 2,5 s/2,2 s identificado como ilustrativo. Sem completar os dois papéis não descritos; Jaeger não substitui APM exigido. |
| 6 — OTel/Alloy | API, SDK, Collector, receivers/processors/exporters; tipos de sinal; amostragem e proteção | 5–11 | Fiel. V02 explicita eventos associados ao span, conforme p. 7. Centralização obrigatória e Alloy opcional separados. |
| 7 — Kubernetes | Pod, Service, Deployment, Node, plano de controle, reconciliação | 5–10 | Fiel. Texto amplo sobre API Server limitado ao controle; automação de incidente separada da reconciliação nativa. |
| 8 — Integração | Arquitetura conjunta, descoberta, labels, propagação e configuração como código | 5–10 | Fiel. Proposta de investigação do ToggleMaster rotulada como Complemento, sem alegar implantação. |

Capas, sumários, introduções, Hands On, fechamento, referências, palavras-chave e páginas finais dos oito PDFs também foram lidos. Lista precisa de visuais efetivamente inspecionados consta na cobertura v02. Não há código de instalação nos PDFs; as p. 4 remetem às videoaulas. Nenhum comando, YAML ou versão de software foi fabricado para preencher essa ausência.

## Mudanças aplicadas

1. Cabeçalho e rodapé usam `guia_base.AGENTE`, `DATA` e `REVISAO`: autoria inicial Codex em 2026-09-16; geração/revisão Codex em 2026-09-17. Referências distinguem leitura integral de conferência.
2. Aula 1: repostas passivas/ativas de coleta descritas como busca periódica (polling) e recepção ativa (trapping), seguindo a p. 7. Não foram criados procedimentos de configuração.
3. Aula 6: breve explicação de eventos associados ao span, seguindo a p. 7.
4. Mantidas cinco incertezas distintas e três limitações, com referências e tratamento editorial explícitos. Não houve novo requisito nem alteração do README.

## De/para e preservação

| Origem | Arquivo preservado | Nova versão vigente |
|---|---|---|
| `docs/aulas-fiap/02.Monitoramento Opensource/GUIA-ESTUDO-Monitoramento-Opensource.html` | `00_COLAB_IA/_ARQUIVO_MORTO/GUIA-ESTUDO-Monitoramento-Opensource-2026-09-16_v01.html` | Mesmo caminho de HTML, regenerado pelo script v02 |
| `02_TRABALHO/criar-guia-opensource-2026-09-16_v01.py` | Mantido integralmente no mesmo caminho | `02_TRABALHO/criar-guia-opensource-2026-09-17_v02.py` |
| `02_TRABALHO/cobertura-opensource-2026-09-16_v01.md` | Mantido integralmente no mesmo caminho | `02_TRABALHO/cobertura-opensource-2026-09-17_v02.md` |

O movimento do HTML usou caminhos absolutos resolvidos e conferidos dentro do projeto, sem sobrescrever arquivo já arquivado.

- SHA-256 do HTML anterior: `40d1c15a17902eb2ca11af3a9969731e2f22e9de13712f803dae5342bd5855d6`.
- SHA-256 do HTML auditado nesta passagem: `472ca512843b8fa78a16153dc4f0dab22bbe36edbfb919f75adc5e98cc8193f1`.
- Tamanho do HTML auditado: 75.878 bytes.
- SHA-256 de todos os oito PDFs comparado com o inventário inicial: **8/8 intactos**.

## Validação

Ferramenta: `validar-guias-2026-09-16_v01.py`, aplicada antes e depois da revisão, somente ao guia B3. Resultado final: **0 erros e 0 avisos**.

Conferidos: UTF-8 e `lang=pt-BR`; estrutura/aninhamento; 15 seções não vazias; sumário correspondente; âncoras internas; existência dos arquivos apontados; referências `#page` dentro da contagem dos PDFs; IDs existentes na matriz; código escapado; ausência de placeholders, mojibake e dados pessoais no HTML; nenhuma dependência externa.

- 26 IDs distintos: 21 REQ-OBR, 2 REQ-BON e 3 SUG.
- 10 blocos rotulados Complemento.
- 1 bloco de código: `{app="api", env="production"} |= "error"`, igualdade literal confirmada no HTML decodificado e na Aula 4, p. 6.
- 0 links externos e 0 recursos externos.
- 5 incertezas documentais distintas: OS-Q01, OS-Q02, OS-Q03, OS-Q04 e OS-Q05.
- 3 limitações: OS-L01, OS-L02 e OS-L03; não contadas como novas dúvidas.

Detalhes e hashes por fonte: `qa-opensource/validacao-estatica-2026-09-17_v01.json`.

Limite desta passagem: sem execução de comandos de aulas, implantação, acesso a links de mercado ou verificação de comportamento de produtos externos. O navegador desktop/mobile está sob responsabilidade do agente principal, conforme coordenação. A abertura local de links Markdown não navega às âncoras; o agente principal está preparando espelho HTML dos requisitos. Caso altere `guia_base.py` para esse espelho, regenerar com v02 e repetir validação/QA do arquivo final; o hash acima identifica esta passagem anterior a essa possível mudança.

## Handoff

B3 está pronto para QA visual central. Não marcar a etapa como integralmente revisada antes dessa QA. Usar o script `criar-guia-opensource-2026-09-17_v02.py` para futura regeneração. Não alterar fontes originais, base/CSS ou documentos centrais como parte desta subtarefa. Agente principal deve transcrever o de/para e o resultado no LOG, atualizar o checklist e agregar as cinco dúvidas ao total final.
