#!/usr/bin/env bash
# Smoke test da bancada Docker — roda com o engine ESTÁVEL (Docker Desktop rodando).
# Verifica conectividade dos serviços base e das ferramentas (dbt/airflow), sem depender
# de soluções de exercícios. Uso:  bash ambiente/validar-bancada.sh
set -uo pipefail
cd "$(dirname "$0")"

ok=0; fail=0
check() { if eval "$2" >/dev/null 2>&1; then echo "  OK   $1"; ok=$((ok+1)); else echo "  FALHA $1"; fail=$((fail+1)); fi; }

echo "== 0. Engine =="
if ! docker info >/dev/null 2>&1; then
  echo "  FALHA docker daemon indisponível — abra o Docker Desktop e tente de novo."
  echo "  (Se o Docker cai ao subir com erro do 'Inference manager', desative o Docker"
  echo "   Model Runner: Settings > AI/Beta features > Docker Model Runner > OFF, e reinicie.)"
  exit 1
fi
echo "  OK   engine no ar"

echo "== 1. Base (postgres/minio/jupyter) =="
[ -f .env ] || cp .env.example .env
docker compose up -d >/dev/null 2>&1
# espera o Postgres aceitar conexões (até ~60s)
for i in $(seq 1 12); do docker compose exec -T postgres pg_isready -U "${POSTGRES_USER:-curso}" >/dev/null 2>&1 && break; sleep 5; done
check "postgres aceita conexões" "docker compose exec -T postgres pg_isready -U ${POSTGRES_USER:-curso}"
check "postgres SELECT 1"        "docker compose exec -T postgres psql -U ${POSTGRES_USER:-curso} -d ${POSTGRES_DB:-curso} -c 'SELECT 1'"
check "minio saudável"           "curl -sf http://localhost:9000/minio/health/live"
check "jupyter respondendo"      "curl -sf -o /dev/null http://localhost:8888"

echo "== 2. dbt <-> Postgres (profile dbt) =="
if docker image ls ghcr.io/dbt-labs/dbt-postgres:1.8.2 -q | grep -q .; then
  check "dbt debug conecta no Postgres" \
    "docker compose --profile dbt run --rm dbt debug \
       --project-dir modulos/07-transformacao-dbt/exercicio-01/projeto_dbt \
       --profiles-dir modulos/07-transformacao-dbt/exercicio-01/projeto_dbt"
else
  echo "  PULAR imagem dbt ausente — rode: docker pull ghcr.io/dbt-labs/dbt-postgres:1.8.2"
fi

echo "== 3. Airflow (profile airflow) =="
if docker image ls apache/airflow:2.10.3-python3.12 -q | grep -q .; then
  docker compose --profile airflow up -d >/dev/null 2>&1
  sleep 20
  check "airflow lista as DAGs do M09" "docker compose --profile airflow exec -T airflow airflow dags list"
else
  echo "  PULAR imagem airflow ausente — rode: docker pull apache/airflow:2.10.3-python3.12"
fi

echo
echo "== Resumo: ${ok} OK, ${fail} falha(s) =="
[ "$fail" -eq 0 ] && echo "Bancada saudável." || echo "Veja as falhas acima."
exit "$fail"
