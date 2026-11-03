"""Cruza evidencias sanitizadas AWS/GitHub da etapa 8; nao faz chamadas remotas."""
from datetime import datetime
from pathlib import Path
import json

BASE = Path(__file__).parent
a = json.loads((BASE / 'aws/inventario-aws-sanitizado.json').read_text(encoding='utf-8'))
g = json.loads((BASE / 'github/configuracao.json').read_text(encoding='utf-8'))['results']
account = a['identity']['data']['Account']
region = a['effective_region']
r = a['responses']
role = r['role']['data']
trust = role['AssumeRolePolicyDocument']['Statement']
checks = {}

def check(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)

check('github_consultas_ok', all(x.get('ok') for x in g.values()))
check('variables_formato_valido', all(g[n]['format_valid'] for n in ['AWS_REGION', 'ECR_REGISTRY', 'AWS_ROLE_ARN']))
check('regiao_aws_github', g['AWS_REGION']['value'] == region)
check('registry_conta_regiao', g['ECR_REGISTRY']['value'] == f'{account}.dkr.ecr.{region}.amazonaws.com')
check('role_arn_aws_github', g['AWS_ROLE_ARN']['value'] == role['Arn'])
repo = g['repository']
owner, name = repo['full_name'].split('/')
prefix = f"repo:{owner}@{repo['owner_id']}/{name}@{repo['id']}"
check('github_subject_imutavel', g['oidc']['use_immutable_subject'] is True and g['oidc']['sub_claim_prefix'] == prefix)
check('trust_unico_allow_federado', len(trust) == 1 and trust[0]['Effect'] == 'Allow' and trust[0]['Action'] == 'sts:AssumeRoleWithWebIdentity')
check('trust_principal_provider_mesma_conta', trust[0]['Principal'] == {'Federated': f'arn:aws:iam::{account}:oidc-provider/token.actions.githubusercontent.com'})
check('trust_subject_main_e_audience', trust[0]['Condition'] == {'StringEquals': {'token.actions.githubusercontent.com:sub': prefix + ':ref:refs/heads/main', 'token.actions.githubusercontent.com:aud': 'sts.amazonaws.com'}})
check('provider_url_audience', r['oidc_provider']['data']['Url'] == 'token.actions.githubusercontent.com' and r['oidc_provider']['data']['ClientIDList'] == ['sts.amazonaws.com'])
for key, value in a['checks'].items():
    if isinstance(value, bool):
        check('aws_' + key, value)
repos = []
lifecycle_missing = []
for service in ['auth', 'flag', 'targeting', 'evaluation', 'analytics']:
    d = r['ecr_' + service]['data']
    check(service + '_ecr_unico', len(d) == 1)
    d = d[0]
    check(service + '_uri_conta_regiao', d['registryId'] == account and d['repositoryUri'] == g['ECR_REGISTRY']['value'] + '/' + service + '-service')
    check(service + '_config', d['imageTagMutability'] == 'MUTABLE' and d['imageScanningConfiguration']['scanOnPush'] is True and d['encryptionConfiguration']['encryptionType'] == 'AES256')
    repos.append(d['repositoryName'])
    life = r['lifecycle_' + service]
    if 'LifecyclePolicyNotFoundException' in life.get('error', ''):
        lifecycle_missing.append(d['repositoryName'])
result = {'verificado_em': datetime.now().astimezone().isoformat(timespec='seconds'), 'checks': checks, 'total_checks': len(checks), 'passou': all(checks.values()), 'account_id': account, 'region': region, 'repositorios': repos, 'lifecycle_ausente': lifecycle_missing, 'limites': ['Sem teste de federacao em workflow, push de imagem ou alteracoes remotas.', 'Sem auditoria de Billing, cotas, tags ou infraestrutura fora dos campos consultados.', 'Diferenca de thumbprints documentada separadamente para reconciliacao do provedor.']}
(BASE / 'correspondencia-aws-github.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'passou': result['passou'], 'checks': len(checks), 'ecr': len(repos), 'lifecycle_ausente': len(lifecycle_missing)}, ensure_ascii=False))
