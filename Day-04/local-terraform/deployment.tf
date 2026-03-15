resource "kubernetes_deployment_v1" "devops-demo" {

  metadata {
    name      = "${var.app_name}-deployment"
    namespace = var.namespace

    labels = {
      app = var.app_name
    }
  }

  spec {

    replicas = var.replicas

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {

      metadata {
        labels = {
          app = var.app_name
        }
      }

      spec {

        container {
          name  = var.app_name
          image = var.image

          port {
            container_port = var.container_port
          }

          # ---- Readiness probe ----
          readiness_probe {

            http_get {
              path = "/health"
              port = var.container_port
            }

            initial_delay_seconds = 3
            period_seconds        = 5
            timeout_seconds       = 2
            failure_threshold     = 3
          }

          # ---- Liveness probe ----
          liveness_probe {

            http_get {
              path = "/hello"
              port = var.container_port
            }

            initial_delay_seconds = 5
            period_seconds        = 5
            timeout_seconds       = 2
            failure_threshold     = 3
          }

          # ---- Optional but recommended ----
          resources {

            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }

            limits = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }

        }

      }
    }
  }
}

