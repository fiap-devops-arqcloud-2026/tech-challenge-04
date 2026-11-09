# Revisão integral do Tech Challenge Fase 4

TL;DR: a base funcional e a instrumentação foram comprovadas localmente. A entrega completa da Fase4 ainda depende de implantação, stack de métricas/logs, APM externo, alertas/incidentes, self-healing e evidências finais. Esta revisão cobre todos os42 IDs do catálogo, identifica falhas herdadas que afetam o desenho dos alertas e não executa implantação ou publicação.

Última atualização: 2026-10-28, Codex. Revisão iniciada em2026-10-27 e retomada após interrupção por créditos. Fuso: America/Sao_Paulo (UTC-03:00). Resultados anteriores mantêm suas datas originais.

## 1. Explicação simples e parecer técnico

Já temos uma aplicação que funciona no laboratório e mostra por onde uma requisição passou. Ainda faltam os painéis e integrações que permitam enxergar problemas no ambiente Kubernetes, avisar o responsável e tentar corrigir a falha automaticamente. Depois, tudo isso precisa aparecer no vídeo e no relatório PDF pedidos pela FIAP.

Tecnicamente, há cinco serviços Go/Python, infraestrutura Terraform e manifests GitOps herdados/adaptados, e pipeline local OTLP/HTTP de traces. O Collector atual tem apenas o pipeline `traces`, exportadores `debug`/arquivo e tratamento de atributos. Logs JSON correlacionados no stdout não equivalem a coleta/exportação ao Loki. Não existem ainda no código operacional os charts da stack, pipelines de métricas/logs, exportação New Relic e automação de incidente/mitigação. Os manifests Kubernetes não definem endpoint OTLP; publicar somente as imagens instrumentadas não ativará o SDK.

**Parecer: projeto em implementação, com base local comprovada; ainda não pronto para submissão da Fase4.** Ausência de prova externa nesta revisão não afirma inexistência de recursos em uma conta externa: AWS, GitHub remoto, New Relic, PagerDuty e Slack não foram consultados.

## 2. Fonte normativa, escopo e limites

- Fonte: [enunciado FIAP original](../../POSTECH%20-%20Tech%20Challenge%20-%20Fase%204.pdf), sete páginas lidas por inteiro e renderizadas em2026-10-27; p.1/7 institucionais, exigências p.2–6. Não há anexos adicionais nesse arquivo.
- A decomposição em42 IDs é do [catálogo do projeto](../../docs/requisitos/README.md), não uma numeração oficial da FIAP. Cada linha abaixo conserva sua evidência de página/trecho, reconferida contra o PDF.
- Abrangência operacional: cinco serviços/Dockerfiles/dependências/testes, Compose/Collector, Terraform/módulos, GitOps, nove workflows, scripts, documentação vigente/histórica e evidências. Inventário de preservação:205 arquivos fora da colaboração/acervo histórico, incluindo32 fontes e sete documentos/guias protegidos adicionais.
- Os31 PDFs de aulas não foram relidos integralmente nesta auditoria de implementação: seus hashes, cinco guias e validação estrutural foram conferidos. Isso preserva a auditoria didática anterior, sem alegar nova auditoria semântica aula a aula. Os guias não são a implantação.
- Não foram executados `terraform plan/apply`, acesso AWS, CI remoto, nova integração completa Compose, consultas de contas, verificação de links externos ou scan atualizado de CVEs. Houve validações locais e uma sonda funcional isolada para um novo achado.
- As33 exclusões históricas preexistentes na árvore de trabalho não foram executadas nem restauradas nesta revisão. Não houve commit, push, PR, alteração de main ou código operacional. Branch local conferida:dev; HEAD`3b21e65d8b22c454e43ba7dc3b3eb3a039ea061e`.

## 3. O que está comprovado e o que cada prova significa

