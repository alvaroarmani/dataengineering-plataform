# CDC por dentro, schema evolution e exactly-once

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você precisa manter uma cópia analítica de um banco transacional **sempre atualizada** — mas
"recarregar a tabela toda de madrugada" não escala (bilhões de linhas) e perde as mudanças do dia. Pior:
um dia a equipe do app **adiciona uma coluna** na fonte, e seu pipeline **quebra** (ou pior, ignora a
coluna em silêncio). E como garantir que, num pipeline que falha e é reprocessado, cada mudança seja
aplicada **exatamente uma vez**? Estes são os problemas difíceis da ingestão em produção: **CDC**
(capturar só o que mudou), **schema evolution** (a fonte muda de forma), e **exactly-once**. Você viu
CDC e idempotência por alto (teoria 01); aqui está a mecânica que a FIAP e vagas de pleno cobram.

## 💡 Conceito (o porquê)

### CDC: as duas famílias
**Change Data Capture** captura as mudanças (INSERT/UPDATE/DELETE) da fonte para propagá-las. Há dois
jeitos, com trade-offs opostos:
- **Query-based (por consulta):** você consulta periodicamente `WHERE updated_at > último_watermark`.
  Simples, sem acesso especial ao banco — mas **não captura DELETEs** (a linha some, o `updated_at` não
  ajuda), sofre com **dados atrasados** e adiciona carga de leitura na fonte.
- **Log-based (pelo log de transações):** lê o **WAL/binlog** do banco (via Debezium, por ex.) e emite
  cada mudança como um **evento**. Captura **tudo, inclusive DELETEs**, em quase tempo real e com baixo
  impacto na fonte. É o padrão moderno — mais poderoso, mais complexo de operar.

### Aplicando o changelog: o merge
CDC produz um **fluxo de eventos** `{op: I/U/D, chave, valores}`. Materializar a tabela-espelho é
**aplicar** esses eventos ao estado, **em ordem**: `I`/`U` fazem upsert por chave; `D` remove. O
resultado é a fonte replicada. Duas sutilezas: a **ordem importa** (aplicar um U antes do I correspon-
dente corrompe) e o mesmo evento pode chegar duas vezes (at-least-once) — por isso o apply precisa ser
**idempotente** (reaplicar o mesmo changelog dá o mesmo estado).

### Soft delete e tombstones
Muitas plataformas não apagam de fato: marcam **soft delete** (uma flag `is_deleted`) ou emitem um
**tombstone** (evento de deleção que fica no log). Isso preserva o **histórico** para auditoria e
permite reprocessar — importante para analytics (você quer saber que algo foi deletado, não que
simplesmente sumiu).

### Schema evolution: quando a fonte muda de forma
Fontes mudam: colunas nascem, mudam de tipo, somem. Um pipeline maduro **espera** isso (**schema
drift**) e reage por política, em vez de quebrar:
- **Coluna nova na fonte:** normalmente **aditiva e compatível** — absorver (adicionar no destino) é
  seguro. Formatos como **Avro/Parquet** carregam schema e ferramentas fazem *schema merge*.
- **Coluna removida / renomeada:** **quebra** consumidores — exige aviso e versionamento (é aqui que
  entram os **data contracts**, M12/M23).
- **Mudança de tipo:** perigosa (int→string); pode corromper silenciosamente — detectar e barrar.

A defesa é **validar o schema recebido contra o esperado na borda** (o contrato) e classificar o drift:
o que é aditivo/compatível segue; o que é incompatível é barrado ou versionado. **Compatibilidade**
(backward/forward) é o conceito-chave — um Schema Registry (no mundo Kafka) formaliza isso.

### Exactly-once na ingestão
"Exatamente uma vez" quase nunca vem do transporte (é **at-least-once**); obtém-se pela combinação
(M17/M23): **entrega at-least-once + apply idempotente**. Na prática:
- **Idempotência por chave** (upsert/merge) — reaplicar não duplica.
- **Dedup por offset/ID de evento** — descartar eventos já vistos.
- **Escrita transacional/atômica** — o destino confirma o batch todo ou nada.
Assim, mesmo com retries e reentregas, o estado final é como se cada mudança tivesse sido aplicada uma vez.

## 🔎 Exemplo
Uma cópia analítica de `pedidos` usa **CDC log-based** (Debezium lê o binlog): cada INSERT/UPDATE/DELETE
vira um evento num tópico Kafka (M17). Um job **aplica o changelog** à tabela-espelho — upsert por
`pedido_id`, remoção nos DELETEs — de forma **idempotente** (reprocessar o tópico não corrompe). Quando
o app adiciona a coluna `cupom`, o pipeline detecta o **drift**: coluna nova e compatível → absorve
automaticamente (Parquet schema merge); se um dia `valor` mudasse de número para texto, o contrato
**barraria** e alertaria. Exactly-once vem de at-least-once (Kafka) + apply idempotente. A cópia fica
minutos atrás da fonte, resiliente a falhas e a mudanças de schema.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann descreve **Change Data Capture** e o log de transações como fonte de verdade para replicar
dados, além de **schema evolution** e compatibilidade (Avro/schema registry). Reis & Housley tratam CDC,
idempotência e evolução de schema como práticas centrais da ingestão. — *Designing Data-Intensive
Applications* (cap. 4 e 11); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
CDC log-based (Debezium + Kafka) virou o padrão para espelhar bancos em (quase) tempo real sem
martelar a fonte — muito superior ao "full reload noturno". E o incidente clássico de ingestão é o
**schema drift silencioso**: a fonte muda e o pipeline ou quebra ou engole a mudança. Por isso se valida
o schema na borda (contrato) e se projeta o apply para ser idempotente. — Kleppmann; Reis & Housley.
:::

