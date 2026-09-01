# Exercicio 04 - Arquivos prontos para commit (staged) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`arquivos_staged`** - status = {arquivo: estado} com estado em {'staged','unstaged','untracked'}. Retorne a lista ORDENADA dos arquivos 'staged'.

```bash
cd modulos/02-linux-git-ambiente/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
filtre os de estado 'staged' e ordene.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def arquivos_staged(status):
    return sorted(a for a, e in status.items() if e == 'staged')
```
:::

---
**Revisado em:** 2026-08-31
