# Exercício 10 — Schema drift na borda: aceitar, avisar ou rejeitar

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A fonte muda sem avisar (teoria 05, schema evolution): uma coluna nova aparece, um `int` vira
`float`, um campo obrigatório some. A ingestão precisa decidir **na borda**, registro a registro, o
que fazer — e a decisão não é binária:

- **aceitar**: está tudo como o contrato diz;
- **aceitar com aviso**: mudanças compatíveis (coluna nova, `int` onde se esperava `float`, nulo em
  coluna que aceita nulo) — o dado entra e alguém revisa o contrato;
- **rejeitar**: mudanças que corrompem o destino (obrigatória ausente, tipo incompatível).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `conciliar_schema(esperado, registro)`.

```bash
cd modulos/08-ingestao-integracao/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o tipo de verdade
Um helper `_tipo(v)` que devolve `"bool"` para booleanos **antes** de olhar `type(v).__name__` — senão `True` passaria por `int`.
:::
:::{dropdown} Dica 2 — uma coluna por vez
Para cada coluna do contrato presente: `None` só vale se `nulo` for verdadeiro; tipo igual → ok; `(esperado, recebido)` em `PROMOCOES` → promovida; senão, incompatível.
:::
:::{dropdown} Dica 3 — a decisão
Faltando ou incompatível → rejeitar; senão, extras ou promovidas → aceitar com aviso; senão, aceitar.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
PROMOCOES = {("float", "int")}   # (esperado, recebido) que se pode alargar sem perda


def _tipo(v):
    return "bool" if isinstance(v, bool) else type(v).__name__


def conciliar_schema(esperado: dict, registro: dict) -> dict:
    faltando = sorted(c for c in esperado if c not in registro)
    extras = sorted(c for c in registro if c not in esperado)
    incomp, promo = [], []
    for c, regra in esperado.items():
        if c not in registro:
            continue
        v = registro[c]
        if v is None:
            if not regra["nulo"]:
                incomp.append(c)
            continue
        t = _tipo(v)
        if t == regra["tipo"]:
            continue
        if (regra["tipo"], t) in PROMOCOES:
            promo.append(c)
        else:
            incomp.append(c)
    if faltando or incomp:
        decisao = "rejeitar"
    elif extras or promo:
        decisao = "aceitar_com_aviso"
    else:
        decisao = "aceitar"
    return {"decisao": decisao, "faltando": faltando, "extras": extras,
            "incompativeis": sorted(incomp), "promovidas": sorted(promo)}
```
O `int → float` é a promoção segura clássica (JSON manda `10` onde o contrato diz `10.0`); o contrário,
`float → int` (`1.0` num id), é rejeitado — aceitar poderia truncar `1.7` para `1` em outro registro.
É a mesma regra de compatibilidade que registros de schema (Avro/Protobuf) aplicam.

O `aceitar_com_aviso` é o que mantém o pipeline de pé sem esconder mudanças: a coluna `canal` entra
(ou vai para uma coluna JSON de "extras"), e um alerta avisa que o contrato precisa ser revisado. Os
rejeitados vão para uma **quarentena**, exatamente como no exercício 09 do M12.
:::

---
**Revisado em:** 2026-09-30
