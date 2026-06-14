# From Code to Production: A Practical DevOps Journey

*A hands-on project documenting how a simple application evolves into a production-ready platform through containerization, Kubernetes, Infrastructure as Code, GitOps, CI/CD, security, and observability.*

---

## Why This Project Exists

When learning DevOps, many tutorials focus on individual tools:

* Docker tutorials
* Kubernetes tutorials
* Terraform tutorials
* GitHub Actions tutorials

While useful, they often fail to show how these tools work together in a real deployment workflow.

This project was created to bridge that gap.

Starting with a minimal FastAPI application, each phase introduces a new DevOps concept and demonstrates how modern engineering teams build, deploy, secure, and operate applications in production environments.

The goal is not application development.

The goal is understanding the complete DevOps lifecycle.

---

## Who This Project Is For

This project is intended for:

* Students learning DevOps.
* Software engineers transitioning into DevOps roles.
* Platform Engineering beginners.
* Cloud and Kubernetes enthusiasts.
* Anyone wanting practical GitOps experience.

If you're comfortable writing a simple application but unsure how that application eventually reaches production, this project is designed to show that journey step-by-step.

---

## What You'll Learn

By following this project, you'll gain hands-on experience with:

### Application Development

* FastAPI
* Health checks
* Prometheus metrics

### Containerization

* Docker
* Multi-stage builds
* Image optimization

### Kubernetes

* Deployments
* Services
* Readiness probes
* Liveness probes

### Infrastructure as Code

* Terraform
* Kubernetes provider
* Resource management
  
### Continuous Delivery (CD)

* ArgoCD
* GitOps deployments
* Desired state management
* Continuous reconciliation

### Continuous Integration (CI)

* GitHub Actions
* Container image publishing
* Automated build workflows
* Manifest updates

---

## Project Evolution

| Day     | Topic                               |
| ------- | ----------------------------------- |
| [Day 01](https://github.com/Janemils/Devops-Project-1/tree/main/Day-01)  | FastAPI Application & Metrics.       |
| [Day 02](https://github.com/Janemils/Devops-Project-1/tree/main/Day-02)  | Docker Containerization.             |
| [Day 03](https://github.com/Janemils/Devops-Project-1/tree/main/Day-03)  | Kubernetes Deployment.               |
| [Day 04](https://github.com/Janemils/Devops-Project-1/tree/main/Day-04)  | Terraform (Infrastructure as Code).  |
| [Day 05](https://github.com/Janemils/Devops-Project-1/tree/main/Day-05)  | GitOps with ArgoCD.                  |
| [Day 06](https://github.com/Janemils/Devops-Project-1/tree/main/Day-06)  | CI with GitHub Actions.              |

---

## Architecture (Current)

```text
Developer
    ↓
GitHub Repository
    ↓
GitHub Actions
    ↓
GitHub Container Registry (GHCR)
    ↓
Update Kubernetes Manifest
    ↓
ArgoCD
    ↓
Kubernetes Cluster
    ↓
FastAPI Application
```

---

## Key Philosophy

The objective of this repository is not to showcase tools.

The objective is to understand the engineering decisions behind those tools:

* Why use Infrastructure as Code?
* Why GitOps instead of push-based deployments?
* Why immutable image tags?
* Why health probes matter?
* Why vulnerability scanning is required?
* Why observability is critical?

Every stage documents not only what was implemented, but also why it was implemented and what trade-offs were considered.

---

## Repository Structure

The project is organized by learning milestones rather than tools.

Each day introduces a new DevOps concept and contains the relevant code, configurations, documentation, troubleshooting notes, and engineering decisions for that stage of the journey.

This structure allows readers to follow the project incrementally, understand the reasoning behind each implementation, and observe how a simple application evolves into a production-ready platform.

---

## Final Outcome

By the end of this project, you'll have built and operated a complete application delivery pipeline:

* Application → Container
* Container → Kubernetes
* Infrastructure → Terraform
* Deployment → GitOps
* Automation → GitHub Actions

More importantly, you'll understand how these pieces fit together to form a modern production platform.
