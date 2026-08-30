-- Dedup de reentrega: mantenha a versão MAIS RECENTE por id.
-- Tabela (o teste cria): raw_eventos(id INT, valor INT, carregado_em DATE) — com duplicatas por id.
-- Devolva (id, valor) da versão mais nova de cada id, ordenado por id.
-- Dica: ROW_NUMBER() OVER (PARTITION BY id ORDER BY carregado_em DESC) e filtre rn = 1.

-- SEU CÓDIGO AQUI
