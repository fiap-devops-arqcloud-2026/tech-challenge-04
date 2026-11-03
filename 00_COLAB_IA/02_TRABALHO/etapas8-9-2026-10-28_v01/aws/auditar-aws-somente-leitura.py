"""Etapa 8: consultas AWS delimitadas, sem credenciais ou mutacoes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import json
import os
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PROFILE = "default"
SERVICES = ["auth", "flag", "targeting", "evaluation", "analytics"]


def call(args, query=None):
    command = ["aws", "--profile", PROFILE, "--no-cli-pager", "--cli-connect-timeout", "10", "--cli-read-timeout", "20"] + args
    if query:
        command += ["--query", query]
    command += ["--output", "json"]
    try:
        process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
        result = {"command": command, "exit_code": process.returncode}
        if process.returncode:
            result["error"] = process.stderr.strip()[:1800]
        else:
            result["data"] = json.loads(process.stdout)
        return result
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        return {"command": command, "exit_code": None, "error_type": type(error).__name__}


def canonical_policy(value):
    """Ignore statement IDs/list order and AWS scalar-vs-single-list formatting."""
    if isinstance(value, dict):
        return {key: canonical_policy(item) for key, item in sorted(value.items()) if key != "Sid"}
    if isinstance(value, list):
        items = [canonical_policy(item) for item in value]
        if len(items) == 1:
            return items[0]
        return sorted(items, key=lambda item: json.dumps(item, sort_keys=True))
    return value


now = datetime.now().astimezone().isoformat(timespec="seconds")
identity = call(["sts", "get-caller-identity"])
if identity["exit_code"] != 0:
    raise RuntimeError("STS nao validado; inventario interrompido sem operacoes adicionais")
account = identity["data"]["Account"]
caller = identity["data"]["Arn"]
kind = "root" if caller.endswith(":root") else "assumed-role" if ":assumed-role/" in caller else "user" if ":user/" in caller else "other"
identity["data"] = {"Account": account, "identity_type": kind, "ArnSanitized": f"arn:aws:iam::{account}:{kind}" + ("" if kind == "root" else "/REDACTED")}
region_process = subprocess.run(["aws", "configure", "get", "region", "--profile", PROFILE], capture_output=True, text=True, timeout=15)
configured_region = region_process.stdout.strip()
region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or configured_region
if region != "us-east-2":
    raise RuntimeError("Regiao difere da regiao esperada; confirmar antes de ampliar consultas")
policy_arn = f"arn:aws:iam::{account}:policy/togglemaster-ci-ecr-push"
provider_arn = f"arn:aws:iam::{account}:oidc-provider/token.actions.githubusercontent.com"
requests = {
    "role": (["iam", "get-role", "--role-name", "togglemaster-github-actions"], "Role.{Arn:Arn,RoleName:RoleName,CreateDate:CreateDate,AssumeRolePolicyDocument:AssumeRolePolicyDocument,PermissionsBoundary:PermissionsBoundary,MaxSessionDuration:MaxSessionDuration}"),
    "attached_policies": (["iam", "list-attached-role-policies", "--role-name", "togglemaster-github-actions"], None),
    "inline_policies": (["iam", "list-role-policies", "--role-name", "togglemaster-github-actions"], None),
    "policy": (["iam", "get-policy", "--policy-arn", policy_arn], "Policy.{Arn:Arn,PolicyName:PolicyName,DefaultVersionId:DefaultVersionId,AttachmentCount:AttachmentCount,PermissionsBoundaryUsageCount:PermissionsBoundaryUsageCount,IsAttachable:IsAttachable}"),
    "oidc_provider": (["iam", "get-open-id-connect-provider", "--open-id-connect-provider-arn", provider_arn], "{Url:Url,ClientIDList:ClientIDList,ThumbprintList:ThumbprintList,CreateDate:CreateDate}"),
    "registry_scanning": (["ecr", "get-registry-scanning-configuration", "--region", region], None),
}
for service in SERVICES:
    name = service + "-service"
    requests[f"ecr_{service}"] = (["ecr", "describe-repositories", "--region", region, "--repository-names", name], "repositories[].{repositoryArn:repositoryArn,registryId:registryId,repositoryName:repositoryName,repositoryUri:repositoryUri,createdAt:createdAt,imageTagMutability:imageTagMutability,imageScanningConfiguration:imageScanningConfiguration,encryptionConfiguration:encryptionConfiguration,imageTagMutabilityExclusionFilters:imageTagMutabilityExclusionFilters}")
    requests[f"lifecycle_{service}"] = (["ecr", "get-lifecycle-policy", "--region", region, "--repository-name", name], None)
with ThreadPoolExecutor(max_workers=6) as pool:
    futures = {key: pool.submit(call, args, query) for key, (args, query) in requests.items()}
    responses = {key: future.result() for key, future in futures.items()}
if responses["policy"]["exit_code"] == 0:
    version = responses["policy"]["data"]["DefaultVersionId"]
    responses["policy_version"] = call(["iam", "get-policy-version", "--policy-arn", policy_arn, "--version-id", version], "PolicyVersion")
for key, response in responses.items():
    if key.startswith("lifecycle_") and response["exit_code"] == 0:
        response["data"]["lifecyclePolicy"] = json.loads(response["data"].pop("lifecyclePolicyText"))

template_dir = ROOT / "00_COLAB_IA" / "02_TRABALHO" / "role-github-oidc-2026-10-28_v01"
expected_trust = json.loads((template_dir / "trust-policy_TEMPLATE.json").read_text(encoding="utf-8").replace("SUBSTITUA_ID_AWS", account))
expected_permissions = json.loads((template_dir / "ecr-permissions_TEMPLATE.json").read_text(encoding="utf-8").replace("SUBSTITUA_ID_AWS", account))
def data(name):
    return responses[name].get("data")

checks = {
    "identity_account": account,
    "region": region,
    "role_found": responses["role"]["exit_code"] == 0,
    "role_arn_expected": data("role") is not None and data("role")["Arn"] == f"arn:aws:iam::{account}:role/togglemaster-github-actions",
    "trust_matches_template": data("role") is not None and canonical_policy(data("role")["AssumeRolePolicyDocument"]) == canonical_policy(expected_trust),
    "only_expected_managed_policy_attached": data("attached_policies") is not None and data("attached_policies")["AttachedPolicies"] == [{"PolicyName": "togglemaster-ci-ecr-push", "PolicyArn": policy_arn}],
    "no_inline_policies": data("inline_policies") is not None and data("inline_policies")["PolicyNames"] == [],
    "permissions_boundary_absent": data("role") is not None and data("role").get("PermissionsBoundary") is None,
    "permissions_match_template": responses.get("policy_version", {}).get("data") is not None and canonical_policy(responses["policy_version"]["data"]["Document"]) == canonical_policy(expected_permissions),
    "provider_url_correct": data("oidc_provider") is not None and data("oidc_provider")["Url"] == "token.actions.githubusercontent.com",
    "provider_audience_exact": data("oidc_provider") is not None and data("oidc_provider")["ClientIDList"] == ["sts.amazonaws.com"],
}
ecr_checks = []
for service in SERVICES:
    response = responses[f"ecr_{service}"]
    repo = response.get("data", [None])[0] if response.get("data") else None
    lifecycle = responses[f"lifecycle_{service}"]
    expected_name = service + "-service"
    ecr_checks.append({"service": service, "exists": repo is not None, "expected_arn": f"arn:aws:ecr:{region}:{account}:repository/{expected_name}", "uri_matches": repo is not None and repo["repositoryUri"] == f"{account}.dkr.ecr.{region}.amazonaws.com/{expected_name}", "mutable": repo is not None and repo["imageTagMutability"] == "MUTABLE", "aes256": repo is not None and repo["encryptionConfiguration"]["encryptionType"] == "AES256", "repository_scan_on_push": repo is not None and repo["imageScanningConfiguration"]["scanOnPush"], "lifecycle_policy_exists": lifecycle["exit_code"] == 0, "lifecycle_error": lifecycle.get("error")})

evidence = {"collected_at": now, "scope": "AWS somente leitura; sem credenciais, alteracoes, billing, plan/apply/import ou teste de federacao", "profile": PROFILE, "configured_region": configured_region, "effective_region": region, "identity": identity, "responses": responses, "checks": checks, "ecr_checks": ecr_checks, "limitations": ["Consultas IAM/ECR nao comprovam autenticacao OIDC real pelo GitHub Actions.", "Creditos, Billing, SCPs, quotas e infraestrutura fora do escopo nao foram consultados.", "Nome e identificador do usuario IAM sanitizados; nenhum arquivo de credenciais lido diretamente.", "Tags e campos nao explicitamente projetados nas consultas nao foram auditados; parecer nao e auditoria exaustiva da conta."]}
tf_source = (ROOT / "terraform" / "modules" / "iam-ci" / "main.tf").read_text(encoding="utf-8")
tf_thumbprints = re.search(r"thumbprint_list\s*=\s*\[(.*?)\]", tf_source, re.S)
declared_thumbprints = re.findall(r'"([a-f0-9]{40})"', tf_thumbprints.group(1)) if tf_thumbprints else None
actual_thumbprints = data("oidc_provider").get("ThumbprintList") if data("oidc_provider") else None
evidence["declarative_differences"] = {"oidc_thumbprints": {"aws": actual_thumbprints, "terraform": declared_thumbprints, "equal": set(actual_thumbprints) == set(declared_thumbprints) if actual_thumbprints is not None and declared_thumbprints is not None else None, "interpretation": "Diferenca declarativa a revisar na importacao ou reutilizacao. Nao comprova falha de autenticacao; AWS valida cadeia de CA em casos aplicaveis."}}
(OUT / "inventario-aws-sanitizado.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"collected_at": now, "account": account, "region": region, "checks": checks, "ecr_checks": ecr_checks, "failed_requests": {k: v.get("error", v.get("error_type")) for k, v in responses.items() if v["exit_code"] != 0}}, ensure_ascii=False))
