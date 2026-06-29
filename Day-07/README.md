# Day-07: Security & Vulnerability Management

Security is a continuous process that helps identify vulnerabilities, prevent credential leaks, and enforce controls before software reaches production.

This section demonstrates:

* Container vulnerability scanning with Grype
* Secret detection with Gitleaks
* Security gates within CI/CD pipelines

---

# Part 1: Container Vulnerability Scanning (Grype)

The objective is to identify known vulnerabilities within container images before deployment.

## Why Grype?

Container vulnerability scanning can be performed using tools such as Trivy, Grype, Clair, and Snyk.

For this project, Grype was selected to gain hands-on experience with an alternative scanning solution and to better understand the vulnerability management process independent of any specific tool.

Grype provides:

* Container image vulnerability scanning
* CI/CD integration capabilities
* Policy-based security enforcement
* Lightweight installation and usage

---

## Installing Grype

### Linux

```bash
# Install Grype
root@ubuntu-host ~ ➜  curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh

root@ubuntu-host ~ ➜  sudo mv ./bin/grype /usr/local/bin/

# Verify installation
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

## Security Assessment Workflow

```text
Scan Image
    ↓
Review Findings
    ↓
Remediate
    ↓
Rebuild Image
    ↓
Rescan & Validate
```

---

## Initial Scan Results (fastapi-v3)

The original application image was scanned using Grype:

```bash
# Let's identify the critical and the high vulnerabilities of the 'janemils/janemils-app:fastapi-v3' image using grype.
root@ubuntu-host ~ ➜ grype janemils/janemils-app:fastapi-v3 --only-fixed | grep -E "High|Critical"
```

Report: [V3 image scanning report.](https://github.com/Janemils/Devops-Project-1/blob/main/Day-07/reports/grype-v3.txt)
  
---

## Analysis

Most findings were associated with packages inherited from the base image rather than the application code itself.

To validate this assumption, the image was rebuilt using a newer Python base image and rescanned.

The results showed a significant reduction in fixable vulnerabilities, confirming that the base image was the primary source of many findings.

---

## Remediation

The image originally used:

```dockerfile
FROM python:3.11-slim
```

It was updated to:

```dockerfile
FROM python:3.13-slim
```

The image was rebuilt and published as:

```text
janemils/janemils-app:fastapi-v4
```

Deployment manifests and Terraform configurations were updated to reference the remediated image version.

---

## Validation Scan Results (fastapi-v4)

The updated image was rescanned:

```bash
#  Let's identify the critical and the high vulnerabilities of the 'janemils/janemils-app:fastapi-v4' image using grype.
root@ubuntu-host Devops-Project-1 on  main [!?] ➜  grype janemils/janemils-app:fastapi-v4 --only-fixed | grep -E "High|Critical"
```

Report: [V4 image scanning report.](https://github.com/Janemils/Devops-Project-1/blob/main/Day-07/reports/grype-v4.txt)
  
---

## Outcome

| Metric                  | fastapi-v3 | fastapi-v4 |
| ----------------------- | ---------- | ---------- |
| Fixable Vulnerabilities | 114        | 9          |
| Critical                | 12         | 1          |
| High                    | 74         | 0          |

Updating the base image significantly improved the security posture without requiring application code changes.

---

## Remaining Finding

One Critical vulnerability remained after remediation:

| CVE           | Component      | Status                  |
| ------------- | -------------- | ----------------------- |
| CVE-2026-7210 | Python Runtime | No stable fix available |

The recommended fix currently requires upgrading to a beta Python release.

Since beta runtimes are generally not considered production-ready, the vulnerability was documented and accepted temporarily.

---

## Key Takeaways

* Container images inherit vulnerabilities from base images.
* Updating runtimes and dependencies can significantly reduce risk.
* Not every vulnerability has an immediate production-ready fix.
* Security findings should be reviewed before remediation decisions are made.
* Vulnerability scanning should be automated within CI/CD pipelines.

---

# Part 2: Secret Detection (Gitleaks)

The objective is to prevent credentials and sensitive information from being committed into source control.

## Why Secret Detection Matters?

Examples of commonly leaked secrets include:

* AWS Access Keys
* GitHub Personal Access Tokens
* Database passwords
* API keys
* Private keys and certificates

Once committed, secrets can remain accessible through Git history even after deletion.

---

## Installing Gitleaks

```bash
root@ubuntu-host ~ ➜  wget https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz

root@ubuntu-host ~ ➜  tar -xzf gitleaks_8.30.1_linux_x64.tar.gz

root@ubuntu-host ~ ➜  sudo mv gitleaks /usr/local/bin/

# Verify the gitleaks installation version.
root@ubuntu-host ~ ➜ gitleaks version
8.30.1
```

---

## Scanning the Repository

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

Example output:

```text
87 commits scanned.
no leaks found
```

---

## Results

The repository and commit history were scanned for exposed credentials and secrets.

```text
87 commits scanned.
no leaks found
```

---

## Key Takeaways

* Secret scanning helps prevent credential exposure.
* Automated scanning reduces human error.
* Security should begin before code reaches production.

---

# Part 3: Security Gates in CI/CD

After validating Grype and Gitleaks locally, both tools were integrated into the GitHub Actions workflow to automate security checks during CI.[Link for the CI Pipeline](https://github.com/Janemils/Devops-Project-1/actions/workflows/ci.yaml).

---

## What is a Security Gate?

A security gate is an automated checkpoint that evaluates security requirements before software progresses through the delivery pipeline.

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

## Gitleaks Integration

```yaml
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
```

---

## Grype Integration

```yaml
- name: Security Scan
  run: |
    grype $IMAGE_NAME:${{ github.sha }} \
      --config .grype.yaml \
      --only-fixed \
      --fail-on critical
```

---

## Why the Pipeline Initially Failed:

When Grype was configured with:

```yaml
--fail-on critical
```

the pipeline failed because the image contained a known Critical vulnerability:

| CVE           | Component      | Status                  |
| ------------- | -------------- | ----------------------- |
| CVE-2026-7210 | Python Runtime | No stable fix available |

Although the vulnerability had a fix, the fix was only available in a beta Python release, which was not considered suitable for production use.

---

## Risk Acceptance

To avoid blocking deployments indefinitely, the vulnerability was documented and added to `.grype.yaml` as an accepted risk.

This allows the pipeline to:

* Ignore the approved exception.
* Continue enforcing security policies.
* Fail automatically for any new Critical vulnerabilities.

This approach mirrors common production practices where security findings are reviewed, documented, and tracked until a stable remediation becomes available.
You can check out this failed pipeline if you want to explore more about the vulnerabilities that I ignored: [Failed Pipeline.](https://github.com/Janemils/Devops-Project-1/actions/runs/27637019809)

---

## Key Takeaways

* Security should be integrated directly into CI pipelines.
* Automated checks improve consistency and reduce manual effort.
* Security gates help prevent vulnerable artifacts from progressing through the delivery pipeline.
* Risk acceptance should be documented and reviewed regularly.
* Not all vulnerabilities should be treated equally; context and remediation availability matter.
