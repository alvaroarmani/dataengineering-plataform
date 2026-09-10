"""Grader do Exercício 07 (M10) — builda o Dockerfile do aluno e roda o container REAL.

Fora da bancada (sem Docker), faz *skip*. Com o Docker de pé, `docker build` + `docker run` —
se o Dockerfile estiver incompleto, o build falha e o teste FALHA.
"""
import shutil
import subprocess
from pathlib import Path

import pytest

CTX = Path(__file__).resolve().parents[1]   # exercicio-07/ = contexto do build
TAG = "curso-m10-ex07"


def _docker_ok() -> bool:
    if shutil.which("docker") is None:
        return False
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


def test_dockerfile_builda_e_roda():
    if not _docker_ok():
        pytest.skip("Docker indisponível — rode na bancada: cd ambiente && docker compose up -d.")
    build = subprocess.run(["docker", "build", "-t", TAG, str(CTX)],
                           capture_output=True, text=True, timeout=420)
    assert build.returncode == 0, (
        "`docker build` falhou — complete o Dockerfile.\n" + build.stderr[-900:]
    )
    run = subprocess.run(["docker", "run", "--rm", TAG],
                         capture_output=True, text=True, timeout=60)
    assert "RESULT=65" in run.stdout, (
        f"o container não imprimiu RESULT=65 (obtido: {run.stdout!r}). "
        "Confira o CMD do Dockerfile."
    )
