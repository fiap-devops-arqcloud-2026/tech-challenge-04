"""Prova local da trust: provider real gera JSON; somente I/O OIDC substituido.

Executa terraform test com command=plan em copia isolada do modulo; nunca
executa apply, importa estado ou usa credenciais reais. Terraform/AWS pinados
pelo lockfile do projeto e provider obtido do cache local, sem backend S3.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[4]
QA = Path(__file__).resolve().parent
HARNESS = QA / "harness"
HARNESS.mkdir(exist_ok=True)
(HARNESS / "tests").mkdir(exist_ok=True)
for source in (REPO / "terraform/modules/iam-ci").glob("*.tf"):
    shutil.copy2(source, HARNESS / source.name)
shutil.copy2(REPO / "terraform/.terraform.lock.hcl", HARNESS / ".terraform.lock.hcl")

(HARNESS / "offline-test.tf").write_text('''terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.46.0"
    }
  }
}
provider "aws" {
  region                      = "us-east-2"
  access_key                  = "offline-test"
  secret_key                  = "offline-test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  endpoints {
    iam = "http://127.0.0.1:9"
    sts = "http://127.0.0.1:9"
  }
}
output "trust_document_test" {
  value = data.aws_iam_policy_document.trust.json
}
''', encoding="utf-8")

expected = "repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main"
test = '''variables {
  project_name               = "offline-test"
  github_repository          = "fiap-devops-arqcloud-2026/tech-challenge-04"
  github_repository_owner_id = "287716251"
  github_repository_id       = "1373159817"
  github_deploy_branch       = "main"
  ecr_repository_arns        = ["arn:aws:ecr:us-east-2:000000000000:repository/auth-service"]
}
override_resource {
  target          = aws_iam_openid_connect_provider.github
  override_during = plan
  values = {
    arn = "arn:aws:iam::000000000000:oidc-provider/token.actions.githubusercontent.com"
  }
}
override_data {
  target = data.aws_iam_openid_connect_provider.github
  values = {
    arn = "arn:aws:iam::000000000000:oidc-provider/token.actions.githubusercontent.com"
  }
}
run "create_provider_main" {
  command = plan
  assert {
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "EXPECTED_SUBJECT"
    error_message = "A trust deve aceitar exatamente o subject main confirmado, com os dois IDs."
  }
  assert {
    condition = length(jsondecode(data.aws_iam_policy_document.trust.json).Statement) == 1 && length(keys(jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition)) == 1
    error_message = "A trust nao deve adicionar outro statement ou operador que amplie a autorizacao."
  }
  assert {
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:aud"] == "sts.amazonaws.com"
    error_message = "Audience deve corresponder ao STS."
  }
}
run "reuse_provider_main" {
  command = plan
  variables { create_oidc_provider = false }
  assert {
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "EXPECTED_SUBJECT"
    error_message = "Reutilizar o provedor nao deve mudar a trust main."
  }
}
run "different_repository_is_parameterized" {
  command = plan
  variables {
    github_repository          = "another-org/another-repo"
    github_repository_owner_id = "12345"
    github_repository_id       = "67890"
    github_deploy_branch       = "release/v1"
  }
  assert {
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:another-org@12345/another-repo@67890:ref:refs/heads/release/v1"
    error_message = "O modulo nao pode fixar os nomes ou IDs da Fase4 internamente."
  }
}
'''.replace("EXPECTED_SUBJECT", expected)
for name, field, value in [
    ("reject_owner_wildcard", "github_repository_owner_id", "*"),
    ("reject_repo_id_wildcard", "github_repository_id", "*"),
    ("reject_repo_name_wildcard", "github_repository", "fiap-devops-arqcloud-2026/*"),
    ("reject_branch_wildcard", "github_deploy_branch", "*"),
    ("reject_context_injection", "github_deploy_branch", "main:environment:prod"),
]:
    test += f'''run "{name}" {{
  command = plan
  variables {{ {field} = "{value}" }}
  expect_failures = [var.{field}]
}}
'''
(HARNESS / "tests/trust.tftest.hcl").write_text(test, encoding="utf-8")

env = {k: v for k, v in os.environ.items() if not k.startswith(("AWS_", "TF_VAR_", "TF_CLI_ARGS"))}
env.update({"AWS_EC2_METADATA_DISABLED": "true", "AWS_ACCESS_KEY_ID": "offline-test", "AWS_SECRET_ACCESS_KEY": "offline-test", "CHECKPOINT_DISABLE": "1", "TF_IN_AUTOMATION": "true", "TF_INPUT": "false"})
empty = QA / "empty-aws-config"
empty.write_text("", encoding="utf-8")
env["AWS_CONFIG_FILE"] = str(empty)
env["AWS_SHARED_CREDENTIALS_FILE"] = str(empty)
tf = shutil.which("terraform")
assert tf, "Terraform nao encontrado"

def run(args, logfile):
    cp = subprocess.run([tf, f"-chdir={HARNESS}", *args], env=env, text=True, encoding="utf-8", errors="replace", capture_output=True)
    (QA / logfile).write_text(cp.stdout + cp.stderr, encoding="utf-8")
    return cp

cp = run(["init", "-backend=false", "-input=false", "-lockfile=readonly", f"-plugin-dir={REPO / 'terraform/.terraform/providers'}", "-no-color"], "offline-init.txt")
assert cp.returncode == 0, cp.stdout + cp.stderr
cp = run(["test", "-json", "-verbose", "-no-color"], "offline-test.jsonl")
print(json.dumps({"exit_code": cp.returncode, "evidence": str(QA / 'offline-test.jsonl')}))
if cp.returncode != 0:
    print(cp.stdout[-16000:] + cp.stderr)
raise SystemExit(cp.returncode)
