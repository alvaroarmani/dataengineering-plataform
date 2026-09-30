# Exercício 07 — Escreva um manifesto de Deployment (TRACK REAL · Kubernetes)

**Onde roda:** 🟢 grader de **artefato** (valida o manifesto, como o CI faria) + 🐳 para rodar num
cluster de verdade, use o [Lab 01 (kind)](lab-01-kubernetes-kind.md). Os exercícios 01–06 cobrem
os conceitos (HPA, scheduler, service) no navegador.

## Tarefa
Complete o [`exercicio-07/deployment.yaml`](exercicio-07/deployment.yaml): um **Deployment** com
**3 réplicas** de um container **`nginx:1.27`**, cujo **`selector.matchLabels`** bata **exatamente**
com os **labels do template** (senão o Deployment não gerencia os próprios pods).

## Como rodar o grader
```bash
pip install pyyaml
pytest -q modulos/20-cloud-kubernetes/exercicio-07
```
> O grader confere estrutura, réplicas, casamento selector↔labels e a imagem. Para ver o Deployment
> **rodando de verdade** (self-healing, scale), faça o **Lab 01** com `kind`.

## Dicas progressivas
:::{dropdown} Dica 1 — o esqueleto
Um Deployment tem `apiVersion: apps/v1`, `kind: Deployment`, `metadata.name` e um `spec` com `replicas`, `selector` e `template` (o molde dos pods). O grader lê o YAML e confere a estrutura.
:::
:::{dropdown} Dica 2 — o elo entre Deployment e pods
O `spec.selector.matchLabels` e o `spec.template.metadata.labels` precisam ter os **mesmos** rótulos (ex.: `{app: web}`): é assim que o Deployment sabe quais pods são dele. Se divergirem, o Kubernetes recusa o manifesto.
:::
:::{dropdown} Dica 3 — o container
Em `spec.template.spec.containers`, um item com `name`, `image` (com tag de versão, não `latest`) e `ports` com o `containerPort`. Defina também `resources.requests` — é o que o scheduler usa (exercício 05).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27
          ports:
            - containerPort: 80
```
:::

---
**Revisado em:** 2026-09-30
