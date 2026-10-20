# ============================================================
# VARIAVEIS DE ENTRADA - camada cluster
# ============================================================
# Repetem alguns valores da base de proposito: sao dois root modules
# independentes, e um nao le as variaveis do outro. Só o ESTADO e
# compartilhado, via remote state em data.tf.
# ============================================================

variable "aws_region" {
  description = "Regiao AWS. Precisa ser a mesma da camada base (F-012)."
  type        = string
  default     = "us-east-2"
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

variable "state_bucket" {
  description = "Bucket novo e exclusivo do estado da Fase 4; deve coincidir com backend.hcl. Nunca reutilizar o estado da Fase 3."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.state_bucket))
    error_message = "Informe o nome real do bucket S3 criado para a Fase 4."
  }
}

variable "state_region" {
  description = "Regiao do bucket de estado da Fase 4; deve coincidir com backend.hcl."
  type        = string
  nullable    = false
}

variable "base_state_key" {
  description = "Chave da base da Fase 4 no bucket de estado."
  type        = string
  default     = "phase4/prod/base.tfstate"
}

variable "project_name" {
  description = "Prefixo dos nomes de recurso. Mesmo valor da base."
  type        = string
  default     = "togglemaster"
}

variable "default_tags" {
  description = "Tags aplicadas a todo recurso (D-009). Em minusculas, igual a base."
  type        = map(string)
  default = {
    project = "fiap"
    phase   = "4"
  }
}

# ------------------------------------------------------------
# Cluster EKS
# ------------------------------------------------------------

variable "kubernetes_version" {
  description = <<-EOT
    Versao herdada da Fase 3. Antes da implantacao da Fase 4, confirmar
    disponibilidade da versao, suporte padrao e compatibilidade dos
    addons na regiao/conta novas. O default nao comprova elegibilidade
    nem representa orcamento ou consulta atual a AWS.
  EOT
  type        = string
  default     = "1.34"
}

variable "node_instance_type" {
  description = <<-EOT
    Tipo x86 herdado da Fase 3. As restricoes daquela conta nao provam
    as cotas/beneficios da nova; revalidar capacidade e custo antes de
    implantar. A stack de observabilidade da Fase 4 ainda exige sizing.
  EOT
  type        = string
  default     = "c7i-flex.large"
}

variable "node_group_min_size" {
  description = "Minimo de nos."
  type        = number
  default     = 1
}

variable "node_group_desired_size" {
  description = <<-EOT
    Nos desejados. 2 e nao 1 porque com um unico no o HPA do
    evaluation-service nao teria onde colocar o pod extra: ele ficaria
    Pending e a demonstracao de escalabilidade falharia no video.
  EOT
  type        = number
  default     = 2
}

variable "node_group_max_size" {
  description = "Maximo de nos, para o auto scaling do node group."
  type        = number
  default     = 4
}

# ------------------------------------------------------------
# Bancos de dados
# ------------------------------------------------------------

variable "rds_instance_class" {
  description = "Classe RDS herdada. Confirmar disponibilidade, cotas, custo e elegibilidade na nova conta."
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Armazenamento por instancia RDS, em GB. 20 e o minimo."
  type        = number
  default     = 20
}

variable "rds_databases" {
  description = <<-EOT
    Base importada: auth/flag no RDS e targeting_db no StatefulSet
    gitops/base/postgres-targeting/. A restricao e a aprovacao registradas
    na Fase 3 sao historicas; revalidar cotas e adequacao ao enunciado
    atual antes de definir a topologia final da Fase 4.
  EOT
  type        = map(string)
  default = {
    auth = "auth_db"
    flag = "flags_db"
  }
}

# ------------------------------------------------------------
# Cache
# ------------------------------------------------------------

variable "elasticache_node_type" {
  description = "Tipo do no do ElastiCache. cache.t3.micro e o menor disponivel."
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_transit_encryption" {
  description = <<-EOT
    Liga TLS na conexao com o ElastiCache.

    PADRAO false, e a escolha e deliberada. O evaluation-service monta o
    cliente com redis.ParseURL do go-redis/v8, que decide usar TLS pelo
    ESQUEMA da URL: "redis://" e texto claro, "rediss://" e TLS.

    Ligar aqui sem trocar o REDIS_URL em
    gitops/overlays/prod/patches/endpoints.yaml para rediss:// faz o
    servico morrer no boot: o codigo chama log.Fatalf quando a conexao
    inicial falha, o pod entra em CrashLoopBackOff e nao se recupera.

    Para ligar, nesta ordem: 1) trocar o esquema no patch do overlay;
    2) passar true aqui. Criptografia em transito NAO e item avaliado; a
    criptografia em repouso, essa sim, fica sempre ligada (S-05).
  EOT
  type        = bool
  default     = false
}
