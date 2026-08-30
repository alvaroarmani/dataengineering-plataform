# Exercício 02 — Validar contrato (campos e tipos) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`valida_contrato`** — contrato = {campo: nome_do_tipo}. Retorne a lista ORDENADA de campos com problema (ausente OU tipo errado).

```bash
cd modulos/12-qualidade-observabilidade/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
para cada campo do contrato: ausente ou type().__name__ != esperado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def valida_contrato(registro, contrato):
    probs = [c for c, t in contrato.items() if c not in registro or type(registro[c]).__name__ != t]
    return sorted(probs)
```
:::

---
**Revisado em:** 2026-08-29
