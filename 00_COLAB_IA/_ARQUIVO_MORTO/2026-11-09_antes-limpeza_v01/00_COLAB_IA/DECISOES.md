# Decisões

TL;DR: D-001 a D-020 preservadas. D-021 registra a autorização para atualizar o runtime Alpine dos dois serviços Go; PR/main, implantação e encerramento permanecem separados. A herança F3 é histórica.

Última atualização: 2026-11-05, Codex.

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

## D-017 — Consolidar a memória da Fase 3 e arquivar os originais (aplicada, 2026-11-01)

Contexto: o usuário pediu ao Claude mesclar o conhecimento de docs/00_COLAB_IA nesta pasta e descartar a duplicata; pediu ao Codex continuar após a interrupção. Fonte: LOG de 2026-11-01 (tarde) e pedido direto de retomada.

Decisão: incorporar sínteses revistas, registrar os 59 IDs F3-D/F3-SN e mover os 39 originais, byte a byte, para [_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/). Remover somente a pasta ativa redundante. Preservar rascunhos, extrações, registros antigos e backups; nenhum commit ou push.

Alternativas: manter duas pastas ativas (ambiguidade na retomada); apagar os originais e depender apenas do Git (pior recuperação local). Motivo: uma memória vigente com rastreabilidade completa. As 34 ausências preexistentes fora dessa pasta não fazem parte da autorização de descarte.

Verificação e de-para: [relatório da mescla](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md). Esta decisão não autoriza AWS, publicação Git, correções funcionais ou adoção automática das propostas herdadas.

## D-018 — Referências a assistentes e IDs internos só no diário (aceita pelo usuário, 2026-11-01)

Contexto: a regra pública da Fase 3 divergia do README atual. Após explicação simples, o usuário respondeu: “Sim, deixar essas referências só no diário interno (recomendado)”.

Decisão: na revisão dos documentos públicos, retirar referências ao Codex/Claude e aos IDs internos de decisões/achados/pendências. Manter autoria, cronologia e referências completas em 00_COLAB_IA. Não apagar histórico nem retirar créditos/licenças de terceiros. CLAUDE.md continua como ponteiro interno conforme as instruções globais atuais.

Alternativas: manter anotações de agentes no README (não escolhida). Motivo: documentos para o avaliador explicam o projeto; o diário explica o trabalho entre agentes. Status: política decidida; aplicação aos documentos públicos fica no B6/P-017. Esta mescla não reescreveu README público nem relatórios antigos.

## D-019 — Desenho do B2: falha, cluster, segredos e Slack (aceita pelo usuário, 2026-11-03)

Contexto: quatro escolhas para o B2, apresentadas pelo Claude com recomendação em 2026-11-03. Resposta do usuário: "ok para as 4 recomendações".

Decisão:
1. **Falha proposital:** estado de erro só em memória no flag-service (`POST /admin/fault`), com `/health` saudável. O alerta abre o incidente no PagerDuty e avisa no Slack. O self-healing, um GitHub Actions disparado por `repository_dispatch`, faz `kubectl rollout restart`, e o processo novo nasce sem a falha.
2. **Cluster:** 2 × m7i-flex.large (8 GiB cada), tipo elegível no plano gratuito. Custo e cota de vCPU ficam para conferir no B3.
3. **Segredos no cluster:** o Terraform cria os Secrets do Kubernetes a partir de variáveis sensíveis locais, como na Fase 3 (F3-D-018). Nada é versionado.
4. **Slack pelos dois caminhos:** o cartão do PagerDuty, pelo app conectado ao canal, e a mensagem detalhada do Grafana, pelo Incoming Webhook.

Alternativas descartadas: 3 × c7i-flex.large; Secrets criados à mão; um só caminho até o Slack.

Motivos: memória suficiente para a stack, reprodutibilidade e redundância caso o cartão do PagerDuty falhe. O 4.4 não notificou em 2026-11-03 (ver LOG).

Status: itens 1 e 2 no código em 2026-11-03; o hook da falha aguarda o TODO(human). Itens 3 e 4 ficam no restante do B2. Esta decisão não autoriza apply, envio de eventos reais nem merge na main.

## D-020 — Riscos aceitos antes do B3: senha do PagerDuty e token do ArgoCD (decisão do usuário, 2026-11-05)

Contexto: no fechamento dos pré-requisitos do B3, faltava trocar a senha do PagerDuty, exposta no chat em 2026-11-03. A validação de 2026-11-05 também mostrou que o `GITHUB_ARGOCD_TOKEN` tem Contents: write, quando o guia pedia Read-only.

Decisão:
1. **Senha do PagerDuty mantida.** Resposta do usuário: "Não irei trocar a senha do PD, vamos continuar com essa já estou ciente do risco." Os agentes continuam sem usar a senha e sem registrá-la.
2. **Token do ArgoCD mantido com escrita.** A pergunta recomendava reduzir o token a Read-only, e o usuário respondeu "Manter com escrita".
   - O ArgoCD funciona do mesmo jeito.
   - O token vira Secret no namespace do ArgoCD. Se vazar, permite alterar o repositório.

Alternativas recomendadas e não escolhidas: trocar a senha; reduzir o token a Read-only ou gerar outro só de leitura.

Status: riscos aceitos. Não reabrir como pendência; reavaliar só a pedido do usuário ou com indício de vazamento. Esta decisão não autoriza login com a senha nem amplia permissões.

## D-021 — Atualizar o runtime dos dois serviços Go para Alpine 3.24 (aceita, 2026-11-05)

**Contexto:** o CI do Claude reportou que a base 3.20 dos serviços auth/evaluation perdeu suporte regular. Um scan sem CVE crítico em uma distribuição sem suporte não cobre a falta de novos avisos.

**Decisão do usuário:** “Sim, atualizar os dois Dockerfiles na dev”. Alterar somente a imagem da etapa final dos dois serviços para `alpine:3.24`; conservar o builder e as políticas de scan. A tag acompanha patches do ramo em builds futuros. Alternativa considerada: manter 3.20 até depois da gravação.

**Aplicação e evidência:** commit `df766b2`. As cópias testadas foram comparadas com os Dockerfiles efetivos. Resolveram para 3.24.3; ambos os processos rodaram sem root com CA presente; auth criou/validou chave em PostgreSQL e evaluation fez leituras de Redis. O Trivy 0.70.0 reportou zero achados CRITICAL nas duas imagens sob o filtro e as exceções do CI. Ver [evidência local](02_TRABALHO/validacao-local-alpine-2026-11-05/RESULTADO.md) e [política oficial de suporte do Alpine](https://alpinelinux.org/releases/). Nenhuma publicação no ECR foi feita para esse teste.

## Decisões herdadas da Fase 3 — registro histórico revisado em 2026-11-01

24 decisões numeradas (F3-D-001–024) e 35 decisões sem ID original (F3-SN-01–35). “SN” é classificação da consolidação Claude, não um número dado pelo usuário na época. Fontes abaixo apontam para os originais arquivados, com linhas originais. Datas indicam a decisão histórica; não são datas de nova aprovação.

Os rótulos da extração são preservados para comparação: 23 vigentes, 26 a revisar, 6 superadas e 4 históricas. **“Vigente” significa compatível com o desenho ou processo descrito, não recurso implantado nem autorização para executar comandos.** Havendo ressalva abaixo, ela prevalece sobre o rótulo herdado. A numeração sem F3 é reservada à Fase 4.

### F3-D-001 — Repositório de destino da Fase 3

Contexto/data: Fase 3, 2026-07-17. Status herdado: **superada**.

Decisão histórica: Usar o tech-challenge-03 como destino de contexto, guias e implementações da Fase 3.

Motivo registrado: Pedido do usuário; isolar a Fase 3 da Fase 2.

Alternativas registradas: Editar o tech-challenge-02 diretamente.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 290-298 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 571-581 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 64-66 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 92 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 98-102 do original).

### F3-D-002 — Guias de estudo em Markdown por módulo

Contexto/data: Fase 3, 2026-07-17. Status herdado: **superada**.

