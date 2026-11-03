"""Confere cobertura, fontes, links, hashes e Git; não altera fontes operacionais."""
from pathlib import Path
import hashlib, json, re, subprocess, unicodedata
from collections import Counter
from datetime import datetime
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '00_COLAB_IA/02_TRABALHO'
OUT = WORK / 'VERIFICACAO_REVISAO_GERAL_2026-10-28_v01.json'
issues=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args,cwd=ROOT): return subprocess.check_output(['git',*args],cwd=cwd).decode('utf-8')
def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if c.isalnum())

source = (ROOT/'docs/requisitos/README.md').read_text(encoding='utf-8')
norm={}
for line in source.splitlines():
    if line.startswith('| <a id="req-obr-'):
        cells=[c.strip() for c in line.strip('|').split('|')]
        key=re.search(r'REQ-OBR-\d+',cells[0]).group()
        norm[key]={'requirement':cells[1],'pdf_evidence':cells[2]}
data=json.loads((WORK/'MATRIZ_REQUISITOS_FASE4_2026-10-28_v01.json').read_text(encoding='utf-8'))
rows=data['requirements']
ids=[r['id'] for r in rows]
if len(ids)!=42 or set(ids)!=set(norm) or len(set(ids))!=42: issues.append('Cobertura42 incorreta')
counts=dict(Counter(r['status'] for r in rows))
if counts!=data['counts']: issues.append('Contagens divergem')
pdf=json.loads((WORK/'qa-revisao-geral-2026-10-27/enunciado.json').read_text(encoding='utf-8'))
quotes=0
for row in rows:
    if any(row[k]!=norm[row['id']][k] for k in ['requirement','pdf_evidence']): issues.append(row['id']+' diverge do catálogo')
    page=int(re.search(r'p\. (\d+)',row['pdf_evidence']).group(1))
    quote=re.search('“(.+?)”',row['pdf_evidence']).group(1)
    if normalize(quote) not in normalize(pdf['pages'][page-1]['text']): issues.append(row['id']+' trecho não encontrado na página')
    else: quotes+=1
if sha(ROOT/data['source'])!=pdf['sha256']: issues.append('PDF alterado após extração')
report=WORK/'REVISAO_GERAL_FASE4_2026-10-28_v01.md'
table_ids=re.findall(r'^\| (REQ-OBR-\d+) \|',report.read_text(encoding='utf-8'),flags=re.M)
if table_ids!=ids: issues.append('TabelaMarkdown diverge da matrizJSON')
files=[report,WORK/'REVISAO_GERAL_APLICACOES_2026-10-28_v01.md',WORK/'REVISAO_GERAL_INFRA_2026-10-28_v01.md',WORK/'REVISAO_GERAL_DOCUMENTACAO_2026-10-27_v01.md']
links=0
for file in files:
    text=file.read_text(encoding='utf-8')
    if '\ufffd' in text: issues.append('Caractere inválido:'+file.name)
    if text.count('```')%2: issues.append('CercasMarkdown:'+file.name)
    for raw in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        target=unquote(raw.split('#')[0].strip('<>'))
        if not target or re.match(r'[a-zA-Z][\w+.-]*:',target): continue
        p=(file.parent/target).resolve()
        links+=1
        if not p.exists() and p!=OUT: issues.append('Link ausente:'+str(p))
initial=json.loads((WORK/'qa-revisao-geral-2026-10-27/estado-inicial.json').read_text(encoding='utf-8'))
changed=[p for p,h in initial['manifest'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
if changed: issues.append('Fontes205 alteradas:'+str(changed))
production=json.loads((WORK/'qa-passos-locais-2026-10-27/production-sha256-sql-final.json').read_text(encoding='utf-8'))
prod_changed=[p for p,h in production.items() if sha(ROOT/p)!=h]
if prod_changed: issues.append('Fontesdoensaio alteradas:'+str(prod_changed))
preservation=json.loads((WORK/'preservacao-importacao-2026-10-20_v01.json').read_text(encoding='utf-8'))
protected=[i for i in preservation['files'] if i['path'].startswith('docs/') or i['path']==data['source']]
if any(not (ROOT/i['path']).exists() or sha(ROOT/i['path'])!=i['sha256'] for i in protected): issues.append('Material protegido alterado')
before=json.loads((WORK/'preservacao-passos-locais-2026-10-22_v01.json').read_text(encoding='utf-8'))
def deleted(s): return {e[3:] for e in s.split('\0') if e.startswith(' D ')}
status=git('status','--porcelain=v1','-z')
deletions=deleted(status)
if deletions!=deleted(before['git_status_before']): issues.append('Exclusões preexistentes mudaram')
branch=git('branch','--show-current').strip()
head=git('rev-parse','HEAD').strip()
main=git('rev-parse','main').strip()
if branch!='dev' or head!=initial['head'] or main!=initial['main']: issues.append('ReferênciasGit mudaram')
source03_clean=not git('status','--porcelain',cwd=ROOT.parent/'tech-challenge-03').strip()
if not source03_clean: issues.append('Fonte03 não está limpa')
tf=[]
for name in ['terraform-validate.json','terraform-cluster-validate.json','terraform-k8s-validate.json']:
    result=json.loads((WORK/'qa-revisao-infra-2026-10-27'/name).read_text(encoding='utf-8-sig'))
    tf.append(result['valid'] and result['error_count']==0 and result['warning_count']==0)
if not all(tf): issues.append('EvidênciaTerraform inválida')
render=(WORK/'qa-revisao-infra-2026-10-27/gitops-renderizado.yaml').read_text(encoding='utf-8-sig')
kinds=Counter(re.findall(r'^kind: (.+)$',render,flags=re.M))
if sum(kinds.values())!=23: issues.append('Render não contém23objetos')
for rel in ['00_COLAB_IA/LOG_DE_TRABALHO.md','00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md','00_COLAB_IA/DOSSIE_CONTEXTO.md']:
    # Diff-check avalia whitespace no conteúdo rastreado; não é teste de runtime.
    proc=subprocess.run(['git','diff','--check','--',rel],cwd=ROOT,capture_output=True,text=True)
    if proc.returncode: issues.append('diff-check:'+rel)
result={'updated':datetime.now().astimezone().isoformat(),'requirements':len(rows),'counts':counts,'pdf_quotes_verified':quotes,'local_report_links_checked':links,'operational_and_document_sources_preserved':len(initial['manifest']),'production_hashes_matching':len(production)-len(prod_changed),'protected_files_preserved':len(protected),'preexisting_deletions_preserved':len(deletions),'branch':branch,'head':head,'main':main,'source03_clean':source03_clean,'terraform_validations_from_2026_10_27':tf,'gitops_objects_from_2026_10_27':dict(kinds),'new_runtime_test':'sonda observacional targeting em cópia isolada,2026-10-27','full_integration_rerun':False,'cloud_or_remote_queries':False,'issues':issues}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(bool(issues))