| Área | Prova disponível | Alcance e limite |
|---|---|---|
| Base funcional | Ensaio de2026-10-22 e regressão de2026-10-27: cinco serviços, autenticação, flags/regras/cache e eventos persistidos | Local; SQS/DynamoDB simulados por Moto. Não demonstra a conta/cluster novo. |
| Instrumentação | Trace de2026-10-27 com19spans/5serviços; SQL auth2/flag1/targeting1, Redis, HTTP, SQS→analytics→DynamoDB | Árvore/contexto e logs correlacionados conferidos; não demonstra tela APM nem Service Map. |
| Testes de aplicações | Evidências de13 testes Go principais+8subtestes e20 Python nas imagens; hashes28fontes produção correspondem ao ensaio | Os testes foram executados no trabalho anterior de27; a revisão reconferiu artefatos/hashes e fez uma nova sonda focada. Não certificam todos os modos de falha. |
| IaC | `fmt -check` e `validate` nas três raízes aprovados em2026-10-27, zero erro/aviso | Código válido localmente; não prova criação, custo, permissão ou estado remoto.40arquivos.tf,7diretórios de módulos locais,8chamadas,51blocos resource. |
| GitOps | Renderização atual de23objetos: base dos aplicativos, PostgreSQL targeting e HPA | Não contém a nova stack de observabilidade. Sentinelas de conta/imagens ainda impedem implantação útil. |
| Materiais |32fontes (31PDFs de aulas+enunciado),5guias e catálogo/espelho:39arquivos protegidos íntegros; guias sem erros estáticos | Não substitui funcionamento prático.123links locais em8Markdown conferidos,2âncoras históricas obsoletas. |

## 4. Achados técnicos e documentais

Os achados abaixo são observações/recomendações da revisão, e não novas obrigações da FIAP. Não foram corrigidos neste trabalho de auditoria.

### F-017 — Falha de targeting pode liberar uma flag habilitada e aparentar sucesso

Prioridade recomendada: alta, antes de desenhar os alertas/cenário de incidente. Em [evaluator.go](../../services/evaluation-service/evaluator.go), linhas113–115 descartam `ruleErr`; a linha258 trata regra ausente como liberação. A sonda isolada de2026-10-27 confirmou que regra404, resposta401, resposta500 e timeout no targeting resultam em HTTP200/`result=true`, com `Rule:null` gravada em cache. O código define TTL de30segundos (linha24). No controle, falha500 no flag-service resulta em502, sem esse cache.

Impacto: indisponibilidade pode ser confundida com inexistência de regra e permitir exposição indevida de uma funcionalidade. Um alerta baseado somente em5xx do evaluation pode não perceber essa falha. A FIAP não prescreve uma política específica de fallback; recomenda-se distinguir404 esperado de falha operacional, definir a política e criar regressão. A sonda passou porque confirmou o comportamento atual, não porque o aprovou.

### F-018 — Auth apresenta erro de banco como credencial inválida

Prioridade recomendada: alta para o desenho do alerta. Em [handlers.go](../../services/auth-service/handlers.go), linhas50–58, qualquer erro do SELECT devolve401, incluindo indisponibilidade do banco; [handlers_test.go](../../services/auth-service/handlers_test.go) explicita essa resposta para erro simulado/cancelamento. Não foi feita nova interrupção de banco real nesta revisão.

Impacto: um alerta apenas de5xx no auth pode perder essa falha; o span SQL ainda marca erro. Distinguir `sql.ErrNoRows` de falha operacional ou escolher um sinal que detecte esta condição. O percentual5% e o auth-service são exemplos da p.5, não imposições do enunciado.

### F-019 — Imagens instrumentadas não ativam observabilidade sozinhas no Kubernetes

Prioridade: bloqueio técnico da observabilidade no cluster. Os [ConfigMaps da base](../../gitops/base) não fornecem endpoint OTLP e não há Collector/stack no overlay; [telemetry.go](../../services/auth-service/telemetry.go), linhas38–41, e [telemetry.py](../../services/flag-service/telemetry.py), linha73, ativam exportação apenas com endpoint configurado. É preciso adicionar stack/endpoint/identidades/configurações e comprovar a chegada dos três sinais. Afeta especialmente06–11,14–15 e20.

### F-020 — O CI integrado não executa a regressão de traces

Prioridade recomendada: média, antes da publicação. [compose-integration.yml](../../.github/workflows/compose-integration.yml), linha22, chama somente `test-compose.sh`; não usa o overlayOTel nem `test-observability.sh`/`test-traces.py`. Os workflows de linguagem executam testes unitários, mas isso não substitui a prova integrada HTTP/SQS/SQL. Acrescentar esse gate é recomendação técnica para proteger a funcionalidade; a FIAP exige CI/CD/DevSecOps, sem nomear este script específico.

### F-021 — O plano e o catálogo não refletem toda a execução atual

