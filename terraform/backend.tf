# ============================================================
# BACKEND REMOTO E VERSOES - FASE 4 / CAMADA BASE
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

  # Versao minima do Terraform aceita para rodar este projeto.
  # >= 1.11 porque a flag use_lockfile (mais abaixo) so existe a partir dela.
  # Rodando com versao anterior, o terraform init falha com erro explicito.
  required_version = ">= 1.11.0"

  # Declara de quais providers este projeto depende e em que versao.
  required_providers {

    # "aws" e o nome local usado nos blocos provider/resource deste projeto.
    aws = {

      # Endereco do provider no registro publico do Terraform.
      source = "hashicorp/aws"

      # Piso de versao, sem teto de proposito. O modulo de VPC da comunidade
      # declara a propria restricao; fixar "~> 6.0" aqui poderia gerar
      # conflito insoluvel no terraform init. Quem trava a versao exata e o
      # .terraform.lock.hcl, que e versionado no Git justamente para isso.
      # Resolvido em 2026-08-27: provider 6.62.0 com modulo VPC 5.21.0.
      version = ">= 5.46"
    }
  }

  # Configuracao parcial da Fase 4. Fornecer bucket e regiao via
  # -backend-config=backend.hcl, criado a partir de backend.hcl.example.
  # Nao reutilizar nem migrar o estado da Fase 3.
  backend "s3" {
    key          = "phase4/prod/base.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}
