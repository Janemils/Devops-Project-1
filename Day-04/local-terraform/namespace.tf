resource "kubernetes_namespace_v1" "devops-demo"{
	metadata{
		name=var.namespace
		}
}
