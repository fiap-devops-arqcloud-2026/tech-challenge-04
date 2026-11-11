"""Gera o guia único de gravação (PowerPoint) a partir do roteiro e do passo a passo.

Fontes, sem cópia manual:
- falas: docs/gravacao/roteiro-conteudo.json (cada fala é dividida em trechos, e o
  script confere que os trechos somados reproduzem a fala original, letra por letra);
- comandos: blocos ```bash/```logql de docs/gravacao/PASSO_A_PASSO_POR_CENA.md
  (cada comando é buscado pelo início e precisa existir uma única vez).

Uso, na raiz do repositório:  py -3.14 -B 00_COLAB_IA/02_TRABALHO/entrega-gravacao-2026-11-11_v03/build_guia_unico.py
"""
import json
import math
import pathlib
import re

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

RAIZ = pathlib.Path(__file__).resolve().parents[3]
SAIDA = RAIZ / "docs/gravacao/ROTEIRO_GRAVACAO_2026-11-11_v03.pptx"
ROTEIRO = json.loads((RAIZ / "docs/gravacao/roteiro-conteudo.json").read_text(encoding="utf-8-sig"))
FALAS = {c["n"]: c for c in ROTEIRO["scenes"]}
MD = (RAIZ / "docs/gravacao/PASSO_A_PASSO_POR_CENA.md").read_text(encoding="utf-8")
BLOCOS = [b.strip() for b in re.findall(r"```(?:bash|logql)\n(.*?)```", MD, flags=re.S)]


def cmd(inicio):
    """Comando do passo a passo que começa com `inicio`; precisa ser único."""
    achados = [b for b in BLOCOS if b.startswith(inicio)]
    assert len(achados) == 1, f"comando não encontrado ou repetido: {inicio!r} ({len(achados)})"
    return achados[0]


def cmd_com(trecho):
    """Comando do passo a passo que contém `trecho`; precisa ser único."""
    achados = [b for b in BLOCOS if trecho in b]
    assert len(achados) == 1, f"comando não encontrado ou repetido: {trecho!r} ({len(achados)})"
    return achados[0]


def literal(c):
    """Comando curto escrito aqui; precisa aparecer no passo a passo."""
    assert c in MD, f"comando ausente do passo a passo: {c!r}"
    return c


# ---------------------------------------------------------------- paleta
NAVY = RGBColor(0x0B, 0x17, 0x2A)
INK = RGBColor(0x16, 0x2D, 0x45)
MUTED = RGBColor(0x50, 0x64, 0x7C)
TEAL = RGBColor(0x00, 0x7F, 0x83)
TINT = RGBColor(0xE3, 0xF3, 0xF2)
MINT = RGBColor(0xBF, 0xF5, 0xE2)
AMBER = RGBColor(0xF8, 0xBE, 0x57)
AMBER_TINT = RGBColor(0xFE, 0xF3, 0xDD)
CODE_BG = RGBColor(0x0F, 0x1E, 0x33)
CODE_FG = RGBColor(0xE6, 0xED, 0xF3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD7, 0xE1, 0xEA)

HEAD = "Cambria"
BODY = "Calibri"
MONO = "Courier New"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
W = 13.333


