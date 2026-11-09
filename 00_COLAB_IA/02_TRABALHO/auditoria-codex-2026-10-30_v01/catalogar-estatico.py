"""Cobertura verificável do snapshot; não executa fontes do projeto."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import ast, collections, hashlib, json, os, re, subprocess
from urllib.parse import unquote, urlsplit
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT/'00_COLAB_IA/02_TRABALHO/validacao-ci04-2026-10-20/python-packages'))
import yaml
snapshot = json.loads((OUT/'inventario-inicial.json').read_text(encoding='utf-8-sig'))
validation = {'yaml': [], 'python': [], 'json': [], 'pdf': [], 'large_files': [], 'helper_code_operations': []}
seen = {}
for x in snapshot['files']:
    p = ROOT/x['path']
    if not x['exists']:
        x['coverage'] = 'ausente antes da auditoria'; continue
    if 'services' in p.relative_to(ROOT).parts:
        x['coverage'] = 'codigo dos servicos excluido por solicitacao, incluindo copias'; continue
    x['identical_to'] = seen.get(x['sha256'])
    seen.setdefault(x['sha256'], x['path'])
    if x['bytes'] > 100*1024*1024:
        validation['large_files'].append({'path':x['path'], 'bytes':x['bytes']})
    x['coverage'] = 'inventario, hash e classificacao'
    if p.suffix.lower() in {'.py','.json','.tf','.hcl','.sh','.md','.html','.yaml','.yml','.toml','.mjs','.css','.txt','.log','.example'} or not p.suffix:
        txt=p.read_text(encoding='utf-8-sig',errors='replace')
        x['lines']=len(txt.splitlines())
        if p.suffix=='.py':
            try:
                tree=ast.parse(txt,filename=x['path']); status='ok'
                calls=[]
                for n in ast.walk(tree):
                    if isinstance(n,ast.Call):
                        fn=ast.unparse(n.func)
                        if any(s in fn for s in ['subprocess','system','unlink','remove','rmtree','rename','replace','write_text','write_bytes','requests','urlopen']):
                            calls.append({'line':n.lineno,'call':ast.unparse(n)[:250]})
                if x['category']=='trabalho_e_evidencias':validation['helper_code_operations'].append({'path':x['path'],'operations':calls})
            except SyntaxError as e:status=f'{e.lineno}: {e.msg}'
            validation['python'].append({'path':x['path'],'status':status})
        if p.suffix=='.json':
            try:json.loads(txt);status='ok'
            except ValueError as e:status=str(e)
            validation['json'].append({'path':x['path'],'status':status})
        if p.suffix in {'.yaml','.yml'}:
            try:list(yaml.safe_load_all(txt));status='ok'
            except yaml.YAMLError as e:status=str(e)
            validation['yaml'].append({'path':x['path'],'status':status})
    if p.suffix=='.pdf':
        reader=PdfReader(p)
        texts=[page.extract_text() or '' for page in reader.pages]
        validation['pdf'].append({'path':x['path'],'pages':len(texts),'empty_pages':[i+1 for i,t in enumerate(texts) if len(t.strip())<50]})
        x['coverage']='integridade e extracao de todas as paginas; releitura normativa integral apenas do enunciado Fase4'

# Fluxos Kubernetes renderizados: só leitura do arquivo produzido por kustomize.
render=(OUT/'validacoes/gitops-renderizado.txt').read_text(encoding='utf-8').split('\nSTDERR:')[0]
objects=list(yaml.safe_load_all(render))
validation['kubernetes']={'objects':len(objects),'kinds':dict(collections.Counter(x['kind'] for x in objects)), 'hpa_conflicts':[]}
for hpa in [o for o in objects if o['kind']=='HorizontalPodAutoscaler']:
    dep=next(o for o in objects if o['kind']=='Deployment' and o['metadata']['name']==hpa['spec']['scaleTargetRef']['name'])
    validation['kubernetes']['hpa_conflicts'].append({'name':dep['metadata']['name'],'git_replicas':dep['spec'].get('replicas'),'hpa_max':hpa['spec']['maxReplicas']})

# Composição normalizada usando apenas os valores públicos de exemplo.
env=os.environ.copy()
for line in (ROOT/'.env.example').read_text().splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1);env[k]=v
for k in ['COMPOSE_FILE','COMPOSE_PROJECT_NAME','OTEL_TRACE_DIR','OTEL_UID','OTEL_GID']:
    env.pop(k,None)
docker=r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
cmd=[docker,'compose','--env-file','.env.example','-f','docker-compose.yaml','-f','docker-compose.integration.yaml','-f','docker-compose.otel.yaml','config','--format','json']
result=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
validation['compose']={'exit_code':result.returncode,'stderr':result.stderr}
if result.returncode==0:
    config=json.loads(result.stdout)
    validation['compose']['ports']={n:s.get('ports',[]) for n,s in config['services'].items() if s.get('ports')}
    validation['compose']['services']=list(config['services'])
    (OUT/'validacoes/compose-config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')

# Bash syntax only; never execute these scripts.
validation['bash']=[]
for p in [*(ROOT/'scripts').glob('*.sh'),ROOT/'infra/postgres-app/01-init-multi-db.sh']:
    r=subprocess.run([r'C:\Program Files\Git\bin\bash.exe','-n',str(p)],capture_output=True,text=True)
    validation['bash'].append({'path':p.relative_to(ROOT).as_posix(),'exit_code':r.returncode,'stderr':r.stderr})

(OUT/'cobertura-arquivos.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'validacoes/analise-estatica.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
for group in ['yaml','python','json','pdf','bash']:
    entries=validation[group]
    print(group,len(entries),'issues',[r for r in entries if r.get('status','ok')!='ok' or r.get('exit_code',0)!=0])
print('compose',validation['compose']['exit_code'],'kubernetes',validation['kubernetes'])
print('large_files',validation['large_files'])
