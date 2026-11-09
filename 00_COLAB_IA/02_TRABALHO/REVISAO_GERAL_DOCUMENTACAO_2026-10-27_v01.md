# Revisão geral — documentação, plano e evidências de entrega

TL;DR: o projeto tem requisitos rastreáveis e cinco guias íntegros, mas ainda não tem o vídeo, PDF e evidências operacionais finais da Fase 4. O README principal distingue adequadamente o ensaio local da implantação futura. O plano de setembro e os status do catálogo de requisitos precisam ser atualizados para refletir o avanço de outubro. Esta revisão não modifica fontes nem declara atendimento integral dos requisitos.

Última atualização: 2026-10-27, 22:35 (America/Sao_Paulo, UTC-03:00), Codex — agente revisor de documentação.

## 1. Escopo e método

- Leitura do protocolo compartilhado, backlog, topo do LOG e decisões/contexto pertinentes, do README principal e do README de requisitos inteiro.
- Revisão dirigida das seções didáticas, decisões, instrumentação, aceite, cronograma, riscos e entrega do plano HTML v02. Os desenhos SVG foram inspecionados por texto e estrutura; não houve nova revisão visual em navegador.
- Inspeção dos documentos históricos de arquitetura, reprodução e entrega da Fase 3 para distinguir referências antigas de evidências válidas da Fase 4. Não foi feita nova certificação de todos os comandos operacionais legados.
- Conferência SHA-256 dos 32 insumos do inventário original e dos 39 arquivos protegidos; execução do validador estático vigente dos cinco guias e do catálogo de requisitos.
- Verificação estática de 123 links locais em oito documentos Markdown, incluindo existência dos arquivos e âncoras Markdown/HTML. Endereços externos não foram acessados.
- Inventário da documentação de entrega disponível. Nenhum comando AWS, publicação Git, implantação, notificação ou ensaio funcional foi executado por este revisor.

Os detalhes de código e infraestrutura são objeto dos relatórios paralelos. A matriz consolidada de todos os 42 obrigatórios será produzida pelo agente principal, que também relê o enunciado integral. As páginas citadas abaixo correspondem ao mapeamento existente no catálogo; a conferência independente do PDF cabe à consolidação.

## 2. Inventário e validação atual

| Grupo | Quantidade observada em 2026-10-27 | Resultado |
|---|---:|---|
| Pastas de módulos da Fase 4 | 5 | Correspondem ao inventário esperado |
| PDFs das aulas | 31 | Todos no inventário e íntegros |
| Enunciado da Fase 4 | 1 | Íntegro; 7 páginas segundo o inventário |
| Guias de estudo HTML | 5 | Um por módulo, íntegros |
| Catálogo e espelho de requisitos | 2 | README e REQUISITOS.html íntegros |
| Arquivos protegidos | 39 | Nenhuma alteração SHA-256 contra o manifesto da importação |
| Requisitos obrigatórios | 42 | IDs únicos 01–42 |
| Opções/preferências chamadas de bônus | 2 | O catálogo não promete pontuação extra |
| Sugestões autorais | 4 | Separadas das exigências FIAP |
| Questões Q-01 a Q-14 | 14 | Dúvidas documentadas; não equivalem a 14 bloqueios atuais |

**Atenção à contagem:** os “32 originais” são 31 PDFs de aulas mais o enunciado, e não 32 PDFs de aulas.

| Módulo | PDFs | Guias | Resultado estático |
|---|---:|---:|---|
| 00.Welcome to Observabilidade e Monitoramento | 1 | 1 | 0 erros |
| 01.Observabilidade e Monitoramento | 5 | 1 | 0 erros |
| 02.Monitoramento Opensource | 8 | 1 | 0 erros |
| 03.APM | 10 | 1 | 0 erros |
| 04.Automação de incidentes | 7 | 1 | 0 erros |

