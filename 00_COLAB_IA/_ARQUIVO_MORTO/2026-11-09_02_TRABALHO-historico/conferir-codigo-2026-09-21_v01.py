"""Confere cada bloco <pre><code> dos fragmentos contra o texto extraído da aula correspondente.

Para cada bloco, extrai os tokens distintivos (>=4 caracteres, alfanuméricos com _ . - / :) e mede
quantos aparecem na extração PDFium daquela aula. Bloco com baixa cobertura é candidato a código
inventado ou transcrito de outra fonte — não é prova, é triagem para conferência visual.

Uso: python -X utf8 conferir-codigo-2026-09-21_v01.py
Autor: Claude (Opus 5), 2026-09-21.
"""
from pathlib import Path
import glob, html, json, re, unicodedata

W = Path(__file__).parent
EXTR = W / 'extracoes-pdfium'

# fragmento -> id do inventário
MAPA = {
    'apm/02-aula-01.html': 15, 'apm/03-aula-02.html': 17, 'apm/04-aula-03.html': 18,
    'apm/05-aula-04.html': 19, 'apm/06-aula-05.html': 20, 'apm/07-aula-06.html': 21,
    'apm/08-aula-07.html': 22, 'apm/09-aula-08.html': 23, 'apm/10-aula-09.html': 24,
    'apm/11-aula-10.html': 16,
    'incidentes/02-aula-01.html': 25, 'incidentes/03-aula-02.html': 26, 'incidentes/04-aula-03.html': 27,
    'incidentes/05-aula-04.html': 28, 'incidentes/06-aula-05.html': 29, 'incidentes/07-aula-06.html': 30,
    'incidentes/08-aula-07.html': 31,
}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', s)

def tokens(s):
    return {t for t in re.findall(r'[A-Za-z0-9_./:\-]{4,}', s) if not t.isdigit()}

total = flag = 0
for frag, fid in MAPA.items():
    p = W / 'fragmentos' / frag
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf8')
    fonte = norm(next(EXTR.glob(f'{fid:02}-*.txt')).read_text(encoding='utf8'))
    fonte_tok = tokens(fonte)
    for i, (cap, cod) in enumerate(re.findall(r'<figcaption>(.*?)</figcaption><pre><code>(.*?)</code></pre>', txt, re.S), 1):
        codigo = html.unescape(re.sub('<[^>]+>', '', cod))
        tk = tokens(codigo)
        if not tk:
            continue
        # token presente se aparecer no texto da aula (comparação normalizada, ignorando caixa)
        achados = {t for t in tk if norm(t) in fonte or t.lower() in fonte_tok}
        cob = len(achados) / len(tk)
        total += 1
        if cob < 0.80:
            flag += 1
            faltando = sorted(tk - achados)[:12]
            legenda = re.sub('<[^>]+>', '', cap)[:70]
            print(f'{frag} bloco {i}: cobertura {cob:.0%} ({len(achados)}/{len(tk)}) — {legenda}')
            print(f'   ausentes na extração: {faltando}')
print(f'\n{total} blocos de código conferidos; {flag} abaixo de 80% de cobertura de tokens.')
