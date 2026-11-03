"""GET GitHub de identificadores/configuracao, sem tokens, secrets ou mutacoes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import json
import re
import subprocess

REPO = 'fiap-devops-arqcloud-2026/tech-challenge-04'
OUT = Path(__file__).parent / 'github'
OUT.mkdir(exist_ok=True)
PATTERNS = {
    'AWS_REGION': r'[a-z]{2}(?:-[a-z]+)+-\d+',
    'ECR_REGISTRY': r'\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com',
    'AWS_ROLE_ARN': r'arn:aws:iam::\d{12}:role/[A-Za-z0-9_+=,.@/-]+'
}

def request(name, endpoint):
    p = subprocess.run(['gh', 'api', endpoint], capture_output=True, text=True, encoding='utf-8', timeout=60)
    if p.returncode:
        m = re.search(r'HTTP (\d{3})', p.stderr)
        return name, {'ok': False, 'http_status': m.group(1) if m else None, 'error': 'Consulta falhou; nenhum corpo bruto registrado.'}
    d = json.loads(p.stdout)
    if name in PATTERNS:
        v = d.get('value', '')
        valid = bool(re.fullmatch(PATTERNS[name], v))
        result = {'ok': True, 'name': name, 'format_valid': valid, 'value': v if valid else '[VALOR OMITIDO: formato inesperado]', 'updated_at': d.get('updated_at')}
    elif name == 'repository':
        result = {'ok': True, 'full_name': d.get('full_name'), 'id': d.get('id'), 'owner_id': d.get('owner', {}).get('id'), 'visibility': d.get('visibility'), 'created_at': d.get('created_at'), 'default_branch': d.get('default_branch')}
    else:
        result = {'ok': True, **{k: d.get(k) for k in ['use_default', 'use_immutable_subject', 'sub_claim_prefix', 'include_claim_keys']}}
    return name, result

requests = [('repository', f'repos/{REPO}'), ('oidc', f'repos/{REPO}/actions/oidc/customization/sub')]
requests += [(n, f'repos/{REPO}/actions/variables/{n}') for n in PATTERNS]
with ThreadPoolExecutor(max_workers=5) as pool:
    values = dict(pool.map(lambda args: request(*args), requests))
result = {'consultado_em': datetime.now().astimezone().isoformat(timespec='seconds'), 'method': 'gh api GET', 'repo': REPO, 'results': values, 'remote_mutations': False, 'workflow_run': False}
(OUT / 'configuracao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
