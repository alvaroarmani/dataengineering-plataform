# Exercício 03 — Particionamento por chave e ordem garantida

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O Kafka garante ordem **dentro de uma partição**, não no tópico (teoria 02). Por isso a **chave** da
mensagem importa: mesma chave → mesma partição → ordem preservada para aquele cliente. Mensagens
**sem chave** são espalhadas para equilibrar a carga — e perdem qualquer garantia de ordem entre si.

A garantia tem uma condição escondida: ela vale **enquanto o número de partições não muda**.
Aumentar partições de um tópico em produção remapeia chaves, e eventos antigos e novos do mesmo
cliente passam a morar em partições diferentes.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `particao(chave, n)`, `produzir(mensagens, n)` e `chaves_remapeadas(chaves, n_antes, n_depois)`.

```bash
cd modulos/17-streaming-tempo-real/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — hash estável
`zlib.crc32(chave.encode("utf-8")) % n` — nunca o `hash()` do Python, que muda entre execuções.
:::
:::{dropdown} Dica 2 — round-robin
Mantenha um contador só para mensagens **sem** chave: partição = `contador % n`, depois incremente.
:::
:::{dropdown} Dica 3 — remapeamento
Compare `particao(c, n_antes)` com `particao(c, n_depois)` para cada chave e devolva as que mudam, ordenadas.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import zlib


def particao(chave: str, n: int) -> int:
    return zlib.crc32(chave.encode("utf-8")) % n


def produzir(mensagens: list, n: int) -> dict:
    saida = {p: [] for p in range(n)}
    rr = 0
    for chave, valor in mensagens:
        if chave is None:
            p = rr % n
            rr += 1
        else:
            p = particao(chave, n)
        saida[p].append(valor)
    return saida


def chaves_remapeadas(chaves: list, n_antes: int, n_depois: int) -> list:
    return sorted({c for c in chaves if particao(c, n_antes) != particao(c, n_depois)})
```
Os `ping` sem chave se espalham pelas três partições (0, 1, 2), enquanto todos os eventos do
cliente 7 ficam juntos e em ordem na partição 2. Um consumidor dessa partição vê `login → compra →
logout` do cliente 7 exatamente na ordem em que aconteceram — o que permite, por exemplo, uma
máquina de estados por cliente sem precisar reordenar nada.

O último teste mostra o risco operacional: dobrar as partições de 3 para 6 muda a partição de metade
das chaves. Durante a transição, eventos novos do `cliente-1` vão para uma partição e os antigos
ainda estão sendo consumidos em outra — a ordem por cliente quebra. Por isso se dimensiona o número
de partições **com folga** na criação do tópico.
:::

---
**Revisado em:** 2026-09-30
