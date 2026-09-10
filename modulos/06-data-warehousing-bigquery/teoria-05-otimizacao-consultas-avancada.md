# Otimização de consultas e modelagem física avançada

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Duas empresas rodam a **mesma** consulta analítica sobre os **mesmos** dados. Uma paga R$ 2 e
responde em 3 segundos; a outra paga R$ 200 e leva 5 minutos. A diferença não está no SQL — está em
**como os dados foram fisicamente organizados** e em **como o motor executa a consulta**. Você já
viu colunar, partição e cluster (teoria 02) e custo (teoria 04); aqui subimos ao nível de quem
**projeta o layout físico a partir do padrão de consultas** e **lê o plano de execução** para achar o
gargalo. É a diferença entre "escrever SQL que funciona" e "arquitetar um DW que performa e custa
pouco em escala" — o nível que a pós cobra.

## 💡 Conceito (o porquê)

### O modelo de custo: você paga pelo que varre
Em warehouses serverless (BigQuery), o custo e a velocidade são dirigidos por **bytes varridos**, e
duas alavancas físicas os reduzem, **multiplicativamente**:
- **Poda de colunas (colunar):** a consulta lê só as colunas do `SELECT`. Ler 3 de 100 colunas ≈ 3%
  dos bytes.
- **Poda de partições (partition pruning):** com filtro na chave de partição (ex.: data), lê só as
  partições que batem. Filtrar 2 de 24 meses ≈ 8% dos bytes.

Combinadas: `bytes ≈ bytes_das_colunas_lidas × (partições_lidas / partições_totais)`. Uma consulta
bem projetada varre **uma fração minúscula** — daí o R$ 2 vs R$ 200. **Clustering** refina ainda mais:
ordena os dados dentro da partição por colunas muito filtradas, permitindo pular blocos (block
pruning) além das partições.

### Projetar o layout físico a partir do workload
A decisão de **qual coluna particionar e qual clusterizar não é arbitrária** — sai do **padrão de
consultas**:
- **Partição:** a coluna mais usada em **filtros de intervalo** (quase sempre **data/tempo**) — é o
  corte mais grosso, que elimina o máximo de dados.
- **Clustering:** as próximas colunas mais **filtradas por igualdade** (cliente, região) — ordenam
  dentro da partição.

Ou seja: você **mede** como as consultas filtram e desenha a física para elas. Particionar pela
coluna errada (uma que ninguém filtra) não poda nada e ainda adiciona overhead.

### Ler o plano de execução
Todo motor mostra **como** vai executar (`EXPLAIN`/query plan). O que procurar:
- **Predicate pushdown:** o filtro foi empurrado para a leitura (varre menos) ou aplicado tarde
  (varre tudo e filtra depois)?
- **Estratégia de join:** **broadcast** (a tabela pequena é replicada a todos os nós — barato quando
  uma é pequena) vs **shuffle/hash join** (redistribui as duas pela rede — caro). Escolher a errada,
  ou não deixar o motor identificar a tabela pequena, é um gargalo comum.
- **Estágios e spill:** operações que estouram a memória e vão para disco (spill) denunciam
  agregações/joins mal dimensionados.

### Denormalização e pré-agregação: trocar espaço por velocidade
No OLAP, **repetir dado** muitas vezes compensa:
- **Denormalização:** achatar dimensões dentro da fato (ou usar *nested/repeated fields* no BigQuery)
  evita joins caros em tempo de consulta — troca-se armazenamento (barato) por velocidade.
- **Pré-agregação / rollups:** materializar os totais que o dashboard pede toda hora, em vez de
  recalcular sobre bilhões de linhas a cada acesso.
- **Materialized views:** o warehouse mantém uma consulta pré-computada **atualizada** e a usa
  automaticamente quando uma query pode ser respondida por ela — aceleração transparente.

O trade-off é sempre o mesmo: mais armazenamento/atualização em troca de menos custo/tempo de
consulta. Em OLAP, esse trade quase sempre vale.

### Funções aproximadas
Para "quantos usuários únicos?" sobre bilhões de linhas, um `COUNT(DISTINCT)` exato é caríssimo.
Funções **aproximadas** (`APPROX_COUNT_DISTINCT`, baseadas em HyperLogLog) dão ~99% de precisão por
uma fração do custo. Quando o negócio tolera erro pequeno (quase sempre em métricas exploratórias),
é a escolha certa.

