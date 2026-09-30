# Exercício 01 — Sharding por módulo: o custo de crescer

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O jeito mais óbvio de distribuir dados é `shard = hash(chave) % N`. Funciona — até o dia em que o
cluster precisa crescer. A teoria 01 afirma que mudar N "remapeia quase tudo"; neste exercício você
vai **medir** isso, e junto calcular o outro custo da distribuição: a **replicação** multiplica o
armazenamento, e réplicas só protegem se ficarem em **nós diferentes**.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `shard(chave, n)`, `fracao_realocada(chaves, n_antes, n_depois)` e
`armazenamento_por_no(dados_gb, fator, n_nos)`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — hash estável
`zlib.crc32(chave.encode("utf-8")) % n`. O `hash()` do Python muda entre execuções para strings — inútil para decidir onde um dado mora.
:::
:::{dropdown} Dica 2 — medir a realocação
Conte as chaves com `shard(c, n_antes) != shard(c, n_depois)` (booleanos somam como 0/1) e divida pelo total.
:::
:::{dropdown} Dica 3 — réplicas em nós distintos
Se `fator > n_nos`, não há nós diferentes suficientes: levante `ValueError` antes de calcular `dados * fator / n_nos`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import zlib


def shard(chave: str, n: int) -> int:
    if n < 1:
        raise ValueError("n deve ser >= 1")
    return zlib.crc32(chave.encode("utf-8")) % n


def fracao_realocada(chaves: list, n_antes: int, n_depois: int) -> float:
    if not chaves:
        return 0.0
    mudam = sum(shard(c, n_antes) != shard(c, n_depois) for c in chaves)
    return round(mudam / len(chaves), 4)


def armazenamento_por_no(dados_gb: float, fator: int, n_nos: int) -> float:
    if fator < 1 or n_nos < 1:
        raise ValueError("fator e n_nos devem ser >= 1")
    if fator > n_nos:
        raise ValueError(f"impossível manter {fator} réplicas em {n_nos} nós distintos")
    return round(dados_gb * fator / n_nos, 2)
```
Passar de 4 para 5 nós move **81%** das chaves; de 10 para 11, **91%**. Na prática, isso significa
copiar quase o banco inteiro pela rede para ganhar 10% de capacidade — durante a cópia, o cluster
fica mais lento e com risco de inconsistência. Dobrar o número de nós move "só" metade, o que
explica por que sistemas com sharding por módulo crescem em potências de 2.

O próximo exercício resolve isso com **hashing consistente**, em que adicionar o 5º nó move perto
de 1/5 das chaves — e só para o nó novo.
:::

---
**Revisado em:** 2026-09-30
