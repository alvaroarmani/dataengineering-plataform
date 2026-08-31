# Exercício 01 — Escolher o serviço de nuvem (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`servico_cloud`** — Mapeie a necessidade ao tipo de serviço gerenciado: objeto/arquivo -> 'object-storage'; fila/evento -> 'mensageria'; funcao -> 'serverless'; warehouse/analitico -> 'data-warehouse'; container -> 'orquestracao'; senão 'computacao'.

```bash
cd modulos/20-cloud-kubernetes/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
dict de necessidade->serviço, caindo em 'computacao' por padrão.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def servico_cloud(necessidade):
    mapa = {
        'objeto': 'object-storage', 'arquivo': 'object-storage',
        'fila': 'mensageria', 'evento': 'mensageria',
        'funcao': 'serverless',
        'warehouse': 'data-warehouse', 'analitico': 'data-warehouse',
        'container': 'orquestracao',
    }
    return mapa.get(necessidade, 'computacao')
```
:::

---
**Revisado em:** 2026-08-31
