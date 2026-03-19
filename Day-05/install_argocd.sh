#!/bin/bash

set -e

echo "Installing ArgoCD..."

# Delete any existing namespace.
kubectl delete namespace argocd --ignore-not-found

# Create namespace
kubectl create namespace argocd || true

# Clean problematic CRD (idempotent)
kubectl delete crd applicationsets.argoproj.io --ignore-not-found=true

# Apply FULL ArgoCD install including the server. This version works for our usecase after trial and error. You can choose whichever version works for your setup.
kubectl apply -n argocd -f \
https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml

echo "Waiting for ArgoCD server to be ready..."
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=180s


# Run ArgoCD in insecure mode (avoid TLS/502 issues)
echo "Patching ArgoCD server to run in insecure mode..."
kubectl patch deployment argocd-server -n argocd \
  -p '{"spec": {"template": {"spec": {"containers": [{"name": "argocd-server","args": ["argocd-server","--insecure"]}]}}}}'

# Restart to apply patch
kubectl rollout restart deployment argocd-server -n argocd

echo "Waiting for patched server..."
kubectl rollout status deployment argocd-server -n argocd

# Port-forward HTTP (not HTTPS now)
echo " Starting port-forward..."

# Binding to 0.0.0.0 as my cluster is in a controlled environment and I cannot access the ui without it being publicly reachable.
kubectl port-forward svc/argocd-server -n argocd 8081:80 --address 0.0.0.0&

sleep 5

echo "ArgoCD Login:"
echo "Username: admin"
echo "Password:"

kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
