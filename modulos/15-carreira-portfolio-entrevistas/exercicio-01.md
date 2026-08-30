# Exercício 01 — README completo? (portfólio) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`secoes_faltando`** — Um bom README tem: 'o que', 'por que', 'arquitetura', 'como rodar', 'o que aprendi'. Dada a lista `presentes`, retorne a lista ORDENADA das seções obrigatórias que faltam.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
conjunto das obrigatórias menos o conjunto das presentes, ordenado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def secoes_faltando(presentes):
    obrigatorias = {'o que', 'por que', 'arquitetura', 'como rodar', 'o que aprendi'}
    return sorted(obrigatorias - set(presentes))
```
:::

---
**Revisado em:** 2026-08-30