Decisão histórica: Guias derivados em docs/guias-de-estudo/fase-2/, um por módulo, em Markdown.

Motivo registrado: Materiais de origem estavam no tech-challenge-02.

Alternativas registradas: Copiar PDFs; pasta única; editar o repositório da Fase 2.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 300-308 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 571-581 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 98-102 do original).

### F3-D-003 — Direção técnica: Terraform modular, GitHub Actions, ECR, ArgoCD e EKS em conta pessoal

Contexto/data: Fase 3, [INCERTO] sem data explícita; registrada entre 2026-07-17 e 2026-07-18. Status herdado: **vigente**.

Decisão histórica: Stack: Terraform modular, GitHub Actions, ECR, ArgoCD e EKS. Conta AWS pessoal (não AWS Academy/LabRole), para criar roles e policies IAM pelo Terraform.

Motivo registrado: O enunciado pede IaC, CI/CD, DevSecOps e GitOps para o ToggleMaster. AWS Academy/LabRole impediria criar IAM por código.

Alternativas registradas: Jenkins; FluxCD; AWS Academy com LabRole; kubectl apply direto no CI.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 320-328 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 100 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 42-44 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 90-92 do original).

### F3-D-004 — Não copiar materiais da fase anterior; usar como fonte externa

Contexto/data: Fase 3, 2026-07-18 (ajuste de formato). Status herdado: **revisar**.

Decisão histórica: Usar PDFs e guias da fase anterior como fonte, sem copiá-los para o repositório da fase seguinte; registrar só sínteses próprias.

Motivo registrado: Evitar duplicar insumos; os materiais ajudam a entender containers, Kubernetes e escalabilidade.

Alternativas registradas: Versionar todo o material da fase anterior no repositório novo.

Aplicação na Fase 4: As 34 ausências de materiais anteriores continuam pendentes; arquivar a colaboração não decide o destino desses outros arquivos.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 330-338 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 571-581 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 98-102 do original).

### F3-D-005 — Guias de estudo HTML, um por módulo

Contexto/data: Fase 3, 2026-07-18. Status herdado: **vigente**.

Decisão histórica: Um guia HTML por vez, salvo na pasta do módulo, com introdução para leigos, glossário, fichas (finalidade, caso de uso, aplicação no ToggleMaster) e resumo. Padrão visual do guia de containers da Fase 2.

Motivo registrado: Os guias Markdown não atenderam; o usuário decidiu estudar por partes.

Alternativas registradas: Manter Markdown; pasta separada; gerar todos de uma vez.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 310-318 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 479 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 563 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 98-102 do original).

### F3-D-006 — Entrega em grupo, prazo 2026-09-15

Contexto/data: Fase 3, 2026-07-30. Status herdado: **superada**.

Decisão histórica: Entrega em grupo, prazo final 2026-09-15, com repositório público.

Motivo registrado: O enunciado diz que o trabalho 'em princípio' é em grupo e pede nomes no relatório, mas não traz prazo; o prazo veio do usuário.

Alternativas registradas: Entrega individual; seguir sem data.

Aplicação na Fase 4: Prazo e grupo são da Fase 3. Na Fase 4 o usuário informou 2026-11-17; a condição individual ainda requer confirmação do tutor.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 280-288 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 11 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 13 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 453-459 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 69 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 103 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 250-251 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 13 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 25 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 126 do original).

### F3-D-007 — Monorepo: serviços, Terraform, GitOps e pipelines no mesmo repositório

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Os 5 microsserviços ficam em services/; infraestrutura em terraform/; manifestos Kustomize em gitops/; pipelines em .github/workflows/. Serviços nomeados <nome>-service, igual ao ECR e ao Kustomize.

Motivo registrado: Os workflows de CI disparam em PR e push; o passo de tag vira commit no próprio repositório, sem token cruzado entre repositórios. O enunciado aceita pasta GitOps no monorepo.

Alternativas registradas: Código em repositório externo; repositório GitOps separado (opcional no enunciado, não adotado).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 268-278 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 24 do original); [ORGANIZACAO_DE_PASTAS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md) (linhas 3 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 441-443 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 70-71 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 104 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 247 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 62 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 102 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 124 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 173 do original); [_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md) (linhas 3 do original); [_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md) (linhas 54 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 86-89 do original).

### F3-D-008 — GitOps com Kustomize (base por serviço, overlay por ambiente)

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Kustomize em gitops/, com base/<serviço> e overlays/<ambiente>. Uma Application do ArgoCD (togglemaster) gerencia os 5 serviços. Helm só para instalar o próprio ArgoCD.

Motivo registrado: Nativo do kubectl e do ArgoCD, sem templating. O CI atualiza a tag com 'kustomize edit set image', mudando um único campo do overlay, fácil de automatizar e auditar.

Alternativas registradas: YAML puro (duplica manifesto por ambiente); Helm Charts próprios (mais complexidade para 5 serviços parecidos); cinco Applications (descartado).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 256-266 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 443 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 105 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 248 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 310-320 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 101 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 125 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 168 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 173 do original); [_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ORGANIZACAO_DE_PASTAS_2026-08-27.md) (linhas 60 do original); [_ARQUIVO_MORTO/EVIDENCIAS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/EVIDENCIAS.md) (linhas 3-5 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 23 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 86 do original).

### F3-D-009 — Tags padrão project=fiap e phase=<fase>, em minúsculas, via default_tags

Contexto/data: Fase 3, 2026-08-27. Status herdado: **revisar**.

Decisão histórica: Todo recurso AWS recebe project = fiap e phase = 3, em minúsculas, uma vez via default_tags no provider. O bucket de estado recebeu as tags à mão. Lifecycle do bucket de estado: versões antigas expiram em 30 dias.

Motivo registrado: Rastrear custo no Cost Explorer (print de custo exigido no relatório). Chave de tag na AWS diferencia maiúsculas: Project e project virariam grupos separados. 30 dias bastam porque o estado é pequeno.

Alternativas registradas: Tags capitalizadas (registradas às 13:10 e corrigidas às 15:55 de 2026-08-27); tag por recurso; lifecycle de 90 dias (descartado pelo grupo).

Aplicação na Fase 4: Na Fase 4 a tag é phase=4. Não reutilizar filtros, contas, states ou lifecycle antigo sem revisar.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 246-254 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 25 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 395 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 419 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 76 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 107 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 431 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 124 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 176-178 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 94-95 do original).

### F3-D-010 — Módulos Terraform híbridos

Contexto/data: Fase 3, 2026-08-27 (nota de estado final em 2026-09-15). Status herdado: **vigente**.

Decisão histórica: Plano inicial: VPC e EKS da comunidade; demais módulos próprios. Estado final: só a VPC vem da comunidade (terraform-aws-modules/vpc/aws ~> 5.0); EKS em módulo próprio, junto com ecr, messaging, iam-ci, rds, elasticache e irsa (7 módulos próprios).

Motivo registrado: EKS do zero é onde projetos perdem dias; os demais recursos são simples e preservam a autoria exigida.

Alternativas registradas: Tudo da comunidade; tudo à mão.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 232-244 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 399 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 108 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 256 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 430 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 131 do original).

### F3-D-011 — Ambiente único chamado prod

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Um único ambiente: overlay gitops/overlays/prod e estados com prefixo prod. Sem overlays dev ou hml.

Motivo registrado: O enunciado não pede vários ambientes; cada ambiente extra multiplica o custo de EKS, RDS e ElastiCache. A estrutura base+overlay permite expandir depois.

Alternativas registradas: dev + prod; dev/staging/prod; overlay único chamado dev.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 220-230 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 381 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 7 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 109 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 262 do original).

### F3-D-012 — Sem Ingress e sem Load Balancer; acesso por kubectl port-forward

Contexto/data: Fase 3, 2026-08-27. Status herdado: **revisar**.

Decisão histórica: Services ClusterIP, sem Ingress nem Load Balancer. ArgoCD (8080:80) e serviços (8001-8004) acessados por port-forward no vídeo.

