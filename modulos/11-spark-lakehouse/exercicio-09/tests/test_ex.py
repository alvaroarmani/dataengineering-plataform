"""Grader do Exercício 09 (M11) — roda a solução no SPARK REAL (bancada) e confere o resultado.

Fora da bancada (sem Docker), faz *skip*. Com o Docker de pé, executa
`spark-submit` no profile spark e valida a saída — se a solução estiver incompleta, FALHA.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[4]          # raiz do repositório
AMB = RAIZ / "ambiente"
RUNNER = "/work/modulos/11-spark-lakehouse/exercicio-09/runner.py"
ESPERADO = [["A", 32, 2], ["B", 21, 2], ["C", 20, 1]]


def _docker_ok() -> bool:
    if shutil.which("docker") is None:
        return False
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


def test_resumo_por_categoria_no_spark():
    if not _docker_ok():
        pytest.skip("Docker indisponível — rode na bancada: cd ambiente && docker compose up -d.")
    proc = subprocess.run(
        ["docker", "compose", "--profile", "spark", "run", "--rm", "spark",
         "/opt/spark/bin/spark-submit", RUNNER],
        cwd=str(AMB), capture_output=True, text=True, timeout=420,
    )
    linhas = [l for l in proc.stdout.splitlines() if l.startswith("RESULT_JSON=")]
    assert linhas, (
        "o job Spark não produziu resultado — implemente `resumo_por_categoria`.\n"
        f"stderr (fim):\n{proc.stderr[-800:]}"
    )
    obtido = json.loads(linhas[-1].split("=", 1)[1])
    assert obtido == ESPERADO
