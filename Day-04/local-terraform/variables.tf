variable "app_name" {
  description = "Name of the Kubernetes application"
  type        = string
  default     = "janemils-app"
}

variable "namespace" {
  description = "Kubernetes namespace to deploy the app"
  type        = string
  default     = "devops-demo"
}

variable "image" {
  description = "Docker image for the FastAPI app"
  type        = string
  default     = "janemils/janemils-app:fastapi-v3"
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
  default     = 8000
}

