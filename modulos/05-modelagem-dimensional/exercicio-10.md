# Exercício 10 — Bridge table: ratear sem contar em dobro

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um produto pode pertencer a **várias** categorias (um livro de receitas está em "livros" e em
"culinária"). Na modelagem dimensional, esse muitos-para-muitos vira uma **bridge table** (teoria 05)
com um **peso** por par produto–categoria. Sem os pesos, a receita de cada venda é contada
**inteira** em cada categoria — e a soma das categorias passa a ser maior que a receita da empresa.
É um dos erros mais caros de BI, porque os números por categoria parecem plausíveis individualmente.

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `alocar_por_ponte(fatos, ponte)` e `soma_ingenua(fatos, ponte)`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — valide os pesos
Antes de alocar, confira que `sum(pesos.values())` é 1 (com tolerância `abs(... - 1) > 1e-6`) para cada produto.
:::
:::{dropdown} Dica 2 — ratear
Para cada venda, percorra as categorias do produto (ou `{"sem_categoria": 1.0}` se ele não estiver na ponte) somando `receita * peso`.
:::
:::{dropdown} Dica 3 — a soma ingênua
É o que um JOIN simples com a ponte faz: cada categoria recebe a receita **inteira**. Multiplique a receita pelo número de categorias do produto.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def alocar_por_ponte(fatos: list, ponte: dict) -> dict:
    for prod, pesos in ponte.items():
        if abs(sum(pesos.values()) - 1) > 1e-6:
            raise ValueError(f"pesos de {prod} não somam 1")
    res = {}
    for _, prod, receita in fatos:
        for cat, peso in ponte.get(prod, {"sem_categoria": 1.0}).items():
            res[cat] = res.get(cat, 0.0) + receita * peso
    return {c: round(v, 2) for c, v in sorted(res.items())}


def soma_ingenua(fatos: list, ponte: dict) -> float:
    return round(sum(receita * len(ponte.get(prod, {"sem_categoria": 1})) for _, prod, receita in fatos), 2)
```
O teste da soma ingênua é o número que aparece num dashboard mal modelado: **R$ 620** "por categoria"
para uma receita real de **R$ 340**. Cada categoria isolada parece razoável; só a soma denuncia. É
exatamente o que acontece quando alguém faz `JOIN` do fato com a bridge sem multiplicar pelo peso.

O último teste mostra um detalhe prático: com pesos de 1/3, cada parte vira 33,33 e a soma dá 99,99.
Em relatórios financeiros, costuma-se jogar a diferença de arredondamento na maior parte (ou na
última) para que a reconciliação feche no centavo — vale documentar a regra escolhida.
:::

---
**Revisado em:** 2026-09-30
