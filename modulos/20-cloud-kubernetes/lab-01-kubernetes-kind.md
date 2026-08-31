# Lab 01 — Kubernetes local com kind: deploy, escala e self-healing

**Onde roda:** 🐳 Bancada Docker (Kubernetes local via **kind** — *Kubernetes in Docker*).
Lab **avançado/opcional** que dá corpo à [teoria 02](teoria-02-kubernetes-conceitos.md): estado
desejado, Deployment, Service, self-healing e escala.

> Pré-requisitos: engine Docker estável e as CLIs **kind** e **kubectl** instaladas
> (<https://kind.sigs.k8s.io/>, <https://kubernetes.io/docs/tasks/tools/>). É um cluster real,
> rodando dentro de contêineres — não precisa de nuvem.

## 1. Crie um cluster local
```bash
kind create cluster --name curso
kubectl cluster-info --context kind-curso
kubectl get nodes            # o(s) nó(s) do cluster
```

## 2. Declare o estado desejado (Deployment com 3 réplicas)
Crie `web.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
        - name: web
          image: nginx:1.27
          ports: [{ containerPort: 80 }]
---
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports: [{ port: 80, targetPort: 80 }]
```
Aplique e observe:
```bash
kubectl apply -f web.yaml
kubectl get pods -o wide      # 3 pods, cada um pode cair num nó
kubectl get deployment web    # READY 3/3 (desejado == atual)
kubectl get service web       # o endereço estável do Service
```
✅ Você **declarou** 3 réplicas; o k8s as criou e mantém (compare com o [Exercício 03](exercicio-03.md)).

## 3. Self-healing: mate um pod e veja renascer
```bash
kubectl delete pod -l app=web --field-selector 'status.phase=Running' --wait=false
kubectl get pods -w           # Ctrl+C após ver um novo pod subir
```
✅ O k8s **recria** o pod para voltar ao estado desejado (3 réplicas) — sem você pedir.

## 4. Escale (scale out) e faça um rolling update
```bash
kubectl scale deployment web --replicas=5      # sobe para 5 (Exercício 02)
kubectl get pods
kubectl set image deployment/web web=nginx:1.27-alpine   # rolling update
kubectl rollout status deployment/web          # troca sem downtime
```

## 5. Alcance o Service (DNS interno)
```bash
kubectl run curl --image=curlimages/curl -it --rm --restart=Never -- \
  curl -s http://web.default.svc.cluster.local | head -3
```
✅ O nome `web.default.svc.cluster.local` (o do [Exercício 06](exercicio-06.md)) resolve para o
Service, que balanceia entre os pods.

## 6. Derrube
```bash
kind delete cluster --name curso
```

## O que você praticou
- **Declarou** um Deployment (estado desejado) e um Service (endereço estável).
- Viu **self-healing** (pod recriado) e **scale out** (mais réplicas).
- Fez **rolling update** sem downtime e alcançou o Service pelo **DNS interno**.

---
**Revisado em:** 2026-08-31
