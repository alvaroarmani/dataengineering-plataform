# Exercício 01 — Completude de uma coluna (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`completude`** — Fração (0..1, arredondada em 4 casas) de linhas onde `campo` está presente e não é None/'' .

```bash
cd modulos/12-qualidade-observabilidade/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
conte linhas com o campo preenchido / total.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def completude(linhas, campo):
    ok = sum(1 for r in linhas if r.get(campo) not in (None, ''))
    return round(ok/len(linhas), 4) if linhas else 0.0
```
:::

---
**Revisado em:** 2026-08-29
