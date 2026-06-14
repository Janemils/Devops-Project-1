# Security & Vulnerability Management

Security is not a single tool or a one-time activity.

Modern DevOps practices integrate security throughout the software delivery lifecycle by continuously identifying vulnerabilities, preventing credential leaks, and enforcing security controls before software reaches production.

This section demonstrates how security can be incorporated into a CI/CD workflow using container image scanning, secret detection, and pipeline security gates.

---
  
  
# Part 1: Container Vulnerability Scanning (Grype)
  
The objective is to identify known vulnerabilities within the container image before deployment.
  
## - Why Grype?

Container vulnerability scanning is commonly performed using tools such as Trivy, Grype, Clair, and Snyk.

For this project, Grype was selected to gain hands-on experience with an alternative scanning solution and to better understand the vulnerability management process independent of any specific tool.

Grype provides:

- Container image vulnerability scanning
- CI/CD integration capabilities
- Policy-based security enforcement
- Lightweight installation and usage

The objective of this phase is not to compare scanners, but to understand how vulnerabilities are identified, assessed, and remediated within containerized workloads.

---

## - Installing Grype:-

### Linux

```bash
# Install Grype:
root@ubuntu-host ~ ➜  curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh

root@ubuntu-host ~ ➜  sudo mv ./bin/grype /usr/local/bin/

# Verify the version of grype installed:
root@ubuntu-host ~ ➜  grype version
Application:         grype
Version:             0.114.0
BuildDate:           2026-06-05T16:10:04Z
GitCommit:           ef8e65adb2dec760f1f923e635da4c7696d3c295
GitDescription:      v0.114.0
Platform:            linux/amd64
GoVersion:           go1.26.3
Compiler:            gc
Syft Version:        v1.45.1
Supported DB Schema: 6
```

---

## - Security Assessment Workflow

The security assessment followed the process below:

1. Scan the existing container image.
2. Review vulnerability findings.
3. Investigate affected packages.
4. Apply remediation.
5. Rebuild the image.
6. Validate improvements through rescanning.

---

## - Initial Scan Results (fastapi-v3)

The existing application image was scanned using Grype:

```bash
# Let's identify the critical and the high vulnerabilities of the 'janemils/janemils-app:fastapi-v3' image using grype.
root@ubuntu-host ~ ➜  grype janemils/janemils-app:fastapi-v3 --only-fixed | grep -E "High|Critical"
 ✔ Loaded image                                           janemils/janemils-app:fastapi-v3 
 ✔ Parsed image                    sha256:f2448c57f6d36309d03cfe51b17c54d103f32d8f811f19a92  
 ✔ Cataloged contents              eb3de8a439e428d95b2aba9379f0f9b256c85e9b5ba6db022d08a858  
   ├── ✔ Packages                        [127 packages]  
   ├── ✔ Executables                     [759 executables]  
   ├── ✔ File metadata                   [2,729 locations]  
   └── ✔ File digests                    [2,729 files]  
 ✔ Scanned for vulnerabilities     [114 vulnerability matches]  
   ├── by severity: 12 critical, 74 high, 72 medium, 14 low, 51 negligible
   └── by status:   114 fixed, 109 not-fixed, 109 ignored 
python                   3.11.15          3.15.0b2                    binary  CVE-2026-7210        Critical    0.2% (40th)    0.2    
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28389       High        0.1% (34th)    0.1    
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28389       High        0.1% (34th)    0.1    
............. (113 vulnerabilities.)

```
---

## - Analysis

The scan results suggested that many vulnerabilities originated from components inherited from the base image rather than the application code itself.

To validate this assumption, the base image was upgraded from Python 3.11 Slim to Python 3.13 Slim and the image was rebuilt.

After rebuilding and rescanning, the number of fixable High and Critical vulnerabilities dropped significantly, confirming that the base image version was a major contributor to the overall vulnerability count.

---

## - Remediation

The application image was originally built using:

```dockerfile
FROM python:3.11-slim
```

To reduce exposure to known vulnerabilities, the base image was upgraded to (latest stable version at the time of this update: 15-06-2026):

```dockerfile
FROM python:3.13-slim
```

The image was rebuilt, pushed to dockerhub and published as:

```text
janemils/janemils-app:fastapi-v4
```

The Kubernetes deployment manifests and Terraform configuration were updated to reference the remediated image version.

Changes were then committed and deployed through the existing GitOps workflow.

---

## - Validation Scan Results (fastapi-v4):

The updated image was rescanned using Grype:

