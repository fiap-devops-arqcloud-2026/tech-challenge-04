# ============================================================
# ENTRADAS DO MODULO IAM-CI
# ============================================================

variable "project_name" {
  description = "Prefixo do nome da role e da policy."
  type        = string
}

variable "github_repository" {
  description = "Repositorio autorizado a assumir a role, no formato owner/repo."
  type        = string
  nullable    = false
  # Sem default de proposito: um valor errado aqui abriria a role para
  # outro repositorio. Melhor obrigar quem chama a declarar.

  validation {
    condition     = can(regex("^[A-Za-z0-9-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "github_repository deve ser owner/repo, sem curingas nem contexto OIDC."
  }
}

variable "github_repository_owner_id" {
  description = "ID numerico imutavel do proprietario do repositorio GitHub."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[1-9][0-9]*$", var.github_repository_owner_id))
    error_message = "github_repository_owner_id deve ser um ID numerico positivo do GitHub."
  }
}

variable "github_repository_id" {
  description = "ID numerico imutavel do repositorio GitHub."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[1-9][0-9]*$", var.github_repository_id))
    error_message = "github_repository_id deve ser um ID numerico positivo do GitHub."
  }
}

variable "github_deploy_branch" {
  description = "Branch exata autorizada a publicar no ECR; deve acompanhar o gate do CI."
  type        = string
  nullable    = false
  default     = "main"

  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9._/-]*$", var.github_deploy_branch))
    error_message = "github_deploy_branch deve ser um nome de branch explicito, sem curingas, dois-pontos ou espacos."
  }
}

variable "ecr_repository_arns" {
  description = "ARNs dos repositorios ECR aos quais o CI pode enviar imagens."
  type        = list(string)
  # Recebido de module.ecr.repository_arns em main.tf. E o que garante que a
  # permissao acompanhe automaticamente os repositorios que existem de fato.
}

variable "create_oidc_provider" {
  description = "true cria o provedor OIDC do GitHub nesta conta; false reaproveita um provedor que ja existe. A AWS aceita um unico provedor por endereco, entao true falha com EntityAlreadyExists se outro projeto ja o criou."
  type        = bool
  # true preserva o comportamento original para quem aplica o projeto
  # numa conta nova, sem nenhum outro uso de OIDC do GitHub.
  default = true
}

variable "eks_cluster_arn" {
  description = "ARN do cluster EKS do projeto. Unico recurso em que a role do self-healing pode chamar eks:DescribeCluster."
  type        = string
}
