# Day-08 Part-4: Alerting with Prometheus, Alertmanager, and Slack

## Objective

Implement production-style alerting for the FastAPI application using Prometheus metrics, Alertmanager, and Slack notifications.

---

## Architecture

FastAPI Application → Prometheus → Alertmanager → Slack

Prometheus scrapes application metrics from `/metrics`.

Alertmanager receives alert events from Prometheus and forwards notifications to Slack.

---

## Metrics Monitored

### Request Count

http_requests_total

Tracks total requests by:

* HTTP method
* Endpoint
* Status code

### Request Latency

http_request_latency_seconds

Tracks API response times.

---

## Alert Rules

### ApplicationDown

Triggers when the application becomes unreachable.

Expression:

absent(up{job="janemils-app"}) or up{job="janemils-app"} == 0

Severity:

critical

---

### HighErrorRate

Triggers when more than five HTTP 500 responses occur within five minutes.

Expression:

increase(http_requests_total{status="500"}[5m]) > 5

Severity:

warning

---

## Alertmanager Configuration

Alertmanager is configured with a Slack Incoming Webhook.

Notifications are delivered to:

YOUR_CHANNEL_NAME

---

## Testing

### Generate HTTP 500 Errors

curl http://localhost:8000/error

Repeated requests trigger the HighErrorRate alert.

### Simulate Application Failure

kubectl scale deployment janemils-app-deployment --replicas=0

This removes all application endpoints and triggers the ApplicationDown alert.

---

## Outcome

Successfully implemented:

* Prometheus Metrics Collection
* Alert Rules
* Alertmanager Routing
* Slack Notifications
* Failure Simulation
* Recovery Notifications

This setup demonstrates a complete monitoring and alerting workflow commonly used in production Kubernetes environments.

