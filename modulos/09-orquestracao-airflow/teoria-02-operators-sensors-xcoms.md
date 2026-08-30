# Operators, tasks, sensors e XComs

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Uma DAG (U1) define **o quê** roda e **em que ordem**. Falta o **como cada task faz o
trabalho**: rodar um script Python, um SQL, esperar um arquivo chegar, ou passar um valor de
uma task para a próxima. No Airflow isso são **operators**, **sensors** e **XComs** — as peças
com que você monta pipelines de verdade.

## 💡 Conceito (o porquê)

### Operators: o "tipo" de uma task
Um **operator** é um molde de task para um tipo de trabalho:
- **BashOperator** — roda um comando shell.
- **PythonOperator** (ou o `@task` da **TaskFlow API**) — roda uma função Python.
- **SQL operators** (ex.: `SQLExecuteQueryOperator`) — roda SQL num banco.
- Muitos outros (transferências, cloud) via **providers**.

Com a **TaskFlow API** (moderna), uma task Python é só uma função decorada:
```python
from airflow.decorators import dag, task

@dag(schedule="@daily", start_date=..., catchup=False)
def meu_pipeline():
    @task
    def extrair():
        return [1, 2, 3]
    @task
    def somar(nums):
        return sum(nums)
    somar(extrair())      # a dependência é inferida pela passagem do valor
meu_pipeline()
```

### Sensors: esperar por uma condição
Um **sensor** é uma task que **espera** algo acontecer antes de liberar o resto: um arquivo
pousar, uma partição existir, um horário chegar. Ele **"poka"** (verifica) periodicamente até
a condição ser verdadeira (ou estourar um timeout). Ex.: `FileSensor`, `ExternalTaskSensor`.
> Prefira o modo **`reschedule`** (libera o worker entre checagens) a `poke` para esperas longas.

### XComs: passar dados entre tasks
Tasks são isoladas; para **passar um valor pequeno** de uma para outra, usa-se **XCom**
(cross-communication). Na TaskFlow API, **o `return` de uma task vira XCom** e o argumento da
próxima o recebe — como no exemplo acima. XCom é para **metadados pequenos** (um caminho, uma
contagem, uma data), **não** para trafegar datasets — dados grandes vão para o storage
(Postgres/MinIO) e você passa só a referência.

### Dependências: fan-out e fan-in
- **Fan-out:** uma task dispara várias em paralelo (`a >> [b, c]`).
- **Fan-in:** várias convergem para uma (`[b, c] >> d`).
- **Trigger rules** controlam quando a de baixo roda (ex.: `all_success` padrão, `all_done`).

## 🔎 Exemplo
`esperar_arquivo` (FileSensor) → `carregar` (PythonOperator lê e insere no Postgres, retorna a
contagem via XCom) → `validar` (lê a contagem do XCom e falha se for 0) → `[notificar_ok,
notificar_erro]`. O sensor segura o pipeline até o arquivo chegar; o XCom leva a contagem adiante.

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do Airflow organiza o trabalho em **operators** (o que a task faz), destaca
**sensors** para esperar por eventos e **XComs** para passar pequenos valores entre tasks —
reforçando que dados grandes trafegam por armazenamento externo, não por XCom. — Apache Airflow,
docs oficiais.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A **TaskFlow API** (`@task`) virou o jeito recomendado de escrever DAGs Python: menos
boilerplate, dependências inferidas pela passagem de valores, e XCom implícito no `return` —
o que aproxima a DAG de código Python normal. — Apache Airflow, docs oficiais.
:::

## ⚠️ Erros comuns
- Passar **dados grandes por XCom** — ele é para metadados pequenos; datasets vão para storage.
- Sensor em modo **`poke`** para esperas longas — ocupa um worker; use `reschedule`.
- Esquecer que **tasks são isoladas** — variáveis de uma não existem na outra (use XCom/storage).
- Não declarar dependências (fan-in/out) corretamente — tasks rodam fora de ordem.
- Misturar muita lógica num operator gigante em vez de tasks pequenas e testáveis.

## 💼 O que o mercado espera
Saber escolher o operator certo, usar sensors para esperar eventos e passar dados com XComs
(sem abusar) é o dia a dia de quem escreve DAGs. A TaskFlow API é o padrão atual.

:::{admonition} ✨ Em resumo
:class: resumo
- **Operator** = tipo de task (Bash, Python/`@task`, SQL...). A **TaskFlow API** escreve tasks como funções.
- **Sensor** = task que espera uma condição (arquivo, partição), "pokando" até liberar (prefira `reschedule`).
- **XCom** = passar **valores pequenos** entre tasks (o `return` do `@task` vira XCom); dados grandes vão para storage.
- **Fan-out/fan-in** e **trigger rules** modelam dependências paralelas/convergentes.
:::

## 🧠 Quiz de recall
1. O que é um operator? Cite três.
   :::{dropdown} Resposta
   O molde de uma task por tipo de trabalho: BashOperator (shell), PythonOperator/@task (função Python), SQL operators (rodar SQL). Também providers para cloud/transferências.
   :::
2. Para que serve um sensor?
   :::{dropdown} Resposta
   Esperar uma condição antes de liberar o pipeline (arquivo pousar, partição existir), "pokando" periodicamente até ser verdadeira ou estourar timeout.
   :::
3. O que é XCom e qual seu limite?
   :::{dropdown} Resposta
   Cross-communication: passar pequenos valores entre tasks (o return do @task vira XCom). Não serve para dados grandes — esses vão para storage e você passa a referência.
   :::
4. Como a TaskFlow API infere dependências?
   :::{dropdown} Resposta
   Pela passagem de valores: `somar(extrair())` faz somar depender de extrair, com o retorno de extrair chegando como XCom.
   :::
5. Diferença entre fan-out e fan-in?
   :::{dropdown} Resposta
   Fan-out: uma task dispara várias em paralelo (`a >> [b, c]`). Fan-in: várias convergem para uma (`[b, c] >> d`).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você passa dados entre tasks no Airflow?"
  :::{dropdown} Resposta modelo
  Valores pequenos (uma contagem, um caminho, uma data) via XCom — na TaskFlow API, o `return` de uma task vira XCom e a próxima o recebe como argumento. Dados grandes não vão por XCom: gravo no Postgres/MinIO e passo só a referência (caminho/ID).
  :::
- **P:** "Quando usar um sensor e qual cuidado?"
  :::{dropdown} Resposta modelo
  Quando o pipeline depende de um evento externo (um arquivo chegar, uma partição existir). O cuidado é o modo: para esperas longas, uso `reschedule` para não segurar um worker ocupado durante todo o poke.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Airflow docs** — *Operators*, *Sensors*, *XComs*, *TaskFlow API*.
- **Astronomer — Airflow Fundamentals** (operators e TaskFlow na prática).

## 📚 Referências
- Apache Airflow — Documentação oficial (operators, sensors, XComs, TaskFlow API). <!-- @docs-airflow -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — orquestração e tasks. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
