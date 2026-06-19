# Part 2 - Application Metrics Integration

The objective of this phase is to integrate application-level metrics with Prometheus and verify that application telemetry can be collected, queried, and analyzed.

---

## Step 1: Verify Application Metrics Endpoint

The FastAPI application was instrumented using the Prometheus Python client and exposed metrics through:

```text
/metrics
```
Follow [Day-03](https://github.com/Janemils/Devops-Project-1/tree/main/Day-03) to get the application up and running in your cluster.

Verification:

```bash
# Verification of the application reachability:
controlplane ~ ➜  curl http://localhost:8000/hello
{"message":"Hello from DevOps app"}

# Verification of the prometheus metrics:
controlplane ~ ➜  curl http://localhost:8000/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 598.0
python_gc_objects_collected_total{generation="1"} 6.0
python_gc_objects_collected_total{generation="2"} 0.0
..................................
```

The output confirmed that Prometheus-compatible metrics are available and the application is reachable.

---
  
## Step 2: Verify Prometheus Installation

Confirm Prometheus is healthy:

```bash
controlplane Devops-Project-1/Day-08/App-to-Prometheus on  main ➜  kubectl get pods -n monitoring
NAME                                                 READY   STATUS    RESTARTS   AGE
prometheus-kube-state-metrics-75866fb88d-gw7l6       1/1     Running   0          12m
prometheus-prometheus-pushgateway-74b59b7bb9-8zfdh   1/1     Running   0          12m
prometheus-server-5c7887b6b5-6qc9r                   1/2     Running   0          5s
```
---

## Step 3: Verify Prometheus Can Reach the Application

Test connectivity from inside the cluster:

```bash
controlplane Devops-Project-1/Day-08/App-to-Prometheus on  main ➜  kubectl exec -it -n monitoring deploy/prometheus-server -- sh
Defaulted container "prometheus-server-configmap-reload" out of: prometheus-server-configmap-reload, prometheus-server
/ $
```

Inside the pod:

```bash
/ $ wget -qO- http://janemils-app-deployment.default.svc.cluster.local:8000/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 594.0
python_gc_objects_collected_total{generation="1"} 6.0
python_gc_objects_collected_total{generation="2"} 0.0
```

Metrics were successfully returned.

This verified that network connectivity between Prometheus and the application existed.

---

## Step 4: Configure Prometheus Scraping

A new scrape job was added to the prometheus-server configmap:

```bash
controlplane Devops-Project-1/Day-08/App-to-Prometheus on  main ➜  kubectl edit configmap prometheus-server -n monitoring -o yaml
```

```yaml
- job_name: "janemils-app"
  metrics_path: /metrics
  static_configs:
    - targets:
      - janemils-app-deployment.default.svc.cluster.local:8000
```
<img width="1000" height="695" alt="image" src="https://github.com/user-attachments/assets/4413926b-3516-4d86-b2dd-36de01db865c" />

This instructs Prometheus to periodically collect metrics from the application.

---

## Step 5: Reload Prometheus

After updating the configuration:

```bash
controlplane Devops-Project-1/Day-08/App-to-Prometheus on  main ➜  kubectl rollout restart deploy/prometheus-server -n monitoring
deployment.apps/prometheus-server restarted

# Verify the pods:
controlplane Devops-Project-1/Day-08/App-to-Prometheus on  main [?] ➜  kubectl get pods -n monitoring
NAME                                                 READY   STATUS    RESTARTS   AGE
prometheus-kube-state-metrics-75866fb88d-gw7l6       1/1     Running   0          33m
prometheus-prometheus-pushgateway-74b59b7bb9-8zfdh   1/1     Running   0          33m
prometheus-server-5c7887b6b5-6qc9r                   2/2     Running   0          21m
```

Prometheus restarted and loaded the new scrape configuration.

---

## Step 6: Verify Target Status

Open the Prometheus UI and navigate to:

```text
Status → Targets
```

Result:

<img width="1000" height="362" alt="image" src="https://github.com/user-attachments/assets/b35947df-8790-409f-a5de-793affa5ac81" />


This confirmed successful metric collection.

---

## Step 7: Query Application Metrics

Verify that custom metrics are being stored.

Example:

```promql
up{job="janemils-app"}
```

Result:

<img width="1000" height="409" alt="image" src="https://github.com/user-attachments/assets/a9df27eb-692a-490f-ad9e-a838d1d54740" />


Additional queries:

```promql
http_requests_total
```

```promql
process_resident_memory_bytes
```

```promql
process_cpu_seconds_total
```

Prometheus successfully collected both application metrics and runtime metrics.

---

# Which Metrics Matter in Production?

This is where observability becomes useful.

Most production teams focus on five categories of metrics.

# The Golden Signals

Most SRE and DevOps teams monitor four core signals:

| Signal     | Metric             |
| ---------- | ------------------ |
| Latency    | Request duration   |
| Traffic    | Request rate       |
| Errors     | Error rate         |
| Saturation | CPU / Memory usage |

These are commonly known as the **Golden Signals**, introduced by Rob Ewaschuk as part of Google's SRE practices.

---

## Recommended Dashboard Panels

For this project, the most valuable Grafana dashboard panels will be:

* Request Rate
* Total Requests
* Average Latency
* Error Rate
* CPU Usage
* Memory Usage
* Target Health (`up`)

These seven panels provide a realistic production monitoring dashboard and establish a strong observability foundation.

You can refer to this to play around for the further metrics testing with the application that we have.



