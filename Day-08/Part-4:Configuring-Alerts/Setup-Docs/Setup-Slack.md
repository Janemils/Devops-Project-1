# Slack Integration for Alertmanager

This guide explains how to create a Slack workspace, configure an incoming webhook, and integrate Alertmanager with Slack notifications.

---

## Step 1: Create a Slack Workspace

1. Visit https://slack.com/get-started
2. Click **Create a New Workspace**
3. Sign up using an email address.
4. Verify your email.
5. Choose a workspace name.

Example:

```text
janemils-devops-alerts
```

---

## Step 2: Create a Channel

Create a dedicated channel for Alertmanager notifications.

Example:

```text
YOUR_CHANNEL_NAME
```

This channel will receive all Prometheus alerts.

---

## Step 3: Create a Slack App

1. Visit:

```text
https://api.slack.com/apps
```
  
2. Click:

```text
Create New App
```
<img width="1830" height="531" alt="image" src="https://github.com/user-attachments/assets/a975b444-4d68-4003-bc0b-957e244cf100" />
  
3. Select:

```text
From Scratch
```
<img width="508" height="347" alt="image" src="https://github.com/user-attachments/assets/f43f28bc-84eb-4e6a-8073-d52a092e8597" />
  
4. Enter:

```text
App Name: Alertmanager
Workspace: Your Workspace
```
<img width="497" height="527" alt="image" src="https://github.com/user-attachments/assets/63883f3c-085f-4676-b62f-af66d85fabfc" />
  
5. Click:

```text
Create App
```
<img width="1895" height="612" alt="image" src="https://github.com/user-attachments/assets/dbc33ac1-ba8c-4330-94a7-9cf5052340d3" />
  

---

## Step 4: Enable Incoming Webhooks

Inside the Slack App:

1. Navigate to:

```text
Features
→ Incoming Webhooks
```

2. Enable:

```text
Activate Incoming Webhooks
```
<img width="1902" height="770" alt="image" src="https://github.com/user-attachments/assets/ac577662-6119-44f3-864e-c52356f28807" />

---

## Step 5: Create a Webhook URL

1. Click:

```text
Add New Webhook to Workspace
```

2. Select the target channel:

```text
YOUR_CHANNEL_NAME
```

3. Click:

```text
Allow
```
<img width="1825" height="700" alt="image" src="https://github.com/user-attachments/assets/5dcfe102-be54-4046-98dd-6a4a28bea233" />

Slack will generate a webhook URL similar to:

```text
YOUR_SLACK_WEBHOOK
```

Copy this URL.
