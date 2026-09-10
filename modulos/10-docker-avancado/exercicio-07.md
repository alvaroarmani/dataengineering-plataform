# Exercício 07 — Escreva um Dockerfile de verdade (TRACK REAL · Docker)

**Onde roda:** 🐳 Bancada Docker (**build/run reais**). O grader **constrói a sua imagem** e **roda
o container**, conferindo a saída. Sem Docker? Os exercícios 01–06 cobrem os conceitos no navegador.

## Tarefa
Complete o [`exercicio-07/Dockerfile`](exercicio-07/Dockerfile) para empacotar e rodar o
`app.py` (que você **não** edita). Ao rodar o container, ele deve imprimir **`RESULT=65`**.

Você precisa: imagem base Python, `WORKDIR`, `COPY` do `app.py` e um `CMD` que rode `python app.py`.

## Como rodar o grader
```bash
pytest -q modulos/10-docker-avancado/exercicio-07
```
> O grader faz `docker build` da sua imagem e `docker run`, e confere a saída. **Fora da bancada,
> faz *skip*.**

## Dica
:::{dropdown} Dica
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```dockerfile
FROM python:3.12-slim   # imagem base enxuta com Python
WORKDIR /app            # diretório de trabalho dentro da imagem
COPY app.py .           # leva o app para dentro da imagem
CMD ["python", "app.py"]  # comando que roda quando o container sobe
```
:::

---
**Revisado em:** 2026-09-09
