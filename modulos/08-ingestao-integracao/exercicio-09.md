# Exercicio 09 - Aplicar changelog CDC (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-cdc-schema-evolution.md).

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py): implemente **`aplicar_cdc`** - Materialize a tabela-espelho aplicando um changelog de CDC. estado = {chave: valor} atual; eventos = lista de dicts {op, chave, valor} com op em 'I'/'U'/'D', aplicados EM ORDEM. I e U fazem upsert; D remove. Retorne o estado final (dict).

```bash
cd modulos/08-ingestao-integracao/exercicio-09
pytest -q
```

## Dica
:::{dropdown} Dica
copie o estado; para cada evento em ordem, D remove (pop), I/U fazem upsert (estado[chave]=valor).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def aplicar_cdc(estado, eventos):
    estado = dict(estado)
    for ev in eventos:
        if ev['op'] == 'D':
            estado.pop(ev['chave'], None)
        else:
            estado[ev['chave']] = ev['valor']
    return estado
```
:::

---
**Revisado em:** 2026-09-09
