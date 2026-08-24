# Template de exercício — TRACK REAL (ferramenta na bancada)

Use este layout quando o exercício exigir uma **ferramenta real** (Postgres, dbt, Airflow,
Spark) rodando na bancada Docker — diferente do track browser (DuckDB/`verificar()`).

```
exercicio-NN/
├── enunciado.md        # tarefa + como subir a bancada + como rodar o pytest
├── solucao.sql         # (ou solucao.py / modelo dbt / dag.py) — o que o aluno edita
├── conftest.py         # fixture `pg` (conexão Postgres via env; skip se indisponível)
└── tests/test_*.py     # cria fixtures em tabela temporária, executa, confere (rollback ao fim)
```

Convenções:
- O grader conecta no Postgres via variáveis do `.env` (`POSTGRES_HOST`, etc.).
- Fora da bancada, os testes fazem **skip** (não falham) — o track browser continua válido para fundamentos.
- Para **dbt**: em vez de `solucao.sql`, o aluno completa modelos em `projeto-dbt/models/`, e o
  grader roda `dbt build && dbt test` + um `pytest` conferindo as tabelas resultantes.
- Para **Airflow**: o aluno escreve um DAG em `dags/`, e o grader roda `airflow dags test <dag> <data>`
  + `pytest` de estrutura (sem erro de import, dependências, idempotência).
