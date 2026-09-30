#!/usr/bin/env python3
"""Linter de conteúdo do curso.

Garante que toda página de teoria respeite o padrão de qualidade (por tipo) e que
nenhuma citação use fonte fora do registro `referencias.yaml` (combate citação inventada).

Uso:
    python scripts/verificar-conteudo.py [--check-links]

Sai com código != 0 se qualquer checagem BLOQUEANTE falhar. O --check-links testa o
alcance dos URLs, mas é sempre NÃO-BLOQUEANTE (apenas avisa).
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERRO: PyYAML não instalado (pip install pyyaml).", file=sys.stderr)
    sys.exit(2)

# Saída em UTF-8 mesmo em consoles legados (Windows cp1252).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Régua por tipo de página de teoria.
# min_refs é um PISO de fontes PERTINENTES — não uma cota a preencher. Uma referência só entra se
# sustenta de fato o conteúdo da página; inflar a lista para bater o número é proibido (ver
# CONTRIBUTING). Por isso o piso é 2, e a checagem de coerência título/ano (abaixo) é bloqueante.
REGRAS = {
    "conceitual": {"min_refs": 2, "quiz": True, "literatura_ou_paraalem": True, "doc_obrigatoria": False},
    "pratico":    {"min_refs": 2, "quiz": True, "literatura_ou_paraalem": False, "doc_obrigatoria": False},
    "ferramenta": {"min_refs": 2, "quiz": False, "literatura_ou_paraalem": False, "doc_obrigatoria": True},
}
TIPO_PADRAO = "conceitual"

RE_TIPO = re.compile(r"<!--\s*tipo:\s*([a-z]+)\s*-->", re.I)
RE_CHAVE = re.compile(r"<!--\s*@([a-z0-9-]+)\s*-->", re.I)
RE_REVISADO = re.compile(r"\*\*Revisado em:\*\*\s*(\d{4}-\d{2}-\d{2})")
RE_URL = re.compile(r"https?://[^\s)\]\"'>]+")


def carregar_registro(caminho: str) -> dict[str, dict]:
    """Retorna {chave: entrada} de todas as obras do registro."""
    with open(caminho, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    registro: dict[str, dict] = {}
    for grupo in data.values():
        if isinstance(grupo, dict):
            for chave, entrada in grupo.items():
                registro[chave] = entrada if isinstance(entrada, dict) else {}
    return registro


def carregar_chaves_registro(caminho: str) -> set[str]:
    return set(carregar_registro(caminho))


_STOP = {"the", "an", "of", "and", "for", "to", "in", "on", "that", "over",
         "da", "de", "do", "das", "dos", "um", "uma", "os", "as", "com", "para"}


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def _palavras_titulo(titulo: str) -> list[str]:
    """As 2 primeiras palavras significativas do título (identificam a obra)."""
    ws = re.findall(r"[a-z0-9]+", _norm(titulo))
    return [w for w in ws if w not in _STOP and len(w) >= 3][:2]


def checar_coerencia_citacoes(txt: str, registro: dict[str, dict]) -> list[str]:
    """Cada linha que cita <!-- @chave --> precisa bater com a obra registrada:
    o ANO e as palavras-chave do TÍTULO têm de aparecer na linha. Impede citar a obra X com a
    chave da obra Y (erro que já aconteceu: chave do Delta Lake 2020 descrita como Lakehouse 2021)."""
    erros: list[str] = []
    for linha in txt.splitlines():
        for chave in RE_CHAVE.findall(linha):
            ent = registro.get(chave)
            if not ent:
                continue  # chave desconhecida já é reportada em outro lugar
            alvo = _norm(linha)
            ano = str(ent.get("ano", "")).strip()
            faltas = []
            if ano and ano not in alvo:
                faltas.append(f"ano {ano}")
            falt_tit = [w for w in _palavras_titulo(str(ent.get("titulo", ""))) if w not in alvo]
            if falt_tit:
                faltas.append("título (" + ", ".join(falt_tit) + ")")
            if faltas:
                erros.append(
                    f"citação @{chave} não bate com o registro — falta {' e '.join(faltas)}; "
                    f"registro: '{ent.get('titulo')}' ({ano}). Linha: {linha.strip()[:90]}"
                )
    return erros


def tem_secao(texto: str, *palavras: str) -> bool:
    """True se houver um heading (##...) contendo alguma das palavras."""
    for linha in texto.splitlines():
        if linha.lstrip().startswith("#"):
            baixo = linha.lower()
            if any(p in baixo for p in palavras):
                return True
    return False


def validar_teoria(caminho: str, chaves: set[str], registro: dict[str, dict] | None = None) -> list[str]:
    erros: list[str] = []
    with open(caminho, encoding="utf-8") as f:
        txt = f.read()
    if registro:
        erros.extend(checar_coerencia_citacoes(txt, registro))

    m = RE_TIPO.search(txt)
    tipo = (m.group(1).lower() if m else TIPO_PADRAO)
    if tipo not in REGRAS:
        erros.append(f"tipo inválido '{tipo}' (use: {', '.join(REGRAS)}) — declare com <!-- tipo: X -->")
        tipo = TIPO_PADRAO
    regra = REGRAS[tipo]

    # Revisado em (data válida)
    mr = RE_REVISADO.search(txt)
    if not mr:
        erros.append("falta a linha '**Revisado em:** AAAA-MM-DD'")
    else:
        try:
            dt.date.fromisoformat(mr.group(1))
        except ValueError:
            erros.append(f"data de revisão inválida: {mr.group(1)}")

    # Seção de Referências
    if not tem_secao(txt, "refer"):
        erros.append("falta a seção '## Referências'")

    # Citações com chave -> todas devem existir no registro
    chaves_usadas = RE_CHAVE.findall(txt)
    desconhecidas = sorted({c for c in chaves_usadas if c not in chaves})
    if desconhecidas:
        erros.append(
            "citação com fonte FORA do registro (referencias.yaml): "
            + ", ".join(f"@{c}" for c in desconhecidas)
        )
    if len(chaves_usadas) < regra["min_refs"]:
        erros.append(
            f"referências insuficientes: {len(chaves_usadas)} < mínimo {regra['min_refs']} "
            f"(tipo {tipo}). Marque cada referência com <!-- @chave -->"
        )

    # Quiz de recall
    if regra["quiz"] and not tem_secao(txt, "quiz"):
        erros.append("falta a seção 'Quiz de recall'")

    # Motivação/problema (conceitual)
    if tipo == "conceitual" and not tem_secao(txt, "problema", "motiva"):
        erros.append("falta a seção de motivação ('O problema' / motivação)")

    # Da literatura OU Para ir além (conceitual)
    if regra["literatura_ou_paraalem"]:
        if ("da literatura" not in txt.lower()) and (not tem_secao(txt, "para ir além", "para ir alem")):
            erros.append("falta ao menos um box '📖 Da literatura' OU a seção 'Para ir além'")

    # Doc oficial obrigatória (ferramenta)
    if regra["doc_obrigatoria"] and not any(c.startswith("docs-") for c in chaves_usadas):
        erros.append("tipo 'ferramenta' exige ao menos uma doc oficial (chave docs-*)")

    return erros


def validar_index(caminho: str) -> list[str]:
    with open(caminho, encoding="utf-8") as f:
        txt = f.read()
    if not RE_REVISADO.search(txt):
        return ["falta a linha '**Revisado em:** AAAA-MM-DD'"]
    return []


def checar_links(caminho: str) -> list[str]:
    """Não-bloqueante: verifica alcance dos URLs. Retorna avisos."""
    import urllib.request

    avisos: list[str] = []
    with open(caminho, encoding="utf-8") as f:
        urls = set(RE_URL.findall(f.read()))
    for url in sorted(urls):
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "curso-linter"})
        try:
            urllib.request.urlopen(req, timeout=8)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"link possivelmente quebrado: {url} ({e.__class__.__name__})")
    return avisos


