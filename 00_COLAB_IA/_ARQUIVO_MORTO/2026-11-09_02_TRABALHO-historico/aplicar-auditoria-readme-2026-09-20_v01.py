"""Aplica ao README de requisitos os achados da auditoria adversarial
`auditorias/auditoria-readme-requisitos-2026-09-16_v01.md` (achados 1 e 3 a 18).

Cada substituição é conferida por contagem: o script falha em vez de editar o arquivo errado.
O achado 2 (coluna "Módulo(s)") e o 19 (índice dos guias) são aplicados no fechamento C,
quando a cobertura real dos cinco guias estiver disponível.
Execução única; idempotência não é garantida (rodar duas vezes falha nas asserções).
Autor: Claude (Opus 5), 2026-09-20.
"""
from pathlib import Path
import re

p = Path(__file__).resolve().parents[2] / 'docs/requisitos/README.md'
s = p.read_text(encoding='utf8')


def sub(velho, novo, n=1):
    global s
    c = s.count(velho)
    assert c == n, f'esperado {n}, achou {c}: {velho[:70]!r}'
    s = s.replace(velho, novo)


# --- Cabeçalho e TL;DR (achados 13 e 1)
sub('Última atualização: 2026-09-16, Codex. Fonte normativa:',
    'Última atualização: 2026-09-20, Codex (redação) e Claude (Opus 5) (auditoria e correções). Fonte normativa:')
sub('Escolha Datadog ou New Relic para instrumentação, tracing distribuído e mapa dos cinco serviços.',
    'Escolha Datadog ou New Relic como APM para exibir o tracing distribuído e o mapa dos cinco serviços; a instrumentação é feita no código ou no Dockerfile, preferencialmente com bibliotecas OpenTelemetry.')
sub('Este documento contém **41 obrigatórios, 2 opções/preferências do PDF e 4 sugestões autorais**.',
    'Este documento contém **42 obrigatórios, 2 bônus (opções/preferências do PDF, sem pontuação extra prometida) e 4 sugestões autorais**.')

# --- §2 contexto (achado 17)
sub('**Em linguagem simples:** o sistema entrega software rapidamente, mas a equipe descobre falhas pelos usuários e demora a localizar a causa.',
    '**Em linguagem simples:** num fim de semana, um serviço passou a falhar sem gerar aviso; a equipe só soube pelos usuários 6 horas depois e levou mais 4 horas para achar a causa nos logs espalhados pelos pods (p. 2–3).')
sub(' O caso narrado levou 6 horas para a equipe ser avisada e mais 4 para achar a causa nos logs (p. 2–3).', '')
sub('A infraestrutura automatizada anterior continua sendo o substrato do monitoramento (p. 2–4).',
    'A infraestrutura automatizada anterior continua sendo o substrato do monitoramento (p. 2–4). O evaluation-service falhou silenciosamente e o HPA escalou recursos para compensar (p. 2). O objetivo declarado é “Observabilidade Total e Resposta Ativa”: trace para lentidão, logs centralizados para erro, acionamento por PagerDuty/OpsGenie ao atingir um limite e Self-Healing (p. 3).')

# --- §3 entregáveis (achado 12)
sub('| Vídeo, até 25 min | Stack e base funcionando; Grafana/Loki/OTel; Service Map/trace; falha proposital → Firing → incidente/notificação → execução corretiva | p. 5–6 |',
    '| Vídeo, até 25 min | Cluster EKS (IaC) e ArgoCD (GitOps) rodando com a nova stack (Q-01); Grafana com dashboard, busca no Loki e explicação do roteamento OTel; Service Map, requisição de teste e trace distribuído; falha proposital → Firing → incidente/notificação → execução corretiva | p. 5–6 |')

# --- §4 (achados 14 e 6)
sub('- Não informa plataforma nem procedimento de submissão (Q-06); Discord aparece apenas como canal para dúvidas (p. 6).',
    '- Não informa plataforma nem procedimento de submissão (Q-06). Como canal de contato com a FIAP, o Discord aparece apenas para dúvidas (p. 6); nas p. 5–6 ele também é opção de ChatOps.')
sub('- Os subitens específicos do vídeo e os prints específicos do relatório continuam exigidos. O “ou” na regra geral de evidência não os torna intercambiáveis (leitura conservadora da p. 5–6).',
    '- O PDF lista itens específicos para o vídeo (p. 5–6) e para o relatório (p. 6), e a regra geral fala em demonstração “no vídeo ou” documentação “no relatório” (p. 5). [INCERTO]: por leitura conservadora, este documento trata os dois conjuntos como exigidos; Q-11.')

# --- §5 introdução (achado 9)
sub('Toda evidência abaixo se refere ao enunciado. Os trechos são curtos; os subitens completos devem ser lidos na página indicada.',
    'Toda evidência abaixo se refere ao enunciado. Os trechos são curtos; os subitens completos devem ser lidos na página indicada.\n\n'
    'O PDF rotula como “(Obrigatório)” apenas o OTel Collector (p. 4), o Self-Healing (p. 5) e as Evidências Visuais (p. 6). Os demais itens também são obrigatórios: usam linguagem imperativa (“deve”, “crie”, “configure”, “escolha”) e a REGRA DE AVALIAÇÃO (p. 5) exige evidenciar todos os requisitos, com dedução direta de pontos.')

