# Day-09: Kubernetes Ingress Controller & Host-Based Routing

## Overview

Until now, every application running inside the Kubernetes cluster required its own port-forward session to be accessed locally.

For example:

| Application  | Access Method          |
| ------------ | ---------------------- |
| FastAPI      | `kubectl port-forward` |
| Grafana      | `kubectl port-forward` |
| Prometheus   | `kubectl port-forward` |
| Alertmanager | `kubectl port-forward` |

This approach works for development but quickly becomes difficult to manage as more services are added.

The goal of this phase is to introduce **Kubernetes Ingress**, allowing multiple services to be accessed through a **single entry point** using host-based routing.

---

# Objectives

By the end of this section you will learn:

* What an Ingress Controller is
* Why Kubernetes needs an Ingress Controller
* Installing NGINX Ingress Controller
* Creating Ingress resources
* Host-based routing
* Routing traffic to multiple applications
* Configuring local DNS using `/etc/hosts`
* Understanding how this setup differs from production environments

---

# Architecture Before Ingress

Before implementing Ingress, every application required its own port-forward session.

```text
Browser
   │
   ▼
kubectl port-forward
   │
   ▼
Application Service
   │
   ▼
Pods
```

If multiple services existed:

```text
Browser
   │
   ├────────► FastAPI
   │
   ├────────► Grafana
   │
   ├────────► Prometheus
   │
   └────────► Alertmanager
```

Each service required:

* Different port
* Different terminal
* Different port-forward command

This does not scale.

---

# Why Ingress?

Ingress provides a **single entry point** into the Kubernetes cluster.

Instead of exposing every service individually, all requests first arrive at the Ingress Controller.

The controller then decides which Service should receive the request.

---

# Architecture After Ingress (The routing flow):

```text
                    Browser
                        │
                        ▼
          NGINX Ingress Controller
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
 app.local       grafana.local    prometheus.local
      │                 │                 │
      ▼                 ▼                 ▼
 FastAPI           Grafana          Prometheus

                        │
                        ▼
               alertmanager.local
                        │
                        ▼
                 Alertmanager
```

Every request now enters the cluster through one gateway.

---

# Project Structure

```
Day-09/

├── ingress-default-namespace.yaml
└── ingress-monitoring-namespace.yaml
```

---

# Part-1: Install NGINX Ingress Controller

Install the official NGINX Ingress Controller.

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
namespace/ingress-nginx created
serviceaccount/ingress-nginx created
serviceaccount/ingress-nginx-admission created
role.rbac.authorization.k8s.io/ingress-nginx created
role.rbac.authorization.k8s.io/ingress-nginx-admission created
clusterrole.rbac.authorization.k8s.io/ingress-nginx created
clusterrole.rbac.authorization.k8s.io/ingress-nginx-admission created
rolebinding.rbac.authorization.k8s.io/ingress-nginx created
rolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx created
clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
configmap/ingress-nginx-controller created
service/ingress-nginx-controller created
service/ingress-nginx-controller-admission created
deployment.apps/ingress-nginx-controller created
job.batch/ingress-nginx-admission-create created
job.batch/ingress-nginx-admission-patch created
ingressclass.networking.k8s.io/nginx created
validatingwebhookconfiguration.admissionregistration.k8s.io/ingress-nginx-admission created
```

Verify installation:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ kubectl get pods -n ingress-nginx
NAME                                       READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-ffd4ff4d7-2b82z   1/1     Running   0          59s

```

Verify services:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ kubectl get svc -n ingress-nginx
NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   10.96.1.240     <pending>     80:31488/TCP,443:31684/TCP   87s
ingress-nginx-controller-admission   ClusterIP      10.96.143.216   <none>        443/TCP                      87s
```

---

# Understanding the LoadBalancer Service

The controller is exposed using a **LoadBalancer** service.

In cloud environments:

```
AWS
Azure
GCP
```

Kubernetes automatically provisions an external load balancer.

Since this project runs inside a local Kubernetes environment (I am using kind cluster or a sandbox setup), there is no cloud provider available.

Therefore:

```
EXTERNAL-IP
<pending>
```

This is expected behaviour.

---

# Part-2: Expose the FastAPI Application

Create an Ingress resource inside the **default** namespace. Or you can use the manifest file: [ingress-default-namespace.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-09/ingress-default-namespace.yaml).

Example:

```yaml
host: app.local
```

The Ingress routes traffic to the FastAPI Service.

Traffic Flow:

```
Browser

↓

Ingress Controller

↓

Ingress Rule

↓

FastAPI Service

↓

Pods
```

---

# Part-3: Expose the Monitoring Stack

Grafana, Prometheus and Alertmanager already exist inside the **monitoring** namespace. Or you can use the manifest file: [ingress-monitoring-namespace.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-09/ingress-monitoring-namespace.yaml).

Instead of creating three different Ingress resources, a single Ingress was created containing multiple host rules.

Hosts:

```
grafana.local

prometheus.local

