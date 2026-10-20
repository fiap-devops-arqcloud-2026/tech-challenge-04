# Verificação final dos guias — 2026-09-21

TL;DR: 72 blocos de código e 253 referências de página conferidos; 3 âncoras incoerentes corrigidas; nenhuma informação inventada encontrada. Validação estática sem erros nos cinco guias e no README.

Última atualização: 2026-09-21, Claude (Opus 5).

## Por que foi feita assim

Três tentativas de verificação com subagentes foram interrompidas por limite de uso da conta (2026-09-16, 2026-09-20 e 2026-09-21), sem gravar arquivos. A verificação foi então executada no laço principal, combinando checagem automatizada de tudo com conferência manual por amostragem dirigida (D-007).

## 1. Fidelidade dos blocos de código (automatizada, cobertura total)

`conferir-codigo-2026-09-21_v01.py` extrai os tokens distintivos de cada bloco `<pre><code>` dos fragmentos de APM e Incidentes e mede quantos aparecem na extração PDFium da aula correspondente. Baixa cobertura sinaliza código que não veio daquela aula.

| Resultado | Blocos |
|---|---|
| Conferidos | 72 |
| Cobertura ≥ 80% dos tokens na extração da própria aula | 63 |
| Abaixo de 80% | 9 |

Os 9 sinalizados são todos blocos transcritos **de figuras** — cujo texto, por ser imagem, não existe na extração: configuração do Serilog, message templates, JSON resultante, middleware `LogContext` e log de falha (Aula 3, Figuras 8 a 12); `conf.yaml` de tail e anotação do Kubernetes (Aula 3, Figuras 3 e 4); cabeçalhos de propagação (Aula 5, Figura 6); exemplo de máscara de dados (Aula 5, Figura 10). Todos foram conferidos nas páginas renderizadas no momento da escrita. Nenhum bloco dos fragmentos escritos por subagentes (Aulas 7, 8 e 9) nem do módulo de Incidentes ficou abaixo do limiar.

## 2. Referências de página (automatizada, cobertura total)

Para cada link `...pdf#page=N` com texto "p. X", verificou-se se N corresponde à primeira página citada.

| Guia | Links com página | Incoerentes |
|---|---|---|
| Observabilidade e Monitoramento | 16 | 0 |
| Monitoramento Opensource | 29 | 0 |
| APM | 162 | 3 → corrigidos |
| Automação de incidentes | 46 | 0 |

As três incoerências estavam no fragmento `08-aula-07.html` (escrito por subagente): o link abria a última página do intervalo em vez da primeira. Corrigidas no fragmento e o guia foi remontado.

## 3. Amostragem dirigida de afirmações (manual)

Conferidas diretamente na extração das aulas, priorizando o material que não foi escrito no laço principal:

| Afirmação do guia | Fonte | Resultado |
|---|---|---|
| `SystemSample` coletado a cada 5 segundos | Aula 7, p. 21 | Confere |
| `ContainerSample` gerado a cada 15 segundos | Aula 7 | Confere |
| Comando `sudo apt-get install -y dotnet-sdk-6.0` | Aula 7 | Confere, literal |
| APM-A07-Q03: repositório usa codinome `focal` com pré-requisito Ubuntu 22.04 | Aula 7 | Achado confirmado |
| APM-A07-Q02: texto anuncia busca por pacote instalado, consulta filtra `ambiente` sobre `SystemSample` | Aula 7 | Achado confirmado |
| Entry span e exit span, definições | Aula 8 | Confere |
| W3C Trace Context recomendado | Aula 8 | Confere |
| APM-I03: Infinite Tracing “nunca sejam perdidos” com 100% dos spans enviados | Aula 8 | Achado confirmado |
| NRQL: apenas `SELECT` e `FROM` obrigatórias; limite de 4 KB; nomes sensíveis a maiúsculas | Aula 9 | Confere |
| APM-A09-Q01: parágrafo de cláusulas opcionais duplicado | Aula 9 | Achado confirmado |
| Código Python de coleta de diagnóstico (Camada 1) | Incidentes, Aula 6, p. 5 | Confere com a página renderizada, inclusive indentação |
| Código Fonte 1 (YAML Prometheus) completo | Observabilidade, Aula 4, p. 10 | Confere com a imagem; F-004 resolvido |

## 4. Verificações estruturais (automatizadas)

- `validar-guias-2026-09-16_v01.py`: 0 erros nos cinco guias e no README — estrutura HTML, âncoras internas, links de arquivo, IDs de requisito existentes, código escapado, ausência de mojibake, de marcadores de rascunho e de dados pessoais.
- Integridade das fontes: 32 PDFs conferidos por SHA-256 contra o inventário — todos intactos.
- Responsividade estrutural: 113 tabelas, todas dentro de `.tablewrap`; nenhuma largura fixa em px; `meta viewport` e 9 media queries em cada arquivo; `pre` com rolagem própria.
- Privacidade: nenhuma ocorrência de nome, e-mail ou RM do titular nos guias ou fragmentos.

## 5. Limites desta verificação

- É por amostragem dirigida, não exaustiva: não foi reconferida cada frase dos 391 KB do guia de APM nem dos demais.
- A revisão visual no navegador não pôde ser repetida nesta sessão (`file://` passou a ser recusado no painel). A checagem de renderização feita em 2026-09-16 no guia de Opensource não apresentou rolagem horizontal a 1280 px; os guias novos usam a mesma base CSS e os mesmos componentes.
- Os achados `[INCERTO]` registrados nos guias descrevem problemas do material didático; não foram comunicados à FIAP nem corrigidos no conteúdo original.
