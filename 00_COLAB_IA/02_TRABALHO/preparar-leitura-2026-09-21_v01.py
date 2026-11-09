"""Prepara a leitura de uma aula: remove cabeçalhos/rodapés repetidos da extração e aponta as
páginas que exigem conferência visual (código, figuras, tabelas).

Uso:
  python -X utf8 preparar-leitura-2026-09-21_v01.py --id 15            # texto limpo no stdout
  python -X utf8 preparar-leitura-2026-09-21_v01.py --id 15 --mapa     # só o mapa de páginas
  python -X utf8 preparar-leitura-2026-09-21_v01.py --id 15 --paginas 5-12

Não altera nenhuma fonte. Autor: Claude (Opus 5), 2026-09-21.
"""
from pathlib import Path
import argparse
import json
import re

W = Path(__file__).parent
INV = json.loads((W / 'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))

CODIGO = re.compile(r'(?m)^\s*(import |from \w+ import|def |class |curl |docker |kubectl |helm |apiVersion|version:|'
                    r'scrape_configs|receivers:|exporters:|processors:|service:|SELECT |FROM |WHERE |\{|\}|"[\w-]+"\s*:|'
                    r'[a-z_]+\s*=\s*[\w\'"(]|DD_[A-Z_]+|NEW_RELIC|newrelic|- name:|\$ |sudo |export |npm |pip |dotnet |'
                    r'java -|node |yum |apt-get)')
MARCA = re.compile(r'Código Fonte|Código Prático|Figura \d|Tabela \d|Quadro \d|Gráfico \d', re.I)


def paginas_do_texto(txt):
    partes = re.split(r'===== PÁGINA (\d+) =====', txt)
    return [(int(partes[i]), partes[i + 1]) for i in range(1, len(partes) - 1, 2)]


def limpar(pag_txt, titulo):
    linhas = []
    for l in pag_txt.splitlines():
        if re.match(r'^\s*$', l):
            continue
        if re.search(r'Página \d+ de \d+', l):
            continue
        if titulo and l.strip().startswith(titulo[:28]) and len(l.strip()) < len(titulo) * 2 + 40:
            continue
        linhas.append(l.rstrip())
    return '\n'.join(linhas)


ap = argparse.ArgumentParser()
ap.add_argument('--id', type=int, required=True)
ap.add_argument('--mapa', action='store_true')
ap.add_argument('--paginas')
a = ap.parse_args()

fonte = next(x for x in INV if x['id'] == a.id)
arq = next(p for p in (W / 'extracoes-pdfium').glob(f'{a.id:02}-*.txt'))
txt = arq.read_text(encoding='utf8')
paginas = paginas_do_texto(txt)
titulo = paginas[0][1].strip().splitlines()[0].strip() if paginas else ''
titulo = re.sub(r'\s*\|?\s*AULA \d+.*$', '', titulo).strip()

quero = None
if a.paginas:
    quero = set()
    for parte in a.paginas.split(','):
        if '-' in parte:
            x, y = parte.split('-')
            quero.update(range(int(x), int(y) + 1))
        else:
            quero.add(int(parte))

if a.mapa:
    print(f'id {a.id}: {Path(fonte["source"]).name} — {len(paginas)} páginas — título: {titulo}')
    for n, p in paginas:
        limpo = limpar(p, titulo)
        marcas = sorted(set(MARCA.findall(p)))
        cod = len(CODIGO.findall(limpo))
        flag = 'CÓDIGO' if cod >= 3 else ('código?' if cod else '')
        if marcas or flag:
            print(f'  p.{n:>2}: {len(limpo):>5} car · {flag:<7} {", ".join(marcas)}')
else:
    for n, p in paginas:
        if quero and n not in quero:
            continue
        limpo = limpar(p, titulo)
        if limpo:
            print(f'----- p.{n}\n{limpo}')