Prioridade recomendada: média. O catálogo de2026-09-20 continua com todos os itens Pendente. O plano v02 mantém cronograma de setembro, bibliotecas previstas diferentes das efetivamente usadas e critérios baseados em Running/Synced. A matriz desta revisão é o retrato atual; o catálogo continua fonte normativa preservada.

Há ainda uma divergência histórica: o plano diz que todo sinal passa pelo Collector, mas também prevê scrape direto de infraestrutura pelo Prometheus; o README atual diferencia esses caminhos. Registrar essa divergência na próxima versão, mantendo clara a exigência de centralização da telemetria dos microsserviços. Dois links históricos perderam âncoras (`docs/GUIA_DE_REPRODUCAO.md:9` e `docs/ARQUITETURA.md:7`), sem arquivo de destino ausente. Não é bloqueio acadêmico por si só.

### F-022 — Revisão das exceções de vulnerabilidade está vencida

Prioridade recomendada: antes de publicar imagens. [.trivyignore](../../.trivyignore), linha58, previa revisão em2026-10-15. É necessário reexecutar os scans nas imagens atuais e reavaliar justificativas/exceções. Esta revisão não consultou a situação atual desses CVEs e não conclui que as imagens atuais estejam vulneráveis ou corrigidas. A evidência de scans da Fase3 não certifica a versão instrumentada da Fase4.

### Preparação operacional ainda necessária

Além da stack ausente, faltam conta/backend/região/cotas/orçamento/identidades confirmados, imagens e outputs reais no overlay, inicialização de schemas e chave de serviço, bootstrap do ArgoCD em suas etapas e teste funcional no cluster. O runbook legado precisa ser adaptado à Fase4. Não transportar estado/segredos da conta anterior. Os três workers do plano são uma proposta de capacidade; o código declara dois por padrão, e o PDF não exige exatamente três.

## 5. Matriz completa dos42 requisitos

Legenda: **Comprovado localmente** = implementação específica e execução local evidenciadas, ainda sujeitas à versão/entrega final; **Parcial** = parte implementada/decidida, faltando operação ou entrega; **Pendente** = resultado exigido ainda não demonstrado/entregue, frequentemente sem implementação; **Confirmar** = regra/procedimento acadêmico incerto, não dispensa do requisito.

Contagem:2 comprovados localmente,10 parciais,28 pendentes e2 a confirmar. **Não representa percentual de nota nem percentual de esforço:** a lista desdobra implementação, demonstração e documentação do mesmo componente.02/13 não encerram, por exemplo, os requisitos de cluster ou publicação.

Referências E01–E09 são detalhadas ao fim; cada evidência normativa é do PDF original, não de sugestão do revisor.

