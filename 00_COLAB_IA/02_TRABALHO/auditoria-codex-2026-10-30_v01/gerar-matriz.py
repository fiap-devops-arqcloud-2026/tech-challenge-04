from pathlib import Path
from datetime import datetime
from collections import Counter
import json,csv

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
prior=json.loads((OUT.parent/'MATRIZ_REQUISITOS_FASE4_2026-10-28_v01.json').read_text(encoding='utf-8'))
reqs=prior['requirements']
for r in reqs:
    n=int(r['id'][-2:]);r['evidence_from_prior_review']=r.pop('current_evidence')
    r['status']=('Evidência local anterior' if n in [2,13] else 'Parcial' if n==17 else r['status'])
    r['source_rechecked']='Enunciado completo, 7 páginas, texto e imagem, em 2026-10-30'
    r['current_evidence']='Nenhuma evidência final da Fase 4 localizada para este item no snapshot; não inferir atendimento a partir da Fase 3.'
    if n in [1,2,13,14,21,23]:
        r['current_evidence']='RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json e relatórios dos passos 1/2 registram aprovação funcional/tracing local em 2026-10-27. Código e imagens dos cinco serviços excluídos desta revisão; resultados não reexecutados em 30.'
    if n==3:
        r['current_evidence']='40 .tf/7 módulos/3 raízes; fmt e três validates aprovados em 2026-10-30. AWS/IAM/ECR conferidos em 28; três backend.hcl criados por Claude em 30. Sem tfvars locais encontrados e sem comprovação do provisionamento completo.'
    if n==4:
        r['current_evidence']='Nove workflows presentes; OIDC/main corrigido, 8/8 testes offline e 34/34 correspondências preservados de 28. Revisão atual encontrou F-020/F-029/F-030; nenhum CI remoto executado nesta auditoria.'
    if n==5:
        r['current_evidence']='Kustomize renderizou 23 objetos em 30; ArgoCD apontado ao repo04/main. Cinco imagens, SQS/Redis e duas roles IRSA ainda usam sentinelas. Sem evidência atual de implantação na conta nova.'
    if n in [6,7,8,9,10]:
        r['current_evidence']='Não existem charts/values/manifests de Prometheus, Loki, Grafana nem dashboard operacional nos diretórios Terraform/GitOps/observability. A descrição do README é planejamento.'
    if n==11:
        r['current_evidence']='observability/otel-collector-local.yaml tem somente pipeline traces e exportação debug/arquivo. Faltam metrics/logs, destinos Prometheus/Loki/APM e configuração do Collector no cluster.'
    if n==12:
        r['current_evidence']='New Relic escolhido (D-009). Claude registra conta criada em 2026-10-28 e região US informada em 30. Plano/benefício educacional e ingestão não foram conferidos nesta rodada.'
    if n==15:
        r['current_evidence']='Há prova histórica de trace local com cinco serviços, mas não imagem/evidência do Service Map New Relic; não é o mesmo aceite.'
    if n==16:
        r['current_evidence']='Alerta existe apenas em planejamento; nenhuma regra operacional de Grafana/APM localizada.'
    if n==17:
        r['current_evidence']='Criação de conta PagerDuty relatada em 28, trial registrado por Claude em 30. Integração do alerta, incidente e acionamento ainda sem evidência. Avanço de Pendente para Parcial por cadastro relatado.'
    if n==18:
        r['current_evidence']='Conta Slack relatada em 28; nenhuma integração/canal/notificação operacional comprovada. Cadastro sozinho não implementa notificação detalhada.'
    if n in [19,22]:
        r['current_evidence']='Nenhum workflow/script operacional de resposta automática a alerta foi localizado. selfHeal do ArgoCD reconcilia Git, não demonstra a cadeia exigida.'
    if n==20:
        r['current_evidence']='Terraform/GitOps da base e Collector local preparados; stack de cluster falta e alterações relevantes estão na árvore local, sem publicação final comprovada.'
    if n in [24,25,26,27,28,29,30,31]:
        r['current_evidence']='Não foi localizado vídeo final/link da Fase 4 com esta demonstração. Evidências de setembro identificadas como Fase 3 não encerram o item.'
    if n in [32,33,34,35,36,37,38]:
        r['current_evidence']='Não foi localizado PDF final da Fase 4 nem conjunto final de prints/links/identificação. docs/RELATORIO_DE_ENTREGA.md e apresentação existentes são Fase 3.'
    if n in [39,40]:
        r['current_evidence']='Há arquitetura/justificativas de planejamento no README e plano; falta registrar no PDF final a implementação que realmente operar.'
    if n==41:
        r['current_evidence']='[INCERTO] PDF p.2 diz em princípio em grupo; não localizada confirmação acadêmica de entrega individual/composição final. Não promover interpretação conservadora a proibição absoluta.'
    if n==42:
        r['current_evidence']='Prazo 2026-11-17 informado pelo usuário, meta interna 2026-11-12; PDF não informa data/hora/canal. Término aproximado de trial PagerDuty em 2026-11-11 precisa de confirmação.'
    # Remove ambiguity about where the old E## references can be resolved.
    if n in [2,13]:r['remaining_and_acceptance']+=' Evidência anterior preservada, sem nova certificação dos serviços nesta rodada.'

data={'updated':datetime.now().astimezone().isoformat(timespec='seconds'),'agent':'Codex','source':prior['source'],'source_pages':7,'counts':dict(Counter(r['status'] for r in reqs)), 'note':'42 IDs são decomposição do catálogo do projeto, não 42 pesos iguais. Evidência local anterior não equivale à entrega final aprovada. Contas criadas por relato não equivalem a integrações testadas.','requirements':reqs}
(OUT/'matriz-requisitos.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
cols=['id','requirement','pdf_evidence','status','current_evidence','remaining_and_acceptance']
with (OUT/'matriz-requisitos.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(reqs)
lines=['# Matriz de execução — 42 requisitos da Fase 4','',f"TL;DR: {data['counts']}. Não há cálculo de nota ou percentual acadêmico. O código dos cinco serviços não foi reavaliado.",'',f"Última atualização: {data['updated']}, Codex.",'','Fonte normativa: `POSTECH - Tech Challenge - Fase 4.pdf`, p. 2–6; todas as sete páginas relidas e vistas em 2026-10-30. Os trechos e IDs foram confrontados com o catálogo original. PDF não promete pontos extras por Alloy/SDK OTel.','', '| ID | Exigência e evidência PDF | Estado | Evidência disponível | O que falta / aceite |','|---|---|---|---|---|']
for r in reqs:
    row=[r['id'],r['requirement']+' '+r['pdf_evidence'],r['status'],r['current_evidence'],r['remaining_and_acceptance']]
    lines.append('| '+' | '.join(str(x).replace('|','/').replace('\n',' ') for x in row)+' |')
lines+=['','## Opções e recomendações','', '- REQ-BON-01 (Alloy): opcional; usar Collector padrão não é lacuna de entrega.','- REQ-BON-02 (SDKs OTel): preferência adotada segundo os relatórios locais anteriores, sem nova revisão dos serviços; não promete pontuação adicional.','- SUG-01 a SUG-04: matriz/ensaio, alerta contextualizado, correlação logs/traces e limites da automação. São autoria técnica do projeto; não novas exigências da FIAP.','', 'A mudança numérica frente à matriz de 2026-10-28 é REQ-OBR-17: Pendente → Parcial devido ao relato de conta PagerDuty criada. A expressão Comprovado localmente dos itens 02/13 passa a Evidência local anterior para explicitar o recorte desta rodada.']
(OUT/'MATRIZ_REQUISITOS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(data['counts'])
