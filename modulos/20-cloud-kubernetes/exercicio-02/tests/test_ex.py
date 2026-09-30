import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import planejar_replicas  # noqa: E402


def test_utilizacao_alvo_muda_a_conta():
    assert planejar_replicas(1000, 100, utilizacao_alvo=1.0) == {"por_zona": 10, "total": 10, "utilizacao_normal": 1.0}
    assert planejar_replicas(1000, 100) == {"por_zona": 15, "total": 15, "utilizacao_normal": 0.67}


def test_espalhar_em_zonas_arredonda_por_zona():
    assert planejar_replicas(1000, 100, zonas=3) == {"por_zona": 5, "total": 15, "utilizacao_normal": 0.67}
    assert planejar_replicas(1000, 100, zonas=4) == {"por_zona": 4, "total": 16, "utilizacao_normal": 0.62}


def test_sobreviver_a_perda_de_uma_zona():
    r = planejar_replicas(1000, 100, zonas=3, tolerar_perda_zona=True)
    assert r == {"por_zona": 8, "total": 24, "utilizacao_normal": 0.42}
    r2 = planejar_replicas(1000, 100, zonas=2, tolerar_perda_zona=True)
    assert r2["total"] == 30                      # com 2 zonas, cada uma precisa aguentar tudo


def test_carga_minima():
    assert planejar_replicas(1, 100)["total"] == 1


@pytest.mark.parametrize("kw", [dict(utilizacao_alvo=0), dict(utilizacao_alvo=1.2), dict(capacidade_pod=0),
                                dict(zonas=1, tolerar_perda_zona=True)])
def test_invalidos(kw):
    base = dict(carga_pico=100, capacidade_pod=10)
    base.update(kw)
    with pytest.raises(ValueError):
        planejar_replicas(**base)