## 🔎 Exemplo
Um dashboard varre `eventos` (2 TB, 80 colunas, particionada por dia, 730 dias) toda hora. A consulta
original (sem filtro de data, `SELECT *`) varre os 2 TB — caríssima. O redesenho: a consulta passa a
ler **4 colunas** e filtrar **os últimos 7 dias** → `bytes ≈ (4/80 × 2 TB) × (7/730) ≈ 1 GB` — de 2
TB para ~1 GB, ~2000× menos. Como sempre filtram por `data` e `regiao`, a tabela é **particionada por
data** e **clusterizada por regiao**. Os KPIs fixos viram uma **materialized view** (pré-agregada), e
"usuários únicos" usa `APPROX_COUNT_DISTINCT`. Mesmo dado, mesma pergunta — custo e latência despencam
por **design físico**, não por sorte.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann detalha o armazenamento colunar, compressão e a mecânica de execução de consultas
analíticas (varredura, agregação, joins). Armbrust et al. discutem otimizações do Lakehouse (data
skipping, layout, caching) sobre object storage. Reis & Housley ligam layout físico e custo às
decisões do engenheiro. — *Designing Data-Intensive Applications* (cap. 3); *Lakehouse*; *Fundamentals
of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A "conta surpresa" do BigQuery quase sempre é uma consulta que varre tudo (sem filtro de partição ou
`SELECT *`) rodando de hora em hora. A correção é design físico: particionar/clusterizar pela forma
como se consulta, podar colunas, e materializar o que é repetido. Times maduros revisam o **query
plan** e o **bytes billed** como parte do code review de SQL. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **`SELECT *` e sem filtro de partição** — varre a tabela inteira; a fatura silenciosa clássica.
- **Particionar pela coluna errada** (uma que ninguém filtra) — não poda nada e ainda adiciona overhead.
- **Join grande×grande sem necessidade** — quando um broadcast da tabela pequena resolveria.
- **Recalcular o mesmo agregado sempre** — em vez de materialized view / rollup.
- **`COUNT(DISTINCT)` exato em bilhões** — quando aproximado (HLL) serve com 99% de precisão.

## 💼 O que o mercado espera
Estimar/reduzir bytes varridos (poda de coluna × partição × cluster), projetar o layout físico a
partir do padrão de consultas, ler um plano de execução (pushdown, broadcast vs shuffle) e usar
denormalização/materialized views/funções aproximadas. "Esta consulta está cara/lenta, o que você
faz?" é pergunta certa de pleno/sênior.

:::{admonition} ✨ Em resumo
:class: resumo
- Custo/tempo ≈ **bytes varridos** = (colunas lidas) × (partições lidas / totais); **cluster** refina com block pruning.
- **Projete a física pelo workload**: particione pela coluna de intervalo mais filtrada (data), clusterize pelas de igualdade.
- **Leia o plano**: predicate pushdown, **broadcast vs shuffle join**, spill.
- **Denormalização, pré-agregação/materialized views e funções aproximadas** trocam espaço por velocidade — em OLAP, quase sempre vale.
:::

## 🧠 Quiz de recall
1. Como se estima os bytes varridos por uma consulta num DW colunar particionado?
   :::{dropdown} Resposta
   Aproximadamente (soma dos bytes das colunas lidas) × (partições lidas / partições totais) — poda de coluna e de partição se multiplicam; clustering reduz mais via block pruning.
   :::
2. Como decidir a coluna de partição e a de cluster?
   :::{dropdown} Resposta
   Pelo padrão de consultas: particione pela coluna mais usada em filtros de intervalo (geralmente data); clusterize pelas próximas colunas mais filtradas por igualdade (cliente, região).
   :::
3. Broadcast join vs shuffle join?
   :::{dropdown} Resposta
   Broadcast replica a tabela pequena a todos os nós (barato quando uma é pequena); shuffle/hash join redistribui as duas pela rede (caro). O motor escolhe pela estimativa de tamanho — importante ter estatísticas boas.
   :::
4. O que é predicate pushdown e por que importa?
   :::{dropdown} Resposta
   Empurrar o filtro para a etapa de leitura, varrendo menos dados, em vez de ler tudo e filtrar depois. Reduz bytes lidos e custo.
   :::
5. Quando usar funções aproximadas como APPROX_COUNT_DISTINCT?
   :::{dropdown} Resposta
   Em cardinalidade sobre volumes enormes onde o negócio tolera ~1% de erro; custam uma fração do COUNT(DISTINCT) exato (usam HyperLogLog).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Uma consulta no BigQuery está custando caro demais. Como você reduz?"
  :::{dropdown} Resposta modelo
  Ataco os bytes varridos. Primeiro, poda de coluna: trocar `SELECT *` por só as colunas necessárias. Segundo, poda de partição: garantir filtro na coluna de partição (data). Se a tabela não está particionada/clusterizada conforme o padrão de filtros, redesenho a física. Para consultas repetidas, uso materialized view/rollup; para cardinalidade, APPROX_COUNT_DISTINCT. Confirmo no plano de execução e no bytes billed antes e depois.
  :::
- **P:** "Como você decide como particionar e clusterizar uma tabela nova?"
  :::{dropdown} Resposta modelo
  A partir do workload esperado: analiso quais colunas as consultas mais filtram. A coluna de intervalo mais filtrada (quase sempre data) vira a partição — é o corte que elimina mais dados. As próximas colunas mais filtradas por igualdade (cliente, região) viram clustering, ordenando dentro da partição. Particionar por algo que ninguém filtra não ajuda e adiciona overhead, então a decisão é dirigida pelos padrões de consulta, não por intuição.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 3, execução de consultas analíticas).
- **Armbrust et al. — Lakehouse** (data skipping, layout e caching).
- **Documentação do BigQuery** — partitioning, clustering, materialized views, query plan.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — colunar e execução de consultas. <!-- @kleppmann2017 -->
- Armbrust, M. et al. *Lakehouse: A New Generation of Open Platforms* (2021) — otimização de layout. <!-- @armbrust2020 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — custo e layout físico. <!-- @reis2022 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
