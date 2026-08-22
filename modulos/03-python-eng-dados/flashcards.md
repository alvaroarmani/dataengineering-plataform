# Flashcards — Módulo 03

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Quando usar list, dict, set e tuple? / **R:** list = sequência ordenada mutável; dict = chave→valor (busca O(1)); set = únicos + pertencimento O(1); tuple = registro fixo imutável (hashável).
- **P:** Por que `set` para checar pertencimento? / **R:** Busca em set é O(1); em list é O(n).
- **P:** O que faz `dict.get(k, 0)`? / **R:** Retorna o valor de `k` ou `0` se ausente — evita `KeyError` ao inicializar acumuladores.
- **P:** Escreva a comprehension de "valores acima de 500". / **R:** `[p["valor"] for p in vendas if p["valor"] > 500]`.
- **P:** list vs tuple? / **R:** list é mutável; tuple é imutável (e hashável — pode ser chave de dict ou elemento de set).
- **P:** Como agregar receita por categoria? / **R:** `acc[c] = acc.get(c, 0.0) + v` num laço; ou `collections.defaultdict(float)`.
- **P:** Como ordenar por receita desc e desempatar por nome asc? / **R:** `sorted(itens, key=lambda kv: (-kv[1], kv[0]))`.
- **P:** Por que Python é tão pedido em dados? / **R:** É a "cola" — ingestão, transformação, automação e testes; segunda skill mais pedida após SQL.
- **P:** "Funções são objetos de primeira classe" — o quê? / **R:** Podem ser atribuídas, passadas como argumento e retornadas — o que permite compor pipelines e usar decorators.
- **P:** Quando usar classe em vez de função? / **R:** Quando há estado que evolui + comportamento sobre ele (ex.: agregador). Se uma função resolve, não crie classe.
- **P:** Por que preferir funções puras? / **R:** Mesmo input → mesmo output, sem efeito colateral: fáceis de testar e casam com idempotência.
- **P:** Armadilha do default mutável? / **R:** `def f(x=[])` reusa o mesmo objeto entre chamadas; use `None` e crie dentro da função.
- **P:** Módulo vs pacote? / **R:** Módulo = um arquivo `.py`; pacote = pasta com `__init__.py`. Importa-se o que precisa.
- **P:** Para que serve `dataclass`? / **R:** Definir registros (dados com pouco comportamento) com menos código (gera `__init__`, `__repr__`, etc.).
- **P:** Por que evitar `except:` pelado? / **R:** Captura qualquer exceção (inclusive bugs e KeyboardInterrupt) e esconde erros. Capture o específico esperado.
- **P:** Padrão de "quarentena" na ingestão? / **R:** Separar válidos de inválidos: processa o que dá certo, coleta/loga o que falhou, sem derrubar o lote.
- **P:** `logging` vs `print`? / **R:** logging tem níveis (DEBUG/INFO/WARNING/ERROR), timestamps e destino configurável; base da observabilidade. print não é controlável em produção.
- **P:** Type hints são validados em runtime? / **R:** Não; documentam contrato e habilitam ferramentas (mypy) e o editor. Para validar, use mypy/pydantic.
- **P:** O que é EAFP? / **R:** "Easier to Ask Forgiveness than Permission" — tentar e tratar a exceção, em vez de checar tudo antes (LBYL).
- **P:** DataFrame vs Series (pandas)? / **R:** DataFrame = tabela (várias colunas); Series = uma coluna (vetor rotulado por índice).
- **P:** loc vs iloc? / **R:** loc seleciona por rótulo (nome); iloc por posição inteira.
- **P:** O que é máscara booleana? / **R:** Series de True/False (ex.: df["v"]>50) usada para filtrar linhas — o "WHERE" do pandas.
- **P:** groupby no pandas? / **R:** Split-apply-combine: divide por grupos, aplica função (sum/mean…), recombina. Ex.: df.groupby("estado")["valor"].sum().
- **P:** Como juntar duas tabelas? / **R:** df.merge(outro, on="chave", how="left") — como um JOIN de SQL.
- **P:** Como tratar NaN? / **R:** dropna() remove; fillna(x) preenche. Decida conscientemente; nulos contaminam contas.
- **P:** Quando pandas não serve? / **R:** Quando os dados não cabem na memória — aí é DuckDB (out-of-core) ou Spark (distribuído).
- **P:** O que é paginação de API? / **R:** A API devolve dados em lotes (páginas); é preciso percorrer todas (page=1,2,3…) até acabar, senão pega só parte.
- **P:** Por que checar `raise_for_status()`? / **R:** Levanta erro se o status HTTP não for 2xx — evita seguir com resposta de erro/vazia.
- **P:** Ingestão incremental? / **R:** Baixar só o novo/que mudou (ex.: ?desde=data) em vez de reprocessar tudo — mais eficiente e reexecutável.
- **P:** CSV vs Parquet? / **R:** Parquet = colunar, binário, tipado, comprime bem, lê só as colunas necessárias. Melhor para analytics em escala.
- **P:** Onde guardar dados brutos de ingestão? / **R:** Object storage (S3/GCS/MinIO) em Parquet, particionado por data (camada raw/bronze).
- **P:** JSON aninhado de API → tabela? / **R:** "Achatar": um dict plano por registro, navegando o aninhamento (ex.: p["cliente"]["nome"]).

---
**Revisado em:** 2026-08-21
