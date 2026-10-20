# ============================================================
# LEITURA DOS ESTADOS ANTERIORES
# ============================================================
# Esta camada precisa de dados das DUAS anteriores:
#   - da base: a URL da fila SQS, que vai no ConfigMap;
#   - do cluster: endereco e certificado do EKS, endpoints do RDS e do
#     Redis, e as URLs de conexao com as senhas.
#
# Tudo por terraform_remote_state, que e SOMENTE LEITURA: nao altera o
# estado do outro lado nem cria dependencia de escrita.
# ============================================================

# ------------------------------------------------------------
# Estado da camada BASE (permanente)
# ------------------------------------------------------------
data "terraform_remote_state" "base" {
  backend = "s3"

  config = {
    bucket = var.state_bucket
    key    = var.base_state_key
    region = var.state_region
  }
}

# ------------------------------------------------------------
# Estado da camada CLUSTER (efemera)
# ------------------------------------------------------------
# Se o cluster nao tiver sido aplicado, este data source falha com
# "Unable to find remote state" - o que e o comportamento desejado:
# melhor falhar cedo e claro do que tentar criar Secret num cluster
# inexistente.
# ------------------------------------------------------------
data "terraform_remote_state" "cluster" {
  backend = "s3"

  config = {
    bucket = var.state_bucket
    key    = var.cluster_state_key
    region = var.state_region
  }
}

# ------------------------------------------------------------
# Atalhos, para nao repetir o caminho longo em cada uso
# ------------------------------------------------------------
locals {
  # --- da camada base ---

  # URL da fila. Vai para o ConfigMap de evaluation e analytics.
  sqs_queue_url = data.terraform_remote_state.base.outputs.sqs_queue_url

  # --- da camada cluster ---

  # Nome do cluster. Usado na autenticacao do provider (providers.tf).
  cluster_name = data.terraform_remote_state.cluster.outputs.cluster_name

  # Endereco da API do Kubernetes.
  cluster_endpoint = data.terraform_remote_state.cluster.outputs.cluster_endpoint

  # Certificado da CA, em base64. O provider precisa decodificar.
  cluster_ca = data.terraform_remote_state.cluster.outputs.cluster_certificate_authority

  # Mapa <banco> = <URL de conexao completa, com senha>. E marcado como
  # sensitive na origem, entao o Terraform nao imprime o conteudo.
  database_urls = data.terraform_remote_state.cluster.outputs.database_urls

  # URL do Redis, ja com o esquema correto (redis:// ou rediss://).
  redis_url = data.terraform_remote_state.cluster.outputs.redis_url
}
