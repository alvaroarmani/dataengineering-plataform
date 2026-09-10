# Exercicio 02 - Paginacao de API (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`paginar`** - APIs paginam resultados. Dada a lista `itens`, retorne a `pagina` (comeca em 1) de tamanho `tamanho`.

```bash
cd modulos/23-apis-microservicos/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
inicio = (pagina-1)*tamanho; fatie itens[inicio:inicio+tamanho].
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def paginar(itens, pagina, tamanho):
    inicio = (pagina - 1) * tamanho
    return itens[inicio:inicio + tamanho]
```
:::

---
**Revisado em:** 2026-09-09
