# Part 1: Prometheus Setup & Monitoring Foundation

The objective of this phase was to deploy Prometheus into the Kubernetes cluster and establish the foundation for observability and monitoring.

Prometheus was deployed using Helm into a dedicated `monitoring` namespace.

---

## Deployment

Create the monitoring namespace:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl create namespace monitoring
namespace/monitoring created
```

Add the Prometheus Helm repository:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
"prometheus-community" has been added to your repositories

controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Install Prometheus:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  helm install prometheus prometheus-community/prometheus \
  --namespace monitoring
NAME: prometheus
LAST DEPLOYED: Wed Jun 17 19:04:39 2026
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.monitoring.svc.cluster.local


Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9090

Prometheus alertmanager can be accessed via port 9093 on the following DNS name from within your cluster:
prometheus-alertmanager.monitoring.svc.cluster.local


Get the Alertmanager URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=alertmanager,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9093

Prometheus Pushgateway can be accessed via port 9091 on the following DNS name from within your cluster:
prometheus-prometheus-pushgateway.monitoring.svc.cluster.local


Get the Pushgateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus-pushgateway,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9091

For more information on running Prometheus, visit:
https://prometheus.io/
```

---

## Initial Deployment Issues

### Issue 1: Node Exporter Failed to Start

After installation, the Node Exporter pod entered a `CreateContainerError` state.

Investigation:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl get pods -n monitoring
NAME                                                 READY   STATUS                 RESTARTS   AGE
prometheus-alertmanager-0                            0/1     Pending                0          23s
prometheus-kube-state-metrics-75866fb88d-hxf4x       1/1     Running                0          23s
prometheus-prometheus-node-exporter-5sqfq            0/1     CreateContainerError   0          23s
prometheus-prometheus-pushgateway-74b59b7bb9-krg7v   1/1     Running                0          23s
prometheus-server-8cdc5469d-5tjnc                    0/2     Pending                0          23s

controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl describe pod prometheus-prometheus-node-exporter-5sqfq -n monitoring
...........
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  51s               default-scheduler  Successfully assigned monitoring/prometheus-prometheus-node-exporter-5sqfq to controlplane
  Normal   Pulling    50s               kubelet            spec.containers{node-exporter}: Pulling image "quay.io/prometheus/node-exporter:v1.11.1"
  Normal   Pulled     48s               kubelet            spec.containers{node-exporter}: Successfully pulled image "quay.io/prometheus/node-exporter:v1.11.1" in 2.544s (2.544s including waiting). Image size: 13308798 bytes.
  Warning  Failed     48s               kubelet            spec.containers{node-exporter}: Error: failed to generate container "354ecda097d53306bb2d569af82c53440d25fd6123231f98daa560367cb31e59" spec: failed to generate spec: path "/" is mounted on "/" but it is not a shared or slave mount
  Warning  Failed     47s               kubelet            spec.containers{node-exporter}: Error: failed to generate container "5604b1bd54de8d269ebd4df8c90be95fa84d655c6692256740a560746e1fa71d" spec: failed to generate spec: path "/" is mounted on "/" but it is not a shared or slave mount
  Warning  Failed     33s               kubelet            spec.containers{node-exporter}: Error: failed to generate container "b974250f7a493ab63b5af096484318c00b362799a2ca6b012c50f51c69ad6518" spec: failed to generate spec: path "/" is mounted on "/" but it is not a shared or slave mount
  Warning  Failed     20s               kubelet            spec.containers{node-exporter}: Error: failed to generate container "5033f36299ff942a8a7fd093d2be898bb9ade7446ae57c08488dc96d753af893" spec: failed to generate spec: path "/" is mounted on "/" but it is not a shared or slave mount
  Normal   Pulled     9s (x4 over 47s)  kubelet            spec.containers{node-exporter}: Container image "quay.io/prometheus/node-exporter:v1.11.1" already present on machine and can be accessed by the pod
  Warning  Failed     9s                kubelet            spec.containers{node-exporter}: Error: failed to generate container "5532a651505d310859ee6a3534e722ac1543721ac43246137023a0571a26a21c" spec: failed to generate spec: path "/" is mounted on "/" but it is not a shared or slave mount

```

Error observed:

```text
path "/" is mounted on "/" but it is not a shared or slave mount
```

### Root Cause

The project is deployed on a Kind cluster running inside containers.

Node Exporter expects access to host-level filesystem mounts that are not available in this environment.

This is a common limitation when running monitoring stacks inside nested container environments.

### Resolution for Issue #1:

Node Exporter was disabled through Helm values in [premetheus-values.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Prometheus/prometheus-values.yaml):

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
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜ kubectl describe pod prometheus-alertmanager-0 -n monitoring
.......
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  2m56s  default-scheduler  0/1 nodes are available: pod has unbound immediate PersistentVolumeClaims. not found
```