# --- Textos de requisitos, repetidos na tabela e no checklist (achados 10, 11, 18, 3)
sub('Implantar em Kubernetes gerenciado via GitOps; alternativas citadas: EKS/GKE/AKS e ArgoCD/Flux. Ver Q-01.',
    'Implantar no Kubernetes (EKS, GKE ou AKS), com a implantação gerenciada via GitOps (ArgoCD/Flux). Ver Q-01.', 2)
sub('Usar Loki para centralizar os logs de todos os contêineres do cluster.',
    'Usar Loki para centralizar e indexar todos os logs dos contêineres do cluster.', 2)
sub('Criar ao menos um dashboard customizado com recursos do cluster, taxa de requisições dos microsserviços e painel de logs em tempo real.',
    'Criar no Grafana ao menos um dashboard customizado que centralize a saúde do ecossistema: (a) uso de recursos do cluster; (b) taxa de requisições dos microsserviços; (c) painel de logs em tempo real.', 2)
sub('Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM).',
    'Centralizar métricas, logs e traces dos microsserviços no OTel Collector, recebendo, processando e exportando para os backends corretos (Prometheus, Loki e APM). Ver Q-08.', 2)
sub('Criar conta no PagerDuty OU OpsGenie e integrar abertura automática de incidente ao alerta.',
    'Criar conta no PagerDuty OU OpsGenie e integrar o alerta para abrir incidente automaticamente, com a ferramenta acionando o time (objetivo da p. 3). Ver Q-09.', 2)
sub('No vídeo: abrir Grafana, exibir dashboard/métricas, buscar logs no Loki e explicar o roteamento do Collector.',
    'No vídeo: (a) abrir o Grafana; (b) exibir o dashboard customizado com as métricas; (c) buscar logs no Loki; (d) explicar como o Collector roteia esses dados.', 2)
sub('No vídeo: abrir Datadog/New Relic, mostrar Service Map, fazer requisição de teste e exibir trace distribuído detalhado.',
    'No vídeo: (a) abrir o painel do Datadog/New Relic e mostrar o Service Map; (b) fazer uma requisição de teste; (c) exibir o trace distribuído detalhado.', 2)
sub('No vídeo: mostrar incidente aberto no PagerDuty/OpsGenie e notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02.',
    'No vídeo: (a) mostrar o incidente sendo aberto no PagerDuty/OpsGenie; (b) mostrar a notificação chegando ao Slack/Discord. [INCERTO] para Teams; Q-02.', 2)
sub('Adotar Grafana Alloy como alternativa ao OTel Collector padrão, mantendo as funções centrais de OTel.',
    'Adotar Grafana Alloy como alternativa ao OTel Collector padrão, mantendo as funções centrais de OTel. Ver Q-10.')
sub('Preferir bibliotecas OpenTelemetry da linguagem na instrumentação; a instrumentação em si continua obrigatória.',
    'Preferir bibliotecas OpenTelemetry da linguagem na instrumentação; a instrumentação em si continua obrigatória. Ver Q-08.')

# --- REQ-OBR-42: submissão no prazo (achado 1)
sub('| <a id="req-obr-41"></a>REQ-OBR-41 | Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03. | p. 2: “em princípio, deve ser desenvolvida em grupo” | a mapear | Pendente |',
    '| <a id="req-obr-41"></a>REQ-OBR-41 | Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03. | p. 2: “em princípio, deve ser desenvolvida em grupo” | a mapear | Pendente |\n'
    '| <a id="req-obr-42"></a>REQ-OBR-42 | Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06. | p. 2: “Importante atentar-se ao prazo de entrega” | a mapear | Pendente |')
sub('- [ ] **REQ-OBR-41** — Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03.',
    '- [ ] **REQ-OBR-41** — Desenvolver em grupo, por interpretação conservadora. [INCERTO]: o PDF diz "em princípio"; Q-03.\n'
    '- [ ] **REQ-OBR-42** — Submeter a entrega da fase (código, vídeo e relatório) dentro do prazo oficial. [INCERTO]: data, horário e canal não constam no PDF; Q-05 e Q-06.')

# --- §8 arquitetura (achados 15, 16, 7, 2-parcial)
sub('| Transporte/roteamento | OTel Collector; Grafana Alloy como alternativa | Collector central obrigatório; distribuição Alloy opcional (p. 4) |',
    '| Transporte/roteamento | OTel Collector; Grafana Alloy como alternativa | Collector como peça central é obrigatório; Alloy no lugar do Collector padrão é opcional (p. 4) |')
sub('| Automação | Runbook Automation, AWS Lambda ou GitHub Action via webhook | Alternativas citadas para cumprir resposta automática (p. 5) |',
    '| Automação | Runbook Automation, AWS Lambda ou GitHub Action via webhook | Alternativas citadas para cumprir resposta automática (p. 5) |\n'
    '| Instrumentação | Código-fonte ou Dockerfile; bibliotecas OpenTelemetry da linguagem | Instrumentação obrigatória; bibliotecas OTel preferenciais (p. 4) |\n'
    '| Visibilidade no APM | Distributed Tracing (requisição no evaluation-service); Service Map dos 5 microsserviços | Obrigatórios (p. 4) |\n'
    '| Contexto do incidente narrado | evaluation-service; HPA | Contexto, não requisito (p. 2) |')
