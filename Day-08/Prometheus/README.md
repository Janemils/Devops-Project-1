# Part 1: Prometheus Setup & Monitoring Foundation

The objective of this phase was to deploy Prometheus into the Kubernetes cluster and establish the foundation for observability and monitoring.

Prometheus was deployed using Helm into a dedicated `monitoring` namespace.

---

## Deployment

Create the monitoring namespace:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main [?] ➜  kubectl create namespace monitoring
```

Add the Prometheus Helm repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update
```

Install Prometheus:

```bash
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring
```

---

## Initial Deployment Issues

### Issue 1: Node Exporter Failed to Start

After installation, the Node Exporter pod entered a `CreateContainerError` state.

Investigation:

```bash
kubectl get pods -n monitoring

kubectl describe pod <node-exporter-pod> -n monitoring
```

Error observed:

```text
path "/" is mounted on "/" but it is not a shared or slave mount
```

### Root Cause

The project is deployed on a Kind cluster running inside containers.

Node Exporter expects access to host-level filesystem mounts that are not available in this environment.

This is a common limitation when running monitoring stacks inside nested container environments.

### Resolution

Node Exporter was disabled through Helm values:

```yaml
prometheus-node-exporter:
  enabled: false
```

Prometheus was then upgraded using the custom values file.

---

## Issue 2: Alertmanager Stuck in Pending State

Following the Node Exporter fix, Alertmanager remained in a `Pending` state.

Investigation:

```bash
kubectl describe pod prometheus-alertmanager-0 -n monitoring
```

Error observed:

```text
pod has unbound immediate PersistentVolumeClaims
```

### Root Cause

The Kind environment does not provide dynamic storage provisioning by default.

Alertmanager attempted to create a PersistentVolumeClaim that could not be satisfied.

### Resolution

Persistent storage was disabled for Alertmanager:

```yaml
alertmanager:
  persistentVolume:
    enabled: false
```

---

## Issue 3: Prometheus Server Stuck in Pending State

The Prometheus server pod also remained in a Pending state.

Investigation:

```bash
kubectl get pvc -n monitoring
```

A pending PersistentVolumeClaim was identified.

### Root Cause

Similar to Alertmanager, Prometheus attempted to provision persistent storage that was unavailable in the lab environment.

### Resolution

Persistent storage was disabled for the Prometheus server:

```yaml
server:
  persistentVolume:
    enabled: false
```

Prometheus was then upgraded:

```bash
helm upgrade prometheus prometheus-community/prometheus \
  -n monitoring \
  -f values.yaml
```

The monitoring stack successfully started afterwards.

---

## Verifying Deployment

Verify pods:

```bash
kubectl get pods -n monitoring
```

Expected result:

```text
prometheus-kube-state-metrics     Running
prometheus-pushgateway            Running
prometheus-server                 Running
```

Verify services:

```bash
kubectl get svc -n monitoring
```

Verify endpoints:

```bash
kubectl get endpoints -n monitoring
```

---

## Issue 4: Unable to Access Prometheus UI

Prometheus was running successfully, but the UI returned a `502 Bad Gateway` error when accessed through the KodeKloud browser URL.

Initial port forwarding:

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
```

Output:

```text
Forwarding from 127.0.0.1:9090 -> 9090
```

Prometheus responded locally:

```bash
curl http://localhost:9090/-/healthy
```

However, the browser still displayed:

```text
502 Bad Gateway
```

### Root Cause

By default, `kubectl port-forward` binds only to localhost (`127.0.0.1`).

The KodeKloud browser proxy cannot access ports that are exposed only on the local loopback interface.

### Resolution

The port-forward was restarted using:

```bash
kubectl port-forward \
  --address 0.0.0.0 \
  svc/prometheus-server \
  9090:80 \
  -n monitoring
```

This exposed the forwarded port on all network interfaces.

The Prometheus UI became accessible immediately.

### Key Learning

Understanding the difference between:

```text
127.0.0.1
```

and

```text
0.0.0.0
```

is important when troubleshooting application accessibility in Kubernetes and containerized environments.

---

## Validation

Once the UI was accessible:

Navigate to:

```text
Status → Targets
```

All discovered targets were successfully reporting:

```text
UP
```

This confirmed:

* Prometheus was operational
* Scraping was functioning correctly
* Service discovery was working
* Monitoring infrastructure was healthy

---

## Outcome

By the end of this phase:

* Prometheus was successfully deployed using Helm.
* Monitoring components were validated.
* Storage-related deployment issues were resolved.
* Networking and port-forwarding issues were diagnosed and fixed.
* Prometheus targets were successfully scraped.
* The monitoring foundation for application observability was established.

The environment is now ready for application metrics collection and PromQL exploration.

