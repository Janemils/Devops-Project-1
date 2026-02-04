# Day 02 – Dockerizing FastAPI App

## Overview

On Day 02, we containerized the FastAPI application from Day 01 using a **multi-stage Docker build**.  
The goal is to create a small, efficient runtime image while keeping the build dependencies separate.

This container can run the FastAPI app and expose Prometheus metrics for monitoring.

---

## Dockerfile Explanation (Line-by-Line)

**Stage 1 – Builder Stage**

1. **Base image**: We use `python:3.11-slim` as the base for building dependencies. It’s lightweight and includes Python.  
2. **WORKDIR /app**: Sets the working directory inside the container. All subsequent commands run relative to this path.  
3. **Copy requirements.txt**: Only the dependencies file is copied first to optimize layer caching.  
4. **Install dependencies**: `pip install --prefix=/install -r requirements.txt` installs Python dependencies in a separate directory (`/install`) to keep the runtime image clean.

**Stage 2 – Runtime Stage**

5. **Base image**: We start again with a fresh `python:3.11-slim` image to reduce the final image size.  
6. **WORKDIR /app**: Sets the working directory for the runtime container.  
7. **Copy installed dependencies**: Dependencies from the builder stage are copied into `/usr/local` in the runtime image.  
8. **Copy application code**: All the app files (`main.py`, `metrics.py`) are copied into the runtime image.  
9. **Expose port 8000**: The container listens on port 8000 for incoming traffic.  
10. **Start the app**: `uvicorn` runs the FastAPI application, listening on all network interfaces (`0.0.0.0`) at port 8000.

> ✅ **Key Idea:** Multi-stage builds separate the heavy build environment from the runtime environment, reducing image size and improving security.

---

## Building the Docker Image

From the `Day02/` folder, run:

```bash
docker build -t fast-api:latest_img -f Dockerfile ../Day-01

