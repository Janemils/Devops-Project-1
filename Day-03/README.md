# Day 03 — Kubernetes Deployment: FastAPI App with Readiness & Liveness Probes

This project demonstrates deploying a simple **FastAPI app** on **local Kubernetes** with **readiness** and **liveness probes**. The focus is on container orchestration, health management, and self-healing in Kubernetes — essential DevOps skills for production-ready deployments.

---

## Project Overview

The FastAPI app includes:

- `/health` → Health check endpoint (used by readiness and liveness probes)
- `/metrics` → Prometheus metrics endpoint
- `/hello` → Demo endpoint

**Key Features Implemented in Day 03:**

1. Kubernetes Deployment of a Dockerized FastAPI app
2. **Readiness probe** — determines if the pod is ready to serve traffic
3. **Liveness probe** — automatically restarts the pod if it becomes unhealthy
4. Manual testing of probe behaviors to simulate real-world scenarios

---

## Prerequisites

- Kubernetes cluster (local using `kind`, `minikube`, or `k3s`)
- kubectl CLI installed and configured
- Docker installed locally
- FastAPI app container image built and pushed to a registry as seen in Day-02 README.md.


---

## Kubernetes Deployment

### 1️⃣ Apply Deployment

```bash
kubectl apply -f Day-03/deployment.yaml
kubectl get pods -w
```

## Readiness & Liveness Probes

### Readiness Probe

- **Endpoint:** `/health`
- **Purpose:** Determines if the pod is ready to receive traffic.
- **Behavior:**
  - HTTP 200 → Pod marked **Ready**
  - HTTP 500 → Pod marked **NotReady** (removed from Service load balancer)
- Pod is **not restarted** if the readiness probe fails.

---

### Liveness Probe

- **Endpoint:** `/health`
- **Purpose:** Determines if the pod is alive and healthy.
- **Behavior:**
  - HTTP 200 → Pod is healthy
  - HTTP 500 → Pod is **restarted automatically**
- Ensures **self-healing** of unhealthy containers.

---

## 3️⃣ Testing Probes

### Test Readiness Probe

1. Temporarily modify `/health` to return HTTP 500:

```python
from fastapi.responses import JSONResponse

@app.get("/health")
async def health():
    return JSONResponse(status_code=500, content={"status": "fail"})
```

- Pod shows NotReady.
- Traffic is removed from Service (if a Service is used).
- Pod itself is still running. Revert /health to return HTTP 200 to mark pod as Ready again.

---

Test Liveness Probe

Trigger liveness failure:
```bash
kubectl exec -it <pod-name> -- curl http://localhost:8000/fail-liveness
```

Watch pod restart automatically:
```bash
kubectl get pods -w
```

Describe pod to view events:
```bash
kubectl describe pod <pod-name>
```

- Event log shows: Killing container with liveness probe failure, which in turn confirms self-healing behavior.
