# Lab 01 — Montando a bancada e seu primeiro commit

**Onde roda:** 🐳 Bancada Docker + terminal local (não é notebook — é o mundo real).

Objetivo: subir o ambiente do curso e versionar seu primeiro trabalho. Ao final você terá a
bancada rodando e um commit no GitHub.

## 1. Suba a bancada Docker

```bash
cd ambiente
cp .env.example .env
docker compose up -d
docker compose ps          # os serviços estão "running"?
```

Abra o JupyterLab em <http://localhost:8888> (token no `.env`) e o console do MinIO em
<http://localhost:9001>. Detalhes em [ambiente/README](../../ambiente/README.md).

## 2. Explore o terminal (aquecimento)

```bash
pwd                        # onde estou?
ls -la                     # o que há aqui (inclui ocultos)?
mkdir -p pratica/dia1 && cd pratica/dia1
echo "linha 1" > notas.txt
echo "linha 2" >> notas.txt
cat notas.txt | wc -l      # quantas linhas? (pipe!)
```

## 3. Versione com Git

```bash
git init                          # se ainda não for um repo
git checkout -b meu-primeiro-lab
echo ".env" >> .gitignore         # nunca versione segredos
git add pratica/dia1/notas.txt .gitignore
git commit -m "chore: primeiro commit do lab de ambiente"
```

Crie um repositório vazio no GitHub e conecte:

```bash
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin meu-primeiro-lab
```

## 4. Derrube a bancada (quando terminar)

```bash
cd ambiente && docker compose down     # mantém os dados (volumes)
```

## Checklist de conclusão
- [ ] `docker compose ps` mostra os serviços rodando.
- [ ] Consegui abrir o JupyterLab no navegador.
- [ ] Fiz um commit e um `push` para o GitHub.
- [ ] Meu `.gitignore` impede versionar o `.env`.

> **Destravou?** Se `docker compose up` falhar, cheque se o Docker Desktop está aberto e,
> no Windows, se o WSL2 está ativo (ver [Infraestrutura](../../ppc/infraestrutura-e-ambiente.md)).

---
**Revisado em:** 2026-08-21
