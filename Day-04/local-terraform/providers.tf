terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.24.1"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  # Optional, can use this, if you have multiple clusters.
  config_context = "kind-devops-test"
}

