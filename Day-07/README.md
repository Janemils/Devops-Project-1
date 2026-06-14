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

---

## Security Assessment Workflow

The security assessment followed the process below:

1. Scan the existing container image.
2. Review vulnerability findings.
3. Investigate affected packages.
4. Apply remediation.
5. Rebuild the image.
6. Validate improvements through rescanning.

---

## Initial Scan Results (fastapi-v3)

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
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28389       High        0.1% (34th)    0.1    
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28390       High        0.1% (34th)    0.1    
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28390       High        0.1% (34th)    0.1    
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28390       High        0.1% (34th)    0.1    
jaraco-context           5.3.0            6.1.0                       python  GHSA-58pv-8j8x-9vj2  High        0.1% (27th)    < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45447       High        < 0.1% (26th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45447       High        < 0.1% (26th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45447       High        < 0.1% (26th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-9076        High        < 0.1% (26th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-9076        High        < 0.1% (26th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-9076        High        < 0.1% (26th)  < 0.1  
libc-bin                 2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2025-15281       High        < 0.1% (25th)  < 0.1  
libc6                    2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2025-15281       High        < 0.1% (25th)  < 0.1  
libc-bin                 2.41-12+deb13u1  2.41-12+deb13u3             deb     CVE-2026-4437        High        < 0.1% (25th)  < 0.1  
libc6                    2.41-12+deb13u1  2.41-12+deb13u3             deb     CVE-2026-4437        High        < 0.1% (25th)  < 0.1  
python                   3.11.15          *3.13.13, 3.14.4, 3.15.0a8  binary  CVE-2026-4224        High        < 0.1% (25th)  < 0.1  
libc-bin                 2.41-12+deb13u1  2.41-12+deb13u3             deb     CVE-2026-4046        High        < 0.1% (24th)  < 0.1  
libc6                    2.41-12+deb13u1  2.41-12+deb13u3             deb     CVE-2026-4046        High        < 0.1% (24th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-7383        High        < 0.1% (20th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-7383        High        < 0.1% (20th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-7383        High        < 0.1% (20th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34180       High        < 0.1% (18th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34180       High        < 0.1% (18th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34180       High        < 0.1% (18th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28388       High        < 0.1% (17th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28388       High        < 0.1% (17th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28388       High        < 0.1% (17th)  < 0.1  
python                   3.11.15          *3.13.13, 3.14.4, 3.15.0a8  binary  CVE-2026-3644        High        < 0.1% (18th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28387       High        < 0.1% (15th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28387       High        < 0.1% (15th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-28387       High        < 0.1% (15th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31790       High        < 0.1% (13th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31790       High        < 0.1% (13th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31790       High        < 0.1% (13th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-42764       High        < 0.1% (13th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-42764       High        < 0.1% (13th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-42764       High        < 0.1% (13th)  < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34183       High        < 0.1% (11th)  < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34183       High        < 0.1% (11th)  < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34183       High        < 0.1% (11th)  < 0.1  
dpkg                     1.22.21          1.22.22                     deb     CVE-2026-2219        High        < 0.1% (7th)   < 0.1  
libc-bin                 2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2026-0915        High        < 0.1% (4th)   < 0.1  
libc6                    2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2026-0915        High        < 0.1% (4th)   < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45445       High        < 0.1% (4th)   < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45445       High        < 0.1% (4th)   < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-45445       High        < 0.1% (4th)   < 0.1  
wheel                    0.45.1           0.46.2                      python  GHSA-8rrh-rw8j-w5fx  High        < 0.1% (3rd)   < 0.1  
libcap2                  1:2.75-10+b3     1:2.75-10+deb13u1           deb     CVE-2026-4878        High        < 0.1% (2nd)   < 0.1  
libc-bin                 2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2026-0861        High        < 0.1% (1st)   < 0.1  
libc6                    2.41-12+deb13u1  2.41-12+deb13u2             deb     CVE-2026-0861        High        < 0.1% (1st)   < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31789       Critical    < 0.1% (0th)   < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31789       Critical    < 0.1% (0th)   < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.5-1~deb13u2             deb     CVE-2026-31789       Critical    < 0.1% (0th)   < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34182       Critical    < 0.1% (0th)   < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34182       Critical    < 0.1% (0th)   < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34182       Critical    < 0.1% (0th)   < 0.1  
libssl3t64               3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34181       High        < 0.1% (0th)   < 0.1  
openssl                  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34181       High        < 0.1% (0th)   < 0.1  
openssl-provider-legacy  3.5.4-1~deb13u2  3.5.6-1~deb13u2             deb     CVE-2026-34181       High        < 0.1% (0th)   < 0.1  

```

### Analysis

The scan results suggested that many vulnerabilities originated from components inherited from the base image rather than the application code itself.

To validate this assumption, the base image was upgraded from Python 3.11 Slim to Python 3.13 Slim and the image was rebuilt.

After rebuilding and rescanning, the number of fixable High and Critical vulnerabilities dropped significantly, confirming that the base image version was a major contributor to the overall vulnerability count.

---

## Remediation

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

## Validation Scan Results (fastapi-v4)

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

### Outcome

The updated image significantly reduced the number of fixable vulnerabilities compared to the previous version.

```
# With the v3 version:
24 fixed vulnerabilities
6 Critical
23 High
```

```
# With the v4 version:
9 fixed vulnerabilities
1 Critical
0 High
```

This demonstrates a common remediation strategy used in production environments where updating base images and dependencies can improve security posture without requiring application code changes.

---

## Remaining Findings

A small number of vulnerabilities remained after remediation.

One notable finding affected the Python runtime itself, where the recommended fix was only available in a beta Python release.

Since beta runtimes are generally not considered production-ready, the finding was documented and accepted temporarily rather than introducing an unstable runtime into the application.

This reflects a common real-world security trade-off where risk must be balanced against operational stability.

---

## Key Takeaways

* Vulnerability scanning should be performed regularly.
* Container images inherit vulnerabilities from their base images.
* Many vulnerabilities can be remediated through dependency and runtime upgrades.
* Not every vulnerability has an immediate production-ready fix.
* Security findings should be analyzed before remediation decisions are made.
* Vulnerability scanning is most effective when integrated into CI/CD pipelines.

---

## Next Steps

Now that you have an understanding of how grype works and have tested it out locally, the next phase of this project will integrate Grype into the GitHub Actions workflow to automate vulnerability scanning during the CI process and prevent vulnerable images from progressing further through the delivery pipeline.

