# Exercicio 06 - Contrato da API: campos faltando (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`campos_faltando`** - Validacao de contrato: dado o `payload` (dict) e a lista de campos `obrigatorios`, retorne a lista ORDENADA dos obrigatorios ausentes.

```bash
cd modulos/23-apis-microservicos/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
filtre os obrigatorios que nao estao no payload e ordene.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def campos_faltando(payload, obrigatorios):
    return sorted(c for c in obrigatorios if c not in payload)
```
:::

---
**Revisado em:** 2026-09-09
