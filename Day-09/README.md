# Day 09 — Exposing Applications with Kubernetes Ingress

## Overview

Until this point in the project, every service has been accessed using `kubectl port-forward`.

While this approach works for local development, it does not resemble how applications are exposed in production Kubernetes environments.

In this phase, we replace temporary port-forwarding with **Kubernetes Ingress**, providing a single entry point for all services running inside the cluster.

By the end of this day, the application and monitoring stack can be accessed using human-friendly hostnames instead of individual ports.

---

# Why Ingress?

So far, accessing the project required multiple terminals:

```text id="cf8mlp"
kubectl port-forward svc/janemils-app 8000:8000

kubectl port-forward svc/prometheus-server 9090:80

kubectl port-forward svc/grafana 3000:80

kubectl port-forward svc/alertmanager 9093:9093
```

Although functional, this approach has several limitations:

* Requires a running terminal for each service.
* Uses different ports for every application.
* Doesn't reflect real-world production deployments.
* Doesn't support hostname-based routing.

Ingress solves these problems by exposing services through a single HTTP entry point.

---

# Architecture

Before Ingress:

```text id="4eovcf"
Browser
    │
    ├── localhost:8000 → FastAPI
    ├── localhost:3000 → Grafana
    ├── localhost:9090 → Prometheus
    └── localhost:9093 → Alertmanager
```

After Ingress:

```text id="o5a1s6"
Browser
    │
    ▼
NGINX Ingress Controller
    │
    ├── app.local → FastAPI
    ├── grafana.local → Grafana
    ├── prometheus.local → Prometheus
    └── alertmanager.local → Alertmanager
```

---

# Learning Objectives

In this phase, you will learn:

* What an Ingress Controller is.
* Why Kubernetes Ingress requires a controller.
* Difference between Service and Ingress.
* Host-based routing.
* Path-based routing.
* Exposing multiple applications through a single entry point.

---

# Project Structure

```text id="8xcruo"
Day-09

├── Part-1: Install NGINX Ingress Controller
│
├── Part-2: Create Ingress Resource
│
├── Part-3: Expose Monitoring Stack
│
└── Part-4: Host & Path Based Routing
```

---

# Part 1 — Install NGINX Ingress Controller

Install the Kubernetes NGINX Ingress Controller.

Topics covered:

* What is an Ingress Controller?
* Why an Ingress resource alone is not enough.
* Deploying the controller inside the cluster.
* Verifying controller installation.

Outcome:

```text id="nlnf4h"
NGINX Ingress Controller running
```

---

# Part 2 — Create an Ingress Resource

Expose the FastAPI application through Ingress.

Instead of:

```text id="gk9knq"
localhost:8000
```

the application becomes accessible via:

```text id="jlwm9y"
http://app.local
```

Topics covered:

* Ingress API
* Rules
* Backend Services
* Default backend

---

# Part 3 — Expose the Monitoring Stack

Instead of exposing only the application, we'll expose the complete observability platform.

Services:

| Host               | Service      |
| ------------------ | ------------ |
| app.local          | FastAPI      |
| grafana.local      | Grafana      |
| prometheus.local   | Prometheus   |
| alertmanager.local | Alertmanager |

This mirrors how internal platforms are commonly organized in production.

---

# Part 4 — Host & Path Based Routing

Learn different routing strategies.

## Host-based Routing

```text id="gyj1qm"
app.local

grafana.local

prometheus.local
```

## Path-based Routing

```text id="g7gyv5"
/api

/docs

/metrics
```

Understanding both routing models provides the foundation for exposing complex microservice architectures.

---

# Skills Demonstrated

By completing this phase, you'll gain experience with:

* Kubernetes Ingress
* NGINX Ingress Controller
* HTTP Routing
* DNS Concepts
* Host-based Routing
* Path-based Routing
* Production-style Application Exposure

---

# Real-World Relevance

Most production Kubernetes clusters expose applications through an Ingress Controller rather than using NodePort or manual port-forwarding.

This architecture enables:

* Single public entry point
* Cleaner URLs
* Reverse proxy capabilities
* TLS termination
* Load balancing
* Routing multiple applications through one endpoint

---

# Future Enhancements

Later phases of this project will extend the Ingress configuration with:

* HTTPS using TLS certificates
* Automatic certificate management
* Custom domains
* Authentication
* Rate limiting
* Canary deployments

---

# Outcome

At the end of Day 09, the application and monitoring stack will no longer rely on `kubectl port-forward`.

Instead, all services will be accessible through a single NGINX Ingress Controller using clean, production-style URLs, providing a deployment model that closely resembles real-world Kubernetes environments.