## ⚠️ Erros comuns
- **CDC query-based achando que captura DELETE** — não captura; a linha some sem rastro.
- **Aplicar o changelog fora de ordem** — um U antes do I, ou D/I trocados, corrompe o estado.
- **Apply não idempotente** — reprocessar o log duplica; use upsert/dedup por chave/offset.
- **Ignorar schema drift** — pipeline quebra na mudança, ou (pior) engole em silêncio.
- **Confiar em "exactly-once" do broker** — é at-least-once; a garantia vem do apply idempotente.

## 💼 O que o mercado espera
Explicar CDC query-based × log-based (e por que log-based captura DELETE), aplicar um changelog de forma
idempotente, tratar schema evolution/compatibilidade (contratos, Avro/registry) e obter exactly-once via
at-least-once + idempotência. É o núcleo de ingestão em tempo quase real.

:::{admonition} ✨ Em resumo
:class: resumo
- **CDC**: query-based (simples, **não pega DELETE**, sofre com atraso) vs **log-based** (WAL/binlog/Debezium: pega tudo, quase tempo real).
- **Aplicar o changelog** = upsert (I/U) + remoção (D), **em ordem** e **idempotente**; soft delete/tombstone preservam histórico.
- **Schema evolution**: absorver o aditivo/compatível; **barrar/versionar** o incompatível (contrato, compatibilidade, Avro/registry).
- **Exactly-once** = at-least-once + **apply idempotente** (upsert/dedup por chave/offset + escrita atômica).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre CDC query-based e log-based?
   :::{dropdown} Resposta
   Query-based consulta periodicamente por updated_at (simples, mas não captura DELETEs e sofre com atraso/carga na fonte); log-based lê o log de transações (WAL/binlog) e emite cada mudança como evento — captura tudo, inclusive DELETEs, em quase tempo real.
   :::
2. O que significa "aplicar o changelog" e quais os cuidados?
   :::{dropdown} Resposta
   Materializar a tabela-espelho aplicando os eventos ao estado: upsert por chave nos I/U e remoção nos D. Cuidados: aplicar em ordem e ser idempotente (reprocessar não corrompe/duplica).
   :::
3. Como reagir a uma coluna nova na fonte vs uma mudança de tipo?
   :::{dropdown} Resposta
   Coluna nova costuma ser aditiva/compatível → absorver (schema merge). Mudança de tipo é incompatível e pode corromper → detectar e barrar/versionar (data contract).
   :::
4. Por que soft delete/tombstone importam em analytics?
   :::{dropdown} Resposta
   Preservam o histórico: você registra que algo foi deletado (auditoria, reprocessamento) em vez de a linha simplesmente sumir.
   :::
5. Como se obtém exactly-once na ingestão?
   :::{dropdown} Resposta
   Combinando entrega at-least-once com apply idempotente: upsert/merge por chave, dedup por offset/ID de evento e escrita atômica do batch.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você manteria uma cópia analítica de um banco OLTP sempre atualizada, sem recarregar tudo?"
  :::{dropdown} Resposta modelo
  Com CDC log-based (Debezium lendo o binlog/WAL) publicando as mudanças num tópico Kafka. Um job aplica o changelog à tabela-espelho — upsert por chave nos INSERT/UPDATE e remoção nos DELETE — de forma idempotente e em ordem. Isso mantém a cópia minutos atrás da fonte sem martelá-la com full reloads. Trato schema drift validando contra o contrato na borda e desenho o apply idempotente para exactly-once (at-least-once + upsert/dedup).
  :::
- **P:** "A fonte adicionou uma coluna e mudou o tipo de outra. Como seu pipeline reage?"
  :::{dropdown} Resposta modelo
  Espero schema drift, então valido o schema recebido contra o esperado. A coluna nova é aditiva/compatível — absorvo (schema merge do Parquet/Avro). A mudança de tipo é incompatível e pode corromper silenciosamente: barro a ingestão e alerto, tratando como quebra de contrato que exige versionamento e coordenação com o produtor. Nunca deixo o drift passar em silêncio.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 4 schema evolution, cap. 11 CDC).
- **Reis & Housley — Fundamentals of Data Engineering** (CDC, idempotência, evolução de schema).
- **Documentação do Debezium** e de **Schema Registry** (compatibilidade backward/forward).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — CDC e schema evolution. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ingestão e CDC. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — padrões de ingestão. <!-- @densmore2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