| ID | Requisito | Fonte FIAP (página e trecho) | Estado | Evidência atual | O que falta / aceite |
|---|---|---|---|---|---|
| REQ-OBR-01 | Manter toda a base das Fases 1, 2 e 3 funcionando. | p. 2: “é obrigatório que toda a base das Fases 1, 2 e 3 esteja funcionando” | Parcial | E01/E03: fluxo funcional local aprovado; AWS simulada por Moto. | Reproduzir a base completa no cluster/conta da Fase4, incluindo autenticação, regras, cache, fila e persistência; tratar F-017/F-018 ao definir as falhas. |
| REQ-OBR-02 | Manter os cinco microsserviços conteinerizados. | p. 2: “Os 5 microsserviços conteinerizados.” | Comprovado localmente | E01/E03: Dockerfiles e execução dos cinco serviços comprovados. | Preservar este resultado na versão publicada e demonstrar a implantação conjunta; a exigência específica de conteinerização está comprovada localmente. |
| REQ-OBR-03 | Provisionar a infraestrutura por Terraform. | p. 2: “A infraestrutura provisionada via código (Terraform).” | Parcial | E04: 40 arquivos .tf; três raízes validadas sem erros. | Confirmar conta/backend/parâmetros e provisionar a infraestrutura via Terraform; validate não comprova apply ou recursos ativos. |
| REQ-OBR-04 | Manter pipelines CI/CD com DevSecOps (GitHub Actions ou similar). | p. 2: “Pipelines de CI/CD (GitHub Actions ou similar) com DevSecOps.” | Parcial | E04: nove workflows, build/testes/lint/SAST/SCA/imagens/GitOps declarados. | Executar CI/CD no repo04 e registrar os resultados/gates; configurar destino AWS. Revisar exceções vencidas e incluir regressão OTel como melhoria F-020. |
| REQ-OBR-05 | Implantar no Kubernetes (EKS, GKE ou AKS), com a implantação gerenciada via GitOps (ArgoCD/Flux). Ver Q-01. | p. 2: “Implantação no Kubernetes (EKS, GKE, AKS) gerenciada via GitOps” | Parcial | E04: manifests GitOps renderizam 23 objetos; ArgoCD declarado. | Implantar no Kubernetes via ArgoCD, substituir sentinelas, publicar imagens, inicializar schemas/chaves e comprovar fluxo funcional, não só Running/Synced. |
| REQ-OBR-06 | Provisionar a stack de observabilidade no cluster e acrescentar Helm charts ao repositório GitOps. | p. 3: “adicionando os Helm charts ao seu repositório GitOps” | Pendente | E04: não há charts/Applications da stack de observabilidade no GitOps operacional. | Adicionar Helm charts e valores versionados, provisionar a stack dentro do cluster e demonstrar reconciliação GitOps. |
| REQ-OBR-07 | Usar Prometheus para armazenar e consultar métricas de infraestrutura. | p. 3: “Prometheus: para armazenamento e consulta de métricas de infraestrutura.” | Pendente | E03/E04: Prometheus não está implementado na composição/overlay operacional. | Instalar Prometheus e comprovar coleta, armazenamento e consulta de métricas reais de infraestrutura. |
| REQ-OBR-08 | Usar Loki para centralizar e indexar todos os logs dos contêineres do cluster. | p. 3: “Loki: para centralização e indexação de todos os logs dos contêineres do cluster.” | Pendente | E03/E04: logs JSON existem no stdout; Loki/coleta central não existem. | Implantar coleta e Loki com cobertura dos logs dos contêineres do cluster; conferir namespaces/seletores e pesquisar logs reais. |
| REQ-OBR-09 | Usar Grafana como visualização principal. | p. 3: “Grafana: como ferramenta principal de visualização.” | Pendente | E04: Grafana só aparece no desenho e material didático. | Implantar Grafana como visualização principal e configurar fontes de dados funcionais. |
| REQ-OBR-10 | Criar no Grafana ao menos um dashboard customizado que centralize a saúde do ecossistema: (a) uso de recursos do cluster; (b) taxa de requisições dos microsserviços; (c) painel de logs em tempo real. | p. 3: “no mínimo, 1 Dashboard customizado” | Pendente | E05: nenhum dashboard operacional da Fase4 localizado. | Criar e mostrar pelo menos um dashboard com recursos do cluster, taxa de requisições dos microsserviços e logs em tempo real. |
| REQ-OBR-11 | Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM). Ver Q-08. | p. 4: “receber, processar e exportar suas métricas, logs e traces” | Parcial | E02/E03: Collector local recebe/processa traces e grava arquivo/debug; logs correlacionados no stdout. | Implementar métricas e coleta de logs, configurar pipelines e exportação para Prometheus/Loki/APM e comprovar os três sinais. JSONL local não é APM. |
| REQ-OBR-12 | Escolher UMA ferramenta APM: Datadog OU New Relic; o PDF orienta contas gratuitas for education. Ver Q-04. | p. 4: “Datadog OU New Relic - use as contas gratuitas for education” | Parcial | E07/D-009: New Relic escolhido; última informação do usuário é conta ainda indisponível. | Disponibilizar/configurar conta e validar uso do APM; confirmar acesso educacional indicado no PDF, sem presumir gratuidade/benefícios. |
| REQ-OBR-13 | Alterar o código-fonte ou Dockerfile dos microsserviços com bibliotecas de instrumentação. | p. 4: “altere o código-fonte ou o Dockerfile dos microsserviços” | Comprovado localmente | E02/E03: cinco serviços instrumentados, 19 spans e testes; 28 fontes correspondem ao ensaio. | Preservar a instrumentação e suas regressões na publicação; seu código/funcionamento local estão comprovados. Ingestão APM é tratada em14/15. |
| REQ-OBR-14 | Gerar tracing distribuído e mostrar no APM o caminho de uma requisição ao evaluation-service. | p. 4: “Ao fazer uma requisição no evaluation-service, o APM deve mostrar o "caminho"” | Parcial | E02/E03: trace W3C atravessa cinco serviços, HTTP/SQS/SQL/Redis/DynamoDB localmente. | Exportar ao New Relic e exibir no painel o caminho de uma requisição ao evaluation-service, incluindo dependências. |
| REQ-OBR-15 | Exibir no APM o mapa de dependências dos cinco microsserviços. | p. 4: “mapa de dependências dos seus 5 microsserviços” | Pendente | E03/E05: árvore local de spans existe, mas não há Service Map comprovado em APM. | Exibir o mapa de dependências dos cinco microsserviços no New Relic; testar reconhecimento das relações HTTP e assíncronas. |
| REQ-OBR-16 | Configurar um alerta inteligente no Grafana ou no APM. | p. 5: “configure um alerta inteligente (no Grafana ou APM)” | Pendente | E04: não há regra operacional de alerta inteligente Grafana/APM. | Definir sinal, condição, janela e cenário; provocar a condição e comprovar Firing. Limiar de5% da aula/enunciado é exemplo, não valor obrigatório. |
| REQ-OBR-17 | Criar conta no PagerDuty OU OpsGenie e integrar o alerta para abrir incidente automaticamente, com a ferramenta acionando o time (objetivo da p. 3). Ver Q-09. | p. 5: “integre o alerta para abrir um incidente automaticamente” | Pendente | E07: PagerDuty escolhido; sem integração/evidência operacional no repo. | Configurar conta, integração e responsável/escala; comprovar abertura automática de incidente e acionamento do responsável. |
| REQ-OBR-18 | Enviar notificação detalhada de ChatOps a Slack, Discord ou Teams. Ver Q-02. | p. 5: “notificação detalhada para um canal do Slack, Discord ou Teams” | Pendente | E07: Slack escolhido; sem configuração/evidência operacional de ChatOps. | Integrar o alerta/incidente e comprovar chegada de notificação detalhada ao canal Slack escolhido. |
| REQ-OBR-19 | Criar automação de Self-Healing que reaja automaticamente ao alerta e tente mitigar sem intervenção humana. | p. 5: “reaja automaticamente ao alerta criado” | Pendente | E04: não há automação reativa ao alerta; selfHeal do ArgoCD é reconciliação GitOps. | Implementar e testar mitigação automática ligada ao alerta, com ação pertinente à falha. Confirmar recuperação após a ação como verificação recomendada. |
| REQ-OBR-20 | Entregar no repositório IaC/GitOps atualizado com stack e OTel Collector. | p. 5: “Código IaC/GitOps atualizado para incluir a stack de monitoramento e o OTel Collector.” | Parcial | E03/E04: base IaC/GitOps e configuração Collector local existem, mas stack/Collector Kubernetes faltam. | Completar e entregar código IaC/GitOps da stack e Collector no repositório acessível; verificar implantação a partir dessa versão. |
| REQ-OBR-21 | Entregar código das aplicações atualizado com instrumentação. | p. 5: “Código fonte das aplicações atualizado com a instrumentação.” | Parcial | E03/E09: aplicações instrumentadas no checkout dev; alterações ainda locais. | Consolidar/versionar/publicar o código após autorização e testar acesso do avaliador. Código no checkout não comprova entrega remota. |
| REQ-OBR-22 | Entregar scripts ou automações de Self-Healing. | p. 5: “Scripts ou automações criadas para o Self-Healing.” | Pendente | E04: scripts/workflow de self-healing da Fase4 não localizados. | Implementar, versionar e entregar os scripts/workflows que realizam a mitigação automática demonstrada. |
| REQ-OBR-23 | Evidenciar funcionamento prático de todas as métricas, configurações e requisitos; material apenas configurado não basta. | p. 5: “Não basta configurar; é preciso mostrar operando na prática.” | Parcial | E01/E02: há evidências locais funcionais e traces; faltam provas da maioria dos novos componentes. | Completar evidências de cada requisito no vídeo/PDF; cruzar requisito, teste, print, minuto do vídeo e versão implantada. |
| REQ-OBR-24 | Entregar vídeo com duração de até 25 minutos. | p. 5: “Vídeo de Demonstração (até 25 min)” | Pendente | E05/E06: vídeo/link final da Fase4 não localizado. | Gravar, revisar e disponibilizar vídeo de até25min com todo o roteiro obrigatório. |
| REQ-OBR-25 | Mostrar no vídeo EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack. [INCERTO]: divergência com alternativas da p. 2; Q-01. | p. 5: “mostre que o cluster EKS (IaC) e o ArgoCD (GitOps) continuam rodando” | Pendente | E05: nenhuma gravação atual de cluster/ArgoCD/stack da Fase4. | Mostrar no vídeo EKS/IaC e ArgoCD/GitOps rodando com a nova stack; a escolha EKS/ArgoCD segue a formulação conservadora Q-01. |
| REQ-OBR-26 | No vídeo: (a) abrir o Grafana; (b) exibir o dashboard customizado com as métricas; (c) buscar logs no Loki; (d) explicar como o Collector roteia esses dados. | p. 5: “Busque logs no Loki. Explique rapidamente como o OTel Collector está roteando esses dados.” | Pendente | E05: guias/diagramas não constituem a demonstração pedida. | No vídeo, abrir Grafana/dashboard, buscar logs Loki e explicar o roteamento efetivamente usado pelo Collector. |
| REQ-OBR-27 | No vídeo: (a) abrir o painel do Datadog/New Relic e mostrar o Service Map; (b) fazer uma requisição de teste; (c) exibir o trace distribuído detalhado. | p. 6: “Faça uma requisição de teste e exiba o Trace Distribuído detalhado no APM.” | Pendente | E05: não há gravação APM; prova JSONL local não é tela New Relic. | No vídeo, abrir New Relic, exibir Service Map, fazer requisição e mostrar trace distribuído detalhado. |
| REQ-OBR-28 | No vídeo: causar um problema proposital no sistema. | p. 6: “Cause um problema proposital no sistema” | Pendente | E03/E05: sondas de auditoria não constituem o incidente demonstrado no sistema implantado. | Escolher/implementar uma falha controlada e provocá-la durante a demonstração. |
| REQ-OBR-29 | No vídeo: mostrar o alerta em Firing no Grafana/APM. | p. 6: “Mostre o alerta disparando (Firing) no Grafana/APM.” | Pendente | E04/E05: alerta operacional e respectiva gravação ausentes. | Mostrar alerta em Firing no Grafana/APM durante a falha demonstrada. |
| REQ-OBR-30 | No vídeo: (a) mostrar o incidente sendo aberto no PagerDuty/OpsGenie; (b) mostrar a notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02. | p. 6: “notificação chegando no Slack/Discord” | Pendente | E05: sem evidência de incidente/notificação da Fase4. | Mostrar abertura no PagerDuty e chegada ao Slack durante o mesmo ciclo de falha. Slack evita a ambiguidade Q-02 sobre Teams. |
| REQ-OBR-31 | No vídeo: mostrar a automação de Self-Healing acionada e executando a ação corretiva. | p. 6: “Mostre a automação de Self-Healing sendo acionada e executando a ação corretiva” | Pendente | E04/E05: sem automação corretiva/gravação do acionamento. | Mostrar a automação acionada automaticamente e executando a ação corretiva, com log/terminal correspondente. |
| REQ-OBR-32 | Entregar relatório no formato PDF. | p. 6: “Relatório de Entrega (.PDF)” | Pendente | E05: relatórios internos Markdown existem; o relatório PDF final da Fase4 não foi localizado. | Gerar/revisar o PDF final com identificação, links, quatro prints e justificativas. |
| REQ-OBR-33 | Incluir nomes, RMs e usernames no relatório. | p. 6: “Nomes, RMs e usernames.” | Pendente | E05: identificação final não consolidada em PDF da Fase4. | Inserir nomes, RMs e usernames dos participantes efetivos; confirmar escopo dos usernames/Q-13 sem copiar o grupo antigo. |
| REQ-OBR-34 | Incluir links do repositório de código e do vídeo no relatório. | p. 6: “Links do repositório de código e do vídeo.” | Pendente | E05/E06: links finais de vídeo/PDF ainda não preenchidos. | Incluir links válidos de código e vídeo no PDF e verificar acesso com as permissões do avaliador. |
| REQ-OBR-35 | Incluir print do dashboard do Grafana no relatório. | p. 6: “Print do Dashboard do Grafana.” | Pendente | E05: nenhum print final do dashboard da Fase4. | Inserir no PDF captura legível do dashboard Grafana operando com dados atuais. |
| REQ-OBR-36 | Incluir print de trace distribuído no APM no relatório. | p. 6: “Print de um Trace distribuído no APM.” | Pendente | E05: resultado de traces local não substitui captura do APM. | Inserir no PDF print legível do trace distribuído no New Relic. |
| REQ-OBR-37 | Incluir print da notificação de incidente no ChatOps no relatório. | p. 6: “Print da notificação de incidente no ChatOps.” | Pendente | E05: nenhuma captura de notificação de incidente da Fase4. | Inserir no PDF print da notificação detalhada no Slack. |
| REQ-OBR-38 | Incluir print de log/execução da automação de Self-Healing no relatório. | p. 6: “Print do log/execução da automação de Self-Healing.” | Pendente | E05: nenhuma evidência visual de execução corretiva da Fase4. | Inserir no PDF print de log/execução da automação de self-healing. |
| REQ-OBR-39 | Explicar brevemente a arquitetura OTel implementada no relatório. | p. 6: “breve explicação da arquitetura do OTel implementada” | Pendente | E06/E07: arquitetura explicada no README e plano, mas PDF final ausente. | Incluir no PDF breve explicação da arquitetura OTel realmente implantada; corrigir divergência de roteamento do plano histórico. |
| REQ-OBR-40 | Justificar no relatório escolhas Datadog versus New Relic e OpsGenie versus PagerDuty. | p. 6: “escolha entre Datadog vs New Relic e OpsGenie vs PagerDuty” | Pendente | E07: escolhas New Relic/PagerDuty registradas; justificativa final no PDF ausente. | Explicar no PDF a escolha New Relic versus Datadog e PagerDuty versus OpsGenie com motivos aplicáveis/verificados. |
| REQ-OBR-41 | Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03. | p. 2: “em princípio, deve ser desenvolvida em grupo” | Confirmar | E07: usuário escolheu execução solo; PDF diz em princípio em grupo. | [INCERTO] Confirmar com tutor se entrega individual é aceita e registrar composição/anuência. Não tratar decisão pessoal como dispensa acadêmica. |
| REQ-OBR-42 | Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06. | p. 2: “Importante atentar-se ao prazo de entrega” | Confirmar | E06/E07: prazo informado pelo usuário2026-11-17; PDF não dá data/hora/canal. | [INCERTO] Confirmar prazo oficial, horário, canal e procedimento; submeter código/vídeo/PDF e guardar comprovante. Meta interna2026-11-12 não é prazo FIAP. |

