from pathlib import Path
import re, json, html, unicodedata
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).parent
E=html.escape

def badge(ident):
    cls='obrigatorio' if ident.startswith('REQ-OBR') else 'bonus' if ident.startswith('REQ-BON') else 'sugestao'
    label={'obrigatorio':'OBRIGATÓRIO','bonus':'BÔNUS / OPÇÃO','sugestao':'SUGESTÃO'}[cls]
    return f'<a class="badge {cls}" href="../../requisitos/README.md#{ident.lower()}">{label} · {ident}</a>'

def section(ident,title,body):
    return f'<section id="{ident}"><h2>{E(title)}</h2><div class="section-rule"></div>{body}</section>'

def table(headers,rows):
    return '<div class="tablewrap"><table><thead><tr>'+''.join('<th scope="col">'+E(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def complement(content):
    return '<aside class="complemento"><strong>📘 Complemento — elaboração didática do Codex</strong>'+content+'</aside>'

def code(text,source,explanation):
    return '<figure class="code-example"><figcaption>'+E(source)+'</figcaption><pre><code>'+E(text)+'</code></pre><p>'+explanation+'</p></figure>'

def write_guide(folder,title,subtitle,content,connections,level='Introdutório a intermediário'):
    module=ROOT/'docs/aulas-fiap'/folder
    inv=json.loads((WORK/'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))
    src=[x for x in inv if Path(x['source']).parent.name==folder]
    src.sort(key=lambda x:int(re.search(r'Aula (\d+)',x['source']).group(1)) if re.search(r'Aula (\d+)',x['source']) else 0)
    sources='<ul class="sources">'+''.join(f'<li><a href="{quote(Path(x["source"]).name)}">{E(Path(x["source"]).name)}</a><br><span class="source">{x["pages"]} páginas · leitura integral</span></li>' for x in src)+'</ul>'
    connection=section('conexao','Conexão com o Tech Challenge Fase 4', '<p>As exigências vêm do enunciado; o vínculo com esta aula é um mapeamento didático. Estudar o tema não comprova atendimento. Status da implementação: <strong>Pendente</strong>.</p>'+table(['ID','Selo','Como este conteúdo ajuda a cumprir'],[(E(i),badge(i),d) for i,d in connections]))
    content+=connection
    headings=re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>',content,re.S)
    toc='<nav class="toc" aria-label="Sumário"><strong>Neste guia</strong><ol>'+''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t in headings)+'</ol></nav>'
    name=re.sub(r'^\d+[._ -]*','',folder)
    name=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode()
    name=re.sub(r'[^A-Za-z0-9]+','-',name).strip('-')
    output=module/f'GUIA-ESTUDO-{name}.html'
    page=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} — Guia de estudo · Fase 4</title><style>{(WORK/'guia-base-2026-09-16_v01.css').read_text(encoding='utf8')}</style></head>
<body><a class="skip" href="#conteudo">Ir ao conteúdo</a><main class="wrap" id="conteudo"><header class="masthead"><p class="eyebrow">FIAP · Tech Challenge Fase 4 · Guia de estudo</p><h1>{E(title)}</h1><p class="sub">{E(subtitle)}</p><div class="meta"><span>Gerado em 2026-09-16 · Codex</span><span>{len(src)} arquivo(s) · {sum(x['pages'] for x in src)} páginas</span><span>{E(level)}</span></div><p><a href="../../requisitos/README.md">Consultar requisitos e índice dos cinco guias</a></p><details class="source-list"><summary>Arquivos-fonte usados integralmente</summary>{sources}</details></header>
<aside class="legend" aria-label="Legenda dos selos"><span class="badge obrigatorio">🔴 Obrigatório</span> <span class="badge bonus">🟢 Bônus / opção</span> <span class="badge sugestao">🔵 Sugestão</span> <span class="badge complemento-badge">📘 Complemento</span><p>“Bônus” identifica opções/preferências do PDF, sem promessa de pontos extras. Complementos são explicações autorais, não texto nem exigência da FIAP. Referências de páginas usam a contagem física do PDF, a partir de 1.</p></aside>
{toc}{content}<footer><a href="#conteudo">Voltar ao início</a><p>Fontes locais consultadas em 2026-09-16. Síntese didática com referências por página, sem execução de comandos ou comprovação de infraestrutura. Requisitos: enunciado da Fase 4, p. 2–6. Material autocontido, sem dependências externas.</p></footer></main></body></html>'''
    output.write_text(page,encoding='utf8')
    print(output)
    return output