```bash
#  Let's identify the critical and the high vulnerabilities of the 'janemils/janemils-app:fastapi-v4' image using grype.
root@ubuntu-host Devops-Project-1 on  main [!?] ➜  grype janemils/janemils-app:fastapi-v4 --only-fixed | grep -E "High|Critical"
 ✔ Loaded image                                           janemils/janemils-app:fastapi-v4 
 ✔ Parsed image                    sha256:f9d242eb6987413af266d8ae0803791d65b28e6916b3ec550  
 ✔ Cataloged contents              07c7e2c0a20176464a70279cc3f910c0a229e6fb3fa9b1bc03c15c1f  
   ├── ✔ Packages                        [109 packages]  
   ├── ✔ Executables                     [752 executables]  
   ├── ✔ File metadata                   [2,681 locations]  
   └── ✔ File digests                    [2,681 files]  
 ✔ Scanned for vulnerabilities     [9 vulnerability matches]  
   ├── by severity: 6 critical, 18 high, 40 medium, 4 low, 50 negligible
   └── by status:   9 fixed, 109 not-fixed, 109 ignored 
python     3.13.14    3.15.0b2           binary  CVE-2026-7210        Critical  0.2% (40th)    0.2 
```
---
## - Outcome

The updated image significantly reduced the number of fixable vulnerabilities compared to the previous version.

| Metric | fastapi-v3 | fastapi-v4 |
|----------|----------|----------|
| Fixable Vulnerabilities | 114 | 9 |
| Critical | 12 | 1 |
| High | 74 | 0 |

This demonstrates a common remediation strategy used in production environments where updating base images and dependencies can improve security posture without requiring application code changes.

---

## - Remaining Findings

A small number of vulnerabilities remained after remediation.

One notable finding affected the Python runtime itself, where the recommended fix was only available in a beta Python release.

Since beta runtimes are generally not considered production-ready, the finding was documented and accepted temporarily rather than introducing an unstable runtime into the application.

This reflects a common real-world security trade-off where risk must be balanced against operational stability.

---

## - Key Takeaways for Part 1 (Container Vulnerability Scanning):

* Vulnerability scanning should be performed regularly.
* Container images inherit vulnerabilities from their base images.
* Many vulnerabilities can be remediated through dependency and runtime upgrades.
* Not every vulnerability has an immediate production-ready fix.
* Security findings should be analyzed before remediation decisions are made.
* Vulnerability scanning is most effective when integrated into CI/CD pipelines.


---
  
  
# Part 2: Secret Detection (Gitleaks)
  
The objective is to prevent secrets and credentials from being committed into source control.
  
## - Why Secret Detection Matters?

Accidentally committing credentials can expose infrastructure, cloud accounts, databases, and third-party services.

Examples include:

* AWS Access Keys
* GitHub Personal Access Tokens
* Database passwords
* API keys
* Certificates and private keys

Once committed, secrets become difficult to completely remove from Git history.

---

## - Installing Gitleaks:-

```bash
root@ubuntu-host ~ ➜ wget https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
root@ubuntu-host ~ ➜ tar -xzf gitleaks_8.30.1_linux_x64.tar.gz
root@ubuntu-host ~ ➜ sudo mv gitleaks /usr/local/bin/

# Verify the gitleaks installation version.
root@ubuntu-host ~ ➜ gitleaks version
8.30.1

```
---

## - Scanning the Repository

Run a repository scan:

```bash
root@ubuntu-host ~ ➜  cd Devops-Project-1/

root@ubuntu-host Devops-Project-1 on  main [!?] ➜  gitleaks detect --source .

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

3:35PM INF 87 commits scanned.
3:35PM INF scanned ~148540 bytes (148.54 KB) in 325ms
3:35PM INF no leaks found
```

---

## - Results

The repository and its commit history were scanned for exposed credentials and secrets.

```text
87 commits scanned.
no leaks found
```

---

## - Key Learnings for Part 2 (Secrets Detection):

* Secret scanning helps prevent credential exposure.
* Automated scanning reduces human error.
* Security should begin before code reaches production.

---
  
  
# Part 3: Security Gates in CI/CD
  
The objective is to integrate automated security checks into the CI/CD pipeline.
  
Now that you have an understanding of how gitleaks and grype works and have tested it out locally, the next phase of this project will integrate Gitleaks and Grype into the GitHub Actions workflow to automate vulnerability scanning during the CI process and prevent vulnerable images from progressing further through the delivery pipeline.

---

## - What is a Security Gate?

A security gate is an automated checkpoint that evaluates security requirements before software progresses through the deployment pipeline.

Example:

```text
Code Commit
      ↓
Build Image
      ↓
Gitleaks Scan
      ↓
Grype Scan
      ↓
Security Review
      ↓
Deploy
```

---

### Grype Integration:-

Example GitHub Actions step:

```yaml
- name: Scan Container Image
  run: |
    grype ghcr.io/${{ github.repository }}:${{ github.sha }}
```

---

### Gitleaks Integration:-

Example GitHub Actions step:

```yaml
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
```

---

## - Current Approach

The pipeline currently performs security scans and reports findings.

The workflow does not automatically fail on vulnerability detection because one known Critical vulnerability currently exists in the latest stable Python image used by the project.

Automatically failing the pipeline would block all deployments without a stable remediation path.

Instead, scan results are reviewed and documented as part of the security process.

---

## - Key Learnings for Part 3 (Security Gating): 

* Security should be integrated into CI/CD pipelines.
* Automated security checks improve consistency.
* Security decisions require balancing risk, stability, and operational requirements.
* Vulnerability reporting is often the first step before enforcement.
