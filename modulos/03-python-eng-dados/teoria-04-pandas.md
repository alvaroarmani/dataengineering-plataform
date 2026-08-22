# pandas: manipulando dados tabulares como um profissional

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Listas e dicionários resolvem o básico, mas quando os dados viram **tabelas** — milhares de
linhas, várias colunas, valores faltando — você precisa de uma ferramenta feita para isso. O
**pandas** é o canivete suíço da manipulação de dados em Python: ler, filtrar, agrupar,
juntar e limpar tabelas com poucas linhas. É onde a maior parte do trabalho de transformação
"na memória" acontece antes de os dados irem para um banco ou warehouse.

## 💡 Conceito (o porquê)

### As duas estruturas: `Series` e `DataFrame`
- **`Series`** — uma coluna (um vetor rotulado por um índice).
- **`DataFrame`** — uma tabela (várias `Series` compartilhando o mesmo índice).

```python
import pandas as pd
df = pd.DataFrame({"estado": ["SP", "RJ", "SP"], "valor": [100, 30, 50]})
```

### Selecionar: rótulo, posição e condição
- **`df["valor"]`** → uma coluna. **`df[["estado", "valor"]]`** → várias.
- **`df.loc[linha, coluna]`** seleciona por **rótulo**; **`df.iloc[i, j]`** por **posição**.
- **Máscara booleana** (o "WHERE" do pandas): `df[df["valor"] > 50]`.

### Agregar: `groupby`
O padrão mais usado em analytics — some/conte por grupo:
```python
df.groupby("estado")["valor"].sum()      # receita por estado
```
Pense nisso como `SELECT estado, SUM(valor) FROM df GROUP BY estado`.

### Juntar: `merge`
Combinar duas tabelas por uma chave (como um JOIN de SQL):
```python
pedidos.merge(clientes, on="cliente_id", how="left")
```

### Dados faltando (`NaN`)
Dados reais vêm sujos. pandas marca ausências como **`NaN`**:
- `df.dropna()` remove linhas com nulos; `df.fillna(0)` preenche.
- Cuidado: nulos "contaminam" contas se não tratados.

## 🔎 Exemplo

```python
# receita por categoria, ignorando linhas sem valor
limpo = df.dropna(subset=["valor"])
receita = limpo.groupby("categoria")["valor"].sum().sort_values(ascending=False)
```

:::{admonition} 📖 Da literatura
:class: seealso
McKinney (criador do pandas) apresenta o `DataFrame` como a estrutura central para análise
tabular em Python, com `groupby` seguindo o modelo **split-apply-combine** — dividir por
grupos, aplicar uma função, recombinar. — *Python for Data Analysis*, caps. 5 e 10.
:::

## ⚠️ Erros comuns
- Confundir **`loc`** (rótulo) com **`iloc`** (posição).
- O aviso *SettingWithCopyWarning*: alterar uma **fatia** achando que altera o original — use `.loc` para atribuir.
- Ignorar **`NaN`** e obter somas/médias erradas.
- Fazer laços `for` linha a linha onde uma operação **vetorizada** (coluna inteira) seria muito mais rápida.
- Achar que pandas escala infinito — para dados **muito** grandes, é Spark/DuckDB (M11/M06).

## 💼 O que o mercado espera
pandas é presença quase certa em vagas de dados. Esperam que você leia um CSV/Parquet,
limpe, agrupe e junte tabelas com fluência — e saiba quando o dado é grande demais para ele.

:::{admonition} ✨ Em resumo
:class: resumo
- **`DataFrame`** = tabela; **`Series`** = coluna.
- Selecione com **`loc`** (rótulo), **`iloc`** (posição) ou **máscara booleana** (WHERE).
- **`groupby`** agrega (split-apply-combine); **`merge`** junta (JOIN).
- Trate **`NaN`** sempre; prefira operações **vetorizadas** a laços.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre `loc` e `iloc`?
   :::{dropdown} Resposta
   `loc` seleciona por **rótulo** (nome do índice/coluna); `iloc` por **posição** inteira (0, 1, 2…).
   :::
2. Como você faria "receita por estado" em pandas?
   :::{dropdown} Resposta
   `df.groupby("estado")["valor"].sum()` — equivalente a `SELECT estado, SUM(valor) GROUP BY estado`.
   :::
3. O que é uma máscara booleana e para que serve?
   :::{dropdown} Resposta
   Uma Series de True/False (ex.: `df["valor"] > 50`) usada para filtrar linhas: `df[mascara]`. É o "WHERE" do pandas.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você trataria valores faltantes numa coluna numérica?"
  :::{dropdown} Resposta modelo
  Depende do caso: remover (`dropna`) se forem poucos e não enviesarem; preencher (`fillna`) com 0, média/mediana ou um valor de negócio; ou marcar e quarentenar. O importante é decidir conscientemente, não ignorar.
  :::
- **P:** "Quando o pandas deixa de ser a ferramenta certa?"
  :::{dropdown} Resposta modelo
  Quando os dados não cabem confortavelmente na memória de uma máquina. Aí parte-se para processamento colunar/out-of-core (DuckDB) ou distribuído (Spark).
  :::

## 🚀 Para ir além (leitura dirigida)
- **McKinney — Python for Data Analysis**, caps. 5 (pandas básico) e 10 (groupby) — aberto online.
- **Docs do pandas** — "10 minutes to pandas" e o guia de *missing data*.

## 📚 Referências
- McKinney, W. *Python for Data Analysis*, 3ª ed. (2022) — [leitura aberta](https://wesmckinney.com/book/), caps. 5 e 10. <!-- @mckinney2022 -->
- pandas. *Documentação oficial* — [pandas.pydata.org/docs](https://pandas.pydata.org/docs/). <!-- @docs-pandas -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
