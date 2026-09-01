# Exercicio 06 - Mapeamento de porta (docker run -p) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`mapa_porta`** - Ao publicar uma porta com 'docker run -p', o formato e 'host:container'. Monte e retorne essa string.

```bash
cd modulos/02-linux-git-ambiente/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
formate '<host>:<container>'.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def mapa_porta(host, container):
    return f'{host}:{container}'
```
:::

---
**Revisado em:** 2026-08-31
