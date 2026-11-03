variables {
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
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main"
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
    condition = jsondecode(data.aws_iam_policy_document.trust.json).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main"
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
run "reject_owner_wildcard" {
  command = plan
  variables { github_repository_owner_id = "*" }
  expect_failures = [var.github_repository_owner_id]
}
run "reject_repo_id_wildcard" {
  command = plan
  variables { github_repository_id = "*" }
  expect_failures = [var.github_repository_id]
}
run "reject_repo_name_wildcard" {
  command = plan
  variables { github_repository = "fiap-devops-arqcloud-2026/*" }
  expect_failures = [var.github_repository]
}
run "reject_branch_wildcard" {
  command = plan
  variables { github_deploy_branch = "*" }
  expect_failures = [var.github_deploy_branch]
}
run "reject_context_injection" {
  command = plan
  variables { github_deploy_branch = "main:environment:prod" }
  expect_failures = [var.github_deploy_branch]
}
