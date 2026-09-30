# Exercício 06 — Resolução de entidades com componentes conexas

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O mesmo cliente aparece como `CRM-17` no CRM, `ECOM-903` no e-commerce e `SAC-55` no atendimento.
Regras de matching (mesmo e-mail, mesmo CPF, mesmo telefone) produzem **pares** "estes dois são a
mesma pessoa" — mas os pares são **transitivos**: se `CRM-17 ~ ECOM-903` (e-mail) e
`ECOM-903 ~ SAC-55` (telefone), os três são a mesma entidade, mesmo sem nenhuma regra ligando
`CRM-17` a `SAC-55` diretamente.

Isso é exatamente uma **componente conexa** num grafo em que os registros são nós e os matches são
arestas — a "resolução de entidades" da teoria 03, base do "cliente 360".

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `resolver_entidades(registros, pares)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — monte o grafo
Nós = registros; cada par vira aresta nos dois sentidos (a relação "é o mesmo que" é simétrica). Valide os ids aqui.
:::
:::{dropdown} Dica 2 — uma busca por grupo
Percorra os registros em ordem; se o registro ainda não tem canônico, faça uma busca (pilha ou fila) a partir dele e colete o grupo inteiro.
:::
:::{dropdown} Dica 3 — o canônico
O canônico do grupo é `min(grupo)`; atribua-o a **todos** os membros de uma vez. Assim cada grupo é explorado uma única vez.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def resolver_entidades(registros: list, pares: list) -> dict:
    ids = set(registros)
    adj = {r: set() for r in ids}
    for a, b in pares:
        if a not in ids or b not in ids:
            raise ValueError(f"par com registro desconhecido: {(a, b)}")
        adj[a].add(b)
        adj[b].add(a)
    canon = {}
    for r in sorted(ids):
        if r in canon:
            continue
        grupo, pilha = {r}, [r]
        while pilha:
            for v in adj[pilha.pop()]:
                if v not in grupo:
                    grupo.add(v)
                    pilha.append(v)
        menor = min(grupo)
        for g in grupo:
            canon[g] = menor
    return dict(sorted(canon.items()))
```
O terceiro teste mostra o risco da transitividade: **um único** par a mais (`SAC-55 ~ SAC-90`,
talvez um telefone compartilhado por uma família) funde dois clientes diferentes num só. Em
produção, por isso, os pares carregam uma **confiança** por regra, e matches fracos (telefone,
endereço) não bastam sozinhos para unir grupos — esse é o trabalho de ferramentas de *entity
resolution* como Splink ou Zingg.

O algoritmo aqui é uma busca por componente (O(n + m)). Em escala, a mesma ideia roda como
*connected components* no Spark GraphFrames ou com a estrutura *union-find*.
:::

---
**Revisado em:** 2026-09-30
