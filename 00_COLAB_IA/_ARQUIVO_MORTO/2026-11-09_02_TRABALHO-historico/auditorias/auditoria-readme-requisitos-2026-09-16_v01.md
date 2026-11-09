# Auditoria adversarial — docs/requisitos/README.md (Fase A)

- Data: 2026-09-16
- Auditor: Claude (Opus 5)
- Documento auditado: `docs/requisitos/README.md` (autoria Codex, "Última atualização: 2026-09-16"). Somente leitura; não foi editado.
- Fonte normativa: `POSTECH - Tech Challenge - Fase 4.pdf` (raiz do repositório, 7 páginas). Somente leitura.

## 1. Veredito

**Correções menores.** Nenhum achado de gravidade alta.

A fidelidade central está preservada:

- as 43 evidências (41 REQ-OBR + 2 REQ-BON) aparecem literalmente na página citada;
- as contagens 41/2/4 conferem;
- o checklist tem 41 checkboxes, um por REQ-OBR, com texto idêntico ao da tabela;
- nenhuma SUG é apresentada como exigência;
- nenhuma regra é atribuída à FIAP sem apoio no PDF.

Há **4 achados médios**:

- um requisito sem ID: prazo e submissão;
- a coluna "Módulo(s)" está vazia, embora o PDF indique as disciplinas;
- faltam duas dúvidas relevantes: agente do fornecedor × Collector; disponibilidade de conta em PagerDuty/OpsGenie.

Há também **15 achados baixos**: redação, contexto, §4, §8, granularidade e §11.

Se as correções forem aceitas:

- o TL;DR passa a **42 obrigatórios** (achado 1);
- a §10 passa a ter as perguntas **Q-01 a Q-14** (achados 3 a 8).

## 2. Método

1. Renderizei as páginas 1–7 na escala 1,5 (`00_COLAB_IA/02_TRABALHO/qa-enunciado/enun-p01.png` … `enun-p07.png`) e inspecionei cada imagem. A inspeção cobriu:
   - capa (p. 1) e contracapa (p. 7);
   - negritos e itálicos;
   - a nota em caixa da p. 4;
   - a "REGRA DE AVALIAÇÃO" em vermelho na p. 5;
   - os sub-bullets "o" das p. 3 e 6.
2. Li as p. 2–6 frase a frase e bullet a bullet, comparando cada item com as seções do README (matriz na seção 5).
3. Comparei as evidências por script. Cada trecho foi confrontado com o texto PDFium da página citada, em dois modos:
   - (a) espaços normalizados;
   - (b) modo estrito: apenas quebra de linha → espaço e aspas curvas → retas.

   Também confirmei que os dois arquivos estão em Unicode NFC.
4. Por script, contei os IDs e os checkboxes e comparei o texto do checklist com o da tabela, linha a linha.

## 3. Achados

Gravidade: alta = pode levar à perda de pontos ou a erro de classificação; média = lacuna relevante de conteúdo ou de decisão; baixa = precisão, clareza ou completude secundária.

