# Day-01: DevOps FastAPI App Project.

A FastAPI application exposing operational endpoints for health checks, metrics, and failure simulation, providing a practical foundation for learning observability, reliability, and deployment automation.

---

## Overview

This app provides:

- **Health check**: `/health` → returns `{"status":"ok"}` or `{"status":"fail"}` depending on `/fail` or `/recover` calls. Used by readiness probe.
- **Demo endpoint**: `/hello` → basic endpoint for generating traffic. Can also be used for liveness probe.
- **Prometheus metrics**: `/metrics` → exposes metrics for monitoring requests and latency.
- **Metrics snapshot**: `/metrics-snapshot` → developer-friendly snapshot of current request counts (local testing only).
- **Fail endpoint**: `/fail` (POST) → sets `/health` to fail (HTTP 500), simulating a pod NotReady state.
- **Recover endpoint**: `/recover` (POST) → restores `/health` to OK (HTTP 200), marking pod Ready.
- **Crash endpoint**: `/crash` (POST) → kills the application process immediately, triggering the liveness probe to restart the container.

All metrics are collected via middleware to track request counts and latency.

---

## Endpoints

| Endpoint            | Method | Description |
|--------------------|--------|-------------|
| `/health`           | GET    | Returns health status. Can return `{"status":"ok"}` or `{"status":"fail"}` depending on `/fail` or `/recover` calls. Used by **readiness probe**. |
| `/hello`            | GET    | Sample endpoint for generating traffic. Used by **liveness probe**. |
| `/metrics`          | GET    | Prometheus metrics endpoint for monitoring request counts and latency. |
| `/metrics-snapshot` | GET    | Developer-friendly snapshot of current request counts (local testing only). |
| `/fail`             | POST   | Sets the `/health` endpoint to return HTTP 500 → simulates pod not ready. |
| `/recover`          | POST   | Restores `/health` endpoint to return HTTP 200 → pod marked Ready again. |
| `/crash`            | POST   | Immediately kills the application process → triggers **liveness probe** to restart the container. |

