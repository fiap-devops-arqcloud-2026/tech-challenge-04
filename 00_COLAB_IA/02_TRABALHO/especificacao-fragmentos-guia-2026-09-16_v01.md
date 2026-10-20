# Especificação de fragmentos dos guias (B4 APM, B5 Incidentes; também referência para correções de B1–B3)

TL;DR: cada guia é montado por `montar-guia-2026-09-16_v01.py` a partir de fragmentos HTML em `02_TRABALHO/fragmentos/<modulo>/`; cabeçalho, CSS, legenda, sumário e "Conexão" são gerados por `guia_base.write_guide`. Usar somente os componentes abaixo, com o mesmo vocabulário visual de B2/B3 e do modelo CI/CD da Fase 3.

Última atualização: 2026-09-16, Claude (Opus 5).

## 1. Arquivos

| Módulo | Pasta de fragmentos | Pasta do guia | Nome final |
|---|---|---|---|
| B4 | `02_TRABALHO/fragmentos/apm/` | `docs/aulas-fiap/03.APM/` | `GUIA-ESTUDO-APM.html` |
| B5 | `02_TRABALHO/fragmentos/incidentes/` | `docs/aulas-fiap/04.Automação de incidentes/` | `GUIA-ESTUDO-Automacao-de-incidentes.html` |

Cada fragmento: um arquivo `NN-<id>.html` contendo uma ou mais `<section>`; `config.json` e `conexoes.json` na mesma pasta (ver docstring do montador). O id `conexao` é reservado.

## 2. Esqueleto

**B4 — APM (10 aulas; Datadog A1–A5, New Relic A6–A10)**

`00-visao-geral` (visao-geral) → `01-glossario` (glossario) → `02-aula-01` … `11-aula-10` (aula-01 … aula-10) → `12-comparativo` (comparativo: Datadog × New Relic por capacidade) → `13-aplicacao` (aplicacao: da aula à demonstração) → `14-boas-praticas` → `15-outros-modulos` → `16-limites` → `17-revisao`.

**B5 — Automação de incidentes (7 aulas)**

`00-visao-geral` → `01-glossario` → `02-aula-01` … `08-aula-07` → `09-ciclo` (ciclo: detecção → incidente → notificação → runbook → self-healing → pós-incidente) → `10-comparativo` (PagerDuty × OpsGenie; Slack × Teams) → `11-aplicacao` → `12-boas-praticas` → `13-outros-modulos` → `14-limites` → `15-revisao`.

Não criar seção vazia só para cumprir o esqueleto; se um tema não existir nas aulas, omitir e registrar no LOG.

## 3. Componentes (marcação exata)

Seção:
```html
<section id="aula-03"><h2>Aula 3 — Título oficial da aula</h2><div class="section-rule"></div> … </section>
```

Ficha de aula (obrigatória em cada `aula-NN`):
```html
<article class="lesson">
  <div class="lesson-head"><span class="num">03</span><div><h3>Título oficial</h3><span class="badge ok">Essencial no projeto</span></div></div>
  <p><a class="badge obrigatorio" href="../../requisitos/REQUISITOS.html#req-obr-14">OBRIGATÓRIO · REQ-OBR-14</a><a class="badge bonus" href="../../requisitos/REQUISITOS.html#req-bon-02">BÔNUS / OPÇÃO · REQ-BON-02</a><a class="badge sugestao" href="../../requisitos/REQUISITOS.html#sug-03">SUGESTÃO · SUG-03</a></p>
  <dl class="facets">
    <div><dt>Em miúdos</dt><dd>…linguagem de leigo…</dd></div>
    <div><dt>Siglas e termos</dt><dd>…</dd></div>
    <div><dt>Para que serve</dt><dd>…</dd></div>
    <div><dt>Caso de uso</dt><dd class="use">…exemplo da própria aula…</dd></div>
    <div><dt>Na Fase 4</dt><dd class="proj">…vínculo com o enunciado, citando IDs…</dd></div>
  </dl>
  <p class="source">Fonte: <a href="POSTECH%20-%20APM%20-%20Aula%203.pdf#page=3">APM — Aula 3, p. 3–5</a>.</p>
  <h4>Subtópico da aula</h4>
  <p><strong>Em miúdos:</strong> …</p>
  <p><strong>Tecnicamente:</strong> …</p>
  <p class="source">Fonte: <a href="…#page=N">APM — Aula 3, p. N–M</a>.</p>
  … código, tabelas, notas, complementos …
  <p><strong>Para memorizar:</strong> …</p>
</article>
```
Selo de relevância (um por ficha): `badge ok` "Essencial no projeto" ou "Útil no projeto"; `badge warn` "Conhecimento complementar" ou "Evolução futura". Justificar pelo enunciado, não por preferência.

