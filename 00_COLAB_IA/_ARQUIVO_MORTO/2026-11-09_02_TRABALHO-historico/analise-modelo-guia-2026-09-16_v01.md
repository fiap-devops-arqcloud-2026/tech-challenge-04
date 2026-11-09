# Análise integral do modelo de guia

TL;DR: preservar a lógica de explicação simples → termos → utilidade → exemplo → projeto, com fichas por aula e visão integrada ao final.

Última atualização: 2026-09-16, Codex.

Fonte lida integralmente: `tech-challenge-03/docs/aulas-fiap/02_CI-CD/GUIA-ESTUDO-CI-CD.html` (32.533 bytes no início da sessão; somente leitura).

## Esqueleto didático

Cabeçalho com contexto e metadados; duas caixas de introdução (conceito e projeto); glossário em duas colunas; sete fichas de aula com “Em miúdos”, “Siglas e termos”, “Para que serve”, “Caso de uso”, “No ToggleMaster”; fluxo de aplicação integrado; tabela de resumo; fontes; rodapé. A progressão reduz siglas antes de exigir compreensão técnica. O vínculo com o projeto explica utilidade, não substitui o conteúdo.

O modelo não possui sumário navegável nem blocos longos de código: eles serão acrescentados porque o pedido atual exige navegação e transcrição fiel quando relevante. Não copiar afirmações de implantação nem tecnologias da Fase 3 como requisitos novos.

## Sistema visual reutilizável

CSS inline, largura máxima 900px, fundo azul-cinza #eef2f8, superfície branca, texto #132339, destaque azul #2f6ae0, destaque de nota âmbar #b26a10. Tema escuro via prefers-color-scheme. Georgia em títulos, Segoe UI/system-ui no texto, Cascadia/Consolas no código. Nenhuma fonte, imagem, biblioteca ou script externo.

Classes reutilizadas: wrap, masthead, eyebrow, meta, intro/box, glossary/term, lessons/lesson, lesson-head/num, badge, facets, flow, tablewrap, note, sources. Tabelas têm rolagem horizontal interna; grades viram coluna abaixo de 600–640px. Há foco visível e respeito a prefers-reduced-motion.

## Adaptações comuns da Fase 4

Base extraída integralmente em `guia-base-2026-09-16_v01.css`, incorporada em cada HTML por `guia_base.py`. Acrescentar sumário, selos textuais com link ao requisito, bloco Complemento, referências por página, código escapado, autoavaliação com respostas e impressão. Fluxos preferem HTML/CSS acessível. Mesma base CSS em todos os guias; nenhuma dependência externa.

A fidelidade prevalece sobre completude aparente: não reconstruir código ilegível; inspecionar páginas renderizadas; rotular erro/incompletude no original como `[INCERTO]`.
