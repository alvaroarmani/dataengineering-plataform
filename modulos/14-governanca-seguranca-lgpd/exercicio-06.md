# Exercício 06 — Anonimizar registro (direito ao esquecimento) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`anonimizar`** — Retorne um NOVO dict igual a `registro`, mas com cada campo de `campos_pessoais` (se existir) substituído por '***'.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
dict comprehension: troque o valor por '***' quando a chave estiver em campos_pessoais.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def anonimizar(registro, campos_pessoais):
    return {k: ('***' if k in campos_pessoais else v) for k, v in registro.items()}
```
:::

---
**Revisado em:** 2026-08-29
