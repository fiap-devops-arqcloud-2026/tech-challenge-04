"""Gera docs/requisitos/REQUISITOS.html a partir de docs/requisitos/README.md (D-006).

Motivo (F-007): aberto por duplo clique, o navegador mostra o Markdown como texto e não rola até
`#req-obr-NN`. O espelho HTML resolve a navegação local dos selos dos guias. A fonte de verdade
continua sendo o README.md: este arquivo é gerado, nunca editado à mão.

Uso: python -X utf8 gerar-espelho-requisitos-2026-09-20_v01.py
Converte o subconjunto de Markdown usado no README: títulos, parágrafos, listas, checkboxes,
tabelas, negrito, código inline, links e HTML inline (âncoras <a id="...">).
Autor: Claude (Opus 5), 2026-09-20.
"""
from pathlib import Path
import html as H
import re
import unicodedata

W = Path(__file__).parent
R = W.parents[1]
SRC = R / 'docs/requisitos/README.md'
OUT = R / 'docs/requisitos/REQUISITOS.html'
CSS = (W / 'guia-base-2026-09-16_v01.css').read_text(encoding='utf8')
DATA = '2026-09-20'
AGENTE = 'Claude (Opus 5)'

TOKEN = '\x00'  # protege HTML inline durante o escape


def inline(txt):
    guardados = []

    def guardar(m):
        guardados.append(m.group(0))
        return f'{TOKEN}{len(guardados) - 1}{TOKEN}'

    txt = re.sub(r'<a id="[^"]+"></a>|<br\s*/?>', guardar, txt)
    txt = H.escape(txt, quote=False)
    txt = re.sub(r'`([^`]+)`', lambda m: '<code>' + m.group(1) + '</code>', txt)
    txt = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', txt)
    txt = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', txt)
    txt = re.sub(TOKEN + r'(\d+)' + TOKEN, lambda m: guardados[int(m.group(1))], txt)
    return txt


def slug(txt):
    s = unicodedata.normalize('NFKD', re.sub(r'<[^>]+>', '', txt)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


linhas = SRC.read_text(encoding='utf8').splitlines()
saida, i, sumario = [], 0, []
while i < len(linhas):
    l = linhas[i]
    if not l.strip():
        i += 1
        continue
    if l.startswith('# '):
        saida.append(f'<h1>{inline(l[2:].strip())}</h1>')
        i += 1
    elif l.startswith('## '):
        t = l[3:].strip()
        s = slug(t)
        sumario.append((s, t))
        saida.append(f'<section id="{s}"><h2>{inline(t)}</h2><div class="section-rule"></div>')
        i += 1
    elif l.startswith('### '):
        saida.append(f'<h3>{inline(l[4:].strip())}</h3>')
        i += 1
    elif l.lstrip().startswith('|') and i + 1 < len(linhas) and re.match(r'^\s*\|[\s:|-]+\|\s*$', linhas[i + 1]):
        cab = [c.strip() for c in l.strip().strip('|').split('|')]
        i += 2
        corpo = []
        while i < len(linhas) and linhas[i].lstrip().startswith('|'):
            corpo.append([c.strip() for c in linhas[i].strip().strip('|').split('|')])
            i += 1
        saida.append('<div class="tablewrap"><table><thead><tr>' + ''.join(f'<th scope="col">{inline(c)}</th>' for c in cab) + '</tr></thead><tbody>'
                     + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in linha) + '</tr>' for linha in corpo) + '</tbody></table></div>')
    elif re.match(r'^\s*-\s', l):
        itens = []
        while i < len(linhas) and re.match(r'^\s*-\s', linhas[i]):
            item = re.sub(r'^\s*-\s+', '', linhas[i])
            marcado = item.startswith('[x] ')
            vazio = item.startswith('[ ] ')
            if marcado or vazio:
                item = item[4:]
                itens.append(f'<li class="check"><span class="box" aria-hidden="true">{"&#10003;" if marcado else "&#9633;"}</span><span class="rotulo">{inline(item)}</span></li>')
            else:
                itens.append(f'<li>{inline(item)}</li>')
            i += 1
        classe = ' class="checklist"' if any('class="check"' in x for x in itens) else ''
        saida.append(f'<ul{classe}>' + ''.join(itens) + '</ul>')
    else:
        par = [l]
        i += 1
        while i < len(linhas) and linhas[i].strip() and not re.match(r'^\s*[-|#]', linhas[i]):
            par.append(linhas[i])
            i += 1
        saida.append('<p>' + inline(' '.join(x.strip() for x in par)) + '</p>')

corpo = ''.join(saida)
corpo = re.sub(r'(<section id="[^"]+">)', lambda m: '</section>' + m.group(1), corpo, count=len(sumario))
corpo = corpo.replace('</section>', '', 1) + '</section>'
toc = '<nav class="toc" aria-label="Sumário"><strong>Neste documento</strong><ol>' + ''.join(f'<li><a href="#{s}">{inline(t)}</a></li>' for s, t in sumario) + '</ol></nav>'
extra = ('.checklist{list-style:none;padding-left:0}.checklist li{display:grid;grid-template-columns:24px 1fr;gap:8px;'
         'align-items:start;padding:6px 0;border-bottom:1px solid var(--line-soft)}.checklist .box{font-family:var(--mono);color:var(--accent-ink)}'
         'ul{max-width:68ch}li{margin-bottom:6px}h1{font-family:var(--serif);font-size:clamp(1.9rem,5.6vw,2.6rem);margin:0 0 6px}'
         'h3{margin-top:28px}td,th{vertical-align:top}')
pagina = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Requisitos — Tech Challenge Fase 4</title><style>{CSS}{extra}</style></head>
<body><a class="skip" href="#conteudo">Ir ao conteúdo</a><main class="wrap" id="conteudo"><header class="masthead"><p class="eyebrow">FIAP · Tech Challenge Fase 4 · Requisitos</p><div class="meta"><span>Espelho HTML gerado em {DATA} · {AGENTE}</span><span>Fonte de verdade: <a href="README.md">README.md</a></span></div></header>
<aside class="legend" aria-label="Aviso"><p>Documento <strong>gerado automaticamente</strong> a partir de <code>README.md</code> por <code>00_COLAB_IA/02_TRABALHO/gerar-espelho-requisitos-2026-09-20_v01.py</code>, para que as âncoras dos selos dos guias funcionem ao abrir os arquivos localmente. Não editar à mão: alterar o Markdown e gerar de novo.</p></aside>
{toc}{corpo}<footer><a href="#conteudo">Voltar ao início</a><p>Conteúdo idêntico ao README.md de requisitos. Classificação e evidências vêm do enunciado da Fase 4, p. 2–6.</p></footer></main></body></html>'''
OUT.write_text(pagina, encoding='utf8')
print(OUT, len(pagina), 'bytes;', len(sumario), 'seções')
