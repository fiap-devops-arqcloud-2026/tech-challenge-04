"""Gera o relatório de entrega da Fase 4 (PDF, A4 paisagem).

Fluxo: dados em docs/relatorio/dados-entrega.json + prints em docs/evidencias/2026-11-09
-> HTML com layout de impressão -> PDF pelo Microsoft Edge em modo headless.
Os prints são recortados (nunca editados) para ampliar a região que comprova cada item.

Uso, na raiz do repositório:
    py -3.14 -B 00_COLAB_IA/02_TRABALHO/entrega-relatorio-2026-11-11_v03/build_relatorio.py
Opcional: --html <arquivo> grava também o HTML intermediário.
"""
import html
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DADOS = json.loads((RAIZ / "docs/relatorio/dados-entrega.json").read_text(encoding="utf-8-sig"))
EVID = RAIZ / "docs/evidencias/2026-11-09"
SAIDA = RAIZ / "docs/relatorio/RELATORIO_ENTREGA_2026-11-11_v03.pdf"
EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
REPO = DADOS["repositorio"]
RUN_GRAVACAO = DADOS["execucao_gravacao"]
RUN_ENSAIO = DADOS["execucao_ensaio"]

e = html.escape

# ---------------------------------------------------------------- recortes dos prints
# (arquivo, caixa x0, y0, x1, y1 em pixels do original; None = imagem inteira)
RECORTES = {
    "grafana-metricas": ("01-grafana-requisicoes.png", (318, 0, 1879, 878)),
    "grafana-logs": ("01-grafana-recursos-logs.png", (318, 0, 1879, 878)),
    "trace-spans": ("02-trace-spans.png", (265, 0, 1495, 718)),
    "trace-mapa": ("02-trace-mapa.png", (265, 0, 1495, 718)),
    "chatops": ("03-chatops.png", (412, 40, 1110, 500)),
    "sh-log": ("04-self-healing-log.png", (340, 0, 1150, 569)),
    "sh-resumo": ("04-self-healing.png", (0, 100, 1160, 480)),
    "firing": ("07-grafana-firing.png", (330, 75, 1490, 860)),
    "pagerduty": ("08-pagerduty.png", (318, 62, 1360, 712)),
    "argocd": ("05-argocd.png", None),
    "lens": ("06-lens-nos.png", (600, 50, 1536, 250)),
}


def preparar_imagens(destino):
    caminhos = {}
    for chave, (arquivo, caixa) in RECORTES.items():
        im = Image.open(EVID / arquivo).convert("RGB")
        if caixa:
            im = im.crop(caixa)
        alvo = destino / f"{chave}.png"
        im.save(alvo)
        caminhos[chave] = (alvo.as_uri(), im.width / im.height)
    return caminhos


# ---------------------------------------------------------------- participantes
def participantes():
    linhas = []
    for item in DADOS["participantes"].split(";"):
        nome, rm, usuario = [p.strip() for p in item.split(" - ")]
        linhas.append((nome, rm, usuario))
    return linhas


