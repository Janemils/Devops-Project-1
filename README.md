# My DevOps App

**End-to-end DevOps project demonstrating CI/CD, Kubernetes, observability, security, and cost-aware infrastructure decisions.**

---

## Project Overview

This project simulates a small production-style service designed to demonstrate real-world DevOps practices.  
The goal is not to build a feature-rich application, but to focus on building reliable, observable, secure, and cost-conscious infrastructure around a minimal API.

The application evolves incrementally to showcase:
- Continuous Integration and Deployment (CI/CD)
- Containerization and Kubernetes orchestration
- Monitoring, logging, and alerting
- Security scanning and secrets management
- Cost optimization and resource awareness

Each stage of development is documented to highlight real engineering decisions, trade-offs, and lessons learned.

---

## Application

The application is a lightweight FastAPI service with the following endpoints:

- `/health` – simple health check returning `{"status": "ok"}`
- `/hello` – demo endpoint returning `{"message": "Hello from DevOps app"}`
- `/metrics` – Prometheus-compatible metrics exposing request counts and latency

The app is designed to be easily containerized, deployed to Kubernetes, and monitored using standard observability tools.

---

## Architecture Overview

High-level system design:

High-level Architecture:

        
                        ┌───────────────┐
                        │    Client     │
                        └──────┬────────┘
                               │
                               v
                        ┌───────────────┐
                        │  FastAPI App  │
                        └──────┬────────┘
                               │
                               v
                        ┌──────────────────┐
                        │ Docker Container │
                        └──────┬───────────┘
                               │
                               v
                        ┌────────────────────┐
                        │   Kubernetes Pod   │
                        └──────┬─────────────┘
                               │
               ┌───────────────┴────────────────┐
               │                                │
               v                                v
       ┌───────────────┐                 ┌───────────────┐
       │ Prometheus    │                 │ ELK (Logs)    │
       │ (Metrics)     │                 │               │
       └───────────────┘                 └───────────────┘


- CI/CD pipelines automate build, test, security scans, and deployment
- Observability integrates metrics, logging, and alerts
- Infrastructure can be provisioned via Terraform

---

## CI/CD Pipeline (Planned / WIP)

The CI/CD pipeline is designed to provide:
- Automated linting and unit tests
- Container image builds
- Security scanning (Trivy, Gitleaks)
- Deployment gating to local Kubernetes clusters (and optionally AKS)
- End-to-end testing with metrics verification

---

## Observability & Reliability

The project emphasizes production-style monitoring:
- **Metrics**: request counts, latency histograms
- **Logging**: structured logs aggregated in ELK stack
- **Alerting**: simulated incident handling to validate monitoring

This ensures the system can be debugged and maintained reliably.

---

## Security Considerations

Security best practices are integrated into the workflow:
- Container image scanning for vulnerabilities
- Secrets management via environment variables or ConfigMaps
- Minimal permissions applied to Kubernetes resources
- CI/CD pipeline blocks unsafe builds

---

## Cost Awareness

Even when deployed locally, resource usage and hypothetical cloud costs are considered:
- Kubernetes pods and nodes are sized realistically
- Auto-scaling behavior can be simulated
- Cost-optimization decisions and trade-offs are documented

---

## Documentation & Articles

Engineering decisions, debugging stories, and trade-offs are documented in `/docs`.  
Planned documents include:
- `/docs/architecture.md` – detailed architecture diagrams
- `/docs/ci-cd.md` – pipeline stages and reasoning
- `/docs/security.md` – scanning tools, secrets, and trade-offs
- `/docs/postmortem.md` – incident debugging stories
- `/docs/cost-optimization.md` – resource savings and cost reasoning

---

## Project Status

- Day 1: FastAPI application with `/health` and `/metrics` endpoints ✔️
- Subsequent days will expand containerization, CI/CD, monitoring, logging, alerting, and cloud deployment.

---

## Key Takeaway

This project prioritizes **DevOps thinking** over application complexity, demonstrating the ability to design, deploy, secure, and monitor production-ready systems.
