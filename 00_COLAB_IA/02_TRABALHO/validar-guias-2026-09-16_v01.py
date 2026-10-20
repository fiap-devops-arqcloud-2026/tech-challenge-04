"""Validador estático dos guias GUIA-ESTUDO-*.html e dos links do README de requisitos.

Uso: python -X utf8 validar-guias-2026-09-16_v01.py [caminho.html ...]
     python -X utf8 validar-guias-2026-09-16_v01.py --fragmento "03.APM" fragmentos/apm/02-aula-01.html ...
Sem argumentos, valida todos os guias em docs/aulas-fiap/*/ e o README.
Saída: relatório por arquivo; código de saída 1 se houver ERRO.
Autor: Claude (Opus 5), 2026-09-16. Não altera nenhum arquivo.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json, re, sys, unicodedata

W = Path(__file__).parent
R = W.parents[1]
README = R / 'docs/requisitos/README.md'
INV = json.loads((W / 'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))
PAGES = {unicodedata.normalize('NFC', Path(x['source']).name): x['pages'] for x in INV}

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
BLOCK_IN_P = {'address', 'article', 'aside', 'blockquote', 'details', 'div', 'dl', 'fieldset', 'figcaption', 'figure',
              'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'main', 'nav', 'ol', 'p', 'pre',
              'section', 'table', 'ul', 'summary'}
ID_RE = re.compile(r'\b(REQ-OBR-\d{2}|REQ-BON-\d{2}|SUG-\d{2})\b')
MOJIBAKE = re.compile(r'Ã[§£©¡º³­ª¢µ‰ƒ‡]|Â[·ª°º]|â€|�')
# "placeholder" sozinho é vocabulário técnico legítimo (message templates do Serilog, por exemplo);
# só marcadores de rascunho de verdade são proibidos.
PROIBIDOS = re.compile(r'\bTODO\b|(?i:lorem ipsum|\[placeholder\]|texto placeholder|a mapear|em construção|preencher aqui)|\bXXX\b|PDF exclusivo|@gmail\.com|\bFIXME\b')

readme_txt = README.read_text(encoding='utf8')
README_IDS = set(re.findall(r'<a id="([^"]+)"></a>', readme_txt))
README_REQ = set(ID_RE.findall(readme_txt))


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.warns = [], [], []
        self.ids, self.hrefs, self.srcs = {}, [], []
        self.text_parts, self.pre_depth = [], 0
        self.sections, self.cur_section = [], None
        self.tables, self.cur_table = [], None
        self.has_charset = self.lang_ok = False
        self.external = []
        self.complement_pending = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == 'html' and a.get('lang') == 'pt-BR':
            self.lang_ok = True
        if tag == 'meta' and (a.get('charset') or '').upper() == 'UTF-8':
            self.has_charset = True
        if tag in ('script', 'link', 'iframe', 'object', 'embed'):
            self.external.append((line, tag))
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append(f'l.{line}: id duplicado "{a["id"]}" (primeiro na l.{self.ids[a["id"]]})')
            else:
                self.ids[a['id']] = line
        if 'href' in a:
            self.hrefs.append((line, a['href']))
        if 'src' in a:
            self.srcs.append((line, a['src']))
            if a['src'].startswith(('http:', 'https:', '//')):
                self.external.append((line, 'src=' + a['src']))
        if self.pre_depth and tag != 'code':
            self.errors.append(f'l.{line}: tag <{tag}> dentro de <pre> (código não escapado?)')
        if tag == 'pre':
            self.pre_depth += 1
        if tag in BLOCK_IN_P and any(t == 'p' for t, _ in self.stack):
            self.errors.append(f'l.{line}: <{tag}> dentro de <p> (HTML inválido; o navegador fecha o <p>)')
        if tag == 'section':
            self.cur_section = {'id': a.get('id'), 'line': line, 'text': []}
        if tag == 'table':
            self.cur_table = {'line': line, 'head': 0, 'rows': [], 'in_head': False, 'cells': 0}
        if self.cur_table is not None:
            if tag == 'thead':
                self.cur_table['in_head'] = True
            elif tag == 'tr':
                self.cur_table['cells'] = 0
            elif tag in ('td', 'th'):
                self.cur_table['cells'] += int(a.get('colspan', 1))
        if tag == 'aside' and 'complemento' in (a.get('class') or '').split():
            self.complement_pending = line
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'l.{line}: </{tag}> sem abertura')
            return
        if self.stack[-1][0] != tag:
            abertos = [t for t, _ in self.stack]
            if tag in abertos:
                while self.stack and self.stack[-1][0] != tag:
                    t, l0 = self.stack.pop()
                    self.errors.append(f'l.{l0}: <{t}> não fechado antes de </{tag}> (l.{line})')
                self.stack.pop()
            else:
                self.errors.append(f'l.{line}: </{tag}> sem abertura correspondente (topo: <{self.stack[-1][0]}> l.{self.stack[-1][1]})')
            return
        self.stack.pop()
        if tag == 'pre':
            self.pre_depth -= 1
        if tag == 'section' and self.cur_section:
            self.sections.append(self.cur_section)
            self.cur_section = None
        if self.cur_table is not None:
            t = self.cur_table
            if tag == 'tr':
                if t['in_head']:
                    t['head'] = t['cells']
                else:
                    t['rows'].append((line, t['cells']))
            elif tag == 'thead':
                t['in_head'] = False
            elif tag == 'table':
                for l, n in t['rows']:
                    if t['head'] and n != t['head']:
                        self.warns.append(f'l.{l}: linha de tabela com {n} células; cabeçalho tem {t["head"]} (tabela l.{t["line"]})')
                self.cur_table = None

    def handle_data(self, data):
        self.text_parts.append(data)
        if self.cur_section is not None:
            self.cur_section['text'].append(data)
        if self.complement_pending is not None and data.strip():
            if not data.strip().startswith('📘 Complemento'):
                self.warns.append(f'l.{self.complement_pending}: aside.complemento sem rótulo inicial "📘 Complemento"')
            self.complement_pending = None


def check_html(path, base_dir=None, fragment=False):
    errs, warns, info = [], [], []
    base_dir = base_dir or path.parent
    raw = path.read_bytes()
    try:
        txt = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        return [f'arquivo não é UTF-8 válido: {e}'], [], []
    if fragment:
        if not txt.lstrip().startswith('<section id="'):
            errs.append('fragmento deve começar com <section id="...">')
    elif not txt.lstrip().lower().startswith('<!doctype html>'):
        errs.append('falta <!doctype html>')
    p = Parser()
    p.feed(txt)
    p.close()
    errs += p.errors
    warns += p.warns
    for t, l in p.stack:
        errs.append(f'l.{l}: <{t}> nunca fechado')
    if not fragment and not p.has_charset:
        errs.append('falta <meta charset="UTF-8">')
    if not fragment and not p.lang_ok:
        errs.append('falta lang="pt-BR" em <html>')
    for l, what in p.external:
        errs.append(f'l.{l}: recurso externo/ativo não permitido: {what}')
    if re.search(r'@import|url\(\s*["\']?https?:', txt):
        errs.append('CSS com recurso externo (@import/url http)')
    visible = ' '.join(p.text_parts)
    for m in MOJIBAKE.finditer(visible):
        errs.append(f'possível mojibake: {visible[max(0, m.start()-25):m.end()+25]!r}')
    for m in PROIBIDOS.finditer(visible):
        errs.append(f'termo proibido/placeholder: {visible[max(0, m.start()-30):m.end()+30]!r}')
    for m in PROIBIDOS.finditer(txt):
        if 'PDF exclusivo' in m.group(0) or '@gmail' in m.group(0):
            errs.append('dado pessoal/marca d\'água no HTML')
    for s in p.sections:
        body = re.sub(r'\s+', ' ', ' '.join(s['text'])).strip()
        if len(body) < 60:
            errs.append(f'l.{s["line"]}: seção "{s["id"]}" praticamente vazia ({len(body)} caracteres)')
    for m in ID_RE.finditer(visible):
        if m.group(1) not in README_REQ:
            errs.append(f'ID citado não existe no README: {m.group(1)}')
    cited = sorted(set(ID_RE.findall(visible)))
    info.append(f'IDs citados: {len(cited)}')
    ext_links = 0
    for l, href in p.hrefs:
        if href.startswith(('http:', 'https:', 'mailto:')):
            ext_links += 1
            continue
        if href.startswith('#'):
            if href[1:] not in p.ids:
                (warns if fragment else errs).append(f'l.{l}: âncora interna inexistente {href}' + (' (pode estar em outro fragmento; conferir após montar)' if fragment else ''))
            continue
        parts = urlsplit(href)
        target = (base_dir / unquote(parts.path)).resolve()
        if not target.exists():
            errs.append(f'l.{l}: link para arquivo inexistente {href}')
            continue
        frag = unquote(parts.fragment)
        if target == README.resolve() and frag and frag not in README_IDS:
            errs.append(f'l.{l}: âncora inexistente no README #{frag}')
        if target.suffix.lower() == '.pdf' and frag.startswith('page='):
            n = int(re.sub(r'\D', '', frag) or 0)
            total = PAGES.get(unicodedata.normalize('NFC', target.name))
            if total and not (1 <= n <= total):
                errs.append(f'l.{l}: #page={n} fora do PDF ({total} p.) {target.name}')
    info.append(f'links externos: {ext_links}')
    for l, src in p.srcs:
        if not src.startswith('data:'):
            target = (base_dir / unquote(src)).resolve()
            if not target.exists():
                errs.append(f'l.{l}: imagem inexistente {src}')
    toc = re.search(r'<nav class="toc".*?</nav>', txt, re.S)
    if fragment:
        pass
    elif toc:
        toc_ids = re.findall(r'href="#([^"]+)"', toc.group(0))
        sec_ids = [s['id'] for s in p.sections if s['id']]
        if toc_ids != sec_ids:
            warns.append(f'sumário ({len(toc_ids)}) difere das seções ({len(sec_ids)})')
    else:
        errs.append('sem sumário navegável (nav.toc)')
    if not fragment and 'id="conexao"' not in txt:
        errs.append('sem seção "Conexão com o Tech Challenge Fase 4" (id=conexao)')
    for m in re.finditer(r'\bp\.\s*(\d+)', visible):
        pass
    info.append(f'{len(raw)//1024} KB · {len(p.sections)} seções · {txt.count("class=\"complemento\"")} complementos · {txt.count("<pre>")} blocos de código')
    return errs, warns, info


def check_readme():
    errs, warns = [], []
    for m in re.finditer(r'\]\(([^)]+)\)', readme_txt):
        href = m.group(1)
        if href.startswith(('http:', 'https:', '#')):
            if href.startswith('#') and href[1:] not in README_IDS and not re.match(r'#\d', href):
                warns.append(f'âncora Markdown {href} (verificar slug gerado)')
            continue
        target = (README.parent / unquote(urlsplit(href).path)).resolve()
        if not target.exists():
            errs.append(f'link inexistente {href}')
    obr = sorted(set(re.findall(r'REQ-OBR-\d{2}', readme_txt)))
    bon = sorted(set(re.findall(r'REQ-BON-\d{2}', readme_txt)))
    sug = sorted(set(re.findall(r'SUG-\d{2}', readme_txt)))
    return errs, warns, [f'REQ-OBR={len(obr)} REQ-BON={len(bon)} SUG={len(sug)} âncoras={len(README_IDS)}']


def main(args):
    base_dir, fragment = None, False
    if args[:1] == ['--fragmento']:
        if len(args) < 3:
            raise SystemExit('uso: --fragmento "<pasta do módulo em docs/aulas-fiap>" arquivo.html ...')
        base_dir, fragment, args = (R / 'docs/aulas-fiap' / args[1]).resolve(), True, args[2:]
        if not base_dir.is_dir():
            raise SystemExit(f'pasta de módulo inexistente: {base_dir}')
    files = [Path(a).resolve() for a in args] or sorted((R / 'docs/aulas-fiap').glob('*/GUIA-ESTUDO-*.html'))
    total_err = 0
    for f in files:
        e, w, i = check_html(f, base_dir, fragment)
        total_err += len(e)
        print(f'\n=== {f.relative_to(R) if f.is_relative_to(R) else f}')
        for x in i:
            print('  info:', x)
        for x in e:
            print('  ERRO:', x)
        for x in w:
            print('  aviso:', x)
    if not args and not fragment:
        e, w, i = check_readme()
        total_err += len(e)
        print('\n=== docs/requisitos/README.md')
        for x in i:
            print('  info:', x)
        for x in e:
            print('  ERRO:', x)
        for x in w:
            print('  aviso:', x)
    print(f'\nTotal de erros: {total_err}')
    return 1 if total_err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
