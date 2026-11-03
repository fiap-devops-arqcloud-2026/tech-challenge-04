# ============================================================
# VARIAVEIS DE ENTRADA
# ============================================================
# A conta de destino precisa ser informada; nao existe default de conta.
# O terraform.tfvars.example existe para deixar explicito o que da para
# ajustar - principalmente o enable_nat_gateway, que mexe no custo.
# ============================================================

# ------------------------------------------------------------
# Identidade do projeto
# ------------------------------------------------------------

variable "aws_region" {
  # `description` aparece no terraform plan e na documentacao gerada.
  description = "Regiao AWS da Fase 4. Confirmar disponibilidade e cotas da nova conta antes de implantar."

  # Tipo de dado esperado. O Terraform recusa qualquer outro valor.
  type = string

  # Valor usado quando ninguem informa nada.
  default = "us-east-2"
}

variable "expected_aws_account_id" {
  description = "ID confirmado da NOVA conta AWS da Fase 4. O provider recusa credenciais de outra conta."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[0-9]{12}$", var.expected_aws_account_id))
    error_message = "Informe o ID real da nova conta AWS, com 12 digitos."
  }
}

variable "project_name" {
  # Sintaxe <<-EOT: texto de varias linhas com a indentacao removida.
  description = <<-EOT
    Prefixo dos nomes de recurso. Mantido como "togglemaster" de proposito:
    a fila e o cache da Fase 2 ja usavam esse prefixo, e o codigo dos servicos
    le esses nomes por variavel de ambiente (F-019). Mudar aqui obriga a mudar
    tambem os manifestos em gitops/.
  EOT
  type        = string
  default     = "togglemaster"
}

variable "default_tags" {
  description = "Tags aplicadas a todo recurso criado por este Terraform (D-009)."

  # map(string) = dicionario de chave/valor, ambos texto.
  type = map(string)

  # ATENCAO: chave de tag na AWS e sensivel a maiuscula/minuscula.
  # Manter em minusculo tambem no futuro bootstrap do bucket da Fase 4.
  # Ainda nao ha bucket confirmado na conta de destino.
  default = {
    project = "fiap"
    phase   = "4"
  }
}

# ------------------------------------------------------------
# Rede
# ------------------------------------------------------------

variable "vpc_cidr" {
  description = "Bloco CIDR da VPC. /16 da 65.536 enderecos, folga de sobra para as 4 subnets."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = <<-EOT
    Duas AZs, no minimo. Nao e escolha estetica: o EKS exige subnets em pelo
    menos duas zonas, e o DB subnet group do RDS tambem.
  EOT

  # list(string) = lista ordenada de textos.
  type    = list(string)
  default = ["us-east-2a", "us-east-2b"]
}

