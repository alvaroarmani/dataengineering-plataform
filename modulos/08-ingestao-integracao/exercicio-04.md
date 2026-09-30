# Exercício 04 — Dedup de reentrega em Python (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Mesma lógica do [Exercício 03](exercicio-03.md) (dedup no Postgres), aqui no navegador.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`dedup(linhas)`** — dado `linhas` = lista de `(id, valor, carregado_em)`, retorne a lista de
  `(id, valor)` da versão **mais recente** (maior `carregado_em`) de cada `id`, **ordenada por id**.

Os testes trazem os casos que aparecem em produção e que a versão ingênua erra:

| Caso real | Regra |
|---|---|
| reentrega antiga chega **depois** da nova | quem manda é `carregado_em`, não a posição na lista |
| duas versões com o **mesmo** `carregado_em` | vence a que vem por último (a ordem de chegada desempata) |
| `valor = None` (exclusão lógica / *tombstone* de CDC) | se a versão mais recente é `None`, o `id` sai do resultado |
| exclusão e depois recriação | vale a mais recente — o registro "renasce" |

```bash
cd modulos/08-ingestao-integracao/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a mais recente por id
Percorra ordenando por `carregado_em` e vá guardando num dict `{id: valor}` — o último a entrar vence.
:::
:::{dropdown} Dica 2 — empate e tombstone
O `sorted` do Python é **estável**: linhas com o mesmo `carregado_em` mantêm a ordem original, então
a última da lista sobrescreve por último. Guarde o `None` no dict normalmente e só filtre **no fim**
— se filtrar antes, uma exclusão não apaga a versão anterior.
:::
:::{dropdown} Dica 3 — saída ordenada
`sorted((k, v) for k, v in mapa.items() if v is not None)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def dedup(linhas):
    mapa = {}
    for id_, valor, _ts in sorted(linhas, key=lambda r: r[2]):   # estável: empate mantém a ordem
        mapa[id_] = valor          # o mais recente sobrescreve (inclusive com None)
    return sorted((k, v) for k, v in mapa.items() if v is not None)
```
Ordenando por `carregado_em` crescente e sobrescrevendo o dict, a última escrita por `id` é a
mais recente — o mesmo efeito do `ROW_NUMBER ... rn=1` do Exercício 03. O tombstone é exatamente
como o CDC (unidade 5) representa um `DELETE`: se você descartar os `None` cedo demais, o registro
apagado na origem **continua vivo** no destino — um bug silencioso clássico.
:::

---
**Revisado em:** 2026-09-29
