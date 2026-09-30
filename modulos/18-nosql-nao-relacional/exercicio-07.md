# Exercício 07 — Índice invertido com posições e busca por frase

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um mecanismo de busca (teoria 04) não varre os textos a cada consulta: ele consulta um **índice
invertido**, que aponta de cada termo para os documentos onde ele aparece. Para ser útil, o
índice passa por **análise de texto**: minúsculas, sem acento, pontuação removida e *stopwords*
("de", "o", "a") descartadas — senão "Café", "cafe" e "café," seriam três termos diferentes.

E para buscar uma **frase** ("banco de dados" como sequência, não três palavras soltas), o índice
precisa guardar também as **posições** de cada termo.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py), implemente `analisar(texto, stopwords)`, `indexar(docs, stopwords)` e `buscar_frase(indice, frase, stopwords)`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — análise
Tire acentos (`unicodedata.normalize("NFKD", ...)`), passe para minúsculas e quebre com `re.split(r"[^a-z0-9]+", ...)`. Numere com `enumerate` **antes** de filtrar as stopwords — assim a posição reflete o texto original.
:::
:::{dropdown} Dica 2 — índice
`indice.setdefault(termo, {}).setdefault(doc_id, []).append(pos)` constrói o dict de dicts de listas em uma linha.
:::
:::{dropdown} Dica 3 — frase
Candidatos = interseção dos documentos de todos os termos. Em cada candidato, para cada posição do 1º termo, confira se os outros estão exatamente no deslocamento esperado (`inicio + (p - base)`).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re
import unicodedata


def analisar(texto: str, stopwords: set) -> list:
    ascii_ = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    tokens = [t for t in re.split(r"[^a-z0-9]+", ascii_) if t]
    return [(i, t) for i, t in enumerate(tokens) if t not in stopwords]


def indexar(docs: list, stopwords: set) -> dict:
    indice = {}
    for doc_id, texto in docs:
        for pos, termo in analisar(texto, stopwords):
            indice.setdefault(termo, {}).setdefault(doc_id, []).append(pos)
    return indice


def buscar_frase(indice: dict, frase: str, stopwords: set) -> list:
    termos = analisar(frase, stopwords)
    if not termos:
        return []
    base = termos[0][0]
    candidatos = None
    for _, t in termos:
        docs = set(indice.get(t, {}))
        candidatos = docs if candidatos is None else candidatos & docs
    resultado = []
    for d in sorted(candidatos or []):
        for inicio in indice[termos[0][1]][d]:
            if all(inicio + (p - base) in indice[t][d] for p, t in termos[1:]):
                resultado.append(d)
                break
    return resultado
```
Guardar a posição **original** (antes de tirar as stopwords) é o que faz "banco de dados" casar
com "banco de DADOS" e não com "dados em banco colunar": o "de" some do índice, mas deixa o buraco
na numeração, e a busca exige `dados` duas posições depois de `banco`. É o que o Elasticsearch faz
numa `match_phrase`.

Repare no efeito colateral do segundo teste: "dados de banco" também casa com "dados **em** banco"
(doc 4), porque qualquer stopword deixa o mesmo buraco. O Elasticsearch tem exatamente esse
comportamento quando se removem stopwords — por isso muitos times preferem **não** removê-las em
campos onde a busca por frase exata importa.

A análise de texto é a parte que mais muda a qualidade da busca: sem a normalização, a busca por
"CAFÉ" não acharia o documento 1. Em português, analisadores reais ainda fazem *stemming* ("dados" →
"dad") para casar singular e plural — com o cuidado de aplicar **a mesma análise** no índice e na
consulta.
:::

---
**Revisado em:** 2026-09-30
