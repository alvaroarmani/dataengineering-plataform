# Exercício 06 — Scorecard de um data product (DATSIS)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Publicar uma tabela" não é publicar um **data product**. A teoria 01 lista o que um produto de
dados precisa para ser usado sem "perguntar para alguém": dono, descrição, SLA, esquema
documentado, testes passando e classificação de dados sensíveis. Em times com Data Mesh, isso
vira um **scorecard** automático que roda sobre os metadados do catálogo e bloqueia a publicação
de produtos incompletos.

A graça está nas regras reais: um dono `"   "` não é dono; um SLA `{}` não é SLA; e uma coluna
sem a marcação de PII (nem `True`, nem `False`) é uma coluna que ninguém avaliou.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `avaliar_produto(produto)`.

```bash
cd modulos/21-data-produto-finops/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — texto de verdade
Um helper `_texto(v)` que devolve `v.strip()` para strings e `""` para o resto resolve dono, descrição e descrições de coluna (inclusive `None`).
:::
:::{dropdown} Dica 2 — regras sobre listas
"Há colunas **e** todas têm X" é `not cols or any(not X for c in cols)` para a pendência. Mesma ideia para os testes com `all(testes.values())`.
:::
:::{dropdown} Dica 3 — PII explícito
Exija `isinstance(c.get("pii"), bool)`: ausente (`None`) significa "ninguém avaliou", o que é diferente de `False`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
REQUISITOS = ["dono", "descricao", "sla", "schema_documentado", "testes_passando", "pii_classificada"]


def _texto(v) -> str:
    return v.strip() if isinstance(v, str) else ""


def avaliar_produto(produto: dict) -> dict:
    pend = []
    if not _texto(produto.get("dono")):
        pend.append("dono")
    if len(_texto(produto.get("descricao"))) < 20:
        pend.append("descricao")
    fresh = (produto.get("sla") or {}).get("freshness_horas")
    if not (isinstance(fresh, (int, float)) and not isinstance(fresh, bool) and fresh > 0):
        pend.append("sla")
    cols = produto.get("colunas") or []
    if not cols or any(not _texto(c.get("descricao")) for c in cols):
        pend.append("schema_documentado")
    testes = produto.get("testes") or {}
    if not testes or not all(testes.values()):
        pend.append("testes_passando")
    if not cols or any(not isinstance(c.get("pii"), bool) for c in cols):
        pend.append("pii_classificada")
    nota = round(100 * (len(REQUISITOS) - len(pend)) / len(REQUISITOS), 1)
    return {"pronto": not pend, "pendencias": sorted(pend), "nota": nota}
```
O teste mais importante é o da coluna `email_cliente`: sem descrição **e** sem marcação de PII. Um
scorecard que só checasse "existe documentação?" deixaria passar exatamente a coluna mais
arriscada para a LGPD (M14). Tratar "não marcado" como pendência — e não como "não é sensível" — é
o princípio de *secure by default*.

A `nota` serve para acompanhar a evolução do catálogo inteiro (quantos % dos produtos estão
prontos), mas a publicação deve depender de `pronto`, não de uma nota "boa o suficiente": 5 de 6
requisitos com o dono faltando ainda é um produto que ninguém vai manter.
:::

---
**Revisado em:** 2026-09-30
