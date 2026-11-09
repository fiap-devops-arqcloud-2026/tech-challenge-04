"""Monta um GUIA-ESTUDO-*.html a partir de fragmentos HTML, com o mesmo cabeçalho, CSS, legenda,
sumário e seção de conexão gerados por guia_base.write_guide (consistência visual com B1–B3).

Uso: python -X utf8 montar-guia-2026-09-16_v01.py fragmentos/apm/config.json

config.json:
{
  "pasta": "03.APM",                      # nome exato da pasta em docs/aulas-fiap
  "titulo": "...", "subtitulo": "...", "nivel": "...",
  "agente": "Claude (Opus 5)", "data": "AAAA-MM-DD", "revisao": "",
  "fragmentos": ["00-visao-geral.html", "01-glossario.html", ...],   # ordem explícita, relativa à pasta do config
  "conexoes": "conexoes.json"             # lista [["REQ-OBR-07", "texto HTML"], ...]
}
Cada fragmento contém uma ou mais <section id="..."><h2>...</h2><div class="section-rule"></div>...</section>.
Autor: Claude (Opus 5), 2026-09-16.
"""
from pathlib import Path
import json, re, sys
import guia_base

cfg_path = Path(sys.argv[1]).resolve()
base = cfg_path.parent
cfg = json.loads(cfg_path.read_text(encoding='utf8'))
guia_base.AGENTE = cfg.get('agente', 'Claude (Opus 5)')
guia_base.DATA = cfg['data']
guia_base.REVISAO = cfg.get('revisao', '')

content, ids = '', []
for nome in cfg['fragmentos']:
    frag = (base / nome).read_text(encoding='utf8').strip()
    if not frag.startswith('<section id="'):
        raise SystemExit(f'{nome}: fragmento deve começar com <section id="...">')
    if frag.count('<section') != frag.count('</section>'):
        raise SystemExit(f'{nome}: <section> desbalanceado')
    novos = re.findall(r'<section id="([^"]+)">\s*<h2>', frag)
    if not novos:
        raise SystemExit(f'{nome}: seção sem <h2> logo após a abertura')
    ids += novos
    content += frag
dup = sorted({i for i in ids if ids.count(i) > 1})
if dup:
    raise SystemExit(f'IDs de seção duplicados: {dup}')
if 'conexao' in ids:
    raise SystemExit('id "conexao" é reservado à seção gerada automaticamente')
conexoes = [tuple(x) for x in json.loads((base / cfg['conexoes']).read_text(encoding='utf8'))]
guia_base.write_guide(cfg['pasta'], cfg['titulo'], cfg['subtitulo'], content, conexoes, cfg.get('nivel', 'Introdutório a intermediário'))