Motivo registrado: O Ingress da Fase 2 exigiria Nginx Ingress Controller e LB a ~US$ 16-20/mês. A varredura do PDF da Fase 3 (7 páginas, em 2026-08-27) achou zero ocorrências de ingress, load balancer, acesso externo, http, url, endpoint, expor, público, nginx e alb. Também evita LB órfão segurando subnet no destroy.

Alternativas registradas: Manter o Ingress/ALB da Fase 2 (melhor demo, ~US$ 16-20/mês a mais).

Aplicação na Fase 4: Acesso por port-forward é o desenho herdado. Saída para SaaS não implica, por si, obrigação de Ingress. Reavaliar com o fluxo final.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 208-218 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 31-32 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 941 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 33-39 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 719-720 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 110 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 31 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 420 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 317-329 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 471-487 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 608-611 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 19 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 15 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 33-35 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 124-128 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1159-1160 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1170-1174 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1198-1201 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1446-1449 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 224-231 do original).

### F3-D-013 — Segredos via Secrets Manager + External Secrets Operator (ESO)

Contexto/data: Fase 3, 2026-08-27. Status herdado: **superada**.

Decisão histórica: Terraform gera senhas (random_password) e grava no Secrets Manager; o ESO sincronizaria para Secrets do Kubernetes. Chaves estáticas da AWS substituídas por IRSA.

Motivo registrado: Na Fase 2, analytics e evaluation recebiam AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY estáticas num Secret; o enunciado critica credenciais em arquivos sem segurança.

Alternativas registradas: Secret preenchido à mão; SSM Parameter Store; Secrets criados pelo Terraform (adotado depois).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 196-206 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 258 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 377 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 111 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 240-243 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 261 do original).

### F3-D-014 — Manifestos da Fase 2 como base do GitOps

Contexto/data: Fase 3, 2026-08-27. Status herdado: **historica**.

Decisão histórica: gitops/base/ derivado dos 28 manifestos de infra/k8s/ da Fase 2. Quase intactos: namespaces, 5 service.yaml, 2 hpa.yaml. Adaptados: 5 deployment.yaml, secret.yaml, configmap.yaml. Descartado: ingress.yaml. postgres-targeting/ copiado depois (D-015).

Motivo registrado: Probes, resources, selectors e portas já testados na Fase 2; reescrever traria risco sem ganho de nota.

Alternativas registradas: Escrever os manifestos do zero.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 184-194 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 381-383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 411 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 112 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 257 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 259 do original).

### F3-D-015 — Dois RDS e banco do targeting em StatefulSet no EKS (caminho A)

Contexto/data: Fase 3, 2026-08-27. Status herdado: **revisar**.

Decisão histórica: auth_db e flags_db em RDS PostgreSQL 16; targeting_db em StatefulSet postgres-targeting no cluster, com PVC gp3 de 5 GB, reaproveitando os manifestos da Fase 2. P-031 (migrar para RDS) cancelada.

Motivo registrado: O enunciado da Fase 3 exige 3 instâncias RDS, mas o plano gratuito da conta da Fase 3 recusou a terceira ('maximum number of instances available with free plan accounts'). O professor confirmou em 2026-08-27 que o arranjo da Fase 2 seguia aceito. Sair do plano gratuito exigiria pagamento e tiraria a proteção contra gasto, com crédito histórico não reproduzido de crédito restante.

Alternativas registradas: Sair do plano gratuito; 1 RDS com três bancos (não atende '3 instâncias'); 3 RDS literais.

Aplicação na Fase 4: Limites e aceite do professor são relatos da conta/Fase 3; comprovante escrito não localizado. Não transferir a exceção automaticamente à Fase 4.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 170-182 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 28 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 32 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 128 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 260-261 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 314 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 363 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 413 do original); [_ARQUIVO_MORTO/ROTEIRO_VIDEO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ROTEIRO_VIDEO.md) (linhas 6-9 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 378-387 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 940 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 487 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 86 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 252 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 255 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 418 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 32 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 21 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 28 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 103 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 39 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 16-17 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 36-41 do original); [_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md) (linhas 30-31 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1005-1015 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1545 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1579 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 152-160 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 294-295 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 313-316 do original).

### F3-D-016 — Node group com 2 x c7i-flex.large

Contexto/data: Fase 3, 2026-08-27. Status herdado: **revisar**.

Decisão histórica: Node group com c7i-flex.large (2 vCPU / 4 GB), mesmo tipo da Fase 2: mínimo 1, desejado 2, máximo 4. Substituiu, no mesmo dia, a escolha de 2 x t3.medium (medida em F-020).

Motivo registrado: A conta da Fase 3 recusou t3.medium ('not eligible for Free Tier'). c7i-flex.large é equivalente e foi aceito naquele plano. t3.micro comporta ~4 pods e 1 GB; t4g é ARM e as imagens são x86; m7i-flex.large custava mais sem necessidade.

Alternativas registradas: Sair do plano gratuito e usar t3.medium (descartado junto com a D-015).

Aplicação na Fase 4: Dois nós são o padrão no código; o plano menciona três. Dimensionar a stack e orçamento da conta atual antes de implantar.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 156-168 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 395 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 407 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 125-126 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 253 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 427-428 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 432 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 518 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 942 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 119-122 do original); [_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md) (linhas 12-13 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 162-165 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 256 do original).

### F3-D-017 — Terraform em camadas com estados separados (base, cluster, k8s)

Contexto/data: Fase 3, 2026-08-27 (duas camadas); terceira camada k8s desde 2026-09-09; nota em 2026-09-15. Status herdado: **vigente**.

Decisão histórica: Raízes independentes no mesmo bucket: terraform/ (base: VPC, 5 ECR, SQS+DLQ, DynamoDB, role do CI e OIDC), terraform/cluster/ (EKS, node group, 2 RDS, ElastiCache, 2 roles IRSA) e terraform/k8s/ (namespaces, 5 Secrets, StorageClass gp3, ArgoCD e Application). Cada camada lê a anterior por terraform_remote_state; o plan falha se a anterior não existir.

Motivo registrado: Com estado único, o destroy de fim de sessão levaria os ECR e, com force_delete, as imagens; o CI teria de reconstruir as 5. A camada k8s é separada porque seu provider depende do cluster que outra camada cria.

Alternativas registradas: Estado único com destroy -target (frágil); estado único recriando ECR sempre; workspaces (separam ambientes, não ciclo de vida); estrutura antiga terraform/bootstrap e environments/dev (removida).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 138-154 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 257 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 343-353 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 7 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 196-197 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 422 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 9 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 35 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 43 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 98 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 118 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 167 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 97-103 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 46-59 do original); [_ARQUIVO_MORTO/GUIA_EXECUCAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_EXECUCAO.md) (linhas 5-7 do original); [_ARQUIVO_MORTO/GUIA_EXECUCAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_EXECUCAO.md) (linhas 35-38 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 39-49 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 522-549 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 304-318 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 9-15 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 58 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 58-80 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 283-286 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 317-320 do original).

### F3-D-018 — Sem ESO: Terraform cria os Secrets do Kubernetes

Contexto/data: Fase 3, 2026-09-01 (nota em 2026-09-15). Status herdado: **revisar**.

Decisão histórica: Cortar o ESO. A camada terraform/k8s (secrets.tf) cria os Secrets dos serviços que precisam de credenciais e o do postgres-targeting. Senhas dos 2 RDS nascem na camada cluster e também vão ao Secrets Manager. Senha do targeting, MASTER_KEY e SERVICE_API_KEY nascem na k8s e ficam só no Secret e no estado. Contrato de nomes e chaves em gitops/SECRETS-CONTRATO.md.

Motivo registrado: ESO era sugestão das aulas (S-02), não requisito; seria peça nova em runtime no caminho crítico da gravação (chart, role IRSA ou ClusterSecretStore falhando derrubariam os 5 serviços). Prazo de 14 dias na época.

Alternativas registradas: Manter o ESO; Secret versionado no Git (o que o enunciado critica); preencher o Secret à mão após o apply.