| nº | tipo | gravidade | descrição | evidência (p. + trecho) | correção proposta (texto pronto) |
|---|---|---|---|---|---|
| 1 | Omissão de requisito | média | O PDF pede atenção ao prazo de uma atividade obrigatória. Não existe REQ-OBR nem checkbox para submeter a entrega: o tema só aparece na §4 e em Q-05/Q-06. O "Checklist final de entrega" pode ser todo marcado sem que a submissão ocorra. | p. 2: “Importante atentar-se ao prazo de entrega, pois trata-se de uma atividade obrigatória” | **§5, nova linha (âncora `req-obr-42`):** REQ-OBR-42 \| Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06. \| p. 2: “Importante atentar-se ao prazo de entrega” \| Entrega (transversal) \| Pendente<br>**§9, novo item:** - [ ] **REQ-OBR-42** — Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06.<br>**TL;DR:** trocar "41 obrigatórios" por "42 obrigatórios". |
| 2 | Omissão / formato | média | A coluna "Módulo(s) relacionado(s)" está como "a mapear" nas 43 linhas das §5 e §6. Porém, o próprio PDF indica as disciplinas de cada bloco técnico, e a §7 já usa nomes de módulos, o que gera inconsistência interna. As quatro linhas "(Disciplinas: …)" não aparecem em nenhuma seção do README. | p. 3: “(Disciplinas: Prometheus, Grafana, Loki, Observabilidade no Kubernetes)”; p. 4: “(Disciplinas: OpenTelemetry (OTel) e Alloy)”; p. 4: “(Disciplinas: APM, Instrumentação, Datadog ou New Relic)”; p. 4: “(Disciplinas: Alert Fatigue, PagerDuty/OpsGenie, ChatOps, Runbook Automation, Self-Healing)” | **Preencher a coluna (mapeamento preliminar, a validar na Fase B com a cobertura dos guias):**<br>• REQ-OBR-01 a 05: "Fases 1–3 (base anterior)"<br>• 06 a 10: "02.Monitoramento Opensource"<br>• 11: "02.Monitoramento Opensource; 01.Observabilidade e Monitoramento"<br>• 12, 14, 15: "03.APM"<br>• 13: "03.APM; 02.Monitoramento Opensource"<br>• 16: "02.Monitoramento Opensource; 03.APM; 04.Automação de incidentes; 01.Observabilidade e Monitoramento"<br>• 17 a 19: "04.Automação de incidentes"<br>• 20: "02.Monitoramento Opensource"<br>• 21: "03.APM; 02.Monitoramento Opensource"<br>• 22: "04.Automação de incidentes"<br>• 23, 24, 32, 33, 34, 41: "Entrega (transversal)"<br>• 25: "Fases 1–3 (base anterior); 02.Monitoramento Opensource"<br>• 26, 35, 39: "02.Monitoramento Opensource"<br>• 27, 36: "03.APM"<br>• 28, 30, 31, 37, 38: "04.Automação de incidentes"<br>• 29: "02.Monitoramento Opensource; 03.APM; 04.Automação de incidentes"<br>• 40: "03.APM; 04.Automação de incidentes"<br>• REQ-BON-01: "02.Monitoramento Opensource"<br>• REQ-BON-02: "03.APM; 02.Monitoramento Opensource"<br>**Acrescentar ao fim da §8:** "Disciplinas indicadas pelo PDF: bloco 1 (p. 3) Prometheus, Grafana, Loki, Observabilidade no Kubernetes; bloco 2 (p. 4) OpenTelemetry (OTel) e Alloy; bloco 3 (p. 4) APM, Instrumentação, Datadog ou New Relic; bloco 4 (p. 4) Alert Fatigue, PagerDuty/OpsGenie, ChatOps, Runbook Automation, Self-Healing." |
| 3 | Dúvida ausente | média | Há uma tensão não registrada. De um lado, as bibliotecas OTel são apenas preferenciais e basta alterar o Dockerfile. De outro, os microsserviços "devem" enviar telemetria ao OTel, e o Collector roteia para o APM. O README não pergunta se vale o agente ou SDK do fornecedor (Datadog/New Relic) enviando direto ao APM. Também não pergunta se a instrumentação feita só no Dockerfile satisfaz "Código fonte das aplicações atualizado". A §6 afirma a conclusão sem [INCERTO]. | p. 4: “Os microsserviços devem enviar os dados de telemetria para o OTel”; p. 4: “altere o código-fonte ou o Dockerfile”; p. 5: “Código fonte das aplicações atualizado com a instrumentação.” | **§10, nova linha:** Q-08 \| O agente ou a biblioteca do fornecedor (Datadog/New Relic), ou a instrumentação feita apenas no Dockerfile, é aceita se a telemetria passar pelo OTel Collector? O envio direto do agente ao APM, sem o Collector, é aceito? \| p. 4 torna as bibliotecas OTel preferenciais, mas exige o envio da telemetria ao OTel e o roteamento pelo Collector; p. 5 pede código fonte atualizado. REQ-OBR-11, 13 e 21 mantidos conservadoramente.<br>**Acrescentar "Ver Q-08."** ao fim de REQ-OBR-11 (tabela e checklist) e de REQ-BON-02. |
| 4 | Dúvida ausente | média | Q-04 trata só da conta educacional de APM. Nada é perguntado sobre a conta em PagerDuty/OpsGenie, que o PDF exige explicitamente. **Informação externa, fora do PDF, a confirmar em fonte oficial antes de usar:** a Atlassian anunciou em 2025 o encerramento da venda do Opsgenie a novos clientes, o que pode inviabilizar uma das duas alternativas. | p. 5: “crie uma conta no PagerDuty OU OpsGenie” | **§10, nova linha:** Q-09 \| Se não for possível criar conta nova em uma das ferramentas de incidentes (por exemplo, OpsGenie), a outra passa a ser a única opção aceita, ou existe alternativa aceita? \| p. 5 exige conta no PagerDuty OU OpsGenie; disponibilidade dos planos gratuitos não verificada no enunciado.<br>**Acrescentar "Ver Q-09."** a REQ-OBR-17 (tabela e checklist). Não registrar o anúncio externo como regra FIAP. |
| 5 | Dúvida ausente | baixa | O Alloy no lugar do Collector é opcional, mas os entregáveis nomeiam "OTel Collector": código IaC/GitOps e explicação no vídeo. Não está registrado se mostrar o Alloy atende a esses itens. | p. 4: “O uso do Grafana Alloy no lugar do OTel Collector padrão é opcional.”; p. 5: “Explique rapidamente como o OTel Collector está roteando esses dados.” | **§10, nova linha:** Q-10 \| Com o Grafana Alloy no lugar do OTel Collector, os entregáveis que citam o Collector (REQ-OBR-20 e REQ-OBR-26) ficam atendidos mostrando o Alloy? \| p. 4 torna o Alloy opcional; p. 5 nomeia o OTel Collector no código e no vídeo.<br>**Acrescentar "Ver Q-10."** a REQ-BON-01. |
| 6 | Interpretação sem [INCERTO] na §4 | baixa | A §4 deveria trazer só o que o PDF diz. A linha 39, porém, contém uma leitura interpretativa ("O 'ou' na regra geral de evidência não os torna intercambiáveis") sem [INCERTO] e sem pergunta. A regra literal fala em demonstrar "no vídeo ou" documentar "no relatório". | p. 5: “claramente demonstrado no vídeo ou documentado no relatório” | **Substituir a linha 39 da §4 por:** "- O PDF lista itens específicos para o vídeo (p. 5–6) e para o relatório (p. 6), e a regra geral fala em demonstração 'no vídeo ou' documentação 'no relatório' (p. 5). [INCERTO]: por leitura conservadora, este documento trata os dois conjuntos como exigidos; Q-11."<br>**§10, nova linha:** Q-11 \| Um requisito demonstrado só no relatório (ou só no vídeo) evita a dedução, ou os subitens específicos de cada entregável são exigidos separadamente? \| p. 5: regra geral com "ou"; p. 5–6: listas específicas de vídeo e de relatório. |
| 7 | Dúvida / alerta ausente | baixa | Os exemplos do PDF não formam um cenário único. O alerta de exemplo mede 5xx do auth-service e a automação reinicia o auth-service; a falha de exemplo do vídeo para o banco do flag-service. Como a automação reage "ao alerta criado", combinar os exemplos ao pé da letra pode não disparar a cadeia. A §8 lista os exemplos sem essa ressalva. | p. 5: “reaja automaticamente ao alerta criado”; p. 6: “pare o banco de dados do flag-service” | **§8, após o parágrafo "Exemplos, não prescrições", acrescentar:** "Os exemplos não formam, sozinhos, um cenário único: o alerta e a reinicialização citam o auth-service (p. 5), e a falha proposital cita o flag-service (p. 6). Pela sequência da p. 6 e pelo vínculo da automação ao alerta criado (p. 5), a falha escolhida para o vídeo deve acionar o alerta configurado. [INCERTO]; Q-12."<br>**§10, nova linha:** Q-12 \| A falha proposital do vídeo precisa acionar o mesmo alerta e a mesma automação configurados, ou podem ser cenários distintos? \| p. 5 vincula a automação "ao alerta criado"; p. 6 usa exemplo de falha em outro serviço. |
| 8 | Dúvidas ausentes | baixa | Dois termos ficam sem definição no PDF e sem pergunta no README: "usernames" (não diz de qual plataforma) e "alerta inteligente" (não diz o que o caracteriza). A nota final da §10 trata só de parâmetros como a janela do alerta. | p. 6: “Nomes, RMs e usernames.”; p. 5: “configure um alerta inteligente” | **§10, novas linhas:**<br>Q-13 \| Os usernames do relatório são de qual plataforma (portal FIAP, GitHub, Discord)? \| p. 6 não especifica.<br>Q-14 \| Que característica torna o alerta "inteligente" para a avaliação? \| p. 5 dá apenas um exemplo (taxa de 5xx maior que 5% no auth-service); a disciplina Alert Fatigue consta na p. 4. |
| 9 | Justificativa de classificação ausente | baixa | O PDF marca "(Obrigatório)" em apenas três itens. Os demais (APM, Service Map, alerta, incidentes, ChatOps etc.) estão corretamente classificados como obrigatórios, mas o README não explica o motivo. Sem isso, um leitor pode tratá-los como opcionais. | p. 4: “OTel Collector (Obrigatório)”; p. 5: “Self-Healing (Obrigatório)”; p. 6: “Evidências Visuais (Obrigatório)”; p. 5: “É obrigatório evidenciar o funcionamento de todas as métricas, configurações e requisitos” | **Acrescentar à introdução da §5:** "O PDF rotula como '(Obrigatório)' apenas o OTel Collector (p. 4), o Self-Healing (p. 5) e as Evidências Visuais (p. 6). Os demais itens também são obrigatórios: usam linguagem imperativa ('deve', 'crie', 'configure', 'escolha') e a REGRA DE AVALIAÇÃO (p. 5) exige evidenciar todos os requisitos, com dedução direta de pontos." |
| 10 | Omissão parcial | baixa | O objetivo narrado diz que o time "deve ser acordado" pela ferramenta de incidentes. REQ-OBR-17 cobre só a abertura do incidente, sem mencionar o acionamento do time. | p. 3: “o time deve ser acordado pelo PagerDuty/OpsGenie” | **Substituir o texto de REQ-OBR-17 (tabela e checklist) por:** "Criar conta no PagerDuty OU OpsGenie e integrar o alerta para abrir incidente automaticamente, com a ferramenta acionando o time (objetivo da p. 3). Ver Q-09." |
| 11 | Redação imprecisa | baixa | Três requisitos perdem nuances do PDF:<br>• REQ-OBR-05 diz "Kubernetes gerenciado via GitOps", mas no PDF quem é gerenciada via GitOps é a *implantação*;<br>• REQ-OBR-08 omite "indexação";<br>• REQ-OBR-10 omite que o dashboard é "no Grafana" e que deve centralizar "a saúde do ecossistema". | p. 2: “Implantação no Kubernetes (EKS, GKE, AKS) gerenciada via GitOps”; p. 3: “centralização e indexação de todos os logs”; p. 3: “1 Dashboard customizado no Grafana que centralize a saúde do ecossistema” | **Tabela e checklist:**<br>• REQ-OBR-05 → "Implantar no Kubernetes (EKS, GKE ou AKS), com a implantação gerenciada via GitOps (ArgoCD/Flux). Ver Q-01."<br>• REQ-OBR-08 → "Usar Loki para centralizar e indexar todos os logs dos contêineres do cluster."<br>• REQ-OBR-10 → "Criar no Grafana ao menos um dashboard customizado que centralize a saúde do ecossistema: uso de recursos do cluster, taxa de requisições dos microsserviços e painel de logs em tempo real." |
| 12 | Afirmação imprecisa (§3) | baixa | Na linha do vídeo, "Stack e base funcionando" sugere demonstrar toda a base: cinco serviços, Terraform e CI/CD. No vídeo, o PDF pede apenas o cluster EKS (IaC) e o ArgoCD (GitOps) rodando com a nova stack. Com limite de 25 min, a generalização induz a gastar tempo com o que não é pedido. | p. 5: “mostre que o cluster EKS (IaC) e o ArgoCD (GitOps) continuam rodando com a nova stack” | **Substituir a célula "Conteúdo exigido" do vídeo por:** "Cluster EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack (Q-01); Grafana com dashboard, busca no Loki e explicação do roteamento OTel; Service Map, requisição de teste e trace distribuído; falha proposital → Firing → incidente/notificação → execução corretiva" |
| 13 | Afirmação imprecisa (TL;DR) | baixa | "Escolha Datadog ou New Relic para instrumentação" atribui a instrumentação à ferramenta APM. O PDF manda alterar o código ou o Dockerfile, preferencialmente com bibliotecas OpenTelemetry; o APM é o destino do tracing e do Service Map. Além disso, o TL;DR chama de "opções/preferências" a categoria pedida como "bônus", o que dificulta conferir o 41/2/4. | p. 4: “preferencialmente utilizando as bibliotecas do OpenTelemetry”; p. 4: “o painel do APM deve exibir o mapa de dependências” | **Linha 10:** "Escolha Datadog ou New Relic como APM para exibir o tracing distribuído e o mapa dos cinco serviços; a instrumentação é feita no código ou no Dockerfile, preferencialmente com bibliotecas OpenTelemetry."<br>**Linha 14:** "Este documento contém **41 obrigatórios, 2 bônus (opções/preferências do PDF, sem pontuação extra prometida) e 4 sugestões autorais**." (usar 42 se o achado 1 for aceito) |
| 14 | Afirmação imprecisa (§4) | baixa | "Discord aparece apenas como canal para dúvidas" é literalmente falso: o Discord também é opção de ChatOps nas p. 5 e 6. | p. 5: “um canal do Slack, Discord ou Teams”; p. 6: “podem nos chamar no Discord” | **Substituir a linha 37 por:** "- Não informa plataforma nem procedimento de submissão (Q-06). Como canal de contato com a FIAP, o Discord aparece apenas para dúvidas (p. 6); nas p. 5–6 ele também é opção de ChatOps." |
| 15 | Atribuição além do PDF (§8) | baixa | Duas afirmações da §8 vão além do texto do PDF:<br>• chamar o Alloy de "distribuição", termo que o PDF não usa;<br>• "O requisito exige respeitar cada sinal e demonstrar seu trajeto": o PDF pede que o Collector roteie aos backends corretos, que o roteamento seja explicado no vídeo e que a arquitetura seja explicada no relatório, não que o trajeto de cada sinal seja demonstrado. | p. 4: “O uso do Grafana Alloy no lugar do OTel Collector padrão é opcional.”; p. 5: “Explique rapidamente como o OTel Collector está roteando esses dados.” | **Célula "Classificação" (Transporte/roteamento):** "Collector como peça central é obrigatório; Alloy no lugar do Collector padrão é opcional (p. 4)".<br>**Substituir a 2ª frase do parágrafo do fluxo conceitual por:** "O PDF exige que o Collector roteie os sinais aos backends corretos (p. 4), que o roteamento seja explicado no vídeo (p. 5) e que a arquitetura OTel seja explicada no relatório (p. 6); isso não implica que todo backend aceite qualquer sinal." |
| 16 | Omissão (§8) | baixa | A tabela de arquitetura deixa de fora elementos citados no PDF:<br>• HPA;<br>• evaluation-service, único serviço nomeado para o trace obrigatório;<br>• código-fonte/Dockerfile e bibliotecas OpenTelemetry como meios de instrumentação;<br>• Distributed Tracing e Service Map;<br>• o exemplo "pod reiniciando automaticamente via terminal", que falta na lista de exemplos. | p. 2: “escalava automaticamente (HPA)”; p. 4: “requisição no evaluation-service”; p. 6: “mostrando o pod reiniciando automaticamente via terminal” | **Novas linhas na tabela da §8:**<br>Instrumentação \| Código-fonte ou Dockerfile; bibliotecas OpenTelemetry da linguagem \| Instrumentação obrigatória; bibliotecas OTel preferenciais (p. 4)<br>Visibilidade no APM \| Distributed Tracing (requisição no evaluation-service); Service Map dos 5 microsserviços \| Obrigatórios (p. 4)<br>Contexto do incidente narrado \| evaluation-service; HPA \| Contexto, não requisito (p. 2)<br>**No parágrafo de exemplos, acrescentar:** "mostrar o pod reiniciando automaticamente via terminal (p. 6)". |
| 17 | Omissão (§2) | baixa | O contexto técnico omite o mecanismo do incidente narrado: falha silenciosa do evaluation-service e aumento de consumo causado pelo HPA. Omite também o objetivo "Observabilidade Total e Resposta Ativa" e a relação entre problema e resposta: lentidão → trace; erro → logs; limite → plantão; e autocorreção. Já o texto leigo generaliza um evento único ("descobre falhas pelos usuários"). | p. 2: “começou a falhar silenciosamente”; p. 3: “Precisamos de Observabilidade Total e Resposta Ativa.” | **Leigo, substituir a 1ª frase por:** "Num fim de semana, um serviço passou a falhar sem gerar aviso; a equipe só soube pelos usuários 6 horas depois e levou mais 4 horas para achar a causa nos logs espalhados pelos pods (p. 2–3)."<br>**Técnico, acrescentar:** "O evaluation-service falhou silenciosamente e o HPA escalou recursos para compensar (p. 2). O objetivo declarado é 'Observabilidade Total e Resposta Ativa': trace para lentidão, logs centralizados para erro, acionamento por PagerDuty/OpsGenie ao atingir um limite e Self-Healing (p. 3)." |
| 18 | Granularidade do checklist | baixa | Alguns REQ-OBR reúnem várias verificações independentes num único checkbox, o que permite marcar como concluído algo atendido só em parte:<br>• REQ-OBR-10: três painéis;<br>• REQ-OBR-26: quatro ações;<br>• REQ-OBR-27: três ações;<br>• REQ-OBR-30: incidente e notificação, em ferramentas distintas. | p. 3: “uso de recursos do cluster, taxa de requisições dos microsserviços e painel de logs em tempo real”; p. 6: “Mostre o incidente sendo aberto no PagerDuty/OpsGenie e a notificação chegando no Slack/Discord.” | **Sem mudar IDs nem contagens, enumerar critérios no texto (tabela e checklist).** Exemplo para REQ-OBR-30: "No vídeo: (a) mostrar o incidente sendo aberto no PagerDuty/OpsGenie; (b) mostrar a notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02." Aplicar o mesmo padrão (a), (b), (c) a REQ-OBR-10, 26 e 27. |
| 19 | Seção incompleta (§11) | baixa | A §11 diz que o índice será preenchido na Fase B, mas já existem três guias no repositório, ainda não rastreados pelo git (módulos 00, 01 e 02). Não é falha de fidelidade ao PDF; é uma pendência de estado. | Repositório (não PDF): `docs/aulas-fiap/00.Welcome to Observabilidade e Monitoramento/GUIA-ESTUDO-Welcome-to-Observabilidade-e-Monitoramento.html`; `docs/aulas-fiap/01.Observabilidade e Monitoramento/GUIA-ESTUDO-Observabilidade-e-Monitoramento.html`; `docs/aulas-fiap/02.Monitoramento Opensource/GUIA-ESTUDO-Monitoramento-Opensource.html` | **Quando os guias forem aprovados, substituir a §11 por:** "Guias disponíveis (em revisão): [00 — Welcome](../aulas-fiap/00.Welcome%20to%20Observabilidade%20e%20Monitoramento/GUIA-ESTUDO-Welcome-to-Observabilidade-e-Monitoramento.html); [01 — Observabilidade e Monitoramento](../aulas-fiap/01.Observabilidade%20e%20Monitoramento/GUIA-ESTUDO-Observabilidade-e-Monitoramento.html); [02 — Monitoramento Opensource](../aulas-fiap/02.Monitoramento%20Opensource/GUIA-ESTUDO-Monitoramento-Opensource.html). Pendentes: 03 — APM; 04 — Automação de incidentes." |