def box(slide, x, y, w, h, fill=None, shape=MSO_SHAPE.RECTANGLE, radius=0.08, name=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    if name:
        s.name = name
    return s


def text(slide, x, y, w, h, paragraphs, size=16, color=INK, font=BODY, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margin=0.0, name=None, space_after=0):
    """paragraphs: str, ou lista de parágrafos; cada parágrafo é str ou lista de (texto, opções)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for lado in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{lado}", Inches(margin))
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    for i, par in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        runs = [(par, {})] if isinstance(par, str) else par
        for conteudo, opt in runs:
            r = p.add_run()
            r.text = conteudo
            f = r.font
            f.name = opt.get("font", font)
            f.size = Pt(opt.get("size", size))
            f.bold = opt.get("bold", bold)
            f.italic = opt.get("italic", False)
            f.color.rgb = opt.get("color", color)
    return tb


def linhas(texto, tamanho, largura, fator=0.50):
    """Estimativa conservadora de linhas para Calibri/Courier."""
    por_linha = max(1, int(largura / (tamanho * fator / 72)))
    return sum(max(1, math.ceil(len(p) / por_linha)) for p in texto.split("\n"))


def pill(slide, x, y, rotulo, fill=AMBER, color=NAVY, w=None):
    w = w or (0.22 + len(rotulo) * 0.105)
    box(slide, x, y, w, 0.34, fill, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
    text(slide, x, y, w, 0.34, rotulo, 11, color, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return w


def code(slide, x, y, w, comando, rotulo=None, size=12):
    """Bloco escuro de terminal. Devolve a altura usada."""
    topo = y
    if rotulo:
        text(slide, x, y, w, 0.3, [[(rotulo, {"bold": True, "color": TEAL})]], 13)
        y += 0.32
    h = linhas(comando, size, w - 0.3, 0.62) * size * 1.18 / 72 + 0.24
    box(slide, x, y, w, h, CODE_BG, MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
    text(slide, x, y, w, h, comando, size, CODE_FG, MONO, margin=0.13, anchor=MSO_ANCHOR.MIDDLE)
    return (y + h) - topo


def notas(slide, conteudo):
    slide.notes_slide.notes_text_frame.text = conteudo


def titulo(slide, t, sub=None):
    text(slide, 0.5, 0.38, 12.3, 0.62, t, 30, NAVY, HEAD, bold=True)
    if sub:
        text(slide, 0.5, 1.0, 12.3, 0.4, sub, 15, MUTED)


def rodape(slide, n):
    text(slide, 0.5, 7.08, 9, 0.26, "ToggleMaster · Fase 4 · guia único de gravação", 10, MUTED)
    text(slide, 11.83, 7.08, 1.0, 0.26, f"{n:02d}", 10, TEAL, bold=True, align=PP_ALIGN.RIGHT)


def novo(fundo=WHITE):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = fundo
    return s


# ================================================================ conteúdo das cenas
# Cada linha: (trecho exato da fala, onde, o que fazer, o que deve aparecer)
CENAS = {
    "01": dict(rows=[
        ("Este é o ToggleMaster, uma plataforma de feature flags com cinco microsserviços. A Fase 4 evolui a base das fases anteriores para responder a três perguntas: o sistema está saudável, onde uma requisição falhou e como reagimos ao incidente?",
         "Aba 1", "topo do README", "título e \"cinco microsserviços\""),
        ("Mantivemos Terraform, CI/CD com verificações de segurança e GitOps. Agora acrescentamos métricas, logs, traces e uma tentativa automática de recuperação.",
         "Aba 1", "role até \"O que foi reaproveitado e o que a Fase 4 acrescentou\"", "coluna da base ao lado da coluna da Fase 4"),
        ("Vou demonstrar o ambiente funcionando e depois provocar uma falha controlada para acompanhar a resposta completa.",
         "Aba 1", "role até \"Arquitetura de observabilidade e resposta\" e \"Serviços e arquitetura da base\"", "diagrama e tabela dos cinco serviços"),
    ]),
    "02": dict(rows=[
        ("A infraestrutura está dividida em três camadas Terraform, com estados separados.",
         "Aba 2", "aponte terraform/ (base), terraform/cluster e terraform/k8s", "as três pastas"),
        ("O código fica no Git; o state fica no backend S3 e relaciona os recursos declarados aos recursos existentes.",
         "Aba 1", "seção \"Terraform e ArgoCD\" do README", "\"O backend guarda o state, não o código\""),
        ("Os cinco serviços possuem pipelines que reutilizam verificações por linguagem. Aqui vemos build e testes, análise do código e das dependências.",
         "Aba 3", "grafo de jobs; clique em SAST (gosec) e SCA (Trivy fs)", "jobs verdes"),
        ("No pull request, a imagem também é construída e verificada.",
         "Aba 3", "clique em #1 no título do run → Checks", "\"Imagem Docker e Trivy (sem push)\" verde"),
        ("No push da main, o pipeline publica no ECR usando OIDC e atualiza a tag no GitOps. É o ArgoCD que reconcilia essa configuração no cluster.",
         "Aba 3", "volte; job \"Imagem Docker e push no ECR\" → passos Trivy, OIDC e Push; depois \"Atualizar tag no GitOps\"", "commit chore(gitops): auth-service para v1.0.0-…"),
    ]),
    "03": dict(rows=[
        ("Este é o cluster EKS provisionado por código.",
         "Lens", "tela Nodes", "2 nós Ready, versão v1.34"),
        ("No Lens, vemos os nós e os pods das aplicações e da observabilidade. O Lens é apenas uma interface de inspeção.",
         "Lens", "Workloads → Pods; filtre togglemaster e depois observability", "tudo Running"),
        ("No ArgoCD, as seis aplicações estão sincronizadas com o estado desejado no Git e saudáveis nesta consulta.",
         "Aba 4", "Applications (opcional antes: Terminal C, comandos abaixo)", "6 cartões Synced e Healthy"),
        ("A aplicação observability organiza os componentes: kube-prometheus-stack, Loki, Collector gateway e Collector agents.",
         "Aba 4", "clique em observability", "árvore com as 4 Applications filhas"),
        ("Os valores dos charts e as configurações do dashboard e dos alertas estão versionados. Assim, a stack de monitoramento também segue GitOps.",
         "Aba 2", "gitops/observability/values e gitops/observability/grafana", "values, dashboard e alertas"),
    ], cmds=[("Terminal C", literal("kubectl get nodes")), ("Terminal C", literal("kubectl get applications -n argocd"))]),
    "04": dict(rows=[
        ("Este dashboard foi customizado para o ToggleMaster. A taxa de requisições mostra o tráfego recebido pelos serviços HTTP.",
         "Aba 5", "painel \"Requisicoes por segundo por servico\"", "uma linha por serviço HTTP"),
        ("A proporção de erros indica quantas respostas falharam, e a latência p95 ajuda a observar a experiência nas requisições mais lentas.",
         "Aba 5", "\"flag-service: erros 5xx agora\", \"Taxa de erro (5xx)\" e \"Latencia p95 por servico\"", "0% de erro; p95 em ms"),
        ("Mais abaixo, CPU e memória permitem relacionar comportamento da aplicação e recursos do cluster.",
         "Aba 5", "role até CPU/Memoria por no e por pod", "2 nós e os pods do togglemaster"),
        ("O painel de logs consulta o Loki. Analytics processa eventos de forma assíncrona, portanto não deve ser apresentado como se tivesse o mesmo tráfego HTTP dos demais serviços.",
         "Aba 5", "\"Logs da aplicacao (Loki)\"; volte ao painel de requisições", "logs recentes; analytics sem linha HTTP"),
        ("Vou conferir o intervalo de tempo e a atualização para demonstrar dados atuais.",
         "Aba 5", "canto superior direito", "Last 15 minutes e 10s"),
    ], prints=["PRINT 01"]),
    "05": dict(rows=[
        ("Métricas resumem valores ao longo do tempo; logs registram eventos; traces mostram o caminho de uma execução, dividido em spans. Aqui consulto logs centralizados pelo Loki.",
         "Aba 6", "fonte Loki → Code → cole a consulta 1 → Run query", "linhas com \"sqs.published\""),
        ("O trace_id permite correlacionar um evento ao rastreamento da requisição.",
         "Aba 6", "abra uma linha (consulta 2 mostra o flag-service)", "service.name, horário e trace_id"),
        ("Em cada nó, um Collector agent lê os logs dos contêineres e os envia ao gateway. As aplicações enviam seus traces ao mesmo gateway.",
         "Aba 1", "diagrama do README (ou \"Pods, nós e distribuição do Collector\")", "agents → gateway"),
        ("Ele processa os dados, encaminha logs ao Loki, traces ao New Relic e gera métricas de aplicação pelo spanmetrics para o Prometheus.",
         "Aba 2", "gitops/observability/values/otel-gateway.yaml, seção pipelines", "traces, metrics e logs"),
        ("As métricas de infraestrutura são coletadas diretamente pelo Prometheus nos exporters.",
         "Lens", "Pods → observability", "node-exporter e kube-state-metrics"),
    ], cmds=[("Consulta 1 · Loki", cmd('{k8s_namespace_name="togglemaster", service_name="evaluation-service"}')),
             ("Consulta 2 · Loki", literal('{k8s_namespace_name="togglemaster", service_name="flag-service"}'))]),
    "06": dict(rows=[
        ("Escolhemos New Relic como o APM comercial desta entrega. Ele recebe os traces via OpenTelemetry. No mapa, observamos as dependências dos cinco microsserviços.",
         "Aba 8", "Service map; amplie as dependências se precisar", "os cinco serviços ligados"),
        ("Agora faço uma requisição ao evaluation-service.",
         "Terminal C", "comandos ① e ② (próximo slide)", "\"Flag criada: video-…\" e \"result\":true"),
        ("No trace detalhado, vemos as chamadas aos serviços de flags, segmentação e autenticação, além das dependências de dados.",
         "Aba 9", "filtre evaluation-service → GET /evaluate → trace do horário do curl", "cascata com os serviços"),
        ("O caminho varia: um acerto no Redis pode encurtar a execução. Para a demonstração completa, seleciono uma requisição sem cache e confiro seu horário.",
         "Aba 9", "aponte o span do Redis e o horário", "o trace da flag nova"),
        ("O fluxo de SQS e analytics é assíncrono; a resposta HTTP não espera a persistência analítica. A duração de cada span ajuda a localizar uma operação lenta.",
         "Aba 9", "span da SQS; clique no span mais longo", "duração e atributos"),
    ], prints=["PRINT 02"]),
    "07": dict(rows=[
        ("Agora vou provocar uma falha transitória controlada no flag-service. O objetivo é demonstrar detecção e reação automáticas, sem desligar um banco.",
         "Terminal A", "aponte o log", "o log mostra -> 200"),
        ("A rota administrativa exige autenticação e faz as rotas de flags responderem 503.",
         "Terminal C", "comando ③ (próximo slide)", "Terminal A passa a -> 503"),
        ("O health check continua saudável; por isso, o Kubernetes não reinicia o processo apenas pela liveness probe.",
         "Terminal C", "comando ④; aponte o Terminal B", "health: 200; pod Running, 0 restarts"),
        ("O tráfego contínuo permite medir a proporção de erros.",
         "Aba 5", "\"flag-service: erros 5xx agora\"", "sobe em 30 a 60 s"),
        ("A falha fica na memória do processo e desaparece quando um novo pod assume. Vou observar a cadeia sem clicar em Run workflow nem reiniciar manualmente o serviço.",
         "Aba 7", "tire as mãos do teclado e vá para Alert rules", ""),
    ]),
    "08": dict(rows=[
        ("A regra avalia a proporção de erros 5xx do flag-service.",
         "Aba 7", "FlagService5xxAlto", "Pending 30 a 60 s depois da falha"),
        ("O limite escolhido é maior que dez por cento durante um minuto; isso evita reagir a um único erro isolado. O exemplo do enunciado usa outro serviço e outro percentual, mas nossa regra atende ao mesmo objetivo.",
         "Aba 7", "espere", "Firing cerca de 1 min depois"),
        ("Quando entra em Firing, o Grafana abre um incidente no PagerDuty e envia o contexto ao Slack.",
         "Aba 10", "incidente novo → abra os detalhes", "Triggered, criado sozinho"),
        ("PagerDuty organiza o incidente e o acionamento humano; Slack concentra a comunicação.",
         "Aba 11", "#incidentes-tech-challenge", "[FIRING:1] FlagService5xxAlto e cartão do PagerDuty"),
        ("Aqui confiro serviço, horário e descrição para mostrar que as telas correspondem à mesma falha. Um DatasourceError não é a evidência desta regra de erros HTTP.",
         "Aba 11", "aponte Servico, Detalhe e Inicio", "mesmo horário do Firing"),
    ], prints=["PRINT 03"],
        aviso="Não leia a linha \"O que aconteceu\" do Slack: ela mostra o texto do modelo no lugar do percentual."),
    "09": dict(rows=[
        ("O mesmo alerta chama o webhook do GitHub e dispara esta execução automaticamente.",
         "Aba 12", "atualize a página", "run novo: repository_dispatch"),
        ("O workflow assume uma role temporária por OIDC.",
         "Aba 12", "run → job → \"Assumir a role do self-healing (OIDC)\"", "passo verde"),
        ("Antes de agir, o script valida o serviço em uma lista permitida e verifica um intervalo mínimo de dez minutos entre reinícios. Ele executa rollout restart e aguarda o rollout terminar.",
         "Aba 12", "expanda \"Reiniciar com allowlist e cooldown\"", "allowlist, cooldown e \"restarted\""),
        ("Aqui vemos o registro da ação e a substituição do pod.",
         "Terminal B", "aponte a troca", "antigo Terminating, novo Running"),
        ("O tráfego volta a 200, o alerta retorna ao normal e o incidente é resolvido.",
         "Terminal A", "depois abas 7, 10 e 11", "log em -> 200; alerta Normal; incidente Resolved"),
        ("Isso é uma tentativa de mitigação, não uma cura universal: um banco indisponível, por exemplo, não seria corrigido apenas reiniciando a aplicação.",
         "Só fala", "mantenha o Terminal A na tela", ""),
    ], prints=["PRINT 04"]),
    "10": dict(rows=[
        ("Demonstramos a base automatizada, as métricas e os logs centralizados, o roteamento pelo Collector e o tracing no APM. Na prova do incidente, acompanhamos a falha controlada, o alerta, a comunicação e a tentativa automática de recuperação.",
         "Aba 1", "segundo diagrama de \"Arquitetura de observabilidade e resposta\"", "Grafana → PagerDuty, Slack e Actions"),
        ("O repositório reúne o código de infraestrutura, a instrumentação e a automação.",
         "Aba 1", "\"Onde está cada requisito da Fase 4\"", "requisito → arquivo"),
        ("O relatório traz os quatro prints exigidos e justifica a arquitetura e as escolhas de New Relic e PagerDuty.",
         "PDF local", "docs/relatorio/RELATORIO_ENTREGA_2026-11-10_v02.pdf", "prints e justificativas"),
        ("As evidências precisam corresponder ao que foi realmente executado. Obrigado.",
         "STOP", "pare a gravação", "duração até 25 min"),
    ]),
}
OBRIGATORIAS = {"03", "04", "05", "06", "07", "08", "09"}

# Confere que os trechos reproduzem a fala original, sem perder nem inventar palavra.
for n, cena in CENAS.items():
    junto = " ".join(r[0] for r in cena["rows"])
    assert junto == FALAS[n]["speech"], f"fala da cena {n} não confere com o roteiro"


def slide_cena(n, cena, numero):
    meta = FALAS[n]
    s = novo()
    # cabeçalho: número em círculo, título, tempo e tela
    box(s, 0.5, 0.4, 0.82, 0.82, TEAL, MSO_SHAPE.OVAL, name=f"Cena {n}")
    text(s, 0.5, 0.4, 0.82, 0.82, n, 24, WHITE, HEAD, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, 1.55, 0.36, 8.4, 0.56, meta["title"], 28, NAVY, HEAD, bold=True)
    text(s, 1.57, 0.9, 8.4, 0.36, f"{meta['time']}  ·  {meta['tool']}", 14, MUTED)
    x = W - 0.5
    for rot, fill in [(p, AMBER) for p in reversed(cena.get("prints", []))] + (
            [("★ OBRIGATÓRIO", MINT)] if n in OBRIGATORIAS else []):
        w = 0.22 + len(rot) * 0.105
        x -= w
        pill(s, x, 0.55, rot, fill, NAVY, w)
        x -= 0.15

    # colunas
    xl, wl, xr, wr = 0.5, 7.0, 7.75, 5.08
    tam = 16
    extras = 0.0
    meio = (12.33 - 0.25) / 2
    rot_w = 1.75
    if cena.get("cmds"):
        extras += 0.2 + max(linhas(c, 12, meio - rot_w - 0.3, 0.62) * 12 * 1.18 / 72 + 0.24 for _, c in cena["cmds"])
    if cena.get("aviso"):
        extras += 0.62
    disponivel = 7.0 - 1.82 - extras
    while True:
        alturas = []
        for fala, onde, faca, ver in cena["rows"]:
            hl = linhas(fala, tam, wl, 0.47) * tam * 1.2 / 72
            hr = (linhas(onde + " · " + faca, tam - 2, wr - 0.3, 0.47) * (tam - 2) * 1.2
                  + (linhas("→ " + ver, 12, wr - 0.3, 0.47) * 12 * 1.2 if ver else 0)) / 72 + 0.2
            alturas.append(max(hl, hr) + 0.12)
        if sum(alturas) <= disponivel or tam <= 14:
            break
        tam -= 1
    assert sum(alturas) <= disponivel + 0.05, f"cena {n} não coube ({sum(alturas):.2f} > {disponivel:.2f})"

    text(s, xl, 1.45, wl, 0.3, [[("DIGA", {"bold": True, "color": TEAL})]], 12)
    text(s, xr, 1.45, wr, 0.3, [[("FAÇA  ·  ONDE  →  O QUE APARECE", {"bold": True, "color": TEAL})]], 12)
    y = 1.82
    for (fala, onde, faca, ver), h in zip(cena["rows"], alturas):
        text(s, xl, y, wl, h - 0.12, fala, tam, NAVY)
        box(s, xr, y - 0.04, wr, h - 0.08, TINT, MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
        pars = [[(onde, {"bold": True, "color": TEAL}), ("  ·  " + faca, {})]]
        if ver:
            pars.append([("→ " + ver, {"size": 12, "color": MUTED, "italic": True})])
        text(s, xr, y - 0.04, wr, h - 0.08, pars, tam - 2, INK, margin=0.13, space_after=2,
             anchor=MSO_ANCHOR.TOP if ver else MSO_ANCHOR.MIDDLE)
        y += h

    if cena.get("aviso"):
        box(s, 0.5, y + 0.05, 12.33, 0.5, AMBER_TINT, MSO_SHAPE.ROUNDED_RECTANGLE, 0.2)
        text(s, 0.5, y + 0.05, 12.33, 0.5, [[("Atenção  ", {"bold": True}), (cena["aviso"], {})]], 14, NAVY,
             margin=0.15, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.62
    if cena.get("cmds"):
        for i, (rot, c) in enumerate(cena["cmds"]):
            x = 0.5 + i * (meio + 0.25)
            h = code(s, x + rot_w, y + 0.12, meio - rot_w, c)
            text(s, x, y + 0.12, rot_w - 0.1, h, [[(rot, {"bold": True, "color": TEAL})]], 13, anchor=MSO_ANCHOR.MIDDLE)
    rodape(s, numero)
    linhas_notas = [f"CENA {n} · {meta['time']} · {meta['tool']}", "", "FALA COMPLETA:", meta["speech"], "",
                    "AÇÕES:"] + [f"- {o}: {f} → {v}" for _, o, f, v in cena["rows"]]
    if cena.get("prints"):
        linhas_notas += ["", "Capture agora: " + ", ".join(cena["prints"]) + "."]
    notas(s, "\n".join(linhas_notas))


def slide_comandos(titulo_slide, subtitulo, itens, numero):
    """itens: (rótulo, comando, esperado)."""
    s = novo()
    titulo(s, titulo_slide, subtitulo)
    y = 1.65
    xl, wl, xc, wc = 0.5, 3.1, 3.85, 8.98
    for rot, c, esperado in itens:
        hc = code(s, xc, y, wc, c)
        pars = [[(rot, {"bold": True, "color": TEAL})]]
        hl = linhas(rot, 14, wl, 0.5) * 14 * 1.2 / 72
        if esperado:
            pars.append([("→ " + esperado, {"size": 12, "color": MUTED, "italic": True})])
            hl += linhas(esperado, 12, wl, 0.5) * 12 * 1.2 / 72 + 0.05
        text(s, xl, y, wl, max(hc, hl), pars, 14, NAVY, space_after=3)
        y += max(hc, hl) + 0.2
    assert y <= 7.0, f"slide de comandos '{titulo_slide}' passou do limite ({y:.2f})"
    rodape(s, numero)
    notas(s, "Comandos para copiar (no PowerPoint, em modo de edição; no PDF a quebra de linha pode cortar o comando):\n\n"
          + "\n\n".join(f"{r}:\n{c}" for r, c, _ in itens))


# ================================================================ montagem
numero = 0

# 1. capa
numero += 1
s = novo(NAVY)
text(s, 0.9, 1.0, 11.5, 0.9, "ToggleMaster · Fase 4", 26, MINT, HEAD, bold=True)
text(s, 0.9, 1.75, 11.5, 1.2, "Guia único de gravação", 52, WHITE, HEAD, bold=True)
text(s, 0.9, 2.95, 11.5, 0.6, "Fala, tela e comando no mesmo lugar, cena por cena", 22, MINT)
for i, (num, rot) in enumerate([("10", "cenas"), ("21 min", "roteiro + 4 de margem"), ("4", "prints obrigatórios"),
                                ("25 min", "limite da FIAP")]):
    x = 0.9 + i * 2.95
    text(s, x, 4.0, 2.8, 0.8, num, 40, WHITE, HEAD, bold=True)
    text(s, x, 4.8, 2.8, 0.4, rot, 15, MINT)
legenda = [("DIGA", "a fala, em ordem"), ("FAÇA", "onde clicar e o que deve aparecer"),
           ("PRINT", "capture naquele momento"), ("★", "bloco exigido pela FIAP")]
for i, (k, v) in enumerate(legenda):
    x = 0.9 + i * 2.95
    box(s, x, 5.75, 2.75, 0.85, INK, MSO_SHAPE.ROUNDED_RECTANGLE, 0.15)
    text(s, x, 5.75, 2.75, 0.85, [[(k, {"bold": True, "color": AMBER if k == "PRINT" else MINT})], [(v, {})]],
         13, WHITE, margin=0.15, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.9, 6.85, 11.5, 0.35, "Fonte das falas: docs/gravacao/roteiro-conteudo.json · comandos: PASSO_A_PASSO_POR_CENA.md · enunciado FIAP p. 5–6",
     11, MINT)
notas(s, "Abra este arquivo em outro monitor ou dispositivo. No modo apresentador, as notas trazem a fala completa de cada cena. "
         "Copie os comandos no PowerPoint em modo de edição ou no PASSO_A_PASSO_POR_CENA.md.")

# 2. mesa
numero += 1
s = novo()
titulo(s, "Monte a mesa antes do REC", "Abas na ordem das cenas; terminais com uma tarefa cada. Docker Desktop fechado.")
abas = [("1", "GitHub · README", "01, 02, 05, 10"), ("2", "GitHub · pasta terraform/", "02, 03, 05"),
        ("3", "Actions · run do auth-service no merge", "02"), ("4", "ArgoCD · Applications (localhost:8080)", "03"),
        ("5", "Grafana · ToggleMaster - Visao geral", "04, 07"), ("6", "Grafana · Explore → Loki", "05"),
        ("7", "Grafana · Alert rules → FlagService5xxAlto", "08, 09"), ("8", "New Relic · Service map", "06"),
        ("9", "New Relic · Distributed tracing", "06"), ("10", "PagerDuty · Incidents", "08, 09"),
        ("11", "Slack · #incidentes-tech-challenge", "08, 09"), ("12", "Actions · workflow self-healing", "09")]
text(s, 0.5, 1.55, 7.2, 0.3, [[("ABAS DO BRAVE", {"bold": True, "color": TEAL})]], 12)
y = 1.9
for num, nome, cenas in abas:
    box(s, 0.5, y, 0.38, 0.38, TEAL, MSO_SHAPE.OVAL)
    text(s, 0.5, y, 0.38, 0.38, num, 12, WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 1.0, y, 5.0, 0.38, nome, 14, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.0, y, 1.7, 0.38, "cena " + cenas, 12, MUTED, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.42
text(s, 8.1, 1.55, 4.7, 0.3, [[("JANELAS", {"bold": True, "color": TEAL})]], 12)
janelas = [("A", "Terminal A", "log do pod trafego · cenas 07–09"), ("B", "Terminal B", "pods do flag-service · cenas 07–09"),
           ("C", "Terminal C", "comandos · cenas 03, 06, 07"), ("D", "Terminal D", "túneis · minimizado, fora do vídeo"),
           ("L", "Lens", "Nodes e Pods · cenas 03 e 05")]
y = 1.9
for k, nome, uso in janelas:
    box(s, 8.1, y, 4.73, 0.78, TINT, MSO_SHAPE.ROUNDED_RECTANGLE, 0.15)
    box(s, 8.25, y + 0.15, 0.48, 0.48, NAVY, MSO_SHAPE.OVAL)
    text(s, 8.25, y + 0.15, 0.48, 0.48, k, 15, MINT, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 8.9, y + 0.08, 3.85, 0.66, [[(nome, {"bold": True})], [(uso, {"size": 13, "color": MUTED})]], 15, NAVY,
         anchor=MSO_ANCHOR.MIDDLE)
    y += 0.9
box(s, 8.1, y + 0.05, 4.73, 0.62, AMBER_TINT, MSO_SHAPE.ROUNDED_RECTANGLE, 0.15)
text(s, 8.1, y + 0.05, 4.73, 0.62, [[("Fora do vídeo: ", {"bold": True}), (".env, Secrets, senhas e páginas de chaves", {})]],
     13, NAVY, margin=0.15, anchor=MSO_ANCHOR.MIDDLE)
rodape(s, numero)
notas(s, "Grafana: período Last 15 minutes e atualização 10s. Lens: cluster togglemaster na tela Nodes.")

# 3. túneis
numero += 1
slide_comandos("Terminal D · abra os três túneis", "Cada túnel roda num laço que o reabre sozinho em 2 s se a conexão cair.", [
    ("1 · portas livres?", cmd("for p in 8080 3000 8004"), "três linhas \"livre\""),
    ("2 · ArgoCD (8080)", cmd("(while true; do kubectl -n argocd"), None),
    ("3 · Grafana (3000)", cmd("(while true; do kubectl -n observability"), None),
    ("4 · evaluation (8004)", cmd("(while true; do kubectl -n togglemaster"), None),
    ("5 · conferência, 5 s depois", cmd("for u in http://127.0.0.1:8080"), "três linhas começando com 200; minimize a janela D sem fechar"),
], numero)

# 4. terminais e logins
numero += 1
slide_comandos("Terminais A, B e C · tráfego, pods e logins", "As senhas vão direto para a área de transferência, sem aparecer na tela.", [
    ("Terminal A · tráfego", cmd("kubectl logs -f trafego"), "flag-service /flags -> 200 a cada segundo"),
    ("Terminal B · pods do flag-service", cmd("kubectl get pods -n togglemaster -l app=flag-service -w"), "1 pod Running"),
    ("Terminal C · senha do ArgoCD (admin, localhost:8080)", cmd("kubectl -n argocd get secret"), None),
    ("Terminal C · senha do Grafana (admin, localhost:3000)", cmd("kubectl -n observability get secret"), None),
    ("Terminal C · última conferência, depois rode clear", literal("kubectl get pods -n togglemaster -l app=flag-service"),
     "AGE maior que 10 min (cooldown de 600 s)"),
], numero)

# 5+. cenas, com slides de comandos depois da 06 e da 07
for n in sorted(CENAS):
    numero += 1
    slide_cena(n, CENAS[n], numero)
    if n == "06":
        numero += 1
        slide_comandos("Cena 06 · comandos do Terminal C", "A chave fica dentro do pod trafego e não aparece na tela.", [
            ("① cria uma flag nova (o cache é por nome da flag)", cmd("kubectl exec -n togglemaster trafego -- sh -c 'NOME="), "Flag criada: video-…"),
            ("② requisição de demonstração: troque NOME_DA_FLAG pelo nome impresso", cmd("curl -s \"http://127.0.0.1:8004/evaluate"),
             "\"result\":true; o trace aparece no New Relic em 10 a 60 s"),
        ], numero)
    if n == "07":
        numero += 1
        slide_comandos("Cena 07 · comandos do Terminal C", "Depois do ③, não reinicie nada: a correção precisa ser automática.", [
            ("③ ativa a falha controlada", cmd_com('{\\"enabled\\":true}'),
             "Terminal A passa a -> 503"),
            ("④ prova que o health continua saudável", cmd("kubectl exec -n togglemaster trafego -- curl"), "health: 200"),
        ], numero)

# se algo der errado
numero += 1
s = novo()
titulo(s, "Se algo der errado", "Não reinicie à mão como se fosse automático; diga no vídeo quando houver intervenção.")
problemas = [
    ("Túnel não responde", "tail -5 /tmp/tunel-grafana.log (troque o nome); porta ocupada: feche o Docker Desktop"),
    ("Alerta não dispara", "Terminal A mostra -> 503? o painel de 5xx subiu? espere de 1 a 3 min"),
    ("Self-healing termina em cooldown", "faz menos de 10 min do último restart: espere e repita"),
    ("Trace não aparece", "espere 10 a 60 s; aumente o período para Last 30 minutes"),
    ("Pod com erro", "kubectl describe pod <pod> -n <namespace> | tail -20 e kubectl logs <pod> -n <namespace>"),
]
y = 1.6
for p, r in problemas:
    box(s, 0.5, y, 12.33, 0.62, TINT, MSO_SHAPE.ROUNDED_RECTANGLE, 0.15)
    text(s, 0.65, y, 3.6, 0.62, p, 15, NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 4.3, y, 8.4, 0.62, r, 14, INK, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.72
code(s, 0.5, y + 0.1, 12.33, cmd_com('{\\"enabled\\":false}'),
     "Contingência: só se a automação falhar; desliga a falha e não conta como self-healing")
rodape(s, numero)
notas(s, "Contingência (enabled=false) encerra a falha manualmente. Registre a intervenção no vídeo.")

# cola rápida
numero += 1
s = novo()
titulo(s, "Cola rápida · números e conceitos", "Para responder sem consultar outro documento.")
stats = [("5", "microsserviços"), ("2", "nós Ready"), ("6", "Applications"), (">10% · 1 min", "regra de 5xx"), ("600 s", "cooldown")]
for i, (v, r) in enumerate(stats):
    x = 0.5 + i * 2.5
    box(s, x, 1.6, 2.33, 1.35, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE, 0.12)
    text(s, x, 1.68, 2.33, 0.75, v, 30 if len(v) < 6 else 22, WHITE, HEAD, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, x, 2.43, 2.33, 0.4, r, 14, MINT, align=PP_ALIGN.CENTER)
conceitos = [
    ("Erro 5xx", "o pedido estava certo, mas o servidor falhou (500 erro interno; 503 indisponível, o da falha controlada). "
                 "4xx é erro de quem chamou, como o 401 de chave inválida, e não entra no alerta."),
    ("Latência p95", "95% das requisições responderam nesse tempo ou menos; 5% demoraram mais. A média esconde os lentos, e o p95 os mostra."),
    ("RED", "Rate, Errors, Duration: requisições/s, erros 5xx e p95, os três painéis do topo do dashboard."),
    ("Self-healing", "Grafana → repository_dispatch → GitHub Actions (OIDC) → lista permitida + cooldown → rollout restart."),
]
y = 3.25
for k, v in conceitos:
    text(s, 0.5, y, 2.4, 0.8, k, 16, TEAL, bold=True)
    text(s, 2.9, y, 9.9, 0.8, v, 15, NAVY)
    y += 0.88
rodape(s, numero)
notas(s, "Exemplo do p95: em 100 requisições, 90 levam 20 ms e 10 levam 1 s. A média dá 118 ms; o p95 dá 1 s.")

# depois do STOP
numero += 1
s = novo(NAVY)
text(s, 0.5, 0.38, 12.3, 0.62, "Depois do STOP", 30, WHITE, HEAD, bold=True)
text(s, 0.5, 1.0, 12.3, 0.4, "Confira vídeo e prints antes de qualquer destroy.", 15, MINT)
prints = [("PRINT 01", "Grafana · dashboard com dados (pode ser em 2 imagens)"), ("PRINT 02", "New Relic · trace aberto com spans e durações"),
          ("PRINT 03", "Slack · mensagem do incidente"), ("PRINT 04", "Actions · passo do restart + Terminal B com o pod novo")]
for i, (k, v) in enumerate(prints):
    x = 0.5 + (i % 2) * 6.25
    y = 1.65 + (i // 2) * 1.2
    box(s, x, y, 6.08, 1.0, INK, MSO_SHAPE.ROUNDED_RECTANGLE, 0.12)
    pill(s, x + 0.2, y + 0.33, k)
    text(s, x + 1.55, y, 4.4, 1.0, v, 15, WHITE, anchor=MSO_ANCHOR.MIDDLE)
passos = ["Salve os prints em docs/evidencias/entrada-local/ e cubra chaves e e-mails.",
          "Apoios úteis: Service Map, Firing, PagerDuty, Loki, ArgoCD e Lens.",
          "Feche o Terminal D para encerrar os túneis; taskkill //IM kubectl.exe //F só no fim.",
          "O encerramento da AWS segue o guia de deploy (Parte 4), com plano salvo."]
text(s, 0.5, 4.25, 12.3, 2.5, [[("•  " + p, {})] for p in passos], 16, WHITE, space_after=8)
rodape(s, numero)
notas(s, "Relatório: nomes, RMs, usernames, links do repositório e do vídeo, quatro prints e justificativas.")

prs.save(SAIDA)
print(f"ok: {numero} slides em {SAIDA.relative_to(RAIZ)}")
