resource "kubernetes_service_v1" "devops_demo" {
  metadata {
    name      = "${var.app_name}-service"
    namespace = kubernetes_namespace_v1.devops-demo.metadata[0].name
    labels = {
      app = var.app_name
    }
  }

  spec {
    selector = {
      app = var.app_name
    }

    port {
      port        = var.container_port   # port exposed by service
      target_port = var.container_port   # port container listens on
    }

    type = "ClusterIP"  
  }
}

