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
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl get pods -n monitoring
NAME                                                 READY   STATUS    RESTARTS         AGE
grafana-76777755bb-9sbql                             1/1     Running   5 (4h17m ago)    46h
prometheus-kube-state-metrics-7656c476c8-pbl5t       1/1     Running   10 (4h16m ago)   46h
prometheus-prometheus-pushgateway-6c7fc5c98c-pwxqj   1/1     Running   5 (4h17m ago)    46h
prometheus-server-554bfd68f5-svlzv                   2/2     Running   4 (4h17m ago)    22h

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl get svc -n monitoring
NAME                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
grafana                             ClusterIP   10.96.81.160    <none>        80/TCP     47h
prometheus-kube-state-metrics       ClusterIP   10.96.15.202    <none>        8080/TCP   47h
prometheus-prometheus-pushgateway   ClusterIP   10.96.250.103   <none>        9091/TCP   47h
prometheus-server                   ClusterIP   10.96.12.216    <none>        80/TCP     47h

```

Ensure:

* FastAPI application is running.
* Prometheus is scraping metrics.
* Grafana dashboards are working.

---

# Step 1: Create Alert Rules

Create a file named: (or you can use the one that is there in this folder: [alerts.yaml](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-4%3AConfiguring-Alerts/alerts.yaml)

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
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl rollout restart deployment prometheus-server -n monitoring
deployment.apps/prometheus-server restarted

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl get pods -n monitoring
NAME                                                 READY   STATUS    RESTARTS         AGE
grafana-76777755bb-9sbql                             1/1     Running   5 (4h23m ago)    46h
prometheus-kube-state-metrics-7656c476c8-pbl5t       1/1     Running   10 (4h22m ago)   46h
prometheus-prometheus-pushgateway-6c7fc5c98c-pwxqj   1/1     Running   5 (4h23m ago)    46h
prometheus-server-6f4bb976c4-glj2r                   2/2     Running   0                2m57s

```

---

# Step 3: Verify Rules

Port-forward Prometheus:

```bash

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
Forwarding from 127.0.0.1:9090 -> 9090
Forwarding from [::1]:9090 -> 9090
Handling connection for 9090

```

Open:

```text
http://localhost:9090/rules
```

Expected:

<img width="1852" height="868" alt="Screenshot from 2026-06-26 23-10-21" src="https://github.com/user-attachments/assets/55dd3a87-8cce-4baa-aa6c-251839ce0496" />


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

<img width="1852" height="868" alt="Screenshot from 2026-06-26 23-15-03" src="https://github.com/user-attachments/assets/2e5afff7-2981-4710-9e24-98deae9239e0" />

---

# Step 5: Trigger HighErrorRate

Generate application errors:

```bash
for i in {1..20}; do
  curl http://localhost:8000/error
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

# 6.1: Let's observe for HighErrorRate:

Inactive state for HighErrorRate Alert:
<img width="1855" height="871" alt="No-Alerts-Triggered" src="https://github.com/user-attachments/assets/04d3c313-7876-49af-8d83-3cf72980a8ee" />
  

Pending state for HighErrorRate Alert:
<img width="1858" height="732" alt="High-Error-Rate-Pending" src="https://github.com/user-attachments/assets/ad1dbe87-ffff-4032-9405-0ada697f47f5" />


Firing state for HighErrorRate Alert:
<img width="1858" height="732" alt="High-Error-Rate-Firing" src="https://github.com/user-attachments/assets/b3678e51-3cd2-46bf-b2db-464709349caf" />


# 6.2: Let's observe for ApplicationDown:

Inactive state for ApplicationDown Alert:
<img width="1855" height="871" alt="No-Alerts-Triggered" src="https://github.com/user-attachments/assets/6c5229cf-7718-4acd-bb32-e62a344bf40e" />
  

Pending state for ApplicationDown Alert:
<img width="1855" height="871" alt="Application-Down-Pending" src="https://github.com/user-attachments/assets/033b26e2-07d7-4431-a494-56d245d9b9cb" />


Firing state for ApplicationDown Alert:
<img width="1855" height="871" alt="Application-Down-Firing" src="https://github.com/user-attachments/assets/03c19aa2-599e-4844-b06c-9bbe0e2963e6" />


---

# Step 7: Install Alertmanager

Deploy [Alertmanager app](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-4%3AConfiguring-Alerts/alertmanager-deployment.yaml) and it's respective [service](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-4%3AConfiguring-Alerts/alertmanager-service.yaml) inside the monitoring namespace.

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜   kubectl apply -f alertmanager-deployment.yaml 
deployment.apps/alertmanager created

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜   kubectl apply -f alertmanager-service.yaml 
service/alertmanager created
```

