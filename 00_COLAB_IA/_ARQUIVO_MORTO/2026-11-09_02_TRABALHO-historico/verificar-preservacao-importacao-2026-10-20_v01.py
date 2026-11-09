from pathlib import Path
import hashlib,json,subprocess,re
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
def git(*args,cwd=R):return subprocess.check_output(['git',*args],cwd=cwd,text=True,encoding='utf8').strip()
baseline=json.loads((W/'preservacao-importacao-2026-10-20_v01.json').read_text(encoding='utf8'))
missing=[];changed=[];same=[]
for x in baseline['files']:
    p=R/x['path']
    if not p.is_file():missing.append(x['path'])
    elif hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:changed.append(x['path'])
    else:same.append(x['path'])
assert not missing,missing
protected=[x for x in baseline['files'] if x['path'].startswith('docs/') or x['path']=='POSTECH - Tech Challenge - Fase 4.pdf']
assert all(x['path'] not in changed for x in protected)
for p in (R/'services').rglob('*'):
    if not p.is_file() or p.suffix in {'.exe','.pyc'}:continue
    rel=p.relative_to(R).as_posix()
    try:original=subprocess.check_output(['git','show',f"{baseline['source_commit']}:{rel}"],cwd=R)
    except subprocess.CalledProcessError:continue
    # CRLF do checkout Windows e LF do objeto Git são representações equivalentes.
    assert p.read_bytes().replace(b'\r\n',b'\n')==original.replace(b'\r\n',b'\n'),rel
assert git('rev-parse','main')==baseline['phase4_main']
assert git('rev-parse','main',cwd=R.parent/'tech-challenge-03')==baseline['source_commit']
assert not git('status','--porcelain',cwd=R.parent/'tech-challenge-03')
subprocess.run(['git','merge-base','--is-ancestor',baseline['source_commit'],'HEAD'],cwd=R,check=True)
subprocess.run(['git','merge-base','--is-ancestor',baseline['phase4_dev'],'HEAD'],cwd=R,check=True)

badlinks=[]
for name in ['README.md','terraform/README.md','gitops/README.md']:
    p=R/name
    for href in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
        if href.startswith(('http:','https:','#','mailto:')):continue
        target=(p.parent/unquote(urlsplit(href).path)).resolve()
        if not target.exists():badlinks.append((name,href))
assert not badlinks,badlinks

# Guarda a versão exata da Fase 3 de todos os arquivos importados que foram adaptados.
archive=R/'00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879'
for rel in git('diff','--name-only','491cd2b').splitlines():
    p=archive/rel
    if p.exists():continue
    try:original=subprocess.check_output(['git','show',f'491cd2b:{rel}'],cwd=R,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:continue
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(original)

result={'files_before':len(baseline['files']),'unchanged':len(same),'modified_expected':changed,'missing':missing,'protected_phase4_files':len(protected),'phase3_source':baseline['source_commit'],'phase4_main_unchanged':baseline['phase4_main'],'source_checkout_clean':True,'readme_local_links':'OK','source_services':'identical','ancestry':'both histories reachable'}
(W/'verificacao-preservacao-importacao-2026-10-20_v01.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
