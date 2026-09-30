# Exercício 04 — Qual arquitetura de dados? (decisão a partir de requisitos)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Contexto
Na vida real ninguém pergunta "qual a arquitetura para *dados brutos*?". Chegam **requisitos**:
"recebemos JSON de app e logs, o time de ciência de dados quer treinar modelos e a diretoria quer
dashboard". Sua tarefa é transformar requisitos em recomendação — **e justificar**, porque uma
recomendação sem motivo não sobrevive à primeira reunião.

A lógica vem da teoria 03 (DW, Lake, Lakehouse):

| Sinal nos requisitos | Pede... | Por quê |
|---|---|---|
| formato não tabular (JSON, log, imagem, áudio) | **lake** | armazenamento barato e sem esquema na escrita |
| consumidor `ml` | **lake** | ML lê arquivos brutos em escala, fora do SQL |
| consumidor `arquivamento` | **lake** | object storage é a camada mais barata |
| consumidor `bi` / `sql_adhoc` | **warehouse** | esquema, SQL rápido, governança |
| `precisa_acid` | **warehouse** | transações, `MERGE`, correções consistentes |

Pediu os dois lados? **Lakehouse** — foi exatamente para esse caso que ele surgiu.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente **`recomendar_arquitetura(req)`**
→ `{"arquitetura": ..., "motivos": [...]}` (motivos em ordem alfabética). Requisito incompleto ou
com valor desconhecido → `ValueError` (falhar alto é melhor do que recomendar às cegas).

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — valide primeiro
Converta para conjuntos: `formatos = set(req.get("formatos") or [])`. Vazio → `ValueError`.
Desconhecido: `formatos - FORMATOS` não vazio → `ValueError`.
:::
:::{dropdown} Dica 2 — junte os motivos num set
Um `if` por motivo, cada um fazendo `motivos.add(...)`. "Algum formato não tabular" é
`formatos - {"tabular"}` não vazio.
:::
:::{dropdown} Dica 3 — a decisão
`lake = bool(motivos & {"dados_nao_estruturados", "consumo_ml", "arquivamento_barato"})`,
`dw = bool(motivos & {"bi_com_esquema", "transacoes_acid"})`. Os dois → lakehouse.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def recomendar_arquitetura(req):
    formatos = set(req.get("formatos") or [])
    consumidores = set(req.get("consumidores") or [])
    if not formatos or not consumidores:
        raise ValueError("requisito incompleto: informe formatos e consumidores")
    if formatos - FORMATOS or consumidores - CONSUMIDORES:
        raise ValueError("formato ou consumidor desconhecido")

    motivos = set()
    if formatos - {"tabular"}:
        motivos.add("dados_nao_estruturados")
    if "ml" in consumidores:
        motivos.add("consumo_ml")
    if "arquivamento" in consumidores:
        motivos.add("arquivamento_barato")
    if consumidores & {"bi", "sql_adhoc"}:
        motivos.add("bi_com_esquema")
    if req.get("precisa_acid", False):
        motivos.add("transacoes_acid")

    lake = bool(motivos & {"dados_nao_estruturados", "consumo_ml", "arquivamento_barato"})
    dw = bool(motivos & {"bi_com_esquema", "transacoes_acid"})
    arq = "lakehouse" if lake and dw else ("data-lake" if lake else "data-warehouse")
    return {"arquitetura": arq, "motivos": sorted(motivos)}
```
Repare no teste `test_acid_sobre_lake_vira_lakehouse`: dados **tabulares**, mas guardados como
arquivo barato **e** precisando de correções transacionais. Não é o formato que decide — é a
combinação de requisitos. Esse raciocínio ("que requisito força qual garantia?") é o mesmo que
você vai usar no desenho do TCC.
:::

---
**Revisado em:** 2026-09-29
