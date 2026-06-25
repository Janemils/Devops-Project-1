# Day-08 Part-4: Alerting with Prometheus, Alertmanager & Slack

## Objective

In this section, we configure alerting for the FastAPI application.

The goal is to:

* Detect application failures automatically.
* Detect increased HTTP 500 errors.
* Send notifications to engineers through Slack.
* Understand the complete alert lifecycle.

---

# Architecture

```text
FastAPI Application
        │
        ▼
Prometheus Metrics
        │
        ▼
Prometheus Alert Rules
        │
        ▼
Alertmanager
        │
        ▼
Slack Notifications
```

---

# Prerequisites

The following parts must already be completed:

* Part-1: Prometheus Installation
* Part-2: Application Metrics Integration
* Part-3: Grafana Dashboards

Verify:

```bash
kubectl get pods
kubectl get svc
```

Ensure:

* FastAPI application is running.
* Prometheus is scraping metrics.
* Grafana dashboards are working.

---

# Step 1: Create Alert Rules

Create a file named:

```text
alerts.yaml
```

Contents:

```yaml
groups:

- name: janemils-app-alerts

  rules:

  - alert: ApplicationDown

    expr: up{job="janemils-app"} == 0

    for: 1m

    labels:
      severity: critical

    annotations:
      summary: "Application Down"
      description: "janemils-app is unreachable"

  - alert: HighErrorRate

    expr: increase(http_requests_total{status="500"}[5m]) > 5

    for: 1m

    labels:
      severity: warning

    annotations:
      summary: "High Error Rate"
      description: "More than 5 HTTP 500 responses in the last 5 minutes."
```

---

# Understanding the Rules

## ApplicationDown

```promql
up{job="janemils-app"} == 0
```

Prometheus exposes an `up` metric.

Value:

```text
1 = Application reachable
0 = Application unreachable
```

If the application remains unreachable for 1 minute:

```yaml
for: 1m
```

the alert becomes FIRING.

---

## HighErrorRate

```promql
increase(http_requests_total{status="500"}[5m]) > 5
```

This checks:

* Number of HTTP 500 responses.
* During the last 5 minutes.

If more than 5 errors occur within 5 minutes, the alert is triggered.

---

# Step 2: Load Rules into Prometheus

The Prometheus ConfigMap contains:

```yaml
alerts: |
  {}
```

Replace the contents with the alert rules from `alerts.yaml`.

Apply the updated ConfigMap.

Restart Prometheus:

```bash
kubectl rollout restart deployment prometheus-server -n monitoring
```

---

# Step 3: Verify Rules

Port-forward Prometheus:

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
```

Open:

```text
http://localhost:9090/rules
```

Expected:

```text
janemils-app-alerts

ApplicationDown

HighErrorRate
```

---

# Step 4: Test Alert Expressions

Verify PromQL queries.

Application status:

```promql
up{job="janemils-app"}
```

Expected:

```text
1
```

Error count:

```promql
increase(http_requests_total{status="500"}[5m])
```

Expected:

```text
0
```

or a positive value if errors were generated.

---

# Step 5: Trigger HighErrorRate

Generate application errors:

```bash
for i in {1..20}
do
  curl -s http://localhost:8000/error > /dev/null
done
```

Check:

```promql
increase(http_requests_total{status="500"}[5m])
```

Expected:

```text
> 5
```

---

# Step 6: Observe Alert Lifecycle

Open:

```text
http://localhost:9090/alerts
```

Alert states:

```text
Inactive
   ↓
Pending
   ↓
Firing
```

Explanation:

## Inactive

Condition is false.

## Pending

Condition became true.

Prometheus waits:

```yaml
for: 1m
```

before notifying.

## Firing

Condition remained true for the configured duration.

Alert is sent to Alertmanager.

---

# Step 7: Install Alertmanager

Deploy Alertmanager inside the monitoring namespace.

Verify:

```bash
kubectl get deploy -n monitoring
kubectl get svc -n monitoring
```

Expected:

```text
alertmanager
```

service on:

```text
9093
```

---

# Step 8: Connect Prometheus to Alertmanager

Inside Prometheus configuration:

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager.monitoring.svc.cluster.local:9093
```

Restart Prometheus:

```bash
kubectl rollout restart deployment prometheus-server -n monitoring
```

---

# Step 9: Verify Alertmanager

Port-forward:

```bash
kubectl port-forward svc/alertmanager 9093:9093 -n monitoring
```

Open:

```text
http://localhost:9093
```

When an alert is firing, it should appear inside Alertmanager.

---

# Step 10: Configure Slack Notifications

Create a Slack Incoming Webhook.

Store the webhook URL.

Update Alertmanager configuration:

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: slack-notifications

receivers:

- name: slack-notifications
  slack_configs:
  - api_url: '<SLACK_WEBHOOK_URL>'
    channel: '<YOUR-CHANNEL-NAME>'
    send_resolved: true
```

Apply configuration.

Restart Alertmanager.

---

# Step 11: Improve Slack Message Formatting

Example:

```yaml
title: >-
  [{{ .Status | toUpper }}]
  {{ range .Alerts }}
  {{ .Annotations.summary }}
  {{ end }}

text: >-
  {{ range .Alerts }}

  *Alert:* {{ .Labels.alertname }}

  *Severity:* {{ .Labels.severity }}

  *Job:* {{ .Labels.job }}

  *Instance:* {{ .Labels.instance }}

  *Description:* {{ .Annotations.description }}

  *Status:* {{ $.Status }}

  {{ end }}
```

---

# Expected Slack Messages

## FIRING

```text
🚨 FIRING - High Error Rate

Alert Name: HighErrorRate
Severity: warning
Job: janemils-app

Description:
More than 5 HTTP 500 responses in the last 5 minutes.
```

---

## RESOLVED

```text
✅ RESOLVED - High Error Rate

Alert Name: HighErrorRate
Severity: warning
Job: janemils-app

Description:
More than 5 HTTP 500 responses in the last 5 minutes.
```

---

<img width="1286" height="487" alt="image" src="https://github.com/user-attachments/assets/78bac5d3-7c39-4509-a57e-572e7b598571" />

<img width="1002" height="462" alt="image" src="https://github.com/user-attachments/assets/321755f9-b494-4633-ab6c-3343a8a236a8" />

# Key Learning Outcomes

By completing this section, we learned:

* How Prometheus evaluates alert rules.
* How alert states transition from Inactive → Pending → Firing.
* How Alertmanager receives firing alerts.
* How Alertmanager routes notifications.
* How Slack integrations work.
* How production monitoring systems notify engineers about incidents.
