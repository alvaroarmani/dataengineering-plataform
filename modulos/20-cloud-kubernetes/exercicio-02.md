# Exercício 02 — Réplicas para a carga (scale out) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`replicas_desejadas`** — Cada pod aguenta `capacidade_por_pod` de carga. Retorne o número MÍNIMO de réplicas para atender `carga` (arredonde para cima).

```bash
cd modulos/20-cloud-kubernetes/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
teto da divisão: -(-carga // capacidade) faz ceil sem importar math.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def replicas_desejadas(carga, capacidade_por_pod):
    return -(-carga // capacidade_por_pod)
```
:::

---
**Revisado em:** 2026-08-31
