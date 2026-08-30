# Observabilidade e deploy do Airflow

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Um pipeline em produção **vai falhar** — uma API cai, um dado vem torto, a rede oscila. A
pergunta não é "se", mas "**você vai saber**?". Observabilidade (logs, retries, alertas) é o que
transforma um pipeline frágil em um **operável**. E, para rodar de verdade, o Airflow precisa
ser **deployado** — na bancada do curso, com Docker. Esta unidade fecha o M9 com as duas coisas.

## 💡 Conceito (o porquê)

### Retries: recuperar de falhas transitórias
No Airflow, cada task pode ter **`retries`** e **`retry_delay`**: se falhar, ela **tenta de
novo** automaticamente após um intervalo (idealmente com backoff). `retries=2` significa até
**3 tentativas** no total (1 original + 2 retries). Isso absorve falhas passageiras (rate limit,
timeout) sem intervenção humana — e só faz sentido se a task for **idempotente** (U3).
```python
default_args = {"retries": 2, "retry_delay": dt.timedelta(minutes=5)}
```

### Logs
Cada execução de task guarda **logs** (acessíveis na UI e no storage). É a primeira parada do
debug: você abre a task vermelha → **Logs** → vê o traceback. Logar bem (o que, com que dados)
é parte do trabalho.

### Alertas
Você não fica olhando a UI o dia todo. Configure **notificações** quando algo quebra:
- **`on_failure_callback`** (uma função chamada quando a task falha) → manda e-mail/Slack.
- **SLA:** um prazo para a task terminar; se estourar, dispara um aviso ("o pipeline está atrasado").
Alertar no **failure** e no **SLA** é o mínimo de observabilidade.

### Monitoramento do run
Uma execução da DAG (**DAG run**) tem um estado agregado: **success** se todas as tasks
passaram; **failed** se alguma falhou (após os retries). Você monitora quantas rodaram, quantas
falharam, e a duração — sinais de saúde do pipeline.

### Deploy: rodar o Airflow de verdade
O Airflow não é um script; são **processos** que precisam subir juntos:
- **scheduler** + **webserver** + **workers** + **metadata DB** (Postgres).
- Em produção, cada um pode escalar (ex.: CeleryExecutor com vários workers).
- **Docker/Compose** é a forma padrão de subir tudo reproduzível (é o que a bancada faz: profile
  `airflow` = `apache/airflow` com LocalExecutor sobre o Postgres). Boas práticas: **DAGs
  versionadas** num repositório, **segredos** fora do código (Connections/Variables do Airflow),
  imagem **pinada**.

## 🔎 Exemplo
A task `carregar_api` tem `retries=3`. Um 429 da API faz a 1ª tentativa falhar; o Airflow espera
e tenta de novo — na 2ª, passa. Se falhasse as 4 vezes, o `on_failure_callback` mandaria um
Slack "carregar_api falhou em 2026-08-29", e o DAG run ficaria **failed** na UI, com os logs de
cada tentativa à mão. Tudo isso rodando no Compose da bancada.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam **observabilidade e confiabilidade** entre as *undercurrents*: logs,
retries, alertas e monitoramento não são opcionais — são o que permite operar pipelines em que
as pessoas confiam. — *Fundamentals of Data Engineering* (observabilidade).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Airflow recomenda `retries`/`retry_delay` por task, `on_failure_callback`/SLAs
para alertas, e o deploy via imagem oficial + Compose/Helm com DAGs versionadas e segredos em
Connections — a base de uma operação saudável. — Apache Airflow, docs oficiais.
:::

## ⚠️ Erros comuns
- **Sem retries** — uma falha transitória derruba o pipeline inteiro.
- **Retries sem idempotência** — o retry duplica dados (ver U3).
- **Sem alertas** — o pipeline falha e ninguém percebe até o dashboard ficar vazio.
- **Segredos no código da DAG** — use Connections/Variables e env, nunca commit.
- Achar que "rodou local" = "deployado" — produção precisa de scheduler/worker/DB de pé e escaláveis.

## 💼 O que o mercado espera
Configurar retries, logs e alertas, e saber como o Airflow é deployado (processos + Docker), é
sinal de **maturidade operacional** — muito valorizado, porque separa quem "escreve DAG" de quem
"opera pipeline".

:::{admonition} ✨ Em resumo
:class: resumo
- **Retries/retry_delay** absorvem falhas transitórias (só com idempotência); `retries=N` = N+1 tentativas.
- **Logs** são a 1ª parada do debug; **alertas** (`on_failure_callback`, **SLA**) avisam quando quebra/atrasa.
- Um **DAG run** é success/failed conforme as tasks — monitore falhas e duração.
- **Deploy** = subir scheduler+webserver+workers+metadata DB juntos, via **Docker/Compose**, com DAGs versionadas e segredos fora do código.
:::

## 🧠 Quiz de recall
1. O que `retries=2` significa, e qual o pré-requisito?
   :::{dropdown} Resposta
   Até 3 tentativas no total (1 + 2 retries), com retry_delay entre elas. Pré-requisito: a task ser idempotente, senão o retry duplica dados.
   :::
2. Como o Airflow te avisa quando uma task falha?
   :::{dropdown} Resposta
   Com `on_failure_callback` (função chamada no failure → e-mail/Slack) e SLAs (aviso se a task estourar o prazo). Além dos logs e do estado na UI.
   :::
3. Onde você olha primeiro para debugar uma task vermelha?
   :::{dropdown} Resposta
   Nos logs da task (UI → task → Logs), onde está o traceback/erro.
   :::
4. Quais processos compõem um deploy do Airflow?
   :::{dropdown} Resposta
   Scheduler, webserver (UI), workers/executor e o metadata DB (Postgres) — subindo juntos (ex.: via Docker/Compose), escaláveis em produção.
   :::
5. Onde guardar segredos (senhas, tokens) de uma DAG?
   :::{dropdown} Resposta
   Em Connections/Variables do Airflow ou variáveis de ambiente — nunca no código da DAG.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você torna um pipeline do Airflow observável?"
  :::{dropdown} Resposta modelo
  Retries com retry_delay para falhas transitórias (com tasks idempotentes), logs bem escritos por task, alertas via on_failure_callback (Slack/e-mail) e SLAs para atrasos, e monitoramento do estado dos DAG runs (falhas, duração). Assim eu sei quando e por que algo quebrou.
  :::
- **P:** "Como o Airflow roda em produção?"
  :::{dropdown} Resposta modelo
  Como processos que sobem juntos — scheduler, webserver, workers e o metadata DB — tipicamente via Docker/Compose ou Kubernetes (Helm), com o executor adequado (Local/Celery/K8s), DAGs versionadas em repositório e segredos em Connections/Variables. Não é "rodar um script".
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Airflow docs** — *Retries*, *Callbacks & SLAs*, *Logging*, *Production Deployment* (Docker/Helm).
- **Reis & Housley — Fundamentals of Data Engineering** (observabilidade, confiabilidade).

## 📚 Referências
- Apache Airflow — Documentação oficial (retries, callbacks/SLA, logging, deploy). <!-- @docs-airflow -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — observabilidade e confiabilidade. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — monitoramento e recuperação de pipelines. <!-- @densmore2021 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
