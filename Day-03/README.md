# Day 03 — Kubernetes Deployment: FastAPI App with Readiness & Liveness Probes

This project demonstrates deploying a simple **FastAPI app** on **local Kubernetes** with **readiness** and **liveness probes**. The focus is on container orchestration, health management, and self-healing in Kubernetes — essential DevOps skills for production-ready deployments.

---

## Project Overview

The FastAPI app includes (Have added 3 new metrics: `/fail`. `/recover` and `/crash` [Day01](https://github.com/Janemils/Devops-Project-1/blob/main/Day-01/main.py])):

- `/health` → Health check endpoint (used by readiness probe)
- `/hello` → Demo endpoint (used by liveness probe)
- `/fail` → Temporarily fail the readiness probe
- `/recover` → Restore readiness probe to healthy state
- `/crash` → Kill the process to trigger liveness probe restart

**Key Features Implemented in Day 03:**

1. Kubernetes Deployment of a Dockerized FastAPI app
2. **Readiness probe** — determines if the pod is ready to serve traffic
3. **Liveness probe** — automatically restarts the pod if it becomes unhealthy
4. Manual testing of probe behaviors to simulate real-world scenarios

---

## Prerequisites

- Kubernetes cluster (local using `kind`, `minikube`, `k3s` or [kodekloud sandbox playground](https://kodekloud.com/playgrounds/playground-kubernetes-single-node-latest?_gl=1*qy56q*_gcl_au*ODYwODgwNDYwLjE3NzAzODgxNjEuNjA1MzA3MzQ4LjE3NzMyMDk5MTUuMTc3MzIwOTkyMg..*_ga*NTYwODA5OTcyLjE3MjYzNDY0MDg.*_ga_GNM9S6ZZKN*czE3NzM0NzU0MDEkbzMyMSRnMSR0MTc3MzQ3NTQxMiRqNDkkbDAkaDIzMTQ5MjI3*_ga_CGG6CZZ99B*czE3NzM0NzU0MDEkbzE0OCRnMSR0MTc3MzQ3NTQxMiRqNDkkbDAkaDQ5NDE2NzI4NQ..*_ga_T25WYDKNNV*czE3NzM0NzU0MDIkbzMzJGcxJHQxNzczNDc1NDEyJGo1MCRsMCRoMTM2Mjk0ODkxNQ..))
- kubectl CLI installed and configured
- FastAPI app container image built and pushed to Docker Hub (`janemils/janemils-app:fastapi-v3`)

---

## Kubernetes Deployment

### 1. Apply Deployment using the manifest file.

```bash
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl apply -f deployment.yaml 
deployment.apps/janemils-app-deployment created

controlplane Devops-Project-1/Day-03 on  main ➜  kubectl describe deploy
Name:                   janemils-app-deployment
Namespace:              default
CreationTimestamp:      Sat, 14 Mar 2026 08:02:38 +0000
Labels:                 app=janemils-app
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=janemils-app
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=janemils-app
  Containers:
   janemils-app:
    Image:         janemils/janemils-app:fastapi-v3
    Port:          8000/TCP
    Host Port:     0/TCP
    Liveness:      http-get http://:8000/hello delay=5s timeout=2s period=5s #success=1 #failure=3
    Readiness:     http-get http://:8000/health delay=3s timeout=2s period=5s #success=1 #failure=3
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   janemils-app-deployment-74c769d8d7 (1/1 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  2m34s  deployment-controller  Scaled up replica set janemils-app-deployment-74c769d8d7 from 0 to 1

controlplane Devops-Project-1/Day-03 on  main ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-74c769d8d7-89tfc   1/1     Running   0          2m55s

```

### 2. Expose the deployment to a service and port forward it to port 8000.

```bash
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl expose deployment janemils-app-deployment --port 8000 --target-port 8000
service/janemils-app-deployment exposed

controlplane Devops-Project-1/Day-03 on  main ✖ kubectl port-forward svc/janemils-app-deployment 8000:8000
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
```

OR.. You can also create the service from the service.yaml manifest file and do the port-forward.
```bash
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl apply -f service.yaml
service/janemils-app-service created

controlplane Devops-Project-1/Day-03 on  main ✖ kubectl port-forward svc/janemils-app-service 8000:8000
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
```

### 3. Test the readiness probe.

Now, open a new terminal and test the following things:

```bash
controlplane Devops-Project-1/Day-03 on  main ➜  curl http://localhost:8000/hello
{"message":"Hello from DevOps app"}
controlplane Devops-Project-1/Day-03 on  main ➜  curl http://localhost:8000/health
{"status":"ok"}

# Check the pod status:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-74c769d8d7-89tfc   1/1     Running   0          9m7s

# LEt's trigger the health check to fail.
controlplane Devops-Project-1/Day-03 on  main ➜  curl -X POST http://localhost:8000/fail
{"message":"health check failing"}
controlplane Devops-Project-1/Day-03 on  main ➜  curl http://localhost:8000/health
{"status":"fail"}

# Verify the readiness state of the pod:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-74c769d8d7-89tfc   0/1     Running   0          10m

# Verify the events log:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl describe po
..............
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  10m                default-scheduler  Successfully assigned default/janemils-app-deployment-74c769d8d7-89tfc to controlplane
  Normal   Pulled     10m                kubelet            spec.containers{janemils-app}: Container image "janemils/janemils-app:fastapi-v3" already present on machine and can be accessed by the pod
  Normal   Created    10m                kubelet            spec.containers{janemils-app}: Container created
  Normal   Started    10m                kubelet            spec.containers{janemils-app}: Container started
  Warning  Unhealthy  3s (x14 over 63s)  kubelet            spec.containers{janemils-app}: Readiness probe failed: HTTP probe failed with statuscode: 500

# As expected, the readiness probe has failed. Let's fix it by triggering the recover endpoint.
controlplane Devops-Project-1/Day-03 on  main ➜  curl -X POST http://localhost:8000/recover
{"message":"health restored"}
controlplane Devops-Project-1/Day-03 on  main ➜  curl http://localhost:8000/health
{"status":"ok"}

# Verify if pod is running now:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-74c769d8d7-89tfc   1/1     Running   0          12m
```


### 4. Test the liveness probe.

Now, open a new terminal and test the following things:

```bash
controlplane Devops-Project-1/Day-03 on  main ➜  curl http://localhost:8000/hello
{"message":"Hello from DevOps app"}

# Trigger the crash endpoint to kill the process.
controlplane Devops-Project-1/Day-03 on  main ➜  curl -X POST http://localhost:8000/crash
curl: (52) Empty reply from server

# Trigger the hello endpoint to check, if that works too.
controlplane Devops-Project-1/Day-03 on  main ✖ curl http://localhost:8000/hello
curl: (52) Empty reply from server

# Verify if the pod has been restarted:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl get po
NAME                                       READY   STATUS    RESTARTS      AGE
janemils-app-deployment-74c769d8d7-89tfc   1/1     Running   1 (21s ago)   14m

# Let's also see the event in the pod to check what happened:
controlplane Devops-Project-1/Day-03 on  main ➜  kubectl describe po
..........
Events:
  Type     Reason     Age                     From               Message
  ----     ------     ----                    ----               -------
  Normal   Scheduled  15m                     default-scheduler  Successfully assigned default/janemils-app-deployment-74c769d8d7-89tfc to controlplane
  Warning  Unhealthy  3m53s (x25 over 5m48s)  kubelet            spec.containers{janemils-app}: Readiness probe failed: HTTP probe failed with statuscode: 500
  Normal   Pulled     66s (x2 over 15m)       kubelet            spec.containers{janemils-app}: Container image "janemils/janemils-app:fastapi-v3" already present on machine and can be accessed by the pod
  Normal   Created    66s (x2 over 15m)       kubelet            spec.containers{janemils-app}: Container created
  Normal   Started    66s (x2 over 15m)       kubelet            spec.containers{janemils-app}: Container started


```
Since the process got killed, the liveness probe check failed (as /hello endpoint is not reachable) and that caused the pod to restart the container.




