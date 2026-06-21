# Part 2: Exploring Application Metrics with Prometheus

The goal of this section is to understand how Prometheus metrics are used in real-world environments by simulating common production scenarios.

---

# Lab 1 — Availability Metrics
## Production Question

Is the application currently available?

## Goal

Understand:

```promql
up{job="janemils-app"}
```

---

## Baseline

Verify the application is currently reachable by Prometheus:

```bash
# Scale the replicas of the deployment to 0.
controlplane ~ ➜  kubectl scale deployment janemils-app-deployment --replicas=0
deployment.apps/janemils-app-deployment scaled

controlplane ~ ➜  kubectl get po
No resources found in default namespace.
```
Wait 15–30 seconds. Since, Prometheus can no longer scrape the application, the value will be 0.  
  
**Expected:**
  
The value of up instance must be 0 as the application is not currently running.
<img width="1000" height="303" alt="image" src="https://github.com/user-attachments/assets/bdea6a29-555a-43e5-80da-a3ede8ab4d93" />
Graphical representation of the data: <img width="1000" height="598" alt="image" src="https://github.com/user-attachments/assets/b86790c0-b832-4829-8f51-bfc02f0042fc" />
  

<br>
<br>

```bash
#  Scale the replicas of the deployment to 1.
controlplane ~ ➜  kubectl scale deployment janemils-app-deployment --replicas=1
deployment.apps/janemils-app-deployment scaled

controlplane ~ ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-765597dd97-kgrx2   1/1     Running   0          7s
```
Wait 15–30 seconds.  
  
**Expected:**
  
The value of up instance must be 1 as the application is currently running.
<img width="1000" height="297" alt="image" src="https://github.com/user-attachments/assets/c2953ce3-b722-4051-b844-502cf18af9ab" />
Graphical representation of the data: <img width="1000" height="594" alt="image" src="https://github.com/user-attachments/assets/a74eb353-6f1a-4fd8-a611-e1c1e1f88d88" /> 

---

# Lab 2 — Traffic Metrics
## Production Question

Are users actively using the application?

## Goal

Understand:

```promql
rate(http_requests_total[5m])
```

---

## Baseline

Run:

```promql
sum(rate(http_requests_total[5m]))
```

```promql
increase(http_requests_total[5m])
```

**Expected:**

<img width="1000" height="516" alt="image" src="https://github.com/user-attachments/assets/9e05a113-80a0-47de-a9de-23e4a77b0098" />
<img width="1000" height="339" alt="image" src="https://github.com/user-attachments/assets/e511a615-b5d5-46c2-ac94-672f9444cc2e" />


if little or no traffic exists.

---

## Generate Traffic

```bash
controlplane ~ ➜ for i in {1..20}; do
  curl -s localhost:8000/hello > /dev/null
done
```

---

## Observe

<img width="1000" height="491" alt="image" src="https://github.com/user-attachments/assets/109cffcc-fd95-4abe-b326-6fc6a50d895f" />
<img width="1000" height="407" alt="image" src="https://github.com/user-attachments/assets/eee482d6-99c8-4cef-932f-59a51e3d64a6" />

If you notice, the /hello endpoint should ideally show only 105 as 85+20 is 105, but, it's showing 110, because it keeps counting probe requests too and as seen in our deployment:
- /hello is called every 5 seconds by the kubelet
- /health is called every 5 seconds by the kubelet

So, by the time you refreshed Prometheus, another probe cycle would have likely happened.
---

# Lab 3 — Endpoint Usage
  
## Production Question

Which APIs are users calling most frequently?

## Goal

Identify which endpoint receives the most traffic.

---
  
## Baseline:
  
<img width="1000" height="443" alt="image" src="https://github.com/user-attachments/assets/670a1d11-2218-4d69-8d15-77414d3da30f" />

  
## Generate Traffic

```bash
controlplane Devops-Project-1/Day-08/Part-2:App-to-Prometheus on  main ➜  for i in {1..100}; do
  curl -s localhost:8000/hello > /dev/null
done

for i in {1..60}; do
  curl -s localhost:8000/health > /dev/null
done
```

---

## Observe

<img width="1000" height="437" alt="image" src="https://github.com/user-attachments/assets/cd1c1635-c079-4c02-939d-686b0610070d" />


## Expected:

```text
/hello   baseline+100
/health  baseline+50
```

---

# Lab 4 — Error Metrics
  
## Production Question

Are users experiencing errors?

## Goal

Track failed requests.

---

## Baseline:
  
<img width="1000" height="354" alt="image" src="https://github.com/user-attachments/assets/809e4204-8c80-4a32-a096-06fd8f46b5af" />


## Generate 404 Errors

```bash
controlplane Devops-Project-1/Day-08/Part-2:App-to-Prometheus on  main ➜  for i in {1..25}; do   curl -s localhost:8000/doesnotexist > /dev/null; done
```

---

## Observe

<img width="1000" height="336" alt="image" src="https://github.com/user-attachments/assets/2b317cd5-6876-490d-a47d-0365c284c372" />


## Expected:

```text
200 → some value
404 → some value
```

---
  

# Lab 5 — Crash Investigation
  
## Production Question

Are application containers restarting unexpectedly?

## Goal

Observe application crashes and restarts.

---

## Trigger Crash

```bash
controlplane ~ ➜  curl -X POST localhost:8000/crash
curl: (52) Empty reply from server

controlplane ~ ✖ ^C

controlplane ~ ✖ kubectl get pods
NAME                                       READY   STATUS    RESTARTS      AGE
janemils-app-deployment-765597dd97-kgrx2   1/1     Running   1 (77s ago)   45m

controlplane ~ ➜  curl -X POST localhost:8000/crash
curl: (52) Empty reply from server

controlplane ~ ➜  kubectl get pods
NAME                                       READY   STATUS    RESTARTS      AGE
janemils-app-deployment-765597dd97-kgrx2   1/1     Running   2 (19s ago)   47m
```

---

## Observe Restarts

<img width="1000" height="259" alt="image" src="https://github.com/user-attachments/assets/0839620c-4152-466f-b2ab-37481bae1f24" />

---

# Lab 6 — CPU Monitoring
  
## Production Question

Is the application under heavy load?

## Goal

Understand CPU utilization.

---

## Observe

```promql
rate(process_cpu_seconds_total[5m])
```

---

## Baseline:
  
<img width="1000" height="273" alt="image" src="https://github.com/user-attachments/assets/537122c9-dfca-4f0d-acad-d93e46a41504" />


## Generate Load

Open another terminal:

```bash
controlplane ~ ➜  for i in {1..5000}; do
  curl -s localhost:8000/hello > /dev/null
done
```

---

## Observe Again

<img width="1000" height="356" alt="image" src="https://github.com/user-attachments/assets/763ee32e-cb9d-45e1-9152-0eb2f7ea44b3" />


## Expected:

CPU usage should increase.

---

# Key Takeaway

These exercises demonstrate the four Golden Signals commonly used by SRE and DevOps teams:

| Signal | Example Metric |
|----------|----------|
| Availability | `up` |
| Traffic | `http_requests_total` |
| Errors | `5xx error rate` |
| Saturation | CPU / Memory usage |

After completing these labs, you'll have practical experience using Prometheus to investigate availability issues, traffic patterns, application errors, crashes, CPU utilization, and memory consumption.

The next logical step is building Grafana dashboards to visualize these metrics instead of querying them manually through PromQL.