sub('O requisito exige respeitar cada sinal e demonstrar seu trajeto; não implica que todo backend aceite indistintamente qualquer sinal.',
    'O PDF exige que o Collector roteie os sinais aos backends corretos (p. 4), que o roteamento seja explicado no vídeo (p. 5) e que a arquitetura OTel seja explicada no relatório (p. 6); isso não implica que todo backend aceite indistintamente qualquer sinal.')
sub('O PDF os rotula como exemplos (p. 5–6). Reiniciar não garante resolver qualquer causa; a tarefa exige mostrar a tentativa corretiva automática.',
    'O PDF os rotula como exemplos (p. 5–6), assim como “mostrando o pod reiniciando automaticamente via terminal” (p. 6). Reiniciar não garante resolver qualquer causa; a tarefa exige mostrar a tentativa corretiva automática.\n\n'
    'Os exemplos não formam, sozinhos, um cenário único: o alerta e a reinicialização citam o `auth-service` (p. 5), e a falha proposital cita o `flag-service` (p. 6). Pela sequência da p. 6 e pelo vínculo da automação “ao alerta criado” (p. 5), a falha escolhida para o vídeo deve acionar o alerta configurado. [INCERTO]; Q-12.\n\n'
    '**Disciplinas indicadas pelo PDF:** bloco 1 (p. 3) Prometheus, Grafana, Loki, Observabilidade no Kubernetes; bloco 2 (p. 4) OpenTelemetry (OTel) e Alloy; bloco 3 (p. 4) APM, Instrumentação, Datadog ou New Relic; bloco 4 (p. 4) Alert Fatigue, PagerDuty/OpsGenie, ChatOps, Runbook Automation, Self-Healing.')

# --- §10 dúvidas novas (achados 3, 4, 5, 6, 7, 8)
sub('| Q-07 | Qual a rubrica detalhada e o valor de cada desconto? | p. 2 informa 90%; p. 5 informa dedução sem valores por item. |',
    '| Q-07 | Qual a rubrica detalhada e o valor de cada desconto? | p. 2 informa 90%; p. 5 informa dedução sem valores por item. |\n'
    '| Q-08 | O agente ou a biblioteca do fornecedor (Datadog/New Relic), ou a instrumentação feita apenas no Dockerfile, é aceita se a telemetria passar pelo OTel Collector? O envio direto do agente ao APM, sem o Collector, é aceito? | p. 4 torna as bibliotecas OTel preferenciais, mas exige o envio da telemetria ao OTel e o roteamento pelo Collector; p. 5 pede código-fonte atualizado. REQ-OBR-11, 13 e 21 mantidos conservadoramente. |\n'
    '| Q-09 | Se não for possível criar conta nova em uma das ferramentas de incidentes, a outra passa a ser a única opção aceita, ou existe alternativa? | p. 5 exige conta no PagerDuty OU OpsGenie; a disponibilidade dos planos não é tratada no enunciado. Verificação externa (F-008, 2026-09-20): a Atlassian encerrou a venda do OpsGenie em 2025-06-04 e desliga o produto em 2027-04-05 — fato de mercado, não regra da FIAP. |\n'
    '| Q-10 | Com o Grafana Alloy no lugar do OTel Collector, os entregáveis que citam o Collector (REQ-OBR-20 e REQ-OBR-26) ficam atendidos mostrando o Alloy? | p. 4 torna o Alloy opcional; p. 5 nomeia o OTel Collector no código e no vídeo. |\n'
    '| Q-11 | Um requisito demonstrado só no relatório (ou só no vídeo) evita a dedução, ou os subitens específicos de cada entregável são exigidos separadamente? | p. 5: regra geral com “ou”; p. 5–6: listas específicas de vídeo e de relatório. |\n'
    '| Q-12 | A falha proposital do vídeo precisa acionar o mesmo alerta e a mesma automação configurados, ou podem ser cenários distintos? | p. 5 vincula a automação “ao alerta criado”; p. 6 usa exemplo de falha em outro serviço. |\n'
    '| Q-13 | Os usernames do relatório são de qual plataforma (portal FIAP, GitHub, Discord)? | p. 6 não especifica. |\n'
    '| Q-14 | Que característica torna o alerta “inteligente” para a avaliação? | p. 5 dá apenas um exemplo (taxa de 5xx maior que 5% no auth-service); a disciplina Alert Fatigue consta na p. 4. |')

p.write_text(s, encoding='utf8')
print('REQ-OBR:', len(set(re.findall(r'REQ-OBR-\d{2}', s))),
      '| checkboxes:', s.count('- [ ] **REQ-OBR'),
      '| dúvidas Q:', len(set(re.findall(r'\bQ-\d{2}\b', s))),
      '| bytes:', len(s))
