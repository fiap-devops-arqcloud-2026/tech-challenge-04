# ============================================================
# BACKEND REMOTO E VERSOES - FASE 4 / CAMADA CLUSTER
# ============================================================
# Backend S3 parcial: a conta e o bucket novos ainda estao pendentes.
# Configuracao futura: copiar backend.hcl.example para backend.hcl e
# informar bucket/regiao confirmados. Nunca copiar .terraform/ ou
# arquivos tfstate da Fase 3; as chaves abaixo sao exclusivas da Fase 4.
# O init -backend=false usado na validacao nao acessa S3.
# Ordem de dependencias: base -> cluster -> k8s. Qualquer destruicao
# exige plano separado e autorizacao explicita; preservar EBS CSI ate
# confirmar remocao dos PVCs/PVs/discos do banco no cluster.
# ============================================================

terraform {
  # Mesma exigencia da base: use_lockfile so existe a partir da 1.11.
  required_version = ">= 1.11.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      # Mesmo criterio da base: piso sem teto, para nao conflitar com a
      # restricao interna dos modulos da comunidade. O lock file trava.
      version = ">= 5.46"
    }

    # Gera as senhas dos dois bancos RDS. Usado em modules/rds/main.tf.
    # Sem declarar aqui, o terraform init nao baixa o provider e o
    # random_password falha com "provider not found".
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }

    # Le o certificado do emissor OIDC do cluster para extrair a
    # impressao digital exigida pelo provedor OIDC do IAM. Usado em
    # modules/eks/main.tf, no bloco que habilita o IRSA (S-06).
    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.0"
    }
  }

  # Configuracao parcial da Fase 4. Fornecer bucket e regiao via
  # -backend-config=backend.hcl, criado a partir de backend.hcl.example.
  # Nao reutilizar nem migrar o estado da Fase 3.
  backend "s3" {
    key          = "phase4/prod/cluster.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}