Aplicação na Fase 4: O código atual tem cinco recursos de Secret em secrets.tf: auth, flag, targeting, postgres_targeting e evaluation; não são seis nem um Secret para analytics. Novos segredos SaaS ainda precisam de contrato.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 118-136 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 29 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 32 do original); [PENDENCIAS_E_PROXIMOS_PASSOS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md) (linhas 29 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 249 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 258 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 31 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 240-243 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 325-327 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 32 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 83 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 88 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 171 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 113-114 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 127-128 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 149 do original); [_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md) (linhas 18 do original).

### F3-D-019 — Preferência dev -> PR -> main

Contexto/data: Fase 3, 2026-09-09. Status herdado: **superada**.

Decisão histórica: Diretriz: alterações humanas partem da dev e são promovidas por PR; sincronizar a dev com a main antes de retomar. A atualização automática de tag pelo CI precisa de política compatível com eventual proteção da main.

Motivo registrado: Auditoria achou commits posteriores direto na main e a dev 19 commits atrás.

Alternativas registradas: Branches curtas por tarefa convergindo para a dev; commits humanos direto na main.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 97-109 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 314 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 331 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 13 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 31 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 82 do original).

### F3-D-020 — Trabalho humano só na dev; promoção para main por PR

Contexto/data: Fase 3, 2026-09-09. Status herdado: **vigente**.

Decisão histórica: Todo trabalho humano ou de agente parte da dev; a main recebe só por PR dev -> main e merge. Não promover branches auxiliares direto para a main. Após cada merge, conferir e sincronizar a dev sem descartar trabalho. A regra não é, por si, ordem para publicar ou fazer merge.

Motivo registrado: Instrução do usuário; origem única de trabalho, revisão e rastreabilidade. Na dev o pipeline só verifica; quem publica imagem e tag é a main.

Alternativas registradas: PRs de branches auxiliares direto para a main (usados nos PRs 4 e 5); push humano direto na main.

Aplicação na Fase 4: Fluxo humano dev → PR → main preservado. Não constitui autorização de commit/push/PR nesta retomada.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 80-94 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 53-64 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 256 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 265 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 276-288 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 566 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 839-840 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 53-54 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 411-412 do original); [_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md) (linhas 13-15 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 43 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 48 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 293-309 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 10-11 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 83-85 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 128-130 do original); [_ARQUIVO_MORTO/auditoria-2026-09-09/PLANO_AUDITORIA_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/auditoria-2026-09-09/PLANO_AUDITORIA_2026-09-09_v01.md) (linhas 7-8 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 20-22 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 33-41 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 130-132 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 156-169 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 859-898 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 233-239 do original).

### F3-D-021 — Robô do CI continua comitando a tag na main

Contexto/data: Fase 3, 2026-09-09. Status herdado: **revisar**.

Decisão histórica: O último job de _ci-go.yml e _ci-python.yml roda 'kustomize edit set image' no overlay prod e 'git push origin HEAD:main', com [skip ci] e laço de 5 tentativas (fetch/reset/edit/commit/push). A F3-D-020 vale para trabalho humano. A dev é sincronizada com a main no início de cada sessão (git merge --ff-only origin/main).

Motivo registrado: A main é o estado desejado que o ArgoCD observa. O commit de tag é resultado mecânico de um build que já passou por PR e portões de segurança. PR do robô para si criaria fila de aprovação e quebraria a demonstração de sincronização automática.

Alternativas registradas: Robô comitando na dev com PR automático para a main (passo manual no caminho crítico; descartado). Branch gitops-bot observada pelo ArgoCD (duas fontes da verdade; descartado).

Aplicação na Fase 4: Exceção do robô é distinta do fluxo humano. Nunca executar reset --hard do job no checkout de trabalho do usuário.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 61-77 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 30 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 53 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 88 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 265 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 267 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 284 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 24 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 51 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 33-35 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 41 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 167 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 22-25 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 233-239 do original).

### F3-D-022 — Provedor OIDC do GitHub: criar ou reaproveitar o existente (create_github_oidc_provider)

Contexto/data: Fase 3, 2026-09-14 (registro em 2026-09-15). Status herdado: **revisar**.

Decisão histórica: Variável create_github_oidc_provider (padrão true). Com false, um data source só lê o provedor token.actions.githubusercontent.com existente e o Terraform nunca o destrói; a role do CI confia nele do mesmo jeito. Um bloco moved preserva estados antigos. Na conta da Fase 3 o valor era false. Plan da base: 35 recursos com false, 36 com true.

Motivo registrado: A conta da Fase 3 já tinha o provedor, criado por outro projeto pessoal. A AWS aceita um provedor por URL; o apply falharia com EntityAlreadyExists, e o plan não avisa porque compara só com o estado.

Alternativas registradas: terraform import (o destroy apagaria recurso alheio); apagar e recriar (quebra o outro projeto); criar outro provedor (AWS recusa URL duplicada).

Aplicação na Fase 4: Provedor novo já inventariado em 2026-10-28; decidir importação versus data source antes do apply. False não impede destruir um recurso que já esteja gerenciado no estado e seja removido da configuração: revisar o plano.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 45-59 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 67 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 124 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 145 do original); [PENDENCIAS_E_PROXIMOS_PASSOS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md) (linhas 51 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 51 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 83-93 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 483-499 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1491-1494 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1532-1533 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 62 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 86-89 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 772-782 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 869-892 do original).

### F3-D-023 — Ordem de subida e destruição, com planos salvos em arquivo

Contexto/data: Fase 3, 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Subida: base -> imagens publicadas no ECR -> cluster -> aws eks update-kubeconfig -> k8s em duas etapas. Destruição: k8s -> cluster -> base; o destroy da k8s não é opcional. Sempre 'plan -out=<camada>.tfplan' e 'apply <camada>.tfplan' (no destroy, 'plan -destroy -out'); nunca apply interativo. tfvars local por camada para apply e destroy lerem os mesmos valores.

Motivo registrado: A base destruída levou ECR e imagens; aplicar a k8s antes das imagens deixa pods em ImagePullBackOff. Colar bloco com apply interativo fez a linha seguinte virar resposta do 'yes'. Ao apagar o PVC, o driver EBS apaga o disco de 5 GB, que não pertence a estado nenhum.

Alternativas registradas: k8s antes das imagens; destruir só o cluster e deixar a k8s (estado órfão e EBS sem dono); valores por -var em cada comando (fácil esquecer um no destroy).

Aplicação na Fase 4: Plan salvo é prévia, apply salvo executa sem confirmação interativa; revisar e obter a autorização de execução antes. Nenhum destroy foi autorizado por esta retomada.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 29-43 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 50-54 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 76-79 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 47-48 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 219-244 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 430 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 894-908 do original).

### F3-D-024 — Consolidação da documentação pública no estado final da Fase 3

