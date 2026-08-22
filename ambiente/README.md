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

## Observações
- **Módulos avançados** (Airflow no M09, Spark no M11, dbt no M07) trazem *overrides* ou compose próprios que estendem esta base — descritos em cada módulo.
- Nunca versione o `.env` (segredos). Ver o ADR 0004 em `docs/decisoes/0004-local-first-bigquery.md` e a [Infraestrutura do PPC](../ppc/infraestrutura-e-ambiente.md).

---
**Revisado em:** 2026-08-20
