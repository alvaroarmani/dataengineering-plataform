# Exercício 02 — Hashing consistente com nós virtuais

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No **anel** de hashing consistente (teoria 01), nós e chaves ganham uma posição; cada chave pertence
ao primeiro nó no sentido horário. Ao entrar um nó, só as chaves do trecho dele mudam de dono. Com
poucos nós, porém, os trechos ficam muito desiguais — um nó pode receber o dobro de dados de
outro. A solução usada pelo Dynamo (DeCandia et al., 2007) e pelo Cassandra são os **nós virtuais**:
cada servidor aparece várias vezes no anel.

O mesmo anel também escolhe as **réplicas**: os próximos nós **distintos** no sentido horário.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `construir_anel`, `no_responsavel`, `fracao_realocada_anel` e `replicas`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o anel é uma lista ordenada
Gere `(posicao, no)` para cada nó e cada vnode e ordene. Posição = `zlib.crc32(f"{no}#{i}".encode()) % 2**32`.
:::
:::{dropdown} Dica 2 — busca binária
`bisect.bisect_left(anel, (pos_chave, ""))` acha o primeiro nó com posição >= a da chave; use `i % len(anel)` para dar a volta.
:::
:::{dropdown} Dica 3 — réplicas distintas
A partir desse índice, ande no anel pulando nós que já estão na lista, até ter `r` nós diferentes (com vnodes, o próximo ponto pode ser o mesmo servidor).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import bisect
import zlib

ESPACO = 2 ** 32


def _pos(texto: str) -> int:
    return zlib.crc32(texto.encode("utf-8")) % ESPACO


def construir_anel(nos: list, vnodes: int = 1) -> list:
    return sorted((_pos(f"{no}#{i}"), no) for no in nos for i in range(vnodes))


def no_responsavel(anel: list, chave: str) -> str:
    if not anel:
        raise ValueError("anel vazio")
    i = bisect.bisect_left(anel, (_pos(chave), ""))
    return anel[i % len(anel)][1]


def fracao_realocada_anel(chaves: list, nos_antes: list, nos_depois: list, vnodes: int = 1) -> float:
    a, d = construir_anel(nos_antes, vnodes), construir_anel(nos_depois, vnodes)
    mudam = sum(no_responsavel(a, c) != no_responsavel(d, c) for c in chaves)
    return round(mudam / len(chaves), 4) if chaves else 0.0


def replicas(anel: list, chave: str, r: int) -> list:
    distintos = {no for _, no in anel}
    if r > len(distintos):
        raise ValueError("réplicas demais para os nós disponíveis")
    i = bisect.bisect_left(anel, (_pos(chave), ""))
    out = []
    while len(out) < r:
        no = anel[i % len(anel)][1]
        if no not in out:
            out.append(no)
        i += 1
    return out
```
Compare com o exercício 01: ao adicionar o 5º nó, o módulo movia **81%** das chaves; o anel move
**20%** — perto do ideal de 1/5 — e **só para o nó novo** (nenhuma chave troca entre nós antigos).
Isso é o que permite ao Cassandra ou ao DynamoDB crescer sem parar o serviço.

O teste de equilíbrio mostra o papel dos nós virtuais: com uma posição por nó, o acaso deixou um
servidor com **97,5%** das chaves (os quatro pontos caíram juntos no anel); com 100 posições por nó,
a maior fatia cai para 28,5% (o ideal é 25%). E
as réplicas precisam pular posições do mesmo servidor — sem isso, "3 réplicas" poderiam estar
todas na mesma máquina.
:::

---
**Revisado em:** 2026-09-30
