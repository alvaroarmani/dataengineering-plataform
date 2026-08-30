# Exercício 02 — Tabelas sem dono (governança) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`tabelas_sem_dono`** — catalogo = {tabela: dono}. Retorne a lista ORDENADA das tabelas cujo dono é None ou string vazia.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
dono 'vazio' = None ou '' — em Python, `not dono` cobre os dois.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tabelas_sem_dono(catalogo):
    return sorted(t for t, dono in catalogo.items() if not dono)
```
:::

---
**Revisado em:** 2026-08-29
