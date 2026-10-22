#!/usr/bin/env python3
"""Verifica os graders dos exercícios (o "faça o pytest passar").

Para cada modulos/*/exercicio-*/ (cada um num processo próprio, numa cópia temporária):
  1. o template vazio precisa FALHAR  — um grader que passa sem resposta não corrige nada;
  2. o gabarito precisa PASSAR        — senão o aluno com a resposta certa fica preso no vermelho.

De onde vem o gabarito, em ordem:
  a) gabaritos/<modulo>/<exercicio>/  — arquivos sobrepostos à cópia (mesmos caminhos relativos);
  b) a "Solução comentada" do exercicio-NN.md — quando há UM arquivo com "SEU CÓDIGO" e UM bloco
     de código da mesma linguagem. Assim o CI também prova que a solução publicada funciona.

Graders que dependem de serviço (Postgres, Docker, Spark...) fazem skip sem ele; isso é reportado,
não reprovado. Uso:
    python scripts/verificar-graders.py [filtro]      # filtro: trecho do caminho, ex. "m04" ou "08-"
Sai != 0 se algum template passar, algum gabarito falhar ou algum exercício estiver sem gabarito.
"""
from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

RAIZ = Path(__file__).resolve().parents[1]
GABARITOS = RAIZ / "gabaritos"
MARCA = re.compile(r"SEU C[ÓO]DIGO", re.I)
# target/ e logs/ são saídas locais do dbt (não versionadas).
IGNORAR = {"tests", "__pycache__", ".pytest_cache", "conftest.py", "target", "logs"}
LING = {".py": {"python", "py"}, ".sql": {"sql"}, ".yml": {"yaml", "yml"}, ".yaml": {"yaml", "yml"},
        "Dockerfile": {"dockerfile", "docker"}}
# Rótulo de cada consulta dentro de um bloco SQL: "-- CONSULTA_A", "-- consulta_b" ou "-- C)".
RE_ROTULO = re.compile(r"^\s*--\s*(?:consulta[ _]?([a-d])\b|([a-d])\))", re.I)
RE_RESUMO = re.compile(r"(\d+) (passed|failed|skipped|error|errors|xfailed|xpassed)")


def arquivos_do_aluno(ex: Path) -> list[Path]:
    """Arquivos que o aluno preenche: os que trazem o marcador "SEU CÓDIGO"."""
    out = []
    for p in ex.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ex).parts) & IGNORAR):
            try:
                if MARCA.search(p.read_text(encoding="utf-8")):
                    out.append(p)
            except (UnicodeDecodeError, OSError):
                pass
    return out


def blocos_da_solucao(md: Path) -> list[tuple[str, str]]:
    """(linguagem, código) de cada bloco cercado dentro da seção "Solução comentada"."""
    if not md.exists():
        return []
    txt = md.read_text(encoding="utf-8")
    m = re.search(r"^#+ .*Solu[çc][ãa]o comentada.*$", txt, re.M | re.I)
    if not m:
        return []
    return re.findall(r"^\s*```(\w*)[^\n]*\n(.*?)^\s*```\s*$", txt[m.end():], re.M | re.S)


def gabarito_de(ex: Path) -> dict[str, str] | None:
    """{caminho relativo: conteúdo} a sobrepor, ou None se não há gabarito."""
    rel = ex.relative_to(RAIZ / "modulos")
    sobre = GABARITOS / rel
    if sobre.is_dir():
        return {str(p.relative_to(sobre)): p.read_text(encoding="utf-8")
                for p in sobre.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    alvos = arquivos_do_aluno(ex)
    blocos = blocos_da_solucao(ex.parent / f"{ex.name}.md")
    de = lambda ling: [c for lang, c in blocos if lang.lower() in ling]  # noqa: E731
    sql = de({"sql"})

    # Consultas em arquivos .sql separados (consulta_a.sql, consulta_b.sql) e UM bloco rotulado.
    if len(alvos) > 1 and all(a.suffix == ".sql" for a in alvos) and len(sql) == 1:
        partes = sql_por_letra(sql[0])
        letras = {a: _letra(a.stem) for a in alvos}
        if all(l in partes for l in letras.values()):
            return {str(a.relative_to(ex)): partes[l] for a, l in letras.items()}
        return None
    if len(alvos) != 1:
        return None
    alvo = alvos[0]

    if alvo.suffix == ".py":
        template = alvo.read_text(encoding="utf-8")
        # Bloco Python que define algo (descarta trechos de demonstração soltos).
        py = [c for c in de(LING[".py"])
              if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for n in _parse(c).body)]
        if len(py) == 1:
            return {str(alvo.relative_to(ex)): mesclar_py(template, py[0])}
        # SQL dentro de strings Python (CONSULTA, CONSULTA_A...) e o .md mostra o SQL.
        consts = constantes_a_preencher(template)
        if consts and len(sql) == 1:
            partes = sql_por_letra(sql[0])
            if len(consts) == 1:
                valores = {consts[0]: partes.get(None, sql[0]) if len(partes) <= 1 else None}
            else:
                valores = {c: partes.get(_letra(c)) for c in consts}
            if None in valores.values():
                return None
            solucao = "\n".join(f"{c} = {v!r}" for c, v in valores.items())
            return {str(alvo.relative_to(ex)): mesclar_py(template, solucao)}
        return None

    chave = alvo.name if alvo.name in LING else alvo.suffix
    blocos_ling = de(LING.get(chave, set()))
    if len(blocos_ling) != 1:
        return None
    return {str(alvo.relative_to(ex)): blocos_ling[0]}


