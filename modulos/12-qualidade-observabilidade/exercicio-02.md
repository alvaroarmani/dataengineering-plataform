# Exercício 02 — Validar um data contract

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um **data contract** (teoria 01) é o acordo entre quem produz e quem consome o dado: quais campos,
de que tipo, obrigatórios ou não, se aceitam nulo. Validar o contrato na **entrada** do pipeline
transforma "o dashboard quebrou na segunda" em "o registro X foi recusado com motivo Y na
sexta".

Você vai implementar o validador — com as pegadinhas de tipo do Python que derrubam validadores
ingênuos (em Python, `True` é um `int`!).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `validar(registro, contrato)`, que devolve a lista de violações, e
`validar_lote(registros, contrato)`, que resume um lote.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — percorra o contrato, depois o registro
Primeiro um laço pelo **contrato** (ausente → nulo → tipo, nessa ordem, com `continue`); depois um laço pelo **registro** para achar campos não previstos.
:::
:::{dropdown} Dica 2 — mapa de tipos
Um dict `{"int": (int,), "float": (int, float), ...}` permite `isinstance(v, TIPOS[tipo])`. Mas `isinstance(True, int)` é `True` — trate `bool` à parte antes.
:::
:::{dropdown} Dica 3 — o resumo
Em `validar_lote`, um registro é válido quando a lista de violações vem vazia (`validos += not v`). Conte cada violação num dict.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
TIPOS = {"int": (int,), "float": (int, float), "str": (str,), "bool": (bool,)}


def validar(registro: dict, contrato: dict) -> list:
    viol = []
    for campo, regra in contrato.items():
        if regra["tipo"] not in TIPOS:
            raise ValueError(f"tipo desconhecido no contrato: {regra['tipo']}")
        if campo not in registro:
            if regra.get("obrigatorio", True):
                viol.append(f"{campo}:ausente")
            continue
        v = registro[campo]
        if v is None:
            if not regra.get("nulo", False):
                viol.append(f"{campo}:nulo")
            continue
        esperado = TIPOS[regra["tipo"]]
        if (isinstance(v, bool) and regra["tipo"] != "bool") or not isinstance(v, esperado):
            viol.append(f"{campo}:tipo")
    viol += [f"{c}:nao_previsto" for c in registro if c not in contrato]
    return sorted(viol)


def validar_lote(registros: list, contrato: dict) -> dict:
    cont, validos = {}, 0
    for r in registros:
        v = validar(r, contrato)
        validos += not v
        for x in v:
            cont[x] = cont.get(x, 0) + 1
    return {"validos": validos, "invalidos": len(registros) - validos, "violacoes": cont}
```
Duas decisões de contrato estão escondidas nos testes. **`float` aceita `int`** porque JSON não
distingue `1` de `1.0` — recusar isso geraria falso positivo em todo lote. **`bool` nunca é
número**: em Python `True == 1`, e um validador com `isinstance(v, int)` aceitaria `"id": true`
vindo de uma API quebrada. É exatamente o tipo de bug que um contrato existe para pegar.

Repare também que o validador **não corrige** nada (não converte `"7"` em `7`): contrato é
detecção. A correção, se houver, é decisão explícita da camada de staging.
:::

---
**Revisado em:** 2026-09-30
