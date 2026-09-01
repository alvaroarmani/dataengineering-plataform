# Exercicio 03 - Mensagem de commit valida? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`commit_valido`** - No padrao Conventional Commits, a mensagem comeca com um tipo (feat/fix/docs/chore/refactor/test) seguido de ':' ou '('. Retorne o booleano.

```bash
cd modulos/02-linux-git-ambiente/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
verifique se comeca com um tipo conhecido + ':' ou '('.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def commit_valido(msg):
    tipos = ('feat', 'fix', 'docs', 'chore', 'refactor', 'test')
    return any(msg.startswith(t + ':') or msg.startswith(t + '(') for t in tipos)
```
:::

---
**Revisado em:** 2026-08-31
