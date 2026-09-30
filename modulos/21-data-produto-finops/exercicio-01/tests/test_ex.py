import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import MIB, TIB, bytes_cobrados, custo_mensal  # noqa: E402


def test_arredonda_e_aplica_minimo_por_tabela():
    assert bytes_cobrados([1]) == 10 * MIB                     # 1 byte paga 10 MiB
    assert bytes_cobrados([10 * MIB + 1]) == 11 * MIB          # arredonda para cima
    assert bytes_cobrados([0, 5 * MIB]) == 20 * MIB            # duas tabelas, dois mínimos
    assert bytes_cobrados([]) == 0


def test_consulta_grande_com_cota():
    consultas = [[TIB // 2]] * 3                                # 1,5 TiB no mês
    assert custo_mensal(consultas, 5.0) == 2.5                  # 0,5 TiB acima da cota
    assert custo_mensal(consultas, 5.0, gratis_tib=2.0) == 0.0


def test_milhares_de_consultas_minusculas():
    # um painel que atualiza a cada minuto, lendo 3 tabelas pequenas: 43.200 consultas/mês
    consultas = [[1_000, 2_000, 500]] * 43_200
    assert bytes_cobrados(consultas[0]) == 30 * MIB
    assert custo_mensal(consultas, 5.0, gratis_tib=0) == 6.18   # ~1,24 TiB por ler ~150 MB de verdade


def test_bytes_negativos():
    with pytest.raises(ValueError):
        bytes_cobrados([-1])
