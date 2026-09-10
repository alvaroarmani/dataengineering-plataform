# Exercicio 10 - Bridge table com alocacao ponderada (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica **bridge tables** (muitos-para-muitos) da [teoria 05](teoria-05-modelagem-avancada.md).

## Contexto
Um produto pode pertencer a **varias categorias** (M:N). Somar receita por categoria juntando cruamente **conta em dobro**. A solucao dimensional e uma **bridge table** com **pesos de alocacao** (quanto da receita cada categoria recebe).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`alocar_por_ponte`** - Bridge table (muitos-para-muitos) com alocacao ponderada. `fatos` = lista de (pedido_id, produto_id, receita); `ponte` = {produto_id: {categoria: peso}} (pesos somam 1 por produto). Cada receita e RATEADA entre as categorias do produto pelos pesos (evita contar em dobro no M:N). Retorne {categoria: receita_alocada} (arredonde a soma final a 2 casas).

```bash
cd modulos/05-modelagem-dimensional/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
para cada fato, distribua a receita entre as categorias do produto (receita*peso) e acumule por categoria; arredonde no fim.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def alocar_por_ponte(fatos, ponte):
    res = {}
    for pedido_id, produto_id, receita in fatos:
        for categoria, peso in ponte.get(produto_id, {}).items():
            res[categoria] = res.get(categoria, 0) + receita * peso
    return {c: round(v, 2) for c, v in res.items()}
```
:::

---
**Revisado em:** 2026-09-09
