# Part 3 - Grafana Integration & Dashboard Creation

## Objective

Visualize Prometheus metrics through Grafana and build a production-style monitoring dashboard for the FastAPI application.

---

# Step 1: Install Grafana

Add the Grafana Helm repository:

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  helm repo add grafana https://grafana.github.io/helm-charts
"grafana" has been added to your repositories

controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "grafana" chart repository
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Install Grafana:

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  helm install grafana grafana/grafana \
  --namespace monitoring \
  --create-namespace
WARNING: This chart is deprecated
NAME: grafana
LAST DEPLOYED: Sun Jun 21 16:24:44 2026
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.monitoring.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace monitoring port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Grafana pod is terminated.                            #####
#################################################################################
```

Verify installation:

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  kubectl get pods -n monitoring
NAME                      READY   STATUS    RESTARTS   AGE
grafana-85f74b946-6x889   1/1     Running   0          84s
```
  
---

# Step 2: Access Grafana

Port-forward Grafana service:

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  kubectl port-forward svc/grafana 3000:80 -n monitoring
Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000
```

Now, you can open http://localhost:3000 in your browser. You should see something similar to the screenshot below.
<img width="1902" height="1150" alt="image" src="https://github.com/user-attachments/assets/e47d3131-03ae-4bd6-beea-262e265abcd0" />
  

If you see something like this, while accessing the grafana site in browser, just terminate the previous port-forward command and run the below command:
<img width="1912" height="561" alt="image" src="https://github.com/user-attachments/assets/b6bbc8f1-ea70-463d-8aff-184e55cce263" />

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main ✖ kubectl port-forward \
  --address 0.0.0.0 \
  svc/grafana \
  3000:80 \
  -n monitoring
Forwarding from 0.0.0.0:3000 -> 3000
```


Retrieve admin password:

```bash
controlplane Devops-Project-1/Day-08/Part-3:Grafana on  main [!?] ➜  kubectl get secret grafana -n monitoring \
-o jsonpath="{.data.admin-password}" | base64 -d
<you'll-get-the-admin-password>

```

Login:

```text
Username: admin
Password: <retrieved password>
```

---

# Step 3: Add Prometheus as Data Source

Before you proceed with this step, ensure you've prometheus running .You can follow [part-1](https://github.com/Janemils/Devops-Project-1/blob/main/Day-08/Part-1%3APrometheus/README.md) to set this up. Ensure that the service is port-forwarded.

Navigate to:

```text
Connections → Data Sources → Add Data Source
```
  
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/03c5e1f6-a8af-4ee0-b660-412ba67b7ff3" />
  
Select:

```text
Prometheus
```
  
<img width="1871" height="622" alt="image" src="https://github.com/user-attachments/assets/34231369-e813-422b-a4a4-cf34adc64b76" />


Configure URL:

```text
http://prometheus-server.monitoring.svc.cluster.local
```
  
<img width="1917" height="1102" alt="image" src="https://github.com/user-attachments/assets/9f844f9f-bfa6-46ca-86e9-1425ee0ba49c" />


Click:

```text
Save & Test
```
  
<img width="1912" height="1146" alt="image" src="https://github.com/user-attachments/assets/ccd6fec4-203e-4252-a57c-6366139c47a4" />


Expected:

```text
Data source is working
```

---

# Step 4: Initial Dashboard Validation

Create a new dashboard.
<img width="1822" height="1147" alt="image" src="https://github.com/user-attachments/assets/5fd3f1f0-ef6b-4680-9d8b-b41b39a59657" />
  
You can import the dashboard template and just change the db that you have setup.
<img width="1907" height="895" alt="image" src="https://github.com/user-attachments/assets/374f9558-a1ee-4d75-8d84-10108df14c7e" />


Or you can create your own dashboard.

Add a panel.

Query:

```promql
up
```

Result:

```text
1
```

This confirms:

* Grafana can communicate with Prometheus.
* Prometheus is successfully scraping targets.

---

# Step 5: Application Status Panel

Query:

```promql
up{job="janemils-app"}
```

Visualization:

```text
Stat
```

Meaning:

```text
1 = Application Healthy
0 = Application Unreachable
```

Testing:

Scale application down:

