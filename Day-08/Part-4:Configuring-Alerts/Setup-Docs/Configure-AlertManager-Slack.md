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

```bash
controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl apply -f alertmanager-config.yaml
configmap/alertmanager-config created

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl get cm -n monitoring 
NAME                  DATA   AGE
alertmanager-config   1      18s
kube-root-ca.crt      1      19m
prometheus-server     6      18m

```

## Deploy and Run your alertmanager.

```bash

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl apply -f alertmanager-deployment.yaml 
deployment.apps/alertmanager created

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl get deploy
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
janemils-app-deployment   1/1     1            1           20m

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl get po -n monitoring 
NAME                                                 READY   STATUS    RESTARTS   AGE
alertmanager-58fbb68559-4hg4q                        1/1     Running   0          4s
prometheus-kube-state-metrics-75866fb88d-spmkq       1/1     Running   0          22m
prometheus-prometheus-pushgateway-74b59b7bb9-7fn87   1/1     Running   0          22m
prometheus-server-5b7cb6b8b7-lb6p6                   2/2     Running   0          22m

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl apply -f alertmanager-service.yaml
service/alertmanager created

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ✖ kubectl get svc -n monitoring
NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
alertmanager                        ClusterIP   172.20.163.101   <none>        9093/TCP   13m
prometheus-kube-state-metrics       ClusterIP   172.20.114.102   <none>        8080/TCP   23m
prometheus-prometheus-pushgateway   ClusterIP   172.20.61.223    <none>        9091/TCP   23m
prometheus-server                   ClusterIP   172.20.11.100    <none>        80/TCP     23m

controlplane Devops-Project-1/Day-08/Part-4:Configuring-Alerts on  main [!?] ➜  kubectl port-forward svc/alertmanager 9093:9093 -n monitoring
Forwarding from 127.0.0.1:9093 -> 9093
Forwarding from [::1]:9093 -> 9093

```

## Test Notification Delivery

Trigger a Prometheus alert.

Example:

for i in {1..20}; do
curl http://localhost:8000/error
done

Slack should receive the notification.
