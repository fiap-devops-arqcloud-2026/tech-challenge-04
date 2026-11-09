"""Verifica cobertura, links, fontes, preservação e limites da P-016; não altera projetos."""
from pathlib import Path
from datetime import datetime
import hashlib, json, re, subprocess, sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
SNAP = json.loads((WORK / 'snapshot-retomada-codex.json').read_text(encoding='utf-8'))
COLAB = ROOT / '00_COLAB_IA'
ACERVO = COLAB / '_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA'
PRE = '--antes' in sys.argv
failures, warnings = [], []

def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def check(condition, name):
    if not condition: failures.append(name)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def text(path): return path.read_text(encoding='utf-8')
def mapped(path):
    if PRE and path.is_relative_to(ACERVO):
        return ROOT / 'docs/00_COLAB_IA' / path.relative_to(ACERVO)
    return path

check(git('branch','--show-current').decode().strip()==SNAP['branch']=='dev','branch')
check(git('rev-parse','HEAD').decode().strip()==SNAP['head'],'HEAD')
check(git('rev-parse','main').decode().strip()==SNAP['main'],'main')
check(not git('diff','--cached','--name-only').strip(),'index possui mudanças preparadas')

context = ['CLAUDE.md'] + ['00_COLAB_IA/' + n + '.md' for n in ['LEIA-PRIMEIRO','PENDENCIAS_E_PROXIMOS_PASSOS','LOG_DE_TRABALHO','DOSSIE_CONTEXTO','DECISOES','ORGANIZACAO_DE_PASTAS']]
verified_files, original_absent = 0, []
for rel, initial in SNAP['files'].items():
    if rel in context or rel.startswith('docs/00_COLAB_IA/'):
        continue
    p = ROOT / rel
    if initial is None:
        check(not p.exists(), 'ausência anterior alterada: ' + rel)
        original_absent.append(rel)
    else:
        check(p.is_file() and digest(p)==initial['sha256'], 'arquivo anterior alterado: '+rel)
        verified_files += 1

source_now = ROOT / 'docs/00_COLAB_IA' if PRE else ACERVO
check(source_now.is_dir(), 'acervo ausente')
if not PRE: check(not (ROOT/'docs/00_COLAB_IA').exists(), 'pasta ativa ainda existe')
actual = {p.relative_to(source_now).as_posix() for p in source_now.rglob('*') if p.is_file()}
expected = {d['path'].removeprefix('docs/00_COLAB_IA/') for d in SNAP['originals']}
check(actual == expected and len(actual)==39, 'inventário acervo diferente de 39')
for entry in SNAP['originals']:
    p = source_now / entry['path'].removeprefix('docs/00_COLAB_IA/')
    check(p.is_file() and digest(p)==entry['sha256'], 'hash acervo: '+entry['path'])
    blob = git('rev-parse', '3b21e65:'+entry['path']).decode().strip()
    check(blob == entry['blob'], 'blob original: '+entry['path'])

dest = [ROOT / rel for rel in context]
dest += [COLAB/'02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md', WORK/'INDICE_RASTREABILIDADE_2026-11-01_v01.md']
link_count = 0
for p in dest:
    check(p.is_file(), 'destino ausente: '+p.name)
    if not p.is_file(): continue
    content = text(p)
    check('\ufffd' not in content, 'UTF-8 substituído: '+p.name)
    check('PREENCHER_VERIFICACAO' not in content, 'placeholder final: '+p.name)
    # Links Markdown; caminhos em crases de registros históricos não são links ativos.
    for m in re.finditer(r'\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)', content):
        url = m.group(1) or m.group(2)
        if re.match(r'^[a-zA-Z][\w+.-]*:', url): continue
        location, _, fragment = unquote(url).partition('#')
        target = mapped((p.parent / location).resolve()) if location else p
        link_count += 1
        check(target.exists(), f'link quebrado: {p.name} -> {url}')
        if fragment and target.is_file() and target.suffix.lower()=='.md':
            headings = re.findall(r'^#{1,6}\s+(.+)$', text(target), re.M)
            anchors = [re.sub(r'[^\w\- ]', '', h.replace('`','').lower()).replace(' ','-') for h in headings]
            check(fragment in anchors, f'âncora ausente: {p.name} -> {url}')
    if p.name!='LOG_DE_TRABALHO.md':
        check('TL;DR' in content and 'Última atualização: 2026-11-01' in content, 'metadados: '+p.name)

dec = text(COLAB/'DECISOES.md')
ids = re.findall(r'^### (F3-(?:D-\d{3}|SN-\d{2})) —', dec, re.M)
expected_ids = [x['id'] for x in json.loads(text(WORK/'rascunhos/consolidar_decisoes.json'))['decisoes']]
check(set(ids)==set(expected_ids) and len(ids)==59, '59 decisões distintas')
index = json.loads(text(WORK/'indice-rastreabilidade.json'))
check(len(index['conhecimentos'])==158 and len({x['id'] for x in index['conhecimentos']})==158, '158 conhecimentos distintos no índice')
check(len(index['pendencias'])==39 and len({x['id'] for x in index['pendencias']})==39, '39 registros de pendências no índice')
index_md = text(WORK/'INDICE_RASTREABILIDADE_2026-11-01_v01.md')
check(all(x['id'] in index_md for xs in index.values() for x in xs), 'índice Markdown incompleto')
for d in ['D-017','D-018']: check(f'## {d} —' in dec, d+' ausente')
for p in dest:
    if not p.is_file(): continue
    used = set(re.findall(r'\bF3-(?:D-\d{3}|SN-\d{2})\b', text(p)))
    check(used <= set(expected_ids), 'ID de decisão inexistente: '+p.name)

