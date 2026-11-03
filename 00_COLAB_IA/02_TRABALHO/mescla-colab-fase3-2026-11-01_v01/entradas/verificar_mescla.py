"""Confere a mescla das pastas 00_COLAB_IA sem imprimir dados sensiveis (so contagens e posicoes)."""
import pathlib, re, subprocess, sys, urllib.parse

RAIZ = pathlib.Path(r'C:/Users/Gabriel/Documents/GitHub/tech-challenge-04')
NOVOS = ['00_COLAB_IA/DECISOES.md', '00_COLAB_IA/DOSSIE_CONTEXTO.md', '00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md',
         '00_COLAB_IA/LEIA-PRIMEIRO.md', '00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md', '00_COLAB_IA/LOG_DE_TRABALHO.md', 'CLAUDE.md',
         '00_COLAB_IA/02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md', '00_COLAB_IA/02_TRABALHO/PASSO2_CONTAS_SAAS_2026-11-01_v01.md']
COMMIT = '3b21e65'
falhas = []

def git(*a):
    return subprocess.run(['git', *a], cwd=RAIZ, capture_output=True, text=True, encoding='utf-8').stdout

# 1. Originais recuperaveis e pasta removida da arvore
arquivos_f3 = [l for l in git('ls-tree', '-r', '--name-only', COMMIT, '--', 'docs/00_COLAB_IA').splitlines() if l]
ok = sum(subprocess.run(['git', 'cat-file', '-e', f'{COMMIT}:{p}'], cwd=RAIZ).returncode == 0 for p in arquivos_f3)
print(f'[1] originais no commit {COMMIT}: {ok}/{len(arquivos_f3)} recuperaveis')
if ok != 39: falhas.append('originais')
existe = (RAIZ / 'docs/00_COLAB_IA').exists()
print(f'    docs/00_COLAB_IA na arvore: {"AINDA EXISTE" if existe else "removida"}')

# 2. Valores sensiveis vindos dos originais (lidos do Git, nunca impressos)
p3 = git('show', f'{COMMIT}:docs/00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md')
conta = re.search(r'togglemaster-tfstate-(\d{12})-', p3).group(1)
d3 = git('show', f'{COMMIT}:docs/00_COLAB_IA/DECISOES.md')
caminhos_pessoais = set(re.findall(r'C:\\Users\\([^\\`]+)\\Documents', d3)) - {'Gabriel'}
# Tabela de integrantes do relatorio preliminar arquivado: nomes, RMs e usuarios do Discord (lidos do Git, nunca impressos).
rel3 = git('show', f'{COMMIT}:docs/00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md').splitlines()
cab = next(i for i, l in enumerate(rel3) if l.startswith('|') and 'RM' in l)
celulas = set()
for l in rel3[cab + 2:]:
    if not l.startswith('|'): break
    celulas |= {c.strip() for c in l.strip('|').split('|') if len(c.strip()) >= 4}
proibidos = {'ID da conta antiga': [conta], 'caminho pessoal da Fase 3': [f'C:\\Users\\{n}' for n in caminhos_pessoais] + list(caminhos_pessoais),
             'dado de integrante (nome/RM/Discord)': sorted(celulas)}
padroes = {
    'e-mail': re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'),
    'webhook Slack real': re.compile(r'hooks\.slack\.com/services/T[A-Z0-9]{6,}/B[A-Z0-9]{6,}/[A-Za-z0-9]{12,}'),
    'chave New Relic (NRAK/NRAL)': re.compile(r'NRAK-[A-Z0-9]{20,}|[0-9a-f]{36}NRAL'),
    'hex de 32 (possivel routing key)': re.compile(r'(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])'),
    'ARN com conta': re.compile(r'arn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:'),
}
for rel in NOVOS:
    p = RAIZ / rel
    if not p.exists():
        print(f'[2] {rel}: (nao existe)'); continue
    t = p.read_text(encoding='utf-8')
    for nome, vals in proibidos.items():
        n = sum(t.count(v) for v in vals)
        if n: falhas.append(f'{rel}: {nome}'); print(f'[2] {rel}: {nome} x{n}  <-- FALHA')
    for nome, rx in padroes.items():
        hits = [m for m in rx.finditer(t) if not (nome == 'e-mail' and m.group().endswith(('anthropic.com', 'example.com')))]
        if hits:
            linhas = sorted({t.count('\n', 0, m.start()) + 1 for m in hits})
            print(f'[2] {rel}: {nome} x{len(hits)} nas linhas {linhas[:8]} (revisar)')
print(f'[2] busca de sensiveis concluida (referencias: {len(caminhos_pessoais)} caminho pessoal, {len(celulas)} celulas da tabela de integrantes)')

# 3. Links relativos dos arquivos novos ou editados
quebrados = []
for rel in NOVOS:
    p = RAIZ / rel
    if not p.exists(): continue
    for m in re.finditer(r'\]\(([^)\s]+)\)', p.read_text(encoding='utf-8')):
        alvo = m.group(1).split('#')[0]
        if not alvo or re.match(r'[a-z]+:', alvo): continue
        if not (p.parent / urllib.parse.unquote(alvo)).exists():
            quebrados.append(f'{rel} -> {alvo}')
print(f'[3] links relativos quebrados: {len(quebrados)}')
for q in quebrados: print('    ', q)
if quebrados: falhas.append('links')

# 4. Ponteiros de estado atual que nao podem mais tratar a pasta da Fase 3 como existente
for rel in ['CLAUDE.md', '00_COLAB_IA/LEIA-PRIMEIRO.md']:
    t = (RAIZ / rel).read_text(encoding='utf-8')
    linhas = [i + 1 for i, l in enumerate(t.splitlines()) if 'docs/00_COLAB_IA' in l and not re.search(r'mesclad|removid|descartad', l)]
    print(f'[4] {rel}: mencoes a docs/00_COLAB_IA sem indicar a mescla: {linhas or "nenhuma"}')
    if linhas: falhas.append(f'{rel}: ponteiro antigo')

# 5. Estado do Git na pasta removida
st = git('status', '--short', '--', 'docs/00_COLAB_IA').splitlines()
print(f'[5] git status em docs/00_COLAB_IA: {len(st)} entradas, {sum(l.startswith(" D") for l in st)} remocoes nao preparadas')
print('RESULTADO:', 'OK' if not falhas else 'FALHAS -> ' + '; '.join(falhas))
sys.exit(1 if falhas else 0)