Selos de requisito: formato exato acima; o texto do selo é `OBRIGATÓRIO · REQ-OBR-NN`, `BÔNUS / OPÇÃO · REQ-BON-NN` ou `SUGESTÃO · SUG-NN`; `href` em minúsculas. Usar só IDs existentes no README (41 OBR, 2 BON, 4 SUG) e só com vínculo real.

Fonte por página: `<p class="source">Fonte: <a href="<nome do PDF codificado>#page=<primeira página>">Módulo — Aula N, p. X–Y</a>.</p>` Nomes codificados: `POSTECH%20-%20APM%20-%20Aula%203.pdf`; `POSTECH%20-%20Automacao%20de%20Incidentes%20-%20Aula%203.pdf`. Página física do PDF, a partir de 1. Toda afirmação de conteúdo precisa estar coberta por uma linha de fonte próxima.

Código/comando (literal, conferido na imagem da página):
```html
<figure class="code-example"><figcaption>Código Fonte 2 — APM, Aula 1, p. 19 · transcrição literal conferida na página renderizada</figcaption><pre><code>…texto ESCAPADO…</code></pre><p>O que faz, segundo a aula (p. 19). Linha a linha quando útil.</p></figure>
```
Literal = mesmos tokens, na mesma ordem, com a mesma grafia e indentação lógica. Quebras e espaçamentos produzidos pela diagramação do PDF (texto justificado que separa `-` de `source_labels:`, linha longa quebrada pela largura da página) podem ser normalizados somente quando for inequívoco, e a legenda deve dizer: "quebras de linha causadas pela diagramação do PDF foram normalizadas; tokens preservados". Na dúvida, manter como está e registrar `[INCERTO]`.
Escapar `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` dentro de `<pre><code>`. Para blocos grandes, gerar o escape com Python: salvar o código em arquivo temporário em `02_TRABALHO/tmp-<modulo>/` e usar `html.escape`. Nunca corrigir o código da aula; problema → nota `[INCERTO]`. Placeholders da aula (`<sua-api-key>`) são mantidos escapados. Explicação autoral extra vai em Complemento.

Tabela:
```html
<div class="tablewrap"><table><thead><tr><th scope="col">…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table></div>
```

Glossário:
```html
<div class="glossary"><div class="term"><span class="k">RUM</span><span class="full">Real User Monitoring</span><span class="d">Definição fiel (APM — Aula 5, p. 13).</span></div></div>
```

Caixas de introdução: `<div class="intro"><div class="box"><h3>…</h3><p>…</p></div><div class="box hi"><h3>…</h3><p>…</p></div></div>`

Fluxo: `<ol class="flow"><li><div><strong>Etapa</strong><span>Descrição</span></div></li></ol>`

Incerteza do material: `<aside class="note"><strong>APM-A03-Q01 · [INCERTO] no original</strong>Descrição, páginas e como tratar.</aside>`

Limite/alerta importante: `<aside class="warning"><strong>Título</strong> texto</aside>` (sem `<p>` dentro de `<strong>`).

Complemento (todo conteúdo que não é da aula nem do enunciado):
```html
<aside class="complemento"><strong>📘 Complemento — elaboração didática do Claude (Opus 5)</strong><p>…</p></aside>
```

Autoavaliação: `<details><summary>Pergunta?</summary><p>Resposta. Fonte: APM — Aula 4, p. 16.</p></details>`

Diagrama: preferir `ol.flow` ou tabela. SVG inline só com `role="img"`, `aria-label`, cores `currentColor`/`var(--…)`, `viewBox` e largura responsiva (`width="100%"`).

## 4. Regras de conteúdo

1. Fidelidade: nada inventado; comandos, versões, nomes de produtos e valores exatamente como nas aulas. Afirmação da aula tecnicamente duvidosa → manter atribuída à aula e sinalizar `[INCERTO]`.
2. Explicação simples → técnica em cada tópico relevante; exemplos da própria aula primeiro.
3. Não atribuir à FIAP exigências fora do enunciado; exemplos da aula não são requisitos.
4. Privacidade: nunca transcrever marca d'água com nome/e-mail do titular.
5. HTML válido: nada de bloco (`div`, `table`, `aside`, `ul`, `ol`, `pre`, `figure`) dentro de `<p>`; todas as tags fechadas; ids únicos no guia inteiro (prefixar ids internos com o id da seção, ex.: `aula-03-sampling`).
6. Sem recursos externos (scripts, fontes, imagens remotas). Links externos só se a aula os citar como referência, com `rel="noopener"`.
7. Português do Brasil, acentuação correta, datas ISO.
8. Validar com `python -X utf8 validar-guias-2026-09-16_v01.py <guia>` (Python do runtime Codex) após montar.