FERRAMENTAS_REAIS = ("bigquery", "dbt", "airflow", "spark", "docker")


def checar_estrutura(avisos_out: list[str]) -> None:
    """Checks estruturais NÃO-BLOQUEANTES (avisos) da doutrina dual-track / fluência.

    - Fluência: a partir do M4, esperamos >=2 exercícios por unidade (teoria).
    - Track real: módulos de ferramenta (BigQuery/dbt/Airflow/Spark/Docker) devem ter ao
      menos um exercício com grader real (exercicio-*/conftest.py), não só DuckDB.
    """
    mod_dir = os.path.join(RAIZ, "modulos")
    if not os.path.isdir(mod_dir):
        return
    for nome in sorted(os.listdir(mod_dir)):
        d = os.path.join(mod_dir, nome)
        if not (os.path.isdir(d) and re.match(r"^\d\d-", nome)):
            continue
        num = int(nome[:2])
        teorias = glob.glob(os.path.join(d, "teoria-*.md"))
        if not teorias:
            continue  # módulo ainda stub — sem cobrança
        exercicios = glob.glob(os.path.join(d, "exercicio-*.md"))
        # fluência (a partir do M4): >=2 exercícios por unidade
        if num >= 4 and len(exercicios) < 2 * len(teorias):
            avisos_out.append(
                f"{nome}: fluência abaixo da barra — {len(exercicios)} exercícios para "
                f"{len(teorias)} unidades (esperado >= {2 * len(teorias)}; ≥2 por unidade)"
            )
        # track real: módulos de ferramenta precisam de prática real —
        # um grader real (exercicio-*/conftest.py) OU um lab guiado na ferramenta real (🐳).
        if any(t in nome for t in FERRAMENTAS_REAIS):
            tem_conftest = bool(glob.glob(os.path.join(d, "exercicio-*", "conftest.py")))
            tem_lab_real = False
            for lab in glob.glob(os.path.join(d, "lab-*.md")):
                try:
                    txt = open(lab, encoding="utf-8").read().lower()
                except OSError:
                    continue
                if "🐳" in txt or "docker compose" in txt or "docker build" in txt or "bancada docker" in txt:
                    tem_lab_real = True
                    break
            if not (tem_conftest or tem_lab_real):
                avisos_out.append(
                    f"{nome}: ferramenta real esperada, mas sem grader real (exercicio-*/conftest.py) "
                    f"nem lab guiado na ferramenta (🐳) — evite DuckDB disfarçado"
                )
        # riqueza: exercício com poucas checagens ou sem escada de dicas vira "lookup" — não treina
        rasos, sem_dicas, sem_acento = [], [], []
        for md in sorted(exercicios):
            base = os.path.splitext(os.path.basename(md))[0]
            testes = glob.glob(os.path.join(d, base, "tests", "*.py"))
            if testes:
                n = sum(len(RE_CHECAGEM.findall(open(t, encoding="utf-8").read())) for t in testes)
                if n < MIN_CHECAGENS:
                    rasos.append(f"{base}({n})")
            txt = open(md, encoding="utf-8").read()
            if len(re.findall(r"Dica \d", txt)) < 2:
                sem_dicas.append(base)
            if RE_SEM_ACENTO.search(txt):
                sem_acento.append(base)
        if rasos:
            avisos_out.append(f"{nome}: exercícios rasos (< {MIN_CHECAGENS} checagens nos testes): "
                              + ", ".join(rasos))
        if sem_dicas:
            avisos_out.append(f"{nome}: exercícios com < 2 dicas progressivas: " + ", ".join(sem_dicas))
        if sem_acento:
            avisos_out.append(f"{nome}: enunciados sem acentuação (ex.: 'nao', 'voce'): " + ", ".join(sem_acento))


