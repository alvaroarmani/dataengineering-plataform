# Exercício 03 — Rolling update: maxSurge e maxUnavailable

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O Deployment do Kubernetes (teoria 02) troca a versão de uma aplicação **sem derrubá-la**: vai
criando pods novos e removendo antigos aos poucos. Dois parâmetros controlam o ritmo:
**maxSurge** (quantos pods a mais que o desejado podem existir durante a troca) e
**maxUnavailable** (quantos podem estar indisponíveis). Mais folga = troca mais rápida, mas mais
custo (surge) ou menos capacidade (unavailable) no meio do caminho.

Você vai simular a troca passo a passo e medir as duas coisas que importam: quantos passos leva e
qual a **menor disponibilidade** durante o processo.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `rolling_update(replicas, max_surge, max_unavailable)` e `resumo(passos, replicas)`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — três números
Guarde `antigos` e `prontos` (novos já prontos). Como os pendentes ficam prontos no fim do próprio passo, basta somá-los a `prontos` ao final.
:::
:::{dropdown} Dica 2 — a ordem do passo
Remova primeiro (respeitando o mínimo disponível `replicas - max_unavailable`), depois crie (respeitando o teto `replicas + max_surge` e o máximo de `replicas` novos).
:::
:::{dropdown} Dica 3 — o resumo
Inclua o estado inicial (`replicas` disponíveis) no cálculo do mínimo e do máximo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def rolling_update(replicas: int, max_surge: int, max_unavailable: int) -> list:
    if max_surge == 0 and max_unavailable == 0:
        raise ValueError("maxSurge e maxUnavailable não podem ser ambos 0")
    antigos, prontos, passos = replicas, 0, []
    while (antigos, prontos) != (0, replicas):
        disponiveis = antigos + prontos
        remover = min(antigos, max(0, disponiveis - (replicas - max_unavailable)))
        antigos -= remover
        espaco = replicas + max_surge - (antigos + prontos)
        criar = max(0, min(espaco, replicas - prontos))
        prontos += criar
        passos.append((antigos, prontos))
    return passos


def resumo(passos: list, replicas: int) -> dict:
    totais = [replicas] + [a + n for a, n in passos]
    return {"passos": len(passos), "min_disponivel": min(totais), "max_total": max(totais)}
```
Os dois primeiros testes são as duas filosofias. Com `maxSurge=1, maxUnavailable=0`, a capacidade
**nunca** cai abaixo de 4, mas por alguns momentos você paga 5 pods. Com `maxSurge=0,
maxUnavailable=1`, nunca paga a mais, mas a cada passo um pod está sendo trocado. Atenção ao detalhe
do modelo: aqui o pod novo fica pronto no mesmo passo; na vida real, entre criar e ficar pronto
(readiness probe) há um intervalo em que a capacidade **cai** para 3 no segundo cenário.

Com `maxUnavailable` igual ao total de réplicas, o rolling update degenera em "derruba tudo e sobe
tudo" (a estratégia `Recreate`): rápido e simples, com indisponibilidade total — aceitável para um
job de dados, raramente para uma API.
:::

---
**Revisado em:** 2026-09-30