CSS = r"""
@page { size: A4 landscape; margin: 0; }
:root {
  --navy:#0B172A; --ink:#162D45; --muted:#50647C; --teal:#007F83; --teal-d:#00666A;
  --tint:#E3F3F2; --mint:#BFF5E2; --amber:#F8BE57; --amber-t:#FEF3DD; --line:#D7E1EA;
  --paper:#F6F8FB; --red:#B42318; --green:#15803D;
}
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; }
body { font-family: Calibri, "Segoe UI", Arial, sans-serif; color: var(--ink); font-size: 10.5pt; line-height: 1.38; }
.page { width: 297mm; height: 209.6mm; padding: 13mm 16mm 11mm; position: relative; overflow: hidden;
        page-break-after: always; break-after: page; background: #fff; }
.page:last-child { page-break-after: auto; break-after: auto; }
h1, h2, h3 { font-family: Cambria, Georgia, serif; color: var(--navy); margin: 0; }
p { margin: 0 0 2.2mm; }
a { color: var(--teal-d); text-decoration: none; }
.mono { font-family: "Cascadia Mono", Consolas, "Courier New", monospace; font-size: .88em; }
.chain { display: flex; align-items: center; gap: 2mm; margin-top: 6mm; }
.chain .st { flex: 1; background: var(--paper); border-radius: 2.4mm; padding: 2.6mm 2.4mm; text-align: center; }
.chain .st b { display: block; color: var(--navy); font-size: 9.6pt; }
.chain .st span { color: var(--muted); font-size: 8.2pt; }
.chain .ar { color: var(--teal); font-weight: 700; font-size: 13pt; }
.chain .st.bad { background: #FDECEA; } .chain .st.good { background: #E8F5EC; }

/* cabeçalho e rodapé das páginas de conteúdo */
.ph { display: flex; justify-content: space-between; align-items: flex-start; gap: 8mm; margin-bottom: 5mm; }
.kicker { font-size: 8.5pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--teal); margin-bottom: 1.2mm; }
.ph h1 { font-size: 21pt; line-height: 1.12; }
.lead { font-size: 11pt; color: var(--muted); margin-top: 1.6mm; max-width: 200mm; }
.tag { white-space: nowrap; font-size: 8.5pt; font-weight: 700; padding: 1.4mm 3.2mm; border-radius: 10mm; margin-top: 1mm; }
.tag.req { background: var(--amber); color: var(--navy); }
.tag.apoio { background: var(--mint); color: var(--navy); }
.tag.info { background: var(--tint); color: var(--teal-d); }
.pf { position: absolute; left: 16mm; right: 16mm; bottom: 6mm; display: flex; justify-content: space-between;
      font-size: 8pt; color: var(--muted); }
.pf b { color: var(--teal); font-size: 9pt; }

/* capa */
.cover { background: var(--navy); color: #fff; padding: 15mm 17mm; }
.cover .top { font-size: 9pt; letter-spacing: .16em; text-transform: uppercase; color: var(--mint); font-weight: 700; }
.cover h1 { color: #fff; font-size: 44pt; margin-top: 7mm; letter-spacing: -.01em; }
.cover h2 { color: var(--mint); font-family: Calibri, "Segoe UI", sans-serif; font-weight: 400; font-size: 17pt; margin-top: 1.5mm; }
.cover .grid { display: grid; grid-template-columns: 1.25fr 1fr; gap: 9mm; margin-top: 10mm; }
.cover .card { background: var(--ink); border-radius: 3.5mm; padding: 5.5mm 6.5mm; }
.cover .card h3 { color: var(--mint); font-family: Calibri, sans-serif; font-size: 9pt; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 3mm; }
.cover table { width: 100%; border-collapse: collapse; font-size: 10.5pt; }
.cover td { padding: 1.5mm 0; border-bottom: 1px solid rgba(191,245,226,.14); vertical-align: top; }
.cover tr:last-child td { border-bottom: 0; }
.cover td.rm { color: var(--mint); width: 25mm; font-variant-numeric: tabular-nums; }
.cover td.user { color: #C9D6E3; width: 38mm; }
.cover .link { margin-bottom: 3.2mm; }
.cover .link .rot { font-size: 8.5pt; color: var(--mint); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.cover .link a, .cover .link span.v { color: #fff; font-size: 10.5pt; word-break: break-all; }
.cover .pend { display: inline-block; background: var(--amber); color: var(--navy); font-weight: 700; padding: .6mm 2.4mm; border-radius: 2mm; }
.cover .kpis { position: absolute; left: 17mm; right: 17mm; bottom: 15mm; display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; }
.cover .kpi .n { font-family: Cambria, Georgia, serif; font-size: 25pt; font-weight: 700; color: #fff; line-height: 1; }
.cover .kpi .t { color: var(--mint); font-size: 10pt; margin-top: 1.6mm; }
.cover .ed { position: absolute; left: 17mm; bottom: 6.5mm; font-size: 8.5pt; color: #8FA3B8; }

/* caixas genéricas */
.cols { display: grid; gap: 7mm; }
.card { background: var(--paper); border-radius: 3mm; padding: 4.5mm 5mm; }
.card h3 { font-size: 12.5pt; margin-bottom: 2mm; }
.card.tint { background: var(--tint); }
.card.amber { background: var(--amber-t); }
ul.clean { margin: 0; padding-left: 4.5mm; }
ul.clean li { margin-bottom: 1.4mm; }
.num { display: inline-flex; align-items: center; justify-content: center; width: 6.2mm; height: 6.2mm; border-radius: 50%;
       background: var(--teal); color: #fff; font-weight: 700; font-size: 9pt; margin-right: 2mm; flex: none; }

/* tabela de verificação */
table.check { width: 100%; border-collapse: collapse; font-size: 10pt; }
table.check th { text-align: left; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--muted);
                 border-bottom: 1.5px solid var(--navy); padding: 1.6mm 2mm; }
table.check td { border-bottom: 1px solid var(--line); padding: 1.9mm 2mm; vertical-align: top; }
table.check td.pg { text-align: right; font-weight: 700; color: var(--teal); white-space: nowrap; }
.ok { color: var(--green); font-weight: 700; }

/* prints */
.shot { border-radius: 2.6mm; overflow: hidden; border: 1px solid #1F2937; background: #111827;
        box-shadow: 0 1.6mm 4.5mm rgba(11,23,42,.22); }
.shot .bar { height: 6.4mm; background: #1F2937; display: flex; align-items: center; gap: 1.6mm; padding: 0 3mm; }
.shot .bar i { width: 2.2mm; height: 2.2mm; border-radius: 50%; background: #4B5563; display: inline-block; }
.shot .bar i:nth-child(1) { background: #F87171; } .shot .bar i:nth-child(2) { background: #FBBF24; } .shot .bar i:nth-child(3) { background: #34D399; }
.shot .bar span { color: #D1D5DB; font-size: 8pt; margin-left: 2.5mm; }
.shot img { display: block; width: 100%; height: auto; }
.facts { font-size: 9.6pt; }
.facts .lbl { font-size: 8pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--teal); margin: 0 0 1.2mm; }
.chips { display: flex; flex-wrap: wrap; gap: 1.6mm; margin-bottom: 2.6mm; }
.chip { background: var(--tint); color: var(--teal-d); border-radius: 2mm; padding: .7mm 2.2mm; font-size: 8.4pt; font-weight: 700; }
.chip.g { background: #E8F5EC; color: var(--green); }
.chip.r { background: #FDECEA; color: var(--red); }
.chip.a { background: var(--amber-t); color: #8A5A00; }
.note { font-size: 8.6pt; color: var(--muted); }

/* linha do tempo */
.kpirow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; margin-bottom: 7mm; }
.kpibox { background: var(--navy); color: #fff; border-radius: 3mm; padding: 4mm 4.5mm; }
.kpibox .n { font-family: Cambria, Georgia, serif; font-size: 22pt; font-weight: 700; line-height: 1; }
.kpibox .t { color: var(--mint); font-size: 9.5pt; margin-top: 1.6mm; }
.tl { position: relative; height: 86mm; margin: 0 8mm; }
.tl .axis { position: absolute; left: 0; right: 0; top: 43mm; height: 1.2mm; background: var(--line); border-radius: 1mm; }
.tl .ev { position: absolute; width: 34mm; transform: translateX(-50%); }
.tl .ev .dot { position: absolute; left: 50%; width: 4.6mm; height: 4.6mm; margin-left: -2.3mm; border-radius: 50%;
               background: #fff; border: 1.2mm solid var(--teal); }
.tl .ev.up { bottom: 43mm; padding-bottom: 6mm; }
.tl .ev.up .dot { bottom: -2.9mm; }
.tl .ev.down { top: 43mm; padding-top: 6mm; }
.tl .ev.down .dot { top: -1.7mm; }
.tl .ev .box { background: var(--paper); border-radius: 2.4mm; padding: 2.4mm 2.8mm; }
.tl .ev .h { font-family: Cambria, Georgia, serif; font-weight: 700; color: var(--teal); font-size: 12pt; }
.tl .ev .ti { font-weight: 700; color: var(--navy); font-size: 9.6pt; line-height: 1.2; margin: .6mm 0; }
.tl .ev .de { font-size: 8.4pt; color: var(--muted); line-height: 1.25; }
.tl .ev .src { display: inline-block; margin-top: 1.2mm; font-size: 7.4pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
               color: var(--teal-d); background: var(--tint); border-radius: 1.5mm; padding: .3mm 1.6mm; }
.tl .ev.bad .dot { border-color: var(--red); }
.tl .ev.bad .h { color: var(--red); }
.tl .ev.good .dot { border-color: var(--green); }
.tl .ev.good .h { color: var(--green); }

/* terminal e mensagens */
.term { background: #0D1117; color: #E6EDF3; border-radius: 2.6mm; padding: 3.4mm 4mm; font-size: 7.9pt; line-height: 1.42;
        font-family: "Cascadia Mono", Consolas, "Courier New", monospace; white-space: pre-wrap; }
.term .t { color: #7D8590; } .term .k { color: #7EE787; } .term .w { color: #F2CC60; }
.msg { border-radius: 2.6mm; background: #1A1D21; color: #D1D2D3; padding: 3mm 3.6mm; margin-bottom: 3mm; font-size: 8.6pt; line-height: 1.38; }
.msg .who { color: #fff; font-weight: 700; } .msg .when { color: #9A9B9E; font-size: 7.8pt; margin-left: 1.6mm; }
.msg .title { color: #4FA3FF; font-weight: 700; margin: .8mm 0; }
.msg.firing { border-left: 0; box-shadow: inset 1.1mm 0 0 #E01E5A; }
.msg.resolved { box-shadow: inset 1.1mm 0 0 #2EB67D; }
.msg.pd { box-shadow: inset 1.1mm 0 0 #06AC38; }

/* matriz */
table.mx { width: 100%; border-collapse: collapse; font-size: 8.7pt; line-height: 1.28; }
table.mx th { text-align: left; font-size: 7.6pt; letter-spacing: .08em; text-transform: uppercase; color: #fff; background: var(--navy);
              padding: 1.7mm 2mm; }
table.mx td { border-bottom: 1px solid var(--line); padding: 1.45mm 2mm; vertical-align: top; }
table.mx tr.grp td { background: var(--tint); color: var(--teal-d); font-weight: 700; font-size: 8pt; letter-spacing: .06em; text-transform: uppercase; padding: 1.2mm 2mm; }
table.mx td.n { color: var(--muted); width: 6mm; }
table.mx td.r { font-weight: 700; color: var(--navy); width: 64mm; }
table.mx td.w { width: 74mm; color: var(--muted); }
.ref { font-size: 9.4pt; }
.ref li { margin-bottom: 1.6mm; }
"""


def pagina(conteudo, n, extra_cls=""):
    rodape = "" if "cover" in extra_cls else (
        f'<div class="pf"><span>ToggleMaster · Tech Challenge Fase 4 · Relatório de entrega</span><b>{n:02d}</b></div>')
    return f'<section class="page {extra_cls}">{conteudo}{rodape}</section>'


