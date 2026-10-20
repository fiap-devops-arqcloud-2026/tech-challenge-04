# Estado do projeto e opções de nuvem

TL;DR: requisitos, cinco guias e plano de implementação estão prontos. A execução parou antes de E0. Azure oferece crédito inicial, mas migrar exige adaptar a base AWS e dois serviços. Recomenda-se desenvolver localmente primeiro e comparar sessões curtas AWS com Azure elegível antes de escolher.

Última atualização: 2026-10-13 16:27 (America/Sao_Paulo, UTC-03:00), Codex. Fontes oficiais consultadas em 2026-10-13; inspeção do repositório e validações executadas nesta data.

## 1. O que está concluído

- README de requisitos: 42 REQ-OBR, 2 REQ-BON (opções/preferências, sem pontos extras prometidos), 4 SUG e 14 dúvidas, com evidências por página, checklist e módulos mapeados.
- Espelho HTML dos requisitos e cinco guias: Welcome; Observabilidade e Monitoramento; Monitoramento Opensource; APM; Automação de incidentes.
- Base reprodutível: extrações PDFium, renderizações, dossiês, fragmentos, scripts geradores, auditorias e verificação de código/referências.
- Plano v02 de implementação, registrado em 2026-09-24: seis diagramas, mudanças previstas no código e infraestrutura, etapas E0–E7, riscos e estimativa histórica AWS.

Fontes: [pendências](../PENDENCIAS_E_PROXIMOS_PASSOS.md), [log](../LOG_DE_TRABALHO.md), [requisitos](../../docs/requisitos/README.md), [plano](PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html), [verificação anterior](verificacoes/verificacao-final-2026-09-21_v01.md).

## 2. Verificação atual e onde paramos

Em 2026-10-13 o validador existente foi executado novamente: **0 erros** nos cinco guias e README. Os SHA-256 dos **32 PDFs, 689 páginas** coincidem com o inventário: nenhum original alterado. Há 31 PDFs de aulas (682 páginas) e um enunciado de 7 páginas.

O repositório 04 ainda não contém `services/`, `terraform/`, `gitops/` ou `.github/workflows/`. Os únicos commits locais são `003a707` e `9696185`, de 2026-09-16. Guias, requisitos e colaboração continuam não rastreados pelo Git. Não foi feito commit/push nesta análise.

**Retomada efetiva: E0 — Fundação.** E0–E7 estão pendentes. As frases antigas mandando retomar a revisão V estão superadas pelo registro de conclusão de 2026-09-21; não refazer guias já entregues.

| Etapa | Trabalho pendente |
|---|---|
| E0 | Inventário da nuvem, trazer código/histórico do 03 ao 04 e preparar contas/identidades |
| E1 | Instrumentar os cinco serviços localmente e visualizar tracing no New Relic |
| E2 | Provisionar a plataforma Kubernetes |
| E3 | Implantar Collector, Prometheus, Loki e Grafana por GitOps |
| E4 | Dashboard, alerta e integrações de incidente/ChatOps |
| E5 | Automação de Self-Healing |
| E6 | Ensaiar a cadeia e reunir evidências |
| E7 | Vídeo até 25 minutos, relatório PDF e submissão |

Limite de QA: a validação estática atual não equivale à revisão visual de todos os guias em telas ampla/estreita. Essa revisão ficou incompleta nas sessões anteriores, conforme F-012; o plano v02 teve revisão Chrome headless registrada. A fidelidade dos guias recebeu verificações de código e amostragem dirigida, não nova auditoria humana integral nesta sessão.

## 3. Decisões e fatos que continuam válidos

D-009 registra respostas do usuário em 2026-09-23: código/histórico do 03 migra ao 04, Fase 3 fica preservada, APM New Relic, ChatOps Slack, Self-Healing por GitHub Actions e implementação solo. PagerDuty integra o desenho de incidentes.

Prazo registrado: **2026-11-17**, informado pelo usuário, não presente no PDF. Entre 2026-10-13 e essa data há **35 dias**. O calendário original começava em 2026-09-23 e precisa ser replanejado.

O usuário informou em 2026-10-13 que os créditos AWS acabaram. Isso resolve a pergunta sobre haver saldo para o plano antigo; **Billing, tipo da conta e recursos ativos não foram consultados ao vivo**. Não inferir que recursos estão desligados ou que haverá cobrança apenas pelo fim do crédito.

## 4. Azure tem equivalente ao Free Tier?

Sim, em duas ofertas principais para este caso:

| Oferta | Benefício anunciado | Condições relevantes |
|---|---|---|
| Azure Free Account | US$ 200 por até 30 dias; franquias mensais gratuitas de serviços específicos, algumas por 12 meses | Para clientes novos; continuidade após crédito/prazo requer mudança para pagamento por uso. Elegibilidade desta conta [INCERTO]. |
| Azure for Students | US$ 100 para usar em 12 meses; dispensa cartão no cadastro | Exige elegibilidade e verificação acadêmica. Ser aluno de pós-graduação não comprova automaticamente elegibilidade. Situação do usuário [INCERTO]. |

