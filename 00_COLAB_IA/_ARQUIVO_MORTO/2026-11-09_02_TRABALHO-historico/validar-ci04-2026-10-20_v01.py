"""Validacao local dos YAML e da trava AWS, sem chamada a GitHub/AWS."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent / 'validacao-ci04-2026-10-20'
sys.path.insert(0, str(WORK / 'python-packages'))
try:
    import yaml  # noqa: E402
except ImportError as exc:
    raise SystemExit(
        'Instale requirements-validacao.txt em '
        '00_COLAB_IA/02_TRABALHO/validacao-ci04-2026-10-20/python-packages '
        'usando pip --target. A dependencia local nao e versionada.'
    ) from exc


class UniqueLoader(yaml.BaseLoader):
    """Preserva `on` como texto e rejeita chaves YAML duplicadas."""


def unique_mapping(loader, node):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in mapping:
            raise ValueError(f'Chave YAML duplicada: {key}')
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)
workflows = {}
for path in sorted((ROOT / '.github/workflows').glob('*.yml')):
    data = yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)
    assert 'on' in data and 'jobs' in data, path
    workflows[path.name] = data
    print(f'{path.name}: YAML sem chaves duplicadas; {len(data["jobs"])} job(s)')

bash = Path('C:/Program Files/Git/bin/bash.exe')
for name in ('_ci-go.yml', '_ci-python.yml'):
    data = workflows[name]
    image = data['jobs']['image']
    assert image['needs'] == ['build', 'lint', 'sast', 'sca']
    assert image['if'] == "github.event_name == 'push' && github.ref == 'refs/heads/main'"
    assert data['jobs']['gitops']['if'] == image['if']
    assert data['env']['ECR_REGISTRY'] == '${{ vars.ECR_REGISTRY }}'
    assert data['env']['AWS_ROLE_ARN'] == '${{ vars.AWS_ROLE_ARN }}'
    assert image['steps'][0]['name'] == 'Validar destino AWS da Fase 4'
    gate = WORK / f'{name}.gate.sh'
    gate.write_text(image['steps'][0]['run'], encoding='utf-8', newline='\n')
    subprocess.run([str(bash), '-n', str(gate)], check=True, cwd=ROOT)
    valid = {
        'AWS_REGION': 'us-east-2',
        'ECR_REGISTRY': '123456789012.dkr.ecr.us-east-2.amazonaws.com',
        'AWS_ROLE_ARN': 'arn:aws:iam::123456789012:role/ci-fase4',
    }
    cases = [
        ('ausentes', {**valid, 'ECR_REGISTRY': '', 'AWS_ROLE_ARN': ''}, 1),
        ('registro malformado', {**valid, 'ECR_REGISTRY': 'invalido'}, 1),
        ('regiao divergente', {**valid, 'AWS_REGION': 'us-east-1'}, 1),
        ('conta divergente', {**valid, 'AWS_ROLE_ARN': 'arn:aws:iam::111111111111:role/ci'}, 1),
        ('coerente', valid, 0),
    ]
    for label, config, expected in cases:
        result = subprocess.run(
            [str(bash), str(gate)], cwd=ROOT, env={**os.environ, **config},
            text=True, capture_output=True, check=False,
        )
        assert result.returncode == expected, (name, label, result.stdout, result.stderr)
        print(f'{name}: trava AWS / {label}: OK (exit {expected})')

for name in ('compose-integration.yml', 'terraform-check.yml'):
    assert 'dev' in workflows[name]['on']['push']['branches']
print('9 YAML e 10 casos da trava AWS validados; nenhuma chamada AWS/GitHub executada.')
