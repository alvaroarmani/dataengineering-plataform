# Exercicio 02 - Versionar ou nao? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`deve_versionar`** - Retorne True se o arquivo DEVE ir para o Git; False para segredos/gerados: '.env', 'node_modules', '__pycache__', '.venv', ou terminando em '.pyc'/'.log'.

```bash
cd modulos/02-linux-git-ambiente/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
bloqueie segredos/gerados; o resto (codigo/docs) versiona.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def deve_versionar(arquivo):
    nao = {'.env', 'node_modules', '__pycache__', '.venv'}
    if arquivo in nao or arquivo.endswith('.pyc') or arquivo.endswith('.log'):
        return False
    return True
```
:::

---
**Revisado em:** 2026-08-31
