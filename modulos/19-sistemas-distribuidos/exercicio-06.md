# Exercício 06 — Conflitos: last-write-wins x vetores de versão

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Com replicação multi-líder ou sem líder (Dynamo, Cassandra), duas réplicas podem aceitar escritas
na mesma chave ao mesmo tempo. A estratégia mais simples, **last-write-wins** (LWW), fica com a de
maior timestamp — e **descarta a outra em silêncio**. Relógios de máquinas diferentes nem sempre
concordam, então "a mais recente" pode ser a errada.

**Vetores de versão** (teoria 02) resolvem o diagnóstico: cada réplica conta suas próprias
escritas, e comparando os vetores dá para saber se uma versão **sucede** a outra ou se as duas são
**concorrentes** — e aí o conflito precisa ser resolvido, não escondido.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `lww(versoes)`, `comparar_vetores(a, b)` e `versoes_sobreviventes(versoes)`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — LWW
`max(versoes, key=lambda v: (v["ts"], v["no"]))` — timestamp primeiro, nome do nó para desempatar.
:::
:::{dropdown} Dica 2 — comparar vetores
Olhe a união dos nós (`set(a) | set(b)`), com 0 para ausente. Calcule se `a` é menor em algum nó e se é maior em algum: os dois ao mesmo tempo é concorrência.
:::
:::{dropdown} Dica 3 — sobreviventes
Uma versão cai se vier "antes" de alguma outra. Para duplicatas ("igual"), mantenha só a primeira ocorrência.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def lww(versoes: list) -> dict:
    if not versoes:
        raise ValueError("sem versões")
    return max(versoes, key=lambda v: (v["ts"], v["no"]))


def comparar_vetores(a: dict, b: dict) -> str:
    nos = set(a) | set(b)
    menor = any(a.get(n, 0) < b.get(n, 0) for n in nos)
    maior = any(a.get(n, 0) > b.get(n, 0) for n in nos)
    if menor and maior:
        return "concorrente"
    if menor:
        return "antes"
    if maior:
        return "depois"
    return "igual"


def versoes_sobreviventes(versoes: list) -> list:
    vivas = []
    for i, v in enumerate(versoes):
        superada = False
        for j, w in enumerate(versoes):
            if i == j:
                continue
            rel = comparar_vetores(v["vetor"], w["vetor"])
            if rel == "antes" or (rel == "igual" and j < i):
                superada = True
                break
        if not superada:
            vivas.append(v["valor"])
    return sorted(vivas)
```
O mesmo cenário nos dois métodos: o cliente pôs um livro no carrinho pela réplica de SP e uma
caneca pela do RJ, quase ao mesmo tempo. O LWW devolve só a caneca — o livro some sem nenhum erro,
porque o relógio do RJ estava 1 ms à frente. Os vetores mostram que as duas versões são
**concorrentes** e devolvem ambas; a aplicação então resolve (no caso clássico do carrinho da
Amazon descrito no paper do Dynamo, fazendo a **união** dos itens).

LWW não é "errado": é a escolha certa quando perder uma escrita concorrente é aceitável (métricas,
último status de um sensor) e simplicidade importa. O erro é usá-lo sem saber que ele descarta dados.
:::

---
**Revisado em:** 2026-09-30
