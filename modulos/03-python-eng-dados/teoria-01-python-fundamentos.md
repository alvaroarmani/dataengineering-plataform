# Python para dados: estruturas que você usa todo dia

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Todo pipeline começa com dados na memória: uma lista de pedidos, um dicionário de
configuração, um conjunto de IDs já processados. **Escolher a estrutura certa** — e saber
percorrê-la de forma limpa — é o que separa um script frágil de um código que você relê em
seis meses e entende. Python é a segunda competência mais pedida em vagas de dados (depois
de SQL) justamente porque **cola tudo**: ingestão, transformação, automação e testes.

## 💡 Conceito (o porquê)

### As quatro estruturas que resolvem 90% dos casos

| Estrutura | Quando usar | Característica |
|---|---|---|
| **list** `[...]` | sequência ordenada, com repetição | mutável, indexável |
| **dict** `{k: v}` | associar chave→valor (um "registro") | busca O(1) por chave |
| **set** `{...}` | coleção **sem repetição**; testar pertencimento | busca O(1), sem ordem garantida |
| **tuple** `(...)` | registro fixo, imutável (ex.: coordenada) | imutável → seguro como chave de dict |

Exemplos de dados:
- Uma linha de venda vira um **dict**: `{"estado": "SP", "valor": 100.0}`.
- Um lote de vendas vira uma **list de dicts**.
- IDs já ingeridos (para evitar duplicar) viram um **set** — pertencimento em O(1).

### Percorrer com clareza: laços e *comprehensions*

O laço básico:
```python
total = 0
for v in vendas:
    total += v["valor"]
```

A forma idiomática para **transformar/filtrar** uma coleção é a *list comprehension* — mais
concisa e legível que um `for` que só preenche uma lista:
```python
altos = [v for v in vendas if v["valor"] > 500]     # filtra
valores = [v["valor"] for v in vendas]              # projeta
```
Isso é o "SQL do Python": `SELECT valor FROM vendas WHERE valor > 500`.

### Funções: a unidade de reuso

Uma função tem **uma responsabilidade** e um contrato claro (o que recebe, o que retorna).
Boas funções são testáveis — e testar é como você corrige exercícios neste curso.

```python
def receita_por_estado(vendas: list[dict]) -> dict:
    acc = {}
    for v in vendas:
        acc[v["estado"]] = acc.get(v["estado"], 0.0) + v["valor"]
    return acc
```

O `dict.get(chave, padrao)` evita o erro clássico de acessar uma chave que ainda não existe
— um padrão que você repete muito em agregação.

## 🔎 Exemplo

Contar quantos pedidos únicos existem e a receita por estado, com estruturas certas:
```python
ids = {p["id"] for p in pedidos}          # set → únicos
qtd = len(ids)
por_estado = receita_por_estado(pedidos)  # dict → agregação
```

:::{admonition} 📖 Da literatura
:class: seealso
McKinney enfatiza que dominar as estruturas nativas de Python (list, dict, set, tuple) é
pré-requisito para usar bem o pandas — a biblioteca constrói sobre esses conceitos.
— *Python for Data Analysis*, cap. 3.
:::

## ⚠️ Erros comuns
- Usar **list** onde um **set** resolveria (checar pertencimento em lista é O(n)).
- Acessar `dict[chave]` sem garantir que a chave existe → `KeyError`; prefira `.get()`.
- `for` que só monta uma lista, onde uma *comprehension* seria mais clara.
- Confundir **mutável** (list, dict) com **imutável** (tuple, str) — e mutar sem querer.
- Não usar ambientes virtuais/versões fixas (visto no lab).

## 💼 O que o mercado espera
Código Python **limpo e testável**: estruturas adequadas, funções pequenas, nomes claros —
não scripts de notebook frágeis. SQL + Python fluentes abrem quase todas as portas Jr.

:::{admonition} ✨ Em resumo
:class: resumo
- Escolha a estrutura certa: **list / dict / set / tuple**.
- **set** para únicos e pertencimento O(1); **`dict.get`** para agregar sem `KeyError`.
- **Comprehensions** são o "SELECT … WHERE" do Python.
- Funções pequenas e testáveis são a unidade de reuso.
:::

## 🧠 Quiz de recall
1. Quando você prefere um `set` a uma `list`?
   :::{dropdown} Resposta
   Quando precisa de elementos únicos e/ou testar pertencimento com frequência — `set` faz isso em O(1); `list` em O(n).
   :::
2. O que faz `dict.get("k", 0)` e por que é útil em agregação?
   :::{dropdown} Resposta
   Retorna o valor da chave `k` ou `0` se ela não existir — evita `KeyError` ao inicializar acumuladores (`acc[k] = acc.get(k,0)+v`).
   :::
3. Reescreva como comprehension: "os valores das vendas acima de 500".
   :::{dropdown} Resposta
   `[v["valor"] for v in vendas if v["valor"] > 500]`.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Qual a diferença entre lista e tupla, e quando usar cada uma?"
  :::{dropdown} Resposta modelo
  Lista é mutável (muda depois de criada); tupla é imutável. Use tupla para registros fixos e quando precisar de algo hashável (ex.: chave de dict ou elemento de set); lista para coleções que mudam.
  :::
- **P:** "Como você somaria um valor por categoria a partir de uma lista de dicionários?"
  :::{dropdown} Resposta modelo
  Percorrendo a lista e acumulando num dict com `.get`: `acc[cat] = acc.get(cat, 0) + v`. Alternativa idiomática: `collections.defaultdict(float)` ou `Counter`.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Sweigart — Automate the Boring Stuff**, caps. de listas/dicionários (aberto, ótimo para começar).
- **McKinney — Python for Data Analysis**, cap. 3 (estruturas nativas) — aberto online.
- **Docs oficiais** — tutorial de estruturas de dados de Python.

## 📚 Referências
- McKinney, W. *Python for Data Analysis*, 3ª ed. (2022) — [leitura aberta](https://wesmckinney.com/book/), cap. 3. <!-- @mckinney2022 -->
- Sweigart, A. *Automate the Boring Stuff with Python*, 2ª ed. (2019) — [leitura aberta](https://automatetheboringstuff.com/). <!-- @sweigart-atbs -->
- Python. *Documentação oficial* — [docs.python.org](https://docs.python.org/3/). <!-- @docs-python -->
- Ramalho, L. *Fluent Python*, 2ª ed. (2022) — cap. sobre modelo de dados. <!-- @ramalho2022 -->

*Acessado em: 2026-08-21.*

---
**Revisado em:** 2026-08-21