O comando `validar-guias-2026-09-16_v01.py` foi relido antes da execução e não grava arquivos. A execução atual terminou com código 0 e “Total de erros: 0”. Verifica, entre outros pontos, estrutura HTML, UTF-8, idioma, âncoras, referências de páginas, IDs citados e marcadores de rascunho. Não representa revalidação semântica integral de todas as aulas nem prova de responsividade visual nesta sessão.

Fontes: `inventario-fontes-2026-09-16_v01.json`; `preservacao-importacao-2026-10-20_v01.json`; `validar-guias-2026-09-16_v01.py`, em `00_COLAB_IA/02_TRABALHO/`. Os arquivos originais não foram alterados.

## 3. O que a documentação já comprova

1. **Escopo da FIAP mapeado:** `docs/requisitos/README.md:49` inicia a tabela com evidências das páginas 2–6; os 42 itens têm identificação e fonte. As opções de Alloy e bibliotecas OTel estão separadas das obrigações (`:93`).
2. **Estado atual legível:** `README.md:5` informa resultado local e pendências; `:25` declara ausência dos links finais de vídeo/relatório. `:181` descreve o ensaio de 19 spans e explicita que New Relic não foi validado.
3. **Planejado versus executado:** `README.md:92` apresenta a arquitetura do EKS como futura; `:123` informa que janela/limiar/cenário/alvo ainda serão definidos. O leitor não deveria interpretar esses diagramas como implantação existente.
4. **Histórico separado:** `README.md:230` e a primeira linha de `docs/ARQUITETURA.md`, `docs/GUIA_DE_REPRODUCAO.md` e `docs/RELATORIO_DE_ENTREGA.md` classificam esses materiais como Fase 3. Os links de CI e ArgoCD antigos não comprovam execução do repositório 04.
5. **Prazo com origem explícita:** `README.md:25` atribui 2026-11-17 ao responsável e informa que a data não está no PDF. A meta interna do plano é 2026-11-12, em `PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html:1082`.

Documentação de estudo e plano de arquitetura são entregas internas úteis; não substituem a evidência operacional exigida pelo REQ-OBR-23.

## 4. Achados e correções documentais recomendadas

### DOC-01 — Status de requisitos ainda não expressa o progresso real

**Evidência:** `docs/requisitos/README.md:5` tem data 2026-09-20; `:14` informa todos os requisitos Pendente; as tabelas e o checklist permanecem nessa condição. Em contraponto, `README.md:5` e `:181` registram a instrumentação e os testes de outubro.

**Impacto:** o catálogo serve bem como referência normativa, mas não é hoje um painel de execução. Um leitor pode concluir que nenhum trabalho foi realizado ou, no sentido inverso, confundir a conclusão dos guias com a entrega operacional.

**Ação:** publicar a matriz atual de implementação/evidência/falta por requisito e ligar o catálogo a ela. Se o catálogo e seu espelho forem atualizados futuramente, preservar a versão anterior e regenerar o HTML pela fonte apropriada. Não marcar trace/APM/entrega como concluídos apenas pela prova local.

### DOC-02 — Plano v02 preserva um cenário anterior à importação e à instrumentação

**Evidências no plano:** `:87` data/estado de 2026-09-23; `:143` menciona 55 dias; `:1086` inicia o calendário em setembro; `:657` prevê `otelsql`; `:662` prevê instrumentação `botocore`; `:947` repete `otelsql` no inventário de alterações. A D-016 atual registra spans manuais onde aplicável e o fechamento local.

**Impacto:** seguir literalmente o plano pode repetir trabalho concluído ou acrescentar instrumentação redundante. Os preços/planos comerciais citados são consultas históricas, não disponibilidade atual confirmada.

**Ação:** produzir versão nova, preservando a v02, com E0/E1 parciais e passos locais concluídos, bibliotecas efetivas, cronograma atual e dependências reais. Consultas comerciais e de custo devem ser atualizadas quando forem orientar contratação/provisionamento; não extrapolar valores de setembro.

