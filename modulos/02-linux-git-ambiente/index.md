# Módulo 02 — Linux, Git e Ambiente de Desenvolvimento

> Ao final, você domina o terminal, versiona código com Git e sobe o ambiente do curso com Docker.

## Perguntas essenciais
Ao final deste módulo, você saberá responder:
1. Por que automatizar pelo terminal e versionar com Git em vez de "salvar e clicar"?
2. Qual a diferença entre imagem, container e volume — e por que isso importa?
3. Como você organiza commits e branches para colaborar sem se atrapalhar?

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 20h
- **Pré-requisitos:** M01
- **Onde roda:** Bancada Docker + terminal local

## Ementa
Linha de comando (Linux/WSL): navegação, arquivos, permissões, pipes e redirecionamentos.
Controle de versão com Git: commits, branches, merge, resolução de conflitos, fluxo com
GitHub. Introdução a containers com Docker (imagens, containers, volumes) e uso do
`docker-compose` para subir a bancada do curso.

## Competências e habilidades
- C3 — operar Linux/CLI, Git e ambientes containerizados.

## Objetivos de aprendizagem
1. **Executar** tarefas comuns no terminal (arquivos, busca, pipes).
2. **Versionar** um projeto com Git e publicá-lo no GitHub.
3. **Subir** a bancada Docker e entender imagem × container × volume.

## Plano de aulas (unidades)
1. **Teoria:** [Terminal, Git e containers](teoria-01-terminal-git-containers.md)
2. **Lab:** [Montando a bancada e seu primeiro commit](lab-01-montando-a-bancada.md)
3. **Exercício:** [O que o `.gitignore` ignora](exercicio-01.md)
4. **Revisão:** [Flashcards](flashcards.md)

## Metodologia e avaliação
**Maestria:** publicar um repositório no GitHub + subir a bancada Docker + `pytest` verde
num exercício de scripting.

## O que o mercado espera
Git e terminal são pré-requisito silencioso de toda vaga. Docker aparece na maioria das
vagas Jr/Pleno de dados.

## Erros comuns
- Commits gigantes e sem mensagem clara.
- Versionar segredos (`.env`) ou dados grandes.
- Confundir imagem com container.

## Recursos
A curar em `recursos.md` (Pro Git book; docs do Docker; missing-semester do MIT).

---
**Revisado em:** 2026-08-20
