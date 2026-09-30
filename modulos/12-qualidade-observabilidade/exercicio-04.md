# Exercício 04 — Validade: domínio e normalização

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O teste `accepted_values` pega status fora do domínio (`'pago'`, `'cancelado'`…). Na prática, a
maior parte das "violações" é **cosmética** — `' Pago'`, `'PAGO'` — e uma minoria é valor
realmente inválido (`'pg'`, `'???'`). Tratar tudo igual gera dois problemas: se você rejeita, joga
fora dado bom; se normaliza tudo às cegas, esconde bug da fonte.

O relatório certo separa as duas coisas **e conta**, para você saber se é um caso isolado ou
metade da tabela.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `relatorio_dominio(valores, permitidos)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — três baldes
Para cada valor: está em `set(permitidos)` exatamente? → válido. Senão, a versão normalizada está no conjunto normalizado? → corrigível. Senão → inválido.
:::
:::{dropdown} Dica 2 — normalizar com cuidado
Só strings têm `.strip()`. Escreva `_normal(v)` que devolve `v.strip().lower()` para `str` e o próprio `v` para o resto — e trate `None` como inválido antes de normalizar.
:::
:::{dropdown} Dica 3 — percentual
`round(100 * sum(invalidos.values()) / len(valores), 2)`, protegendo a divisão por zero.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _normal(v):
    return v.strip().lower() if isinstance(v, str) else v


def relatorio_dominio(valores: list, permitidos: list) -> dict:
    ok = {_normal(p) for p in permitidos}
    exatos = set(permitidos)
    validos, corr, inv = 0, {}, {}
    for v in valores:
        if v in exatos:
            validos += 1
        elif v is not None and _normal(v) in ok:
            corr[v] = corr.get(v, 0) + 1
        else:
            inv[v] = inv.get(v, 0) + 1
    total = len(valores)
    pct = round(100 * sum(inv.values()) / total, 2) if total else 0.0
    return {"validos": validos, "corrigiveis": corr, "invalidos": inv, "pct_invalido": pct}
```
O teste principal conta a história típica: 2 válidos exatos, 3 **corrigíveis** (espaço e caixa — a
camada de staging resolve com `TRIM`/`LOWER`, como no M06) e 4 **inválidos** de verdade (44%). Um
`accepted_values` puro reprovaria 7 de 9 valores; o relatório mostra que o problema real é o
`'pg'`, que merece conversa com o time que produz o dado.

Note que o próprio contrato pode vir sujo (`"PAGO "` nos permitidos): por isso eles também são
normalizados para a comparação, mas só contam como **válidos exatos** quando batem letra a letra.
:::

---
**Revisado em:** 2026-09-30
