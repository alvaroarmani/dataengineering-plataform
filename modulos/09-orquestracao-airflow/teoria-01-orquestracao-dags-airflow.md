# Orquestração, DAGs e a arquitetura do Airflow

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Você já sabe ingerir (M8) e transformar (M7). Mas um pipeline real tem **muitos passos com
dependências** — extrair → carregar → transformar → validar → notificar — que rodam **na ordem
certa**, **no horário certo**, **de novo se falharem**, e alguém precisa **ver** quando quebra.
Um `cron` não dá conta disso. É o papel do **orquestrador** — e o **Apache Airflow** é o mais
pedido do mercado. Esta unidade dá o conceito (DAGs) e a anatomia do Airflow.

## 💡 Conceito (o porquê)

### Orquestração ≠ cron
Um `cron` dispara um script num horário. Um **orquestrador** cuida do pipeline inteiro:
**dependências** (B só roda depois de A), **retries** (tentar de novo ao falhar),
**backfill** (rodar para datas passadas), **paralelismo**, **monitoramento** (logs, alertas) e
**agendamento**. É a diferença entre "roda um script" e "opera um pipeline".

### DAG: o pipeline como um grafo
No Airflow, um pipeline é uma **DAG** — *Directed Acyclic Graph* (grafo dirigido acíclico):
- **Tasks** (nós): as unidades de trabalho (extrair, carregar, transformar).
- **Dependências** (arestas dirigidas): a ordem (A → B).
- **Acíclico:** sem ciclos — senão o pipeline nunca terminaria.

```{mermaid}
flowchart LR
    E[extrair] --> C[carregar] --> T[transformar] --> V[validar]
    V --> N[notificar]
```
O Airflow lê o grafo e executa as tasks **em ordem topológica** (dependências primeiro),
paralelizando o que é independente.

### Uma DAG é código Python
Você declara a DAG e as tasks em Python; as dependências com `>>`:
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
import datetime as dt

with DAG("pipeline_vendas", start_date=dt.datetime(2026, 1, 1),
         schedule="@daily", catchup=False) as dag:
    extrair    = BashOperator(task_id="extrair",    bash_command="echo extrai")
    transformar= BashOperator(task_id="transformar",bash_command="echo transforma")
    extrair >> transformar        # transformar depende de extrair
```
`schedule="@daily"` agenda diariamente; `catchup=False` evita rodar todo o passado ao ligar.

### Anatomia do Airflow
- **Scheduler:** lê as DAGs, decide o que rodar e quando, e enfileira as tasks.
- **Executor / Workers:** executam as tasks (Local, Celery, Kubernetes...).
- **Metadata DB:** um banco (Postgres) com o **estado** de tudo (execuções, status, XComs).
- **Webserver (UI):** onde você vê DAGs, logs, retries e dispara execuções.

Na bancada do curso, o Airflow roda no profile `airflow` (LocalExecutor sobre o Postgres).

## 🔎 Exemplo
O pipeline de ingestão do M8 vira uma DAG: `baixar_api` → `carregar_postgres` → `dbt_build`
(M7) → `validar`. O scheduler roda **@daily**; se `carregar_postgres` falhar, o Airflow
**tenta de novo** (retries) e `dbt_build` só roda depois do sucesso. Na UI você vê o verde/
vermelho de cada task e os logs.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam a **orquestração** entre as *undercurrents* da engenharia de dados: não é
só agendar, é gerenciar dependências, retries e observabilidade de todo o ciclo — o que
diferencia um pipeline confiável de um punhado de scripts em cron. — *Fundamentals of Data
Engineering* (orquestração).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Airflow descreve a DAG como o modelo central (tasks + dependências, acíclico)
e a arquitetura scheduler/executor/metadata DB/UI — o desenho que sustenta desde pipelines
pequenos até milhares de DAGs em produção. — Apache Airflow, documentação oficial.
:::

## ⚠️ Erros comuns
- Usar **cron** para pipelines com dependências — vira colcha de retalhos frágil.
- **Lógica pesada dentro do arquivo da DAG** (ele é lido a cada scan do scheduler) — mantenha o topo leve.
- Criar **ciclos** ou dependências erradas — a DAG não roda ou roda fora de ordem.
- Ligar com **catchup=True** sem querer — o Airflow tenta rodar todo o histórico de uma vez.
- Confundir **definir** a DAG (código) com **executar** (o scheduler/worker fazem isso).

## 💼 O que o mercado espera
Airflow é **o orquestrador mais pedido** em vagas de DE. Saber modelar um pipeline como DAG,
declarar dependências e entender scheduler/executor/metadata é o mínimo — e cai em entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- **Orquestração** > cron: dependências, retries, backfill, monitoramento, agendamento.
- Um pipeline é uma **DAG** (grafo dirigido **acíclico**): tasks + dependências; roda em ordem topológica.
- A DAG é **código Python**; dependências com `>>`; `schedule`/`catchup` controlam o agendamento.
- Airflow = **scheduler + executor/workers + metadata DB + UI**.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre cron e um orquestrador como o Airflow?
   :::{dropdown} Resposta
   Cron só dispara um script num horário; o orquestrador gerencia o pipeline: dependências, retries, backfill, paralelismo, monitoramento e agendamento.
   :::
2. O que é uma DAG e por que "acíclica"?
   :::{dropdown} Resposta
   Directed Acyclic Graph: tasks (nós) + dependências dirigidas (arestas), sem ciclos — um ciclo faria o pipeline nunca terminar.
   :::
3. Como se declara que uma task depende de outra no Airflow?
   :::{dropdown} Resposta
   Com o operador `>>` (ou `set_downstream`): `a >> b` significa que `b` só roda depois de `a`.
   :::
4. Cite os componentes da arquitetura do Airflow.
   :::{dropdown} Resposta
   Scheduler (decide o que rodar), executor/workers (executam), metadata DB (estado), webserver/UI (visualização e disparo).
   :::
5. O que fazem `schedule` e `catchup`?
   :::{dropdown} Resposta
   `schedule` define a periodicidade (ex.: @daily); `catchup=False` evita rodar todas as execuções passadas ao ligar a DAG.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que Airflow em vez de um cron com scripts?"
  :::{dropdown} Resposta modelo
  Porque pipelines têm dependências, falhas e datas. O Airflow modela isso como DAG, roda na ordem certa, reexecuta o que falhou (retries), permite backfill de datas passadas, paraleliza o independente e dá observabilidade (logs, UI, alertas) — coisas que um cron com scripts não entrega sem virar frágil.
  :::
- **P:** "Onde NÃO colocar lógica pesada numa DAG?"
  :::{dropdown} Resposta modelo
  No topo do arquivo da DAG (fora das tasks), porque o scheduler lê o arquivo repetidamente para descobrir o grafo — código pesado ali degrada o scheduler. A lógica vai dentro das tasks/operators, que rodam nos workers.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Airflow docs** — *Core Concepts* (DAGs, tasks, operators) e *Architecture*.
- **Reis & Housley — Fundamentals of Data Engineering** (orquestração como undercurrent).

## 📚 Referências
- Apache Airflow — Documentação oficial (DAGs, arquitetura, scheduling). <!-- @docs-airflow -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — orquestração. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — agendamento e dependências de pipeline. <!-- @densmore2021 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
