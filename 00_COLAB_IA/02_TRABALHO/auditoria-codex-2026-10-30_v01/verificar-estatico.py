"""Auditoria local: sem rede, init real, apply ou leitura de services/**."""
from pathlib import Path
import json, subprocess, datetime, importlib.util

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'validacoes'
OUT.mkdir(exist_ok=True)
TF = r'C:\Users\Gabriel\AppData\Local\bin\terraform.exe'
KUBE = r'C:\Program Files\Docker\Docker\resources\bin\kubectl.exe'
results = []

def run(name, args, cwd=ROOT, timeout=90):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    (OUT / (name + '.txt')).write_text(p.stdout + '\nSTDERR:\n' + p.stderr, encoding='utf-8')
    results.append({'name': name, 'command': args, 'exit_code': p.returncode, 'evidence': (OUT / (name + '.txt')).relative_to(ROOT).as_posix()})
    print(name, p.returncode, flush=True)
    return p

run('terraform-version', [TF, 'version', '-json'])
run('terraform-fmt', [TF, 'fmt', '-check', '-recursive', 'terraform'])
for layer in ['terraform', 'terraform/cluster', 'terraform/k8s']:
    run(layer.replace('/', '-') + '-validate', [TF, '-chdir=' + layer, 'validate', '-json'])
run('gitops-renderizado', [KUBE, 'kustomize', 'gitops/overlays/prod'])
for f in Path(ROOT / 'scripts').rglob('*.py'):
    compile(f.read_text(encoding='utf-8-sig'), str(f), 'exec')
results.append({'name': 'python-scripts-compile-memory', 'exit_code': 0, 'files': [p.relative_to(ROOT).as_posix() for p in (ROOT/'scripts').rglob('*.py')]})
# Reprodução isolada da expressão do argocd.tf, usando provider built-in.
repro = OUT / 'repro-count-sensitive'
repro.mkdir(exist_ok=True)
(repro/'main.tf').write_text('variable "github_token" {\n type = string\n sensitive = true\n default = ""\n}\nresource "terraform_data" "repo" {\n count = var.github_token != "" ? 1 : 0\n input = "dummy-public-value"\n}\n', encoding='utf-8')
run('repro-count-init', [TF, 'init', '-backend=false', '-input=false', '-no-color'], cwd=repro)
run('repro-count-plan', [TF, 'plan', '-refresh=false', '-input=false', '-no-color', '-var=github_token=dummy-public-value'], cwd=repro)
(OUT/'resultados.json').write_text(json.dumps({'at': datetime.datetime.now().astimezone().isoformat(), 'checks': results}, ensure_ascii=False, indent=2), encoding='utf-8')
print('modules:', {m: bool(importlib.util.find_spec(m)) for m in ['yaml','hcl2','lxml','pypdf','pptx']})
