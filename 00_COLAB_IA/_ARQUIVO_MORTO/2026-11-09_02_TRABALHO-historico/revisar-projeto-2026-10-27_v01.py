"""Inventário/preservação e leitura do enunciado, sem operações de nuvem."""
from pathlib import Path
import hashlib, json, subprocess
from datetime import datetime
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '00_COLAB_IA/02_TRABALHO/qa-revisao-geral-2026-10-27'
QA.mkdir(exist_ok=True)
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8', errors='replace').strip()
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
paths = subprocess.check_output(['rg', '--files', '--hidden', '-g', '!.git/**', '-g', '!00_COLAB_IA/**', '-g', '!docs/00_COLAB_IA/**'], cwd=ROOT).decode('utf-8').splitlines()
manifest = {Path(p).as_posix(): sha(ROOT/p) for p in paths if (ROOT/p).is_file()}
out = {'updated': datetime.now().astimezone().isoformat(), 'branch': git('branch','--show-current'), 'head': git('rev-parse','HEAD'), 'main': git('rev-parse','main'), 'status': git('status','--porcelain'), 'manifest': manifest}
target = QA/'estado-inicial.json'
if target.exists():
    old = json.loads(target.read_text(encoding='utf-8'))
    changed = [p for p,h in old['manifest'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    result = {'updated': out['updated'], 'source_files': len(old['manifest']), 'changed': changed, 'head_unchanged': old['head']==out['head'], 'main_unchanged': old['main']==out['main']}
    (QA/'preservacao-final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    assert not changed and result['head_unchanged'] and result['main_unchanged']
else:
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
pdf = ROOT/'POSTECH - Tech Challenge - Fase 4.pdf'
reader = PdfReader(pdf)
pages = [{'page':i+1, 'text':p.extract_text() or ''} for i,p in enumerate(reader.pages)]
(QA/'enunciado.json').write_text(json.dumps({'sha256':sha(pdf),'pages':pages}, ensure_ascii=False, indent=2),encoding='utf-8')
(QA/'enunciado.txt').write_text('\n\n'.join(f"--- PÁGINA {p['page']} ---\n{p['text']}" for p in pages), encoding='utf-8')
print(json.dumps({'pages':len(pages),'source_files':len(manifest),'chars':[len(p['text']) for p in pages]},ensure_ascii=False))
