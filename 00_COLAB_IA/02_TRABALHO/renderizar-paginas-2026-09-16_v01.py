"""Renderiza páginas de um PDF do inventário para inspeção visual (somente leitura dos originais).

Uso (Python do runtime Codex, que possui pypdfium2):
  python -X utf8 renderizar-paginas-2026-09-16_v01.py --id 15 --paginas 4,15-17 --saida qa-apm --prefixo a01 [--escala 2]

--id: campo "id" do inventario-fontes-2026-09-16_v01.json (0 = enunciado; 15–24 = APM; 25–31 = Incidentes).
Saída: 02_TRABALHO/<saida>/<prefixo>-pNN.png. Não sobrescreve arquivo existente, a menos que --forcar seja usado.
Autor: Claude (Opus 5), 2026-09-16.
"""
from pathlib import Path
import argparse, json
import pypdfium2 as pdfium

W = Path(__file__).parent
R = W.parents[1]

def paginas(expr, total):
    out = []
    for parte in expr.split(','):
        parte = parte.strip()
        if not parte:
            continue
        if '-' in parte:
            a, b = parte.split('-', 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(parte))
    invalidas = [p for p in out if p < 1 or p > total]
    if invalidas:
        raise SystemExit(f'Páginas fora do intervalo 1–{total}: {invalidas}')
    return sorted(set(out))

ap = argparse.ArgumentParser()
ap.add_argument('--id', type=int, required=True)
ap.add_argument('--paginas', required=True)
ap.add_argument('--saida', required=True)
ap.add_argument('--prefixo', required=True)
ap.add_argument('--escala', type=float, default=2.0)
ap.add_argument('--forcar', action='store_true')
a = ap.parse_args()

inv = json.loads((W / 'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))
fonte = next(x for x in inv if x['id'] == a.id)
destino = W / a.saida
destino.mkdir(exist_ok=True)
doc = pdfium.PdfDocument(R / fonte['source'])
try:
    for n in paginas(a.paginas, len(doc)):
        arq = destino / f'{a.prefixo}-p{n:02}.png'
        if arq.exists() and not a.forcar:
            print(f'existe: {arq}')
            continue
        pg = doc[n - 1]
        bm = pg.render(scale=a.escala)
        bm.to_pil().save(arq)
        bm.close(); pg.close()
        print(arq)
finally:
    doc.close()