def cabecalho(kicker, titulo, lead, tag=None, tag_cls="req"):
    t = f'<span class="tag {tag_cls}">{e(tag)}</span>' if tag else ""
    return (f'<div class="ph"><div><div class="kicker">{e(kicker)}</div><h1>{e(titulo)}</h1>'
            f'<div class="lead">{lead}</div></div>{t}</div>')


def shot(imgs, chave, rotulo, largura_mm):
    uri, _ = imgs[chave]
    return (f'<div class="shot" style="width:{largura_mm}mm"><div class="bar"><i></i><i></i><i></i>'
            f'<span>{e(rotulo)}</span></div><img src="{uri}" alt="{e(rotulo)}"></div>')


def largura_para_altura(imgs, chave, altura_mm):
    _, ar = imgs[chave]
    return round((altura_mm - 6.4) * ar, 1)


# ---------------------------------------------------------------- páginas
ORDEM = ["capa", "sumario", "arquitetura", "justificativa", "linha", "ev1a", "ev1b", "ev2a", "ev2b",
         "ev3", "ev4a", "ev4b", "apoio1", "apoio2", "matriz", "matriz2", "fecho"]
PG = {k: i + 1 for i, k in enumerate(ORDEM)}


def p_capa(imgs):
    linhas = "".join(f'<tr><td>{e(n)}</td><td class="rm">{e(rm)}</td><td class="user">{e(u)}</td></tr>'
                     for n, rm, u in participantes())
    video = DADOS.get("video_url", "").strip()
    video_html = (f'<a href="{e(video)}">{e(video)}</a>' if video
                  else '<span class="pend">a incluir</span> <span class="v">link do vídeo gravado em 2026-11-11</span>')
    c = f"""
    <div class="top">Pós Tech FIAP · Tech Challenge · Fase 4</div>
    <h1>ToggleMaster</h1>
    <h2>Relatório de entrega: observabilidade, resposta a incidentes e self-healing no EKS</h2>
    <div class="grid">
      <div class="card"><h3>Participantes</h3>
        <table><tbody>{linhas}</tbody></table></div>
      <div class="card"><h3>Links da entrega</h3>
        <div class="link"><div class="rot">Repositório</div><a href="{REPO}">{e(REPO.replace('https://', ''))}</a></div>
        <div class="link"><div class="rot">Vídeo de demonstração</div>{video_html}</div>
        <div class="link"><div class="rot">Self-healing executado na gravação</div><a href="{RUN_GRAVACAO['url']}">execução {RUN_GRAVACAO['id']} · GitHub Actions</a></div>
      </div>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="n">5</div><div class="t">microsserviços instrumentados com OpenTelemetry</div></div>
      <div class="kpi"><div class="n">6</div><div class="t">Applications Synced/Healthy no ArgoCD</div></div>
      <div class="kpi"><div class="n">2 min 50 s</div><div class="t">da falha proposital à volta do HTTP 200</div></div>
      <div class="kpi"><div class="n">0</div><div class="t">ações humanas na recuperação</div></div>
    </div>
    <div class="ed">Edição 2026-11-11 · prints do ensaio integrado de 2026-11-09 · execução gravada em 2026-11-11</div>
    """
    return pagina(c, PG["capa"], "cover")


def p_sumario(imgs):
    itens = [
        ("Nomes, RMs e usernames", "capa"),
        ("Links do repositório e do vídeo", "capa"),
        ("Print do dashboard do Grafana", "ev1a"),
        ("Print de um trace distribuído no APM", "ev2a"),
        ("Print da notificação de incidente no ChatOps", "ev3"),
        ("Print do log e da execução do self-healing", "ev4a"),
        ("Justificativa: arquitetura do OTel", "arquitetura"),
        ("Justificativa: Datadog × New Relic e OpsGenie × PagerDuty", "justificativa"),
    ]
    linhas = "".join(f'<tr><td><span class="ok">✓</span>&nbsp; {e(t)}</td><td class="pg">p. {PG[k]}</td></tr>' for t, k in itens)
    c = cabecalho("Sumário da entrega", "O que este relatório comprova",
                  "Cada exigência do relatório (enunciado, p. 6) e onde encontrá-la. A matriz da p. "
                  f"{PG['matriz']} cobre também os requisitos técnicos e o vídeo.") + f"""
    <div class="cols" style="grid-template-columns: 1fr 1.08fr;">
      <div>
        <div class="card" style="margin-bottom:4.5mm"><h3>O desafio</h3>
          <p>O evaluation-service falhou em silêncio: o time levou 6 horas para ser avisado e mais 4 para achar a causa.
          O objetivo da Fase 4 é observabilidade total e resposta ativa: trace para lentidão, logs centralizados para erros,
          plantão acionado e uma tentativa automática de cura.</p></div>
        <div class="card tint" style="margin-bottom:4.5mm"><h3>O que construímos</h3>
          <p>Sobre a base das fases 1 a 3 (cinco microsserviços, Terraform, CI/CD com DevSecOps e EKS com ArgoCD),
          a Fase 4 entrega Prometheus, Loki e Grafana por GitOps, um OpenTelemetry Collector central, APM no New Relic
          e uma cadeia de resposta: alerta no Grafana, incidente no PagerDuty, aviso no Slack e self-healing no GitHub Actions.</p></div>
        <div class="card amber"><h3>A prova</h3>
          <p>Na gravação de 2026-11-11, uma falha proposital no flag-service foi detectada, comunicada e corrigida sem
          intervenção humana em 2 min 50 s (p. {PG['linha']}). Os prints vêm do ensaio integrado de 2026-11-09,
          com a mesma implantação e a mesma configuração.</p></div>
      </div>
      <div>
        <table class="check"><thead><tr><th>Exigência do relatório</th><th style="text-align:right">Onde</th></tr></thead>
        <tbody>{linhas}</tbody></table>
        <p class="note" style="margin-top:3.5mm">Horários em America/Sao_Paulo (UTC-03), salvo quando indicado UTC.
        Os prints não foram editados: só recortados para ampliar a região que comprova cada item.</p>
      </div>
    </div>"""
    return pagina(c, PG["sumario"])


