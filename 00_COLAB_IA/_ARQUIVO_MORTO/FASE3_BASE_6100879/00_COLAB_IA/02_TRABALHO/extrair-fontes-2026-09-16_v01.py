from pathlib import Path
import json, hashlib, re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).parent
OUT = WORK / 'extracoes'
OUT.mkdir(exist_ok=True)
files = [ROOT / 'POSTECH - Tech Challenge - Fase 4.pdf'] + sorted((ROOT / 'docs/aulas-fiap').rglob('*.pdf'))
inventory=[]
for index, source in enumerate(files):
    reader=PdfReader(source)
    pages=[]
    for n,p in enumerate(reader.pages,1):
        t=p.extract_text(extraction_mode='layout') or ''
        pages.append({'page':n,'text':t,'images':len(p.images)})
    key=f'{index:02d}-'+source.stem
    (OUT/(key+'.txt')).write_text('\n\n'.join(f'===== PÁGINA {p["page"]} =====\n{p["text"]}' for p in pages),encoding='utf-8')
    (OUT/(key+'.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
    inventory.append({'id':index,'source':source.relative_to(ROOT).as_posix(),'pages':len(pages),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'extraction':(OUT/(key+'.txt')).relative_to(ROOT).as_posix(),'sparse_pages':[p['page'] for p in pages if len(p['text'].strip())<100], 'image_pages':[p['page'] for p in pages if p['images']]})
(WORK/'inventario-fontes-2026-09-16_v01.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
for f in inventory: print(f'{f["id"]:02d} | {f["pages"]:3d} p | {f["source"]} | pouca extração: {f["sparse_pages"]}')
