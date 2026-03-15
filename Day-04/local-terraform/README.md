# Day 04 — Local Terraform Kubernetes Setup

## Overview

This project demonstrates deploying a Dockerized FastAPI application to a **local Kubernetes cluster (Kind)** using **Terraform**.  

Day-04 builds on the previous days (FastAPI app setup, Docker containerization, and manual Kubernetes deployment) by introducing **Infrastructure-as-Code (IaC)** to manage:

- Namespaces  
- Deployments  
- Services  

This ensures **reproducible, version-controlled infrastructure** and forms a foundation for CI/CD and production-ready automation.

---

## Features Implemented

- Terraform manages Kubernetes resources:
  - Namespace (`devops-demo`)  
  - Deployment (`janemils-app-deployment`) with readiness and liveness probes  
  - Service (`janemils-app-service`) to expose the application internally
- Docker image is pulled from **public Docker Hub registry** (`janemils/janemils-app:fastapi-v3`)  
- Readiness probe ensures **traffic is routed only to healthy pods**  
- Liveness probe ensures **automatic container restart on failure**  
- Terraform state tracks all resources, enabling:
  - `terraform apply` → create or update resources  
  - `terraform destroy` → remove resources cleanly

---

## Prerequisites

- Ubuntu or Linux-based VM (sandbox environment). I used the kodekloud [Ubuntu 22.04](https://kodekloud.com/playgrounds/playground-ubuntu-22-04?_gl=1*wd71cu*_gcl_au*ODYwODgwNDYwLjE3NzAzODgxNjEuNjA1MzA3MzQ4LjE3NzMyMDk5MTUuMTc3MzIwOTkyMg..*_ga*NTYwODA5OTcyLjE3MjYzNDY0MDg.*_ga_GNM9S6ZZKN*czE3NzM1NjQyMDAkbzMyMyRnMSR0MTc3MzU2NDI4NCRqMzYkbDAkaDE2OTg1ODk2ODY.*_ga_CGG6CZZ99B*czE3NzM1NjQyMDAkbzE1MCRnMSR0MTc3MzU2NDI4NCRqMzYkbDAkaDA.*_ga_T25WYDKNNV*czE3NzM1NjQyMDAkbzM1JGcxJHQxNzczNTY0Mjg0JGozNiRsMCRoMTM4Njk2Mzcy) sandbox for this.
- **Kind** for local Kubernetes cluster  
- **kubectl** configured to manage the Kind cluster  
- **Terraform v1.6+** installed  
- Docker installed and accessible for local image pulls  

If you are also using an Ubuntu-flavored VM, just execute these commands to install **Kind**, **kubectl**, **Terraform** and **Docker (optional)**, to meet the pre-requisite.

***Install Docker*** (Optional):
``` bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

***Install kubectl***:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

***Install Kind***:
``` bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.25.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind --version
```

***Install Terraform***:
```bash
sudo apt update
sudo apt install -y unzip
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  unzip -v
UnZip 6.00 of 20 April 2009, by Debian. Original by Info-ZIP.

curl -LO https://releases.hashicorp.com/terraform/1.6.4/terraform_1.6.4_linux_amd64.zip
ls -lh terraform_1.6.4_linux_amd64.zip

unzip terraform_1.6.4_linux_amd64.zip
ls -lh terraform

sudo mv terraform /usr/local/bin/
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ✖ terraform -v
Terraform v1.6.4
on linux_amd64
+ provider registry.terraform.io/hashicorp/kubernetes v3.0.1

Your version of Terraform is out of date! The latest version
is 1.14.7. You can update by downloading from https://www.terraform.io/downloads.html

# Cleanup:
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  rm terraform_1.6.4_linux_amd64.zip
```
---

## Folder Structure:
```
Day-04/local-terraform
├── deployment.tf # Deployment resource
├── namespace.tf # Namespace resource
├── service.tf # Service resource
├── variables.tf # Variable definitions
├── providers.tf # Initializing the kind cluster to create all the resources.
└── README.md
```


---

## Terraform Workflow

1. **Initialize Terraform:**

```bash

# Downloads required providers and sets up backend (state file):
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  terraform init 
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/kubernetes from the dependency lock file
- Using previously-installed hashicorp/kubernetes v3.0.1

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

────────────────────────────────────────────────────────────────────────────────────────────
# Shows what Terraform intends to create in the cluster.
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  terraform plan 

Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:
................
Plan: 3 to add, 0 to change, 0 to destroy.

────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take
exactly these actions if you run "terraform apply" now.

# Creates namespace, deployment, and service in the Kind cluster.
# Waits for pods to become ready before completing.

root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ✖ terraform apply -auto-approve

Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:
........................
Plan: 3 to add, 0 to change, 0 to destroy.
kubernetes_namespace_v1.devops-demo: Creating...
kubernetes_namespace_v1.devops-demo: Creation complete after 0s [id=devops-demo]
kubernetes_service_v1.devops_demo: Creating...
kubernetes_deployment_v1.devops-demo: Creating...
kubernetes_service_v1.devops_demo: Creation complete after 0s [id=devops-demo/janemils-app-service]
kubernetes_deployment_v1.devops-demo: Creation complete after 8s [id=devops-demo/janemils-app-deployment]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```
---

## Validate if the resources got created successfully:
```bash
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  kubectl get all -n devops-demo 
NAME                                           READY   STATUS    RESTARTS   AGE
pod/janemils-app-deployment-5f56f6b5fc-hszqx   1/1     Running   0          81s

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/janemils-app-service   ClusterIP   10.96.177.180   <none>        8000/TCP   81s

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/janemils-app-deployment   1/1     1            1           81s

NAME                                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/janemils-app-deployment-5f56f6b5fc   1         1         1       81s
```


```bash
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  kubectl port-forward svc/janemils-app-service 8000:8000 -n devops-demo
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000

────────────────────────────────────────────────────────────────────────────────────────────
# In another terminal, run these endpoints:

root@ubuntu-host ~ ✖ curl http://localhost:8000/health
{"status":"ok"}
root@ubuntu-host ~ ➜  curl http://localhost:8000/hello
{"message":"Hello from DevOps app"}
root@ubuntu-host ~ ➜  curl http://localhost:8000/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 823.0
python_gc_objects_collected_total{generation="1"} 185.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 121.0
python_gc_collections_total{generation="1"} 11.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="15",version="3.11.15"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 2.13516288e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 5.3260288e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.77357116327e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 1.1600000000000001
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 9.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/health",method="GET",status="200"} 26.0
http_requests_total{endpoint="/hello",method="GET",status="200"} 26.0
# HELP http_requests_created Total HTTP requests
# TYPE http_requests_created gauge
http_requests_created{endpoint="/health",method="GET",status="200"} 1.773571168241874e+09
http_requests_created{endpoint="/hello",method="GET",status="200"} 1.7735711682428796e+09
# HELP http_request_latency_seconds Request latency in seconds
# TYPE http_request_latency_seconds histogram
http_request_latency_seconds_bucket{le="0.005"} 52.0
http_request_latency_seconds_bucket{le="0.01"} 52.0
http_request_latency_seconds_bucket{le="0.025"} 52.0
http_request_latency_seconds_bucket{le="0.05"} 52.0
http_request_latency_seconds_bucket{le="0.075"} 52.0
http_request_latency_seconds_bucket{le="0.1"} 52.0
http_request_latency_seconds_bucket{le="0.25"} 52.0
http_request_latency_seconds_bucket{le="0.5"} 52.0
http_request_latency_seconds_bucket{le="0.75"} 52.0
http_request_latency_seconds_bucket{le="1.0"} 52.0
http_request_latency_seconds_bucket{le="2.5"} 52.0
http_request_latency_seconds_bucket{le="5.0"} 52.0
http_request_latency_seconds_bucket{le="7.5"} 52.0
http_request_latency_seconds_bucket{le="10.0"} 52.0
http_request_latency_seconds_bucket{le="+Inf"} 52.0
http_request_latency_seconds_count 52.0
http_request_latency_seconds_sum 0.06012415885925293
# HELP http_request_latency_seconds_created Request latency in seconds
# TYPE http_request_latency_seconds_created gauge
http_request_latency_seconds_created 1.773571167511748e+09
────────────────────────────────────────────────────────────────────────────────────────────

# Test the /fail endpoint.
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/fail
{"message":"health check failing"}
root@ubuntu-host ~ ➜  curl http://localhost:8000/health
{"status":"fail"}
root@ubuntu-host ~ ✖ kubectl get po -n devops-demo
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-5f56f6b5fc-dn24k   0/1     Running   0          3m10s

────────────────────────────────────────────────────────────────────────────────────────────
# Test the /recover endpoint.
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/recover
{"message":"health restored"}
root@ubuntu-host ~ ➜  curl http://localhost:8000/health
{"status":"ok"}
root@ubuntu-host ~ ➜  kubectl get po -n devops-demo
NAME                                       READY   STATUS    RESTARTS   AGE
janemils-app-deployment-5f56f6b5fc-dn24k   1/1     Running   0          3m26s

────────────────────────────────────────────────────────────────────────────────────────────
# Test the /crash endpoint.
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/crash
curl: (52) Empty reply from server

root@ubuntu-host ~ ✖ kubectl get po -n devops-demo
NAME                                       READY   STATUS    RESTARTS     AGE
janemils-app-deployment-5f56f6b5fc-dn24k   0/1     Running   1 (6s ago)   3m45s

root@ubuntu-host ~ ➜  kubectl get po -n devops-demo
NAME                                       READY   STATUS    RESTARTS     AGE
janemils-app-deployment-5f56f6b5fc-dn24k   1/1     Running   1 (9s ago)   3m48s

root@ubuntu-host ~ ➜  kubectl get deploy -n devops-demo
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
janemils-app-deployment   1/1     1            1           4m5s
```
---

## Delete the resources created by Terraform:
```bash
root@ubuntu-host Devops-Project-1/Day-04/local-terraform on  main [?] via 💠 default ➜  terraform destroy -auto-approve 
kubernetes_namespace_v1.devops-demo: Refreshing state... [id=devops-demo]
kubernetes_deployment_v1.devops-demo: Refreshing state... [id=devops-demo/janemils-app-deployment]
kubernetes_service_v1.devops_demo: Refreshing state... [id=devops-demo/janemils-app-service]

Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:
  - destroy
.................
Plan: 0 to add, 0 to change, 3 to destroy.
kubernetes_service_v1.devops_demo: Destroying... [id=devops-demo/janemils-app-service]
kubernetes_deployment_v1.devops-demo: Destroying... [id=devops-demo/janemils-app-deployment]
kubernetes_service_v1.devops_demo: Destruction complete after 0s
kubernetes_namespace_v1.devops-demo: Destroying... [id=devops-demo]
kubernetes_deployment_v1.devops-demo: Destruction complete after 0s
kubernetes_namespace_v1.devops-demo: Destruction complete after 6s



Destroy complete! Resources: 3 destroyed.
```

If you want to delete only like a certain resource, say for example, service, then run the following:
```bash
terraform destroy -target=kubernetes_service.app_service

# And then validate, if the resource actually got deleted:
terraform state list
```

Note: Only resources tracked in Terraform state can be destroyed.
Manually deleted resources are detected as drift and recreated on next apply.

---
***Key Learnings:***

- Terraform allows state-driven management of Kubernetes resources.
- Resource drift detection ensures deleted resources can be automatically recreated.
- Readiness and liveness probes are critical for traffic routing and pod self-healing.
- Local testing with Kind provides a production-like environment for validating Terraform manifests.

So, to wrap it up, this is how the workflow looks for a local-cluster setup:
```
Terraform
   │
   │ creates
   ▼
Namespace (devops-demo)
   │
   │ contains
   ▼
Deployment (janemils-app-deployment)
   │
   │ runs
   ▼
Pod(s) with FastAPI container
   │
   │ exposed via
   ▼
Service (janemils-app-service)
   │
   │ accessed locally via
   ▼
kubectl port-forward 8000:8000 → http://localhost:8000
```




