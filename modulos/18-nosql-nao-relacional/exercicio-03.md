# Exercício 03 — Cache key-value com TTL e despejo LRU

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O uso mais comum de um key-value como o Redis (teoria 02) é **cache**: guardar por alguns minutos
o resultado de uma consulta cara. Dois mecanismos mantêm o cache útil e dentro da memória: o
**TTL** (a chave expira sozinha depois de um tempo) e a **política de despejo** quando a memória
enche — a mais comum é **LRU** (*least recently used*), que joga fora o que ninguém usa há mais
tempo.

Um detalhe que surpreende: o Redis expira chaves de forma **preguiçosa** — a chave vencida só é
removida quando alguém tenta lê-la (além de uma varredura periódica). Aqui você vai simular o
comportamento e as métricas que dizem se o cache está funcionando: **hit rate**.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente a classe `Cache`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — OrderedDict
`collections.OrderedDict` guarda a ordem de uso: `move_to_end(chave)` marca como mais recente e `popitem(last=False)` remove a menos recente. Guarde `(valor, expira_em)` como valor.
:::
:::{dropdown} Dica 2 — expiração preguiçosa
Em `get`, se a chave existe mas `agora >= expira_em`, apague, conte `expiradas` e trate como miss. Sem TTL, `expira_em` é `None`.
:::
:::{dropdown} Dica 3 — inserir num cache cheio
Só chaves **novas** podem estourar a capacidade. Nesse caso, primeiro limpe as vencidas; só se ainda faltar espaço despeje a LRU.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from collections import OrderedDict


class Cache:

    def __init__(self, capacidade: int):
        if capacidade < 1:
            raise ValueError("capacidade deve ser >= 1")
        self.capacidade = capacidade
        self._dados = OrderedDict()          # chave -> (valor, expira_em ou None); fim = mais recente
        self.hits = self.misses = self.despejos = self.expiradas = 0

    def _vencida(self, chave, agora) -> bool:
        exp = self._dados[chave][1]
        return exp is not None and agora >= exp

    def set(self, chave, valor, agora: float, ttl: float = None) -> None:
        if chave in self._dados:
            self._dados.move_to_end(chave)
        elif len(self._dados) >= self.capacidade:
            for k in [k for k in self._dados if self._vencida(k, agora)]:
                del self._dados[k]
                self.expiradas += 1
            if len(self._dados) >= self.capacidade:
                self._dados.popitem(last=False)
                self.despejos += 1
        self._dados[chave] = (valor, None if ttl is None else agora + ttl)

    def get(self, chave, agora: float):
        if chave not in self._dados:
            self.misses += 1
            return None
        if self._vencida(chave, agora):
            del self._dados[chave]
            self.expiradas += 1
            self.misses += 1
            return None
        self._dados.move_to_end(chave)
        self.hits += 1
        return self._dados[chave][0]

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return round(self.hits / total, 2) if total else 0.0
```
O teste `vencidas_saem_antes` mostra por que a ordem importa: despejar direto pela LRU jogaria
fora a chave `fixa` (válida) e manteria a `temp`, que já não serve para nada. O Redis tem várias
políticas configuráveis (`allkeys-lru`, `volatile-lru`, `volatile-ttl`…) justamente para esse tipo de
escolha.

Em pipelines de dados, o hit rate é a métrica que diz se o cache paga o próprio custo: um cache de
resultados de consulta com hit rate de 10% só adiciona latência e memória. E o TTL é o que limita o
quão **velho** o dado pode estar — é o freshness (M12) do cache.
:::

---
**Revisado em:** 2026-09-30
