# Exercício 02 — A lógica do incremental (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Implemente a **marca d'água** que sustenta a ingestão incremental — o que o Exercício 01 usa
por baixo.

## Tarefas
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py) (entrada: lista de `(id, updated_at)`):

- **`incremental(linhas, marca)`** — `id`s (ordenados) cujo `updated_at` é **estritamente maior**
  que `marca` (o que ingerir).
- **`nova_marca(linhas)`** — o maior `updated_at` (a nova marca a persistir); `None` se vazio.

```bash
cd modulos/08-ingestao-integracao/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — incremental
`sorted(i for i, ts in linhas if ts > marca)` (datas ISO comparam como texto).
:::
:::{dropdown} Dica 2 — nova marca
`max((ts for _, ts in linhas), default=None)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def incremental(linhas, marca):
    return sorted(i for i, ts in linhas if ts > marca)

def nova_marca(linhas):
    return max((ts for _, ts in linhas), default=None)
```
O `>` (estritamente maior) evita reprocessar a última linha já ingerida. A `nova_marca` é
salva como estado do pipeline para a próxima execução começar de onde parou — o coração do
incremental.
:::

---
**Revisado em:** 2026-08-29