Contexto/data: Fase 3, 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Três documentos públicos sem sobreposição: README (o quê e por quê), docs/GUIA_DE_REPRODUCAO.md (como) e docs/ARQUITETURA.md (referência técnica). Cada fato com detalhe em um único lugar. Documentos públicos não citam IA nem códigos internos; a pasta de colaboração pode. Arquivo morto não é editado. Não editar services/** nem .github/workflows/** (merge rodaria image e gitops, que falhariam no OIDC sem a role). SECURITY.md corrigido: MASTER_KEY e SERVICE_API_KEY são segredos estáticos de aplicação, e a trust do CI aceitava qualquer branch ou PR do repositório.

Motivo registrado: Projeto entregue e ambiente destruído em 2026-09-15; o mesmo fato estava em até cinco lugares; docs/OPERACAO.md tinha 1.636 linhas; havia links quebrados e rastro de assistente no relatório.

Alternativas registradas: Editar variables.tf ou tfvars.example (violaria 'nenhuma mudança de código'); terraform init -backend-config como caminho principal; apagar PNGs da auditoria; editar services/ ou workflows; tirar o sufixo '-an' do bucket.

Aplicação na Fase 4: Trava histórica de services/workflows não anula autorizações posteriores. A regra pública foi confirmada como D-018. Não há autorização genérica de editar qualquer código na dev.

Fontes: [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 3-27 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 19 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 93 do original); [PENDENCIAS_E_PROXIMOS_PASSOS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md) (linhas 29 do original); [PENDENCIAS_E_PROXIMOS_PASSOS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md) (linhas 35-36 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 3-14 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 40 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 44 do original).

### F3-SN-01 — Região us-east-2 (Ohio) em tudo

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Toda a infraestrutura e o bucket de estado em us-east-2, a mesma da Fase 2. Exemplos herdados com us-east-1 estão errados; vale o Terraform.

Motivo registrado: Informação do usuário; a inferência anterior (us-east-1) veio de exemplo errado em README de serviço.

Alternativas registradas: us-east-1 (descartada, era erro).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 429-437 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 434-435 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 33 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 40-42 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 107-111 do original).

### F3-SN-02 — Bucket de estado por bootstrap manual, versionado e protegido

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Criar o bucket do tfstate uma vez, fora do Terraform (console, caminho A), com procedimento documentado. Configuração: versionamento ligado; SSE-S3 (AES256); a menção original a Bucket Key está incorreta; 4 bloqueios de acesso público; ACLs desabilitadas; Object Lock desligado; policy DenyInsecureTransport; lifecycle apagando versões não correntes após 30 dias. É a única exceção à regra 'se não está no código, não existe'.

Motivo registrado: Ovo e galinha: o Terraform precisa do bucket para guardar o próprio estado. O enunciado exige estado remoto em S3. O estado guarda senhas em texto puro; o versionamento recupera estado corrompido; HTTPS obrigatório evita achado clássico de scanner.

Alternativas registradas: Caminho B pela CLI; Apêndice A: criar com Terraform em estado local e migrar com 'terraform init -migrate-state' (evidência de IaC mais forte, com um passo a mais).

Aplicação na Fase 4: Correção: S3 Bucket Key é recurso SSE-KMS, não SSE-S3. Estado pode conter segredos; persistência remota não elimina arquivos locais excepcionais de recuperação. Ver fontes técnicas no relatório.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 417 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 429-437 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 443 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 3-5 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 21-27 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 35-37 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 85 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 113-176 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 195-197 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 343-353 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 21 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 197 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 206 do original).

### F3-SN-03 — Nome do bucket com ID da conta e região

Contexto/data: Fase 3, 2026-08-27. Status herdado: **superada**.

Decisão histórica: O grupo nomeou o bucket com o ID da conta e a região (togglemaster-tfstate-<CONTA_FASE3>-us-east-2-an), em vez de sufixo aleatório.

Motivo registrado: Nome de bucket é único no mundo; o grupo preferiu identificar conta e região.

Alternativas registradas: Sufixo aleatório de 6 caracteres.

Aplicação na Fase 4: O rótulo “superada” só afasta o identificador da conta antiga. A convenção com conta/região ainda pode ser usada na nova, em backend.hcl ignorado; não há proibição desse padrão.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 423 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 34 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 87-105 do original).

### F3-SN-04 — Lock nativo do S3 (use_lockfile) e Terraform >= 1.11

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Backend S3 com use_lockfile = true e encrypt = true nas três camadas; Terraform mínimo 1.11.0; sem tabela DynamoDB de lock. O CI usa Terraform 1.16.0.

Motivo registrado: Lock evita gravações concorrentes do estado. O projeto fixou mínimo 1.11.0, mas o recurso foi introduzido na 1.10.0; a justificativa original confundia essas versões.

Alternativas registradas: Tabela DynamoDB de lock.

Aplicação na Fase 4: Correção: lock nativo S3 existe desde Terraform 1.10.0. >=1.11.0 é a restrição deste projeto, não a primeira versão do recurso. Comentários no código ainda precisam de ajuste.

Fontes: [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 38 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 300-322 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 337-338 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 425 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 436-438 do original).

### F3-SN-05 — NAT Gateway por variável, com padrões opostos

Contexto/data: Fase 3, 2026-09-15. Status herdado: **vigente**.

Decisão histórica: enable_nat_gateway: padrão true no variables.tf (para não derrubar o cluster por esquecimento) e false no terraform.tfvars.example (para não pagar recurso ocioso).

Motivo registrado: Equilíbrio entre não quebrar o cluster e não pagar NAT parado (~US$ 33/mês).

Alternativas registradas: Padrão único.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 553-555 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 571-576 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 606-612 do original).

### F3-SN-06 — Política de custo entre sessões: pausa (NAT desligado) ou destruir também a base

Contexto/data: Fase 3, 2026-09-09 a 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Opção A entre sessões: destruir k8s, conferir EBS, destruir cluster, preservar base e bucket, aplicar enable_nat_gateway=false na base (o plano deve remover só NAT, EIP e rota); religar o NAT antes do cluster. Opção B no encerramento: destruir também a base (ECR e role do CI somem). Em 2026-09-11 a base ficou; em 2026-09-15 foi destruída.

Motivo registrado: Cluster completo custava ~US$ 0,37/h (depois 0,385/h) e o crédito era limitado; derrubar ao fim da sessão foi tratado como requisito. A opção A preserva imagens e acelera a próxima subida.

Alternativas registradas: Manter tudo ligado (~US$ 0,385/h); exclusão completa a cada sessão.

Aplicação na Fase 4: Escolha de preservação da base versus destroy completo continua aberta e depende da posse dos recursos manuais. Custos históricos não estimam a conta atual.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 157 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 177 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 210-212 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 11-19 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 179-201 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 209-210 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 465-469 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 592-628 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 326 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1451-1494 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 130-133 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 511-514 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 885-915 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 189-192 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 749-811 do original).

### F3-SN-07 — Ordem da exclusão completa, com a Application do ArgoCD removida antes

Contexto/data: Fase 3, 2026-09-11. Status herdado: **revisar**.

Decisão histórica: Excluir a Application togglemaster com kubectl (após conferir finalizers; wait 5m); destruir terraform/k8s com EKS, NAT e CSI vivos; confirmar a remoção do PV/EBS; destruir terraform/cluster; destruir terraform/; conferir sobras; só então esvaziar e excluir o bucket. Um bloco por vez, sem -auto-approve, checando exit code.

Motivo registrado: Evita corrida entre selfHeal/CreateNamespace do ArgoCD e o namespace sendo destruído. O disco do targeting foi criado pelo CSI e depende do driver vivo para ser apagado. O bucket guarda estado e locks até o fim.

Alternativas registradas: Deixar o Terraform remover tudo (risco de corrida); pausa preservando a base (F3-SN-06).

Aplicação na Fase 4: Roteiro histórico; definir antes os namespaces/PVCs da stack e os recursos que devem sobreviver. Não executar remoções ao ler esta seção.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 157 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 177 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 3 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 27-38 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 77-206 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 216-218 do original).

### F3-SN-08 — Plano ordenado por custo, cluster no fim

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Ordenar o trabalho por custo, não por dependência técnica: o que não consome crédito vem primeiro; o cluster fica para o fim, em sessões de 3 horas; ensaio 4 dias antes da gravação. Aplicar a base com enable_nat_gateway = false.

Motivo registrado: Workflows de CI dependem só do ECR e da role OIDC (base). Itens de vídeo sem cluster podem ser gravados antes. Se o primeiro apply completo quebrar, há tempo para corrigir com o cluster desligado.

Alternativas registradas: Ordem por dependência técnica.

Aplicação na Fase 4: Adiar recursos cobrados não dispensa respeitar dependências técnicas. NAT desligado antes do cluster precisa ser revisto para rede privada sem endpoints substitutos.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 357-365 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 369 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 3-4 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 677 do original).

### F3-SN-09 — Âncora de escopo: entregar o básico que funciona

Contexto/data: Fase 3, 2026-08-27 (reafirmada em 2026-09-09). Status herdado: **revisar**.

Decisão histórica: Priorizar o básico que atende ao enunciado. README com três listas: obrigatório, extras com justificativa e o que ficou de fora. Antes de propor algo, conferir se é obrigatório (O-*) ou sugestão (S-*). Na Fase 3: sem múltiplos ambientes, Ingress, charts próprios, ESO, KEDA, DAST ou plataformas de observabilidade.

Motivo registrado: O usuário avaliou que o assistente estava complicando o projeto; nenhum requisito expresso pedia os extras.

Alternativas registradas: Ampliar escopo com extras.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 314 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 371-377 do original); [INSTRUCOES_ASSISTENTES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/INSTRUCOES_ASSISTENTES.md) (linhas 69 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 86 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 105 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 173-175 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 101 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 89 do original).

### F3-SN-10 — EKS em versão de suporte padrão (1.34 em vez de 1.31)

Contexto/data: Fase 3, 2026-09-09. Status herdado: **revisar**.

Decisão histórica: Default do EKS trocado de 1.31 para 1.34 em terraform/cluster/variables.tf.

Motivo registrado: 1.31 saiu do suporte padrão em 2025-11-26; no suporte estendido o control plane vai de US$ 0,10/h para US$ 0,60/h (6x), sem ganho.

Alternativas registradas: Manter 1.31 e corrigir o custo.

Aplicação na Fase 4: [INCERTO] data exata de fim de suporte EKS 1.34; verificar fonte AWS antes da implantação. Não presumir custos atuais a partir das cifras antigas.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 224 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 427 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1589-1592 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 943 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 61 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 81 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 97 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 99-105 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 38 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 89 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 46 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 119-122 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 167-174 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 255 do original).

### F3-SN-11 — Sem chave estática da AWS: OIDC no CI e IRSA nos pods

Contexto/data: Fase 3, 2026-08-27 a 2026-09-15. Status herdado: **vigente**.

Decisão histórica: Os workflows assumem a role togglemaster-github-actions pelo provedor OIDC do GitHub; a role só aceita token deste repositório. Pods acessam SQS e DynamoDB por IRSA; nenhum Secret ou GitHub Secret guarda AWS_ACCESS_KEY_ID.

Motivo registrado: Eliminar o risco de vazamento de credencial; na Fase 2 as chaves estáticas num Secret eram 'a dor citada no enunciado'.

Alternativas registradas: Chaves estáticas nos Secrets do GitHub ou do Kubernetes (guia antigo, considerado o ponto mais grave).

Aplicação na Fase 4: Sem chaves AWS estáticas não significa ausência de segredos de aplicação/SaaS. OIDC da árvore local já foi corrigido e testado offline em 2026-10-28; CI real segue sem prova.

Fontes: [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 32-37 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1399-1402 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 96-99 do original); [_ARQUIVO_MORTO/GUIA_EXECUCAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_EXECUCAO.md) (linhas 8-13 do original); [_ARQUIVO_MORTO/GUIA_EXECUCAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_EXECUCAO.md) (linhas 32-34 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 27-30 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 90-92 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 53 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 114-116 do original).

### F3-SN-12 — Imagens por nome lógico e URL da fila fora do Secret

Contexto/data: Fase 3, 2026-08-27. Status herdado: **vigente**.

Decisão histórica: Deployments referenciam só o nome lógico da imagem; registro e tag entram pelo bloco images: do overlay. AWS_SQS_URL sai do Secret e vai para ConfigMap. analytics fica sem segredo.

Motivo registrado: Permitir 'kustomize edit set image' alterando um campo, sem sed em YAML. URL de fila nunca foi segredo.

Alternativas registradas: sed em YAML; manter a URL no Secret.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 383 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 411 do original).

### F3-SN-13 — ArgoCD pelo chart oficial via provider helm, versão fixa, com prune e selfHeal

Contexto/data: Fase 3, 2026-09-09. Status herdado: **revisar**.

Decisão histórica: ArgoCD instalado em terraform/k8s/argocd.tf pelo provider helm, chart oficial 7.7.11 fixo. Application aponta para gitops/overlays/prod na main, sync automático com prune e selfHeal, sem finalizer.

Motivo registrado: O enunciado permite Helm ou Terraform; instalar por Kustomize exigiria remendar o install.yaml (desligar Dex, réplicas). Versão fixa dá reprodutibilidade.

Alternativas registradas: Kustomize sobre o install.yaml oficial; kubectl apply de manifesto remoto (guia antigo).

Aplicação na Fase 4: Confirmado documentalmente em 2026-11-01: chart 7.7.11 tem appVersion v2.13.2, versão anterior à correção da CVE-2025-55190 (2.13.9). Isso não prova exploração nem versão executada na conta atual. Atualização é pendência TFK-02.

Fontes: [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 8 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 199-202 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 310-320 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 63 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 65 do original); [_ARQUIVO_MORTO/GUIA_EXECUCAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_EXECUCAO.md) (linhas 7-8 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 103 do original).

### F3-SN-14 — Bootstrap do ArgoCD em duas etapas

Contexto/data: Fase 3, 2026-09-09. Status herdado: **vigente**.

Decisão histórica: Em cluster novo, primeiro 'terraform -chdir=terraform/k8s apply -target=helm_release.argocd' e depois o apply completo.

Motivo registrado: O provider kubernetes valida o tipo Application no plan, antes de o Helm instalar o CRD; sem o -target o apply falha com 'no matches for kind "Application"'. depends_on não resolve.

Alternativas registradas: Um único apply (falha em cluster novo); provider de terceiros (descartado); criar a Application fora do Terraform (tiraria do código o objeto que demonstra o GitOps).

Aplicação na Fase 4: Procedimento de duas fases deve usar planos salvos, conforme F3-D-023. -target é expediente de bootstrap, não rotina para ocultar mudanças.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 248 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 271 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 318 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 19 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 42 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 77 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 91 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 231-258 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 42-48 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 50 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 63 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 89 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 211-222 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 329-332 do original).

### F3-SN-15 — Reconciliação do ArgoCD em 30 s

Contexto/data: Fase 3, 2026-09-11. Status herdado: **vigente**.

Decisão histórica: timeout.reconciliation de 180 s (padrão) para 30 s, com sync automático.

Motivo registrado: Sem Ingress não há webhook do GitHub. Na gravação, 3 minutos de tela parada ou um corte enfraquecem a prova de sincronização automática.

Alternativas registradas: Padrão de 180 s; clicar em Refresh (parece provocado); webhook (exige exposição).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 460-470 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 68 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 903-905 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1198-1201 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1389-1391 do original).

### F3-SN-16 — Credencial do repositório para o ArgoCD criada só se houver token

Contexto/data: Fase 3, 2026-09-09 a 2026-09-15. Status herdado: **revisar**.

Decisão histórica: count = var.github_token != "" ? 1 : 0. Repositório público clona sem credencial. Para repositório privado: token fine-grained (Contents read-only, só o repositório, dono = organização) via TF_VAR_github_token em variável de ambiente, nunca em arquivo.

Motivo registrado: Repositório público não precisa de credencial; token nunca em arquivo. Sem credencial em repositório privado, a Application fica Unknown com 'authentication required'.

Alternativas registradas: Token clássico com escopo repo (permissão larga); terraform.tfvars (grava o valor); repositório público sem token.

Aplicação na Fase 4: Repositório 04 privado foi confirmado em 2026-10-28. Token somente leitura e acesso do ArgoCD devem ser testados sem imprimir credenciais; não houve nova consulta nesta sessão.

Fontes: [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 65-164 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 925-997 do original).

### F3-SN-17 — Senha inicial do ArgoCD fora dos outputs

Contexto/data: Fase 3, 2026-09-15. Status herdado: **vigente**.

Decisão histórica: Ler a senha do Secret argocd-initial-admin-secret por kubectl e base64; não expor como output do Terraform.

Motivo registrado: Um output fica gravado em texto no arquivo de estado.

Alternativas registradas: Output sensível do Terraform.

Aplicação na Fase 4: sensitive oculta a exibição normal, mas não retira o valor do state. Ler um Secret para uso local não autoriza mostrá-lo em vídeo/chat.

Fontes: [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1177-1196 do original).

### F3-SN-18 — SERVICE_API_KEY provisória e ignore_changes no Secret do evaluation-service

Contexto/data: Fase 3, 2026-09-09. Status herdado: **vigente**.

Decisão histórica: O Terraform cria evaluation-service-secret com valor provisório; o seed troca pela chave real; o recurso declara lifecycle { ignore_changes = [data] }.

Motivo registrado: O banco nasce depois do Secret, então a chave real só existe após o seed; sem ignore_changes, o Terraform restauraria a chave provisória.

Alternativas registradas: Terraform gerenciar o valor sempre; seed gravando fora do Terraform sem ignore_changes.

Aplicação na Fase 4: ignore_changes protege contra atualização do campo, não contra perda do banco nem recriação do Secret. Testar seed e restart; não garantir recuperação só por existir lifecycle.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 249 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 318 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 20 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 79 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 94 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1270-1302 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1553 do original).

### F3-SN-19 — Schemas do RDS aplicados por pod psql descartável

Contexto/data: Fase 3, 2026-09-09. Status herdado: **vigente**.

Decisão histórica: Ler DATABASE_URL dos Secrets auth-service-secret e flag-service-secret para variáveis do shell e rodar 'kubectl run ... --rm -i --restart=Never --image=postgres:16-alpine -- psql "$VAR" < services/<svc>/db/init.sql'; conferir com '\dt'.

Motivo registrado: O Terraform cria instâncias e bancos vazios; o RDS está em subnet privada; a senha não deve aparecer na tela da gravação.

Alternativas registradas: Digitar senhas e endereços (descartado por expor senha).

Aplicação na Fase 4: Comando histórico transporta segredo em argumentos do processo/pod; não copiar literalmente para o runbook novo. Preferir mecanismo que não exponha a URL em argv, YAML ou log e revisar o acesso.

Fontes: [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 331-461 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1005-1015 do original).

### F3-SN-20 — Trivy estrito: ignore-unfixed false e exceções nominais datadas em .trivyignore

Contexto/data: Fase 3, 2026-09-09 (validada no pipeline em 2026-09-10). Status herdado: **revisar**.

Decisão histórica: ignore-unfixed: false nos 4 scans Trivy CRITICAL (2 em _ci-go.yml, 2 em _ci-python.yml). Exceções sem correção publicada ficam uma a uma no .trivyignore, com justificativa e data de revisão.

Motivo registrado: O enunciado da Fase 3 (p.4) exige falha em crítica sem prever exceção; ignore-unfixed escondia vulnerabilidades. A exceção vira linha revisável no diff de PR, em vez de flag silenciosa.

Alternativas registradas: ignore-unfixed true; desligar a regra; continue-on-error.

Aplicação na Fase 4: Exceções devem ser reavaliadas no artefato final. Data de revisão vencida não é prova de vulnerabilidade explorável nem aprovação de novas exceções.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 195 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 217 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 247 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 269 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 944 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 910-943 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 18 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 31 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 76 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 90 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 53 do original); [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 89 do original); [_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 34-40 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 49 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 105-113 do original); [_ARQUIVO_MORTO/ARQUITETURA.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/ARQUITETURA.md) (linhas 103-106 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 192-209 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 325-328 do original).

### F3-SN-21 — Scans sem continue-on-error; correção do CVE em golang.org/x/crypto e versões em cascata

Contexto/data: Fase 3, 2026-09-11 (relato). Status herdado: **vigente**.

Decisão histórica: Atualizar golang.org/x/crypto de v0.20.0 para v0.55.0. Em cascata: Go 1.25 nos Dockerfiles e no SAST, golangci-lint da linha 1.x para 2.x e três tratamentos de erro corrigidos. Scans não usam continue-on-error.

Motivo registrado: O Trivy acusou o CVE-2026-56854 (crítico); os pipelines passavam verdes porque os scans usavam continue-on-error.

Alternativas registradas: Não registradas na fonte.

Aplicação na Fase 4: CVE e versões antigas são relato histórico, não nova checagem de vulnerabilidades de todos os serviços.

Fontes: [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 176-190 do original); [_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md) (linhas 111-113 do original).

### F3-SN-22 — Lint e SAST: corrigir achado real, nosec pontual, estilo em .pylintrc

Contexto/data: Fase 3, 2026-09-09. Status herdado: **revisar**.

Decisão histórica: errcheck corrigido no código; bandit B608 e B104 marcados como falso positivo com '# nosec' pontual e justificativa; pylint: achados reais corrigidos e regras de estilo desligadas em .pylintrc com justificativa por regra; nenhuma regra da família E tocada; corte --fail-under=7.0 mantido. gosec/bandit falham só em severidade alta.

Motivo registrado: Notas iniciais de 4.84 a 5.66 abaixo do corte; achado real deve ser corrigido, não afrouxado.

Alternativas registradas: Baixar o corte do pylint; afrouxar o SAST.

Aplicação na Fase 4: Claude mediu em 2026-11-01: lint atual reprova sem dependências; requirements + pytest elevou notas acima do corte. Correção ainda não aplicada.

Fontes: [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 179-182 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 335-352 do original).

### F3-SN-23 — Gate de imagem por needs e CI sem kubectl apply

Contexto/data: Fase 3, 2026-09-11 (relato). Status herdado: **revisar**.

Decisão histórica: O job de imagem declara needs: [build, lint, sast, sca]; se algum falhar, a imagem não é construída. O último job grava a tag no overlay e comita; nenhum workflow faz kubectl apply; quem aplica é o ArgoCD.

Motivo registrado: Interpretar ao pé da letra 'falhar e não prosseguir' do enunciado; resolver deploy manual e deriva do cluster.

Alternativas registradas: Não registradas.

Aplicação na Fase 4: Self-healing por Actions é escopo novo; exige identidade e RBAC próprios. Instalar kustomize para editar tag não equivale a renderizar/validar manifests no CI.

Fontes: [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 107-112 do original); [_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md) (linhas 129-146 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 330-338 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 702-717 do original).

### F3-SN-24 — Publicação de imagem e tag GitOps só em push na main

Contexto/data: Fase 3, 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Jobs 'Imagem Docker e push no ECR' e 'Atualizar tag no GitOps' só rodam com github.event_name == 'push' e github.ref == 'refs/heads/main'. workflow_dispatch roda testes e não publica.

Motivo registrado: [INCERTO] Motivo não declarado na fonte; implícito o controle de promoção para produção.

Alternativas registradas: workflow_dispatch publicando.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 637-640 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 842-843 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 879-898 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 1539 do original).

### F3-SN-25 — CI de Terraform roda só fmt e validate, sem plan

Contexto/data: Fase 3, 2026-09-09. Status herdado: **revisar**.

Decisão histórica: terraform-check.yml roda fmt e validate nas três camadas, com -backend=false, em PR e push; não roda plan.

Motivo registrado: plan exigiria credencial AWS no CI e acesso ao estado remoto; o ganho não compensava expor a conta. plan feito à mão no início de cada sessão.

Alternativas registradas: plan automatizado com credencial no CI.

Aplicação na Fase 4: O CI de Terraform sem credenciais é diferente dos jobs de imagens, que já assumem role. Não afirmar que todo o CI está sem acesso AWS.

Fontes: [_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md) (linhas 117 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 43 do original); [_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md) (linhas 71 do original).

### F3-SN-26 — SQS desligado no Compose padrão; fluxo assíncrono testado com Moto

Contexto/data: Fase 3, 2026-09-15. Status herdado: **vigente**.

Decisão histórica: No Compose padrão, AWS_SQS_URL vazio em evaluation e analytics (o worker do analytics não inicia). docker-compose.integration.yaml acrescenta o Moto (SQS e DynamoDB) e um inicializador de fila e tabela.

Motivo registrado: Ninguém precisa de conta ou credencial AWS para testar flags, regras, avaliação e cache.

Alternativas registradas: Exigir AWS real localmente.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 329-343 do original); [_ARQUIVO_MORTO/OPERACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/OPERACAO_2026-09-15.md) (linhas 351-354 do original).

### F3-SN-27 — Demonstração só com regras PERCENTAGE de 100 ou 0

Contexto/data: Fase 3, 2026-09-09. Status herdado: **vigente**.

Decisão histórica: Flag 'novo-painel' com {type: PERCENTAGE, value: 100} (sempre true) e outra flag com value 0 (sempre false) para o caso oposto.

Motivo registrado: O evaluation-service só implementa PERCENTAGE; regra com user_ids seria aceita pelo targeting e ignorada na avaliação. 100 e 0 são determinísticos.

Alternativas registradas: Trocar user_id na mesma flag (não funciona com 100%).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 520-557 do original).

### F3-SN-28 — Identidades: usuário IAM pessoal com MFA para bootstrap; root sem chave

Contexto/data: Fase 3, 2026-08-27. Status herdado: **revisar**.

Decisão histórica: Conta pessoal; MFA no root, usado só em emergência e sem chaves. Cada integrante com usuário IAM próprio (AdministratorAccess e MFA) para bootstrap e uso diário. Menor privilégio real nas roles criadas pelo Terraform. Access key pessoal, em gerenciador de senhas, nunca no repositório nem compartilhada.

Motivo registrado: A AWS desaconselha chaves do root. AdministratorAccess aceito para bootstrap de conta de estudo.

Alternativas registradas: Não registradas.

Aplicação na Fase 4: Preferência histórica não recomenda AdministratorAccess permanente nem chaves estáticas para a conta nova. Avaliar identidade temporária e menor privilégio.

Fontes: [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 44-81 do original); [_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md) (linhas 293-298 do original); [_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md) (linhas 208 do original); [_ARQUIVO_MORTO/RUNBOOK-SESSAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/RUNBOOK-SESSAO.md) (linhas 227-229 do original).

### F3-SN-29 — Estimativa de custo com fonte única

Contexto/data: Fase 3, 2026-09-11. Status herdado: **revisar**.

Decisão histórica: A estimativa de custo fica num só lugar (seção 8 do relatório), com números oficiais do AWS Pricing Calculator; sem arquivo próprio.

Motivo registrado: Dois lugares com o mesmo número divergem (já havia 0,37 e 0,385 em arquivos diferentes).

Alternativas registradas: Arquivo separado de estimativa (descartado).

Aplicação na Fase 4: Custos antigos são referência de método. Nova estimativa deve incluir a observabilidade e a condição real de cobrança.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 130 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 135 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 200 do original).

### F3-SN-30 — Gerador do PDF do relatório

Contexto/data: Fase 3, 2026-09-11 a 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Em 2026-09-11, scripts/gerar-relatorio-pdf.py (Markdown para PDF, com capa e captura de custos) foi declarado canônico. Em 2026-09-14, o docstring do build-report-fase3.py (ReportLab) se declara canônico, com texto dentro do script. Em 2026-09-15, a D-024 arquivou o build-report e o capturar-estimativa-aws.cjs.

Motivo registrado: O gerador ReportLab não rodava na máquina (reportlab ausente), escrevia em output/pdf/ (ignorado) e divergia do formato da Fase 2. O ReportLab acrescentava desafios, decisões e captura de custos.

Alternativas registradas: Um ou outro gerador; escolha da identidade visual ficou com o usuário.

Aplicação na Fase 4: Ambos os geradores foram preservados integralmente; escolha futura não exige reconstruir a extração.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 23 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 196 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 201 do original); [DECISOES.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/DECISOES.md) (linhas 3-27 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 1-10 do original); [_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py) (linhas 32-34 do original); [_ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py) (linhas 22-28 do original); [_ARQUIVO_MORTO/capturar-estimativa-aws_2026-09-11.cjs](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/capturar-estimativa-aws_2026-09-11.cjs) (linhas 35-41 do original).

### F3-SN-31 — Material de aula da FIAP mantido no repositório

Contexto/data: Fase 3, 2026-09-13. Status herdado: **revisar**.

Decisão histórica: Os 33 arquivos de aula (18 MB, 87% do peso do repositório) voltaram ao controle de versão; o bloco saiu do .gitignore. Em 2026-09-15 foram movidos para docs/aulas-fiap/.

Motivo registrado: Decisão do usuário. A preocupação de publicar material da instituição em repositório aberto ficou como ressalva.

Alternativas registradas: Retirar do versionamento (feito em 2026-09-11 e revertido).

Aplicação na Fase 4: Preservação/retirada dos 34 materiais ausentes continua independente desta mescla.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 20 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 138-142 do original); [ORGANIZACAO_DE_PASTAS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md) (linhas 21-24 do original); [ORGANIZACAO_DE_PASTAS.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md) (linhas 38-39 do original).

### F3-SN-32 — Vídeo no YouTube como Não listado

Contexto/data: Fase 3, 2026-09-11 / 2026-09-15. Status herdado: **revisar**.

Decisão histórica: Publicar como Não listado e testar o link numa aba anônima; o link entra no README e no relatório.

Motivo registrado: Vídeo privado o avaliador não abre.

Alternativas registradas: Privado.

Aplicação na Fase 4: Garantir acesso real ao avaliador; Não listado é uma opção, não requisito literal de plataforma da FIAP.

Fontes: [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 744-745 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 929-931 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 978 do original).

### F3-SN-33 — Plano de gravação de 15/09 substitui o guia de 11/09

Contexto/data: Fase 3, 2026-09-14. Status herdado: **historica**.

Decisão histórica: O GUIA_GRAVACAO (gravação de 11/09) foi substituído pelo PLANO_GRAVACAO_2026-09-15. A cena de GitOps passou a mostrar troca de versão de imagem, não de réplicas.

Motivo registrado: A gravação de 11/09 saiu sem áudio e a conta foi destruída. O guia tinha cenas que não funcionavam com a conta recriada (plan do cluster antes da base, 'base permanente', troca de réplicas).

Alternativas registradas: Plano C: usar a gravação muda de 11/09 (17min58s) com narração por cima, dizendo que as cenas são de 11/09.

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 3-6 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 477-488 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 1-5 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 1057-1060 do original).

### F3-SN-34 — Demonstração DevSecOps e GitOps com PyYAML no flag-service

Contexto/data: Fase 3, 2026-09-15. Status herdado: **historica**.

Decisão histórica: Na demo, PyYAML==5.3.1 (vulnerável) na primeira linha do requirements.txt do flag-service; a correção (PyYAML==6.0.1) mergeada na main dispara pipeline, commit do robô e sincronização do ArgoCD (cena de GitOps).

Motivo registrado: Localmente, o Trivy 0.74 não leu pacotes listados após setuptools<81 e Werkzeug<3; no CI (Trivy v0.70.0) a linha no fim foi detectada. O enunciado pede 'sincronizando a nova versão'.

Alternativas registradas: Linha no fim do arquivo; trocar réplicas de 1 para 2 (guia de 11/09).

Aplicação na Fase 4: Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.

Fontes: [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 57-59 do original); [LOG_DE_TRABALHO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/LOG_DE_TRABALHO.md) (linhas 136 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 414-415 do original); [_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md) (linhas 632-717 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 434-449 do original); [_ARQUIVO_MORTO/GUIA_GRAVACAO.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/GUIA_GRAVACAO.md) (linhas 982 do original).

### F3-SN-35 — Caminho C e merge híbrido dev -> main com -X theirs

Contexto/data: Fase 3, 2026-09-08 a 2026-09-09. Status herdado: **historica**.

Decisão histórica: Manter a base própria já aplicada e trazer os módulos EKS, ElastiCache e RDS da implementação paralela da main para terraform/cluster/. Merge dev -> main com prioridade para a dev nos 30 conflitos add/add, preservando histórico, com tag de backup criada antes. Remoção de estruturas duplicadas (terraform/environments, terraform/bootstrap, gitops/apps, gitops/infrastructure) e de dois workflows.

Motivo registrado: A main tinha implementação paralela nunca aplicada, com EKS para LabRole do AWS Academy e Trivy com continue-on-error.

Alternativas registradas: Adotar a implementação da main; descartá-la; merge manual arquivo por arquivo.

Aplicação na Fase 4: Lição: não usar estratégia de conflitos para descartar alterações silenciosamente; importação da Fase 4 já foi concluída, não repetir.

Fontes: [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 266-281 do original); [_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md) (linhas 354-371 do original).
