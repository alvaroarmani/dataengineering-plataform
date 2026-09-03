# Bancada Docker (ambiente principal)

Esta é a sua **bancada de trabalho** — onde a engenharia de dados de verdade acontece.
Notebooks de fundamentos rodam no navegador (JupyterLite); tudo que envolve Postgres,
MinIO, dbt, Airflow ou Spark roda **aqui**.

## Pré-requisitos
- **Docker Desktop** instalado e rodando.
- Windows: **WSL2** habilitado (recomendado).

## Subir a bancada

```bash
cd ambiente
cp .env.example .env      # ajuste as senhas se quiser
docker compose up -d
```

Serviços:

| Serviço | URL | Credenciais |
|---|---|---|
| JupyterLab | http://localhost:8888 | token = `JUPYTER_TOKEN` do `.env` |
| Postgres | localhost:5432 | user/senha/db do `.env` |
| MinIO (console) | http://localhost:9001 | user/senha do `.env` |

O repositório do curso é montado dentro do Jupyter em `/home/jovyan/curso`.

## Derrubar

```bash
docker compose down          # mantém os dados (volumes)
docker compose down -v       # apaga também os dados
```

## Verificar rapidamente

```bash
docker compose ps            # serviços de pé?
docker compose logs -f jupyter
```

## Validar a bancada

```bash
bash ambiente/validar-bancada.sh
```
Smoke test dos serviços (postgres/minio/jupyter) e das ferramentas (dbt↔Postgres, Airflow),
sem depender de soluções de exercícios. Rode com o **engine estável**.

### Status da validação (2026-09-03) — bancada validada ponta a ponta
Executado contra o engine ao vivo:
- ✅ **Base**: `postgres`, `minio`, `jupyter` sobem com `docker compose up -d`.
- ✅ **Graders Postgres reais** (com `psycopg2-binary`): M08 ex‑01/ex‑03, M09 ex‑05 → **PASS**.
- ✅ **dbt (M07)**: `dbt build` + `pytest` em ex‑01/03/05 → **PASS** (6/6, 8/8, 10/10). *Corrigido um
  bug real: seeds eram lidos como `source()` — trocado para `ref()` (ver histórico do git).*
- ✅ **Airflow (M09)**: `airflow dags test` em `pipeline_exemplo` e `pipeline_taskflow` → **SUCCESS**.
- ✅ **Spark (M11)**: job de exemplo via `spark-submit` → **OK**. *Corrigido: imagem `bitnami/spark:3.5.3`
  não existe mais → trocada por `apache/spark:3.5.3`.*
- ⏳ **BigQuery (M06)**: requer projeto GCP + credenciais do aluno (não validável sem a conta dele).

## Solução de problemas

**Docker Desktop cai logo após subir** (engine some do `docker info`), com erro do tipo
`initializing Inference manager: ... dockerInference: The file cannot be accessed by the system`:
é o **Docker Model Runner / Inference** falhando ao criar o socket e derrubando o engine. Correção:
1. **Settings → AI (ou Beta features) → Docker Model Runner → desligar** e **Apply & Restart**; ou
2. `Troubleshoot → Clean / Purge data` (ou reinstalar/reparar o Docker Desktop) se persistir.

Com o engine estável, rode `bash ambiente/validar-bancada.sh` e depois puxe as imagens dos módulos:
`docker pull ghcr.io/dbt-labs/dbt-postgres:1.8.2` e `docker pull apache/airflow:2.10.3-python3.12`.

## Observações
- **Módulos avançados** (Airflow no M09, Spark no M11, dbt no M07) trazem *overrides* ou compose próprios que estendem esta base — descritos em cada módulo.
- Os graders reais fazem *skip* limpo sem `psycopg2` ou sem Postgres; instale `psycopg2-binary` (já no `requirements.txt`) e suba a bancada para eles **rodarem**.
- Nunca versione o `.env` (segredos). Ver o ADR 0004 em `docs/decisoes/0004-local-first-bigquery.md` e a [Infraestrutura do PPC](../ppc/infraestrutura-e-ambiente.md).

---
**Revisado em:** 2026-08-30