alertmanager.local
```

Each host routes traffic to the corresponding Service.

---

# Why Separate Ingress Resources?

Ingress resources are **namespace scoped**.

An Ingress can only route traffic to Services inside its own namespace.

For this reason:

```
default
└── app-ingress.yaml
```

and

```
monitoring
└── monitoring-ingress.yaml
```

were created separately.

This closely resembles how production Kubernetes clusters are organised.

---

# Local Testing

Since the LoadBalancer cannot obtain an external IP inside the local cluster, the Ingress Controller is temporarily exposed using:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
```

Only **one** port-forward session is now required.

---

# Local DNS Configuration

The browser needs to resolve custom hostnames.

Edit:

```
/etc/hosts
```

Add this in the bottom of the file:

```text
127.0.0.1 app.local
127.0.0.1 grafana.local
127.0.0.1 prometheus.local
127.0.0.1 alertmanager.local
```

Now the applications become accessible through:

```
http://app.local:8080

http://grafana.local:8080

http://prometheus.local:8080

http://alertmanager.local:8080
```

No special curl headers are required.

---

# Final Architecture (The observability flow):

```text
                FastAPI Application
                        │
                Exposes /metrics
                        │
                        ▼
                  Prometheus
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   Grafana Queries              Alert Rules
                                        │
                                        ▼
                                 Alertmanager
                                        │
                                        ▼
                                     Slack
```

---

# Testing

Verify application routing:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ curl -H "Host: app.local" http://localhost:8080/hello
{"message":"Hello from DevOps app"}
```

Open this in the browser:

```text
http://app.local:8080/hello
```
  
<img width="1852" height="228" alt="image" src="https://github.com/user-attachments/assets/a886db69-4c69-4aca-a026-b5ee99a7b515" />
  
  
Verify Grafana:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ curl -H "Host: grafana.local" http://localhost:8080
<a href="/login">Found</a>.

```
  
Open this in the browser:

```text
http://grafana.local:8080
```
  
<img width="1852" height="1008" alt="image" src="https://github.com/user-attachments/assets/429b799f-ad35-4335-b6ed-70a6dec7afc7" />
  
  
Verify Prometheus:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ curl -H "Host: prometheus.local" http://localhost:8080
<a href="/query">Found</a>.
```
  
Open this in the browser:

```text
http://prometheus.local:8080
```
  
<img width="1852" height="686" alt="image" src="https://github.com/user-attachments/assets/49b9ddcf-ab93-4bdf-bf9b-beac0f9a53fd" />
  
  
Verify Alertmanager:

```bash
controlplane Devops-Project-1/Day-09 on  main ➜ curl -H "Host: alertmanager.local" http://localhost:8080
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="icon" type="image/x-icon" href="favicon.ico" />
        <title>Alertmanager</title>
    </head>
    <body>
        <script>
            // If there is no trailing slash at the end of the path in the url,
            // add one. This ensures assets like script.js are loaded properly
            if (location.pathname.substr(-1) != '/') {
                location.pathname = location.pathname + '/';
                console.log('added slash');
            }
        </script>
        <script src="script.js"></script>
        <script>
            var app = Elm.Main.init({
                flags: {
                    production: true,
                    firstDayOfWeek: JSON.parse(localStorage.getItem('firstDayOfWeek')),
                    defaultCreator: localStorage.getItem('defaultCreator'),
                    groupExpandAll: JSON.parse(localStorage.getItem('groupExpandAll'))
                }
            });
            app.ports.persistDefaultCreator.subscribe(function(name) {
                localStorage.setItem('defaultCreator', name);
            });
            app.ports.persistGroupExpandAll.subscribe(function(expanded) {
                localStorage.setItem('groupExpandAll', JSON.stringify(expanded));
            });
            app.ports.persistFirstDayOfWeek.subscribe(function(firstDayOfWeek) {
                localStorage.setItem('firstDayOfWeek', JSON.stringify(firstDayOfWeek));
            });
        </script>
    </body>

```

Open this in the browser:

```text
http://alertmanager.local:8080
```
  
<img width="1852" height="686" alt="image" src="https://github.com/user-attachments/assets/d9236a35-9765-43ef-a6a9-ba3da30aaa56" />
  
  
---

# What Was Achieved

The project now provides:

* Single entry point into the Kubernetes cluster
* Host-based routing
* Centralized traffic management
* Multiple applications behind one reverse proxy
* Production-style application access
* Reduced operational complexity
* Cleaner developer workflow

---

# Production Considerations

In production:

```
Browser

↓

DNS

↓

Cloud Load Balancer

↓

NGINX Ingress Controller

↓

Ingress Rules

↓

Kubernetes Services

↓

Pods
```

Instead of editing `/etc/hosts`, DNS records would point to the cloud Load Balancer.

Examples:

```
app.company.com

grafana.company.com

prometheus.company.com

alertmanager.company.com
```

The remainder of the routing process remains exactly the same.

---

# Key Learnings

* Kubernetes Ingress
* NGINX Ingress Controller
* Host-based routing
* Reverse Proxy architecture
* Namespace-scoped Ingress resources
* Local DNS configuration
* Centralized application exposure
* Production networking concepts

---

# Next Steps

The next phase of the project will focus on securing the platform using HTTPS.

Planned topics:

* TLS Certificates
* cert-manager
* ClusterIssuer
* Let's Encrypt
* Automatic certificate renewal
* HTTPS-enabled Ingress
