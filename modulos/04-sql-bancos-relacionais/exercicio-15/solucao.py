"""Exercício 15 (M4) — SQL em dados REAIS de táxi de NY (mini-caso).

Os testes carregam no DuckDB (datasets/amostras/):
  corridas(viagem_id, VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count,
           trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, tip_amount, total_amount)
  zonas(LocationID, Borough, Zone, service_zone)
Preencha as quatro queries e rode `pytest -q`. Os testes rodam cada query em DUAS bases (a amostra
inteira e só as corridas do fornecedor 2) — resultado "decorado" não passa.
"""

# A) Top 5 zonas de EMBARQUE por nº de corridas com total_amount > 0.
#    Colunas (zona, borough, corridas, receita = SUM(total_amount) com 2 casas),
#    ordenado por corridas DESC, zona.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) Ticket médio por HORA do embarque (corridas com total_amount > 0), só horas com >= 100 corridas.
#    Colunas (hora, corridas, ticket_medio = AVG(total_amount) com 2 casas),
#    ordenado por ticket_medio DESC, hora.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""

# C) Para cada borough, a zona de embarque de MAIOR receita (total_amount > 0).
#    Ignore os boroughs 'Unknown' e 'N/A'. Empate: zona em ordem alfabética.
#    Colunas (borough, zona, receita com 2 casas), ordenado por borough.
CONSULTA_C = """
-- SEU CÓDIGO AQUI
"""

# D) Diagnóstico de qualidade: classifique CADA corrida numa única situação, nesta prioridade:
#      'tarifa_nao_positiva' (total_amount <= 0) > 'desembarque_antes' (dropoff < pickup)
#      > 'passageiros_nulo' (passenger_count nulo) > 'ok'.
#    Colunas (situacao, corridas, pct = % do total com 2 casas), ordenado por corridas DESC, situacao.
CONSULTA_D = """
-- SEU CÓDIGO AQUI
"""
