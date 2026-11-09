"""Recolhe do journal do workflow wf_ede16310-9b4 os resultados prontos e prepara as entradas da rodada 2."""
import json, pathlib, re, collections

J = pathlib.Path(r'C:/Users/Gabriel/.claude/projects/C--Users-Gabriel-Documents-GitHub-tech-challenge-04/0c6ae1db-1d45-4b74-9ec0-857241e35810/subagents/workflows/wf_ede16310-9b4/journal.jsonl')
OUT = pathlib.Path(__file__).parent
# So o ID da conta da Fase 3 e mascarado (lido do nome do bucket antigo, sem fixar o numero aqui).
# Outros numeros de 12 digitos, como IDs de artigos da ajuda do Slack, sao legitimos.
_P3 = pathlib.Path(r'C:/Users/Gabriel/Documents/GitHub/tech-challenge-04/docs/00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md')
CONTA = re.compile(re.escape(re.search(r'togglemaster-tfstate-(\d{12})-', _P3.read_text(encoding='utf-8')).group(1)))

rotulo, res = {}, {}
for linha in J.read_text(encoding='utf-8').splitlines():
    o = json.loads(linha)
    if o['type'] == 'started':
        rotulo[o['agentId']] = o['label']
    elif o['type'] == 'result':
        res[o['agentId']] = o['result']
prontos = {rotulo[a]: r for a, r in res.items()}
print('prontos:', sorted(prontos))

def grava(nome, dado):
    texto = json.dumps(dado, ensure_ascii=False, indent=1)
    achados = set(CONTA.findall(texto))
    if achados:  # nenhum ID de 12 digitos deve sair daqui
        texto = CONTA.sub('<CONTA_FASE3>', texto)
        print(f'  {nome}: {len(achados)} numero(s) de 12 digitos mascarado(s)')
    (OUT / nome).write_text(texto, encoding='utf-8')
    print(f'{nome}: {len(texto):,} caracteres, {texto.count(chr(10)):,} linhas')

ext = {k.split(':', 1)[1]: v for k, v in prontos.items() if k.startswith('extrair:')}
assert len(ext) == 11, sorted(ext)
grava('extracao_todas.json', ext)

def junta(campo):
    return [{**i, 'lote': lote} for lote, r in sorted(ext.items()) for i in r[campo]]

dec, conh, pend, confl = junta('decisoes'), junta('conhecimentos'), junta('pendencias'), junta('conflitos_fase4')

# Decisoes agrupadas pelo ID original (D-0xx); sem ID ficam juntas.
grupos = collections.defaultdict(list)
for d in dec:
    m = re.search(r'D-(\d{3})', d['id_original'])
    grupos[f'D-{m.group(1)}' if m else 'SEM_ID'].append(d)
grava('entrada_DEC.json', {'decisoes_por_id': dict(sorted(grupos.items())), 'conflitos_extracao': confl})

SETS = {
    'TEC-A': ['arquitetura', 'terraform', 'gitops_kubernetes', 'seguranca'],
    'TEC-B': ['ci_cd', 'custo', 'tempo_medido', 'operacao_aws', 'armadilha'],
    'PROC-A': ['gravacao_video', 'avaliacao_fiap', 'relatorio_entrega'],
    'PROC-B': ['licao_aprendida', 'boa_pratica', 'regra_permanente', 'processo_colaboracao', 'risco', 'referencia'],
}
for k, tipos in SETS.items():
    itens = sorted((c for c in conh if c['tipo'] in tipos), key=lambda c: (c['tipo'], c['titulo']))
    dado = {'itens': itens}
    if k == 'PROC-B':
        dado |= {'pendencias': pend, 'conflitos_extracao': confl}
    grava(f'entrada_{k}.json', dado)
print('itens por conjunto:', {k: sum(c['tipo'] in t for c in conh) for k, t in SETS.items()}, 'fora:', sum(not any(c['tipo'] in t for t in SETS.values()) for c in conh))

grava('entrada_relatorio.json', {
    'arquivos': junta('arquivos'), 'descartavel': junta('descartavel'), 'sensiveis': junta('sensiveis'),
    'limitacoes': {lote: r['limitacoes'] for lote, r in sorted(ext.items())}})

for f in ['newrelic', 'pagerduty', 'slack-grafana']:
    grava(f'pesquisa_{f}.json', prontos.get('pesquisa:' + f))
    if 'verifica:' + f in prontos:
        grava(f'verificacao_{f}.json', prontos['verifica:' + f])
print('decisoes:', len(dec), 'grupos:', len(grupos), '| conhecimentos:', len(conh), '| pendencias:', len(pend), '| conflitos:', len(confl))