## 6. Opções, sugestões e dúvidas

- REQ-BON-01/Alloy: alternativa opcional da p.4, sem pontuação adicional prometida. Não adotá-lo não é lacuna obrigatória; Collector padrão já escolhido.
- REQ-BON-02/bibliotecas OTel: preferência da p.4 já adotada nos cinco serviços. Não substitui o encaminhamento ao APM nem fecha os demais sinais.
- SUG-01/matriz+ensaio: matriz atual entregue nesta revisão; ensaio final completo pendente. SUG-02/janela/deduplicação: pendente. SUG-03/correlação: comprovada localmente, ainda precisa ser explorada nos backends. SUG-04/limites da automação e verificação: pendente. São sugestões, não obrigações extras.
- Permanecem14 questões no catálogo, sem equivaler a14 bloqueios. Q-03 (individual/grupo), Q-04 (acesso APM), Q-05/Q-06 (prazo/horário/canal), Q-13 (usernames) merecem confirmação. As escolhas EKS/ArgoCD, Slack, Collector padrão e OTel evitam parte das ambiguidades de alternativas.
- O PDF não exige3workers, arquitetura agent+gateway específica, janela5min, taxa5%, reinício do auth em particular, formato de nome de arquivo ou um diagrama separado. São decisões/exemplos, quando usados. O Service Map no APM é exigido.
- O enunciado p.5 prevê dedução por falta de demonstração/documentação; não fornece rubrica numérica por item. A data2026-11-17 vem do usuário, não do PDF; meta interna2026-11-12 também não é regra FIAP.