### Impacto consolidado das correções

- Tabela da §5 e checklist da §9: +1 linha (REQ-OBR-42). Novos textos em REQ-OBR-05, 08, 10, 11, 17 e 30, repetidos no checklist para mantê-lo idêntico à tabela.
- TL;DR: 42 obrigatórios, 2 bônus e 4 sugestões.
- §10: novas perguntas Q-08 a Q-14.
- Coluna "Módulo(s)": preenchida nas 44 linhas (42 REQ-OBR + 2 REQ-BON).

## 4. Verificado sem problema

1. **Estrutura:**
   - as 11 seções pedidas estão presentes e na ordem;
   - o TL;DR traz data ISO (2026-09-16) e agente (Codex);
   - o link relativo `../../POSTECH%20-%20Tech%20Challenge%20-%20Fase%204.pdf` aponta para o PDF na raiz;
   - as colunas das tabelas §5, §6 e §7 seguem o formato pedido.
2. **Evidências:** as 43 aparecem literalmente na página citada, também na comparação estrita (só quebra de linha e aspas normalizadas). Nenhuma cita a página errada e nenhuma diverge em acentuação (NFC nos dois arquivos).
3. **Contagens e consistência:**
   - 41 REQ-OBR, 2 REQ-BON e 4 SUG, conforme o TL;DR;
   - 41 checkboxes, todos de REQ-OBR, com texto idêntico ao da tabela;
   - todos com status "Pendente", coerente com os checkboxes desmarcados.
