import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import achar_segredos  # noqa: E402


def test_ler_do_ambiente_e_o_jeito_certo():
    assert achar_segredos({"etl.py": "import os\nsenha = os.environ['DB_PASS']\n"}) == []
    assert achar_segredos({"etl.py": "db = connect(password=os.getenv('DB_PASS'))"}) == []


def test_acha_os_tres_tipos():
    arquivos = {
        "config.py": "HOST = 'db'\npassword = 'S3nh@Forte'\n",
        "notebook.py": "# testando\nclient = boto3.client(aws_access_key_id='AKIAIOSFODNN7EXAMPLE')\n",
        "deploy/key.pem": "-----BEGIN RSA PRIVATE KEY-----\nMIIEow...\n",
    }
    assert achar_segredos(arquivos) == [
        ("config.py", 2, "senha"), ("deploy/key.pem", 1, "chave_privada"), ("notebook.py", 2, "chave_aws")]


@pytest.mark.parametrize("linha", [
    "password = ${DB_PASSWORD}",
    "senha: <sua-senha-aqui>",
    "token = {{ secrets.TOKEN }}",
    "PASSWORD=changeme",
    "password = '****'",
    "secret = None",
])
def test_placeholders_nao_sao_acusados(linha):
    assert achar_segredos({"app.yaml": linha}) == []


def test_arquivo_env_e_case_insensitive():
    arquivos = {"api/.env": "TOKEN=abc123\n", "vazio/.env": "  \n", "README.md": "Senha: hunter2"}
    assert achar_segredos(arquivos) == [("README.md", 1, "senha"), ("api/.env", 0, "arquivo_env"),
                                        ("api/.env", 1, "senha")]
