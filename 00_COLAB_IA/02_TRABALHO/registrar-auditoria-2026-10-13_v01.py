from pathlib import Path
from datetime import datetime, timezone, timedelta
R=Path(__file__).resolve().parents[2]
collab=R/'00_COLAB_IA'; archive=collab/'_ARQUIVO_MORTO/2026-10-13_auditoria'; archive.mkdir(parents=True,exist_ok=True)
now=datetime.now(timezone(timedelta(hours=-3)))
stamp=now.strftime('%Y-%m-%d %H:%M')
def save_version(name, content):
    src=collab/name; dst=archive/name
    assert src.resolve().is_relative_to(R) and dst.resolve().is_relative_to(R)
    if dst.exists(): raise RuntimeError(f'já existe snapshot: {dst}')
    src.rename(dst); src.write_text(content,encoding='utf8')

p=collab/'LOG_DE_TRABALHO.md';t=p.read_text(encoding='utf8');idx=t.index('## 2026-')
entry=f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — Estado do projeto e avaliação Azure

Feito: leitura de protocolo, pendências, histórico, dossiê, decisões, requisitos, verificações e plano v02. Auditoria somente leitura do código da Fase 3. Validador dos cinco guias e README: 0 erros; hashes de 32 PDFs/689 páginas: intactos. Confirmado: repositório 04 não contém services/terraform/gitops/workflows; implementação parou antes de E0, apesar de requisitos, guias e plano prontos.

Decisões/Por quê: D-009 continua como base; Azure é hipótese, não decisão aprovada. Recomendação: E0/E1 local primeiro; comparar sessões curtas AWS com Azure elegível. Q-01 permanece relevante (PDF p.2 admite AKS; roteiro p.5 nomeia EKS). Nenhuma operação de nuvem, commit/push ou migração executada.

Arquivos/de-para: criado 02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md. LOG, PENDENCIAS, DOSSIE e DECISOES anteriores movidos integralmente para _ARQUIVO_MORTO/2026-10-13_auditoria/ antes das atualizações; LOG mantém todas as entradas antigas no arquivo atual.

Descobertas: F-013 — usuário informou em 2026-10-13 que crédito AWS acabou; Billing/tipo da conta/recursos ativos não verificados. F-014 — ofertas Azure oficiais: US$200/30 dias para novo cliente; Students US$100/12 meses sujeito à elegibilidade; AKS Free cobra recursos dos nós e há limites de cotas. Fontes e consulta 2026-10-13 no relatório. F-015 — instruções antigas de retomar V eram obsoletas; V já concluída, retomada efetiva é E0. Revisão visual final dos guias continua com limitação registrada, não confundida com o teste estrutural.

Estado p/ o próximo agente: P-003 aguarda escolha de provedor/benefício/cotas/orçamento e esclarecimento Q-01. P-002 em E0; planejamento antigo AWS precisa ser revisto após decisão. Prazo do usuário 2026-11-17 (35 dias desde 2026-10-13), não data do PDF. Começar por trabalho local reaproveitável. Sem perguntas refeitas sobre New Relic/Slack/GitHub Actions já definidos.

'''
t=t[:idx]+entry+t[idx:]
lines=t.splitlines();lines[2]='TL;DR: documentação e plano prontos; implementação parada antes de E0. Auditoria 2026-10-13 e comparação Azure registradas; crédito AWS esgotado segundo o usuário; provedor ainda não decidido.'
lines[4]='Última atualização: 2026-10-13, Codex.'
save_version(p.name,'\n'.join(lines)+'\n')

p=collab/'PENDENCIAS_E_PROXIMOS_PASSOS.md';t=p.read_text(encoding='utf8')
t=t.replace('Última atualização: 2026-09-24, Claude (Opus 5.5).','Última atualização: 2026-10-13, Codex.')
line=t.splitlines()[2];t=t.replace(line,'TL;DR: requisitos e cinco guias concluídos. Plano v02 entregue; implementação E0–E7 ainda pendente. Crédito AWS acabou segundo o usuário (2026-10-13); avaliar provedor em P-003. Prazo registrado: 2026-11-17.')
intro='''## P-003 — Escolha do provedor após fim do crédito AWS (2026-10-13)

- [x] Auditar estado local, plano e acoplamentos AWS; consultar ofertas oficiais Azure.
- [ ] Confirmar elegibilidade ao benefício Azure e cotas/VMs da assinatura [INCERTO].
- [ ] Comparar orçamento atualizado de sessões curtas AWS com implantação Azure; nenhuma estimativa nova aprovada.
- [ ] Esclarecer Q-01 com FIAP se optar por AKS (p. 2 aceita AKS; roteiro p. 5 cita EKS).
- [ ] Decidir provedor e replanejar calendário/arquitetura; escolha não foi feita nesta sessão.

