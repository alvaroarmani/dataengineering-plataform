"""Gera as AMOSTRAS REAIS versionadas em datasets/amostras/ a partir dos dados completos.

Os exercícios e labs usam estas amostras (pequenas, commitadas) para serem determinísticos e
rodarem em qualquer lugar; os dados completos ficam em datasets/data/ (fora do Git).

Pré-requisito (baixa os completos):
    python datasets/baixar.py nyc_taxi nyc_taxi_zonas bcb_ptax   # corridas (~48 MB), zonas, PTAX

Uso:
    python datasets/gerar_amostras.py

Amostra NYC = 2.500 corridas pseudoaleatórias (ordem por md5 do id — reproduzível) + até 20 registros REAIS de cada tipo de
anomalia encontrada no mês (tarifa negativa, passageiros nulo/zero, desembarque antes do embarque,
distância absurda, fora do mês). As anomalias NÃO são inventadas: são linhas reais do arquivo da TLC.
"""
from pathlib import Path
import shutil

import duckdb

RAIZ = Path(__file__).resolve().parent
DATA = RAIZ / "data"
AMOSTRAS = RAIZ / "amostras"
PARQUET = DATA / "nyc_taxi" / "yellow_tripdata_2024-01.parquet"
ZONAS = DATA / "nyc_taxi" / "taxi_zone_lookup.csv"
PTAX = DATA / "bcb" / "ptax_2024_01.json"

COLS = ("viagem_id, VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, "
        "trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, tip_amount, total_amount")

# todas as colunas do parquet: ordenação total, sem empate que dependa da ordem de leitura
ORDEM_TOTAL = ("tpep_pickup_datetime, tpep_dropoff_datetime, VendorID, PULocationID, DOLocationID, "
               "passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, payment_type, fare_amount, "
               "extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, "
               "congestion_surcharge, Airport_fee")

ANOMALIAS = {
    "tarifa_negativa": "fare_amount < 0",
    "passageiros_nulo": "passenger_count IS NULL",
    "passageiros_zero": "passenger_count = 0",
    "desembarque_antes": "tpep_dropoff_datetime < tpep_pickup_datetime",
    "distancia_absurda": "trip_distance > 100",
    "fora_do_mes": "tpep_pickup_datetime < '2024-01-01' OR tpep_pickup_datetime >= '2024-02-01'",
}


def main() -> None:
    AMOSTRAS.mkdir(exist_ok=True)
    con = duckdb.connect()
    # REPRODUTÍVEL por construção (os testes dependem disso):
    # - viagem_id: ROW_NUMBER ordenado por TODAS as colunas do registro (sem empate ambíguo);
    # - amostra: as 2.500 com menor md5(viagem_id) — determinístico entre execuções, threads e
    #   versões do DuckDB (ao contrário de USING SAMPLE ... REPEATABLE, que varia com paralelismo).
    con.execute(f"""
        CREATE TABLE base AS
        SELECT ROW_NUMBER() OVER (ORDER BY {ORDEM_TOTAL}) AS viagem_id, *
        FROM '{PARQUET.as_posix()}'
    """)
    partes = [f"SELECT {COLS} FROM (SELECT * FROM base ORDER BY md5(viagem_id::VARCHAR) LIMIT 2500)"]
    for cond in ANOMALIAS.values():
        partes.append(f"SELECT {COLS} FROM (SELECT * FROM base WHERE {cond} ORDER BY viagem_id LIMIT 20)")
    uniao = " UNION ".join(f"({p})" for p in partes)
    saida = AMOSTRAS / "nyc_taxi_2024_01_amostra.csv"
    con.execute(f"COPY (SELECT * FROM ({uniao}) ORDER BY viagem_id) TO '{saida.as_posix()}' (HEADER)")
    n = con.execute(f"SELECT count(*) FROM '{saida.as_posix()}'").fetchone()[0]
    print(f"[ok] {saida.name}: {n} corridas reais")

    shutil.copy(ZONAS, AMOSTRAS / "taxi_zone_lookup.csv")
    print("[ok] taxi_zone_lookup.csv (dimensão real de zonas da TLC)")
    shutil.copy(PTAX, AMOSTRAS / "ptax_2024_01.json")
    print("[ok] ptax_2024_01.json (resposta real da API PTAX do Banco Central, jan/2024)")


if __name__ == "__main__":
    main()