SVG = """
<svg viewBox="0 0 1000 400" width="236mm" xmlns="http://www.w3.org/2000/svg" font-family="Calibri, Segoe UI, sans-serif">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#007F83"/></marker>
    <marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#50647C"/></marker>
  </defs>
  <!-- origens -->
  <rect x="10" y="15" width="215" height="170" rx="12" fill="#F6F8FB" stroke="#D7E1EA"/>
  <text x="26" y="42" font-size="16" font-weight="700" fill="#0B172A">Microsserviços</text>
  <text x="26" y="61" font-size="12" fill="#50647C">SDK OpenTelemetry · logs JSON</text>
  <g font-size="12.5" fill="#00666A" font-weight="700">
    <rect x="26" y="74" width="88" height="26" rx="6" fill="#E3F3F2"/><text x="35" y="92">auth · Go</text>
    <rect x="122" y="74" width="92" height="26" rx="6" fill="#E3F3F2"/><text x="130" y="92">evaluation · Go</text>
    <rect x="26" y="108" width="88" height="26" rx="6" fill="#E3F3F2"/><text x="35" y="126">flag · Py</text>
    <rect x="122" y="108" width="92" height="26" rx="6" fill="#E3F3F2"/><text x="130" y="126">targeting · Py</text>
    <rect x="26" y="142" width="88" height="26" rx="6" fill="#E3F3F2"/><text x="35" y="160">analytics · Py</text>
  </g>
  <rect x="10" y="235" width="215" height="95" rx="12" fill="#F6F8FB" stroke="#D7E1EA"/>
  <text x="26" y="262" font-size="16" font-weight="700" fill="#0B172A">Exporters do cluster</text>
  <text x="26" y="284" font-size="12.5" fill="#50647C">node-exporter</text>
  <text x="26" y="302" font-size="12.5" fill="#50647C">kube-state-metrics</text>
  <text x="26" y="320" font-size="12.5" fill="#50647C">kubelet / cAdvisor</text>
  <!-- agent -->
  <rect x="270" y="215" width="170" height="115" rx="12" fill="#0B172A"/>
  <text x="285" y="242" font-size="16" font-weight="700" fill="#FFFFFF">Collector agent</text>
  <text x="285" y="262" font-size="12.5" fill="#BFF5E2">DaemonSet · 1 por nó (2)</text>
  <text x="285" y="286" font-size="12" fill="#C9D6E3">file_log em /var/log/pods</text>
  <text x="285" y="304" font-size="12" fill="#C9D6E3">→ k8s_attributes → batch</text>
  <!-- gateway -->
  <rect x="470" y="15" width="185" height="315" rx="14" fill="#0B172A"/>
  <text x="486" y="44" font-size="16" font-weight="700" fill="#FFFFFF">Collector gateway</text>
  <text x="486" y="63" font-size="12.5" fill="#BFF5E2">Deployment · peça central</text>
  <g font-size="12" fill="#0B172A">
    <rect x="484" y="76" width="157" height="32" rx="7" fill="#BFF5E2"/><text x="494" y="97" font-weight="700">receiver OTLP</text>
    <rect x="484" y="116" width="157" height="98" rx="7" fill="#E3F3F2"/>
    <text x="494" y="135" font-weight="700">processadores</text>
    <text x="494" y="153">memory_limiter</text><text x="494" y="169">filter/health</text>
    <text x="494" y="185">transform/sanitize</text><text x="494" y="201">k8s_attributes · batch</text>
    <rect x="484" y="222" width="157" height="32" rx="7" fill="#F8BE57"/><text x="494" y="243" font-weight="700">conector spanmetrics</text>
    <rect x="484" y="262" width="157" height="32" rx="7" fill="#BFF5E2"/><text x="494" y="283" font-weight="700">exporters OTLP/HTTP</text>
  </g>
  <text x="486" y="318" font-size="11.5" fill="#8FA3B8">chave do New Relic só aqui</text>
  <!-- destinos -->
  <rect x="705" y="15" width="155" height="75" rx="12" fill="#FEF3DD" stroke="#F8BE57"/>
  <text x="720" y="44" font-size="16" font-weight="700" fill="#0B172A">New Relic</text>
  <text x="720" y="64" font-size="12.5" fill="#50647C">APM · traces · Service Map</text>
  <text x="720" y="80" font-size="11" fill="#8A5A00">SaaS, fora do cluster</text>
  <rect x="705" y="115" width="155" height="75" rx="12" fill="#F6F8FB" stroke="#D7E1EA"/>
  <text x="720" y="144" font-size="16" font-weight="700" fill="#0B172A">Loki</text>
  <text x="720" y="164" font-size="12.5" fill="#50647C">logs de todos os pods</text>
  <rect x="705" y="215" width="155" height="75" rx="12" fill="#F6F8FB" stroke="#D7E1EA"/>
  <text x="720" y="244" font-size="16" font-weight="700" fill="#0B172A">Prometheus</text>
  <text x="720" y="264" font-size="12.5" fill="#50647C">métricas de app e infra</text>
  <rect x="890" y="115" width="100" height="175" rx="12" fill="#007F83"/>
  <text x="904" y="146" font-size="16" font-weight="700" fill="#FFFFFF">Grafana</text>
  <text x="904" y="170" font-size="12" fill="#E3F3F2">dashboard</text>
  <text x="904" y="187" font-size="12" fill="#E3F3F2">ToggleMaster</text>
  <text x="904" y="212" font-size="12" fill="#E3F3F2">regra</text>
  <text x="904" y="229" font-size="12" fill="#E3F3F2">FlagService</text>
  <text x="904" y="246" font-size="12" fill="#E3F3F2">5xxAlto</text>
  <!-- setas -->
  <g stroke="#007F83" stroke-width="2.6" fill="none">
    <path d="M225 92 L466 92" marker-end="url(#a)"/>
    <path d="M150 185 C150 205 355 190 355 211" marker-end="url(#a)"/>
    <path d="M440 272 L466 272" marker-end="url(#a)"/>
    <path d="M655 52 L701 52" marker-end="url(#a)"/>
    <path d="M655 152 L701 152" marker-end="url(#a)"/>
    <path d="M655 238 L701 238" marker-end="url(#a)"/>
    <path d="M860 152 L886 152" marker-end="url(#a)"/>
    <path d="M860 252 L886 252" marker-end="url(#a)"/>
  </g>
  <path d="M225 300 L250 300 L250 368 L782 368 L782 294" stroke="#50647C" stroke-width="2.2" stroke-dasharray="7 5" fill="none" marker-end="url(#b)"/>
  <g font-size="12.5" fill="#00666A" font-weight="700">
    <text x="300" y="84">traces · OTLP</text>
    <text x="150" y="226">logs no stdout</text>
    <text x="662" y="44">traces</text>
    <text x="664" y="144">logs</text>
    <text x="660" y="230">RED</text>
  </g>
  <text x="300" y="389" font-size="12.5" fill="#50647C" font-weight="700">scrape direto: CPU e memória de nós e pods (não passa pelo Collector)</text>
</svg>
"""


def p_arquitetura(imgs):
    c = cabecalho("Justificativa técnica · 1 de 2", "Arquitetura do OpenTelemetry",
                  "O Collector é a peça central: recebe, processa e roteia traces, logs e métricas de aplicação para o backend certo. "
                  "As aplicações não conhecem os destinos.", "Exigência p. 4 e 6", "info") + f"""
    <div style="margin: 0 0 4mm; text-align:center">{SVG}</div>
    <div class="cols" style="grid-template-columns: repeat(3, 1fr); gap: 5.5mm; font-size: 9.7pt;">
      <div class="card"><h3>Agent em cada nó</h3>
        <p>DaemonSet com um pod por nó. Lê os arquivos de log de todos os contêineres em <span class="mono">/var/log/pods</span>,
        acrescenta namespace, pod e deployment, e envia ao gateway por OTLP/gRPC. Os logs entram no Loki sem mudar o código.</p></div>
      <div class="card"><h3>Gateway central</h3>
        <p>Recebe os traces dos SDKs, descarta spans de <span class="mono">/health</span> e mantém só atributos permitidos antes de
        sair do cluster. Exporta traces ao New Relic e logs ao Loki; o <b>spanmetrics</b> gera taxa, erros e latência (RED) para o Prometheus.</p></div>
      <div class="card tint"><h3>Por que este desenho</h3>
        <ul class="clean"><li>Trocar de APM é trocar um exporter, não o código dos cinco serviços.</li>
        <li>A chave do New Relic fica só no gateway.</li>
        <li>CPU e memória já vêm do Prometheus por scrape; o Collector não duplica esse caminho.</li></ul></div>
    </div>"""
    return pagina(c, PG["arquitetura"])


