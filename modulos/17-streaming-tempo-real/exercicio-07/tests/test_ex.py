"""Grader do Exercício 07 (M17) — produz/consome de um Kafka REAL (bancada) e valida a
garantia de ordem por partição (mesma chave -> mesma partição).

Fora da bancada (broker indisponível), faz *skip*. Com o profile kafka de pé, executa de
verdade — se a solução keyar errado (ou usar chave constante), FALHA.
"""
import sys
import time
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from solucao import preparar_mensagens  # noqa: E402

BROKER = "localhost:9092"
EVENTOS = [
    {"cliente_id": 42, "acao": "login"},
    {"cliente_id": 7, "acao": "view"},
    {"cliente_id": 42, "acao": "buy"},
    {"cliente_id": 7, "acao": "logout"},
    {"cliente_id": 99, "acao": "login"},
    {"cliente_id": 42, "acao": "logout"},
]


def _broker_ok() -> bool:
    try:
        from kafka.admin import KafkaAdminClient
        KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=4000).close()
        return True
    except Exception:
        return False


def test_particionamento_por_cliente_no_kafka_real():
    if _broker_ok() is False:
        pytest.skip("Kafka indisponível — suba: cd ambiente && docker compose --profile kafka up -d")
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.admin import KafkaAdminClient, NewTopic

    topico = f"ex07_{int(time.time() * 1000)}"
    admin = KafkaAdminClient(bootstrap_servers=BROKER)
    admin.create_topics([NewTopic(topico, num_partitions=3, replication_factor=1)])
    time.sleep(1)

    msgs = preparar_mensagens(EVENTOS)
    assert isinstance(msgs, list) and all(len(m) == 2 for m in msgs), \
        "retorne uma lista de tuplas (chave, valor)"

    prod = KafkaProducer(bootstrap_servers=BROKER, key_serializer=str.encode, value_serializer=str.encode)
    for chave, valor in msgs:
        prod.send(topico, key=str(chave), value=str(valor))
    prod.flush()

    cons = KafkaConsumer(topico, bootstrap_servers=BROKER, group_id=f"g_{topico}",
                         auto_offset_reset="earliest", consumer_timeout_ms=8000)
    recebidas = [(m.partition, m.key.decode(), m.value.decode()) for m in cons]
    cons.close()

    assert len(recebidas) == len(EVENTOS), "todas as mensagens devem chegar (sem perda)"

    parts = {}
    for particao, chave, _ in recebidas:
        parts.setdefault(chave, set()).add(particao)
    for chave, ps in parts.items():
        assert len(ps) == 1, (
            f"eventos do cliente {chave} espalharam em {sorted(ps)} — a MESMA chave deve ir "
            "sempre para a MESMA partição (ordem por cliente)"
        )
    assert len({p for p, _, _ in recebidas}) >= 2, (
        "use a chave por cliente: clientes diferentes devem se espalhar entre partições "
        "(chave constante põe tudo numa partição só)"
    )
