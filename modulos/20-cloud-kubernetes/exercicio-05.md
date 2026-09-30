# Exercício 05 — Scheduler: onde cada pod vai rodar

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O scheduler do Kubernetes (teoria 02) decide em que nó cada pod roda em duas fases: **filtrar** os
nós onde o pod cabe (os *requests* de CPU **e** memória somados aos que já estão lá não podem
passar da capacidade) e **pontuar** os que sobraram. Uma pontuação comum espalha a carga: vence o
nó que fica com **mais recurso livre** depois de receber o pod. Pod que não cabe em lugar nenhum
fica **Pending** — o sinal clássico de que o cluster precisa crescer (ou de que alguém pediu recurso
demais).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `agendar(pods, nos)`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — filtrar
Mantenha o livre de cada nó (`[cpu, mem]`). Um nó é viável se `cpu_livre >= cpu` **e** `mem_livre >= mem`.
:::
:::{dropdown} Dica 2 — pontuar
Fração livre depois = `(livre_cpu - cpu) / cpu_total`. Queremos a maior: `min(viaveis, key=lambda n: (-fracao, n))`.
:::
:::{dropdown} Dica 3 — alocar
Desconte CPU e memória do nó escolhido; sem viável, `"Pending"` (e nada é descontado).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def agendar(pods: list, nos: dict) -> dict:
    livre = {n: [c, m] for n, (c, m) in nos.items()}
    aloc = {}
    for nome, cpu, mem in pods:
        if cpu <= 0 or mem <= 0:
            raise ValueError(f"requests inválidos em {nome}")
        viaveis = [n for n, (c, m) in livre.items() if c >= cpu and m >= mem]
        if not viaveis:
            aloc[nome] = "Pending"
            continue
        escolhido = min(viaveis, key=lambda n: (-(livre[n][0] - cpu) / nos[n][0], n))
        livre[escolhido][0] -= cpu
        livre[escolhido][1] -= mem
        aloc[nome] = escolhido
    return {"alocacao": aloc, "livre": {n: (c, m) for n, (c, m) in sorted(livre.items())}}
```
No último teste, sobram **4 CPUs livres** no cluster (1 + 2 + 1), mas o `etl-4` pede 3 e fica
Pending: nenhum nó sozinho tem 3 livres. É a **fragmentação** — recurso existe, mas espalhado. Por
isso os *requests* precisam refletir o uso real: pedir 3 CPUs "por garantia" para um job que usa 1
desperdiça cluster e gera Pending.

A pontuação por fração livre espalha os pods (bom para disponibilidade: um nó que cai leva poucos
pods). A alternativa oposta, empacotar nos nós mais cheios (*bin packing*), economiza máquinas e
permite desligar nós ociosos — é a escolha de clusters de jobs de dados com autoscaler, onde custo
pesa mais que espalhamento.
:::

---
**Revisado em:** 2026-09-30