Verify:

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl get deploy -n monitoring
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
alertmanager                        1/1     1            1           47h
grafana                             1/1     1            1           47h
prometheus-kube-state-metrics       1/1     1            1           47h
prometheus-prometheus-pushgateway   1/1     1            1           47h
prometheus-server                   1/1     1            1           47h
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜  kubectl get svc -n monitoring
NAME                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
alertmanager                        ClusterIP   10.96.219.65    <none>        9093/TCP   47h
grafana                             ClusterIP   10.96.81.160    <none>        80/TCP     47h
prometheus-kube-state-metrics       ClusterIP   10.96.15.202    <none>        8080/TCP   47h
prometheus-prometheus-pushgateway   ClusterIP   10.96.250.103   <none>        9091/TCP   47h
prometheus-server                   ClusterIP   10.96.12.216    <none>        80/TCP     47h

```

---

# Step 8: Connect Prometheus to Alertmanager

Inside Prometheus configuration (configmap):

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager.monitoring.svc.cluster.local:9093
```

Your configmap should look something like this:

<img width="1855" height="871" alt="Config-Map-Changes-For-Alerts" src="https://github.com/user-attachments/assets/15f0a540-f99a-46c2-b86a-664fd9b09b61" />
  
Restart Prometheus:

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl rollout restart deployment prometheus-server -n monitoring
deployment.apps/prometheus-server restarted

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl get pods -n monitoring
NAME                                                 READY   STATUS    RESTARTS         AGE
grafana-76777755bb-9sbql                             1/1     Running   5 (4h23m ago)    46h
prometheus-kube-state-metrics-7656c476c8-pbl5t       1/1     Running   10 (4h22m ago)   46h
prometheus-prometheus-pushgateway-6c7fc5c98c-pwxqj   1/1     Running   5 (4h23m ago)    46h
prometheus-server-6f4bb976c4-glj2r                   2/2     Running   0                2m57s
```

---

# Step 9: Verify Alertmanager

Port-forward:

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜  kubectl port-forward svc/alertmanager 9093:9093 -n monitoring
Forwarding from 127.0.0.1:9093 -> 9093
Forwarding from [::1]:9093 -> 9093
```

Open:

```text
http://localhost:9093
```

<img width="1852" height="868" alt="Screenshot from 2026-06-26 23-35-19" src="https://github.com/user-attachments/assets/39483ca1-1a5f-4378-8b77-b7d700339d58" />
  
When an alert is firing, it should appear inside Alertmanager.
<img width="1852" height="868" alt="image" src="https://github.com/user-attachments/assets/a994784c-24ce-4231-8976-badbd776594a" />
<img width="1852" height="868" alt="image" src="https://github.com/user-attachments/assets/2a50461b-6be5-4c56-92e1-27a21d9bf02e" />
  

---

# Step 10: Configure Slack Notifications

Create a [Slack Incoming Webhook](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-4%3AConfiguring-Alerts/Setup-Slack.md).

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

Apply configuration and restart Alertmanager.

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜  kubectl apply -f alertmanager-config.yaml 
configmap/alertmanager-config created

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main ➜ kubectl rollout restart deployment alertmanager -n monitoring
deployment.apps/alertmanager restarted

```
  
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
