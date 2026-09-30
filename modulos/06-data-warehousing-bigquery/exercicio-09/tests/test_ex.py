import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import bytes_varridos, economia_pct  # noqa: E402

GB = 10 ** 9
# 3 anos de eventos particionados por dia (1.095 partições)
EVENTOS = {"particoes": 1095, "coluna_particao": "data_evento",
           "bytes_por_coluna": {"data_evento": 20 * GB, "usuario": 150 * GB, "tipo": 40 * GB,
                                "valor": 60 * GB, "payload_json": 2_500 * GB}}


def test_select_estrela_sem_filtro():
    assert bytes_varridos(EVENTOS, {"colunas": ["*"], "filtro_particao": None}) == 2_770 * GB


def test_poda_de_coluna_e_de_particao():
    c = {"colunas": ["tipo", "valor"], "filtro_particao": {"coluna": "data_evento", "particoes": 7}}
    assert bytes_varridos(EVENTOS, c) == 639_269_406
    assert economia_pct(EVENTOS, c) == 100.0


def test_so_poda_de_coluna():
    c = {"colunas": ["tipo", "valor"], "filtro_particao": None}
    assert bytes_varridos(EVENTOS, c) == 100 * GB
    assert economia_pct(EVENTOS, c) == 96.4


def test_filtro_em_outra_coluna_nao_poda():
    c = {"colunas": ["tipo", "valor"], "filtro_particao": {"coluna": "data_ingestao", "particoes": 7}}
    assert bytes_varridos(EVENTOS, c) == 100 * GB


def test_star_com_filtro_de_um_dia():
    c = {"colunas": ["*"], "filtro_particao": {"coluna": "data_evento", "particoes": 1}}
    assert bytes_varridos(EVENTOS, c) == 2_529_680_365


def test_invalidos():
    with pytest.raises(ValueError):
        bytes_varridos(EVENTOS, {"colunas": ["preco"], "filtro_particao": None})
    with pytest.raises(ValueError):
        bytes_varridos(EVENTOS, {"colunas": ["tipo"], "filtro_particao": {"coluna": "data_evento", "particoes": 0}})
