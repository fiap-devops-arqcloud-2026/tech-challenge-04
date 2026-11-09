from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,subprocess
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent;C=R/'00_COLAB_IA'
A=C/'_ARQUIVO_MORTO/2026-10-20_fechamento-importacao';A.mkdir(parents=True,exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf8').strip()
assert git('branch','--show-current')=='dev'
assert git('rev-parse','main')=='003a7075a8908011ece83d317d5c700ac2525b58'
assert git('rev-parse','import-fase3')=='31f92e4e29b6c5bc00fd07f7e317f8cd98014d53'
stamp=datetime.now(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M')
def save(name,t):
    p=C/name;old=A/name
    assert not old.exists();p.rename(old);p.write_text(t,encoding='utf8')

p=C/'LEIA-PRIMEIRO.md';t=p.read_text(encoding='utf8')
t=t.replace('A tarefa atual produz requisitos documentais e cinco guias; não implementa infraestrutura.','Código/histórico da Fase 3 importados; contexto e materiais do 04 preservados. Retomar na dev; conta AWS e instrumentação continuam pendentes.')
t=t.replace('Última atualização: 2026-09-16, Codex.','Última atualização: 2026-10-20, Codex.')
old='Fontes originais e todo `tech-challenge-03` são somente leitura. Escrita autorizada: `docs/requisitos`, `00_COLAB_IA` e novos `GUIA-ESTUDO-*.html` dentro das cinco pastas de aulas. Trabalho auxiliar em `00_COLAB_IA/02_TRABALHO`. Não criar arquivos na raiz, não commitar nem publicar. As permissões específicas prevalecem sobre a estrutura global genérica.'
new='Fontes originais de aula/enunciado e todo `tech-challenge-03` são somente leitura. O usuário autorizou em 2026-10-20 a importação do código/histórico e os ajustes nos caminhos de código do 04, com commits locais em `import-fase3` e merge na `dev`. Importação concluída; continuar na `dev`. Sem push, PR, merge na `main` ou operação AWS nesta etapa. Trabalho auxiliar em `00_COLAB_IA/02_TRABALHO`; caches/renderizações permanecem locais e ignorados. A colaboração vigente é esta pasta na raiz; `docs/00_COLAB_IA` é acervo histórico importado e não altera o estado/instruções atuais.'
assert old in t;t=t.replace(old,new);save(p.name,t)

p=C/'PENDENCIAS_E_PROXIMOS_PASSOS.md';t=p.read_text(encoding='utf8');lines=t.splitlines();lines[2]='TL;DR: importação com histórico concluída e mesclada na dev em 2026-10-20; Fase3 e materiais04 preservados. README/CI/ArgoCD adaptados. Main/PR/push intactos. ContaAWS e integração Docker pendentes; E1 de observabilidade ainda não iniciada.';t='\n'.join(lines)+'\n'
i=t.index('## P-004');j=t.index('## P-002')
t=t[:i]+'''## P-004 — Importação da base da Fase 3 (concluída, 2026-10-20)

- [x] Base fixada em 61008794090f582c098e2edc42041339c556f14c, Fase3 limpa e somente leitura.
- [x] Checkpoint curado do 04 (`4c76a2d`) e merge dos históricos (`491cd2b`) na branch exata `import-fase3`.
- [x] README/CI/CD/ArgoCD/Terraform ajustados para o repo04; conta anterior removida das configurações operacionais. Adaptação: `31f92e4`.
- [x] Merge local para dev (`cb81b00`); branch import-fase3 preservada. Main04 segue003a707; nenhum push/PR/deploy.
- [x] Preservação SHA-256 dos39arquivos preexistentes de docs/enunciado04 e ausência de perdas no manifesto de933arquivos; serviços idênticos à fonte.
- [x] Validações locais de Terraform, GitOps, YAML/gates, buildsGo, sintaxePython, Composeconfig, guias e links; revisão independente sem achados pendentes.

Resultado detalhado: `02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md`. Scripts, contexto e entregáveis versionados; renderizações/extrações/caches mantidos localmente e ignorados.

## P-005 — Ensaio integrado local (pendente de Docker)

- [ ] Iniciar Docker Desktop com engine Linux funcional. O start tentado nesta sessão terminou após50s sem engine; serviço consultado parado.
- [ ] Executar `bash scripts/test-compose.sh` em projeto isolado `tc04-integration`; conferir os cinco serviços, autenticação, flags/regras, cache e fluxo SQS/DynamoDB viaMoto.
- [ ] Registrar resultado e encerrar somente os contêineres/volumes descartáveis desse teste.

Não confundir `docker compose config` aprovado ou buildsGo aprovados com integração funcional. Go informou ausência de testes unitários; CI remoto também não foi executado porque não houve push/PR.

'''+t[j:]
t=t.replace('- [ ] E0 — Fundação: inventário AWS somente leitura, migração do código para o 04, contas New Relic/PagerDuty/Slack, token do GitHub','- [ ] E0 — Fundação (parcial): importação concluída; faltam conta/backend/cotas/identidades e contas de observabilidade/incidentes confirmadas')
t=t.replace('estratégia de estado do Terraform após a migração;','estados próprios da Fase4 definidos (bucket/região reais pendentes);')
i=t.index('## Retomada');t=t[:i]+'''## Retomada

1. Trabalhar na `dev` do repo04. Importação já concluída; não repetir, não alterar a Fase3. PR/main e push aguardam pedido do usuário.
2. Aguardar dados da nova conta; preencher repositoryvars e configurações locais de backend/tfvars, conferir conta/cotas/orçamento e substituir todos os marcadoresGitOps pelos outputs reais. Não transportar estado/segredos antigos.
3. Resolver P-005 e iniciar E1 (instrumentação/Collector local/NewRelic). Ainda não foi implementada observabilidade nem Self-Healing nesta importação.
4. Fontes/guia: preservados; validadores agora selecionam só os cinco módulos04 pelo inventário original. Docs/00_COLAB_IA é histórico03; contexto vigente está na raiz00_COLAB_IA.
5. Prazo informado pelo usuário2026-11-17; o calendário antigo deve ser replanejado. Destruições exigem autorização específica.
'''
save(p.name,t)

p=C/'DECISOES.md';t=p.read_text(encoding='utf8')
t+='''
## D-014 — Importação autorizada e integrada na dev (concluída, 2026-10-20)

Contexto: usuário autorizou explicitamente importar o código, manter os materiais04, criar a branch exata import-fase3 e fazer merge local para dev, ajustar README/CI/ArgoCD e atualizar memória/contexto. PR/main foram expressamente adiados; a contaAWS nova ainda será informada.

Decisão executada: checkpoint4c76a2d; merge491cd2b com segundo pai6100879 (histórico03); adaptação31f92e4; mergecb81b00 emdev. Branchimport preservada; main04=003a707 e Fase3=6100879 intactas. Sem push/PR/deploy. As permissões anteriores limitadas aos estudos foram ampliadas somente para a execução autorizada; não pedir novamente a autorização já dada.

Por quê: preserva o histórico de ambos repositórios e os caminhos operacionais. Documentos e fontes04 intactos; documentos operacionais antigos mantidos como históricos com aviso. Estado/backend da conta antiga não foi transferido.

Configuração: AWS por repositoryvars; expected_aws_account_id obrigatório; chaves S3 phase4/prod; Argo/OIDC repo04, main como destino futuro. Sentinelas tornam explícito o runtime pendente. Não implementar observabilidade durante a importação.

Alternativas: cópia simples e fork/subtree descartados pela D-013. D-013 deixou de ser mera proposta com a autorização desta sessão; esta ADR registra o resultado.

Validação: verificações locais e revisão independente aprovadas; único P2 (validador incluindo guias03) corrigido por seleção baseada no inventário04. Teste integrado Docker não executado por indisponibilidade da engine; P-005. Nenhuma execução do CIremoto foi alegada.
'''
save(p.name,t)

p=C/'DOSSIE_CONTEXTO.md';t=p.read_text(encoding='utf8');lines=t.splitlines();lines[2]='TL;DR: código e histórico da Fase3 importados na branch import-fase3 e integrados à dev em2026-10-20; main intacta. Requisitos/cinco guias e materiais04 preservados. README/CI/ArgoCD adaptados; contaAWS e integraçãoDocker pendentes.';t='\n'.join(lines)+'\n'
t=t.replace('Nada foi implantado: os guias são material de estudo, não prova de infraestrutura.','Código-base importado e validado localmente; nada foi implantado na nova conta. Guias são material de estudo, não prova de infraestrutura.')
t=t.replace('preservação dos originais, sem commit/push.','preservação dos originais; commits e merge locais autorizados para esta importação, sem push/PR/main.')
t=t.replace('P-001 concluída. P-002: execução E0–E7 não iniciada.','P-001 e P-004 concluídas. P-002: E0 parcialmente concluída com a importação; E1–E7 pendentes.')
t=t.replace('P-004: importação Git com histórico proposta e ainda não executada.','P-005: teste integrado aguarda Docker Linux engine funcional.')
t=t.replace('Retomar P-003 e a etapa E0 de P-002; V já concluída em 2026-09-21.','Retomar na dev: P-003 para conta/backend e P-005 para Docker; depois E1. V e importaçãoP-004 já concluídas.')
t=t.replace('Não comitar nem publicar sem autorização.','A importação recebeu autorização de commits/merge locais; publicação/push/PR/main continuam aguardando pedido.')
t=t.replace('Memória global não foi alterada.','Memória global receberá nota durável na pasta extensions/ad_hoc/notes por pedido explícito do usuário em2026-10-20, com escopo e validações da importação; sem dados sensíveis.')
t+='''
## 15. Fechamento da importação — 2026-10-20

Branch atualdev. Import-fase3 aponta31f92e4, já ancestral de dev pelo mergecb81b00. Histórico03 mantém commit6100879; checkpoint04 é4c76a2d. Main04 continua003a707. Não houve push/PR/nuvem e o 03 segue limpo/somenteleitura.

39arquivos atuais de docs/enunciado04 intactos por SHA-256; todos933arquivos preexistentes preservados, com alterações esperadas de ferramentas/contexto arquivadas. Serviços correspondem à base03. Caches/renderizações/extrações locais não foram excluídos nem versionados; fontes dos guias/contexto/entregáveis foram versionadas.

README e CLAUDE apontam o estado04; CIvalida dev semAWS e exige repositoryvars antes da publicação futura; Argo/OIDC repo04 e main futura; backendparcial/statephase4 e expected_aws_account_id impedem presumir a conta antiga. Conta, bucket, região e outputs reais ainda pendentes. Nenhum dado novo inventado.

Validado: Terraform3raízes sembackend; 23objetosKustomize; YAML/gates de9workflows e10casosAWS; buildsGo (sem testesunitários); ASTPython6arquivos; Composeconfig; guias/requisitos/links. DockerDesktop não iniciou, então integração emcontêineres ficou emP-005. RuntimeAWS/CIremoto não comprovados. Resultado completo em02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md.
'''
save(p.name,t)

p=C/'LOG_DE_TRABALHO.md';t=p.read_text(encoding='utf8');i=t.index('## 2026-')
entry=f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — Importação concluída e merge na dev

Feito: importação com histórico da base6100879 viaimport-fase3, preservando materiais04. Checkpoint4c76a2d, mergehistórico491cd2b, adaptação31f92e4 e merge localcb81b00 na dev. Main04 segue003a707; branchimport preservada; source03 limpo. README/CI/CD/Argo/OIDC repo04, estados próprios, guards da conta e sentinelas pendingAWS preparados.

Decisões/Por quê: D-014 executa autorização desta sessão. DadosAWS ainda pendentes; nenhum recurso, CIremoto, push ou PR. Prodsegue main como destino futuro; trabalho atualna dev. Guias/insumos preservados; acervo03 separado pelo inventário.

Verificação: todos933arquivos preexistentes mantidos;39docs/enunciado04 intactos porhash. BuildsGo e ASTPython aprovados; Go não tem testesunitários. Terraform3initsembackend/3validate/fmt, 23objetosGitOps,9YAML e10casosguardAWS, Bash, Composeconfig e5guias/README/links aprovados. Revisão independente achou P2 no globdosguias, corrigido e revalidado. Composeintegrado NÃO executado: DockerLinuxengine indisponível, start50stimeout; P-005. actionlint ausente, usado parserYAML/regraslocais. Arquivosarquivados preservam aformatação original; diff--check do código vigente aprovado (snapshot.gitignore herdado temblanklineEOF).

Arquivos/de-para: relatórioRESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md, manifesto/verificação/integracaoJSON, README,CLAUDE,.github,Terraform,GitOps e3ferramentasdeguias. Originais substituídos em_ARQUIVO_MORTO/FASE3_BASE_6100879 e2026-10-20_ferramentas-guias. Contexto/LOG/PENDENCIAS/DECISOES antes deste fechamento movidos para2026-10-20_fechamento-importacao; histórico do LOG atual mantido. Renderizações/extrações~230MB preservadas localmenteignoradas.

Memória: usuário pediu atualização explícita; nota durável será gravada em C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes com branch/escopo/pendências, sem credenciais ou dados da conta.

Estado p/ o próximo agente: trabalhar somente na dev; importaçãoP-004 concluída. Aguardar conta paraP-003/E0restante; iniciarDocker/repetirensaioP-005 e partirE1. Não repetirimportação, não alterar03/main, não publicarsem pedido. Contexto vigente00_COLAB_IA na raiz; docs/00_COLAB_IA é histórico03.

'''
t=t[:i]+entry+t[i:];lines=t.splitlines();lines[2]='TL;DR: importação com histórico concluída na dev (mergecb81b00), README/CI/ArgoCD adaptados e materiais04 preservados. Main/push/PR/nuvem intactos. ContaAWS e integraçãoDocker permanecem pendentes.';save(p.name,'\n'.join(lines)+'\n')

p=W/'RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md';t=p.read_text(encoding='utf8')
t=t.replace('Integração local à dev será registrada no fechamento; sem push, PR, main ou implantação.','Integração local à dev concluída (merge cb81b00); main intacta. Sem push, PR ou implantação.')
t+='''
## Integração concluída

Em 2026-10-20, adaptação31f92e4 integrada pelo mergecb81b00 à dev. Import-fase3 preservada. Main04 permanece003a7075a8908011ece83d317d5c700ac2525b58; source03 permanece6100879 limpo. O histórico de ambos projetos é alcançável a partir da dev. Contexto e memória atualizados no fechamento; nenhum PR/push/nuvem.
''';p.write_text(t,encoding='utf8')

p=W/'integracao-dev-2026-10-20_v01.json';j=json.loads(p.read_text(encoding='utf8'));j['new_files_and_changes_staged_explicitly']=len(git('show','--format=','--name-only','31f92e4').splitlines());p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
print('Contexto e relatório finalizados na dev; snapshots anteriores preservados.')
