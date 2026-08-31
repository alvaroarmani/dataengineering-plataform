# Recursos — Módulo 20 (Cloud e Kubernetes)

Curadoria de fontes. As obras estão registradas em [`referencias.yaml`](../../referencias.yaml).

## Livros e artigos
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): nuvem, custo (FinOps),
  contêineres e orquestração como *undercurrents* e infraestrutura padrão.
- **Armbrust, M. et al. — Lakehouse: A New Generation of Open Platforms** (2021): plataformas de dados
  sobre object storage da nuvem.
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017): os fundamentos distribuídos por baixo de nuvem e k8s.

## Documentação oficial
- **Kubernetes** — <https://kubernetes.io/docs/concepts/> (Pods, Deployments, Services, HPA, StatefulSets, Jobs).
- **kind (Kubernetes in Docker)** — <https://kind.sigs.k8s.io/> (cluster local para o lab).
- **kubectl** — <https://kubernetes.io/docs/reference/kubectl/> (CLI do cluster).
- **Terraform** — <https://developer.hashicorp.com/terraform> (provisionar cluster e nuvem, M13).
- Free-tier: **AWS** <https://aws.amazon.com/free/> · **Google Cloud** <https://cloud.google.com/free> · **Azure** <https://azure.microsoft.com/free/>.

## Prática
- **Lab deste módulo:** [Kubernetes local com kind](lab-01-kubernetes-kind.md) — cluster real dentro
  de contêineres (não precisa de nuvem).

## Onde isto conecta no curso
Sequência de **M10 (Docker)**; usa **M13 (IaC/Terraform)** para provisionar; apoia-se em **M19
(sistemas distribuídos/etcd)**; roda **M09 (Airflow)** e **M11 (Spark)** em escala.

---
**Revisado em:** 2026-08-31
