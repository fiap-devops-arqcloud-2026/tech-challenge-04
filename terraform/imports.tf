# ============================================================
# IMPORTS - recursos que ja existem na conta nova (Fase 4)
# ============================================================
# Na preparacao da conta nova, os 5 repositorios ECR, a role do CI e a
# policy de push foram criados A MAO no console, para o GitHub Actions
# poder publicar imagens antes do primeiro apply. O estado desta camada
# comeca vazio, entao sem os blocos abaixo o apply tentaria criar tudo de
# novo, falharia com AlreadyExists no meio do caminho e deixaria VPC e NAT
# criados num estado parcial.
#
# Um bloco `import` diz ao Terraform: "este recurso ja existe com este
# ID; adote-o no estado em vez de cria-lo". O plan mostra "will be
# imported" e, depois do primeiro apply, o recurso passa a ser gerenciado
# como qualquer outro. Rodar o plan de novo nao reimporta nada.
#
# CRITERIO DE ACEITE DO PRIMEIRO PLAN: "N to import" e 0 to destroy, sem
# nenhum "must be replaced". Diferencas "~ update in-place" sao esperadas
# (tags padrao, descricao da role) e nao recriam nada.
#
# O provedor OIDC NAO entra aqui: ele ja existia na conta e fica fora do
# Terraform com create_github_oidc_provider = false (data source em
# modules/iam-ci).
#
# LIGA/DESLIGA: var.import_manual_resources. Com false, os for_each
# abaixo ficam vazios e nenhum import acontece - o caso de uma conta sem
# recursos manuais ou de um estado que ja os contem. Depois de um
# destroy, os recursos deixam de existir e a variavel deve voltar a
# false; senao o plan falha com "Cannot import non-existent remote
# object".
#
# Testado em 2026-11-03 com Terraform 1.16 (diretorio temporario, provider
# random): for_each vazio cria em vez de importar, e um conjunto de um
# elemento importa um recurso sem chave de instancia.
# ============================================================

locals {
  # Um conjunto de um elemento liga os imports de recursos sem for_each
  # (role, policy, anexo); o conjunto vazio desliga.
  import_iam_ci = var.import_manual_resources ? toset(["ci"]) : toset([])

  # Mesmas chaves do for_each do modulo ecr ("auth", "flag"...), para o
  # endereco module.ecr.aws_ecr_repository.this["auth"] casar.
  import_ecr = var.import_manual_resources ? toset(var.services) : toset([])

  # ARN da policy criada no console. Montada a partir do ID da conta que
  # o provider ja exige (allowed_account_ids), para nenhum numero de
  # conta ficar escrito em arquivo versionado.
  ci_policy_arn = "arn:aws:iam::${var.expected_aws_account_id}:policy/${var.project_name}-ci-ecr-push"
}

# Os 5 repositorios ECR. O ID de importacao e o nome do repositorio.
import {
  for_each = local.import_ecr
  to       = module.ecr.aws_ecr_repository.this[each.key]
  id       = "${each.key}-service"
}

# Role assumida pelo CI via OIDC. O ID e o nome da role.
import {
  for_each = local.import_iam_ci
  to       = module.iam_ci.aws_iam_role.github_actions
  id       = "${var.project_name}-github-actions"
}

# Policy de push no ECR. O ID e o ARN.
import {
  for_each = local.import_iam_ci
  to       = module.iam_ci.aws_iam_policy.ecr_push
  id       = local.ci_policy_arn
}

# Anexo da policy na role. O ID e "<nome-da-role>/<arn-da-policy>".
import {
  for_each = local.import_iam_ci
  to       = module.iam_ci.aws_iam_role_policy_attachment.ecr_push
  id       = "${var.project_name}-github-actions/${local.ci_policy_arn}"
}
