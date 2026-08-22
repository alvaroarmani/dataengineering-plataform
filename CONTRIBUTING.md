# Guia de Autoria

Como o conteúdo do curso é criado e mantido — para que **todo módulo saia consistente**.

## Princípios

1. **Ensine o *porquê*, linke o *como* volátil.** Conceitos são estáveis; APIs de dbt/Airflow/BigQuery mudam. Explique o conceito e aponte para a **doc oficial** para detalhes de versão.
2. **Prática obrigatória.** Toda unidade termina com algo que roda (lab) e algo que se corrige sozinho (exercício `pytest` ou `verificar()`).
3. **Datasets reais.** Nada de `dados_ficticios.csv`. Use os do [`datasets/`](datasets/README.md).
4. **Datar tudo.** Toda página tem `Revisado em: AAAA-MM-DD`.
5. **Documentação viva.** Mudou arquitetura/decisão? Atualize `ARCHITECTURE.md` e/ou abra um ADR em `docs/decisoes/`.

## Padrão de referências (imposto pelo linter)

Toda teoria é sempre referenciada, e `scripts/verificar-conteudo.py` verifica isto (roda no CI).

- Declare o **tipo** no topo da página: `<!-- tipo: conceitual | pratico | ferramenta -->`.
- Cite **apenas** obras do registro [`referencias.yaml`](referencias.yaml); marque cada referência com a chave: `- Autor, *Título* ... <!-- @chave -->`. **Fonte fora do registro reprova.** Falta uma obra? Adicione-a ao registro primeiro (dados verificados).
- **Nunca invente** citações/páginas. Paráfrase fiel + citação precisa (autor, livro, capítulo); verbatim só de fonte aberta; ≥1 fonte aberta por conceito central.
- Rode antes de commitar: `python scripts/verificar-conteudo.py` (adicione `--check-links` para testar URLs).

## Criando um módulo

Use a skill de projeto **`autoria-modulo`** (em `.claude/skills/autoria-modulo/`). Ela
codifica este padrão. A estrutura de um módulo:

```
modulos/NN-nome/
├── index.md            # ementa MEC (a partir de templates/template-modulo.md)
├── teoria-NN-*.md      # páginas de leitura (template-teoria.md)
├── lab-NN-*.ipynb      # lab guiado (declara onde roda)
├── exercicio-NN/       # "faça o pytest passar" (template-exercicio/)
├── recursos.md         # livros, papers, vídeos, docs oficiais
└── flashcards.md       # revisão espaçada
```

## Fluxo de autoria: editar → salvar no arquivo → publicar

O site publicado (GitHub Pages / JupyterLite) é **só para consumir** — o que se digita nos
notebooks do site vive apenas no navegador (IndexedDB) e **não** volta para o repositório
(limite de site estático, ver [ADR 0001](docs/decisoes/0001-jupyter-book.md)).

**Para editar de verdade e persistir no arquivo, use o JupyterLab da bancada Docker**, que
monta o repositório dentro do container (`../:/home/jovyan/curso` no
`ambiente/docker-compose.yml`). O loop:

```{mermaid}
flowchart LR
    A[Editar no JupyterLab Docker<br/>em /home/jovyan/curso] -->|salva DIRETO| B[Arquivo .ipynb/.md no repo]
    B --> C[jupyter-book build .<br/>preview local]
    B --> D[git commit + push]
    D --> E[GitHub Actions rebuilda]
    E --> F[Site publicado atualizado]
```

Passo a passo:

1. `cd ambiente && docker compose up -d` e abra o JupyterLab em `http://localhost:8888`.
2. No JupyterLab, navegue até `curso/` e edite os notebooks/páginas — **cada save grava no arquivo real** do repositório (é o mesmo arquivo que o site renderiza).
3. Rebuild local para conferir: `./.venv/Scripts/jupyter-book.exe build .` (Windows) ou `jupyter-book build .`.
4. `git add -p && git commit && git push` → o workflow `deploy.yml` reconstrói e publica.

> **Regra:** conteúdo novo/edição sempre pelo JupyterLab (ou editor de arquivos) — nunca
> "salvando" pelo JupyterLite do site, que não persiste.

## Padrão de correção

- **Exercício sério:** pasta com `enunciado.md`, `solucao.py` (com `# SEU CÓDIGO AQUI`) e `tests/test_*.py`. Meta: `pytest -q` verde.
- **Checagem rápida no browser:** função `verificar(resposta)` que imprime ✅/❌ + dica (roda no JupyterLite).
- **Dicas progressivas:** ofereça *hint ladders* (dica 1 → dica 2 → solução) em `<details>`.
- **Solução comentada:** liberada **depois** de passar, explicando o raciocínio.

## Nomenclatura

- Pastas e arquivos em `kebab-case`, sem acento.
- Módulos numerados `01`..`15` (o TCC vive em `tcc/`).
- Notebooks: `lab-NN-descricao.ipynb`, `exercicio-NN/`.

## Critério de "pronto" (Definition of Done) de uma unidade

- [ ] Teoria com o *porquê* + referências datadas.
- [ ] Lab que roda (declara browser vs Docker).
- [ ] Exercício com correção automática + hint ladder + solução comentada.
- [ ] Flashcards adicionados ao baralho do módulo.
- [ ] Critério de maestria refletido no `index.md` e no `progresso.md`.
- [ ] `jupyter-book build .` sem novos warnings.
