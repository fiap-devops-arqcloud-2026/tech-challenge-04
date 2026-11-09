from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
def run(*args):
    return subprocess.run(['git',*args],cwd=R,capture_output=True,check=True)
assert run('branch','--show-current').stdout.decode().strip()=='import-fase3'
paths=set()
for args in [('diff','--name-only','-z'),('ls-files','--others','--exclude-standard','-z')]:
    paths.update(p.decode('utf8') for p in run(*args).stdout.split(b'\0') if p)
for p in paths:
    assert not any(s in p for s in ['/.terraform/','/python-packages/','/__pycache__/','/extracoes/','/extracoes-pdfium/']),p
    assert not p.endswith(('.tfstate','.tfstate.backup','.pem','.key','.exe')),p
    assert (R/p).is_file(),p
run('add','--',*sorted(paths))
# Snapshots imutáveis conservam inclusive a formatação original; validar o código vigente.
run('diff','--cached','--check','--','.',':!00_COLAB_IA/_ARQUIVO_MORTO/**')
run('commit','-q','-m','feat: adapta base importada para o repositorio e a conta da fase 4')
adapt=run('rev-parse','HEAD').stdout.decode().strip()
assert not run('status','--porcelain').stdout.strip()
run('switch','dev')
run('merge','--no-ff','import-fase3','-m','merge: integra importacao da fase 3 na dev da fase 4')
merge=run('rev-parse','HEAD').stdout.decode().strip()
assert run('branch','--show-current').stdout.decode().strip()=='dev'
assert run('rev-parse','main').stdout.decode().strip()=='003a7075a8908011ece83d317d5c700ac2525b58'
run('merge-base','--is-ancestor','import-fase3','dev')
run('merge-base','--is-ancestor','61008794090f582c098e2edc42041339c556f14c','dev')
result={'checkpoint':'4c76a2d','import_merge':'491cd2b','adaptation':adapt,'dev_merge':merge,'branch':'dev','main_unchanged':'003a7075a8908011ece83d317d5c700ac2525b58','push':False,'pull_request':False,'new_files_and_changes_staged_explicitly':len(paths)}
(W/'integracao-dev-2026-10-20_v01.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
