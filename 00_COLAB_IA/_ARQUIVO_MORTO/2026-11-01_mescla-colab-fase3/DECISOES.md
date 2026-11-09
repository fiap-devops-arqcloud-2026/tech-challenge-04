# Decisões

TL;DR: fontes imutáveis, auxiliares na colaboração, requisitos rastreáveis ao enunciado; guias por dossiê → fragmento → verificação → validação (D-003 a D-005).

Última atualização: 2026-10-27, Codex.

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

## D-011 — Avaliar nuvem com trabalho local primeiro (proposta, 2026-10-13, Codex)

Contexto: usuário declarou crédito AWS esgotado e cogita Azure. Não há implementação Fase4 no 04; o código anterior usa AWS SQS/DynamoDB, Terraform, IAM e ECR. Prazo registrado 2026-11-17.

Proposta: desenvolver a instrumentação local reaproveitável antes de consumir crédito; comparar sessões curtas AWS pagas com Azure elegível. AKS Free é candidato, sujeito a cotas/orçamento e esclarecimento Q-01. Ofertas verificadas e diferenças técnicas constam da auditoria de 2026-10-13.

Alternativas: migrar integralmente de imediato (maior retrabalho em infraestrutura e dois serviços); solução híbrida (menos reescrita inicial, porém duas contas e autenticação/cobrança distribuídas). Sem escolha de provedor aprovada ou implantação executada.

Status: proposta de recomendação, aguardando decisão do usuário em P-003; não substitui D-009 automaticamente.

## D-012 — Continuar na AWS (decidida pelo usuário, 2026-10-20)

Contexto: após avaliar Azure, usuário informou que pretende criar outra conta AWS para continuar no mesmo provedor.

Decisão: manter AWS; não executar migração Azure. A intenção de criar conta não comprova sua existência, crédito nem elegibilidade. A FAQ e os termos oficiais, verificados em 2026-10-20, excluem cliente que já possuiu conta do novo Free plan/crédito e benefícios adicionais por criar mais contas. Orçamento não deve pressupor esse benefício.

Alternativas: Azure foi avaliada em 2026-10-13 e não escolhida. Recomendação de desenvolver localmente antes do cluster continua útil. P-003 agora trata de conta/cotas/orçamento.

## D-013 — Importação por merge dos históricos (proposta, 2026-10-20, Codex)

Contexto: D-009 já preferiu histórico preservado; repo04 já possui materiais próprios. Em 2026-10-20 Fase3 main/dev=6100879, limpa; 04 dev=9696185/main=003a707, com novos arquivos não rastreados. Árvores sem colisões exatas.

Proposta: checkpoint revisado do 04, branch de importação e merge da base 6100879 com --allow-unrelated-histories. Preservar ambos históricos, os materiais do 04 e a Fase3. Adaptar referências de repo/conta e validar antes de publicar. Não transportar estado/segredos/caches locais.

Alternativas: cópia perde ancestralidade; fork exige reincorporar o histórico/documentos do 04; subtree em subpasta muda caminhos operacionais sem necessidade. Plano em 02_TRABALHO/PLANO_IMPORTACAO_FASE3_2026-10-20_v01.md.

Status: recomendação, não executada. Usuário perguntou a melhor opção; não houve autorização nova para commit/push.

## D-014 — Importação autorizada e integrada na dev (concluída, 2026-10-20)

Contexto: usuário autorizou explicitamente importar o código, manter os materiais04, criar a branch exata import-fase3 e fazer merge local para dev, ajustar README/CI/ArgoCD e atualizar memória/contexto. PR/main foram expressamente adiados; a contaAWS nova ainda será informada.

Decisão executada: checkpoint4c76a2d; merge491cd2b com segundo pai6100879 (histórico03); adaptação31f92e4; mergecb81b00 emdev. Branchimport preservada; main04=003a707 e Fase3=6100879 intactas. Sem push/PR/deploy. As permissões anteriores limitadas aos estudos foram ampliadas somente para a execução autorizada; não pedir novamente a autorização já dada.

Por quê: preserva o histórico de ambos repositórios e os caminhos operacionais. Documentos e fontes04 intactos; documentos operacionais antigos mantidos como históricos com aviso. Estado/backend da conta antiga não foi transferido.

