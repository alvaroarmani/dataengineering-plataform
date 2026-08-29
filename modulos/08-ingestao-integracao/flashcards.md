# Flashcards — Módulo 08

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** ETL vs ELT? / **R:** ETL transforma antes de carregar; ELT carrega cru e transforma dentro do warehouse (o que o dbt faz). A ingestão é o E(+L) dos dois.
- **P:** Full load vs incremental? / **R:** Full recarrega tudo; incremental traz só o que mudou desde a última carga, via marca d'água (ex.: updated_at) persistida.
- **P:** O que é uma marca d'água (high-water mark)? / **R:** O valor de referência (updated_at/id) da última carga; a próxima traz só `> marca` e salva a nova marca como estado.
- **P:** O que é idempotência na ingestão? / **R:** Rodar o passo 2x dá o mesmo resultado que 1x — essencial porque jobs são reexecutados. Consegue-se com upsert ou sobrescrita de partição.
- **P:** Como um upsert garante idempotência? / **R:** `INSERT ... ON CONFLICT (chave) DO UPDATE` insere se novo, atualiza se existe — reexecutar não duplica.
- **P:** O que é CDC e as duas abordagens? / **R:** Change Data Capture = capturar as mudanças da origem. Por query (updated_at; sem deletes) ou por log (lê o log de transações; pega tudo, ~tempo real).
- **P:** Por que o incremental por query não pega deletes? / **R:** Ele só vê linhas presentes com updated_at > marca; uma linha apagada some da origem sem aparecer. Precisa de CDC por log ou soft-delete.

---
**Revisado em:** 2026-08-29