variable "private_subnet_cidrs" {
  description = "Subnets privadas: nos do EKS, RDS e ElastiCache. Nada aqui recebe IP publico."
  type        = list(string)

  # /24 = 256 enderecos por subnet. A ordem casa com availability_zones:
  # o primeiro CIDR vai para a primeira AZ, e assim por diante.
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "Subnets publicas: apenas o NAT Gateway. Nao ha Load Balancer no projeto (D-012)."
  type        = list(string)

  # Faixa .101 e .102 so para separar visualmente das privadas nos logs.
  default = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "enable_nat_gateway" {
  description = <<-EOT
    O NAT Gateway custa cerca de US$ 33/mes e so e necessario quando existe algo
    rodando em subnet privada, ou seja, a partir da Etapa 2 (EKS, RDS, Redis).
    Durante a Etapa 1 mantenha false no seu terraform.tfvars para nao pagar por
    um recurso ocioso. O padrao e true para nao deixar o cluster sem saida por
    esquecimento.
  EOT

  # bool = true ou false.
  type    = bool
  default = true
}

# ------------------------------------------------------------
# Aplicacao
# ------------------------------------------------------------

variable "services" {
  description = "Os 5 microsservicos do ToggleMaster. Cada item vira um repositorio ECR <servico>-service."
  type        = list(string)

  # Nomes curtos. O sufixo "-service" e adicionado dentro do modulo de ECR,
  # para bater com o que os deployments da Fase 2 ja referenciam (F-019).
  default = ["auth", "flag", "targeting", "evaluation", "analytics"]
}

variable "dynamodb_table_name" {
  description = "Nome literal exigido pelo enunciado (F-009). Nao alterar."
  type        = string

  # O enunciado cita o nome com estas maiusculas exatas. Mudar quebra o requisito.
  default = "ToggleMasterAnalytics"
}

variable "ecr_image_tag_mutability" {
  description = <<-EOT
    MUTABLE permite reenviar a mesma tag. IMMUTABLE e a opcao endurecida e
    combina com tags por commit hash, mas faz falhar qualquer re-execucao do
    workflow sobre o mesmo commit - situacao comum durante a gravacao do video.
    Comeca em MUTABLE; trocar para IMMUTABLE e uma linha.
  EOT
  type        = string
  default     = "MUTABLE"

  # Bloco validation: barra valores invalidos ainda no plan, com mensagem
  # clara, em vez de deixar a API da AWS recusar durante o apply.
  validation {
    # Condicao que precisa ser verdadeira para o valor ser aceito.
    condition = contains(["MUTABLE", "IMMUTABLE"], var.ecr_image_tag_mutability)

    # Mensagem exibida quando a condicao falha.
    error_message = "Use MUTABLE ou IMMUTABLE."
  }
}

variable "ecr_images_to_keep" {
  description = "Quantas imagens manter por repositorio. As mais antigas expiram para conter custo."

  # number = numerico.
  type = number

  # 10 e suficiente para voltar algumas versoes sem acumular lixo indefinidamente.
  default = 10
}

# ------------------------------------------------------------
# CI
# ------------------------------------------------------------

variable "github_repository" {
  description = <<-EOT
    Repositorio autorizado a assumir a role do CI via OIDC, no formato owner/repo.
    Qualquer outro repositorio recebe AccessDenied, mesmo dentro da mesma organizacao.
  EOT
  type        = string
  nullable    = false

  # Destino da importacao autorizada em 2026-10-20.
  default = "fiap-devops-arqcloud-2026/tech-challenge-04"

  validation {
    condition     = can(regex("^[A-Za-z0-9-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "github_repository deve ser owner/repo, sem curingas nem contexto OIDC."
  }
}

# IDs confirmados por GET autenticado do GitHub em 2026-10-28 (F-023).
# Nao sao credenciais. Ao reutilizar a base em outro repo, conferir ambos.
variable "github_repository_owner_id" {
  description = "ID numerico imutavel do proprietario do repositorio GitHub."
  type        = string
  nullable    = false
  default     = "287716251"

  validation {
    condition     = can(regex("^[1-9][0-9]*$", var.github_repository_owner_id))
    error_message = "github_repository_owner_id deve ser um ID numerico positivo do GitHub."
  }
}

variable "github_repository_id" {
  description = "ID numerico imutavel do repositorio GitHub."
  type        = string
  nullable    = false
  default     = "1373159817"

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

# ------------------------------------------------------------
# Provedor OIDC do GitHub: criar ou reaproveitar
# ------------------------------------------------------------
# A AWS permite UM provedor OIDC por endereco em cada conta. Numa conta
# nova, esta camada cria o provedor. Numa conta onde outro projeto ja o
# registrou, criar de novo falha no apply com EntityAlreadyExists - e ai
# o certo e reaproveitar, sem virar dono do recurso alheio.
#
# Para descobrir o seu caso, antes do apply:
#   aws iam list-open-id-connect-providers
# Se aparecer token.actions.githubusercontent.com, use false.
# ------------------------------------------------------------
variable "create_github_oidc_provider" {
  description = "true: esta camada cria o provedor OIDC do GitHub. false: reaproveita o provedor que ja existe na conta (obrigatorio quando outro projeto ja o criou)."
  type        = bool
  # true mantem o comportamento original em contas sem OIDC do GitHub.
  default = true
}
