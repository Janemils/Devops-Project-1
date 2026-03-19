# CI/CD Evolution: From Push-Based to GitOps:

## Current Architecture (GitOps with ArgoCD):

This project uses a **GitOps-based deployment model** with ArgoCD for Continuous Deployment and GitHub Actions for Continuous Integration.

### Workflow:

1. Developer pushes code to the application repository.
2. GitHub Actions (CI):
   - Runs linting and tests.  
   - Builds Docker image.  
   - Pushes image to container registry, in my case, I am using DockerHub. 
   - Updates Kubernetes manifests repository with new image tag.[  
3. ArgoCD (running inside Kubernetes cluster, in my case, it's the ephemeral sandbox):
   - Continuously monitors the manifests repository [the current repo].  
   - Pulls changes and synchronizes cluster state to match the latest one in repo.  

### Key Benefits:

- Improved security (no cluster credentials in CI). No need of configuring secrets in Github.  
- Declarative deployments (Git as source of truth).  
- Automatic drift detection and self-healing.  
- Resilient to ephemeral cluster environments. This is a huge benefit with my cluster setup as, I bring up my cluster in the Kodekloud sandbox, which will be available only for an hour or 2, hence ephemeral.  

---

## Initial Approach: Push-Based CI/CD:

Initially, I was planning to use a traditional **push-based deployment model**, where GitHub Actions directly deployed to the Kubernetes cluster.

### Workflow

1. Developer pushes code  
2. GitHub Actions:
   - Builds Docker image  
   - Uses `kubectl` to deploy directly to the cluster  

### Some of the Challenges Faced:

- **Ephemeral Cluster Issues**  
  The Kubernetes cluster had a limited lifetime, causing frequent changes in kubeconfig and breaking the pipeline.

- **Security Concerns**  
  Cluster credentials (kubeconfig) had to be stored in GitHub Secrets, increasing risk.

- **Tight Coupling**  
  CI pipeline was tightly coupled with the cluster, making deployments fragile and harder to maintain.

- **No Drift Detection**  
  Manual changes in the cluster were not detected or reverted.

---

## Key Insight

The core issue was not tooling, but architecture.

The CI pipeline was directly interacting with the cluster, creating a tightly coupled and fragile system. This made it difficult to handle dynamic environments and raised security concerns.

---

##  Why GitOps (ArgoCD)?

To address these challenges, I had to change my approach and transition to a **pull-based GitOps model using ArgoCD** approach.

### Architectural Shift

From:

CI → Kubernetes Cluster

To:

CI → Git → ArgoCD → Kubernetes Cluster

---

## Final Outcome:

The system is now:

- **Declarative** → All infrastructure defined in Git.  
- **Secure** → No direct cluster access from CI.  
- **Resilient** → Handles ephemeral clusters via automated bootstrap.  
- **Scalable** → Easily extendable to multi-environment setups.  

---

## Key Learnings:

- Importance of separating CI and CD responsibilities.
- Differences between push-based and pull-based deployment models.  
- Practical implementation of GitOps using ArgoCD.
- Handling ephemeral infrastructure through automation.  
- Security implications of exposing cluster credentials in CI.

If you have a persistent cluster, you can always go ahead with the traditional approach.I just chose to go with approach as this is more suitable for my cluster setup.
