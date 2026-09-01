# Exercicio 05 - Imagem, container ou volume? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`tipo_docker`** - Classifique o conceito Docker: molde/template -> 'imagem'; instancia/processo -> 'container'; dados_persistentes/disco -> 'volume'; senao 'desconhecido'.

```bash
cd modulos/02-linux-git-ambiente/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
imagem=molde, container=instancia em execucao, volume=dados persistentes.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def tipo_docker(desc):
    mapa = {'molde': 'imagem', 'template': 'imagem', 'instancia': 'container', 'processo': 'container', 'dados_persistentes': 'volume', 'disco': 'volume'}
    return mapa.get(desc, 'desconhecido')
```
:::

---
**Revisado em:** 2026-08-31
