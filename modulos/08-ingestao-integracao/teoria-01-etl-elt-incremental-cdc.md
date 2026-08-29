# Ingestão: ETL vs ELT, full vs incremental, CDC e idempotência

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Todo pipeline começa **trazendo dados de fora para dentro** — de arquivos, bancos, APIs. Isso
é **ingestão**, o "pão com manteiga" da Engenharia de Dados. E aqui moram decisões que separam
um pipeline confiável de um que quebra toda semana: recarrego **tudo** ou só **o que mudou**?
E se o job rodar duas vezes — duplica os dados? Esta unidade dá o vocabulário e os padrões que
o mercado cobra: full vs incremental, **CDC** e **idempotência**.

## 💡 Conceito (o porquê)

### ETL vs ELT — onde a transformação acontece
- **ETL** (Extract-**Transform**-Load): transforma **antes** de carregar no destino. Clássico
  quando o destino é caro/limitado.
- **ELT** (Extract-Load-**Transform**): carrega cru primeiro e transforma **dentro** do
  warehouse (é o que o dbt faz, M7). Domina hoje, com DWs cloud baratos e elásticos.
A ingestão é o **E** (+ **L**) dos dois — trazer os dados para dentro, de forma confiável.

### Full load vs incremental
- **Full load:** recarrega **tudo** toda vez. Simples e robusto para tabelas pequenas; caro e
  lento para grandes.
- **Incremental:** traz **só o que mudou** desde a última carga. Usa uma **marca d'água
  (high-water mark)** — tipicamente `updated_at` ou um `id` crescente: "traga tudo com
  `updated_at > última_marca`". Guarda-se a última marca como **estado** do pipeline.

```{mermaid}
flowchart LR
    F[(Fonte)] -->|updated_at > marca| I[Ingestão incremental]
    I --> D[(Destino)]
    I -->|salva nova marca| S[Estado do pipeline]
```

### CDC (Change Data Capture)
Capturar **as mudanças** (inserts/updates/deletes) de um banco de origem, em vez de reler tudo:
- **Baseado em query:** consulta por `updated_at`/versão (é o incremental acima). Simples, mas
  não pega **deletes** e depende de uma coluna confiável.
- **Baseado em log:** lê o **log de transações** do banco (ex.: WAL do Postgres) e captura toda
  mudança, inclusive deletes, quase em tempo real. Mais poderoso (ferramentas: Debezium), mais
  complexo.

### Idempotência — rodar de novo sem estragar
Um passo é **idempotente** se rodá-lo **duas vezes** dá o **mesmo resultado** que rodar uma vez.
É essencial: jobs falham e são **reexecutados**. Sem idempotência, um retry **duplica** dados.
Como conseguir:
- **Upsert / merge:** `INSERT ... ON CONFLICT (chave) DO UPDATE` — insere se novo, atualiza se
  existe. Reexecutar não duplica.
- **Chave natural/negócio** estável para deduplicar.
- **Partições sobrescrevíveis:** reprocessar um dia = **substituir** a partição daquele dia
  (não anexar).

## 🔎 Exemplo
Uma tabela `clientes` de origem com `updated_at`. Ingestão incremental: guarda a última marca
(`2026-08-20 10:00`), na próxima execução traz só `updated_at > '2026-08-20 10:00'`, faz
**upsert** por `id` no destino e salva a nova marca. Se o job rodar duas vezes seguidas, o
upsert não duplica nada — **idempotente**. Delete na origem? O CDC por log pegaria; o por query,
não.

