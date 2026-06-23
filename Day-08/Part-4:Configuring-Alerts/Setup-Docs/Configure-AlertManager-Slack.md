# Alertmanager Slack Integration

This guide configures Alertmanager to send notifications to Slack.

## Update Alertmanager Configuration

Replace:

YOUR_SLACK_WEBHOOK_URL

with the webhook URL generated during Slack setup. You can refer [here](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-4%3AConfiguring-Alerts/Setup-Docs/Setup-Slack.md#step-5-create-a-webhook-url) as to how to get the webhook.

Example:

receivers:

* name: slack-notifications
  slack_configs:

  * api_url: 'YOUR_SLACK_WEBHOOK_URL'
    channel: 'YOUR_CHANNEL_NAME'
    send_resolved: true

## Apply Configuration

kubectl apply -f alertmanager-config.yaml

kubectl rollout restart deployment alertmanager -n monitoring

## Verify Alertmanager

kubectl get pods -n monitoring

kubectl logs -n monitoring deployment/alertmanager

## Test Notification Delivery

Trigger a Prometheus alert.

Example:

for i in {1..20}; do
curl http://localhost:8000/error
done

Slack should receive the notification.
