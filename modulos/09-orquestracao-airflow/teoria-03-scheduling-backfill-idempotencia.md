# Scheduling, backfill e idempotência

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Uma DAG roda **repetidamente no tempo** — todo dia, toda hora. Aí surgem as perguntas que
definem um pipeline confiável: por qual **data** essa execução é responsável? E se eu precisar
**reprocessar** ontem (backfill)? Se eu rodar a mesma data **duas vezes**, vou **duplicar** os
dados? Dominar **scheduling**, **backfill** e **idempotência** é o coração do M9 — e o critério
de maestria do módulo.

## 💡 Conceito (o porquê)

### Scheduling e a "data lógica"
Cada execução de uma DAG agendada é responsável por um **intervalo de tempo** e carrega uma
**data lógica** (o *logical/execution date* — o início do período que ela cobre). Você usa essa
data para processar **exatamente aquele período** ("carregue os pedidos **do dia** `{{ ds }}`"),
em vez de "o que existe agora". Isso torna a execução **determinística** e reprodutível.
- `schedule="@daily"` → uma execução por dia, cada uma dona de um dia.
- Referencie a data com templates (`{{ ds }}` = a data lógica em `AAAA-MM-DD`).

### Catchup e backfill
- **Catchup:** ao ligar uma DAG com `start_date` no passado e `catchup=True`, o Airflow roda
  **todas as execuções pendentes** desde então. `catchup=False` roda só a mais recente.
- **Backfill:** rodar **de propósito** um intervalo de datas passadas (ex.: corrigir um bug e
  reprocessar a última semana). Só é seguro se cada execução for **idempotente**.

### Idempotência no orquestrador (a regra de ouro)
Rodar a **mesma data** de novo tem que dar o **mesmo resultado** — sem duplicar. Como cada
execução é dona de um período, o padrão é **reprocessar aquele período** de forma repetível:
- **Overwrite da partição:** `DELETE` das linhas daquele dia e `INSERT` de novo — reprocessar
  substitui, não acumula. (Ótimo quando a execução é dona de um dia inteiro.)
- **Upsert por chave** (`ON CONFLICT`, M8) — insere/atualiza sem duplicar.
Ambos tornam **backfill** e **retry** seguros.

```{mermaid}
flowchart LR
    R[Reprocessar dia D] --> DEL[DELETE onde data = D] --> INS[INSERT dados de D]
    INS --> OK[Mesmo resultado, sem duplicar]
```

### Reprocessamento seguro
Com execuções idempotentes e "donas de um período", você pode **reexecutar qualquer data** (por
falha, bug corrigido, dado corrigido na origem) sem medo — o pilar de um pipeline operável.

## 🔎 Exemplo
A DAG `@daily` de vendas é dona de um dia. A task de carga faz `DELETE FROM fato WHERE data =
'{{ ds }}'` e depois `INSERT` das vendas daquele dia. Se um retry rodar, ou você fizer backfill
da semana, cada dia é **substituído** — nunca duplicado. O dia `2026-08-09` fica intacto quando
você reprocessa `2026-08-10`.

:::{admonition} 📖 Da literatura
:class: seealso
Densmore e a prática de engenharia funcional (Beauchemin) defendem tasks **idempotentes e
determinísticas** — cada execução dona de uma partição/período, reprocessável por overwrite —
como base para backfill e recuperação sem duplicar dados. — *Data Pipelines Pocket Reference*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Airflow trata a **data lógica** e o **catchup/backfill** como centrais: use a
data da execução para processar o período certo e projete tasks idempotentes para que
reprocessar seja seguro. — Apache Airflow, docs oficiais.
:::

## ⚠️ Erros comuns
- Task **não idempotente** (só `INSERT`) — retry/backfill **duplica** os dados.
- Processar "o que existe agora" em vez do **período da data lógica** — resultados não reprodutíveis.
- Ligar com **catchup=True** sem querer — dispara todo o histórico de uma vez.
- Fazer overwrite **sem filtrar pela data** — apaga dados de outros dias.
- Depender de estado externo mutável — quebra a reprodutibilidade.

## 💼 O que o mercado espera
"Como você garante que reprocessar um dia não duplica os dados?" é **a** pergunta de maturidade
em orquestração. A resposta — data lógica + idempotência (overwrite/upsert) — é o critério de
maestria deste módulo.

:::{admonition} ✨ Em resumo
:class: resumo
- Cada execução agendada é **dona de um período** e carrega a **data lógica** (`{{ ds }}`) — processe esse período.
- **Catchup** roda execuções pendentes ao ligar; **backfill** reprocessa datas passadas de propósito.
- **Idempotência** é obrigatória: **overwrite da partição** (DELETE+INSERT do dia) ou **upsert** por chave.
- Com isso, **retry e backfill são seguros** — reprocessar dá o mesmo resultado, sem duplicar.
:::

## 🧠 Quiz de recall
1. O que é a "data lógica" de uma execução e para que serve?
   :::{dropdown} Resposta
   É o início do período que a execução cobre (execution/logical date). Serve para processar exatamente aquele período de forma determinística (ex.: os pedidos do dia {{ ds }}).
   :::
2. Diferença entre catchup e backfill?
   :::{dropdown} Resposta
   Catchup: ao ligar a DAG com start_date no passado, roda automaticamente as execuções pendentes. Backfill: rodar de propósito um intervalo de datas passadas (ex.: reprocessar após corrigir um bug).
   :::
3. Cite dois padrões de idempotência para a carga de um dia.
   :::{dropdown} Resposta
   Overwrite da partição (DELETE das linhas do dia + INSERT) e upsert por chave (ON CONFLICT DO UPDATE).
   :::
4. Por que idempotência é pré-requisito para backfill?
   :::{dropdown} Resposta
   Porque backfill reexecuta datas; sem idempotência, cada reexecução duplicaria os dados daquele período.
   :::
5. Qual o risco de um overwrite sem filtrar pela data?
   :::{dropdown} Resposta
   Apagar dados de outros dias — o DELETE precisa ser restrito ao período da execução (WHERE data = {{ ds }}).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você garante que reprocessar um dia não duplica os dados?"
  :::{dropdown} Resposta modelo
  Faço a execução dona daquele dia (data lógica) e a carga idempotente: `DELETE FROM fato WHERE data = {{ ds }}` seguido do `INSERT` do dia (overwrite da partição), ou um upsert por chave. Assim retry e backfill convergem para o mesmo estado, sem duplicar.
  :::
- **P:** "O que é catchup e quando desligá-lo?"
  :::{dropdown} Resposta modelo
  Catchup faz o Airflow rodar todas as execuções pendentes desde o start_date ao ligar a DAG. Desligo (`catchup=False`) quando não quero reprocessar todo o histórico automaticamente — e faço backfill controlado quando preciso.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Airflow docs** — *DAG Runs*, *Catchup and Backfill*, *Templates* (`ds`).
- **Beauchemin — Functional Data Engineering** (idempotência e determinismo em pipelines).

## 📚 Referências
- Apache Airflow — Documentação oficial (scheduling, catchup/backfill, data lógica). <!-- @docs-airflow -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — idempotência e reprocessamento. <!-- @densmore2021 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — orquestração e reprodutibilidade. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
