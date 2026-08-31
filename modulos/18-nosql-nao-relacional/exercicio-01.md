# Exercício 01 — Escolher a família NoSQL (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`familia_nosql`** — Dado o caso de uso, recomende a família: cache/sessao -> 'key-value'; catalogo/perfil -> 'documento'; metricas/series -> 'time-series'; eventos/escrita-massiva -> 'wide-column'; senão 'relacional'.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
use um dict de caso->família e caia em 'relacional' por padrão.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def familia_nosql(caso):
    mapa = {
        'cache': 'key-value', 'sessao': 'key-value',
        'catalogo': 'documento', 'perfil': 'documento',
        'metricas': 'time-series', 'series': 'time-series',
        'eventos': 'wide-column', 'escrita-massiva': 'wide-column',
    }
    return mapa.get(caso, 'relacional')
```
:::

---
**Revisado em:** 2026-08-31
