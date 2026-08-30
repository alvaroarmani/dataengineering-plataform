# Exercício 06 — Parse de referência de imagem (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`parse_imagem`** — sem '/' o registry é docker.io; sem ':' a tag é latest.

```bash
cd modulos/10-docker-avancado/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
Separe registry pelo 1º '/', e a tag pelo último ':'.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def parse_imagem(ref):
    registry = 'docker.io'; resto = ref
    if '/' in ref:
        registry, resto = ref.split('/', 1)
    if ':' in resto:
        nome, tag = resto.rsplit(':', 1)
    else:
        nome, tag = resto, 'latest'
    return (registry, nome, tag)
```
:::

---
**Revisado em:** 2026-08-29
