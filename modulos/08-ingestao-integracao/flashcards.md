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
- **P:** Dois estilos de paginação de API? / **R:** Offset/limit (pede por posição; frágil se muda) e cursor/token (segue um next até vir vazio; robusto).
- **P:** O que é HTTP 429 e como reagir? / **R:** Too Many Requests (estourou o rate limit). Reaja com retry e backoff exponencial (espera crescente + jitter).
- **P:** Onde guardar a chave de uma API? / **R:** Em variável de ambiente — nunca no código/commit (é segredo).
- **P:** Como fazer ingestão incremental de uma API? / **R:** Filtro de data (ex.: ?since=) + marca d'água: guarda a última data e pede só o que veio depois.
- **P:** Por que sempre usar timeout numa requisição? / **R:** Para não pendurar o pipeline se a API não responder — falha rápido e você trata/reintenta.
- **P:** Parquet vs CSV? / **R:** Parquet é colunar, binário, comprimido e com schema (ótimo p/ análise/DW); CSV é linha, texto, sem tipos — só p/ interop, ruim p/ volume.
- **P:** Por que Avro é comum em streaming? / **R:** Linha, binário, guarda o schema junto e suporta evolução de schema — encaixa em mensageria (Kafka).
- **P:** O que é evolução de schema? / **R:** Mudar o schema no tempo (ex.: campo novo opcional) sem quebrar quem lê o dado antigo.
- **P:** Batch vs streaming? / **R:** Batch processa lotes periódicos (simples/barato); streaming processa eventos contínuos com baixa latência (fraude, dashboards ao vivo).
- **P:** O que é o Kafka em uma frase? / **R:** Um log distribuído de mensagens: produtores escrevem em tópicos (partições), consumidores leem por offset e committam até onde leram.

---
**Revisado em:** 2026-08-29
