# From Code to Production: A Practical DevOps Journey:

*A hands-on project documenting how a simple FastAPI application evolves into a modern DevOps platform through containerization, Kubernetes, Infrastructure as Code, GitOps, CI/CD, security, observability, and networking.*

<img width="1100" height="733" alt="image" src="https://github.com/user-attachments/assets/71ae306e-f30f-4c48-a6a1-dc2ded5acfd3" />

---

# Why This Project Exists?

When learning DevOps, most tutorials focus on **individual tools**.

- Docker tutorials
- Kubernetes tutorials
- Terraform tutorials
- GitHub Actions tutorials
- ArgoCD tutorials
- Prometheus tutorials

Each tutorial teaches *how* to use a tool.

Very few explain **why the tool exists** or **how it fits into the bigger picture**.

I built this project because I wanted to answer one simple question:

> **"How does an application actually travel from a developer's laptop to production?"**

Instead of learning tools in isolation, this repository documents one continuous journey where every stage naturally introduces the next engineering problem to solve.

The goal isn't to build a complex application.

The goal is to understand the complete DevOps lifecycle.

---

# Who This Project Is For?

This project is intended for:

- Students learning DevOps.
- Software Test Engineers transitioning into DevOps.
- Platform Engineering beginners.
- Cloud & Kubernetes enthusiasts.
- Anyone who understands individual tools but struggles to connect them into one complete workflow.

If you've ever finished a Kubernetes tutorial and wondered,

> *"Okay... what happens next?"*

this project is for you.

---

# What You'll Learn:

## Application Development

- FastAPI
- Health endpoints
- Prometheus metrics

## Containerization

- Docker
- Multi-stage builds
- Image optimization

## Kubernetes

- Deployments
- Services
- Readiness Probes
- Liveness Probes

## Local Terraform Kubernetes Setup

- Terraform
- Kubernetes Provider
- Declarative resource management

## GitOps

- ArgoCD
- Desired State Management
- Continuous Reconciliation
- Automated Sync

## Continuous Integration

- GitHub Actions
- Automated Docker Builds
- GitHub Container Registry (GHCR)
- Manifest Updates

## DevSecOps

- Container vulnerability scanning
- Grype
- Shift-left security

## Monitoring & Observability

- Prometheus
- Grafana
- Alertmanager
- Slack Notifications

## Networking

- NGINX Ingress Controller
- Host-based Routing
- Kubernetes Ingress

---

# Project Evolution:

| Day | Topic |
|------|-------|
| [Day-01](https://github.com/Janemils/Devops-Project-1/tree/main/Day-01) | FastAPI Application |
| [Day-02](https://github.com/Janemils/Devops-Project-1/tree/main/Day-02) | Docker Containerization |
| [Day-03](https://github.com/Janemils/Devops-Project-1/tree/main/Day-03) | Kubernetes Deployment |
| [Day-04](https://github.com/Janemils/Devops-Project-1/tree/main/Day-04) | Local Terraform Kubernetes Setup |
| [Day-05](https://github.com/Janemils/Devops-Project-1/tree/main/Day-05) | GitOps with ArgoCD |
| [Day-06](https://github.com/Janemils/Devops-Project-1/tree/main/Day-06) | Continuous Integration with GitHub Actions |
| [Day-07](https://github.com/Janemils/Devops-Project-1/tree/main/Day-07) | DevSecOps with Grype |
| [Day-08](https://github.com/Janemils/Devops-Project-1/tree/main/Day-08) | Monitoring, Observability & Alerting |
| [Day-09](https://github.com/Janemils/Devops-Project-1/tree/main/Day-09) | Ingress & External Access |

---

# Current Architecture:

```text
                    Developer
                        │
                        ▼
                 GitHub Repository
                        │
        ┌───────────────┴───────────────┐
        ▼                               │
 GitHub Actions (CI)                    │
        │                               │
        ▼                               │
 GitHub Container Registry (GHCR)       │
        │                               │
        └────────── Updates Deployment Manifest
                        │
                        ▼
                     ArgoCD
                        │
                        ▼
                Kubernetes Cluster
                        │
        ┌───────────────┼─────────────────────────┐
        ▼               ▼                         ▼
    FastAPI App     Prometheus               Grafana
        │               │                         │
        │               ▼                         ▼
        │          Alertmanager ─────► Slack Alerts
        │
        ▼
NGINX Ingress Controller
        │
        ▼
      Users
```

---

# Repository Structure:

The repository is organized by **learning milestones**, not by tools.

Each day introduces one new DevOps concept while building on everything that came before.

Every folder contains:

- Source code
- Configuration files
- Documentation
- Screenshots
- Troubleshooting notes
- Engineering decisions

This allows readers to understand **not only what was built, but why it was built.**

---

# Engineering Philosophy:

This repository is **not** a collection of tool tutorials.

It is an attempt to understand the engineering decisions behind modern DevOps.

Throughout this project you'll find discussions around questions like:

- Why Docker before Kubernetes?
- Why Infrastructure as Code?
- Why GitOps instead of push-based deployments?
- Why immutable image tags?
- Why automate deployments?
- Why shift security left?
- Why monitor applications instead of waiting for users to report issues?
- Why expose services using an Ingress Controller?

Understanding **why** each technology exists is often more valuable than simply knowing **how** to use it.

---

# Final Outcome:

By the end of Version 1, you'll have followed the journey of an application through every major stage of a modern DevOps workflow:

```text
Application
      │
      ▼
Containerization
      │
      ▼
Kubernetes
      │
      ▼
Local Terraform Kubernetes Setup
      │
      ▼
GitOps
      │
      ▼
Continuous Integration
      │
      ▼
Security Scanning
      │
      ▼
Monitoring & Alerting
      │
      ▼
Ingress & External Access
```

More importantly, you'll understand **how these stages connect together** to form a production-inspired software delivery platform.

---

# Version 2:

Version 1 focuses on building a complete DevOps workflow locally using Kind.

Version 2 will expand the project by introducing cloud-native concepts, including:

- Azure Kubernetes Service (AKS)
- Cloud Infrastructure with Terraform
- HTTPS using cert-manager & Let's Encrypt
- Horizontal Pod Autoscaling (HPA)
- Kubernetes RBAC
- Advanced monitoring
- Production-grade GitOps
- Logging & Distributed Tracing
- Multi-environment deployments

📄 **Roadmap:** [Version-2.md](https://github.com/Janemils/Devops-Project-1/blob/main/roadmap-for-v2.md)

---

# Medium Article:

I also documented **why** I built this project and the lessons I learned throughout the journey.

📖 *[I Knew Docker. I Knew Kubernetes. I Still Didn’t Understand DevOps!](https://medium.com/@janemils/i-knew-docker-i-knew-kubernetes-i-still-didnt-understand-devops-138bc6230bac)*

---

# Contributions:

Suggestions, improvements, and feedback are always welcome.

If you find something that could be improved, feel free to:

- Open an Issue.
- Submit a Pull Request.
- Connect with me on [LinkedIn](www.linkedin.com/in/nileenajames).

Learning DevOps is a continuous journey, and I'd love to keep learning alongside the community.

---

## ⭐ If you found this project helpful...

Please consider giving the repository a **Star**.

It helps more learners discover the project and motivates me to continue building Version 2.

Thank you for stopping by! 🚀
