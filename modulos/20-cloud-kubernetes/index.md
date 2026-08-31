# Módulo 20 — Cloud e Kubernetes

> A infraestrutura da engenharia de dados moderna: serviços gerenciados na nuvem e orquestração de
> contêineres em escala com Kubernetes — a sequência natural do Docker (M10).

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 30h
- **Pré-requisitos:** M10 (Docker), M13 (IaC/Terraform)
- **Onde roda:** 🟢 Browser (exercícios de lógica) + 🐳 Kubernetes local via **kind** (lab avançado)

## Ementa
A nuvem para dados: modelos de serviço (**IaaS/PaaS/SaaS/serverless**) e serviços gerenciados (object
storage, warehouse, serverless, mensageria, bancos), região/zona, disponibilidade e **custo**.
**Kubernetes**: modelo declarativo (estado desejado), objetos (**pod, deployment, service, namespace**),
scheduler/etcd, **self-healing** e **autoscaling (HPA)**. Rodando dados em k8s: **Jobs/CronJobs**,
**StatefulSets/PVC**, Airflow e Spark em k8s, e provisionamento com **IaC (Terraform)**. Quando (não) usar k8s.

## Competências e habilidades
- C18 — usar serviços de nuvem e orquestrar contêineres com Kubernetes para cargas de dados.

## Objetivos de aprendizagem
1. **Escolher** o serviço de nuvem adequado a uma necessidade.
2. **Explicar** o modelo declarativo do Kubernetes e seus objetos.
3. **Raciocinar** sobre self-healing, autoscaling e scheduling.
4. **Descrever** como pipelines (Airflow/Spark) e estado rodam em k8s, provisionados por IaC.

## Plano de aulas (unidades)

**Unidade 1 — A nuvem para dados**
1. **Teoria:** [A nuvem para dados: modelos de serviço](teoria-01-nuvem-para-dados.md)
2. **Exercícios:** [Escolher o serviço (🟢)](exercicio-01.md) · [Cabe no nó / scheduler (🟢)](exercicio-05.md)

**Unidade 2 — Kubernetes: conceitos**
1. **Teoria:** [Kubernetes: orquestração de contêineres](teoria-02-kubernetes-conceitos.md)
2. **Lab:** [Kubernetes local com kind (🐳 avançado)](lab-01-kubernetes-kind.md)
3. **Exercícios:** [Réplicas para a carga (🟢)](exercicio-02.md) · [Deployment saudável (🟢)](exercicio-03.md)

**Unidade 3 — Dados no Kubernetes e IaC**
1. **Teoria:** [Rodando dados no Kubernetes: jobs, estado e IaC](teoria-03-dados-no-kubernetes.md)
2. **Exercícios:** [Autoscaling / HPA (🟢)](exercicio-04.md) · [DNS de service (🟢)](exercicio-06.md)

> **Módulo completo.** Fecha a infra do Eixo 3: do contêiner (M10) à orquestração em escala na nuvem.

## Metodologia e avaliação
**Maestria:** escolher serviços de nuvem para um cenário, explicar os objetos do k8s e o modelo
declarativo, e (opcional) subir o lab com kind — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Quase toda vaga cita uma nuvem; Kubernetes aparece muito em pleno/sênior. Saber escolher serviços
gerenciados e raciocinar sobre orquestração é diferencial claro.

## Erros comuns
- Operar tudo em IaaS quando gerenciado/serverless resolveria.
- Rodar banco como Deployment (efêmero) em vez de StatefulSet + PVC.
- Adotar k8s sem escala que o justifique.
- Provisionar clicando no console em vez de IaC.

## Recursos
Ver [`recursos.md`](recursos.md) (docs do Kubernetes/kind; Reis & Housley; Terraform).

---
**Revisado em:** 2026-08-31
