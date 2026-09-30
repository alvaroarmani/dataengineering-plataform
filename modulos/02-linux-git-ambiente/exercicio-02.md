# Exercício 02 — Pre-commit: achar segredos antes do commit

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O `.gitignore` (exercício 01) evita versionar o arquivo `.env`. Mas o vazamento mais comum não é o
`.env` — é a senha **colada no código** "só para testar", ou a chave de nuvem num notebook. Uma vez
no histórico do Git (e num repositório público), o segredo está vazado, mesmo que você apague no
commit seguinte.

Por isso times usam um **hook de pre-commit** que varre os arquivos antes de cada commit e bloqueia
o que parece segredo. Você vai escrever o núcleo dessa varredura — incluindo a parte difícil: **não**
acusar placeholders como `password = ${DB_PASSWORD}`, senão o time desliga o hook em uma semana.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `achar_segredos(arquivos)`.

```bash
cd modulos/02-linux-git-ambiente/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma regex por tipo
`re.compile(r"AKIA[0-9A-Z]{16}")` para a chave AWS; `-----BEGIN [A-Z ]*PRIVATE KEY-----` para chave privada; para senha, capture o **resto da linha** como valor: `(password|senha|secret|token)\s*[:=]\s*(.+)` com `(?i)`.
:::
:::{dropdown} Dica 2 — placeholders
Limpe o valor capturado (`strip()`, aspas, `)` e `,` nas pontas) e teste contra uma regex de placeholders (`${...}`, `<...>`, `{{...}}`, asteriscos, `changeme`, `os.environ`/`os.getenv`...). Se casar, ignore.
:::
:::{dropdown} Dica 3 — o .env
`caminho.split("/")[-1] == ".env"` pega o arquivo em qualquer pasta; só acuse se o conteúdo não for vazio. Numere as linhas com `enumerate(..., start=1)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re

PADROES = [
    ("chave_aws", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("chave_privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("senha", re.compile(r"(?i)\b(password|senha|secret|token)\s*[:=]\s*(.+)")),
]
PLACEHOLDER = re.compile(r"^(\$\{.*\}|<.*>|\{\{.*\}\}|\*+|x+|changeme|none|null|os\.(environ|getenv).*)$", re.I)


def achar_segredos(arquivos: dict) -> list:
    achados = []
    for caminho, conteudo in arquivos.items():
        if caminho.split("/")[-1] == ".env" and conteudo.strip():
            achados.append((caminho, 0, "arquivo_env"))
        for n, linha in enumerate(conteudo.splitlines(), start=1):
            for tipo, rx in PADROES:
                m = rx.search(linha)
                if not m:
                    continue
                if tipo == "senha" and PLACEHOLDER.match(m.group(2).strip().strip("'\"").rstrip(",)")):
                    continue
                achados.append((caminho, n, tipo))
    return sorted(achados)
```
Os placeholders são a parte que decide se a ferramenta sobrevive no time: `${DB_PASSWORD}`,
`{{ secrets.TOKEN }}` e `<sua-senha-aqui>` são exatamente como se **deve** escrever configuração —
acusá-los ensinaria todo mundo a ignorar o hook. Ferramentas reais (gitleaks, detect-secrets, o
secret scanning do GitHub) combinam regex, entropia do valor e listas de exceção pelo mesmo motivo.

E se o segredo já foi commitado? Apagar no commit seguinte **não** resolve: ele continua no
histórico. O procedimento correto é **revogar e trocar** a credencial imediatamente — e só depois
limpar o histórico. Gestão de segredos volta no M14.
:::

---
**Revisado em:** 2026-09-30