all_sources, invalid_sources, invalid_lines = set(), [], []
for file in sorted((WORK/'rascunhos').glob('consolidar*.json')):
    if 'pagerduty' in file.name: continue
    data = json.loads(text(file))
    def walk(o):
        if isinstance(o, dict):
            for k,v in o.items():
                if k=='fontes' and isinstance(v,list):
                    all_sources.update(s for s in v if s.startswith('docs/00_COLAB_IA/'))
                else: walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(data)
for ref in sorted(all_sources):
    m = re.match(r'^(docs/00_COLAB_IA/.*?)(?::(\d+)(?:-(\d+))?)?$',ref)
    rel, start, end = m.groups()
    p = source_now / rel.removeprefix('docs/00_COLAB_IA/')
    if not p.is_file(): invalid_sources.append(ref); continue
    if start and p.suffix.lower() not in ['.pdf','.png']:
        lines=len(text(p).splitlines())
        if not 1<=int(start)<=int(end or start)<=lines: invalid_lines.append(ref)
check(not invalid_sources, 'fontes inexistentes na consolidação')
check(not invalid_lines, 'linhas de fonte fora de alcance')

# Checar ausência de dados pessoais extraídos nos novos documentos. Não imprimir valores.
old_p = git('show','3b21e65:docs/00_COLAB_IA/PENDENCIAS_E_PROXIMOS_PASSOS.md').decode()
old_account = re.search(r'togglemaster-tfstate-(\d{12})-',old_p).group(1)
old_dec = git('show','3b21e65:docs/00_COLAB_IA/DECISOES.md').decode()
users = set(re.findall(r'C:\\Users\\([^\\`]+)\\Documents',old_dec)) - {'Gabriel'}
old_report = git('show','3b21e65:docs/00_COLAB_IA/_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md').decode().splitlines()
begin = next(i for i,l in enumerate(old_report) if l.startswith('|') and 'RM' in l)
cells=set()
for line in old_report[begin+2:]:
    if not line.startswith('|'): break
    cells.update(c.strip() for c in line.strip('|').split('|') if len(c.strip())>=4)
for p in dest:
    if not p.is_file(): continue
    content = text(p)
    # LOG mantém entradas históricas intactas: checar só a adição da sessão.
    baseline = Path(SNAP['context_backups']) / p.relative_to(ROOT)
    if p.name=='LOG_DE_TRABALHO.md' and baseline.exists():
        old_lines=set(text(baseline).splitlines())
        content='\n'.join(l for l in content.splitlines() if l not in old_lines)
    for kind, vals in [('conta antiga',[old_account]),('caminho pessoal',users),('participante',cells)]:
        check(not any(v in content for v in vals), f'dado herdado indevido ({kind}): {p.name}')
    for label, regex in [('Slack',r'hooks\.slack\.com/services/T[A-Z0-9]{6,}/B[A-Z0-9]{6,}/[A-Za-z0-9]{12,}'),('New Relic',r'NRAK-[A-Z0-9]{20,}|[0-9a-f]{36}NRAL')]:
        check(not re.search(regex,content), f'padrão de segredo ({label}): {p.name}')

# Não reescrever as antigas sessões do LOG; o conteúdo anterior inteiro deve sobreviver.
log_before = text(Path(SNAP['context_backups'])/'00_COLAB_IA/LOG_DE_TRABALHO.md')
log_after = text(COLAB/'LOG_DE_TRABALHO.md')
check(log_before.partition('\n\n')[2] in log_after, 'histórico do LOG reescrito')

if not PRE:
    deleted=git('diff','--name-only','--diff-filter=D','-z','--','docs/00_COLAB_IA').decode().split('\0')
    check(set(filter(None,deleted))==set(x['path'] for x in SNAP['originals']), '39 remoções esperadas no Git')

result={'date':datetime.now().astimezone().isoformat(),'mode':'antes' if PRE else 'depois','ok':not failures,'checks':{'originals':len(actual),'preserved_other_files':verified_files,'preexisting_absences':len(original_absent),'decision_ids':len(ids),'knowledge_index':158,'pending_source_records':39,'local_links':link_count,'source_references':len(all_sources)},'failures':failures,'warnings':warnings,'invalid_source_files':invalid_sources,'invalid_source_lines':invalid_lines,'limits':'Hash comprova preservação, não leitura semântica integral. Varredura de dados limitada a padrões e valores derivados dos originais; arquivo morto preserva o conteúdo antigo.'}
(WORK/f'verificacao-codex-{"antes" if PRE else "depois"}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if result['ok'] else 1)
