# Exercício 06 — Undercurrents faltando no design (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`undercurrents_faltando`** — As undercurrents esperadas num system design: 'qualidade','seguranca','observabilidade','custo','idempotencia'. Dada a lista `mencionadas`, retorne a lista ORDENADA das que faltam.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
conjunto esperadas menos mencionadas, ordenado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def undercurrents_faltando(mencionadas):
    esperadas = {'qualidade', 'seguranca', 'observabilidade', 'custo', 'idempotencia'}
    return sorted(esperadas - set(mencionadas))
```
:::

---
**Revisado em:** 2026-08-30
