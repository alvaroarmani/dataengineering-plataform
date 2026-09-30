# Exercício 04 — Eleição no Raft: quem pode receber o voto

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No Raft (Ongaro e Ousterhout, 2014; teoria 03), um líder precisa da maioria dos votos. Mas não
basta pedir: cada nó vota **no máximo uma vez por termo** e só vota em candidato cujo **log está
pelo menos tão atualizado quanto o seu** — é a "restrição de eleição" que garante que um líder novo
nunca apague entradas já confirmadas.

"Mais atualizado" tem definição precisa: compara-se o **termo** da última entrada do log; se
empatar, vence o log mais **longo**.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `log_ok(candidato, eleitor)` e `apurar_eleicao(pedidos, eleitores, n_total)`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — comparar logs
Termo maior vence direto; com termo igual, compare os índices com `>=`. É uma comparação lexicográfica — em Python, `candidato >= eleitor` com tuplas faz exatamente isso.
:::
:::{dropdown} Dica 2 — um voto por eleitor
Comece com cada candidato já tendo votado em si mesmo (`votou` = candidatos, `votos` = 1 para cada). Depois, para cada pedido, os eleitores que ainda não votaram e aceitam o log votam nele — em ordem alfabética, para o resultado ser determinístico.
:::
:::{dropdown} Dica 3 — maioria estrita
Líder é quem tem `votos > n_total / 2`. Em cluster de 4, 2 votos não bastam.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def log_ok(candidato: tuple, eleitor: tuple) -> bool:
    return candidato[0] > eleitor[0] or (candidato[0] == eleitor[0] and candidato[1] >= eleitor[1])


def apurar_eleicao(pedidos: list, eleitores: dict, n_total: int):
    votou = {c for c, _ in pedidos}
    votos = {c: 1 for c, _ in pedidos}
    for candidato, log_cand in pedidos:
        for eleitor, log_eleitor in sorted(eleitores.items()):
            if eleitor in votou or eleitor == candidato:
                continue
            if log_ok(log_cand, log_eleitor):
                votou.add(eleitor)
                votos[candidato] += 1
    lider = next((c for c, v in votos.items() if v > n_total / 2), None)
    return {"votos": votos, "lider": lider}
```
No primeiro teste, `a` pede votos primeiro, mas seu log `(3, 10)` é mais curto que o de `b`, `c` e
`e`: eles recusam. `a` só leva o voto de `d`, cujo log é de um termo antigo. Quando `b` pede,
`c` e `e` ainda não votaram — `b` vence com 3 de 5. Se `a` tivesse vencido, entradas confirmadas
que só existem nos logs mais longos poderiam ser apagadas pelo novo líder.

Quando todos os nós se candidatam ao mesmo tempo, cada um vota em si mesmo e ninguém chega à
maioria: é o *split vote*. O termo expira e há nova eleição. O Raft reduz essa chance com
**timeouts aleatórios** — um nó quase sempre se candidata antes dos outros e recolhe os votos. E o
último teste mostra o outro lado da regra: `b` tem o log mais atualizado, mas chegou tarde — `x` e
`y` já tinham votado em `a` neste termo, e voto não se troca.
:::

---
**Revisado em:** 2026-09-30
