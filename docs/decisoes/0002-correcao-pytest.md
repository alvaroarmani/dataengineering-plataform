# ADR 0002 — Correção via "faça o pytest passar"

- **Status:** Aceito
- **Data:** 2026-08-20

## Contexto

Precisamos corrigir atividades automaticamente, num curso autodirigido (sem instrutor).
Correção com `assert` visível é simples, mas fraca: o aluno vê a resposta esperada e não
exercita uma habilidade real.

## Decisão

Adotar o padrão **"faça o `pytest` passar"** como forma principal de correção: o
exercício é uma pasta com código a completar (`solucao.py`) e uma suíte de testes
(`tests/test_*.py`); a tarefa é rodar `pytest -q` até tudo ficar verde. Para checagens
rápidas de fundamentos **no navegador** (JupyterLite), usa-se uma função `verificar()`
com `assert` que imprime ✅/❌ + dica.

## Consequências

- ✅ Ensina uma habilidade real de DE (ler testes, TDD, interpretar falhas).
- ✅ Feedback objetivo e reproduzível; funciona local e em CI.
- ⚠️ Exige escrever boas suítes de teste (parte do trabalho de autoria).
- ⚠️ `verificar()` no browser é mais fraco — reservado a fundamentos, não a projetos.