def p_justificativa(imgs):
    def tabela(cab, linhas):
        th = "".join(f"<th>{e(x)}</th>" for x in cab)
        corpo = "".join(f'<tr><td style="width:25%;font-weight:700;color:#0B172A">{a}</td><td style="width:39%">{b}</td><td>{c}</td></tr>'
                        for a, b, c in linhas)
        return f'<table class="check" style="font-size:9.4pt"><thead><tr>{th}</tr></thead><tbody>{corpo}</tbody></table>'
    apm = tabela(["Critério", "New Relic", "Datadog"], [
        ("Plano gratuito", "Permanente: 100 GB/mês e 1 usuário completo, com APM, tracing e Service Map",
         "Gratuito só para infraestrutura; APM no teste de 14 dias ou em plano pago"),
        ("Entrada OpenTelemetry", "Endpoint OTLP nativo: o gateway exporta direto, sem agente proprietário",
         "OTLP pelo Datadog Agent ou por exporter próprio"),
        ("No desafio", "Trace distribuído e mapa de dependências a partir dos spans OTel", "Recursos equivalentes, com custo após o teste"),
    ])
    inc = tabela(["Critério", "PagerDuty", "OpsGenie"], [
        ("Disponibilidade", "Ativo; conta criada para o projeto",
         "Venda encerrada em 2025-06-04, sem contas novas; fim do suporte em 2027-04-05"),
        ("Integração com o Grafana", "Contact point nativo (Events API v2): abre e resolve o incidente sozinho",
         "Também tinha, mas sem conta nova não há como usar"),
        ("ChatOps", "App do PagerDuty no Slack publica o cartão do incidente", "Migração indicada para o Jira Service Management"),
    ])
    c = cabecalho("Justificativa técnica · 2 de 2", "Por que New Relic e PagerDuty",
                  "Os critérios foram custo sem prazo, encaixe com o OpenTelemetry já implantado e disponibilidade do serviço.",
                  "Exigência p. 6", "info") + f"""
    <div class="cols" style="grid-template-columns: 1fr 1fr;">
      <div class="card"><div class="kicker">APM</div><h3 style="font-size:15pt;margin-bottom:3mm">New Relic em vez de Datadog</h3>
        {apm}
        <p style="margin-top:3.5mm"><b>Decisão:</b> New Relic. Custo zero sem prazo de expiração e ingestão OTLP direta do gateway:
        o mesmo dado que alimenta o Prometheus vira trace e Service Map no APM.</p></div>
      <div class="card"><div class="kicker">Gestão de incidentes</div><h3 style="font-size:15pt;margin-bottom:3mm">PagerDuty em vez de OpsGenie</h3>
        {inc}
        <p style="margin-top:3.5mm"><b>Decisão:</b> PagerDuty. O OpsGenie não aceita contas novas desde 2025-06-04. O PagerDuty
        integra nativamente com o Grafana e o Slack, e o incidente fecha sozinho quando o alerta se resolve.</p></div>
    </div>
    <p class="note" style="margin-top:4mm">Fontes, consultadas em 2026-11-11: newrelic.com/pricing; datadoghq.com/pricing;
    atlassian.com/licensing/opsgenie; documentação do Grafana sobre o contact point do PagerDuty. Links na p. {PG['fecho']}.</p>"""
    return pagina(c, PG["justificativa"])


EVENTOS = [
    ("00:58:48", "Falha ativada", "POST /admin/fault autenticado; 1ª resposta 503", "Loki", "bad"),
    ("01:00:50", "Alerta em Firing", "FlagService5xxAlto: 100% de 5xx por mais de 1 min", "Grafana", "bad"),
    ("01:00:53", "Webhook dispara a automação", f"repository_dispatch · execução {RUN_GRAVACAO['id']}", "GitHub", ""),
    ("01:01:00", "Slack recebe o alerta", "mensagem detalhada do Grafana", "Slack", ""),
    ("01:01:04", "PagerDuty abre o incidente", "cartão publicado no mesmo canal", "Slack", ""),
    ("01:01:09", "rollout restart", "lista permitida e cooldown aprovados", "GitHub", ""),
    ("01:01:38", "HTTP 200 de novo", "pod novo, sem a falha em memória", "Loki", "good"),
    ("01:03:00", "Resolved", "alerta normal e incidente resolvido", "Slack", "good"),
]


def p_linha(imgs):
    n = len(EVENTOS)
    evs = ""
    for i, (h, t, d, src, cls) in enumerate(EVENTOS):
        pos = i / (n - 1) * 100
        lado = "up" if i % 2 == 0 else "down"
        evs += (f'<div class="ev {lado} {cls}" style="left:{pos:.2f}%"><div class="dot"></div><div class="box">'
                f'<div class="h">{h}</div><div class="ti">{e(t)}</div><div class="de">{e(d)}</div>'
                f'<span class="src">{e(src)}</span></div></div>')
    c = cabecalho("A prova real · gravação de 2026-11-11", "Da falha à recuperação, sem intervenção humana",
                  "Falha proposital no flag-service, medida nos próprios registros: logs no Loki, log do GitHub Actions e mensagens do Slack.",
                  "Vídeo: incidente e self-healing", "apoio") + f"""
    <div class="kpirow">
      <div class="kpibox"><div class="n">2 min 02 s</div><div class="t">da falha ao Firing (regra: acima de 10% por 1 min)</div></div>
      <div class="kpibox"><div class="n">19 s</div><div class="t">do Firing ao rollout restart</div></div>
      <div class="kpibox"><div class="n">2 min 50 s</div><div class="t">da falha à volta do HTTP 200</div></div>
      <div class="kpibox"><div class="n">159</div><div class="t">respostas 503 vistas pelo gerador de tráfego</div></div>
    </div>
    <div class="tl"><div class="axis"></div>{evs}</div>
    <div class="chain">
      <div class="st bad"><b>Falha</b><span>503 nas rotas de flags</span></div><div class="ar">→</div>
      <div class="st"><b>Métrica</b><span>spanmetrics no Prometheus</span></div><div class="ar">→</div>
      <div class="st"><b>Alerta</b><span>Grafana em Firing</span></div><div class="ar">→</div>
      <div class="st"><b>Incidente</b><span>PagerDuty</span></div><div class="ar">→</div>
      <div class="st"><b>Comunicação</b><span>Slack</span></div><div class="ar">→</div>
      <div class="st"><b>Correção</b><span>GitHub Actions</span></div><div class="ar">→</div>
      <div class="st good"><b>Recuperação</b><span>HTTP 200</span></div>
    </div>
    <p class="note" style="margin-top:4mm">O ensaio de 2026-11-09 percorreu a mesma cadeia: Firing às 15:59:20, restart às 15:59:39,
    HTTP 200 às 16:00:19 e Resolved às 16:01:30 (execução {RUN_ENSAIO['id']}, incidente #4 no PagerDuty).
    O /health seguiu saudável durante a falha: o Kubernetes sozinho não teria reiniciado o pod.</p>"""
    return pagina(c, PG["linha"])


def pagina_print(chave_pg, kicker, titulo, lead, tag, tag_cls, img, rotulo, fatos_html, altura_img=146):
    largura = min(largura_para_altura(IMGS, img, altura_img), 265 - 62)
    c = cabecalho(kicker, titulo, lead, tag, tag_cls) + f"""
    <div style="display:flex; gap:7mm; align-items:flex-start">
      {shot(IMGS, img, rotulo, largura)}
      <div class="facts" style="flex:1">{fatos_html}</div>
    </div>"""
    return pagina(c, PG[chave_pg])


def fatos(chips, itens, nota=""):
    ch = "".join(f'<span class="chip {c}">{e(t)}</span>' for t, c in chips)
    li = "".join(f"<li>{i}</li>" for i in itens)
    n = f'<p class="note" style="margin-top:3mm">{nota}</p>' if nota else ""
    return f'<div class="chips">{ch}</div><div class="lbl">O que o print mostra</div><ul class="clean">{li}</ul>{n}'


