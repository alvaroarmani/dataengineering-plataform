# Lab 01 — Dockerfile multi-stage e cache (walkthrough guiado)

**Onde roda:** 🐳 Docker na sua máquina. Confira os **self-checks** ✅. A lógica (cache,
.dockerignore) você fixa nos [Exercícios 01](exercicio-01.md) e [02](exercicio-02.md).

Exemplo pronto em [`exemplo/`](exemplo/) (`Dockerfile` multi-stage + `main.py` + `requirements.txt` + `.dockerignore`).

---

## 1. Build da imagem
```bash
cd modulos/10-docker-avancado/exemplo
docker build -t curso-app:1.0 .
docker run --rm curso-app:1.0
```
✅ *Self-check:* imprime `Olá do container! soma = 6 | pandas 2.2.3`.

---

## 2. Veja o tamanho (multi-stage + slim)
```bash
docker images curso-app:1.0
```
✅ *Self-check:* a imagem é **bem menor** que uma baseada em `python:3.12` cheio, porque o
estágio final (`-slim`) recebe só o que o builder produziu.

---

## 3. Prove o cache de camadas
Edite `main.py` (mude o texto do print) e rebuilde:
```bash
docker build -t curso-app:1.1 .
```
✅ *Self-check:* o build **reaproveita** as camadas de `pip install` (aparece `CACHED`) e só
refaz a partir do `COPY . .` — segundos, não minutos. Se você mudasse `requirements.txt`, aí
sim o `pip install` rebuildaria.

---

## 4. .dockerignore em ação
O `exemplo/.dockerignore` exclui `__pycache__`, `.git`, `.env` do contexto. Rode com log:
```bash
docker build -t curso-app:1.2 . 2>&1 | head -1
```
✅ *Self-check:* o "transferring context" é pequeno (não manda lixo/segredos para o build).

---

## O que você levou daqui
Construiu uma imagem **multi-stage + slim**, provou o **cache de camadas** (deps antes do
código) e o **.dockerignore**. Fixe a lógica nos [Exercícios 01](exercicio-01.md) e [02](exercicio-02.md).

---
**Revisado em:** 2026-08-29
