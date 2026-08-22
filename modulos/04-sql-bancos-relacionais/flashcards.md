# Flashcards — Módulo 04

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que é chave primária (PK) e estrangeira (FK)? / **R:** PK identifica cada linha de forma única; FK aponta para a PK de outra tabela, ligando-as (integridade referencial).
- **P:** Estrutura básica do SELECT? / **R:** `SELECT colunas FROM tabela WHERE filtro GROUP BY ... ORDER BY ... LIMIT n`.
- **P:** WHERE vs HAVING? / **R:** WHERE filtra linhas antes de agrupar; HAVING filtra grupos depois do GROUP BY.
- **P:** Ordem lógica de execução do SELECT? / **R:** FROM → WHERE → GROUP BY → SELECT → ORDER BY → LIMIT (diferente da ordem escrita).
- **P:** Como agregar por grupo? / **R:** `GROUP BY coluna` com funções de agregação (COUNT, SUM, AVG, MIN, MAX).
- **P:** Por que `coluna = NULL` não funciona? / **R:** NULL é "desconhecido"; comparações com `=` dão NULL. Use `IS NULL` / `IS NOT NULL`.
- **P:** Sem `ORDER BY`, a ordem é garantida? / **R:** Não — a ordem das linhas não é garantida sem `ORDER BY` explícito.
- **P:** Por que SQL é "declarativo"? / **R:** Você diz o que quer (resultado); o otimizador do banco decide como executar (plano, índices).
- **P:** `DISTINCT` faz o quê? / **R:** Remove linhas duplicadas do resultado.

---
**Revisado em:** 2026-08-22