def p_ev1a(imgs):
    return pagina_print("ev1a", "Evidência visual obrigatória · 1 de 4", "Dashboard do Grafana: tráfego, erros e latência",
                        "Dashboard customizado ToggleMaster - Visao geral, versionado no GitOps.", "Print exigido", "req",
                        "grafana-metricas", "Grafana · ToggleMaster - Visao geral · últimos 30 min",
                        fatos([("2026-11-09 · ensaio", ""), ("Grafana 13.3", ""), ("dados reais", "g")], [
                            "<b>Erros 5xx agora</b> do flag-service: 0% antes da falha.",
                            "<b>Taxa de erro (5xx)</b> e <b>requisições por segundo</b> de cada serviço HTTP.",
                            "<b>Latência p95</b>: 95% das requisições abaixo de 25 ms.",
                            "<b>CPU e memória</b> de cada nó do EKS.",
                        ], "As métricas de requisição vêm dos traces (spanmetrics); as de nó, do Prometheus por scrape. "
                           "O eixo do painel de erros foi limitado a 100% no repositório depois desta captura."))


def p_ev1b(imgs):
    return pagina_print("ev1b", "Evidência visual obrigatória · 1 de 4", "Dashboard do Grafana: recursos e logs em tempo real",
                        "Continuação do mesmo dashboard: consumo por pod e o painel de logs do Loki.", "Print exigido", "req",
                        "grafana-logs", "Grafana · ToggleMaster - Visao geral · recursos e logs",
                        fatos([("2026-11-09 · ensaio", ""), ("Loki", ""), ("JSON com trace_id", "g")], [
                            "<b>CPU e memória por pod</b> do namespace togglemaster.",
                            "<b>Logs da aplicação</b>, consultados no Loki em tempo real.",
                            "Cada log traz <span class='mono'>service.name</span> e <span class='mono'>trace_id</span>: o evento leva direto ao trace no APM.",
                        ], "Os logs chegam pelos agents do Collector, sem alteração no código de log das aplicações."))


def p_ev2a(imgs):
    return pagina_print("ev2a", "Evidência visual obrigatória · 2 de 4", "Trace distribuído no New Relic",
                        "Uma requisição ao evaluation-service e o caminho que ela percorre pelos serviços e bancos.", "Print exigido", "req",
                        "trace-spans", "New Relic · Distributed tracing · GET /evaluate",
                        fatos([("2026-11-09 18:28 UTC", ""), ("19 spans", "g"), ("0 erros", "g"), ("56,63 ms", "")], [
                            "Entrada em <b>GET /evaluate</b> no evaluation-service.",
                            "Consulta ao <b>Redis</b> (1,01 ms) e chamada ao flag-service <b>GET /flags/&lt;name&gt;</b>.",
                            "O flag-service valida a chave no auth-service (<b>GET /validate</b>), que consulta o <b>PostgreSQL</b>.",
                            "Duração de cada span na direita: localiza a operação mais lenta.",
                        ], "Trace 2ad625552c9917f6aa53c27567f49835, com as operações expandidas."))


def p_ev2b(imgs):
    return pagina_print("ev2b", "Evidência visual obrigatória · 2 de 4", "O mesmo trace no mapa de entidades",
                        "Dez entidades na mesma execução: os serviços e as dependências de dados.", "Print exigido", "req",
                        "trace-mapa", "New Relic · Entity map do trace",
                        fatos([("10 entidades", "g"), ("SQS → analytics", ""), ("DynamoDB", "")], [
                            "evaluation-service no centro, com Redis e três bancos PostgreSQL.",
                            "O contexto atravessa a fila SQS: o analytics-service grava no <b>DynamoDB</b> dentro do mesmo trace.",
                            "Fluxo assíncrono: a resposta HTTP não espera a persistência analítica.",
                        ], "O Service Map global com os cinco microsserviços é mostrado no vídeo, no bloco de APM."))


def p_ev3(imgs):
    largura = largura_para_altura(IMGS, "chatops", 124)
    c = cabecalho("Evidência visual obrigatória · 3 de 4", "Notificação do incidente no ChatOps",
                  "Canal #incidentes-tech-challenge no Slack: o Grafana publica o alerta detalhado e o PagerDuty, o cartão do incidente.",
                  "Print exigido", "req") + f"""
    <div style="display:flex; gap:7mm; align-items:flex-start">
      {shot(IMGS, "chatops", "Slack · #incidentes-tech-challenge · 2026-11-09 16:01", largura)}
      <div style="flex:1">
        <div class="lbl" style="font-size:8pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#007F83;margin-bottom:2mm">
          Na gravação de 2026-11-11 · mensagens lidas pela API do Slack</div>
        <div class="msg firing"><span class="who">grafana-alertas-tc4</span><span class="when">01:01</span>
          <div class="title">[FIRING] FlagService5xxAlto - flag-service</div>
          Serviço: flag-service (critical) · Valor medido: A = 1 (100%)<br>Início: 04:00:50 UTC ·
          Ação automática: self-healing via GitHub Actions</div>
        <div class="msg pd"><span class="who">PagerDuty</span><span class="when">01:01</span>
          <div class="title">[FIRING] FlagService5xxAlto - flag-service</div>
          Urgency: High · Service: ToggleMaster Fase 4 · Triggered via: Grafana</div>
        <div class="msg resolved"><span class="who">grafana-alertas-tc4</span><span class="when">01:03</span>
          <div class="title">[RESOLVED] FlagService5xxAlto - flag-service</div>
          Valor medido: A = 0 · regra, runbook e link para silenciar</div>
        <p class="note">A linha "O que aconteceu" mostrou o texto do modelo no lugar do percentual; o valor aparece em
        "Valor medido". O modelo foi corrigido no repositório.</p>
      </div>
    </div>"""
    return pagina(c, PG["ev3"])


def p_ev4a(imgs):
    return pagina_print("ev4a", "Evidência visual obrigatória · 4 de 4", "Log da automação de self-healing",
                        "GitHub Actions disparado pelo alerta via repository_dispatch; o passo de restart registra a ação corretiva.",
                        "Print exigido", "req", "sh-log", "GitHub Actions · self-healing #1 · job restart",
                        fatos([("2026-11-09 · ensaio", ""), ("sucesso", "g"), ("passo em 26 s", "")], [
                            "<b>Assumir a role do self-healing (OIDC)</b>: credencial temporária, sem chave guardada.",
                            "<b>Reiniciar com allowlist e cooldown</b>: confere a lista permitida e 10 min desde o último restart.",
                            "<span class='mono'>deployment.apps/flag-service restarted</span> e <span class='mono'>successfully rolled out</span>.",
                            "<b>Pods do serviço depois do self-healing</b>: o pod novo em execução.",
                        ], f"Execução {RUN_ENSAIO['id']}, iniciada por repository_dispatch, sem nenhum clique humano."))


