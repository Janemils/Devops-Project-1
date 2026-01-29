# My DevOps FastAPI App

My minimal FastAPI application demonstrating **DevOps best practices** such as containerization readiness, monitoring with Prometheus, and CI/CD preparation.

---

## Overview

This app provides:

- **Health check**: `/health`  
- **Demo endpoint**: `/hello`  
- **Prometheus metrics**: `/metrics`  

All metrics are collected via middleware to track request counts and latency.

---

## Endpoints

| Endpoint            | Method | Description |
|--------------------|--------|-------------|
| `/health`           | GET    | Returns simple health status `{"status": "ok"}` |
| `/hello`            | GET    | Sample endpoint for generating traffic |
| `/metrics`          | GET    | Prometheus-f
| `/metrics-snapshot` | GET    | Developer-friendly snapshot of current request counts (local testing only)

============================================================================================================================================

HOW TO RUN THIS APP IN YOUR LOCAL:-

- Install dependencies:

pip install -r requirements.txt

============================================================================================================================================
- Run the app:

uvicorn main:app --reload --host 0.0.0.0 --port 8000
![alt text](image.png)

============================================================================================================================================

- Test endpoints:

# Health check
curl http://localhost:8000/health

# Basic hello endpoint
curl http://localhost:8000/hello

# Prometheus metrics
curl http://localhost:8000/metrics

# Debugging: current counts.
This endpoint is purely for debugging purpose only. Use it to validate if the http_request counts are being incremented successfully.

curl http://localhost:8000/metrics-snapshot
