# Exercício 07 — Delta log: reconstruir versões, time travel e VACUUM

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Uma tabela Delta é uma pasta de arquivos Parquet mais um **log de transações** (teoria 04). Cada commit
do log registra **ações**: `add` (este arquivo passou a fazer parte da tabela) e `remove` (este deixou
de fazer parte). O estado de uma versão é obtido **reproduzindo** os commits de 0 até ela. É assim que
funcionam o time travel (`VERSION AS OF`, `TIMESTAMP AS OF`) e a atomicidade: um arquivo gravado por
uma escrita que falhou nunca chega a entrar no log.

O `VACUUM` apaga fisicamente os arquivos que saíram da tabela há mais tempo que a retenção — e, a partir
daí, o time travel para versões antigas deixa de funcionar.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py), implemente `arquivos_da_versao(log, versao)`, `versao_no_instante(log, ts)` e
`removiveis_no_vacuum(log, agora, retencao)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — reprodução
Um set de arquivos ativos: para cada commit até a versão pedida, `-=` os removidos e `|=` os adicionados.
:::
:::{dropdown} Dica 2 — por instante
A maior versão cujo `ts <= instante`. Nenhuma → a tabela ainda não existia.
:::
:::{dropdown} Dica 3 — vacuum
Guarde em que instante cada arquivo foi removido; são removíveis os que não estão na versão atual e cuja remoção tem mais idade que a retenção.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def arquivos_da_versao(log: list, versao: int) -> list:
    if not 0 <= versao < len(log):
        raise ValueError(f"versão inexistente: {versao}")
    ativos = set()
    for commit in log[:versao + 1]:
        ativos -= set(commit.get("remove", []))
        ativos |= set(commit.get("add", []))
    return sorted(ativos)


def versao_no_instante(log: list, ts: int) -> int:
    versoes = [i for i, c in enumerate(log) if c["ts"] <= ts]
    if not versoes:
        raise ValueError("instante anterior à criação da tabela")
    return versoes[-1]


def removiveis_no_vacuum(log: list, agora: int, retencao: int) -> list:
    atuais = set(arquivos_da_versao(log, len(log) - 1))
    removidos_em = {}
    for c in log:
        for f in c.get("remove", []):
            removidos_em[f] = c["ts"]
    return sorted(f for f, t in removidos_em.items() if f not in atuais and agora - t > retencao)
```
O commit do `OPTIMIZE` (v3) mostra que o log é só metadado: os dados não mudaram, mas 3 arquivos foram
trocados por 1 compactado — e as versões antigas continuam legíveis enquanto os arquivos existirem. Com
`agora = 600` e retenção de 100, o `VACUUM` apaga os quatro arquivos antigos; depois disso, `VERSION AS
OF 2` falha, porque os Parquet daquela versão sumiram.

Por isso a retenção padrão do Delta é de 7 dias: é a janela em que você consegue desfazer um `MERGE`
errado com time travel. E é também por isso que um `DELETE` por LGPD (M14) só apaga o dado **de fato**
depois do VACUUM.
:::

---
**Revisado em:** 2026-09-30
