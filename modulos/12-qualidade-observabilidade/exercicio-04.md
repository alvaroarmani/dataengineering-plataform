# Exercício 04 — Validade: valores fora do domínio (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`valores_invalidos`** — Retorne a lista ORDENADA e sem repetição dos valores que NÃO estão em `permitidos`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
conjunto de permitidos; retorne os que ficam de fora.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def valores_invalidos(valores, permitidos):
    ok = set(permitidos)
    return sorted({v for v in valores if v not in ok})
```
:::

---
**Revisado em:** 2026-08-29
