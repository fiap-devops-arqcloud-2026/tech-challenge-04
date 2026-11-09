from pathlib import Path
import pypdfium2 as pdfium
import json, re
R=Path(__file__).resolve().parents[2]; W=Path(__file__).parent
out=W/'extracoes-pdfium'; out.mkdir(exist_ok=True)
inv=json.loads((W/'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))
for f in inv:
    doc=pdfium.PdfDocument(R/f['source']); pages=[]
    for i in range(len(doc)):
        pg=doc[i]; tp=pg.get_textpage(); txt=tp.get_text_range().replace('\r\r\n','\n').replace('\r\n','\n').replace('\r','\n')
        # Omitir marcas pessoais dos extratos de trabalho; o original permanece intacto.
        txt='\n'.join(l for l in txt.splitlines() if 'PDF exclusivo para' not in l and '@gmail.com' not in l)
        pages.append({'page':i+1,'text':txt}); tp.close(); pg.close()
    doc.close()
    key=Path(f['extraction']).stem
    (out/(key+'.txt')).write_text('\n\n'.join(f'===== PÁGINA {p["page"]} =====\n{p["text"]}' for p in pages),encoding='utf8')
    (out/(key+'.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{f["id"]:02}: {len(pages)} páginas; {sum(len(p["text"]) for p in pages)} caracteres')
