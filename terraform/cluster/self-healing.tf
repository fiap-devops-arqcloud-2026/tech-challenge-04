# ============================================================
# SELF-HEALING - acesso da role do GitHub Actions ao cluster (Fase 4)
# ============================================================
# A role togglemaster-self-healing (camada base) so consegue DESCREVER o
# cluster na AWS. Para o kubectl dela funcionar, o EKS precisa saber
# quem ela e dentro do Kubernetes - e isso e um access entry.
#
# O access entry diz ao EKS: "quando esta role IAM chegar, trate-a como
# membro do grupo Kubernetes togglemaster-self-healing". O que esse grupo
# pode fazer e decidido por um Role/RoleBinding no namespace das
# aplicacoes, versionado em gitops/base/self-healing-rbac.yaml.
#
# POR QUE GRUPO PROPRIO E NAO UMA ACCESS POLICY DA AWS: as policies
# prontas (AmazonEKSEditPolicy, por exemplo) liberam criar e apagar quase
# tudo no namespace. O self-healing so precisa reiniciar um Deployment e
# acompanhar o resultado - o RBAC proprio entrega exatamente isso.
#
# Funciona porque o cluster usa authentication_mode API_AND_CONFIG_MAP
# (modules/eks/main.tf), que aceita access entries pela API.
# ============================================================

resource "aws_eks_access_entry" "self_healing" {
  cluster_name = module.eks.cluster_name

  # ARN publicado pela camada base (output self_healing_role_arn). A base
  # precisa ter sido aplicada com esse output antes deste plan.
  principal_arn = data.terraform_remote_state.base.outputs.self_healing_role_arn

  # Nome do grupo usado no RoleBinding do gitops. Precisa ser identico,
  # caractere por caractere; grupos com prefixo system: sao recusados.
  kubernetes_groups = ["togglemaster-self-healing"]

  # STANDARD e o tipo para roles e usuarios IAM comuns (os outros tipos
  # sao para nos do cluster e integracoes da propria AWS).
  type = "STANDARD"
}
