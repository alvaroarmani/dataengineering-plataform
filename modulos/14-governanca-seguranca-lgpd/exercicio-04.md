# Exercício 04 — RBAC com herança, curinga e negação explícita

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
RBAC de verdade (teoria 02) é mais que "o papel tem a permissão na lista". Papéis **herdam** de
outros (o `analista_senior` tem tudo do `analista` e mais um pouco), permissões usam **curinga** por
schema (`vendas.*`), e existe **negação explícita**: mesmo com `vendas.*` liberado, a tabela
`vendas.salarios_comissao` fica bloqueada. As duas regras que nunca mudam: **negação vence
permissão** e, na ausência de regra, **nega** (menor privilégio).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `pode_acessar(usuario, recurso, acao, politicas)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — papéis efetivos
Colete os papéis com uma pilha e um conjunto de visitados, seguindo `herda`. O conjunto de visitados é o que impede o ciclo `estagiario ↔ estagiario_b` de travar.
:::
:::{dropdown} Dica 2 — casar o padrão
`"vendas.*"` casa com recursos que começam com `"vendas."` (mantenha o ponto!). Sem curinga, só igualdade.
:::
:::{dropdown} Dica 3 — a ordem da decisão
Primeiro procure uma negação que case (→ `False`); só depois uma permissão (→ `True`); no fim, `False`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _casa(padrao: str, recurso: str) -> bool:
    if padrao.endswith(".*"):
        return recurso.startswith(padrao[:-1])
    return padrao == recurso


def _papeis_efetivos(papeis_iniciais, definicoes) -> set:
    vistos, pilha = set(), list(papeis_iniciais)
    while pilha:
        p = pilha.pop()
        if p in vistos or p not in definicoes:
            continue
        vistos.add(p)
        pilha.extend(definicoes[p].get("herda", []))
    return vistos


def pode_acessar(usuario: str, recurso: str, acao: str, politicas: dict) -> bool:
    papeis = _papeis_efetivos(politicas["usuarios"].get(usuario, []), politicas["papeis"])
    regras_nega, regras_permite = [], []
    for p in papeis:
        regras_nega += politicas["papeis"][p].get("nega", [])
        regras_permite += politicas["papeis"][p].get("permite", [])

    def casa(regra):
        padrao, a = regra
        return _casa(padrao, recurso) and a in ("*", acao)

    if any(casa(r) for r in regras_nega):
        return False
    return any(casa(r) for r in regras_permite)
```
O `bruno` mostra por que a negação precisa ser avaliada **depois** de resolver a herança: ele
ganha `vendas.*` para escrever pelo papel sênior, mas herda também a negação do `analista` sobre
`vendas.salarios_comissao`. Se a negação só valesse no papel em que foi declarada, subir de cargo
abriria acesso aos salários.

O teste do `rhx.folha` pega um bug clássico de curinga: comparar só com `startswith("rh")` liberaria
qualquer schema cujo nome começa com "rh". É o mesmo cuidado dos *grants* no BigQuery e no
Snowflake: o escopo é o schema inteiro, não um prefixo de texto.
:::

---
**Revisado em:** 2026-09-30