### DOC-03 — Critérios de aceite incompletos em E0/E2/E4

**Evidência:** o plano `:978` pede CI verde para E0, ainda sem prova remota no 04. E2 em `:1005` considera os cinco pods Running e ArgoCD Synced. E4 em `:1032` menciona incidente aberto e mensagens/disparo, mas não explicita a confirmação do acionamento do responsável. A síntese em `:1076` omite o REQ-OBR-12, embora ele esteja alocado na E0 em `:979`.

**Impacto:** aprovação por estado visual de pod/sincronização pode deixar falha de autenticação, banco, fila ou regra sem diagnóstico. Abrir incidente não comprova que o time foi acionado, objetivo registrado no REQ-OBR-17.

**Ação:** incluir o ensaio funcional dos cinco serviços no cluster, comprovação de CI/CD real, ingestão e mapa APM, e acionamento humano pelo PagerDuty. Corrigir a síntese de cobertura do 12 sem criar requisito novo. A conferência de 2026-10-21 já apontava parte dessas lacunas.

### DOC-04 — Formulação absoluta sobre telemetria conflita com o próprio desenho

**Evidência:** plano `:282` diz “Todo sinal passa pelo OTel Collector”, enquanto `:142` e `:748` descrevem CPU/memória coletadas diretamente pelo Prometheus. O README atual `:121` já distingue os caminhos.

**Impacto:** explicação imprecisa do roteamento na gravação ou no PDF (REQ-OBR-26/39).

**Ação:** na nova versão do plano, distinguir telemetria dos microsserviços centralizada no Collector de scrape dos exporters de infraestrutura. Preservar a divergência histórica nesta revisão, sem editar unilateralmente o plano original.

### DOC-05 — Dois links históricos perderam âncoras

**Evidência:** `docs/GUIA_DE_REPRODUCAO.md:9` aponta a `../README.md#8-custo`; `docs/ARQUITETURA.md:7` aponta a `../README.md#5-decisões-e-o-porquê`. Essas seções não existem no README atual. Os avisos de contexto histórico continuam presentes.

**Impacto:** baixo, restrito à navegação de referências legadas; não impede abrir os arquivos nem demonstra descumprimento de um requisito FIAP.

**Ação:** ao revisar a documentação histórica, encaminhar essas referências para a cópia histórica correspondente ou explicitar que a seção mudou, preservando a fonte original conforme o protocolo do projeto.

Resultado da inspeção dos oito Markdown: 123 links locais, dois problemas de âncora e nenhum arquivo de destino inexistente. README principal (27 links) e catálogo de requisitos (seis links) sem falhas locais nessa verificação. Não houve verificação HTTP de links externos.

## 5. O que falta para a documentação e entrega da Fase 4

