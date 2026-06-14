# Day 07 - Container Vulnerability Scanning

## Objective

Introduce container security practices by identifying, analyzing, and remediating vulnerabilities within application container images.

---

## Why Grype?

Container vulnerability scanning is commonly performed using tools such as Trivy, Grype, Clair, and Snyk.

For this project, Grype was selected to gain hands-on experience with an alternative scanning solution and to better understand the vulnerability management process independent of any specific tool.

Grype provides:

- Container image vulnerability scanning
- CI/CD integration capabilities
- Policy-based security enforcement
- Lightweight installation and usage

The objective of this phase is not to compare scanners, but to understand how vulnerabilities are identified, assessed, and remediated within containerized workloads.

---

## Installing Grype

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