def p_ev4b(imgs):
    largura = 196
    log = (
        '<span class="t">04:01:07</span> Run bash scripts/self-healing/restart.sh\n'
        '<span class="t">04:01:07</span>   SERVICE: flag-service\n'
        '<span class="t">04:01:07</span>   ALERT_NAME: FlagService5xxAlto\n'
        '<span class="t">04:01:07</span>   ALERT_STATUS: firing\n'
        '<span class="t">04:01:07</span>   COOLDOWN_SECONDS: 600\n'
        '<span class="t">04:01:08</span> <span class="w">Reiniciando deployment/flag-service no namespace togglemaster.</span>\n'
        '<span class="t">04:01:09</span> <span class="k">deployment.apps/flag-service restarted</span>\n'
        '<span class="t">04:01:10</span> Waiting for deployment "flag-service" rollout to finish:\n'
        '                  1 old replicas are pending termination...\n'
        '<span class="t">04:01:31</span> <span class="k">deployment "flag-service" successfully rolled out</span>\n'
        '<span class="t">04:01:31</span> <span class="k">Self-healing concluido: flag-service reiniciado e com o rollout completo.</span>\n'
        '<span class="t">04:01:32</span> NAME                           READY   STATUS    AGE\n'
        '<span class="t">04:01:32</span> flag-service-cb85cd74d-lz4wq   1/1     Running   23s'
    )
    c = cabecalho("Evidência visual obrigatória · 4 de 4", "Execução do self-healing: ensaio e gravação",
                  "O resumo mostra o gatilho automático; o trecho ao lado é o log da execução feita durante a gravação do vídeo.",
                  "Print exigido", "req") + f"""
    <div style="display:flex; gap:7mm; align-items:flex-start">
      {shot(IMGS, "sh-resumo", "GitHub Actions · self-healing #1 · resumo do ensaio", largura)}
      <div class="facts" style="flex:1">{fatos([("Triggered via repository dispatch", "g"), ("Success · 43 s", "g")], [
            "O run nasce do webhook do Grafana: <b>Triggered via repository dispatch</b>.",
            "Job <b>restart</b> concluído em 39 s; execução total em 43 s.",
        ])}</div>
    </div>
    <div class="kicker" style="margin:5mm 0 2mm">Gravação de 2026-11-11 · execução {RUN_GRAVACAO['id']} · horários UTC</div>
    <div class="term">{log}</div>
    <p class="note" style="margin-top:2.2mm">Trecho exportado com <span class="mono">gh run view {RUN_GRAVACAO['id']} --log</span>.
    As credenciais temporárias aparecem mascaradas no log original e foram omitidas aqui.</p>"""
    return pagina(c, PG["ev4b"])


def p_apoio1(imgs):
    # Mesma altura para os dois prints: a soma das larguras ocupa a linha toda.
    ar1, ar2 = IMGS["firing"][1], IMGS["pagerduty"][1]
    h_img = (265 - 7) / (ar1 + ar2)
    w1, w2 = round(h_img * ar1, 1), round(h_img * ar2, 1)
    c = cabecalho("Evidência de apoio", "Alerta em Firing e incidente no PagerDuty",
                  "Os dois passos da prova real que vêm antes do ChatOps: a regra disparando e o incidente aberto sem clique humano.",
                  "Apoio", "apoio") + f"""
    <div style="display:flex; gap:7mm; align-items:flex-start">
      {shot(IMGS, "firing", "Grafana · Alert rules · FlagService5xxAlto", w1)}
      {shot(IMGS, "pagerduty", "PagerDuty · Incident #4", w2)}
    </div>
    <div class="cols" style="grid-template-columns: {w1}mm 1fr; gap:7mm; margin-top:4mm">
      <p class="note"><b>Firing</b> às 15:59:20: a razão 5xx ÷ total do flag-service sobe de 0 para 1 e cruza o limite de 0,1
      (linha vermelha). Avaliação a cada 30 s, período pendente de 1 min. Rótulos selfheal=true, service=flag-service e severity=critical.</p>
      <p class="note"><b>Incidente #4</b>: aberto às 3:59 PM, resolvido às 4:01 PM, duração de 2 minutos, urgência High,
      serviço ToggleMaster Fase 4.</p>
    </div>"""
    return pagina(c, PG["apoio1"])


def p_apoio2(imgs):
    w1, w2 = 172, 196
    c = cabecalho("Evidência de apoio", "Cluster EKS e GitOps em operação",
                  "A base das fases anteriores continua rodando com a nova stack: o ArgoCD reconcilia aplicação e observabilidade.",
                  "Apoio", "apoio") + f"""
    <div style="display:flex; gap:7mm; align-items:flex-start">
      {shot(IMGS, "argocd", "ArgoCD v2.13.9 · Applications", w1)}
      <div class="facts" style="flex:1">
        <div class="chips"><span class="chip g">6 Synced</span><span class="chip g">6 Healthy</span><span class="chip">2 nós Ready</span></div>
        <div class="lbl">O que os prints mostram</div>
        <ul class="clean">
          <li><b>togglemaster</b>: os cinco microsserviços, pelo overlay de produção.</li>
          <li><b>observability</b>, que organiza kube-prometheus-stack, Loki, otel-gateway e otel-agent como charts Helm.</li>
          <li>Abaixo, os dois nós m7i-flex.large do EKS, com Kubernetes v1.34.</li>
        </ul>
      </div>
    </div>
    <div style="margin-top:5mm">{shot(IMGS, "lens", "Lens · Nodes do cluster togglemaster", w2)}</div>"""
    return pagina(c, PG["apoio2"])


MATRIZ = [
    ("Base das fases 1 a 3 · p. 2", [
        ("5 microsserviços conteinerizados", "auth e evaluation em Go; flag, targeting e analytics em Python; imagens no ECR", "Vídeo: visão geral · services/"),
        ("Infraestrutura por Terraform", "3 camadas com estados próprios: base, cluster (EKS, RDS, Redis, IRSA) e k8s (ArgoCD, Secrets)", "Vídeo: visão geral · terraform/"),
        ("CI/CD com DevSecOps", "build, testes, lint, SAST (gosec, bandit), SCA e scan de imagem (Trivy); publicação no ECR por OIDC", "Vídeo: visão geral · .github/workflows/"),
        ("Kubernetes gerenciado por GitOps", "EKS 1.34 e ArgoCD v2.13.9 com 6 Applications Synced/Healthy", f"Vídeo: visão geral · p. {PG['apoio2']} · gitops/"),
    ]),
    ("Monitoramento open source · p. 3", [
        ("Prometheus por Helm no GitOps", "kube-prometheus-stack como Application própria", "gitops/observability/applications"),
        ("Loki com os logs dos contêineres", "Loki por Helm; agents em DaemonSet leem /var/log/pods de cada nó", f"Vídeo: métricas e logs · p. {PG['ev1b']}"),
        ("Dashboard customizado no Grafana", "recursos do cluster, requisições por serviço, erros, p95 e logs em tempo real", f"Vídeo · p. {PG['ev1a']}–{PG['ev1b']} · togglemaster-overview.json"),
    ]),
    ("OpenTelemetry · p. 4", [
        ("OTel Collector como peça central", "gateway e agents; traces → New Relic, logs → Loki, spanmetrics → Prometheus", f"Vídeo · p. {PG['arquitetura']} · otel-gateway.yaml, otel-agent.yaml"),
    ]),
    ("APM e tracing · p. 4", [
        ("Ferramenta APM comercial", "New Relic, com ingestão OTLP a partir do gateway", f"p. {PG['justificativa']}"),
        ("Instrumentação com OpenTelemetry", "SDK OTel em Go e Python (telemetry.go, telemetry.py); logs JSON com trace_id", "services/*/telemetry.*"),
        ("Distributed tracing do evaluation-service", "trace de GET /evaluate com 19 spans e o caminho entre os serviços", f"Vídeo: APM · p. {PG['ev2a']}"),
        ("Service Map dos 5 microsserviços", "mapa de dependências no New Relic", f"Vídeo: APM · p. {PG['ev2b']}"),
    ]),
    ("Alertas, incidentes e self-healing · p. 4–5", [
        ("Alerta inteligente", "FlagService5xxAlto: 5xx do flag-service acima de 10% por 1 min, avaliado a cada 30 s", f"Vídeo · p. {PG['apoio1']} · rules.yaml"),
        ("Incidente aberto automaticamente", "PagerDuty pela Events API v2; abre e resolve sozinho", f"Vídeo · p. {PG['apoio1']}, {PG['linha']} · contactpoints.yaml"),
        ("Notificação detalhada no ChatOps", "Slack: alerta detalhado do Grafana e cartão do PagerDuty", f"Vídeo · p. {PG['ev3']}"),
        ("Self-healing sem intervenção humana", "repository_dispatch → OIDC → lista permitida e cooldown de 600 s → rollout restart", f"Vídeo · p. {PG['ev4a']}–{PG['ev4b']} · self-healing.yml, restart.sh"),
    ]),
    ("Entregáveis · p. 5–6", [
        ("Código IaC/GitOps com a stack e o Collector", "gitops/observability e terraform/k8s", "repositório"),
        ("Código das aplicações instrumentado", "cinco serviços em services/", "repositório"),
        ("Scripts do self-healing", "scripts/self-healing, workflow self-healing e RBAC em gitops/base", "repositório"),
        ("Vídeo de até 25 min", "visão geral, métricas e logs, APM e prova real, gravados em 2026-11-11", "link na capa"),
        ("Relatório em PDF", "identificação, links, 4 prints e justificativa técnica", f"este documento, p. 1–{PG['ev4b']}"),
    ]),
]


