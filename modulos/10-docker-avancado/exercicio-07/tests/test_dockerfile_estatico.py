"""Checagens estáticas do Dockerfile (rodam sem Docker): boas práticas que o build não pega."""
import json
from pathlib import Path

DOCKERFILE = Path(__file__).resolve().parents[1] / "Dockerfile"


def _instrucoes():
    linhas = DOCKERFILE.read_text(encoding="utf-8").splitlines()
    return [l.strip().split(None, 1) for l in linhas if l.strip() and not l.strip().startswith("#")]


def _args(nome):
    return [i[1] if len(i) > 1 else "" for i in _instrucoes() if i[0].upper() == nome]


def test_tem_from_cmd_e_copy():
    assert _args("FROM"), "falta o FROM (imagem base)"
    assert _args("CMD"), "falta o CMD"
    assert any("app.py" in a for a in _args("COPY") + _args("ADD")), "o app.py não é copiado para a imagem"


def test_imagem_base_com_tag_fixa():
    imagem = _args("FROM")[0].split()[0]
    assert ":" in imagem and not imagem.endswith(":latest"), (
        f"'{imagem}': fixe a tag (ex.: python:3.12-slim). Sem tag ou com latest, o build muda sozinho."
    )


def test_cmd_na_forma_exec():
    cmd = _args("CMD")[-1]
    assert cmd.startswith("["), "use a forma exec: CMD [\"python\", \"app.py\"] (a forma shell não repassa o SIGTERM)"
    assert json.loads(cmd)[-1].endswith("app.py")


def test_sem_comentario_no_fim_da_linha():
    # '#' no meio da instrução vira argumento e quebra o build
    assert not [i for i in _instrucoes() if len(i) > 1 and " #" in i[1]], "comentário só no início da linha"
