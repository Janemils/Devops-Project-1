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
Push to main
      ↓
Build Docker Image
      ↓
Push Image to GHCR
      ↓
Update deployment.yaml
      ↓
Commit Changes
      ↓
ArgoCD Sync
      ↓
Deploy to Kubernetes
```

---

## Key Learnings

* GitHub Actions workflow automation.
* Container image lifecycle management.
* GitHub Container Registry (GHCR).
* Immutable image tagging using commit SHAs.
* Automated manifest updates.
* GitOps deployment using ArgoCD.
* Registry cleanup and maintenance.