Configuração: AWS por repositoryvars; expected_aws_account_id obrigatório; chaves S3 phase4/prod; Argo/OIDC repo04, main como destino futuro. Sentinelas tornam explícito o runtime pendente. Não implementar observabilidade durante a importação.

Alternativas: cópia simples e fork/subtree descartados pela D-013. D-013 deixou de ser mera proposta com a autorização desta sessão; esta ADR registra o resultado.

Validação: verificações locais e revisão independente aprovadas; único P2 (validador incluindo guias03) corrigido por seleção baseada no inventário04. Teste integrado Docker não executado por indisponibilidade da engine; P-005. Nenhuma execução do CIremoto foi alegada.

## D-015 — Consolidar explicações e arquitetura planejada no README (aplicada, 2026-10-22)

Contexto: usuário perguntou se as explicações da conversa e as tecnologias/arquitetura estavam documentadas no README. O arquivo enumerava a stack e o estado da importação, mas tinha apenas o diagrama de CI/CD; os detalhes didáticos estavam na conversa, LOG, guias e plano.

Decisão editorial: ampliar o README principal com métricas/logs/traces, responsabilidades e localização das ferramentas, conceitos de Kubernetes, distribuição condicional dos Collectors e diagramas separados de telemetria, resposta a incidentes e publicação. Vincular o plano, a conferência de cobertura, backlog e fontes oficiais. Preservar a documentação técnica da Fase 3 como histórica.

Por quê: permite compreender as escolhas e o desenho do projeto a partir do README, mantendo explícita a instrumentação/implantação pendente. Três workers continuam proposta e o gateway continua sem réplicas fixadas; os exemplos de quatro/cinco pods não são decisão de capacidade. D-009, D-012 e D-014 permanecem vigentes.

Alternativas: deixar as explicações somente no chat/LOG dificulta a retomada; substituir o documento histórico apagaria o contexto da entrega anterior. Versões anteriores preservadas em `_ARQUIVO_MORTO/2026-10-22_readme-observabilidade/`.

Status: texto e três diagramas revisados; 21 links locais aprovados; sem alteração de código, arquitetura escolhida, estado da AWS ou branch. Sem commit, publicação ou implantação.

## D-016 — Instrumentação local antes do APM externo (aplicada em 2026-10-27; autorizada em 2026-10-22)

Contexto: após o relatório Terraform/backend, usuário autorizou o ensaio local (passo1) e a instrumentação (passo2). Confirmou não ter conta New Relic e escolheu validar localmente primeiro. Baseline aprovado antes de alterar os serviços.

Decisão: opt-in por endpoint OTLP/HTTP, SDK Go/Python, service.name por aplicação, contexto W3C HTTP e atributos SQS sem alterar JSON de negócio. Collector contrib local fixado por versão/digest, memory_limiter, exclusão health, allowlist de atributos e limpeza de detalhes de erro antes da saída arquivo/debug. Logs JSON correlacionados no stdout; coleta de logs e métricas permanecem na etapa E3. Sem exporter New Relic ou credenciais reais.

Por quê: comprova integração/contexto sem consumir recursos AWS e deixa a dependência de conta APM explícita. Dependências fixadas e compatíveis com Go1.25/Python3.12 dos Dockerfiles; spans manuais SQS/Dynamo evitam duplicar autoinstrumentação. Não pressupor que versão latest seja compatível com a base.

Alternativas: aguardar contas impediria validação local; enviar direto ao APM não foi escolhido pelo usuário. A arquitetura futura D-009/D-015 permanece vigente, sem implantação de agents/gateway Kubernetes nesta execução. Estado: instrumentação/testes locais aprovados em 2026-10-27, com 19 spans/5 serviços e SQL dos três serviços. RealDictCursor definido no connect/pool evita substituir a factory instrumentada no cursor. Prova antiga de 17 spans passou a ser rejeitada pelo gate SQL. Evidências em P-008 e relatório do passo2; New Relic segue pendente.

Verificação final da D-016: 13 testes Go principais + oito subtestes e 20 Python nas imagens; regressão funcional; árvore HTTP/SQS/SQL e privacidade aprovadas. 28 fontes estáveis no build/teste final; 39 materiais protegidos intactos e 33 exclusões anteriores mantidas. Laboratório identificado encerrado. O verificador de padrões foi corrigido para ignorar somente cópias dele próprio no arquivo morto, evitando autorreferência; não é uma auditoria de segurança completa.