Error observed:

```text
pod has unbound immediate PersistentVolumeClaims
```

### Root Cause

The Kind environment does not provide dynamic storage provisioning by default.

Alertmanager attempted to create a PersistentVolumeClaim that could not be satisfied.

### Resolution

Persistent storage was disabled for Alertmanager in [premetheus-values.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Prometheus/prometheus-values.yaml)::

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
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl get pvc -n monitoring
NAME                                STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
prometheus-server                   Pending                                                     <unset>                 3m32s
storage-prometheus-alertmanager-0   Pending                                                     <unset>                 3m32s
```

A pending PersistentVolumeClaim was identified.

### Root Cause

Similar to Alertmanager, Prometheus attempted to provision persistent storage that was unavailable in the lab environment.

### Resolution

Persistent storage was disabled for the Prometheus server in [premetheus-values.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Prometheus/prometheus-values.yaml)::

```yaml
server:
  persistentVolume:
    enabled: false
```

Prometheus was then upgraded:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  helm upgrade prometheus prometheus-community/prometheus \
  -n monitoring \
  -f prometheus-values.yaml
Release "prometheus" has been upgraded. Happy Helming!
NAME: prometheus
LAST DEPLOYED: Wed Jun 17 19:09:21 2026
NAMESPACE: monitoring
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.monitoring.svc.cluster.local


Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9090
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Server pod is terminated.                             #####
#################################################################################



Prometheus Pushgateway can be accessed via port 9091 on the following DNS name from within your cluster:
prometheus-prometheus-pushgateway.monitoring.svc.cluster.local


Get the Pushgateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus-pushgateway,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9091

For more information on running Prometheus, visit:
https://prometheus.io/
```

The monitoring stack successfully started afterwards.

---

## Verifying Deployment

Verify pods:

```bash
# Verify if all the pods are up and running:
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl get po -n monitoring
NAME                                                 READY   STATUS    RESTARTS   AGE
prometheus-kube-state-metrics-75866fb88d-hxf4x       1/1     Running   0          4m56s
prometheus-prometheus-pushgateway-74b59b7bb9-krg7v   1/1     Running   0          4m56s
prometheus-server-7c4bf6db77-bv8gx                   1/2     Running   0          13s
```

Verify services:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl get svc -n monitoring
NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
prometheus-kube-state-metrics       ClusterIP   172.20.86.44     <none>        8080/TCP   6m24s
prometheus-prometheus-pushgateway   ClusterIP   172.20.144.69    <none>        9091/TCP   6m24s
prometheus-server                   ClusterIP   172.20.214.195   <none>        80/TCP     6m24s
```

Verify endpoints:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ✖ kubectl get endpoints -n monitoring
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                                ENDPOINTS         AGE
prometheus-kube-state-metrics       172.17.0.6:8080   6m44s
prometheus-prometheus-pushgateway   172.17.0.5:9091   6m44s
prometheus-server                   172.17.0.7:9090   6m44s
```

---

## Issue 4: Unable to Access Prometheus UI

Prometheus was running successfully, but the UI returned a `502 Bad Gateway` error when accessed through the KodeKloud browser URL.

Initial port forwarding:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
Forwarding from 127.0.0.1:9090 -> 9090
Forwarding from [::1]:9090 -> 9090

```

In a new terminal, prometheus responded locally:

```bash
controlplane ~ ➜  curl http://localhost:9090/-/healthy
Prometheus Server is Healthy.
```

However, the browser still displayed:

```text
502 Bad Gateway
```

<img width="1512" height="756" alt="image" src="https://github.com/user-attachments/assets/101211df-9b2b-4424-857a-9c21d9a6b95b" />


### Root Cause

By default, `kubectl port-forward` binds only to localhost (`127.0.0.1`).

The KodeKloud browser proxy cannot access ports that are exposed only on the local loopback interface.

### Resolution

The port-forward was restarted using:

```bash
controlplane Devops-Project-1/Day-08/Prometheus on  main ➜  kubectl port-forward \
  --address 0.0.0.0 \
  svc/prometheus-server \
  9090:80 \
  -n monitoring
Forwarding from 0.0.0.0:9090 -> 9090
```

This exposed the forwarded port on all network interfaces.

The Prometheus UI became accessible immediately.

<img width="1912" height="922" alt="image" src="https://github.com/user-attachments/assets/e5d27e41-2aa3-4b74-88e3-a07f64360261" />


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
<img width="1912" height="1092" alt="image" src="https://github.com/user-attachments/assets/9afb63af-e103-4239-abdb-3abae25b53ac" />

All discovered targets were successfully reporting:

```text
UP
```
<img width="1912" height="847" alt="image" src="https://github.com/user-attachments/assets/8581e4e2-a55c-4ed2-9ad1-a64a6402bd43" />
  
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

