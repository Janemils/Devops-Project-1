# Day-05: CI/CD Evolution: From Push-Based to GitOps:

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

If you have a persistent cluster, you can always go ahead with the traditional approach. I just chose to go with approach as this is more suitable for my cluster setup.

### How to implement Day-05:
Pre-requisite:
- You need to have a kubernetes cluster setup ready. I used the [kodekloud](https://kodekloud.com/playgrounds/playground-kubernetes-single-node-latest?_gl=1*4kgt29*_gcl_au*ODYwODgwNDYwLjE3NzAzODgxNjEuMTYwMjE2NjIzOC4xNzczOTExMTUwLjE3NzM5MTE2NTE.*_ga*NTYwODA5OTcyLjE3MjYzNDY0MDg.*_ga_GNM9S6ZZKN*czE3NzQxMDMwOTAkbzMzMyRnMCR0MTc3NDEwMzA5MCRqNjAkbDAkaDU3NTY2NTcyNg..*_ga_CGG6CZZ99B*czE3NzQxMDMwOTAkbzE2NCRnMCR0MTc3NDEwMzA5MCRqNjAkbDAkaDM3MTE1NzI1Nw..*_ga_T25WYDKNNV*czE3NzQxMDEwNDckbzQ0JGcxJHQxNzc0MTAxMDU4JGo0OSRsMCRoMTY2NTgzMDE3MQ..) sandbox for my cluster setup.
Clone the Day-05 in your workspace (your cluster) and run the install_argocd.sh file to install the required dependencies and the argocd server:
```bash
controlplane Devops-Project-1/Day-05 on  main ➜  ./install_argocd.sh
Installing ArgoCD...
namespace/argocd created
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/applicationsets.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/appprojects.argoproj.io created
serviceaccount/argocd-application-controller created
serviceaccount/argocd-applicationset-controller created
serviceaccount/argocd-dex-server created
serviceaccount/argocd-notifications-controller created
serviceaccount/argocd-redis created
serviceaccount/argocd-repo-server created
serviceaccount/argocd-server created
role.rbac.authorization.k8s.io/argocd-application-controller created
role.rbac.authorization.k8s.io/argocd-applicationset-controller created
role.rbac.authorization.k8s.io/argocd-dex-server created
role.rbac.authorization.k8s.io/argocd-notifications-controller created
role.rbac.authorization.k8s.io/argocd-server created
clusterrole.rbac.authorization.k8s.io/argocd-application-controller created
clusterrole.rbac.authorization.k8s.io/argocd-server created
rolebinding.rbac.authorization.k8s.io/argocd-application-controller created
rolebinding.rbac.authorization.k8s.io/argocd-applicationset-controller created
rolebinding.rbac.authorization.k8s.io/argocd-dex-server created
rolebinding.rbac.authorization.k8s.io/argocd-notifications-controller created
rolebinding.rbac.authorization.k8s.io/argocd-server created
clusterrolebinding.rbac.authorization.k8s.io/argocd-application-controller created
clusterrolebinding.rbac.authorization.k8s.io/argocd-server created
configmap/argocd-cm created
configmap/argocd-cmd-params-cm created
configmap/argocd-gpg-keys-cm created
configmap/argocd-notifications-cm created
configmap/argocd-rbac-cm created
configmap/argocd-ssh-known-hosts-cm created
configmap/argocd-tls-certs-cm created
secret/argocd-notifications-secret created
secret/argocd-secret created
service/argocd-applicationset-controller created
service/argocd-dex-server created
service/argocd-metrics created
service/argocd-notifications-controller-metrics created
service/argocd-redis created
service/argocd-repo-server created
service/argocd-server created
service/argocd-server-metrics created
deployment.apps/argocd-applicationset-controller created
deployment.apps/argocd-dex-server created
deployment.apps/argocd-notifications-controller created
deployment.apps/argocd-redis created
deployment.apps/argocd-repo-server created
deployment.apps/argocd-server created
statefulset.apps/argocd-application-controller created
networkpolicy.networking.k8s.io/argocd-application-controller-network-policy created
networkpolicy.networking.k8s.io/argocd-applicationset-controller-network-policy created
networkpolicy.networking.k8s.io/argocd-dex-server-network-policy created
networkpolicy.networking.k8s.io/argocd-notifications-controller-network-policy created
networkpolicy.networking.k8s.io/argocd-redis-network-policy created
networkpolicy.networking.k8s.io/argocd-repo-server-network-policy created
networkpolicy.networking.k8s.io/argocd-server-network-policy created
Waiting for ArgoCD server to be ready...
deployment.apps/argocd-server condition met
Patching ArgoCD server to run in insecure mode...
deployment.apps/argocd-server patched
deployment.apps/argocd-server restarted
Waiting for patched server...
Waiting for deployment "argocd-server" rollout to finish: 0 out of 1 new replicas have been updated...
Waiting for deployment "argocd-server" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "argocd-server" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "argocd-server" rollout to finish: 1 old replicas are pending termination...
deployment "argocd-server" successfully rolled out
 Starting port-forward...
Forwarding from 0.0.0.0:8081 -> 8080
ArgoCD Login:
Username: admin
Password:
<Admin-password>
```

Make a note of the username and the password obtained in the above output.

In the secrets.yaml and secrets_1.yaml manifest files, add the repo url, your github username and password.
Now, create the secret using the manifest files.
```bash
# NOTE: This step is only cause, the repo is private for now. Once the repo is public, this step can be ignored."
controlplane Devops-Project-1/Day-05 on  main [?] ➜  kubectl apply -f secrets.yaml 
secret/repo-devops-project created

controlplane Devops-Project-1/Day-05 on  main [?] ➜  kubectl apply -f secrets_1.yaml
secret/repo-devops-project created

# Validate if both your secret is created successfully.
controlplane Devops-Project-1/Day-05 on  main ➜  kubectl get secret -n argocd
NAME                          TYPE     DATA   AGE
argocd-initial-admin-secret   Opaque   1      23m
argocd-notifications-secret   Opaque   0      23m
argocd-secret                 Opaque   5      23m
repo-devops-project           Opaque   3      11m

controlplane ~ ➜  kubectl get secrets
NAME                  TYPE                             DATA   AGE
secret-repo-deploy   kubernetes.io/dockerconfigjson   1      7m51s
```

Now, let's deploy the argocd application using the argocd-app.yaml manifest file.

```bash
controlplane Devops-Project-1/Day-05 on  main ➜  kubectl apply -f argocd-app.yaml 
application.argoproj.io/devops-project created

# Validate if the application is running successfully and if it's healthy and synced.
controlplane Devops-Project-1/Day-05 on  main [?] ➜  kubectl get application -n argocd
NAME             SYNC STATUS   HEALTH STATUS
devops-project   Synced        Healthy
```

Now, let's log in to the argocd app.
In the argocd-repo-server, we can see that the app is launched in port 8081. So, you should be able to access your app through port 8081.
<img width="1250" height="42" alt="image" src="https://github.com/user-attachments/assets/3ce28b1c-6eb3-44a7-b7aa-23e36aa1a0cc" />

Enter the username and the password credentials that you've noted above:
<img width="1917" height="982" alt="image" src="https://github.com/user-attachments/assets/35a2b65c-7f1d-4b11-8a3e-55e24af2769d" />

On successful login, you should be taken to a landing dashboard that looks something similar to this.
<img width="1917" height="995" alt="image" src="https://github.com/user-attachments/assets/ae5b4390-3925-4fe0-8319-42d5d3016f05" />

You can view further details of our resources and application by clicking on the 'devops-project'.
<img width="1898" height="1031" alt="image" src="https://github.com/user-attachments/assets/994d1a4a-21ca-477a-969a-ee0991d35f6e" />

Now, to test out, if argocd actually picks up the changes made in the repo and does syncing within itself and keep it up to date, I am going to make a change in this readme file and commit the changes to main.

As of now, you can see that the it's synced to the commit [f1ac487](https://github.com/Janemils/Devops-Project-1/commit/f1ac487a60c1583dd99e81f867d377bce508e511) :
<img width="1910" height="983" alt="image" src="https://github.com/user-attachments/assets/93dda254-9993-46c6-9407-c55873c3a5fe" />

Now, I am going to save the changes in the readme file and push and merge this commit to my main branch. As seen in the below screenshot, argocd has picked up the latest commit (1d55d39)[https://github.com/Janemils/Devops-Project-1/commit/1d55d395b79b6d1d9687a6aa7dec59008f1c35cd]
<img width="1610" height="992" alt="image" src="https://github.com/user-attachments/assets/6a724568-584f-4b14-8922-ee85bfb86af1" />
<img width="1903" height="987" alt="image" src="https://github.com/user-attachments/assets/82ffc0de-8635-44c9-8380-26b204c2ee46" />


Argocd is tested and working as expected.
Now, any changes we make in our repo, will be picked up by argocd and synced.
You can see that argocd has synced with the latest version of master automatically and is now up and running with the latest commit.



