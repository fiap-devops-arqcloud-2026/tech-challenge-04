# ============================================================
# TESTE DO MODULO IAM-CI - quem pode assumir as roles via OIDC
# ============================================================
# A politica de confianca (trust) e a parte mais sensivel deste modulo:
# um curinga no lugar errado deixaria QUALQUER repositorio do GitHub
# assumir as roles da conta. Este arquivo prova, a cada alteracao, que:
#
#   1. a trust aceita exatamente o subject da branch main deste
#      repositorio, com os IDs imutaveis do dono e do repositorio;
#   2. curingas e "injecao de contexto" sao recusados na entrada, antes
#      de virarem policy;
#   3. a role do self-healing usa a mesma trust e so pode descrever o
#      cluster do projeto;
#   4. a role do CI so publica nos repositorios ECR recebidos.
#
# COMO RODA SEM AWS
# Todos os "run" usam `command = plan`: nada e criado. O provider abaixo
# usa credenciais falsas e aponta IAM e STS para 127.0.0.1:9, uma porta
# que recusa conexao. Se algum recurso tentasse falar com a AWS, o teste
# falharia na hora, em vez de tocar em uma conta real. O unico dado que
# consultaria a AWS (o provedor OIDC existente) e substituido por um
# valor fixo com override_data.
#
# COMO RODAR
#   terraform -chdir=terraform/modules/iam-ci init -backend=false
#   terraform -chdir=terraform/modules/iam-ci test
# O workflow Terraform Check roda os mesmos comandos a cada alteracao.
# ============================================================

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

# Valores do repositorio real. Os IDs nao sao segredo: aparecem na API
# publica do GitHub e no proprio token OIDC.
variables {
  project_name               = "offline-test"
  github_repository          = "fiap-devops-arqcloud-2026/tech-challenge-04"
  github_repository_owner_id = "287716251"
  github_repository_id       = "1373159817"
  github_deploy_branch       = "main"
  ecr_repository_arns        = ["arn:aws:ecr:us-east-2:000000000000:repository/auth-service"]
  eks_cluster_arn            = "arn:aws:eks:us-east-2:000000000000:cluster/togglemaster"
}

# ARN ficticio do provedor OIDC, nos dois modos do modulo: criado aqui
# (recurso) ou reaproveitado da conta (data source).
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

# ------------------------------------------------------------
# 1. A trust aceita exatamente o subject da main
# ------------------------------------------------------------

run "create_provider_main" {
  command = plan

  assert {
    condition     = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main"
    error_message = "A trust deve aceitar exatamente o subject da main, com os dois IDs imutaveis."
  }

  assert {
    condition     = length(jsondecode(data.aws_iam_policy_document.trust.json).Statement) == 1 && length(keys(jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition)) == 1
    error_message = "A trust nao deve ganhar outro statement nem outro operador (como StringLike) que amplie a autorizacao."
  }

  assert {
    condition     = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:aud"] == "sts.amazonaws.com"
    error_message = "O audience deve ser o STS, o valor usado pela action configure-aws-credentials."
  }
}

run "reuse_provider_main" {
  command = plan

  variables {
    create_oidc_provider = false
  }

  assert {
    condition     = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main"
    error_message = "Reaproveitar o provedor OIDC da conta nao deve mudar a trust da main."
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
    condition     = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:another-org@12345/another-repo@67890:ref:refs/heads/release/v1"
    error_message = "O modulo nao pode fixar internamente os nomes ou IDs deste repositorio."
  }
}

# ------------------------------------------------------------
# 2. Entradas perigosas sao recusadas pelas validations
# ------------------------------------------------------------
# expect_failures inverte a logica: o run passa SOMENTE se a validation
# da variavel indicada reprovar o valor.

run "reject_owner_wildcard" {
  command = plan

  variables {
    github_repository_owner_id = "*"
  }

  expect_failures = [var.github_repository_owner_id]
}

run "reject_repo_id_wildcard" {
  command = plan

  variables {
    github_repository_id = "*"
  }

  expect_failures = [var.github_repository_id]
}

run "reject_repo_name_wildcard" {
  command = plan

  variables {
    github_repository = "fiap-devops-arqcloud-2026/*"
  }

  expect_failures = [var.github_repository]
}

run "reject_branch_wildcard" {
  command = plan

  variables {
    github_deploy_branch = "*"
  }

  expect_failures = [var.github_deploy_branch]
}

# O sufixo ":environment:prod" tentaria encaixar outro contexto do token
# dentro do subject. Dois-pontos nao sao aceitos no nome da branch.
run "reject_context_injection" {
  command = plan

  variables {
    github_deploy_branch = "main:environment:prod"
  }

  expect_failures = [var.github_deploy_branch]
}

# ------------------------------------------------------------
# 3. Self-healing: mesma trust, permissao minima no cluster
# ------------------------------------------------------------

run "self_healing_shares_trust_and_minimal_policy" {
  command = plan

  # jsondecode compara o conteudo, e nao o texto: o provider AWS
  # normaliza o JSON da role (espacos e ordem), e a comparacao de texto
  # reprovaria duas policies identicas.
  assert {
    condition     = jsondecode(aws_iam_role.self_healing.assume_role_policy) == jsondecode(data.aws_iam_policy_document.trust.json) && jsondecode(aws_iam_role.github_actions.assume_role_policy) == jsondecode(data.aws_iam_policy_document.trust.json)
    error_message = "As duas roles (CI e self-healing) devem usar a mesma trust da main."
  }

  assert {
    condition     = length(jsondecode(data.aws_iam_policy_document.self_healing.json).Statement) == 1
    error_message = "A policy do self-healing deve ter um unico statement."
  }

  assert {
    condition     = flatten([jsondecode(data.aws_iam_policy_document.self_healing.json).Statement[0].Action]) == ["eks:DescribeCluster"]
    error_message = "O self-healing so pode chamar eks:DescribeCluster na AWS; o que ele faz dentro do cluster vem do RBAC."
  }

  assert {
    condition     = flatten([jsondecode(data.aws_iam_policy_document.self_healing.json).Statement[0].Resource]) == [var.eks_cluster_arn]
    error_message = "O self-healing so pode descrever o cluster do projeto."
  }
}

# ------------------------------------------------------------
# 4. CI: publica somente nos repositorios ECR recebidos
# ------------------------------------------------------------

run "ci_policy_scoped_to_project_repositories" {
  command = plan

  variables {
    ecr_repository_arns = [
      "arn:aws:ecr:us-east-2:000000000000:repository/auth-service",
      "arn:aws:ecr:us-east-2:000000000000:repository/flag-service",
    ]
  }

  assert {
    condition     = toset(flatten([[for s in jsondecode(data.aws_iam_policy_document.ecr_push.json).Statement : s.Resource if s.Sid == "EcrPushPull"]])) == toset(var.ecr_repository_arns)
    error_message = "O push no ECR deve valer somente para os repositorios recebidos."
  }

  assert {
    condition     = alltrue([for s in jsondecode(data.aws_iam_policy_document.ecr_push.json).Statement : alltrue([for a in flatten([s.Action]) : !strcontains(a, "*")])])
    error_message = "Nenhuma acao pode usar curinga (como ecr:*)."
  }

  # GetAuthorizationToken e a unica acao que a AWS exige com recurso "*".
  assert {
    condition     = alltrue([for s in jsondecode(data.aws_iam_policy_document.ecr_push.json).Statement : s.Sid == "EcrAuthToken" || !contains(flatten([s.Resource]), "*")])
    error_message = "Somente o statement EcrAuthToken pode usar recurso \"*\"."
  }
}