## 7. Lista de trabalho restante, na ordem sugerida

1. Tratar F-017/F-018 e escolher falha/sinal/mitigação coerentes. Atualizar o plano e a matriz com critérios de aceite; preservar as evidências locais concluídas.
2. Configurar conta New Relic e exportador no Collector, mantendo sanitização; demonstrar trace e Service Map ainda a partir do Compose. Não enviar chaves no chat/Git.
3. Implementar métricas e coleta/exportação de logs, preparar Prometheus/Loki/Grafana e seus charts/valores GitOps; incluir a regressão OTel no CI como melhoria.
4. Em paralelo, preparar contaAWS/backend/parâmetros/orçamento e acessos de observabilidade/incidentes. Validar planejamento antes do provisionamento autorizado.
5. Publicar a versão autorizada e implantar pela ordem base → imagens → cluster → k8s, completar schemas/chaves/outputs e stack. Comprovar CI/CD e fluxo funcional real, com os três sinais chegando aos backends.
6. Entregar dashboard com os três conteúdos exigidos; configurar alerta, abertura de incidente, acionamento do responsável e Slack; implementar self-healing ligado ao alerta e ensaiar a recuperação.
7. Coletar evidências de todos os requisitos, gravar vídeo≤25min, montar PDF com identificação/links/quatro prints/justificativas, testar acesso e realizar a submissão oficial. Confirmar grupo e procedimento antes do fechamento acadêmico.

