from pathlib import Path
from datetime import datetime, timezone, timedelta
R=Path(__file__).resolve().parents[2]; C=R/'00_COLAB_IA'
A=C/'_ARQUIVO_MORTO/2026-10-20_importacao-proposta'; A.mkdir(parents=True,exist_ok=True)
def update(name,text):
    p=C/name; old=A/name
    assert p.resolve().is_relative_to(R) and old.resolve().is_relative_to(R)
    if old.exists(): raise RuntimeError('snapshot anterior já existe')
    p.rename(old); p.write_text(text,encoding='utf8')
stamp=datetime.now(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M')

p=C/'LOG_DE_TRABALHO.md';t=p.read_text(encoding='utf8');i=t.index('## 2026-')
entry=f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — AWS mantida e recomendação de importação Git

Feito: usuário decidiu continuar AWS e disse que pretende criar outra conta. Conferência somente leitura: Fase3 main/dev=6100879, checkout limpo; Fase4 dev=9696185/main=003a707, materiais de trabalho não rastreados. Comparação independente das árvores: sem colisões de caminhos exatos. Elaborado plano de importação preservando os dois históricos.

Decisões/Por quê: D-012 registra escolha AWS, sem presumir novo crédito ou conta criada. D-013 recomenda merge dos históricos numa branch do 04, preservando o 03. O método ainda não foi aprovado/executado; pergunta atual do usuário era sobre a melhor opção. Não houve commit/push, fetch, branch nova ou mudança de remote.

Arquivos/de-para: criado 02_TRABALHO/PLANO_IMPORTACAO_FASE3_2026-10-20_v01.md. Versões anteriores de LOG, PENDENCIAS, DOSSIE e DECISOES movidas para _ARQUIVO_MORTO/2026-10-20_importacao-proposta/ antes das atualizações; entradas antigas do LOG preservadas integralmente.

Descobertas: F-016 — FAQ/termos oficiais AWS consultados em 2026-10-20 excluem cliente que já tem/teve conta do novo Free plan/crédito e benefícios adicionais por criar mais contas. Fontes: https://aws.amazon.com/free/free-tier-faqs/ e https://aws.amazon.com/free/terms/. Plano de custos não pode assumir crédito renovado. Estado e identidades da conta anterior não devem ser usados como se fossem recursos de outra conta.

Estado p/ o próximo agente: provedor AWS definido; E0 continua pendente. Antes da importação, preparar checkpoint revisável dos materiais do 04 e obter autorização para commits quando necessária. Fonte recomendada 6100879; método documentado em D-013. Configuração da conta/backend/OIDC/ECR e validação local vêm antes de publicar/deploy. Sem alterar a Fase3.

'''
t=t[:i]+entry+t[i:];lines=t.splitlines();lines[2]='TL;DR: AWS mantida por escolha do usuário em 2026-10-20. Recomendação: importar a Fase3 com histórico para branch do 04. E0 pendente; nova conta/crédito não confirmados; nenhuma importação executada.';lines[4]='Última atualização: 2026-10-20, Codex.'
update(p.name,'\n'.join(lines)+'\n')

p=C/'PENDENCIAS_E_PROXIMOS_PASSOS.md';t=p.read_text(encoding='utf8');t=t.replace('Última atualização: 2026-10-13, Codex.','Última atualização: 2026-10-20, Codex.')
lines=t.splitlines();lines[2]='TL;DR: requisitos e cinco guias concluídos; execução E0–E7 pendente. Usuário escolheu manter AWS em 2026-10-20; método de importação Git proposto. Conta/crédito ainda não confirmados. Prazo registrado: 2026-11-17.';t='\n'.join(lines)+'\n'
i=t.index('## P-003');j=t.index('## P-002')
t=t[:i]+'''## P-003 — Provedor escolhido; conta e orçamento pendentes (2026-10-20)

- [x] Provedor: manter AWS, conforme resposta direta do usuário em 2026-10-20. Avaliação Azure arquivada como referência; não executar migração Azure.
- [ ] Confirmar conta efetivamente disponível e condições de cobrança. Outra conta do mesmo cliente não renova elegibilidade Free Tier, conforme fontes oficiais de 2026-10-20.
- [ ] Atualizar orçamento e cotas antes da implantação; nenhuma conta/recurso criado nesta análise.

## P-004 — Importação da base da Fase 3

- [x] Comparar estado e árvores: main/dev da Fase3 no commit 6100879; sem colisões exatas com o 04 em 2026-10-20.
- [x] Propor método: merge dos históricos em branch própria do 04, preservando código/histórico de ambos e Fase3 intacta.
- [ ] Preparar checkpoint revisável dos arquivos atuais do 04 e confirmar autorização para commits antes de executá-los.
- [ ] Executar importação, revisar documentação/referências e configurar conta/estado/OIDC/ECR/ArgoCD do destino.
- [ ] Validar preservação, ancestralidade, Compose e infraestrutura; publicar só com autorização.

Detalhes: `02_TRABALHO/PLANO_IMPORTACAO_FASE3_2026-10-20_v01.md`. Método ainda proposto; não há branch/importação/commit/push novos.

'''+t[j:]
i=t.index('## Retomada');t=t[:i]+'''## Retomada

1. Manter AWS (D-012); verificar conta/cotas/orçamento sem presumir renovação do Free Tier.
2. Preparar o checkpoint e a importação com histórico (P-004/D-013), respeitando a exigência de autorização para commits/push. O usuário atual pediu recomendação, não executamos a migração.
3. Continuar E0/E1 local com New Relic, Slack e GitHub Actions já definidos. Não refazer os guias; V concluída.
4. Replanejar calendário até 2026-11-17, prazo informado pelo usuário.
5. Preservar a Fase3 e separar o estado da conta anterior de qualquer conta nova. Não executar operações destrutivas sem autorização.
'''
update(p.name,t)

p=C/'DECISOES.md';t=p.read_text(encoding='utf8').replace('Última atualização: 2026-10-13, Codex.','Última atualização: 2026-10-20, Codex.')
t+='''
## D-012 — Continuar na AWS (decidida pelo usuário, 2026-10-20)

Contexto: após avaliar Azure, usuário informou que pretende criar outra conta AWS para continuar no mesmo provedor.

Decisão: manter AWS; não executar migração Azure. A intenção de criar conta não comprova sua existência, crédito nem elegibilidade. A FAQ e os termos oficiais, verificados em 2026-10-20, excluem cliente que já possuiu conta do novo Free plan/crédito e benefícios adicionais por criar mais contas. Orçamento não deve pressupor esse benefício.

Alternativas: Azure foi avaliada em 2026-10-13 e não escolhida. Recomendação de desenvolver localmente antes do cluster continua útil. P-003 agora trata de conta/cotas/orçamento.

## D-013 — Importação por merge dos históricos (proposta, 2026-10-20, Codex)

Contexto: D-009 já preferiu histórico preservado; repo04 já possui materiais próprios. Em 2026-10-20 Fase3 main/dev=6100879, limpa; 04 dev=9696185/main=003a707, com novos arquivos não rastreados. Árvores sem colisões exatas.

Proposta: checkpoint revisado do 04, branch de importação e merge da base 6100879 com --allow-unrelated-histories. Preservar ambos históricos, os materiais do 04 e a Fase3. Adaptar referências de repo/conta e validar antes de publicar. Não transportar estado/segredos/caches locais.

Alternativas: cópia perde ancestralidade; fork exige reincorporar o histórico/documentos do 04; subtree em subpasta muda caminhos operacionais sem necessidade. Plano em 02_TRABALHO/PLANO_IMPORTACAO_FASE3_2026-10-20_v01.md.

Status: recomendação, não executada. Usuário perguntou a melhor opção; não houve autorização nova para commit/push.
'''
update(p.name,t)

p=C/'DOSSIE_CONTEXTO.md';t=p.read_text(encoding='utf8').replace('Última atualização: 2026-10-13, Codex.','Última atualização: 2026-10-20, Codex.')
t=t.replace('P-003: escolha de nuvem após crédito AWS esgotado declarado pelo usuário em 2026-10-13; analisar ofertas, cotas, custo e Q-01.','P-003: AWS escolhida em 2026-10-20, conta/cotas/orçamento pendentes; não presumir crédito por criar outra conta. P-004: importação Git com histórico proposta e ainda não executada.')
t+='''
## 14. Atualização de 2026-10-20

Usuário escolheu continuar AWS e informou intenção de criar outra conta. Conta não foi criada/verificada nesta sessão; a regra oficial atual exclui cliente que já teve conta dos créditos para novos clientes. Fontes e detalhes no plano de importação de 2026-10-20.

Recomendação de importação: merge dos históricos em branch do 04 a partir da base 6100879 da Fase3 (main/dev iguais e checkout limpo), preservando os materiais do 04. Cópia/fork/subtree foram comparados; método segue como proposta (D-013). Nenhum commit/push ou mudança Git foi feito. AWS é decisão confirmada (D-012); E0/P-004 continuam pendentes. Backend e identidades devem corresponder à conta efetivamente usada.
'''
update(p.name,t)
print('Handoff registrado; snapshots anteriores preservados; nenhum estado Git/nuvem alterado.')
