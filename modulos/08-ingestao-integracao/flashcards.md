# Flashcards — Módulo 08

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** ETL vs ELT? / **R:** ETL transforma antes de carregar; ELT carrega cru e transforma dentro do warehouse (o que o dbt faz). A ingestão é o E(+L) dos dois.
- **P:** Full load vs incremental? / **R:** Full recarrega tudo; incremental traz só o que mudou desde a última carga, via marca d'água (ex.: updated_at) persistida.
- **P:** O que é uma marca d'água (high-water mark)? / **R:** O valor de referência (updated_at/id) da última carga; a próxima traz só `> marca` e salva a nova marca como estado.
- **P:** O que é idempotência na ingestão? / **R:** Rodar o passo 2x dá o mesmo resultado que 1x — essencial porque jobs são reexecutados. Consegue-se com upsert ou sobrescrita de partição.
- **P:** Como um upsert garante idempotência? / **R:** `INSERT ... ON CONFLICT (chave) DO UPDATE` insere se novo, atualiza se existe — reexecutar não duplica.
- **P:** O que é CDC e as duas abordagens? / **R:** Change Data Capture = capturar as mudanças da origem. Por query (updated_at; sem deletes) ou por log (lê o log de transações; pega tudo, ~tempo real).
- **P:** Por que o incremental por query não pega deletes? / **R:** Ele só vê linhas presentes com updated_at > marca; uma linha apagada some da origem sem aparecer. Precisa de CDC por log ou soft-delete.
- **P:** O que é uma landing zone? / **R:** Onde o arquivo cru é pousado (MinIO/S3) antes de transformar — imutável, permite reprocessar; a camada raw/bronze com arquivos.
- **P:** Por que COPY em vez de INSERT para arquivos grandes? / **R:** COPY faz carga em bloco, ordens de grandeza mais rápida que INSERT linha a linha.
- **P:** Schema-on-write vs schema-on-read? / **R:** On-write define o schema ao gravar (banco relacional); on-read guarda cru e aplica schema na leitura (data lake, mais flexível).
- **P:** Como deduplicar um arquivo reentregue ficando com a versão mais nova? / **R:** ROW_NUMBER() OVER (PARTITION BY chave ORDER BY carregado_em DESC) e filtrar rn = 1.

---
**Revisado em:** 2026-08-29