Esta ordem é recomendação de execução, não autorização de deploy/publicação nem substituição das escolhas já registradas. A revisão não reabre AWS/New Relic/PagerDuty/Slack/GitHub Actions, já escolhidos pelo usuário.

## 8. Evidências e referências verificáveis

| Código | Fonte local | Data e uso |
|---|---|---|
| E01 | [Relatório do ensaio funcional](RELATORIO_PASSO1_REVALIDACAO_2026-10-27_v01.md) | Execução2026-10-27; baseline22 preservado. |
| E02 | [Resultados locais](RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json) e [relatório OTel](RELATORIO_PASSO2_OBSERVABILIDADE_LOCAL_2026-10-27_v01.md) | Provas do trace19, testes e limites do ambiente local. |
| E03 | [Revisão das aplicações](REVISAO_GERAL_APLICACOES_2026-10-28_v01.md) | Fontes/hashes/evidências e sonda de falhas executada27. |
| E04 | [Revisão de infraestrutura e CI](REVISAO_GERAL_INFRA_2026-10-28_v01.md) | Validações27; lacunas IaC/GitOps/CI e preparação de implantação. |
| E05 | [Revisão documental](REVISAO_GERAL_DOCUMENTACAO_2026-10-27_v01.md) | Inventário, integridade, guias, plano, links e entregáveis. |
| E06 | [README vigente](../../README.md) | Estado local/arquitetura planejada/limites. |
| E07 | [Decisões compartilhadas](../DECISOES.md) | D-009/D-012/D-014/D-016; escolhas e autorizações, sem presumir recursos ativos. |
| E08 | [Plano histórico v02](PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html) | Base de planejamento, com divergências registradas nesta revisão. |
| E09 | [Inventário inicial da revisão](qa-revisao-geral-2026-10-27/estado-inicial.json) |205hashes, Git local e alterações preexistentes; arquivoQA local ignorado. |

