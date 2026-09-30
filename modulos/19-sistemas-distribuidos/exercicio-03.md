# Exercício 03 — Partição de rede: quem pode continuar?

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Quando a rede se parte, cada grupo de nós só enxerga os do próprio lado — e cada lado pode achar
que o outro morreu. Se os dois continuarem aceitando escritas, é **split-brain**: duas verdades que
depois não se reconciliam. A regra da teoria 03 resolve: só o lado com **maioria** do cluster
original continua; o resto para de aceitar escritas.

Com isso vêm as contas que todo mundo que opera ZooKeeper, etcd ou o KRaft do Kafka precisa fazer
de cabeça: quantas falhas um cluster de N nós tolera, e por que um número **par** de nós não ajuda.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `falhas_toleradas(n)`, `lado_com_quorum(n_total, particoes)` e
`nos_para_tolerar(f)`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a conta das falhas
Maioria de n é `n // 2 + 1`; o que sobra para cair é `n - maioria`, que é igual a `(n - 1) // 2`.
:::
:::{dropdown} Dica 2 — maioria do cluster ORIGINAL
Compare o tamanho de cada partição com `n_total / 2` — não com o total de nós vivos. Nó morto conta contra, porque ele poderia estar vivo do outro lado da partição.
:::
:::{dropdown} Dica 3 — valide as partições
Acumule os nós num set; se uma partição tiver interseção com o que já foi visto, levante `ValueError`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def falhas_toleradas(n: int) -> int:
    if n < 1:
        raise ValueError("cluster vazio")
    return (n - 1) // 2


def nos_para_tolerar(f: int) -> int:
    if f < 0:
        raise ValueError("f negativo")
    return 2 * f + 1


def lado_com_quorum(n_total: int, particoes: list):
    vistos = set()
    for p in particoes:
        if vistos & set(p):
            raise ValueError("nó em duas partições")
        vistos |= set(p)
    for i, p in enumerate(particoes):
        if len(p) > n_total / 2:
            return i
    return None
```
O teste dos nós mortos é o ponto mais contraintuitivo: com 5 nós, 2 mortos e os 3 vivos separados
em 2 + 1, **ninguém** tem quórum e o sistema para de aceitar escritas — mesmo com 3 máquinas de pé.
É o preço da segurança: do ponto de vista do lado com 2 nós, os "mortos" podem estar vivos do outro
lado da rede, aceitando escritas. Esse é o **C** escolhido no lugar do **A** no teorema CAP.

E o cluster de 4 nós tolera a mesma falha única que o de 3, mas pode empatar em 2 × 2 — por isso
ZooKeeper, etcd e controllers do Kafka rodam com 3 ou 5.
:::

---
**Revisado em:** 2026-09-30
