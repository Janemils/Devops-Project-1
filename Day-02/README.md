# Day 02 – Dockerizing FastAPI App.

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

> **Key Idea:** Multi-stage builds separate the heavy build environment from the runtime environment, reducing image size and improving security.

---

## Building the Docker Image

From the `Day02/` folder, run:

```bash
# To build your Dockerfile.
docker build -t fast-api:latest_img -f Dockerfile ../Day-01
```
---
```bash
# Verify your image.
➜ docker images
REPOSITORY   TAG          IMAGE ID       CREATED          SIZE
fast-api     latest_img   c9072caee3c3   16 seconds ago   140MB
python       3.11-slim    4b9bdfe9d486   40 hours ago     124MB

# Run your image with an appropriate tag and expose the ports.
➜  docker run --name fastapi-app -p 8000:8000 fast-api:latest_img 
```
<img width="981" height="248" alt="image" src="https://github.com/user-attachments/assets/1dca077d-a822-46be-9f8f-fc86ac092030" />

---

Now that your app is running, you can test out your endpoints to cross-verify:



---

## Push the image to the registry.
We will be using the dockerhub registry. <https://hub.docker.com/>

```bash
# Login to your docker account.
admin@docker-host ➜  docker login

USING WEB-BASED LOGIN
To sign in with credentials on the command line, use 'docker login -u <username>'

Your one-time device confirmation code is: .........

# Follow as per the rest of the steps to login.
```

```bash
# Tag your image that you want to push to your registry and push the image.
admin@docker-host ➜  docker tag fastapi-api:latest_img janemils/janemils-app:fastapi-<version-number>
admin@docker-host ➜  docker push janemils/janemils-app:fastapi-v1
```

Validate, whether your image actually got pushed to the registry:

<img width="897" height="682" alt="image" src="https://github.com/user-attachments/assets/992ddf67-054b-422a-a6ee-f7e2842c5f13" />


This step is important for day-03 as we will be using the image from the registry.





