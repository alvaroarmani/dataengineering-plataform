# Exercício 02 — Consistent hashing: nó do dado (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`no_no_anel`** — Num anel de hashing consistente, o dado vai para o 1º nó cuja posição é >= hash da chave; se não houver, dá a volta (menor posição). posicoes = lista de posições dos nós. Retorne a posição do nó responsável.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
ordene as posições >= hash e pegue a 1ª; se nenhuma, dê a volta para min(posicoes).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def no_no_anel(hash_chave, posicoes):
    candidatos = sorted(p for p in posicoes if p >= hash_chave)
    return candidatos[0] if candidatos else min(posicoes)
```
:::

---
**Revisado em:** 2026-08-31
