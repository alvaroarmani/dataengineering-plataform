"""Checagens estáticas da solução (rodam sem Spark): o que o resultado certo não garante."""
import ast
from pathlib import Path

SOLUCAO = Path(__file__).resolve().parents[1] / "solucao.py"


def _funcao():
    arvore = ast.parse(SOLUCAO.read_text(encoding="utf-8"))
    return next(n for n in arvore.body if isinstance(n, ast.FunctionDef) and n.name == "resumo_por_categoria")


def _metodos_chamados():
    return {n.func.attr for n in ast.walk(_funcao()) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}


def test_implementada():
    assert not any(isinstance(n, ast.Raise) for n in ast.walk(_funcao())), "implemente a função"


def test_sem_acao_dentro_da_transformacao():
    # ações trazem os dados ao driver; a transformação deve devolver um DataFrame lazy
    acoes = _metodos_chamados() & {"collect", "toPandas", "show", "take", "toLocalIterator"}
    assert not acoes, f"ação dentro da transformação: {sorted(acoes)} — devolva o DataFrame, quem chama decide"


def test_sem_udf_python():
    assert not _metodos_chamados() & {"udf", "pandas_udf"}, "use funções nativas (F.*): UDF Python tira o Catalyst do jogo"


def test_colunas_de_saida_nomeadas():
    nomes = {a.value for n in ast.walk(_funcao())
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr in {"alias", "withColumnRenamed", "withColumn"}
             for a in n.args if isinstance(a, ast.Constant)}
    assert {"total_receita", "n_itens"} <= nomes, "nomeie as saídas com .alias('total_receita') e .alias('n_itens')"
