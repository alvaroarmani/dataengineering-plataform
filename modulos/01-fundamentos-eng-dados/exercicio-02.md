# Exercicio 02 - OLTP ou OLAP? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`classifica_carga`** - Classifique a carga: transacao/escrita_pequena/atualizacao_frequente -> 'OLTP'; agregacao/relatorio/historico/analise -> 'OLAP'; senao 'indefinido'.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
dois conjuntos (oltp, olap); o resto e 'indefinido'.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def classifica_carga(desc):
    oltp = {'transacao', 'escrita_pequena', 'atualizacao_frequente'}
    olap = {'agregacao', 'relatorio', 'historico', 'analise'}
    if desc in oltp:
        return 'OLTP'
    if desc in olap:
        return 'OLAP'
    return 'indefinido'
```
:::

---
**Revisado em:** 2026-08-31
