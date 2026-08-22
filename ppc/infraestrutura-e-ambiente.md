# Infraestrutura e Ambiente

O curso é **local-first**: quase tudo roda na sua máquina via Docker, sem custo. A nuvem
entra pontualmente com o **BigQuery** (*free tier*).

## Requisitos de máquina

- **SO:** Windows 10/11, macOS ou Linux. No Windows, **WSL2** é fortemente recomendado.
- **RAM:** 8 GB mínimo; **16 GB** recomendado (Spark/Airflow são famintos).
- **Disco:** ~20 GB livres para imagens Docker e datasets.
- **Docker Desktop** instalado e funcional.

## Duas formas de rodar código

1. **Navegador (JupyterLite):** para fundamentos de Python/pandas/SQL-DuckDB. Zero instalação — basta o botão na página do notebook.
2. **Bancada Docker (ambiente principal):** para engenharia real (Postgres, Airflow, dbt, Spark, MinIO). Ver [`ambiente/README.md`](../ambiente/README.md).

Cada notebook declara no topo **onde deve rodar**.

## Contas e serviços externos

| Serviço | Uso | Custo |
|---|---|---|
| **Google Cloud / BigQuery** | DW cloud (M06, M07, TCC) | *Free tier* (suficiente para o curso) |
| **GitHub** | Portfólio, versionamento, GitHub Pages, CI | Gratuito |

## Segurança e boas práticas

- **Nunca** versione segredos: use `.env` (ver `ambiente/.env.example`) e mantenha-o no `.gitignore`.
- Credenciais do Google Cloud como *service account* com escopo mínimo.
- Datasets grandes ficam **fora** do git (ver [`datasets/README.md`](../datasets/README.md)).

## Publicação da plataforma

O próprio curso (este site) é publicado via **GitHub Pages** pelo workflow
`.github/workflows/deploy.yml` a cada push na `main`.

---
**Revisado em:** 2026-08-20
