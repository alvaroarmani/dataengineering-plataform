# Recursos — Módulo 08 (Ingestão e Integração)

Curadoria de fontes. Todas registradas em [`referencias.yaml`](../../referencias.yaml).

## Livros
- **Densmore, J. — Data Pipelines Pocket Reference** (2021): ingestão incremental, idempotência, padrões de pipeline.
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017), cap. 11: CDC, streams, mensageria.
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): ingestão no ciclo de vida do dado.

## APIs públicas para praticar ingestão
- **Banco Central (SGS)** — séries temporais (câmbio, juros): <https://dadosabertos.bcb.gov.br/>
- **IBGE** — <https://servicodados.ibge.gov.br/api/docs>
- **NYC TLC** (arquivos Parquet) — ver [`datasets/README.md`](../../datasets/README.md).

## Ferramentas na bancada
- Postgres (destino da ingestão) e MinIO (data lake) via `ambiente/docker-compose.yml`.
- Padrão de exercício real: `templates/template-exercicio-ferramenta/`.

---
**Revisado em:** 2026-08-29
