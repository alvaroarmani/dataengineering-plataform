import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import analisar_commit, proxima_versao  # noqa: E402


def test_formatos_validos():
    assert analisar_commit("feat: nova DAG de vendas") == {
        "tipo": "feat", "escopo": None, "breaking": False, "descricao": "nova DAG de vendas"}
    assert analisar_commit("fix(dbt): corrige join duplicado") == {
        "tipo": "fix", "escopo": "dbt", "breaking": False, "descricao": "corrige join duplicado"}
    assert analisar_commit("refactor(api)!: remove endpoint v1")["breaking"] is True


def test_breaking_no_rodape():
    msg = "feat(schema): troca tipo de valor\n\nBREAKING CHANGE: valor agora é decimal"
    assert analisar_commit(msg)["breaking"] is True


@pytest.mark.parametrize("msg", [
    "mudei umas coisas",
    "Feat: maiúscula não vale",
    "feat:sem espaço",
    "feat: ",
    "wip: ainda não",
    "fix: " + "x" * 70,
])
def test_invalidos(msg):
    with pytest.raises(ValueError):
        analisar_commit(msg)


def test_proxima_versao():
    assert proxima_versao("1.4.2", ["fix: a", "docs: b"]) == "1.4.3"
    assert proxima_versao("1.4.2", ["fix: a", "feat: b"]) == "1.5.0"
    assert proxima_versao("1.4.2", ["feat: a", "fix!: b"]) == "2.0.0"
    assert proxima_versao("1.4.2", ["docs: a", "chore: b"]) == "1.4.2"
    with pytest.raises(ValueError):
        proxima_versao("1.4.2", ["feat: ok", "ajustes"])
