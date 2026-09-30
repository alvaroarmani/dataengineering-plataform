"""Testes do Exercício 05 (M2). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import simular  # noqa: E402


def test_dado_na_camada_morre_com_o_container():
    estado = simular(["pull postgres:16", "run db postgres:16", "escrever db /var/lib/pg/base",
                      "rm db"])
    assert estado == {"imagens": ["postgres:16"], "containers": [], "volumes": {}, "camadas": {}}


def test_dado_no_volume_sobrevive_e_e_reaproveitado():
    estado = simular([
        "pull postgres:16",
        "run db postgres:16 -v pgdata:/dados",
        "escrever db /dados/base",
        "escrever db /tmp/cache",            # fora de /dados: vai para a camada
        "rm db",
        "run db2 postgres:16 -v pgdata:/dados",
        "escrever db2 /dados/wal",
    ])
    assert estado["containers"] == ["db2"]
    assert estado["volumes"] == {"pgdata": ["/dados/base", "/dados/wal"]}   # o /tmp/cache sumiu
    assert estado["camadas"] == {"db2": []}


def test_dois_containers_da_mesma_imagem_tem_camadas_isoladas():
    estado = simular(["pull python:3.12", "run a python:3.12", "run b python:3.12",
                      "escrever a /app/saida.csv"])
    assert estado["camadas"] == {"a": ["/app/saida.csv"], "b": []}
    assert estado["containers"] == ["a", "b"] and estado["imagens"] == ["python:3.12"]


def test_container_sem_volume_nao_grava_em_volume():
    estado = simular(["pull alpine", "run x alpine", "escrever x /dados/arquivo"])
    assert estado["volumes"] == {} and estado["camadas"] == {"x": ["/dados/arquivo"]}


def test_imagem_so_sai_depois_do_container():
    with pytest.raises(ValueError):
        simular(["pull alpine", "run x alpine", "rmi alpine"])
    estado = simular(["pull alpine", "run x alpine", "rm x", "rmi alpine"])
    assert estado["imagens"] == [] and estado["containers"] == []


def test_volume_em_uso_nao_pode_ser_removido():
    with pytest.raises(ValueError):
        simular(["pull alpine", "run x alpine -v v1:/dados", "volume rm v1"])
    estado = simular(["pull alpine", "run x alpine -v v1:/dados", "rm x", "volume rm v1"])
    assert estado["volumes"] == {}


@pytest.mark.parametrize("comandos", [
    ["run x alpine"],                                     # imagem não baixada
    ["pull alpine", "run x alpine", "run x alpine"],      # nome de container repetido
    ["pull alpine", "escrever fantasma /a"],              # container inexistente
    ["pull alpine", "rm fantasma"],
    ["pull alpine", "docker-compose up"],                 # comando desconhecido
])
def test_comandos_invalidos(comandos):
    with pytest.raises(ValueError):
        simular(comandos)