4. **Classificação:**
   - os 41 REQ-OBR têm apoio em linguagem imperativa ou obrigatória, em entregável ou na REGRA DE AVALIAÇÃO;
   - REQ-BON-01 ("é opcional") e REQ-BON-02 ("preferencialmente") estão corretamente como bônus;
   - a regra de desempate (obrigatório + [INCERTO]) foi aplicada corretamente em REQ-OBR-25, 30 e 41;
   - nenhum item do PDF foi rebaixado a sugestão.
5. **Exemplos:** HTTP 5xx > 5% no auth-service, `kubectl rollout restart deployment/auth-service` e a parada do banco do flag-service ou injeção de erro aparecem como exemplos, não como prescrições, e com páginas corretas (p. 5–6).
6. **Sugestões:** SUG-01 a SUG-04 estão rotuladas como autoria Codex, "não são exigências FIAP". Nenhuma aparece em tabela de requisito ou no checklist.
7. **Nada atribuído indevidamente à FIAP:**
   - as negativas da §3 são verdadeiras: não há exigência de diagrama como arquivo separado, README na raiz, formato de nome, nem plataforma de hospedagem;
   - a §6 diz corretamente que não há pontuação extra;
   - Q-05 não transporta prazo da Fase 3.
8. **§4 (conferido com o PDF):**
   - atividade obrigatória que vale 90% da nota (p. 2);
   - ausência de data (p. 2);
   - "dedução direta de pontos" sem valor por item (p. 5);
   - ausência de plataforma de submissão.

   Ressalvas nos achados 6 e 14.