| Requisitos | Obrigação do enunciado | Situação documental e ação faltante |
|---|---|---|
| 20–22 | Código IaC/GitOps, instrumentação e automação no repositório, p. 5 | A instrumentação existe localmente segundo os relatórios atuais. Consolidar implementação restante, publicação futura autorizada e acesso do avaliador. Configuração local não é entrega remota comprovada. |
| 23 | Evidenciar funcionamento, p. 5 | Criar matriz final com evidência atual por requisito, telas/artefatos e localização no vídeo/PDF. Provas de 2026-09 da Fase 3 não fecham a Fase 4. |
| 24 | Vídeo de até 25 min, p. 5 | Não foi localizado vídeo/URL final da Fase 4. Preparar roteiro, ensaio cronometrado, gravação e link acessível. |
| 25–26 | Cluster/ArgoCD/stack, dashboard, busca Loki e explicação Collector, p. 5 | Registrar demonstração real após implantação; diagramas e guias não substituem telas operacionais. |
| 27 | Service Map, requisição e trace no APM, p. 6 | Capturar New Relic real; o arquivo local de spans ainda não comprova a tela APM. |
| 28–31 | Falha proposital, Firing, incidente/ChatOps e ação corretiva, p. 6 | Implementar/ensaiar o ciclo e gravá-lo. A evidência antiga de ArgoCD selfHeal não é a automação reativa ao alerta exigida nesta fase. |
| 32 | Relatório PDF, p. 6 | Não foi localizado PDF final da Fase 4. Os relatórios atuais em Markdown são registros técnicos, não esse entregável. |
| 33–34 | Identificação e links, p. 6 | Confirmar participantes e usernames pertinentes; preencher links finais de código/vídeo e testar acesso. Não copiar automaticamente o grupo da Fase 3. |
| 35–38 | Quatro prints: Grafana, trace APM, ChatOps e execução corretiva, p. 6 | Capturar evidências novas após a operação. A imagem de custos e apresentação da Fase 3 não atendem estes quatro itens. |
| 39–40 | Arquitetura OTel e justificativas APM/incidentes, p. 6 | Aproveitar a explicação do README, ajustando-a ao que de fato for implantado, e incluir no PDF final. |
| 41 | Grupo, por leitura conservadora de “em princípio”, p. 2 | [INCERTO] Confirmar aceitação da execução individual/composição da entrega com tutor; decisão de trabalhar solo não é autorização acadêmica comprovada. |
| 42 | Entrega no prazo, p. 2 | 2026-11-17 foi informado pelo usuário; confirmar horário/canal/procedimento/acesso aos links e registrar submissão. O PDF não contém a data absoluta. |

Questões ainda relevantes para fechar a entrega: Q-03 (individual/grupo), Q-04 (acesso APM), Q-05/Q-06 (data/hora/canal), Q-13 (plataforma dos usernames). As demais devem ser resolvidas por implementação aderente ou tutor quando afetarem o aceite. A escolha atual de EKS/ArgoCD, Slack, Collector padrão e OTel reduz a relevância prática das dúvidas sobre alternativas, sem apagar o histórico.

O “bônus” Alloy é opcional, não algo faltante para concluir o projeto. Bibliotecas OTel já foram adotadas na implementação registrada; a preferência não substitui ingestão/APM nem promete pontos adicionais. As quatro SUG são recomendações autorais, não obrigações extras da FIAP.

## 6. Fontes examinadas e limites

Principais arquivos: `00_COLAB_IA/LEIA-PRIMEIRO.md`; PENDENCIAS, LOG, DOSSIE e DECISOES vigentes; `README.md`; `docs/requisitos/README.md`; plano v02 e conferência de cobertura de 2026-10-21; relatórios/resultados locais de 2026-10-27; `terraform/README.md`; `gitops/README.md`; `observability/README.md`; três documentos legados em `docs/`; inventário, manifesto e validador de guias.

Inventário de entrega legado: `docs/RELATORIO_DE_ENTREGA.md`, `docs/apresentacao/ToggleMaster_Fase3.pptx`, `docs/evidencias/estimativa-custos-aws-2026-09-11.png` e `docs/POSTECH - Tech Challenge - Fase 3.pdf`. Seus nomes/conteúdo/contexto os identificam como Fase 3; não foram contabilizados como entregáveis finais da Fase 4. Não foram reabertos todos os slides nem reavaliada a rubrica antiga.

As aulas não foram relidas integralmente nesta revisão de implementação. Integridade e validação estrutural atuais preservam as análises de estudo existentes, mas não substituem uma nova auditoria semântica aula a aula. Não foram consultados Billing, contas externas, branch remota, execução atual de CI ou permissões de links; esses itens permanecem não comprovados nesta revisão.

## 7. Handoff

Este relatório é uma contribuição documental à revisão consolidada; não altera status dos 42 requisitos nem o plano original. O próximo agente deve usar a matriz consolidada para registrar implementação versus evidência e, posteriormente, atualizar plano/catálogo/espelho com versões preservadas. Não repetir importação nem instrumentação concluída. Continuar na dev, com limites de publicação/implantação já registrados.
