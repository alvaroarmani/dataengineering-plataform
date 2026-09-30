# Exercício 02 — Um pipeline de agregação estilo MongoDB

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No MongoDB, análises não são feitas com `GROUP BY`, e sim com o **pipeline de agregação** (teoria
02): uma lista de estágios em que a saída de um é a entrada do próximo — `$match` filtra, `$unwind`
"explode" um array em um documento por elemento, `$group` agrega e `$sort` ordena. Entender o
pipeline por dentro é o que permite traduzir mentalmente entre SQL e documento — e perceber que
`$unwind` é o equivalente do JOIN com a tabela de itens que a desnormalização (exercício 01) embutiu.

Você vai implementar um mini-interpretador com os quatro estágios, incluindo campos **aninhados**
(`"cliente.cidade"`).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `agregar(docs, pipeline)`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — campo aninhado
Escreva `_pegar(doc, "cliente.cidade")`: quebre por `.` e desça nos dicts; se algo faltar no caminho, devolva `None`.
:::
:::{dropdown} Dica 2 — um estágio por vez
Cada estágio é `{op: arg}` — desempacote com `(op, arg), = estagio.items()` e despache para uma função. A saída vira a entrada do próximo.
:::
:::{dropdown} Dica 3 — unwind e group
No `$unwind`, gere uma **cópia** do doc para cada elemento (`dict(d)` e troque o campo). No `$group`, agrupe num dict pela chave (tire o `$` do caminho) e aplique os acumuladores em cada grupo; `{"$sum": 1}` conta.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _pegar(doc, caminho: str):
    atual = doc
    for parte in caminho.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return None
        atual = atual[parte]
    return atual


def _match(docs, filtro):
    return [d for d in docs if all(_pegar(d, k) == v for k, v in filtro.items())]


def _unwind(docs, campo):
    out = []
    for d in docs:
        for elem in d.get(campo) or []:
            novo = dict(d)
            novo[campo] = elem
            out.append(novo)
    return out


def _group(docs, spec):
    chave = spec["_id"]
    grupos = {}
    for d in docs:
        k = _pegar(d, chave[1:]) if isinstance(chave, str) and chave.startswith("$") else chave
        grupos.setdefault(k, []).append(d)
    out = []
    for k, membros in grupos.items():
        linha = {"_id": k}
        for nome, acc in spec.items():
            if nome == "_id":
                continue
            (op, arg), = acc.items()
            valores = [1] * len(membros) if arg == 1 else [_pegar(m, arg[1:]) or 0 for m in membros]
            if op == "$sum":
                linha[nome] = sum(valores)
            elif op == "$avg":
                linha[nome] = round(sum(valores) / len(valores), 2)
            else:
                raise ValueError(f"acumulador desconhecido: {op}")
        out.append(linha)
    return out


def _sort(docs, ordem):
    for campo, sentido in reversed(list(ordem.items())):
        docs = sorted(docs, key=lambda d: _pegar(d, campo), reverse=sentido == -1)
    return docs


def agregar(docs: list, pipeline: list) -> list:
    atual = [dict(d) for d in docs]
    for estagio in pipeline:
        (op, arg), = estagio.items()
        if op == "$match":
            atual = _match(atual, arg)
        elif op == "$unwind":
            atual = _unwind(atual, arg)
        elif op == "$group":
            atual = _group(atual, arg)
        elif op == "$sort":
            atual = _sort(atual, arg)
        else:
            raise ValueError(f"estágio desconhecido: {op}")
    return atual
```
O pipeline do segundo teste é o equivalente de:
```sql
SELECT i.sku, SUM(i.valor) AS receita, SUM(i.qtd) AS qtd
FROM pedidos p JOIN itens i ON i.pedido_id = p.id
WHERE p.status = 'pago' GROUP BY i.sku ORDER BY receita DESC
```
O `$unwind` faz o papel do JOIN com os itens — só que os itens já estavam **dentro** do pedido.
Repare no pedido 4, sem itens: ele some no `$unwind`, exatamente como sumiria num `INNER JOIN`
(no MongoDB real, `preserveNullAndEmptyArrays: true` faz o papel do `LEFT JOIN`).

A ordem dos estágios importa para desempenho: `$match` **antes** do `$unwind` filtra pedidos inteiros
e usa índice; depois, filtraria item por item.
:::

---
**Revisado em:** 2026-09-30