def tabela_matriz(grupos, inicio):
    linhas, i = "", inicio
    for grupo, itens in grupos:
        linhas += f'<tr class="grp"><td colspan="4">{e(grupo)}</td></tr>'
        for r, como, onde in itens:
            i += 1
            linhas += f'<tr><td class="n">{i}</td><td class="r">{e(r)}</td><td>{e(como)}</td><td class="w">{e(onde)}</td></tr>'
    return (f'<table class="mx"><thead><tr><th>#</th><th>Requisito</th><th>Como foi atendido</th><th>Onde comprovar</th></tr></thead>'
            f'<tbody>{linhas}</tbody></table>'), i


def p_matriz(imgs):
    tabela, _ = tabela_matriz(MATRIZ[:4], 0)
    c = cabecalho("Cobertura dos requisitos · 1 de 2", "Matriz: requisito, solução e onde comprovar",
                  "A regra de avaliação (p. 5) desconta o que não for demonstrado no vídeo ou documentado no relatório. "
                  "Esta tabela aponta a prova de cada item.", "Enunciado p. 2–6", "info") + tabela
    return pagina(c, PG["matriz"])


def p_matriz2(imgs):
    antes = sum(len(itens) for _, itens in MATRIZ[:4])
    tabela, _ = tabela_matriz(MATRIZ[4:], antes)
    c = cabecalho("Cobertura dos requisitos · 2 de 2", "Matriz: resposta a incidentes e entregáveis",
                  "Continuação da matriz. A coluna da direita indica o bloco do vídeo, a página deste relatório ou o caminho no repositório.",
                  "Enunciado p. 4–6", "info") + tabela
    return pagina(c, PG["matriz2"])


def p_fecho(imgs):
    c = cabecalho("Encerramento", "Limites conhecidos, reprodução e referências",
                  "O que a solução não faz, como reproduzir o ambiente e de onde vieram os dados deste relatório.") + f"""
    <div class="cols" style="grid-template-columns: 1fr 1fr 1fr; gap:6mm">
      <div class="card amber"><h3>Limites conhecidos</h3><ul class="clean">
        <li>Reiniciar resolve falhas transitórias do processo, não uma dependência fora do ar. Com o banco parado, o alerta continuaria e o PagerDuty acionaria o plantão.</li>
        <li>O cooldown de 600 s evita reinícios em laço; um segundo alerta nesse intervalo fica só com o atendimento humano.</li>
        <li>O analytics consome a fila SQS de forma assíncrona; por isso não aparece com tráfego HTTP no dashboard.</li></ul></div>
      <div class="card"><h3>Como reproduzir</h3><ul class="clean">
        <li>Terraform em três camadas: base, cluster e k8s, cada uma com plano salvo.</li>
        <li>O ArgoCD sincroniza gitops/overlays/prod e gitops/observability a partir da main.</li>
        <li>Passo a passo em docs/GUIA_DE_REPRODUCAO.md; requisitos em docs/requisitos/README.md.</li>
        <li>Prints e índice em docs/evidencias/; roteiro do vídeo em docs/gravacao/.</li></ul></div>
      <div class="card"><h3>Execuções citadas</h3><ul class="clean">
        <li>Gravação: <a href="{RUN_GRAVACAO['url']}">self-healing {RUN_GRAVACAO['id']}</a></li>
        <li>Ensaio: <a href="{RUN_ENSAIO['url']}">self-healing {RUN_ENSAIO['id']}</a></li>
        <li>Repositório: <a href="{REPO}">{e(REPO.replace('https://', ''))}</a></li></ul></div>
    </div>
    <div class="card" style="margin-top:6mm"><h3>Referências</h3><ul class="clean ref">
      <li>FIAP. Tech Challenge Fase 4, enunciado (PDF no repositório), p. 2–6.</li>
      <li>New Relic. Pricing: <a href="https://newrelic.com/pricing">newrelic.com/pricing</a>.</li>
      <li>Datadog. Pricing: <a href="https://www.datadoghq.com/pricing/">datadoghq.com/pricing</a>.</li>
      <li>Atlassian. Opsgenie end of sale e end of support: <a href="https://www.atlassian.com/licensing/opsgenie">atlassian.com/licensing/opsgenie</a>.</li>
      <li>Grafana. Configure PagerDuty for alerting: <a href="https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/pager-duty/">grafana.com/docs/…/pager-duty</a>.</li>
      <li>OpenTelemetry. Collector Helm chart, presets de coleta de logs: <a href="https://opentelemetry.io/docs/platforms/kubernetes/helm/collector/">opentelemetry.io/docs/…/collector</a>.</li>
    </ul><p class="note" style="margin-top:1.6mm">Sites consultados em 2026-11-11. Dados da gravação obtidos do Loki, do log do GitHub Actions e da API do Slack.</p></div>"""
    return pagina(c, PG["fecho"])


PAGINAS = {"capa": p_capa, "sumario": p_sumario, "arquitetura": p_arquitetura, "justificativa": p_justificativa,
           "linha": p_linha, "ev1a": p_ev1a, "ev1b": p_ev1b, "ev2a": p_ev2a, "ev2b": p_ev2b, "ev3": p_ev3,
           "ev4a": p_ev4a, "ev4b": p_ev4b, "apoio1": p_apoio1, "apoio2": p_apoio2, "matriz": p_matriz,
           "matriz2": p_matriz2, "fecho": p_fecho}

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        IMGS = preparar_imagens(tmp)
        corpo = "".join(PAGINAS[k](IMGS) for k in ORDEM)
        doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
               f'<title>ToggleMaster · Relatório de entrega da Fase 4</title><style>{CSS}</style></head><body>{corpo}</body></html>')
        pagina_html = tmp / "relatorio.html"
        pagina_html.write_text(doc, encoding="utf-8")
        if "--html" in sys.argv:
            shutil.copy(pagina_html, sys.argv[sys.argv.index("--html") + 1])
        perfil = tmp / "perfil-edge"
        cmd = [str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
               f"--user-data-dir={perfil}", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=4000",
               f"--print-to-pdf={SAIDA}", pagina_html.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not SAIDA.exists():
            print(r.stdout, r.stderr)
            sys.exit("PDF não foi gerado")
    print(f"ok: {SAIDA.relative_to(RAIZ)} ({SAIDA.stat().st_size // 1024} KB, {len(ORDEM)} páginas planejadas)")
