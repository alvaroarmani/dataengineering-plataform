# Ingestão de arquivos e bancos (landing zone, COPY, dedup)

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Grande parte da ingestão real é **arquivo**: um CSV que cai num bucket toda madrugada, um
JSON que uma API despeja, um export de um banco. Trazer isso para dentro **de forma confiável**
tem armadilhas — encoding, delimitador, schema, e o clássico **arquivo reentregue** que
duplica linhas. Esta unidade mostra os padrões: **landing zone**, carga eficiente no Postgres
(`COPY`) e **deduplicação** na leitura.

## 💡 Conceito (o porquê)

### Landing zone (zona de pouso)
O padrão robusto: **primeiro pouse o arquivo cru** num armazenamento de objetos (MinIO/S3),
**depois** processe. A landing zone é imutável (guarda o dado como chegou), permite
**reprocessar** e separa "receber" de "transformar". É a camada **raw/bronze** do M6, agora
com arquivos.

### Ler arquivos: as armadilhas
- **Encoding** (UTF-8 vs Latin-1) — acentos quebram se errar.
- **Delimitador/aspas** — CSV com `;` ou vírgula dentro de campo.
- **Schema** — tipos (a coluna "valor" veio como texto?), cabeçalho, nulos representados como `""`/`NA`.
- **JSON semi-estruturado** — campos aninhados que viram colunas.

### Carregar no Postgres: `COPY` >> `INSERT`
Para volume, **`COPY`** (carga em bloco a partir de um arquivo/stream) é ordens de grandeza
mais rápido que `INSERT` linha a linha:
```sql
COPY raw_pedidos FROM STDIN WITH (FORMAT csv, HEADER true);
```
Depois, uma camada de staging limpa/converte (como no M6/M7).

### Schema-on-write vs schema-on-read
- **Schema-on-write** (banco relacional): você define o schema **ao gravar**; rejeita o que não encaixa.
- **Schema-on-read** (data lake): guarda cru e aplica schema **na leitura**. Flexível para dados
  variados; o preço é validar mais tarde.

### Dedup na reentrega
Arquivos são **reentregues** (reprocessamento, falha parcial), trazendo linhas repetidas. Padrão
para ficar com a **versão mais recente por chave**:
```sql
SELECT id, valor
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY carregado_em DESC) AS rn
      FROM raw_eventos) t
WHERE rn = 1;
```
`ROW_NUMBER` numera as versões por chave; `rn = 1` mantém a mais nova. (Combina com a
idempotência do upsert, U1.)

## 🔎 Exemplo
Um CSV do Olist cai no MinIO (landing). Um job faz `COPY` para `raw_pedidos` no Postgres. Como
o mesmo arquivo foi reentregue ontem, há linhas duplicadas por `pedido_id`; a camada de staging
aplica o `ROW_NUMBER`/`rn=1` e fica só com a versão mais recente — sem duplicar o fato depois.

:::{admonition} 📖 Da literatura
:class: seealso
Densmore recomenda pousar os dados crus antes de transformar (landing zone) e carregar em bloco
(bulk/`COPY`) para eficiência, tratando reentrega e deduplicação como parte esperada de
pipelines de arquivo. — *Data Pipelines Pocket Reference*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Postgres destaca o `COPY` como a via de carga em massa (muito mais rápida que
`INSERT`s individuais), ideal para ingerir arquivos — a base de quase todo loader de CSV para
Postgres. — PostgreSQL, documentação oficial (`COPY`).
:::

## ⚠️ Erros comuns
- **Transformar antes de pousar** o cru — perde a fonte da verdade e a capacidade de reprocessar.
- `INSERT` linha a linha para milhões de linhas — lento; use `COPY`.
- Ignorar **encoding/delimitador** — acentos e colunas quebram silenciosamente.
- Assumir que **arquivo não se repete** — reentrega é comum; dedup por chave (ou upsert).
- Tratar tudo como `TEXT` e nunca converter os tipos na staging.

## 💼 O que o mercado espera
Carregar arquivos de forma confiável (landing zone + `COPY` + dedup) é rotina de ingestão.
Saber por que se pousa o cru antes de transformar, e como deduplicar reentrega, aparece em
projeto e em entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- **Landing zone:** pouse o arquivo cru (MinIO/S3) antes de transformar — imutável, reprocessável.
- Cuidado com **encoding, delimitador, schema, JSON aninhado** ao ler arquivos.
- Carregue em bloco com **`COPY`** (>> `INSERT` linha a linha).
- **Dedup** de reentrega: `ROW_NUMBER() OVER (PARTITION BY chave ORDER BY carregado_em DESC)` + `rn=1`.
:::

## 🧠 Quiz de recall
1. O que é uma landing zone e por que usá-la?
   :::{dropdown} Resposta
   Uma zona onde o arquivo cru é pousado (MinIO/S3) antes de transformar — imutável, permite reprocessar e separa receber de transformar (camada raw/bronze).
   :::
2. Por que `COPY` em vez de `INSERT` para arquivos grandes?
   :::{dropdown} Resposta
   `COPY` faz carga em bloco, ordens de grandeza mais rápida que `INSERT` linha a linha — feito para volume.
   :::
3. Schema-on-write vs schema-on-read?
   :::{dropdown} Resposta
   Schema-on-write define o schema ao gravar (banco relacional, rejeita o que não encaixa); schema-on-read guarda cru e aplica schema na leitura (data lake, mais flexível).
   :::
4. Como deduplicar linhas de um arquivo reentregue, ficando com a mais recente?
   :::{dropdown} Resposta
   `ROW_NUMBER() OVER (PARTITION BY chave ORDER BY carregado_em DESC)` e filtrar `rn = 1`.
   :::
5. Cite duas armadilhas ao ler arquivos.
   :::{dropdown} Resposta
   Encoding errado (acentos quebram) e delimitador/aspas (CSV com `;` ou vírgula em campo); também schema/tipos e nulos representados como texto.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que pousar o arquivo cru antes de transformar?"
  :::{dropdown} Resposta modelo
  Para ter uma fonte da verdade imutável e poder reprocessar sem depender da origem de novo. A landing zone separa a ingestão (receber) da transformação, e é barata em object storage. Se a lógica de transformação mudar, reprocesso do cru.
  :::
- **P:** "Um arquivo foi reprocessado e duplicou linhas. Como resolve?"
  :::{dropdown} Resposta modelo
  Dedup por chave mantendo a versão mais recente: `ROW_NUMBER() OVER (PARTITION BY id ORDER BY carregado_em DESC)` e fico com `rn=1`; ou faço upsert por chave (idempotência). Assim reentrega não infla os dados.
  :::

## 🚀 Para ir além (leitura dirigida)
- **PostgreSQL docs** — `COPY` (carga em massa).
- **Densmore — Data Pipelines Pocket Reference** (landing zone, arquivos, dedup).

## 📚 Referências
- PostgreSQL — Documentação oficial (`COPY`, carga em massa). <!-- @docs-postgres -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — ingestão de arquivos, landing zone. <!-- @densmore2021 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — armazenamento e ingestão. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
