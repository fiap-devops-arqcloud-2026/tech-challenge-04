# ============================================================
# OBSERVABILIDADE - namespace, segredos e Application (Fase 4)
# ============================================================
# A stack (Prometheus, Grafana, Loki e os Collectors) e implantada pelo
# ArgoCD a partir de gitops/observability. Este arquivo cuida do que o
# Git NAO pode ter: os segredos das integracoes SaaS e a senha do
# Grafana, mais o namespace onde eles moram e a Application que liga o
# ArgoCD a pasta.
#
# MESMA RAZAO DE ORDEM DO secrets.tf: os Secrets precisam existir antes
# dos pods que os leem, e os pods so nascem quando o ArgoCD sincroniza.
#
# CONTRATO DE NOMES (os values de gitops/observability dependem dele):
#   newrelic-license      NEW_RELIC_LICENSE_KEY      -> Collector gateway
#   grafana-admin         admin-user, admin-password -> Grafana
#   grafana-notificacoes  PAGERDUTY_INTEGRATION_KEY,
#                         SLACK_WEBHOOK_URL,
#                         GITHUB_DISPATCH_TOKEN      -> contact points
# ============================================================

resource "kubernetes_namespace_v1" "observability" {
  metadata {
    name = var.observability_namespace

    labels = {
      "app.kubernetes.io/part-of" = "togglemaster"
    }
  }
}

# ------------------------------------------------------------
# Senha do admin do Grafana
# ------------------------------------------------------------
# Gerada aqui e entregue ao chart por existingSecret, para nao existir
# senha padrao ("admin") nem senha em values versionado. Para ler, no dia
# da gravacao:
#   kubectl get secret grafana-admin -n observability \
#     -o jsonpath='{.data.admin-password}' | base64 -d
# Fica fora dos outputs pelo mesmo motivo da senha inicial do ArgoCD.
# ------------------------------------------------------------

resource "random_password" "grafana_admin" {
  length  = 24
  special = false
}

resource "kubernetes_secret_v1" "grafana_admin" {
  metadata {
    name      = "grafana-admin"
    namespace = kubernetes_namespace_v1.observability.metadata[0].name
  }

  # Chaves padrao do chart do Grafana para admin.existingSecret.
  data = {
    admin-user     = "admin"
    admin-password = random_password.grafana_admin.result
  }

  type = "Opaque"
}

# ------------------------------------------------------------
# License key do New Relic - lida pelo Collector gateway
# ------------------------------------------------------------

resource "kubernetes_secret_v1" "newrelic_license" {
  metadata {
    name      = "newrelic-license"
    namespace = kubernetes_namespace_v1.observability.metadata[0].name
  }

  data = {
    NEW_RELIC_LICENSE_KEY = var.new_relic_license_key
  }

  type = "Opaque"
}

# ------------------------------------------------------------
# Segredos dos contact points do Grafana
# ------------------------------------------------------------
# Um Secret so, carregado inteiro como variaveis de ambiente do Grafana
# (envFromSecret do chart). Os arquivos de alerting versionados citam
# apenas os NOMES das variaveis; os valores nunca entram no Git.
# ------------------------------------------------------------

resource "kubernetes_secret_v1" "grafana_notificacoes" {
  metadata {
    name      = "grafana-notificacoes"
    namespace = kubernetes_namespace_v1.observability.metadata[0].name
  }

  data = {
    PAGERDUTY_INTEGRATION_KEY = var.pagerduty_integration_key
    SLACK_WEBHOOK_URL         = var.slack_webhook_url
    GITHUB_DISPATCH_TOKEN     = var.github_dispatch_token
  }

  type = "Opaque"
}

# ------------------------------------------------------------
# A APPLICATION DA OBSERVABILIDADE (padrao app of apps)
# ------------------------------------------------------------
# Uma Application "mae" que observa gitops/observability. La dentro
# estao as Applications "filhas" (um chart Helm cada) e os ConfigMaps de
# dashboard e de alerta. Assim o Terraform cria um objeto so, e o resto
# da stack fica versionado e sincronizado pelo GitOps.
#
# Mesma ressalva do app_togglemaster em argocd.tf: num cluster novo,
# primeiro `apply -target=helm_release.argocd`, depois o apply completo.
# ------------------------------------------------------------

resource "kubernetes_manifest" "app_observability" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"

    metadata = {
      name      = "observability"
      namespace = kubernetes_namespace_v1.argocd.metadata[0].name
    }

    spec = {
      project = "default"

      source = {
        repoURL        = var.gitops_repo_url
        path           = "gitops/observability"
        targetRevision = var.gitops_repo_branch
      }

      # Destino padrao dos ConfigMaps da pasta; as Applications filhas
      # declaram o proprio namespace (argocd).
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = kubernetes_namespace_v1.observability.metadata[0].name
      }

      syncPolicy = {
        automated = {
          prune    = true
          selfHeal = true
        }

        retry = {
          limit = 5
          backoff = {
            duration    = "5s"
            factor      = 2
            maxDuration = "3m"
          }
        }
      }
    }
  }

  depends_on = [helm_release.argocd]
}
