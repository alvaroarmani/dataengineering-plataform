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

> **Armadilhas nos testes:** além do build e da execução (na bancada), checagens que rodam sem Docker: tag de imagem fixa (sem `latest`), `CMD` na forma exec (JSON) e nenhum comentário no fim de uma instrução.

## Dicas progressivas
:::{dropdown} Dica 1 — o que a imagem precisa ter
Uma imagem de Python mínima precisa de três coisas: uma **base** com Python (prefira uma `-slim`), o **código** copiado para dentro e o **comando** que roda quando o container sobe. O grader faz `docker build` e depois `docker run` e procura a saída do script.
:::
:::{dropdown} Dica 2 — a ordem das instruções
`FROM` sempre primeiro; depois defina a pasta de trabalho (`WORKDIR`) para não espalhar arquivos na raiz; copie só o necessário (`COPY app.py .`, não `COPY .`); e termine com `CMD` na forma de lista (`["python", "app.py"]`), que não passa por um shell.
:::
:::{dropdown} Dica 3 — quase lá
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```
Se o build passar e a saída não aparecer, confira se o `CMD` aponta para o arquivo no `WORKDIR`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```dockerfile
# imagem base enxuta com Python, com tag fixa (nunca latest)
FROM python:3.12-slim
# diretório de trabalho dentro da imagem
WORKDIR /app
# leva o app para dentro da imagem
COPY app.py .
# forma exec (JSON): o python vira o PID 1 e recebe o SIGTERM do docker stop
CMD ["python", "app.py"]
```
No Dockerfile, `#` só é comentário no **início** da linha. Escrito no fim de uma instrução,
ele vira argumento e quebra o build.
:::

---
**Revisado em:** 2026-09-30