def _parse(codigo: str) -> ast.Module:
    try:
        return ast.parse(codigo)
    except SyntaxError:
        return ast.Module(body=[], type_ignores=[])


def _letra(nome: str) -> str | None:
    m = re.search(r"[_ ]([a-d])$", nome, re.I)
    return m.group(1).upper() if m else None


def constantes_a_preencher(template: str) -> list[str]:
    """Nomes de constantes string do template que ainda trazem o marcador (ex.: CONSULTA_A)."""
    out = []
    for n in _parse(template).body:
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
            if MARCA.search(n.value.value):
                out += [t.id for t in n.targets if isinstance(t, ast.Name)]
    return out


def sql_por_letra(bloco: str) -> dict[str | None, str]:
    """Divide um bloco SQL pelos rótulos (-- CONSULTA_A / -- A)). Sem rótulo: {None: bloco}."""
    partes: dict[str | None, list[str]] = {}
    atual = None
    for linha in bloco.splitlines():
        m = RE_ROTULO.match(linha)
        if m:
            atual = (m.group(1) or m.group(2)).upper()
        partes.setdefault(atual, []).append(linha)
    if len(partes) > 1:
        partes.pop(None, None)  # texto antes do primeiro rótulo
    return {k: "\n".join(v).strip() + "\n" for k, v in partes.items()}


def _nomes_topo(arvore: ast.Module) -> dict[str, ast.stmt]:
    out = {}
    for n in arvore.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[n.name] = n
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                if isinstance(t, ast.Name):
                    out[t.id] = n
    return out


def mesclar_py(template: str, solucao: str) -> str:
    """Preenche o template como o aluno faria: a solução publicada costuma trazer só as funções
    (as constantes já estão no template). Tira do template o que a solução redefine e junta."""
    redefinidos = set(_nomes_topo(ast.parse(solucao)))
    linhas = template.splitlines()
    cortar = set()
    for nome, n in _nomes_topo(ast.parse(template)).items():
        if nome in redefinidos:
            ini = min([n.lineno] + [d.lineno for d in getattr(n, "decorator_list", [])])
            cortar.update(range(ini - 1, n.end_lineno))
    base = "\n".join(l for i, l in enumerate(linhas) if i not in cortar)
    return base + "\n\n# ---- gabarito (Solução comentada) ----\n" + solucao


def _autoteste_mesclar() -> None:
    t = 'X = 1\n\n\ndef f():\n    """doc"""\n    raise NotImplementedError\n'
    r = mesclar_py(t, "def f():\n    return X\n")
    ns: dict = {}
    exec(r, ns)
    assert ns["f"]() == 1 and r.count("def f") == 1, r
    p = sql_por_letra("-- CONSULTA_A: x\nSELECT 1;\n-- A partir daqui não é rótulo\n-- B) y\nSELECT 2;")
    assert set(p) == {"A", "B"} and "SELECT 1" in p["A"] and "A partir" in p["A"] and "SELECT 2" in p["B"], p
    assert sql_por_letra("SELECT 1") == {None: "SELECT 1\n"}


def _path_sem_docker() -> str:
    """PATH sem o executável do docker: graders que usam a bancada (docker compose) leem os
    arquivos do repo pelo volume do container, então não dá para verificá-los numa cópia — eles
    fazem skip, como fariam para um aluno sem Docker."""
    nomes = ("docker", "docker.exe")
    return os.pathsep.join(d for d in os.environ.get("PATH", "").split(os.pathsep)
                           if not any((Path(d) / n).exists() for n in nomes))


PATH_SEM_DOCKER = _path_sem_docker()


def rodar_pytest(pasta: Path) -> tuple[int, dict[str, int], str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PATH": PATH_SEM_DOCKER}
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header"],
                       cwd=pasta, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, timeout=300)
    saida = r.stdout + r.stderr
    linhas = [l for l in saida.strip().splitlines() if l.strip()]
    cont: dict[str, int] = {}
    for n, k in RE_RESUMO.findall(linhas[-1] if linhas else ""):
        cont[k.rstrip("s") if k == "errors" else k] = int(n)
    return r.returncode, cont, saida