The last three end-points `/fail`,`/recover` and `/crash` ar used extensively in [Day-03](https://github.com/Janemils/Devops-Project-1/tree/main/Day-03) to test out the liveness probe and the readiness probe.

============================================================================================================================================

  
## How to Run This App Locally:-

### Clone the repository first:
```bash
root@ubuntu-host ~ ➜  git clone https://github.com/Janemils/Devops-Project-1.git
Cloning into 'Devops-Project-1'...
Username for 'https://github.com': <enter-your-username>
Password for 'https://Janemils@github.com': <enter-your-PAT>
remote: Enumerating objects: 294, done.
remote: Counting objects: 100% (123/123), done.
remote: Compressing objects: 100% (77/77), done.
remote: Total 294 (delta 54), reused 79 (delta 28), pack-reused 171 (from 1)
Receiving objects: 100% (294/294), 18.30 MiB | 31.02 MiB/s, done.
Resolving deltas: 100% (95/95), done.

root@ubuntu-host ~ ➜  cd Devops-Project-1/Day-01

root@ubuntu-host Devops-Project-1/Day-01 on  main via 🐍 ➜  
```

### Install dependencies:
```bash
# Currently, I am in a virtual environment:
root@ubuntu-host Devops-Project-1/Day-01 on  main via 🐍 v3.12.3 (venv) ➜  pip install -r requirements.txt
Collecting annotated-doc==0.0.4 (from -r requirements.txt (line 1))
  Downloading annotated_doc-0.0.4-py3-none-any.whl.metadata (6.6 kB)
Collecting annotated-types==0.7.0 (from -r requirements.txt (line 2))
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
...................

# If successful, you should see these three packages:
root@ubuntu-host Devops-Project-1/Day-01 on  main via 🐍 v3.12.3 (venv) ➜  pip list
Package           Version
----------------- -------
fastapi           0.128.0
prometheus_client 0.24.1
uvicorn           0.40.0
```

**Troubleshooting Tip:**  
If you face this issue while running the above command:

> [!TIP]
> ### Issue: `pip: command not found`
> 
> **Error**
> ```bash
> -bash: pip: command not found
> ```
> 
> **Cause**
> Some minimal Ubuntu installations do not include `pip` or the packages required to create Python virtual environments by default.
> 
> **Resolution**
> Install `pip` and the required Python packages:
> ```bash
> sudo add-apt-repository universe
> sudo apt update
> sudo apt install python3-pip
> sudo apt install python3-full -y
> ```
> 
> Create and activate a virtual environment:
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> ```
> 
> Then install the project dependencies:
> ```bash
> pip install -r requirements.txt
> ```
> 
> **Why use a virtual environment?**  
> A virtual environment isolates project dependencies from the system Python installation, preventing version conflicts and ensuring a reproducible development setup.


============================================================================================================================================
### Run the app:
```bash
root@ubuntu-host Devops-Project-1/Day-01 on  main via 🐍 v3.12.3 (venv) ➜  uvicorn main:app --reload --host 0.0.0.0 --port 8000
INFO:     Will watch for changes in these directories: ['/root/Devops-Project-1/Day-01']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [5761] using StatReload
INFO:     Started server process [5769]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
![alt text](image.png)

============================================================================================================================================

### Test endpoints:
Now open a new terminal and let's test out all the endpoints:

# Health check
```bash
root@ubuntu-host ~ ➜  curl http://localhost:8000/health
{"status":"ok"}
```

# Basic hello endpoint
```bash
root@ubuntu-host ~ ➜  curl http://localhost:8000/hello
{"message":"Hello from DevOps app"}
```

# Prometheus metrics
```bash
root@ubuntu-host ~ ➜  curl http://localhost:8000/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 410.0
python_gc_objects_collected_total{generation="1"} 71.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 105.0
python_gc_collections_total{generation="1"} 9.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="12",patchlevel="3",version="3.12.3"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.34344704e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 4.5871104e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.78108209202e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.27
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 13.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/health",method="GET",status="200"} 1.0
http_requests_total{endpoint="/hello",method="GET",status="200"} 1.0
# HELP http_requests_created Total HTTP requests
# TYPE http_requests_created gauge
http_requests_created{endpoint="/health",method="GET",status="200"} 1.781082116288453e+09
http_requests_created{endpoint="/hello",method="GET",status="200"} 1.7810821407909093e+09
# HELP http_request_latency_seconds Request latency in seconds
# TYPE http_request_latency_seconds histogram
http_request_latency_seconds_bucket{le="0.005"} 2.0
http_request_latency_seconds_bucket{le="0.01"} 2.0
http_request_latency_seconds_bucket{le="0.025"} 2.0
http_request_latency_seconds_bucket{le="0.05"} 2.0
http_request_latency_seconds_bucket{le="0.075"} 2.0
http_request_latency_seconds_bucket{le="0.1"} 2.0
http_request_latency_seconds_bucket{le="0.25"} 2.0
http_request_latency_seconds_bucket{le="0.5"} 2.0
http_request_latency_seconds_bucket{le="0.75"} 2.0
http_request_latency_seconds_bucket{le="1.0"} 2.0
http_request_latency_seconds_bucket{le="2.5"} 2.0
http_request_latency_seconds_bucket{le="5.0"} 2.0
http_request_latency_seconds_bucket{le="7.5"} 2.0
http_request_latency_seconds_bucket{le="10.0"} 2.0
http_request_latency_seconds_bucket{le="+Inf"} 2.0
http_request_latency_seconds_count 2.0
http_request_latency_seconds_sum 0.0013682842254638672
# HELP http_request_latency_seconds_created Request latency in seconds
# TYPE http_request_latency_seconds_created gauge
http_request_latency_seconds_created 1.7810820925906413e+09
```


# To fail the health check:
```bash
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/fail
{"message":"health check failing"}

# Let's cross-verify if it actually failed:
root@ubuntu-host ~ ➜  curl http://localhost:8000/health
{"status":"fail"}

# We can also check from the application logs:
INFO:     127.0.0.1:43148 - "POST /fail HTTP/1.1" 200 OK
INFO:     127.0.0.1:59990 - "GET /health HTTP/1.1" 500 Internal Server Error
```

# To recover the failed health check:
```bash
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/recover
{"message":"health restored"}

# Let's cross-verify if it actually restored:
root@ubuntu-host ~ ➜  curl http://localhost:8000/health
{"status":"ok"}

# Application Logs:
INFO:     127.0.0.1:51266 - "POST /recover HTTP/1.1" 200 OK
INFO:     127.0.0.1:51280 - "GET /health HTTP/1.1" 200 OK
```

# To manipulate an internal server error:
```bash
root@ubuntu-host ~ ➜  curl  http://localhost:8000/error
{"details":"Internal Server Error"}

# Application Logs:
INFO:     127.0.0.1:59888 - "GET /error HTTP/1.1" 500 Internal Server Error
```

# To crash the application (i.e; just kill the process)
```bash
root@ubuntu-host ~ ➜  curl -X POST http://localhost:8000/crash
curl: (52) Empty reply from server

# Let's cross-verify if the application actually crashed:
root@ubuntu-host ~ ✖ curl http://localhost:8000/health

# This will hang as the application has crashed. This is expected. You can re-run the uvicorn command to get the application running again.
```

# Debugging: current counts.
This endpoint is purely for debugging purpose only. Use it to validate if the http_request counts are being incremented successfully.

curl http://localhost:8000/metrics-snapshot