QA bruta preservada nas pastas `qa-revisao-geral-2026-10-27`, `qa-revisao-infra-2026-10-27`, `qa-revisao-aplicacoes-2026-10-27` e nas evidências do ensaio de27. A sonda de targeting é um teste observacional em cópia isolada, não uma alteração dos fontes oficiais. A [matriz JSON](MATRIZ_REQUISITOS_FASE4_2026-10-28_v01.json) permite conferir cobertura/contagens sem interpretar visualmente a tabela.

## 9. Verificação e handoff

Verificação final registrada em [resultado da revisão](VERIFICACAO_REVISAO_GERAL_2026-10-28_v01.json): conferir42IDs únicos, correspondência de fonte/citação com o catálogo, estados/contagens, links locais, preservação de205arquivos e28fontes de produção,39protegidos,33exclusões anteriores e referências Git. As evidências de execução conservam suas datas; nenhuma ausência de consulta externa foi convertida em afirmação de inexistência.

P-009 encerra a revisão, não a implementação da Fase4. P-003/P-002/E1–E7 continuam com as lacunas desta matriz. O próximo agente deve ler LOG/PENDENCIAS, este relatório e as três revisões setoriais. Não repetir a importação nem a instrumentação já concluídas; iniciar pelo achado/etapa autorizado pelo usuário. Código, planoHTML, catálogo e materiais originais permanecem preservados nesta auditoria.