9. **Q-01 a Q-07:** todas pertinentes, com páginas corretas:
   - Q-01: p. 2 × p. 5;
   - Q-02: p. 5 × p. 6;
   - Q-03: p. 2;
   - Q-04: p. 4;
   - Q-05: p. 2;
   - Q-06: ausência nas p. 2–6;
   - Q-07: p. 2 e p. 5.
10. **§8 (linhas existentes):** estão corretas as linhas da base (p. 2), dos Helm charts (p. 3), de Prometheus/Loki/Grafana (p. 3), de "Datadog OU New Relic" (p. 4), de "PagerDuty OU OpsGenie" (p. 5), de ChatOps "Slack, Discord ou Teams" (p. 5–6) e das alternativas de automação (p. 5).
11. **Páginas 1 e 7:** a inspeção visual confirma capa preta com logotipo POS TECH (p. 1) e contracapa com logotipo POS TECH (p. 7), sem conteúdo normativo. A afirmação do TL;DR está correta.
12. **Formatação visual:** negritos ("conclusão", "é obrigatório que toda a base…", "em cima", "UMA", "1 Dashboard customizado", "sofrerá dedução direta de pontos"), itálicos, nota em caixa e cor vermelha não mudam o sentido do que foi capturado. Todos os sub-bullets "o" foram cobertos:
    - dashboard da p. 3 → REQ-OBR-10;
    - quatro passos do vídeo na p. 6 → REQ-OBR-28 a 31;
    - quatro prints na p. 6 → REQ-OBR-35 a 38.
