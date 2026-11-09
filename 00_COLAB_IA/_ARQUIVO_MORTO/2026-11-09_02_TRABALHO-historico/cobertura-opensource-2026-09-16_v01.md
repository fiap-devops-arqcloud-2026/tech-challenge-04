# Cobertura de leitura — Monitoramento Opensource

TL;DR: 8 PDFs, 118 páginas lidas integralmente; falha de extração layout recuperada com PDFium. Guia em redação, sem execução de comandos.

Última atualização: 2026-09-16 21:25 -03:00, Codex.

## Leitura completa

Todos os nomes abaixo pertencem a `docs/aulas-fiap/02.Monitoramento Opensource/`. Extratos completos oficiais em `00_COLAB_IA/02_TRABALHO/extracoes-pdfium/`, IDs 07–14. Incluídas capas, sumários, texto, tabelas, referências, palavras-chave e páginas finais institucionais.

| Arquivo | Páginas lidas | Visuais revisados por renderização |
|---|---|---|
| POSTECH - Monitoramento Opensource - Aula 1.pdf | 1–15 | 1–8: capa, sumário, introdução, hands-on, ilustração de infraestrutura, tabela de conceitos, arquitetura |
| POSTECH - Monitoramento Opensource - Aula 2.pdf | 1–14 | 5–8: ecossistema, arquitetura, ilustração de dashboard |
| POSTECH - Monitoramento Opensource - Aula 3.pdf | 1–13 | 5–8: tabela de componentes e arquitetura |
| POSTECH - Monitoramento Opensource - Aula 4.pdf | 1–14 | 5–9: comparação de indexação, LogQL, fluxo, arquitetura e ecossistema |
| POSTECH - Monitoramento Opensource - Aula 5.pdf | 1–16 | 5–12: introdução divergente, tracing, cascata, arquitetura, recomendações e referências a cases |
| POSTECH - Monitoramento Opensource - Aula 6.pdf | 1–16 | 5–8: definições, componentes e pipelines |
| POSTECH - Monitoramento Opensource - Aula 7.pdf | 1–15 | 5–9: evolução, objetos, arquitetura do cluster |
| POSTECH - Monitoramento Opensource - Aula 8.pdf | 1–15 | 5–9: pilares, ecossistema, Prometheus, Zabbix e fluxo OTel/Alloy |

Renderizações de todas as páginas foram preservadas em `qa-opensource/aulaNN-PP.png`; grades auxiliares `grade-NN-PP.jpg`. Inspeção visual efetiva é a listada acima; não confundir renderização com leitura visual. Textos completos foram lidos via PDFium, que recuperou conteúdo omitido por extração layout. Nenhuma página permaneceu ilegível.

## Incertezas e limites para o guia

- OS-Q01 [INCERTO]: Aula 4 p. 4 e Aula 5 p. 4 repetem Hands On de Zabbix; Aula 5 p. 5 abre com parágrafo de Zabbix. Contexto das demais páginas identifica Loki e Jaeger, mas o roteiro prático correto não está no PDF. Confirmar nas videoaulas/tutor.
- OS-Q02 [INCERTO]: Aula 6 p. 4 descreve hosts, itens e triggers para OTel/Alloy. Não transformar terminologia possivelmente copiada em procedimento de configuração.
- OS-Q03 [INCERTO]: Aula 5 p. 8 anuncia cinco papéis Jaeger, mas só descreve collector, query e ingester; p. 9 combina diagrama de agentes/clientes com texto sobre v2. Não inventar dois papéis nem manifestos.
- OS-Q04 [INCERTO]: Aula 7 p. 9 diz que toda comunicação passa pelo API Server; contexto é controle do cluster. Não estender ao tráfego de aplicação. Exemplo de Docker como runtime na p. 8 não especifica integração/versão.
- OS-Q05 [INCERTO]: Aula 5 p. 10 associa amostragem adaptativa a captura garantida de todo erro/alta latência; Aula 6 p. 10 simplifica head-based como percentual fixo. Não prometer garantia sem política e cobertura verificadas.
- OS-L01: p. 4 das oito aulas remete a prática em vídeos; vídeos, transcrições, scripts auxiliares e YAML não existem na pasta inventariada. Nenhum foi executado, reconstruído ou consultado externamente.
- OS-L02: imagens dizem ter auxílio de IA; figuras de dashboards/traces são ilustrações didáticas, não evidências de execução. Setas de ecossistema não definem protocolos nem configuração real.
- OS-L03: cases e percentuais apresentados pelas apostilas não foram verificados nos sites; guia os apresenta como referências da aula, sem converter em resultado do projeto.

## Estado incremental

- [x] Ler os oito PDFs integralmente e inspecionar figuras pertinentes.
- [x] Mapear limitações e referências por página.
- [ ] Finalizar script e HTML.
- [ ] Validar HTML, IDs, âncoras, arquivos e código literal.
- [ ] Revisar no navegador em desktop e mobile (coordenação com agente principal).

Próximo passo: terminar `criar-guia-opensource-2026-09-16_v01.py` usando `guia_base.py`, gerar HTML no módulo e validar.
