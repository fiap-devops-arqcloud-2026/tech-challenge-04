"""Seleciona somente os materiais da Fase 4, mesmo com a Fase 3 importada.

O inventário preservado identifica os 31 PDFs e cinco módulos originais do 04.
Não usar um glob geral de aulas-fiap: ele também encontra o acervo histórico.
"""
from pathlib import Path
import json

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[1]

def inventario_fase4():
    return json.loads((WORK / 'inventario-fontes-2026-09-16_v01.json').read_text(encoding='utf8'))

def pastas_fase4():
    return sorted({ROOT / Path(item['source']).parent for item in inventario_fase4()
                   if item['source'].startswith('docs/aulas-fiap/')})

def guias_fase4():
    return sorted(path for folder in pastas_fase4() for path in folder.glob('GUIA-ESTUDO-*.html'))
