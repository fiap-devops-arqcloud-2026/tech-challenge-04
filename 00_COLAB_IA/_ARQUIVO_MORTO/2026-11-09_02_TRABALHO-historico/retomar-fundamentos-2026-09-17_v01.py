from pathlib import Path
from datetime import datetime
import json
W=Path(__file__).parent; R=W.parents[1]; A=R/'00_COLAB_IA/_ARQUIVO_MORTO/2026-09-17_revisao';A.mkdir(parents=True,exist_ok=True)
def archive(path,name):
    dest=A/name
    if not path.resolve().is_relative_to(R) or not dest.resolve().is_relative_to(R): raise ValueError('fora do projeto')
    if dest.exists(): raise ValueError(f'arquivo preservado já existe: {dest}')
    path.rename(dest)
    return dest

base=W/'guia_base.py'; txt=base.read_text(encoding='utf8')
archive(base,'guia_base-2026-09-16_v02-claude.py')
txt=txt.replace('href="../../requisitos/README.md#','href="../../requisitos/REQUISITOS.html#')
txt=txt.replace('<a href="../../requisitos/README.md">Consultar requisitos e índice dos cinco guias</a>', '<a href="../../requisitos/REQUISITOS.html">Consultar requisitos e índice dos cinco guias</a> · <a href="../../requisitos/README.md">Fonte Markdown</a>')
base.write_text(txt,encoding='utf8')

script=(W/'criar-guias-fundamentos-2026-09-16_v01.py').read_text(encoding='utf8')
script=script.replace('from guia_base import *','import guia_base\nguia_base.DATA="2026-09-17"\nguia_base.REVISAO="Revisão: Codex, com auditoria documental de Claude (2026-09-16)"\nfrom guia_base import *')
old="""snippet='''    - source_labels: [__meta_kubernetes_namespace]
      target_label: namespace
    - source_labels: [__meta_kubernetes_service_name]
      target_label: service_name'''"""
new="""snippet='''scrape_configs:
  - job_name: 'kubernetes-services'
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_service_name]
        target_label: service_name'''"""
assert old in script;script=script.replace(old,new)
script=script.replace('Transcrição do trecho final legível — Aula 4, p. 10; indentação relativa preservada','Código Fonte 1 completo — Aula 4, p. 10; quebras de diagramação normalizadas, tokens e indentação lógica preservados')
script=script.replace('Copia metadados de namespace e nome do Service para os rótulos','Descobre Services, mantém os marcados pela annotation de scrape, define o caminho de métricas e copia metadados de namespace e nome do Service para os rótulos')
script=script.replace('O guia preserva a figura, não oferece uma configuração “corrigida” atribuída à FIAP.','O guia preserva a figura e todos os tokens; a transcrição apenas reconstitui as quebras e a hierarquia visual inequívocas. Nenhum filtro ausente foi acrescentado e a configuração não foi executada.')
# Toda a ponte conceitual do Welcome fica dentro do bloco de complemento.
needle="welcome+=section('glossario','Termos para começar','<div class=\"glossary\">'"
assert needle in script;script=script.replace(needle,"welcome+=section('glossario','Termos para começar',complement('<div class=\"glossary\">'")
script=script.replace("+'</div>'+complement('<p>As definições breves", "+'</div>'+'<p>As definições breves")
script=script.replace("welcome+=section('revisao','Revisão rápida'", """welcome+=section('leitura-critica','Como interpretar a abertura',complement('<p><strong>WEL-01 · [INCERTO]</strong>: o capítulo usa “rotas de acionamento (call rotation)” (p. 2–3). No glossário, a explicação de escala de plantão é complementar; roteamento e rodízio são conceitos relacionados, mas distintos.</p><p>O capítulo chama a atividade de Projeto Integrador; o enunciado usa Tech Challenge. “Qualquer falha” (p. 3) expressa a meta da introdução; os critérios concretos de entrega são os do enunciado. O termo Functions não determina um provedor. OTel aparece associado a tracing na introdução, mas o enunciado p. 4 exige os três sinais.</p>'))
welcome+=section('revisao','Revisão rápida'""")
script=script.replace("cobertura-fundamentos-2026-09-16_v01.md", "cobertura-fundamentos-2026-09-17_v02.md")
script=script.replace('Última atualização: 2026-09-16, Codex.','Última atualização: 2026-09-17, Codex; revisão com dossiê Welcome de Claude.')
script=script.replace('com fragmento final legível transcrito e explicado','com transcrição integral dos tokens e indentação lógica, normalizando quebras da diagramação')
script=script.replace('## Incertezas distintas','## Incertezas distintas\n- WEL-01: Capítulo p. 2–3, tradução de call rotation mistura rota e escala; distinção em Complemento.')
(W/'criar-guias-fundamentos-2026-09-17_v02.py').write_text(script,encoding='utf8')
for prefix in ['00.','01.']:
    for path in (R/'docs/aulas-fiap').glob(prefix+'*/GUIA-ESTUDO-*.html'):
        archive(path,path.name.replace('.html','-2026-09-16_v01.html'))

log=R/'00_COLAB_IA/LOG_DE_TRABALHO.md';t=log.read_text(encoding='utf8');pos=t.index('## 2026-')
stamp=datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
entry=f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — Retomada após Claude

Feito: protocolo, pendências, log, decisões e dossiê lidos. Três HTMLs existem; validação estática inicial de Claude retornou zero erros. Auditoria README e dossiê Welcome aproveitados. B4/B5 retomados por subagentes com contexto preservado; B3 em auditoria independente.

Decisões/Por quê: D-006 cria espelho HTML dos requisitos para resolver navegação local (F-007). D-005 aplicado à revisão de B1/B2, mantendo scripts v01 e criando v02. Extração PDFium recuperou texto integral: a hipótese anterior de rasterização generalizada era incorreta; falhava o modo layout do pypdf.

Arquivos/de-para: guia_base.py anterior movido para _ARQUIVO_MORTO/2026-09-17_revisao/guia_base-2026-09-16_v02-claude.py; guias B1/B2 movidos para a mesma pasta com sufixo -2026-09-16_v01.html antes da nova geração. Novo gerador criar-guias-fundamentos-2026-09-17_v02.py.

Descobertas: F-008 atualizado com fonte oficial de preços da Atlassian: novos cadastros OpsGenie encerrados em 2025-06-04; encerramento do acesso em 2027-04-05. Fonte: https://www.atlassian.com/software/opsgenie/pricing, consulta 2026-09-17. Não altera a regra FIAP automaticamente.

Estado p/ o próximo agente: gerar/revisar B1/B2 v02; concluir B3–B5; revisar README com achados de Claude, espelho e links; validação estática/visual e hashes; depois marcar C. Sem commit/push.

'''
log.write_text(t[:pos]+entry+t[pos:],encoding='utf8')
print('Base preservada e revisada; gerador v02 pronto; guias anteriores arquivados; log atualizado.')
