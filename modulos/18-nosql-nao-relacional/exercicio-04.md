# Exercício 04 — Chave de partição: medir o hotspot antes de ir para produção

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 03 avisa: a decisão que mais dói em Cassandra/DynamoDB é a **partition key**. Errou, e um
nó recebe metade do tráfego enquanto os outros dormem — o famoso **hotspot**. O problema é que
esse erro só aparece com dados de verdade, e aí já é tarde para trocar a chave (trocar = reescrever a
tabela inteira).

A saída profissional é **medir antes**: pegar uma amostra do tráfego real, simular a distribuição
de cada chave candidata e escolher com número na mão. É isso que você vai fazer, com 1.200 eventos de
um app em que uma conta corporativa (`c00`) gera um terço do tráfego.

Duas forças puxam em sentidos opostos:
- **distribuição:** quanto mais "única" a chave, mais uniforme (o `evento_id` é quase perfeito);
- **consulta:** a partition key tem de ser **conhecida pela consulta** — senão o banco não sabe em
  qual nó procurar e vira um scan em todos.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `particao`, `distribuicao`,
`fator_skew` e `escolher_chave`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — hash estável
O `hash()` do Python muda a cada execução para strings (`PYTHONHASHSEED`). Use o `zlib.crc32` da
docstring — é o mesmo tipo de função determinística que os bancos usam (o Cassandra usa Murmur3).
:::
:::{dropdown} Dica 2 — distribuição e skew
`cont = [0] * n`; para cada registro, monte `tuple(r[c] for c in chave)` e some 1 em
`cont[particao(...)]`. O skew é `max(cont) / (sum(cont) / len(cont))`.
:::
:::{dropdown} Dica 3 — a escolha
Filtre as elegíveis com `set(chave) <= set(campos_da_consulta)` e use
`min(..., key=lambda c: (skew(c), len(c), c))`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import zlib

def particao(valores, n):
    return zlib.crc32("|".join(str(v) for v in valores).encode("utf-8")) % n

def distribuicao(registros, chave, n):
    cont = [0] * n
    for r in registros:
        cont[particao(tuple(r[c] for c in chave), n)] += 1
    return cont

def fator_skew(contagens):
    total = sum(contagens)
    if not contagens or total == 0:
        raise ValueError("sem registros")
    return round(max(contagens) / (total / len(contagens)), 2)

def escolher_chave(registros, candidatas, n, campos_da_consulta):
    campos = set(campos_da_consulta)
    elegiveis = [list(c) for c in candidatas if set(c) <= campos]
    if not elegiveis:
        raise ValueError("nenhuma chave atende a consulta")
    melhor = min(elegiveis, key=lambda c: (fator_skew(distribuicao(registros, c, n)), len(c), c))
    return tuple(melhor), fator_skew(distribuicao(registros, melhor, n))
```
**Lendo os números:**

| Chave | Skew | Diagnóstico |
|---|---|---|
| `pais` | 7,2 | só 2 valores → no máximo 2 nós trabalham; 6 ficam ociosos |
| `cliente` | 3,33 | o `c00` concentra ~500 eventos num nó só: hotspot |
| `cliente` + `dia` | 1,07 | o "bucketing" por dia espalha o cliente gigante por 28 partições |
| `evento_id` | 1,01 | uniforme — mas nenhuma consulta de negócio conhece o id |

Compor a chave com um **bucket** (dia, hora, ou um sufixo `0..k`) é a técnica padrão para domar
clientes gigantes — ao custo de a consulta ter de informar (ou varrer) os buckets.
:::

---
**Revisado em:** 2026-09-29
