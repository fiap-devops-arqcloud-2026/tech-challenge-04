# Decisões

TL;DR: fontes imutáveis, auxiliares na colaboração, requisitos rastreáveis ao enunciado; guias por dossiê → fragmento → verificação → validação (D-003 a D-005).

Última atualização: 2026-09-24, Claude (Opus 5.5).

## D-001 — Caminhos e organização (aceita, 2026-09-16)

Contexto: repositório novo; usuário autorizou escrita apenas em áreas específicas.

Decisão: usar `00_COLAB_IA/02_TRABALHO` para scripts, extrações, anotações e QA; não criar CLAUDE.md ou estrutura genérica na raiz. Documentação compartilhada fica em `00_COLAB_IA`.

Alternativas: criar `02_TRABALHO`/CLAUDE.md na raiz exigiria permissão adicional sem ajudar a tarefa.

## D-002 — Evidência e status (aceita, 2026-09-16)

Contexto: a tarefa é estudar e documentar; materiais não provam implantação.

Decisão: status dos requisitos permanece `Pendente`. Usar IDs distintos para obrigação, opção do PDF e sugestão autoral. Checklist histórico da Fase 3 serve apenas de estrutura, sem transportar datas ou resultados.

Alternativas: marcar requisitos concluídos pela existência de guias confundiria documentação com funcionamento real.

## D-003 — Metadados de autoria em `guia_base.py` (aceita, 2026-09-16, Claude)

Contexto: `write_guide` e `complement` gravavam "Codex" fixo; guias produzidos ou revisados por outro agente ficariam com autoria errada.

Decisão: variáveis de módulo `AGENTE`, `DATA` e `REVISAO` com padrões que reproduzem a saída do Codex. Retrocompatibilidade comprovada: regeneração de B1/B2 com o script v01 produziu arquivos byte a byte idênticos (SHA-256). Versão anterior preservada em `_ARQUIVO_MORTO/guia_base-2026-09-16_v01-codex.py`.

Alternativas: duplicar `guia_base.py` para cada agente (divergência de CSS/estrutura) ou editar HTML à mão (perde reprodutibilidade).

## D-004 — Autoria de B4/B5 por fragmentos e validação automática (aceita, 2026-09-16, Claude)

Contexto: APM (335 p.) e Incidentes (142 p.) excedem o que um único agente lê e escreve com fidelidade; o prompt exige código literal, referências por página e HTML válido.

Decisão: (1) um dossiê por aula em `02_TRABALHO/dossies/`, com inspeção visual das páginas com código/figuras; (2) fragmentos HTML por seção montados por `montar-guia-2026-09-16_v01.py`, que reutiliza `guia_base.write_guide` (mesmo cabeçalho, CSS, legenda, sumário e conexão); (3) verificação adversarial de cada fragmento contra a fonte; (4) `validar-guias-2026-09-16_v01.py` para estrutura, âncoras, links, IDs, código escapado, mojibake, placeholders e dados pessoais.

Alternativas: script Python único por módulo, como B2/B3 (arquivo de 100+ KB difícil de revisar e paralelizar).

## D-005 — Auditar B1–B3 antes de marcá-los (aceita, 2026-09-16, Claude)

Contexto: B1–B3 foram gerados sem registro no LOG e sem validação; B2 tem código parcial (F-004).

Decisão: leitor por aula também audita adversarialmente o trecho correspondente do guia; correções serão aplicadas em cópias `_v02` dos scripts geradores, preservando os `_v01`, e o cabeçalho do guia indicará a revisão. README auditado da mesma forma.

## D-006 — Espelho HTML dos requisitos (decidida por Codex em 2026-09-17, implementada por Claude em 2026-09-20)

Contexto: F-007 — abertos por duplo clique, os guias linkavam `README.md#req-obr-NN`, e o navegador mostra o Markdown como texto, sem rolar até a âncora. O Codex decidiu criar um espelho HTML e passou os selos a apontar para `REQUISITOS.html`, mas o arquivo não chegou a ser criado, deixando 13 a 40 links quebrados por guia (F-009).

Decisão: manter o espelho e gerá-lo por script a partir do README (`gerar-espelho-requisitos-2026-09-20_v01.py`), com aviso de arquivo gerado no topo. O Markdown continua sendo a fonte de verdade; o HTML é regerado a cada alteração.

Alternativas: reverter os selos para o Markdown resolveria o link quebrado, mas devolveria o problema de navegação local; manter o espelho editado à mão criaria uma segunda fonte de verdade.

## D-007 — Autoria inline do B4 em vez de subagentes (aceita, 2026-09-21, Claude)

Contexto: duas execuções com subagentes foram interrompidas por limite de uso da conta (32 agentes em 2026-09-16, 12 em 2026-09-20), perdendo ~4 milhões de tokens de leitura. O padrão de falha é o mesmo: o agente lê muito antes de gravar qualquer coisa, e a interrupção apaga tudo.

Decisão: escrever o guia de APM aula a aula, no laço principal, gravando cada fragmento assim que fica pronto. Os três fragmentos que sobreviveram à interrupção (aulas 7, 8 e 9) foram conferidos, validados e aproveitados em vez de refeitos.

Alternativas: insistir em subagentes com prompts menores ainda perderia o trabalho em curso a cada limite; refazer as aulas 7–9 desperdiçaria material correto já gravado.

## D-008 — Coluna "Módulo(s)" derivada da cobertura real (aceita, 2026-09-21, Claude)

Contexto: o README precisava indicar o módulo de cada requisito, e a auditoria propunha um mapeamento manual.

Decisão: derivar por script (`mapear-modulos-readme-2026-09-20_v01.py`) de quem cita cada ID na seção "Conexão com o Tech Challenge Fase 4" de cada guia. Requisito sem nenhum guia citando fica explicitamente como "Fases 1–3 (base anterior)" ou "Entrega (transversal)" — o script falha e avisa se algum ID ficar sem destino, em vez de preencher por suposição.

Alternativas: preencher à mão criaria vínculo que o guia não sustenta e envelheceria a cada revisão.

## D-009 — Ferramentas e repositório da implementação (decidida pelo usuário em 2026-09-23)

Contexto: o plano de implementação dependia de escolhas "uma OU outra" do enunciado e de onde o código mora.

Decisão (respostas diretas do usuário): o código da Fase 3 migra para o `tech-challenge-04` com histórico, deixando a Fase 3 congelada como foi entregue; APM New Relic; ChatOps Slack; self-healing por GitHub Actions via `repository_dispatch`. PagerDuty é imposto pelo mercado: a venda do OpsGenie terminou em 2025-06-04 (F-008). Implementação solo, entrega em 2026-11-17 — data informada pelo usuário; o PDF não a traz (Q-05).

Alternativas: continuar no `tech-challenge-03` (zero migração, mas o CI comita na `main` da Fase 3); Datadog (APM fora do plano gratuito); Discord ou Teams; AWS Lambda ou automação dentro do cluster.

## D-010 — Desenvolver localmente antes de ligar o cluster (recomendação, 2026-09-23)

Contexto: implementação solo, crédito AWS limitado, ambiente único que segue a `main`.

Decisão proposta: instrumentação e trace completo são construídos no Compose de integração da Fase 3, que já emula SQS e DynamoDB com o moto, com um Collector local exportando para o New Relic. O EKS só sobe a partir da semana 4 do calendário.

Alternativas: desenvolver direto no cluster, pagando cada iteração em crédito e em merges na `main`.
