# Exercício 04 — TCO: self-hosted x gerenciado e o mês de virada

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Rodar nós mesmos é mais barato, a licença do gerenciado é cara" — até colocar na conta as
**horas de pessoas** para operar, atualizar e apagar incêndio. O **TCO** (custo total de
propriedade, teoria 03) soma custo inicial, custo recorrente de infraestrutura **e** de pessoas ao
longo do tempo. Com crescimento de uso, o recorrente cresce mês a mês, e a opção mais barata pode
**virar** no meio do caminho.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `tco(opcao, meses)`, `comparar(opcoes, meses)` e `mes_de_virada(a, b, max_meses)`.

```bash
cd modulos/21-data-produto-finops/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — somatório mês a mês
`sum(mensal * (1 + g) ** (m - 1) for m in range(1, meses + 1))` — no mês 1 o expoente é 0 (sem crescimento ainda). Pessoas: `horas_mes * custo_hora * meses`.
:::
:::{dropdown} Dica 2 — comparar
Calcule o TCO de cada opção e escolha com `min(valores, key=lambda n: (valores[n], n))`.
:::
:::{dropdown} Dica 3 — virada
Percorra `m` de 1 a `max_meses` e devolva o primeiro em que `tco(a, m) <= tco(b, m)`. Sem virada → `None`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tco(opcao: dict, meses: int) -> float:
    if meses < 0:
        raise ValueError("meses negativo")
    infra = sum(opcao["mensal"] * (1 + opcao["crescimento"]) ** (m - 1) for m in range(1, meses + 1))
    pessoas = opcao["horas_mes"] * opcao["custo_hora"] * meses
    return round(opcao["inicial"] + infra + pessoas, 2)


def comparar(opcoes: dict, meses: int) -> dict:
    valores = {n: tco(o, meses) for n, o in sorted(opcoes.items())}
    return {"tco": valores, "mais_barata": min(valores, key=lambda n: (valores[n], n))}


def mes_de_virada(a: dict, b: dict, max_meses: int = 120):
    for m in range(1, max_meses + 1):
        if tco(a, m) <= tco(b, m):
            return m
    return None
```
No horizonte de 1 ano, o gerenciado ganha com folga (R$ 99,9 mil contra R$ 122 mil): sem custo
inicial e com pouca operação. Mas o crescimento de 2% ao mês na infraestrutura faz a conta virar
no **mês 18**, e em 3 anos o self-hosted sai R$ 116 mil mais barato.

Na vida real, a decisão raramente é só esse número: as 40 horas/mês de operação são 40 horas que o
time não gasta construindo produto (custo de oportunidade), e o risco de incidente no self-hosted
não aparece no TCO. Apresente o TCO **com** as premissas (crescimento, horas) — são elas que a
diretoria vai questionar.
:::

---
**Revisado em:** 2026-09-30
