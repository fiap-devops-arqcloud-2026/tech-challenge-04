"""Fechamento C: preenche a coluna "Módulo(s) relacionado(s)" do README e o índice da §11.

O mapeamento não é inventado: para cada requisito, lista os módulos cujo guia o cita na seção
"Conexão com o Tech Challenge Fase 4". Requisitos que nenhum guia sustenta recebem a origem
documental correspondente (base das fases anteriores ou entrega), conforme o enunciado.

Uso: python -X utf8 mapear-modulos-readme-2026-09-20_v01.py [--conferir]
--conferir apenas relata o que faria. Depois de rodar, regere o espelho HTML.
Autor: Claude (Opus 5), 2026-09-20.
"""
from pathlib import Path
from fontes_fase4 import guias_fase4
import re
import sys

R = Path(__file__).resolve().parents[2]
README = R / 'docs/requisitos/README.md'
GUIAS = guias_fase4()

# Requisitos herdados das fases anteriores ou puramente de entrega: nenhum módulo da Fase 4 os ensina.
FORA_DOS_MODULOS = {
    'REQ-OBR-01': 'Fases 1–3 (base anterior)', 'REQ-OBR-02': 'Fases 1–3 (base anterior)',
    'REQ-OBR-03': 'Fases 1–3 (base anterior)', 'REQ-OBR-04': 'Fases 1–3 (base anterior)',
    'REQ-OBR-24': 'Entrega (transversal)', 'REQ-OBR-32': 'Entrega (transversal)',
    # EKS e ArgoCD vêm da base anterior: nenhum módulo da Fase 4 os ensina.
    'REQ-OBR-25': 'Fases 1–3 (base anterior)',
    'REQ-OBR-33': 'Entrega (transversal)', 'REQ-OBR-34': 'Entrega (transversal)',
    'REQ-OBR-41': 'Entrega (transversal)', 'REQ-OBR-42': 'Entrega (transversal)',
}

TITULOS = {
    '00.Welcome to Observabilidade e Monitoramento': '00 — Welcome',
    '01.Observabilidade e Monitoramento': '01 — Observabilidade e Monitoramento',
    '02.Monitoramento Opensource': '02 — Monitoramento Opensource',
    '03.APM': '03 — APM',
    '04.Automação de incidentes': '04 — Automação de incidentes',
}

cobertura = {}
indice = []
for g in GUIAS:
    txt = g.read_text(encoding='utf8')
    pasta = g.parent.name
    conexao = re.search(r'<section id="conexao">.*?</section>', txt, re.S)
    ids = sorted(set(re.findall(r'\b(?:REQ-OBR|REQ-BON|SUG)-\d{2}\b', conexao.group(0)))) if conexao else []
    for i in ids:
        cobertura.setdefault(i, []).append(pasta)
    indice.append((pasta, g.name, len(ids)))
    print(f'{pasta}: {len(ids)} IDs na seção de conexão')

s = README.read_text(encoding='utf8')
faltando, preenchidos = [], 0
for linha in re.findall(r'^\|\s*<a id="[^"]+"></a>(REQ-(?:OBR|BON)-\d{2}).*$', s, re.M):
    pass
for m in list(re.finditer(r'^(\|\s*<a id="[^"]+"></a>(REQ-(?:OBR|BON)-\d{2}).*?\|)\s*a mapear\s*\|', s, re.M)):
    ident = m.group(2)
    mods = cobertura.get(ident)
    if mods:
        valor = '; '.join(TITULOS.get(x, x) for x in mods)
    elif ident in FORA_DOS_MODULOS:
        valor = FORA_DOS_MODULOS[ident]
    else:
        valor = None
        faltando.append(ident)
    if valor:
        s = s.replace(m.group(0), f'{m.group(1)} {valor} |', 1)
        preenchidos += 1

print(f'\npreenchidos: {preenchidos} | sem cobertura em nenhum guia: {faltando or "nenhum"}')
if faltando:
    print('Resolva antes de fechar: ou o guia do módulo deve citar o requisito, ou ele pertence a FORA_DOS_MODULOS.')

links = '; '.join(f'[{TITULOS.get(p, p)}](../aulas-fiap/{p.replace(" ", "%20")}/{n})' for p, n, _ in indice)
novo_indice = f'Guias de estudo dos cinco módulos, gerados a partir dos PDFs das aulas e ligados a estes requisitos pelos selos: {links}.'
s = re.sub(r'A Fase A foi concluída antes da autoria dos guias\. Este índice será preenchido no fechamento da Fase B\.', novo_indice, s)

if '--conferir' in sys.argv:
    print('\n[conferência] nada gravado')
else:
    README.write_text(s, encoding='utf8')
    print('\nREADME atualizado; regere o espelho com gerar-espelho-requisitos-2026-09-20_v01.py')
