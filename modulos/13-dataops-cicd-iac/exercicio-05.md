# Exercício 05 — Plano do Terraform (diff) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`plano_terraform`** — Compare dicts {recurso: config}. Retorne {'criar':[...], 'atualizar':[...], 'destruir':[...]} (listas ordenadas).

```bash
cd modulos/13-dataops-cicd-iac/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
criar: só no desejado; destruir: só no atual; atualizar: em ambos com config diferente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def plano_terraform(atual, desejado):
    criar = sorted(k for k in desejado if k not in atual)
    destruir = sorted(k for k in atual if k not in desejado)
    atualizar = sorted(k for k in desejado if k in atual and desejado[k] != atual[k])
    return {'criar': criar, 'atualizar': atualizar, 'destruir': destruir}
```
:::

---
**Revisado em:** 2026-08-29
