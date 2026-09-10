# Exercicio 10 - Conciliar schema (drift) (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-cdc-schema-evolution.md).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`conciliar_schema`** - Detecte schema drift na borda. esperado = {coluna: tipo} (tipo como 'int'/'str'/...); recebido = {coluna: valor}. Retorne {'faltando': [obrigatorias ausentes], 'extras': [colunas novas], 'tipo_incompativel': [colunas cujo tipo do valor difere do esperado]}, todas as listas ORDENADAS.

```bash
cd modulos/08-ingestao-integracao/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
compare as chaves (faltando/extras) e, nas comuns, compare type(valor).__name__ com o tipo esperado.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def conciliar_schema(esperado, recebido):
    faltando = sorted(c for c in esperado if c not in recebido)
    extras = sorted(c for c in recebido if c not in esperado)
    tipo_incompativel = sorted(c for c in recebido if c in esperado and type(recebido[c]).__name__ != esperado[c])
    return {'faltando': faltando, 'extras': extras, 'tipo_incompativel': tipo_incompativel}
```
:::

---
**Revisado em:** 2026-09-09