:::{admonition} 📖 Da literatura
:class: seealso
Densmore trata a ingestão incremental e a idempotência como fundamentos de pipelines
confiáveis: extrair só o que mudou (por marca d'água) e escrever de forma que reexecuções não
dupliquem — via upsert ou sobrescrita de partição. — *Data Pipelines Pocket Reference*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Kleppmann descreve o **CDC baseado em log** como a forma robusta de manter sistemas derivados
(DW, índices, caches) em sincronia com o banco de origem, lendo o log de replicação — a base de
ferramentas como o Debezium. — *Designing Data-Intensive Applications*, cap. 11 (streams/CDC).
:::

## ⚠️ Erros comuns
- **Full load em tudo, sempre** — lento e caro; ignore o incremental só quando a tabela é pequena.
- **Incremental sem idempotência** — um retry duplica linhas.
- Confiar num `updated_at` que a origem **não atualiza** de forma confiável.
- Achar que o incremental por query pega **deletes** — não pega (precisa de CDC por log ou soft-delete).
- Não **persistir a marca d'água** — o pipeline "esquece" onde parou.

## 💼 O que o mercado espera
Ingestão incremental idempotente é **muito cobrada** — é o exercício de maestria deste módulo e
tema recorrente de entrevista ("como você evita duplicar dados num retry?"). Saber quando usar
CDC (e log vs query) diferencia.

:::{admonition} ✨ Em resumo
:class: resumo
- Ingestão é o **E**(+**L**): trazer dados de fora com confiabilidade. ETL transforma antes; ELT depois.
- **Full** = recarrega tudo; **incremental** = só o que mudou, via **marca d'água** persistida.
- **CDC**: por query (simples, sem deletes) ou por log (robusto, pega tudo, ~tempo real).
- **Idempotência** = rodar 2x == rodar 1x; consiga com **upsert** (`ON CONFLICT`) ou sobrescrita de partição.
:::

## 🧠 Quiz de recall
1. Diferença entre full load e incremental?
   :::{dropdown} Resposta
   Full recarrega tudo toda vez; incremental traz só o que mudou desde a última carga, usando uma marca d'água (ex.: updated_at) persistida como estado.
   :::
2. O que é idempotência e por que importa na ingestão?
   :::{dropdown} Resposta
   Rodar o passo 2x dá o mesmo resultado que rodar 1x. Importa porque jobs falham e são reexecutados; sem idempotência, o retry duplica dados. Consegue-se com upsert ou sobrescrita de partição.
   :::
3. O que é CDC e quais as duas abordagens?
   :::{dropdown} Resposta
   Change Data Capture = capturar as mudanças da origem. Por query (consulta updated_at; simples, não pega deletes) ou por log (lê o log de transações; pega tudo, quase em tempo real).
   :::
4. Como um upsert garante idempotência?
   :::{dropdown} Resposta
   `INSERT ... ON CONFLICT (chave) DO UPDATE` insere se a chave é nova e atualiza se já existe — então reexecutar com os mesmos dados não cria duplicatas.
   :::
5. Por que o incremental por query não pega deletes?
   :::{dropdown} Resposta
   Porque ele só vê linhas presentes com updated_at maior que a marca; uma linha apagada some da origem sem "aparecer" na consulta. Precisa de CDC por log ou soft-delete (flag).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você faz uma ingestão que não duplica dados se o job rodar de novo?"
  :::{dropdown} Resposta modelo
  Torno o passo idempotente: escrevo com upsert (`ON CONFLICT (chave) DO UPDATE`) usando a chave natural, ou reprocesso por partição sobrescrevendo o período. Assim, um retry converge para o mesmo estado, sem duplicar.
  :::
- **P:** "Quando você usaria CDC por log em vez de incremental por query?"
  :::{dropdown} Resposta modelo
  Quando preciso de baixa latência (quase tempo real), capturar deletes, ou não confio numa coluna updated_at. O CDC por log (ex.: Debezium lendo o WAL) captura toda mudança; o custo é mais complexidade operacional.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Densmore — Data Pipelines Pocket Reference** (ingestão incremental, idempotência).
- **Kleppmann — Designing Data-Intensive Applications**, cap. 11 (CDC, streams).
- **Reis & Housley — Fundamentals of Data Engineering** (ingestão no ciclo de vida).

## 📚 Referências
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — ingestão incremental e idempotência. <!-- @densmore2021 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 11 (CDC, streams). <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ingestão (ciclo de vida). <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
