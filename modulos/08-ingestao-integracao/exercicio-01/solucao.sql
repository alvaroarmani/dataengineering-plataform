-- Ingestão idempotente: faça o UPSERT de `batch` para `clientes`.
-- Insira novos e atualize existentes por `id`, de forma que rodar 2x NÃO duplique.
-- Tabelas (o teste cria):
--   clientes(id INT PRIMARY KEY, nome TEXT)   -- destino, já com dados
--   batch(id INT, nome TEXT)                  -- lote incremental que chegou
--
-- Dica: INSERT INTO clientes (id, nome) SELECT ... FROM batch ON CONFLICT (id) DO UPDATE ...

-- SEU CÓDIGO AQUI
