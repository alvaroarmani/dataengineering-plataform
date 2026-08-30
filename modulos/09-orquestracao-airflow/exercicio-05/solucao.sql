-- Carga IDEMPOTENTE de um dia (overwrite da partição), como faria a task de uma DAG @daily.
-- A execução é "dona" do dia 2026-08-10: reprocessá-la deve SUBSTITUIR, não acumular.
-- Tabelas (o teste cria):
--   fato(data DATE, id INT, valor INT)   -- já tem uma linha de OUTRO dia (2026-08-09), que deve permanecer
--   batch(id INT, valor INT)             -- os dados do dia 2026-08-10 a carregar
--
-- Escreva DUAS instruções: apague as linhas do dia e insira as do batch com data = 2026-08-10.
-- Dica: DELETE ... WHERE data = DATE '2026-08-10';  INSERT INTO fato SELECT DATE '2026-08-10', ... FROM batch;

-- SEU CÓDIGO AQUI
