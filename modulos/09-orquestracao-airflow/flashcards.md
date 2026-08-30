# Flashcards — Módulo 09

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Cron vs orquestrador (Airflow)? / **R:** Cron dispara um script num horário; o orquestrador gerencia dependências, retries, backfill, paralelismo, monitoramento e agendamento do pipeline inteiro.
- **P:** O que é uma DAG e por que "acíclica"? / **R:** Directed Acyclic Graph: tasks (nós) + dependências dirigidas (arestas), sem ciclos — um ciclo faria o pipeline nunca terminar.
- **P:** Como declarar dependência entre tasks no Airflow? / **R:** Com `>>`: `a >> b` faz `b` rodar depois de `a`.
- **P:** Componentes do Airflow? / **R:** Scheduler (decide o que rodar), executor/workers (executam), metadata DB (estado), webserver/UI (visualização e disparo).
- **P:** O que fazem schedule e catchup? / **R:** schedule define a periodicidade (ex.: @daily); catchup=False evita rodar todas as execuções passadas ao ligar a DAG.
- **P:** Em que ordem o Airflow roda as tasks? / **R:** Ordem topológica (dependências primeiro), paralelizando o que é independente — algoritmo de Kahn.
- **P:** Onde NÃO colocar lógica pesada? / **R:** No topo do arquivo da DAG (é lido a cada scan do scheduler); a lógica vai dentro das tasks.
- **P:** O que é um operator? / **R:** O molde de uma task por tipo: BashOperator (shell), PythonOperator/@task (função), SQL operators. TaskFlow API escreve tasks como funções.
- **P:** Para que serve um sensor? / **R:** Esperar uma condição (arquivo pousar, partição existir), pokando até liberar ou estourar timeout; para esperas longas use reschedule.
- **P:** O que é XCom e qual o limite? / **R:** Passar valores pequenos entre tasks (o return do @task vira XCom). Dados grandes vão para storage — passe só a referência.
- **P:** Como a TaskFlow API infere dependências? / **R:** Pela passagem de valores: somar(extrair()) faz somar depender de extrair, com o retorno vindo por XCom.
- **P:** Fan-out vs fan-in? / **R:** Fan-out: uma task dispara várias em paralelo (a >> [b,c]); fan-in: várias convergem para uma ([b,c] >> d).

---
**Revisado em:** 2026-08-29
