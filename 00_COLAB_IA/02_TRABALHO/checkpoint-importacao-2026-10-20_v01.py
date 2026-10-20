from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[2]
assert subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='import-fase3'
paths=[]
for p in (R/'00_COLAB_IA').rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(R)
    if any(x=='__pycache__' or x.startswith('qa-') or x.startswith('extracoes') for x in rel.parts):continue
    if p.suffix.lower() in {'.md','.html','.py','.css','.json','.js','.mjs','.ps1'}:paths.append(rel.as_posix())
paths += [p.relative_to(R).as_posix() for p in (R/'docs/aulas-fiap').glob('*/GUIA-ESTUDO-*.html')]
paths += [p.relative_to(R).as_posix() for p in (R/'docs/requisitos').rglob('*') if p.is_file()]
assert paths and all(not p.endswith(('.tfstate','.env')) for p in paths)
subprocess.run(['git','add','--',*sorted(paths)],cwd=R,check=True)
print('Checkpoint:',len(paths),'arquivos selecionados explicitamente; renderizações/extrações locais preservadas fora do índice.')
