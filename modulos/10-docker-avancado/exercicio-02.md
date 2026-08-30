# Exercício 02 — .dockerignore: contexto de build (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`enviados_ao_contexto`** — arquivos casando com um ignore (prefixo `pasta/` ou nome exato) ficam de fora do contexto.

```bash
cd modulos/10-docker-avancado/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
Filtre os que não casam com nenhum padrão e ordene.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def enviados_ao_contexto(arquivos, ignore):
    def _ig(f):
        for p in ignore:
            if p.endswith('/') and f.startswith(p):
                return True
            if f == p:
                return True
        return False
    return sorted(f for f in arquivos if not _ig(f))
```
:::

---
**Revisado em:** 2026-08-29
