# Exercicio 13 - Qual indice usar? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-13/solucao.py`](exercicio-13/solucao.py): implemente **`indice_recomendado`** - Recomende o tipo de indice: 'igualdade' -> 'hash'; 'intervalo'/'ordenacao' -> 'btree'; 'texto_busca'/'json' -> 'gin'; 'append_only' (tabela enorme por tempo) -> 'brin'; qualquer outro -> 'btree' (o coringa).

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-13
pytest -q
```

## Dica
:::{dropdown} Dica
hash=igualdade exata; btree=intervalo/ordem (coringa); gin=texto/json; brin=append-only enorme.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def indice_recomendado(caso):
    mapa = {'igualdade': 'hash', 'intervalo': 'btree', 'ordenacao': 'btree', 'texto_busca': 'gin', 'json': 'gin', 'append_only': 'brin'}
    return mapa.get(caso, 'btree')
```
:::

---
**Revisado em:** 2026-09-09