```bash
kubectl scale deployment janemils-app-deployment --replicas=0
```

Observe:

```promql
up{job="janemils-app"}
```

Expected:

```text
0
```

Scale back:

```bash
kubectl scale deployment janemils-app-deployment --replicas=1
```

Expected:

```text
1
```

---

# Step 6: Request Rate Panel

Query:

```promql
sum(rate(http_requests_total[5m]))
```

Visualization:

```text
Time Series
```

Purpose:

Displays requests per second received by the application.

Traffic Generation:

```bash
for i in {1..500}; do
  curl -s localhost:8000/hello > /dev/null
done
```

Expected:

Traffic graph rises.

Production Question:

```text
How much traffic is reaching the application?
```

---

# Step 7: Requests by Endpoint Panel

Query:

```promql
sum by (endpoint)(
  increase(http_requests_total[5m])
)
```

Visualization:

```text
Bar Chart
```

Purpose:

Shows endpoint popularity.

Example:

```text
/hello   100
/health   50
```

Production Question:

```text
Which API endpoints are most frequently used?
```

---

# Step 8: HTTP Status Distribution Panel

Query:

```promql
sum by (status)(
  http_requests_total{job="janemils-app"}
)
```

Visualization:

```text
Pie Chart
```

Purpose:

Displays request distribution by HTTP status code.

Example:

```text
200 -> 1200
404 -> 70
500 -> 5
```

Production Question:

```text
Are users encountering failures?
```

---

# Step 9: Understanding Delayed Metric Updates

Observation:

After generating traffic:

```bash
for i in {1..10}; do
  curl -s localhost:8000/doesnotexist > /dev/null
done
```

The metric did not update immediately.

Investigation:

```bash
kubectl exec -it -n monitoring deploy/prometheus-server -- \
grep scrape_interval /etc/config/prometheus.yml
```

Output:

```yaml
scrape_interval: 1m
```

Explanation:

Prometheus uses a pull model.

Flow:

```text
Request arrives
↓
Application updates metric
↓
Prometheus scrapes /metrics
↓
Prometheus stores new value
↓
Grafana displays update
```

Because scraping occurs every minute, metric changes may appear delayed.

Key Lesson:

```text
Application metrics update instantly.
Prometheus learns about them only during the next scrape.
```

---

# Step 10: Memory Usage Panel

Query:

```promql
process_resident_memory_bytes{
  job="janemils-app"
} / 1024 / 1024
```

Visualization:

```text
Time Series
```

Unit:

```text
Megabytes (MB)
```

Purpose:

Tracks application memory consumption.

Production Question:

```text
Is the application leaking memory?
```

---

# Step 11: CPU Usage Panel

Query:

```promql
rate(process_cpu_seconds_total{
  job="janemils-app"
}[5m])
```

Visualization:

```text
Time Series
```

Purpose:

Tracks CPU usage trends.

Load Generation:

```bash
for i in {1..5000}; do
  curl -s localhost:8000/hello > /dev/null
done
```

Expected:

CPU usage increases.

Production Question:

```text
Is the application under heavy load?
```

---

# Step 12: Error Monitoring

Generate 404 traffic:

```bash
for i in {1..20}; do
  curl -s localhost:8000/doesnotexist > /dev/null
done
```

Verify:

```promql
http_requests_total{status="404"}
```

Observation:

Metrics appeared after approximately one minute.

Root Cause:

Prometheus scrape interval was configured as:

```yaml
scrape_interval: 1m
```

Therefore metric collection was functioning correctly.

---

# Dashboard Panels Created

1. Application Status
2. Request Rate
3. Requests by Endpoint
4. HTTP Status Distribution
5. Memory Usage
6. CPU Usage

These panels collectively provide visibility into:

* Availability
* Traffic
* Errors
* Resource Consumption

which align with the core observability principles used in production environments.

---

# Key Learnings

* Grafana never talks directly to the application.
* Grafana queries Prometheus.
* Prometheus scrapes the application.
* Scrape intervals affect dashboard freshness.
* Counters should usually be visualized using `rate()` or `increase()`.
* Observability issues often originate from instrumentation rather than Prometheus itself.
* A small set of well-designed panels can provide meaningful production visibility.