def copia(ex: Path, destino: Path) -> Path:
    """Copia mantendo a profundidade modulos/<mod>/<ex> (há graders que acham a raiz por
    parents[4]) e, se o grader usa datasets/amostras, leva a amostra junto."""
    rel = ex.relative_to(RAIZ)
    alvo = destino / rel
    shutil.copytree(ex, alvo, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    testes = " ".join(p.read_text(encoding="utf-8", errors="ignore") for p in (ex / "tests").glob("*.py"))
    if "datasets" in testes:
        shutil.copytree(RAIZ / "datasets" / "amostras", destino / "datasets" / "amostras")
    return alvo


def verificar(ex: Path) -> dict:
    rel = str(ex.relative_to(RAIZ)).replace("\\", "/")
    res = {"ex": rel, "template": None, "gabarito": None, "detalhe": ""}
    bancada = GABARITOS / ex.relative_to(RAIZ / "modulos") / "BANCADA"
    if bancada.exists():
        # Grader de ferramenta real que lê o que a ferramenta construiu (dbt build, docker build):
        # não há como verificar numa cópia; o arquivo diz como verificar na bancada.
        res["template"] = res["gabarito"] = "BANCADA"
        return res
    with tempfile.TemporaryDirectory() as tmp:
        # 1) template vazio: precisa falhar (ou skip, se o grader depende de serviço ausente)
        rc, cont, saida = rodar_pytest(copia(ex, Path(tmp) / "t"))
        if rc == 0 and cont.get("passed"):
            res["template"] = "PASSA_VAZIO"
        elif rc == 0:
            res["template"] = "SKIP"
        elif rc == 1:
            res["template"] = "ok"
        else:
            res["template"] = f"ERRO_COLETA(rc={rc})"
            res["detalhe"] = saida[-1500:]

        # 2) gabarito: precisa passar
        gab = gabarito_de(ex)
        if gab is None:
            res["gabarito"] = "SEM_GABARITO"
            return res
        alvo = copia(ex, Path(tmp) / "g")
        for caminho, conteudo in gab.items():
            p = alvo / caminho
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(conteudo, encoding="utf-8")
        rc, cont, saida = rodar_pytest(alvo)
        if rc == 0 and cont.get("passed"):
            res["gabarito"] = "PASSA" if not cont.get("skipped") else "PASSA_PARCIAL"
        elif rc == 0:
            res["gabarito"] = "SKIP"
        else:
            res["gabarito"] = "FALHA"
            res["detalhe"] = saida[-2500:]
    return res


def main() -> int:
    _autoteste_mesclar()
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    exs = sorted(p for p in (RAIZ / "modulos").glob("*/exercicio-*") if p.is_dir() and (p / "tests").is_dir())
    exs = [e for e in exs if filtro in str(e.relative_to(RAIZ)).replace("\\", "/").lower()]
    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as pool:
        resultados = list(pool.map(verificar, exs))

    # No CI o Postgres é um serviço do job: um grader de Postgres (conftest.py) em skip ali significa
    # que o serviço não subiu — e o CI ficaria verde sem testar nada.
    exigir_pg = os.environ.get("EXIGIR_POSTGRES") == "1"
    ruins = []
    for r in resultados:
        ruim = (r["template"] not in ("ok", "SKIP", "BANCADA")) or (r["gabarito"] in ("FALHA", "SEM_GABARITO"))
        if exigir_pg and r["gabarito"] == "SKIP" and (RAIZ / r["ex"] / "conftest.py").exists():
            ruim = True
            r["detalhe"] = "EXIGIR_POSTGRES=1, mas o grader de Postgres fez skip: o serviço não está acessível."
        pulou = {"SKIP", "BANCADA", "PASSA_PARCIAL"} & {r["template"], r["gabarito"]}
        marca = "❌" if ruim else ("⏭️ " if pulou else "✅")
        print(f"{marca} {r['ex']:<55} template={r['template']:<16} gabarito={r['gabarito']}")
        if ruim:
            ruins.append(r)

    for r in ruins:
        if r["detalhe"]:
            print(f"\n{'=' * 70}\n{r['ex']}  (template={r['template']}, gabarito={r['gabarito']})\n{r['detalhe']}")

    def n(chave, valor):
        return sum(1 for r in resultados if r[chave] == valor)
    print("\n" + "=" * 70)
    print(f"Exercícios: {len(resultados)} · gabarito passa: {n('gabarito', 'PASSA') + n('gabarito', 'PASSA_PARCIAL')} · "
          f"skip (serviço ausente): {n('gabarito', 'SKIP')} · falha: {n('gabarito', 'FALHA')} · "
          f"sem gabarito: {n('gabarito', 'SEM_GABARITO')} · template passa vazio: {n('template', 'PASSA_VAZIO')} · "
          f"só na bancada: {n('gabarito', 'BANCADA')}")
    if ruins:
        print(f"FALHOU — {len(ruins)} exercício(s) com problema.")
        return 1
    print("OK — todo grader reprova o template e aprova o gabarito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
