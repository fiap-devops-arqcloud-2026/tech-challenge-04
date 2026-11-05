"""Conferência de leitura do overlay de produção no primeiro deploy (B3).

Uso a partir da raiz do projeto: py -3.14 CAMINHO/checar_overlay.py --help.
Requer PyYAML, kubectl com Kustomize, Terraform e, no pre-sync, Git e AWS CLI.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


SERVICOS = ("auth", "flag", "targeting", "evaluation", "analytics")


class Falha(Exception):
    """Mensagem de diagnóstico que pode aparecer no terminal sem expor valores."""


def executar(pasta, args):
    try:
        processo = subprocess.run(
            args, cwd=pasta, capture_output=True, encoding="utf-8",
            errors="replace", timeout=90, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as erro:
        raise Falha(f"{args[0]} indisponível ou tempo de consulta excedido.") from erro
    if processo.returncode:
        # stderr pode incluir uma URL com credenciais ou conteúdo de um manifesto.
        raise Falha(f"{args[0]} retornou código {processo.returncode}.")
    return processo.stdout.strip()


def output(pasta, nome):
    try:
        return json.loads(executar(pasta, ["terraform", "output", "-json", nome]))
    except (Falha, ValueError) as erro:
        raise Falha(f"Falha ao consultar o output {nome} em {pasta.name}.") from erro


def igual(obtido, esperado, campo):
    if not isinstance(esperado, str) or not esperado.strip():
        raise Falha(f"Valor de referência ausente em {campo}.")
    if any(item in esperado.lower() for item in (".invalid", "conta-pendente", "conta_aws_pendente")):
        raise Falha(f"O valor de referência de {campo} contém uma sentinela.")
    if obtido != esperado:
        raise Falha(f"Valor ausente ou divergente em {campo}.")


def conferir_render(documentos, fila, redis, roles, repositorios=None, sha=None):
    objetos = {}
    for recurso in documentos:
        if recurso and recurso.get("metadata", {}).get("namespace") == "togglemaster":
            chave = (recurso["kind"], recurso["metadata"]["name"])
            if chave in objetos:
                raise Falha(f"Objeto duplicado: {'/'.join(chave)}.")
            objetos[chave] = recurso

    def objeto(tipo, nome):
        if (tipo, nome) not in objetos:
            raise Falha(f"Ausente em togglemaster: {tipo}/{nome}.")
        return objetos[tipo, nome]

    imagens = []
    for servico in (SERVICOS if repositorios is not None else ("evaluation", "analytics")):
        nome = servico + "-service"
        pod = objeto("Deployment", nome)["spec"]["template"]["spec"]
        principais = [c for c in pod["containers"] if c["name"] == nome]
        if len(principais) != 1:
            raise Falha(f"Contêiner principal ausente ou duplicado em {nome}.")
        container = principais[0]
        if servico in ("evaluation", "analytics"):
            arn = objeto("ServiceAccount", nome)["metadata"].get("annotations", {}).get("eks.amazonaws.com/role-arn")
            igual(arn, roles.get(servico), f"{nome} / anotação IRSA")
            igual(pod.get("serviceAccountName"), nome, f"{nome} / ServiceAccount usada")
            # envFrom pode combinar vários ConfigMaps; o último valor vence.
            ambiente = {}
            for origem in container.get("envFrom", []):
                ref = origem.get("configMapRef")
                if not ref:
                    raise Falha(f"Origem envFrom não verificável em {nome}.")
                dados = objeto("ConfigMap", ref["name"]).get("data", {})
                ambiente.update({origem.get("prefix", "") + k: v for k, v in dados.items()})
            for entrada in container.get("env", []):
                # env explícito tem precedência; valueFrom não comprova o endpoint.
                ambiente[entrada["name"]] = entrada.get("value")
            igual(ambiente.get("AWS_SQS_URL"), fila, f"{nome} / AWS_SQS_URL")
            if servico == "evaluation":
                igual(ambiente.get("REDIS_URL"), redis, f"{nome} / REDIS_URL")
        if repositorios is not None:
            url = repositorios.get(servico, "")
            padrao = r"([0-9]{12})\.dkr\.ecr\.([a-z0-9-]+)\.amazonaws\.com/" + re.escape(nome)
            destino = re.fullmatch(padrao, url)
            if not destino:
                raise Falha(f"Output ECR inválido para {nome}.")
            tag = "v1.0.0-" + sha[:7]
            igual(container.get("image"), url + ":" + tag, f"{nome} / imagem do merge")
            imagens.append((destino[1], destino[2], nome, tag))
    return imagens


def conferir_checkout(checkout):
    if executar(checkout, ["git", "--no-optional-locks", "status", "--porcelain", "--untracked-files=all", "--", "gitops"]):
        raise Falha("O checkout tem mudanças locais em gitops.")
    atual = executar(checkout, ["git", "rev-parse", "HEAD"])
    remoto = executar(checkout, ["git", "ls-remote", "--exit-code", "origin", "refs/heads/main"]).split()
    if remoto != [atual, "refs/heads/main"]:
        raise Falha("HEAD do checkout diverge da main remota. Atualize a cópia e confira novamente.")
    return atual


def conferir_tags(checkout, imagens):
    for conta, regiao, nome, tag in imagens:
        try:
            resultado = executar(checkout, [
                "aws", "ecr", "describe-images", "--region", regiao, "--registry-id", conta,
                "--repository-name", nome, "--image-ids", "imageTag=" + tag, "--no-cli-pager",
                "--query", "imageDetails[].{tags:imageTags,digest:imageDigest}", "--output", "json",
            ])
            linhas = json.loads(resultado)
            if len(linhas) == 1 and tag in linhas[0]["tags"] and re.fullmatch(r"sha256:[0-9a-f]{64}", linhas[0]["digest"]):
                continue
        except (Falha, KeyError, TypeError, ValueError):
            pass
        raise Falha(f"A existência da tag esperada no ECR não foi confirmada para {nome}.")


def principal():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("etapa", choices=("pre-pr", "pre-sync"))
    cli.add_argument("--checkout", type=Path, default=Path.cwd(),
                     help="Raiz da cópia Git a renderizar. Padrão: pasta atual.")
    cli.add_argument("--terraform-dir", type=Path, default=Path.cwd() / "terraform",
                     help="Pasta da base Terraform inicializada para a Fase 4 na conta de destino.")
    cli.add_argument("--sha-publicacao", help="SHA completo do merge que disparou os cinco pipelines do B3.")
    args = cli.parse_args()
    sync = args.etapa == "pre-sync"
    if sync and not re.fullmatch(r"[0-9a-f]{40}", args.sha_publicacao or ""):
        cli.error("pre-sync requer --sha-publicacao com os 40 caracteres do commit de publicação.")
    checkout = args.checkout.resolve()
    base = args.terraform_dir.resolve()
    cluster = base / "cluster"
    if sync:
        inicio = conferir_checkout(checkout)
        try:
            executar(checkout, ["git", "merge-base", "--is-ancestor", args.sha_publicacao, "HEAD"])
        except Falha as erro:
            raise Falha("O commit de publicação não foi confirmado no histórico do checkout.") from erro
    render = executar(checkout, ["kubectl", "kustomize", "gitops/overlays/prod"])
    imagens = conferir_render(
        yaml.safe_load_all(render), output(base, "sqs_queue_url"), output(cluster, "redis_url"),
        output(cluster, "irsa_role_arns"), output(base, "ecr_repository_urls") if sync else None,
        args.sha_publicacao,
    )
    if sync:
        conferir_tags(checkout, imagens)
        if conferir_checkout(checkout) != inicio:
            raise Falha("A main mudou durante a verificação. Confira novamente.")
    print("OK: SQS, Redis e as duas identidades IRSA conferidos no render de produção.")
    if sync:
        print("OK: cinco Deployments com as tags do merge no ECR e checkout igual à main remota.")


if __name__ == "__main__":
    try:
        principal()
    except Falha as erro:
        sys.exit(f"FALHA: {erro}")
    except (AttributeError, KeyError, TypeError, ValueError, yaml.YAMLError):
        sys.exit("FALHA: estrutura inesperada no manifesto ou no output consultado.")
