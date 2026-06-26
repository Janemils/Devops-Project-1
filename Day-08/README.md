# Day 08 — Monitoring, Visualization & Alerting

## Overview

Day 08 introduces a complete observability stack for the FastAPI application deployed on Kubernetes.

By the end of this phase, the application is capable of:

* Exposing application metrics
* Collecting metrics with Prometheus
* Visualizing metrics with Grafana
* Detecting failures using Prometheus Alert Rules
* Routing alerts through Alertmanager
* Notifying engineers via Slack

This mirrors the monitoring workflow used in modern cloud-native environments.

---

# Monitoring Stack

| Component    | Responsibility               |
| ------------ | ---------------------------- |
| FastAPI      | Exposes application metrics  |
| Prometheus   | Scrapes and stores metrics   |
| Grafana      | Visualizes metrics           |
| Alertmanager | Processes and routes alerts  |
| Slack        | Receives alert notifications |

---

# Architecture

```text
                        +--------------------+
                        |   FastAPI App      |
                        +---------+----------+
                                  |
                                  | /metrics
                                  |
                                  v
                        +--------------------+
                        |    Prometheus      |
                        +---------+----------+
                                  |
              +-------------------+-------------------+
              |                                       |
              |                                       |
              v                                       v
      +---------------+                     +------------------+
      |   Grafana     |                     | Alertmanager     |
      +---------------+                     +--------+---------+
                                                     |
                                                     |
                                                     v
                                              +-------------+
                                              |   Slack     |
                                              +-------------+
```

---

# Project Structure

```text
Day-08
│
├── Part-1: Prometheus
│   ├── Install Prometheus
│   ├── Configure scrape jobs
│   └── Verify metric collection
│
├── Part-2: App to Prometheus
│   ├── Instrument FastAPI
│   ├── Expose /metrics
│   └── Verify custom metrics
│
├── Part-3: Grafana
│   ├── Connect Prometheus
│   ├── Build dashboards
│   └── Visualize application metrics
│
└── Part-4: Configuring Alerts
    ├── Create alert rules
    ├── Configure Alertmanager
    ├── Integrate Slack
    └── Test alert lifecycle
```

---

# Metrics Monitored

The application exposes custom Prometheus metrics for:

* HTTP Request Count
* HTTP Response Status Codes
* Request Latency
* Application Health

These metrics are visualized through Grafana dashboards and evaluated by Prometheus alert rules.

---

# Implemented Alerts

| Alert           | Purpose                             | Severity |
| --------------- | ----------------------------------- | -------- |
| ApplicationDown | Detect application outages          | Critical |
| HighErrorRate   | Detect excessive HTTP 500 responses | Warning  |

Each alert follows the complete lifecycle:

```text
Inactive
    ↓
Pending
    ↓
Firing
    ↓
Resolved
```

---

# Notification Flow

When an alert fires:

```text
FastAPI
    ↓
Prometheus Metrics
    ↓
Prometheus Alert Rule
    ↓
Alertmanager
    ↓
Slack Notification
```

Both **FIRING** and **RESOLVED** notifications are delivered automatically.

---

# Skills Demonstrated

* Kubernetes Monitoring
* Prometheus Configuration
* Application Instrumentation
* PromQL
* Grafana Dashboard Creation
* Alertmanager Configuration
* Slack Integration
* End-to-End Observability

---

# Future Enhancements

Planned improvements for Version 2:

* NGINX Ingress Controller
* TLS / HTTPS
* GitOps with ArgoCD
* Terraform-managed Infrastructure
* Kubernetes Resource Monitoring
* Node Exporter
* Blackbox Exporter
* Service Level Objective (SLO) Dashboards
* Multi-environment Deployments

---

# Related Documentation

Each implementation is documented separately:

* [**Part-1:** Prometheus Installation & Configuration.](https://github.com/Janemils/Devops-Project-1/tree/main/Day-08/Part-1%3APrometheus)
* [**Part-2:** Instrumenting the FastAPI Application.](https://github.com/Janemils/Devops-Project-1/tree/main/Day-08/Part-2%3AApp-to-Prometheus)
* [**Part-3:** Grafana Dashboards.](https://github.com/Janemils/Devops-Project-1/tree/main/Day-08/Part-2%3AApp-to-Prometheus)
* [**Part-4:** Alert Rules, Alertmanager & Slack Notifications.](https://github.com/Janemils/Devops-Project-1/tree/main/Day-08/Part-4%3AConfiguring-Alerts)