Referência: `02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md`. Crédito AWS esgotado é declaração do usuário, não leitura de Billing. Permanecem desconhecidos o tipo da conta AWS e os recursos ativos. Recomendações registradas não autorizam ativação de conta, gasto ou migração.

'''
t=t.replace('## P-002 —',intro+'## P-002 —',1)
t=t.replace('crédito AWS restante; estratégia','crédito AWS esgotado declarado em 2026-10-13 (Billing não consultado); estratégia')
t=t[:t.index('## Retomada')]+'''## Retomada

1. Ler a auditoria de 2026-10-13 e P-003. A revisão V já foi concluída; não refazer guias.
2. P-002 permanece antes de E0: preparar migração do código e instrumentação local (E1), com as ferramentas já definidas.
3. Validar benefício/cotas/custo e escolha de nuvem antes de reescrever Terraform ou criar recursos. Se Azure for escolhida, incluir adaptação SQS/DynamoDB e esclarecer Q-01.
4. Replanejar as datas até 2026-11-17, prazo informado pelo usuário. Calendário iniciado em 2026-09-23 está defasado.
5. Revisão visual ampla/estreita dos guias ainda é oportunidade de QA (F-012); estrutura/links passaram na validação atual.
6. Sem commit/push nem operações destrutivas sem autorização.
'''
save_version(p.name,t)

p=collab/'DOSSIE_CONTEXTO.md';t=p.read_text(encoding='utf8')
t=t.replace('Em 2026-09-23 começou a implementação:','Em 2026-09-23 foi elaborado o plano de implementação:')
t=t.replace('Última atualização: 2026-09-24, Claude (Opus 5.5).','Última atualização: 2026-10-13, Codex.')
t=t.replace('P-001 concluída. P-002: implementação em oito etapas (E0–E7), ainda não iniciada, com sete perguntas em aberto. Detalhes em PENDENCIAS e no plano v02.','P-001 concluída. P-002: execução E0–E7 não iniciada. P-003: escolha de nuvem após crédito AWS esgotado declarado pelo usuário em 2026-10-13; analisar ofertas, cotas, custo e Q-01. Detalhes em PENDENCIAS, auditoria atual e plano v02.')
t=t.replace('Retomar pelo item V.','Retomar P-003 e a etapa E0 de P-002; V já concluída em 2026-09-21.')
t+='''
## 13. Snapshot de 2026-10-13

Guias/README novamente validados: 0 erros; 32 fontes intactas por SHA-256. O 04 ainda não contém serviços ou infraestrutura e só tem dois commits de insumos (2026-09-16); entregáveis continuam não rastreados. Código AWS da Fase 3 foi lido para estimar impacto da migração, sem alterações.

Usuário informou que o crédito AWS acabou e pediu recomendação sobre Azure. Azure tem ofertas US$200/30 dias e Students US$100/12 meses, verificadas em fontes oficiais nesta data; elegibilidade/cotas da conta [INCERTO]. AKS Free não elimina custo dos nós. Recomendação registrada: trabalhar E0/E1 local primeiro e comparar orçamento AWS curto com Azure elegível. Azure ainda não aprovada como provedor.

Prazo informado pelo usuário: 2026-11-17; 35 dias desde 2026-10-13. Q-01 segue aberta (AKS permitido p.2; vídeo nomeia EKS p.5). Fontes, impacto em SQS/DynamoDB e limites de QA em `02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md`.
'''
save_version(p.name,t)

p=collab/'DECISOES.md';t=p.read_text(encoding='utf8')
t=t.replace('Última atualização: 2026-09-24, Claude (Opus 5.5).','Última atualização: 2026-10-13, Codex.')
t+='''
## D-011 — Avaliar nuvem com trabalho local primeiro (proposta, 2026-10-13, Codex)

Contexto: usuário declarou crédito AWS esgotado e cogita Azure. Não há implementação Fase4 no 04; o código anterior usa AWS SQS/DynamoDB, Terraform, IAM e ECR. Prazo registrado 2026-11-17.

Proposta: desenvolver a instrumentação local reaproveitável antes de consumir crédito; comparar sessões curtas AWS pagas com Azure elegível. AKS Free é candidato, sujeito a cotas/orçamento e esclarecimento Q-01. Ofertas verificadas e diferenças técnicas constam da auditoria de 2026-10-13.

Alternativas: migrar integralmente de imediato (maior retrabalho em infraestrutura e dois serviços); solução híbrida (menos reescrita inicial, porém duas contas e autenticação/cobrança distribuídas). Sem escolha de provedor aprovada ou implantação executada.

Status: proposta de recomendação, aguardando decisão do usuário em P-003; não substitui D-009 automaticamente.
'''
save_version(p.name,t)

p=R/'00_COLAB_IA/02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md';t=p.read_text(encoding='utf8');t=t.replace('2026-10-13 16:30',stamp);p.write_text(t,encoding='utf8')
print('Auditoria e handoff atualizados. Snapshots anteriores preservados em '+str(archive))
