# ============================================================
# BACKEND REMOTO E VERSOES - FASE 4 / CAMADA K8S
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
  # Mesma exigencia das outras camadas.
  required_version = ">= 1.11.0"

  required_providers {
    # Ainda necessario: esta camada le segredos do Secrets Manager.
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.46"
    }

    # Cria os Secrets, o namespace do ArgoCD e a StorageClass.
    kubernetes = {
      source = "hashicorp/kubernetes"
      # Travado na linha 3.x, e nao ">= 2.30". Motivo: entre a 2 e a 3 os
      # recursos sem sufixo (kubernetes_secret) foram depreciados em favor
      # dos com _v1, e o codigo aqui ja usa os novos. Um ">= " sem teto
      # deixaria um v4 futuro entrar sozinho e quebrar sem aviso.
      version = "~> 3.0"
    }

    # Instala o ArgoCD a partir do chart oficial (O-23).
    helm = {
      source = "hashicorp/helm"
      # Travado na linha 3.x pelo mesmo motivo: na 3 o "kubernetes" do
      # provider virou ATRIBUTO em vez de bloco, e providers.tf ja usa a
      # sintaxe nova. Com a 2.x instalada, o validate falharia.
      version = "~> 3.0"
    }

    # Gera a MASTER_KEY do auth-service e a SERVICE_API_KEY provisoria.
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }

  # Configuracao parcial da Fase 4. Fornecer bucket e regiao via
  # -backend-config=backend.hcl, criado a partir de backend.hcl.example.
  # Nao reutilizar nem migrar o estado da Fase 3.
  backend "s3" {
    key          = "phase4/prod/k8s.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}