Fontes oficiais, consulta 2026-10-13: [Azure Free Account](https://azure.microsoft.com/en-us/free/), [Azure for Students](https://azure.microsoft.com/en-us/free/students/), [termos acadêmicos](https://azure.microsoft.com/en-us/pricing/offers/ms-azr-0170p).

O crédito é saldo finito e não significa que toda a arquitetura seja gratuita. No **AKS Free**, a gestão do cluster/plano de controle é gratuita, mas os recursos dos nós são cobrados. Discos, rede e serviços adicionais precisam entrar no orçamento conforme o desenho escolhido. Fonte: [preços AKS](https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/), consulta 2026-10-13.

As VMs gratuitas da série B anunciadas na oferta não garantem um AKS gratuito: o AKS não suporta série B no pool de sistema. Free Trial/Students também têm restrições de cotas, e aumentos exigem migração para pagamento por uso. Fonte: [cotas e tamanhos AKS](https://learn.microsoft.com/en-us/azure/aks/quotas-skus-regions), consulta 2026-10-13. Capacidade e cotas reais da assinatura [INCERTO].

Se o crédito de 30 dias começar em **2026-10-13**, seu horizonte fica aproximadamente em **2026-11-12**, antes da entrega registrada para 2026-11-17. Cálculo de calendário; não há horário de ativação conhecido. Ativar quando a base local estiver pronta aproveita melhor o benefício, mas não garante duração até a entrega: o saldo também pode se esgotar antes.

Em contas com créditos, o limite de gastos normalmente acompanha o saldo; em pagamento por uso, esse limite não está disponível. Fonte: [limite de gastos Azure](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit), consulta 2026-10-13. Nenhuma assinatura foi criada/alterada.

## 5. O que precisaria mudar para Azure

Conferência somente leitura do código real de `tech-challenge-03` em 2026-10-13:

| Parte | Impacto |
|---|---|
| Serviços/Dockerfiles, PostgreSQL e Redis | Amplo reaproveitamento; revisar endpoints, autenticação, TLS, persistência e redes |
| EKS/ECR/Terraform AWS | Provisionamento AKS, registry, rede e identidades Azure novos; reaproveitar organização e padrões, não os recursos AWS |
| CI/CD | Preservar build/testes/scans; trocar login AWS/ECR e publicação de imagens |
| IAM/IRSA e StorageClass gp3 | Adaptar identidade dos pods/RBAC e persistência para Azure |
| SQS em evaluation e analytics | Azure Service Bus é candidato funcional; exige SDK, envio/recebimento, confirmação/redelivery e contexto de trace adaptados |
| DynamoDB em analytics | Cosmos DB é candidato funcional; exige SDK e modelo de dados/partição/gravação adaptados |
| OTel, Prometheus, Loki, Grafana, New Relic, PagerDuty, Slack, ArgoCD | Desenho em grande parte portátil; implementação da Fase 4 ainda está pendente |
| GitHub Actions Self-Healing | Mecanismo pode permanecer, com autenticação/autorização AKS no lugar de EKS |

SQS→Service Bus e DynamoDB→Cosmos DB **não são trocas automáticas de endpoint**. Evidências: `evaluation-service/main.go:77`, `sqs.go:42`, `analytics-service/app.py:43/82/86/106`, workflows `_ci-go.yml:426`, `_ci-python.yml:453`, patch IRSA e StatefulSet do PostgreSQL targeting. Mapeamentos são propostas técnicas, não decisões aprovadas.

## 6. Aceitação pela FIAP

O enunciado **p. 2 permite EKS, GKE e AKS**, mas **p. 5 nomeia EKS/ArgoCD no roteiro do vídeo**. A dúvida já está em Q-01/REQ-OBR-25 do README. AKS é um candidato explicitamente citado; confirmar com professor/tutor o roteiro em AKS antes de assumir que a troca não exige esclarecimento. Não foi enviada mensagem ao tutor.

## 7. Recomendação

Recomendação técnica do Codex, não decisão do usuário:

1. Priorizar E0/E1 local e instrumentação com Compose/Collector/New Relic; o Compose de integração já permite emular SQS/DynamoDB com Moto. Essa parte é útil em qualquer nuvem.
2. Para concluir com menor retrabalho, comparar primeiro um orçamento AWS de sessões curtas de ensaio/gravação. A estimativa ≈US$ 0,47/h do plano é histórica e incompleta, não um preço atual; precisa de orçamento novo antes de autorizar gastos.
3. Se o objetivo exigir evitar gasto direto e houver benefício Azure elegível, capacidade suficiente e esclarecimento FIAP, AKS Free é uma alternativa viável para laboratório. Replanejar incluindo migração de infraestrutura, fila e analytics, sem prometer que US$ 100/200 bastem.
4. Evitar manter a stack inteira ligada durante todas as semanas de desenvolvimento. Não trocar o APM exigido por Azure Monitor/Application Insights como se fosse uma alternativa aceita pelo PDF.

Não recomendo automaticamente uma implantação híbrida AKS+SQS/DynamoDB AWS: poupa reescrita inicial, mas acrescenta duas contas, autenticação entre nuvens, rede e cobrança distribuída à entrega solo.

## 8. Próxima decisão e handoff

Antes da escolha definitiva faltam: elegibilidade Azure/new customer ou Students, cotas/VMs disponíveis, orçamento tolerado e esclarecimento Q-01. P-003 registra a avaliação do provedor; P-002 continua em E0. Nenhuma migração, conta, implantação, alteração de código ou operação destrutiva foi executada.
