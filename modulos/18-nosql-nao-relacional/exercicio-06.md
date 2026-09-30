# Exercício 06 — Quóruns na prática: simular R + W > N

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A regra `R + W > N` (teoria 01) costuma ser decorada. Aqui você vai **simulá-la**: um sistema sem
líder, no estilo Dynamo/Cassandra, com N réplicas. A escrita só é confirmada quando W réplicas
gravam; a leitura consulta R réplicas e fica com a **versão mais nova** entre as respostas. Com
réplicas fora do ar e réplicas atrasadas, dá para ver exatamente quando a leitura pode voltar um
dado velho — e quando o sistema prefere recusar a operação.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `escrever(replicas, w, valor, versao)` e `ler(replicas, r)`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — réplicas disponíveis
`[i for i, r in enumerate(replicas) if r is not None]` dá os índices de quem responde, na ordem. Se forem menos que W (ou R), a operação falha — sem gravar nada.
:::
:::{dropdown} Dica 2 — escrita
Copie a lista (`copy.deepcopy`) e grave `{"versao": v, "valor": x}` só nas W primeiras disponíveis.
:::
:::{dropdown} Dica 3 — leitura
Entre as R primeiras disponíveis, `max(..., key=lambda x: x["versao"])` escolhe a mais nova.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import copy


def escrever(replicas: list, w: int, valor, versao: int) -> list:
    disponiveis = [i for i, r in enumerate(replicas) if r is not None]
    if len(disponiveis) < w:
        raise ValueError(f"só {len(disponiveis)} réplicas disponíveis para W={w}")
    novas = copy.deepcopy(replicas)
    for i in disponiveis[:w]:
        novas[i] = {"versao": versao, "valor": valor}
    return novas


def ler(replicas: list, r: int):
    disponiveis = [x for x in replicas if x is not None]
    if len(disponiveis) < r:
        raise ValueError(f"só {len(disponiveis)} réplicas disponíveis para R={r}")
    return max(disponiveis[:r], key=lambda x: x["versao"])["valor"]
```
Com N = 3, `W = 2, R = 2` garante que o conjunto lido e o escrito **se cruzam** em pelo menos uma
réplica — por isso a leitura sempre vê a versão nova, mesmo começando pela atrasada. Com
`W = 1, R = 1` (soma 2), a leitura pode cair justamente na réplica que não recebeu a escrita. E
`W = 1, R = 3` volta a ser consistente: escrita rápida, leitura cara — é o ajuste de trade-off que o
Cassandra oferece por consulta (`CONSISTENCY ONE`, `QUORUM`, `ALL`).

O último teste de quórum é o **C** do CAP em ação: com duas réplicas fora, o sistema recusa a
escrita em vez de aceitar algo que não consegue replicar. Com `W = 1`, teria aceitado — ganhando
disponibilidade e arriscando perder o dado se a única réplica que gravou cair.
:::

---
**Revisado em:** 2026-09-30
