# Version 2 Roadmap:

Version 1 focused on understanding the complete DevOps lifecycle by building and operating a cloud-native application locally.

Version 2 aims to evolve the same project into a more production-oriented platform by introducing cloud infrastructure, scalability, security, and operational best practices.

Rather than building a larger application, the focus will remain on improving the platform around it—mirroring how DevOps engineers continuously evolve production systems over time.

---

# Planned Features

## Cloud Infrastructure

- [ ] Provision an Azure Kubernetes Service (AKS) cluster using Terraform.
- [ ] Deploy the existing application to the cloud.
- [ ] Manage cloud resources using Infrastructure as Code.

---

## Production GitOps

- [ ] Configure ArgoCD on AKS.
- [ ] Continue GitOps-based deployments.
- [ ] Support environment-specific deployment configurations.

---

## Secure Application Delivery

- [ ] Configure cert-manager.
- [ ] Automate TLS certificates using Let's Encrypt.
- [ ] Serve the application securely over HTTPS.

---

## Kubernetes Improvements

- [ ] Horizontal Pod Autoscaler (HPA).
- [ ] Resource requests and limits.
- [ ] Network Policies.
- [ ] Pod Disruption Budgets.
- [ ] Production-ready namespaces and RBAC.

---

## Observability

- [ ] Kubernetes cluster monitoring.
- [ ] Node Exporter integration.
- [ ] kube-state-metrics.
- [ ] Enhanced Grafana dashboards.
- [ ] SLI/SLO-oriented dashboards.

---

## Security

- [ ] Kubernetes RBAC.
- [ ] Secret management.
- [ ] Image signing and verification.
- [ ] Admission controllers.
- [ ] Container runtime security.

---

## Reliability

- [ ] Rolling deployments.
- [ ] Canary deployments.
- [ ] Backup and restore strategies.
- [ ] Zero-downtime application updates.

---

## Application Enhancements

The application will intentionally remain lightweight while becoming more representative of a real-world service.

Planned additions include:

- [ ] Basic user management APIs.
- [ ] Simple authentication.
- [ ] PostgreSQL integration.
- [ ] Redis caching.
- [ ] Background task processing.

These additions are intended to create realistic operational scenarios without shifting the focus away from DevOps.

---

## Future Explorations (Optionl perhaps for a v3).

As the platform matures, additional technologies may be explored:

* Helm
* External Secrets Operator
* Loki for centralized logging
* Tempo / OpenTelemetry for distributed tracing
* Service Mesh (Istio or Linkerd)
* Multi-environment deployments
* Multi-cluster GitOps

---

# Goal

Version 2 seems like a lot, but it is not about adding more tools.

It is about answering the next question:

> **"How would this project evolve if it were running in a real production environment?"**

Every improvement will continue to follow the same philosophy established in Version 1 - learning not just *how* a tool works, but *why* it exists and the engineering problem it solves.
