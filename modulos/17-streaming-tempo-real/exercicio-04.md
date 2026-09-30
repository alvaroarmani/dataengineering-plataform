# Exercício 04 — Consumer group: atribuição de partições e lag por consumidor

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Num consumer group (teoria 02), as partições são **divididas** entre os membros: cada partição é
lida por exatamente um consumidor. A estratégia de atribuição por faixas (*range*, a padrão
histórica do Kafka) ordena os consumidores e dá a cada um um bloco contíguo de partições; os
primeiros levam uma partição a mais quando a divisão não é exata. Consumidores **além** do número
de partições ficam ociosos.

O **lag** (offset final − offset commitado) diz se o grupo acompanha o ritmo. Somado por partição,
ele esconde o problema; somado **por consumidor**, mostra qual instância está travada.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `atribuir_range(n_particoes, consumidores)` e `lag_por_consumidor(fim, commits, atribuicao)`.

```bash
cd modulos/17-streaming-tempo-real/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — divmod
`base, extra = divmod(n_particoes, len(consumidores))`: cada um leva `base`, e os `extra` primeiros (na ordem alfabética) levam mais uma. Avance um ponteiro de início para as faixas ficarem contíguas.
:::
:::{dropdown} Dica 2 — lag
Por consumidor: soma de `fim[p] - commits.get(p, 0)` nas partições dele. Um valor negativo é impossível numa operação saudável — erro.
:::
:::{dropdown} Dica 3 — o mais atrasado
`min(saida, key=lambda c: (-saida[c], c))` e só devolva o nome se o lag dele for maior que zero.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def atribuir_range(n_particoes: int, consumidores: list) -> dict:
    if not consumidores:
        raise ValueError("grupo sem consumidores")
    ordem = sorted(consumidores)
    base, extra = divmod(n_particoes, len(ordem))
    saida, inicio = {}, 0
    for i, c in enumerate(ordem):
        qtd = base + (1 if i < extra else 0)
        saida[c] = list(range(inicio, inicio + qtd))
        inicio += qtd
    return saida


def lag_por_consumidor(fim: dict, commits: dict, atribuicao: dict) -> dict:
    saida = {}
    for c, parts in atribuicao.items():
        total = 0
        for p in parts:
            lag = fim[p] - commits.get(p, 0)
            if lag < 0:
                raise ValueError(f"commit à frente do fim na partição {p}")
            total += lag
        saida[c] = total
    pior = min(saida, key=lambda c: (-saida[c], c)) if saida else None
    saida["_mais_atrasado"] = pior if pior is not None and saida[pior] > 0 else None
    return saida
```
No teste de lag, o total do grupo é 827 — um número que, sozinho, não diz nada. Por consumidor, fica
claro que `b` concentra quase tudo (730): é a instância a investigar (travada, lenta, ou com as
partições "quentes" do tópico). Ferramentas de monitoramento de Kafka (Burrow, o próprio
`kafka-consumer-groups.sh --describe`) mostram o lag justamente por partição e por membro.

E o teste dos ociosos responde a uma pergunta clássica de entrevista: colocar 5 consumidores num
tópico de 3 partições não aumenta o paralelismo — dois ficam parados (úteis só como reserva num
rebalanceamento). O paralelismo máximo de um grupo é o número de partições.
:::

---
**Revisado em:** 2026-09-30
