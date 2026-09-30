import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ingerir_com_cursor, pagina_cursor, pagina_offset  # noqa: E402


def _base():
    return [{"id": i} for i in range(10, 70, 10)]          # ids 10..60


def test_offset_basico():
    assert pagina_offset([1, 2, 3, 4, 5], 1, 2) == [1, 2]
    assert pagina_offset([1, 2, 3, 4, 5], 3, 2) == [5]
    assert pagina_offset([1, 2], 5, 2) == []
    with pytest.raises(ValueError):
        pagina_offset([1], 0, 2)


def test_offset_duplica_quando_chega_item_novo():
    base = sorted(_base(), key=lambda x: -x["id"])         # a API lista do mais novo para o mais antigo
    p1 = pagina_offset(base, 1, 3)                          # 60, 50, 40
    base.insert(0, {"id": 70})                              # chegou um novo durante a ingestão
    p2 = pagina_offset(base, 2, 3)                          # 40 de novo!
    ids = [x["id"] for x in p1 + p2]
    assert ids == [60, 50, 40, 40, 30, 20]


def test_cursor_nao_duplica():
    base = _base()
    p1, c1 = pagina_cursor(base, None, 3)
    base.append({"id": 5})                                  # id menor que o cursor: não bagunça
    base.append({"id": 65})                                 # id novo depois do cursor: entra na próxima
    p2, c2 = pagina_cursor(base, c1, 3)
    assert [x["id"] for x in p1] == [10, 20, 30] and c1 == 30
    assert [x["id"] for x in p2] == [40, 50, 60] and c2 == 60
    p3, c3 = pagina_cursor(base, c2, 3)
    assert [x["id"] for x in p3] == [65] and c3 is None


def test_ingerir_tudo_e_cursor_travado():
    base = _base()
    assert ingerir_com_cursor(lambda c, t: pagina_cursor(base, c, t), 4) == [10, 20, 30, 40, 50, 60]
    with pytest.raises(ValueError):
        ingerir_com_cursor(lambda c, t: ([{"id": 1}], 1), 2)
