import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import mudancas, proxima_versao  # noqa: E402

V1 = {
    "requisicao": {"cliente_id": {"tipo": "int", "obrigatorio": True},
                   "cupom": {"tipo": "str", "obrigatorio": False},
                   "canal": {"tipo": "str", "obrigatorio": True}},
    "resposta": {"id": {"tipo": "int"}, "total": {"tipo": "float"}, "status": {"tipo": "str"}},
}


def _v2(**alt):
    import copy
    v = copy.deepcopy(V1)
    for caminho, valor in alt.items():
        lado, campo = caminho.split("__")
        if valor is None:
            del v[lado][campo]
        else:
            v[lado][campo] = valor
    return v


def test_so_adicoes_compativeis():
    v2 = _v2(resposta__moeda={"tipo": "str"}, requisicao__origem={"tipo": "str", "obrigatorio": False})
    m = mudancas(V1, v2)
    assert m == {"incompativeis": [], "compativeis": ["requisicao.origem:adicionado", "resposta.moeda:adicionado"]}
    assert proxima_versao("2.4.1", m) == "2.5.0"


def test_quebras_na_resposta():
    m = mudancas(V1, _v2(resposta__status=None, resposta__total={"tipo": "str"}))
    assert m["incompativeis"] == ["resposta.status:removido", "resposta.total:tipo"]
    assert proxima_versao("2.4.1", m) == "3.0.0"


def test_assimetria_da_requisicao():
    v2 = _v2(requisicao__cupom={"tipo": "str", "obrigatorio": True},
             requisicao__canal={"tipo": "str", "obrigatorio": False},
             requisicao__loja={"tipo": "int", "obrigatorio": True},
             requisicao__cliente_id=None)
    assert mudancas(V1, v2) == {
        "incompativeis": ["requisicao.cupom:virou_obrigatorio", "requisicao.loja:novo_obrigatorio"],
        "compativeis": ["requisicao.canal:virou_opcional", "requisicao.cliente_id:removido"]}


def test_sem_mudancas_e_versao_invalida():
    m = mudancas(V1, V1)
    assert m == {"incompativeis": [], "compativeis": []}
    assert proxima_versao("1.0.9", m) == "1.0.10"
    with pytest.raises(ValueError):
        proxima_versao("v1.2", m)
