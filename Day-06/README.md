# Day 06 - GitHub Actions CI/CD Pipeline

> **Note**
>
> The actual GitHub Actions workflow for this project is located under:
>
> ```
> .github/workflows/ci.yaml
> ```
>
> GitHub only recognizes workflow files placed inside the `.github/workflows/` directory. Because of this limitation, the workflow itself cannot be stored inside the `Day-06/` folder.
>
> This directory exists solely to document the concepts, design decisions, implementation details, and lessons learned during Day 06 of the project.
>
> The implementation lives in `.github/workflows/ci.yaml`, while this README serves as the accompanying technical documentation.


**This is the github actions pipeline link: [WORKFLOW LINK](https://github.com/Janemils/Devops-Project-1/actions/workflows/ci.yaml).**

---
  
## Repository Structure

```text
Day-06/
└── README.md

.github/
└── workflows/
    └── ci.yaml
```
- *README.md* documents the CI/CD implementation and engineering decisions.
- *ci.yaml* contains the executable GitHub Actions workflow.
---
  
# GitHub Actions CI/CD Pipeline

## Overview

This GitHub Actions workflow automates the container build and deployment process for the application.

On every push to the `main` branch, the workflow:

1. Builds a Docker image.
2. Pushes the image to GitHub Container Registry (GHCR).
3. Updates the Kubernetes deployment manifest with the new image tag.
4. Commits the updated manifest back to the repository.
5. Allows ArgoCD to automatically deploy the new version.
6. Removes older container images from GHCR.

---

## Why GitHub Actions?

After containerizing the application (Day 02), deploying it to Kubernetes (Day 03), and managing infrastructure using Terraform (Day 04), the next logical step was automating the software delivery process.

The objective of this stage was to eliminate manual image builds and deployment updates by creating a repeatable CI/CD workflow capable of:

* Building application images automatically.
* Versioning images using immutable tags.
* Publishing images to a container registry.
* Updating Kubernetes manifests automatically.
* Supporting GitOps-based deployments through ArgoCD.

This forms the foundation for future stages involving security scanning, monitoring, and production-style deployment workflows.

---

## Workflow Trigger

```yaml
on:
  push:
    branches: [ main ]
```

The workflow runs automatically whenever changes are pushed to the `main` branch.

---

## Pipeline Stages

### 1. Checkout Repository

Downloads the latest source code into the GitHub Actions runner.

```yaml
uses: actions/checkout@v4
```

---

### 2. Authenticate with GHCR

Authenticates to GitHub Container Registry using the automatically generated `GITHUB_TOKEN`.

```bash
docker login ghcr.io
```

Required permissions:

```yaml
permissions:
  contents: write
  packages: write
```

---

### 3. Build Docker Image

Builds the application image using the Dockerfile created in Day 02.

```bash
docker build \
  -t ghcr.io/janemils/devops-project-1:${GITHUB_SHA} \
  -f Day-02/Dockerfile .
```

Each image is tagged using the commit SHA to ensure version traceability.

---

### 4. Push Image to GHCR

Pushes the newly built image to GitHub Container Registry.

```bash
docker push ghcr.io/janemils/devops-project-1:${GITHUB_SHA}
```

---

### 5. Update Kubernetes Manifest

Updates the image reference in the deployment manifest with the latest image tag.

Before:

```yaml
image: ghcr.io/janemils/devops-project-1:<old-tag>
```

After:

```yaml
image: ghcr.io/janemils/devops-project-1:<new-commit-sha>
```

This ensures the Git repository always contains the latest deployable version.

---

### 6. Commit Manifest Changes

Commits the updated deployment manifest back to the repository.

```bash
git add Day-03/deployment.yaml
git commit
git push
```

The commit message includes:

```text
[skip ci]
```

to prevent the workflow from triggering itself again.

---

### 7. GitOps Deployment

The workflow does **not** deploy directly to Kubernetes.

Instead:

```text
GitHub Actions
      ↓
Update deployment.yaml
      ↓
Push changes to Git
      ↓
ArgoCD detects changes
      ↓
Deploy to Kubernetes
```

This follows the GitOps model where Git remains the single source of truth.

---

### 8. Registry Cleanup

To prevent registry growth, older container images are automatically removed.

```yaml
min-versions-to-keep: 3
```

Only the latest three container images are retained.

---

## Workflow Summary

```text
Developer Pushes Code
          ↓
GitHub Actions Triggered
          ↓
Build Docker Image
          ↓
Push Image to GHCR
          ↓
Update Kubernetes Manifest
          ↓
Commit Changes to Git
          ↓
ArgoCD Detects Changes
          ↓
Deploy Updated Version
```

---

## Key Learnings

* GitHub Actions workflow automation.
* CI/CD pipeline fundamentals.
* GitHub Container Registry (GHCR).
* Immutable image versioning using commit SHAs.
* Automated Kubernetes manifest updates.
* GitOps deployment patterns with ArgoCD.
* Registry lifecycle management.
* Separation of CI responsibilities (GitHub Actions) and CD responsibilities (ArgoCD).

---

## Challenges Encountered

### Workflow Trigger Loops

Updating the deployment manifest from within the workflow caused a new Git commit, which could potentially trigger the pipeline again.

This was solved by including:

```text
[skip ci]
```

in the automated commit message.

### Private Container Registry Access

During development, image pulls required authentication because the repository and registry packages were private.

This highlighted the importance of registry permissions and image pull secrets when working with Kubernetes.

### Image Traceability

Using mutable tags such as `latest` makes rollbacks and troubleshooting difficult.

To address this, every image is tagged using the Git commit SHA, providing a clear link between deployed workloads and source code revisions.

