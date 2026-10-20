from pathlib import Path
W=Path(__file__).parent;R=W.parents[1]
A=R/'00_COLAB_IA/_ARQUIVO_MORTO/2026-10-20_ferramentas-guias';A.mkdir(parents=True,exist_ok=True)
changes={
'validar-guias-2026-09-16_v01.py':("from pathlib import Path","from pathlib import Path\nfrom fontes_fase4 import guias_fase4", "sorted((R / 'docs/aulas-fiap').glob('*/GUIA-ESTUDO-*.html'))",'guias_fase4()'),
'mapear-modulos-readme-2026-09-20_v01.py':("from pathlib import Path","from pathlib import Path\nfrom fontes_fase4 import guias_fase4", "sorted((R / 'docs/aulas-fiap').glob('*/GUIA-ESTUDO-*.html'))",'guias_fase4()'),
'extrair-fontes-2026-09-16_v01.py':("from pathlib import Path","from pathlib import Path\nfrom fontes_fase4 import pastas_fase4", "sorted((ROOT / 'docs/aulas-fiap').rglob('*.pdf'))", "sorted(p for folder in pastas_fase4() for p in folder.glob('*.pdf'))"),
}
for name,(a,b,c,d) in changes.items():
    p=W/name;t=p.read_text(encoding='utf8');assert t.count(a)==1 and t.count(c)==1
    old=A/name;assert not old.exists();p.rename(old)
    p.write_text(t.replace(a,b).replace(c,d),encoding='utf8')
print('Seleção de guias/mapeamento/extração limitada às cinco pastas da Fase 4; versões anteriores preservadas.')
