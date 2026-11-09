from pathlib import Path
import json,re,unicodedata
from urllib.parse import unquote,urlsplit

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
files=[ROOT/f for f in ['README.md','SECURITY.md','terraform/README.md','gitops/README.md','gitops/SECRETS-CONTRATO.md','observability/README.md','docs/ARQUITETURA.md','docs/GUIA_DE_REPRODUCAO.md','docs/RELATORIO_DE_ENTREGA.md','docs/requisitos/README.md']]
files+=list(OUT.glob('*.md'))
cache={}
def anchors(p):
    if p in cache:return cache[p]
    text=p.read_text(encoding='utf-8-sig')
    ids=set(re.findall(r'\bid=["\']([^"\']+)',text))
    counts={}
    for m in re.finditer(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
        s=re.sub(r'<[^>]+>','',m[1]).lower()
        s=''.join(c for c in s if c.isalnum() or c in '_- ')
        s=s.replace(' ','-');num=counts.get(s,0);counts[s]=num+1
        ids.add(s+(f'-{num}' if num else ''))
    cache[p]=ids;return ids
checks=[]
for p in files:
    text=p.read_text(encoding='utf-8-sig')
    # Keep line numbers while excluding fenced examples.
    text=re.sub(r'```[\s\S]*?```',lambda m:'\n'*m[0].count('\n'),text)
    for m in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)',text):
        href=m[1].strip('<>');u=urlsplit(href)
        if u.scheme or href.startswith('//'):continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        result='ok'
        if not target.exists():result='arquivo inexistente'
        elif u.fragment and target.suffix.lower() in ['.md','.html'] and unquote(u.fragment) not in anchors(target):result='ancora inexistente'
        checks.append({'source':p.relative_to(ROOT).as_posix(),'line':text.count('\n',0,m.start())+1,'href':href,'result':result})
(OUT/'validacoes/links.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('local_links',len(checks))
for c in checks:
    if c['result']!='ok':print(c)