# Riqueza de exercício: assert/pytest.raises contam como checagem.
RE_CHECAGEM = re.compile(r"^\s*assert\b|pytest\.raises", re.M)
MIN_CHECAGENS = 4
# Texto em português sem acento (resquício de arquivos gerados às pressas).
RE_SEM_ACENTO = re.compile(r"(?<![\w/.`-])(nao|voce|funcao|codigo|tambem|entao|solucao)(?![\w/.`-])", re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-links", action="store_true", help="testa alcance dos URLs (não-bloqueante)")
    args = ap.parse_args()

    reg = os.path.join(RAIZ, "referencias.yaml")
    if not os.path.exists(reg):
        print("ERRO: referencias.yaml não encontrado na raiz.", file=sys.stderr)
        return 2
    registro = carregar_registro(reg)
    chaves = set(registro)

    teorias = glob.glob(os.path.join(RAIZ, "modulos", "**", "teoria-*.md"), recursive=True)
    indices = glob.glob(os.path.join(RAIZ, "modulos", "**", "index.md"), recursive=True)

    total_erros = 0
    total_avisos = 0

    for caminho in sorted(teorias):
        rel = os.path.relpath(caminho, RAIZ)
        erros = validar_teoria(caminho, chaves, registro)
        if erros:
            total_erros += len(erros)
            print(f"\n❌ {rel}")
            for e in erros:
                print(f"   - {e}")
        else:
            print(f"✅ {rel}")
        if args.check_links:
            for a in checar_links(caminho):
                total_avisos += 1
                print(f"   ⚠️  {a}")

    for caminho in sorted(indices):
        rel = os.path.relpath(caminho, RAIZ)
        erros = validar_index(caminho)
        if erros:
            total_erros += len(erros)
            print(f"\n❌ {rel}")
            for e in erros:
                print(f"   - {e}")

    # Checks estruturais (não-bloqueantes) — doutrina dual-track / fluência
    avisos_estrut: list[str] = []
    checar_estrutura(avisos_estrut)
    if avisos_estrut:
        print("\n— Avisos estruturais (não-bloqueantes) —")
        for a in avisos_estrut:
            total_avisos += 1
            print(f"   ⚠️  {a}")

    print("\n" + "=" * 60)
    print(f"Teorias: {len(teorias)} · Índices: {len(indices)} · "
          f"Erros (bloqueantes): {total_erros} · Avisos: {total_avisos}")
    if total_erros:
        print("FALHOU — corrija os erros acima.")
        return 1
    print("OK — padrão de conteúdo respeitado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