13. **Documento complementar:** o "Capítulo de Projeto - Fase 4", em `docs/aulas-fiap/00…`, não foi importado como fonte normativa. Isso está correto: ele não traz prazo, rubrica nem regra de entrega.

## 5. Matriz de cobertura frase a frase (p. 2–6)

| Trecho do PDF | Onde está no README | Situação |
|---|---|---|
| p. 2, "Tech Challenge é o projeto…" | — (contexto institucional) | ok, sem requisito |
| p. 2, "em princípio, deve ser desenvolvida em grupo" | REQ-OBR-41, Q-03 | ok |
| p. 2, "atentar-se ao prazo… atividade obrigatória… 90%" | §4, Q-05 | sem REQ/checkbox (achado 1) |
| p. 2, "Importante: Projeto Evolutivo e Cumulativo" + base das Fases 1–3 | REQ-OBR-01 | ok |
| p. 2, quatro bullets "seu projeto deve conter" | REQ-OBR-02 a 05 | ok; redação de 05 (achado 11) |
| p. 2, "aplicado em cima dessa arquitetura" | §2 técnico | ok |
| p. 2–3, DESAFIO (DevOps Solutions Inc., HPA, falha silenciosa, 6 h + 4 h) | §2 | parcial (achado 17) |
| p. 3, "O novo objetivo é claro…" | §2 leigo | parcial (achados 10 e 17) |
| p. 3, PROPOSTA | §2 técnico, TL;DR | ok |
| p. 3–4, quatro linhas "(Disciplinas: …)" | — | ausente (achado 2) |
| p. 3, bloco 1: Helm/GitOps, Prometheus, Loki, Grafana, dashboard | REQ-OBR-06 a 10 | ok; nuances (achado 11) |
| p. 4, "O monitoramento moderno exige padronização." | §2 técnico ("padronizar") | ok |
| p. 4, OTel Collector (Obrigatório) + "Os microsserviços devem enviar…" | REQ-OBR-11 | ok; dúvida ausente (achado 3) |
| p. 4, Nota Alloy | REQ-BON-01 | ok; dúvida ausente (achado 5) |
| p. 4, Ferramenta APM "UMA… for education" | REQ-OBR-12, Q-04 | ok |
| p. 4, Instrumentação do Código (código-fonte ou Dockerfile; preferencialmente OTel) | REQ-OBR-13, REQ-BON-02 | ok; achado 3 |
| p. 4, Distributed Tracing (evaluation-service) | REQ-OBR-14 | ok |
| p. 4, Service Map (5 microsserviços) | REQ-OBR-15 | ok |
| p. 5, Criação do Alerta + exemplo | REQ-OBR-16, §8 | ok; achados 7 e 8 |
| p. 5, Gerenciamento de Incidentes | REQ-OBR-17 | ok; achados 4 e 10 |
| p. 5, Notificação (ChatOps) | REQ-OBR-18, Q-02 | ok |
| p. 5, Self-Healing (Obrigatório) + alternativas + exemplo | REQ-OBR-19, §8 | ok |
| p. 5, REGRA DE AVALIAÇÃO | REQ-OBR-23, §4 | ok; achado 6 |
| p. 5, Código Fonte no Repositório (3 bullets) | REQ-OBR-20 a 22 | ok |
| p. 5, Vídeo (até 25 min) | REQ-OBR-24 | ok |
| p. 5, Visão Geral (EKS/ArgoCD) | REQ-OBR-25, Q-01 | ok; §3 impreciso (achado 12) |
| p. 5, Métricas, Logs e OTel | REQ-OBR-26 | ok; achado 18 |
| p. 6, APM e Tracing | REQ-OBR-27 | ok; achado 18 |
| p. 6, Incidente e Self-Healing (4 sub-bullets) | REQ-OBR-28 a 31 | ok; achados 7, 16 e 18 |
| p. 6, Relatório de Entrega (.PDF) | REQ-OBR-32 | ok |
| p. 6, Nomes, RMs e usernames | REQ-OBR-33 | ok; achado 8 |
| p. 6, Links do repositório e do vídeo | REQ-OBR-34, Q-06 | ok |
| p. 6, Evidências Visuais (4 prints) | REQ-OBR-35 a 38 | ok |
| p. 6, Justificativa Técnica | REQ-OBR-39 e 40 | ok |
| p. 6, "qualquer dúvida… Discord" | §4, Q-06 | ok; achado 14 |
| p. 6, "Boa Sorte!" | — | sem requisito |

— Claude (Opus 5), 2026-09-16
