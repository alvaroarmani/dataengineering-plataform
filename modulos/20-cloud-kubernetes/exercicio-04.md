# Exercício 04 — HPA de verdade: tolerância, limites e várias métricas

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A fórmula do HorizontalPodAutoscaler (teoria 02) é `desejado = ceil(atual × métrica_atual / alvo)`.
Aplicada crua, ela faz o número de pods **oscilar** a cada pequena flutuação. O HPA real tem três
proteções: uma **tolerância** (por padrão 10%: se a razão métrica/alvo está entre 0,9 e 1,1, nada
muda), **limites** mínimo e máximo de réplicas, e, quando há várias métricas (CPU e fila, por
exemplo), ele calcula o desejado para **cada uma** e fica com o **maior**.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `hpa(atual, metricas, min_replicas, max_replicas, tolerancia)`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma proposta por métrica
Para cada `(valor, alvo)`: razão = `valor / alvo`. Dentro da tolerância, a proposta é o próprio `atual`; fora dela, `math.ceil(atual * razao)`.
:::
:::{dropdown} Dica 2 — a maior vence
`min(propostas, key=lambda n: (-propostas[n], n))` acha a métrica com a maior proposta (e desempata pelo nome).
:::
:::{dropdown} Dica 3 — limites por último
Só depois de escolher o desejado aplique `max_replicas` e `min_replicas`, informando no `motivo` quando o limite mudou o resultado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def hpa(atual: int, metricas: dict, min_replicas: int, max_replicas: int, tolerancia: float = 0.1) -> dict:
    if not metricas or min_replicas > max_replicas:
        raise ValueError("configuração inválida")
    propostas = {}
    for nome, (valor, alvo) in metricas.items():
        if alvo <= 0:
            raise ValueError(f"alvo inválido em {nome}")
        razao = valor / alvo
        propostas[nome] = atual if abs(razao - 1) <= tolerancia else math.ceil(atual * razao)
    motivo = min(propostas, key=lambda n: (-propostas[n], n))
    desejado = propostas[motivo]
    if desejado > max_replicas:
        return {"replicas": max_replicas, "motivo": "limite_max"}
    if desejado < min_replicas:
        return {"replicas": min_replicas, "motivo": "limite_min"}
    return {"replicas": desejado, "motivo": motivo}
```
O teste de várias métricas é o caso típico de um consumidor de fila: a CPU está baixa (30% contra
alvo de 60%), mas há 900 mensagens por réplica esperando. Escalar só por CPU manteria o lag crescendo
— o HPA com métrica externa (tamanho da fila, lag do Kafka do M17) pega o que a CPU esconde. Ferramentas
como o KEDA existem justamente para escalar por esse tipo de métrica.

O `limite_max` também é informação: se o motivo aparece com frequência, o teto está baixo demais
para a carga real — ou há um problema que mais réplicas não resolvem (um banco lento a jusante, por
exemplo).
:::

---
**Revisado em:** 2026-09-30
