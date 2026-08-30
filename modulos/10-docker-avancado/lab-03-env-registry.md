# Lab 03 — Env, segredos e registry (walkthrough guiado)

**Onde roda:** 🐳 Docker na sua máquina. Confira os **self-checks** ✅. A lógica (resolver env,
parse de imagem) você fixa nos [Exercícios 05](exercicio-05.md) e [06](exercicio-06.md).

---

## 1. Configuração por variável de ambiente (sem rebuild)
A mesma imagem, comportamento diferente por env:
```bash
docker run --rm -e SAUDACAO="Olá, prod" alpine sh -c 'echo "$SAUDACAO"'
docker run --rm -e SAUDACAO="Olá, dev"  alpine sh -c 'echo "$SAUDACAO"'
```
✅ *Self-check:* a saída muda conforme `-e SAUDACAO=...`, sem reconstruir a imagem.

---

## 2. `.env` e `${VAR:-default}` no Compose
A bancada usa `${POSTGRES_PASSWORD:-curso}` vindo do `.env` (que está no `.gitignore`; versionado
só o `.env.example`). Confirme:
```bash
cd ambiente
grep -n "POSTGRES_PASSWORD" docker-compose.yml
git check-ignore .env && echo ".env está ignorado (bom!)"
```
✅ *Self-check:* o compose lê `${POSTGRES_PASSWORD:-curso}` e o `.env` é ignorado pelo git.

> ⚠️ **Nunca** `ENV SENHA=...` nem `COPY .env` na imagem — fica gravado nas camadas (vazamento).

---

## 3. Tag e registry (build → tag → push)
Uma referência de imagem é `registry/nome:tag`. Taggeie a imagem do Lab 01:
```bash
docker tag curso-app:1.0 ghcr.io/SEU_USUARIO/curso-app:1.0.0
docker image inspect ghcr.io/SEU_USUARIO/curso-app:1.0.0 --format '{{.RepoTags}}'
```
✅ *Self-check:* a nova tag aparece. Para publicar (opcional, exige login no registry):
```bash
# echo $TOKEN | docker login ghcr.io -u SEU_USUARIO --password-stdin
# docker push ghcr.io/SEU_USUARIO/curso-app:1.0.0
```
> Pine a tag (`1.0.0`), não use `latest` em produção.

---

## O que você levou daqui
Configurou por **env** (sem rebuild), viu o **.env** ignorado (segredo fora da imagem) e
**taggeou** uma imagem no formato `registry/nome:tag`. Fixe a lógica nos
[Exercícios 05](exercicio-05.md) e [06](exercicio-06.md).

---
**Revisado em:** 2026-08-29
