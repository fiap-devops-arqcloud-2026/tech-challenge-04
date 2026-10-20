from pathlib import Path
import json
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
W=Path(__file__).parent; R=W.parents[1]; out=W/'qa-fundamentos';out.mkdir(exist_ok=True)
inv=json.loads((W/'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))
selection={1:[1,2,3,4],2:[7,10,11,12],3:[5,9,10,11,12],4:[6,7],5:[10]}
for fileid,nums in selection.items():
    f=inv[fileid];doc=pdfium.PdfDocument(R/f['source'])
    for n in nums:
        pg=doc[n-1];bm=pg.render(scale=2);im=bm.to_pil().copy();im.save(out/f'{fileid:02}-p{n:02}.png');bm.close();pg.close()
    for k in range(0,len(nums),4):
        group=nums[k:k+4];sheet=Image.new('RGB',(1600,1160*((len(group)+1)//2)),'#dde5ee');d=ImageDraw.Draw(sheet)
        for j,n in enumerate(group):
            im=Image.open(out/f'{fileid:02}-p{n:02}.png');im.thumbnail((800,1125));x=(j%2)*800;y=(j//2)*1160
            sheet.paste(im,(x,y+25));d.text((x+10,y+5),f'Fonte {fileid:02} / pagina {n}',fill='black')
        sheet.save(out/f'contato-{fileid:02}-{k//4}.png')
    doc.close()
print(out)
