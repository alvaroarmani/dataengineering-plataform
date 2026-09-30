import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resolver_entidades  # noqa: E402

REGISTROS = ["CRM-17", "ECOM-903", "SAC-55", "CRM-02", "ECOM-111", "SAC-90", "CRM-40"]
PARES = [("CRM-17", "ECOM-903"),      # mesmo e-mail
         ("ECOM-903", "SAC-55"),      # mesmo telefone
         ("CRM-02", "ECOM-111"),      # mesmo CPF
         ("SAC-90", "ECOM-111")]      # mesmo telefone


def test_transitividade_forma_os_grupos():
    assert resolver_entidades(REGISTROS, PARES) == {
        "CRM-02": "CRM-02", "CRM-17": "CRM-17", "CRM-40": "CRM-40",
        "ECOM-111": "CRM-02", "ECOM-903": "CRM-17", "SAC-55": "CRM-17", "SAC-90": "CRM-02"}


def test_numero_de_clientes_unicos():
    canon = resolver_entidades(REGISTROS, PARES)
    assert len(set(canon.values())) == 3          # 7 registros, 3 pessoas


def test_um_par_a_mais_funde_dois_grupos():
    canon = resolver_entidades(REGISTROS, PARES + [("SAC-55", "SAC-90")])
    assert set(canon.values()) == {"CRM-02", "CRM-40"}


def test_sem_pares_e_par_repetido():
    assert resolver_entidades(["b", "a"], []) == {"a": "a", "b": "b"}
    assert resolver_entidades(["b", "a"], [("a", "b"), ("b", "a")]) == {"a": "a", "b": "a"}


def test_par_com_registro_desconhecido():
    with pytest.raises(ValueError):
        resolver_entidades(["a"], [("a", "z")])
