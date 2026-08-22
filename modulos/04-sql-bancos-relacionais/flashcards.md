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
- **P:** INNER JOIN vs LEFT JOIN? / **R:** INNER só as linhas que casam nos dois lados; LEFT todas as da esquerda + NULL onde não há par.
- **P:** O que causa produto cartesiano? / **R:** JOIN sem `ON` (ou condição errada) — combina cada linha com todas da outra tabela, explodindo linhas.
- **P:** COUNT(*) vs COUNT(coluna)? / **R:** COUNT(*) conta linhas; COUNT(coluna) ignora NULLs dessa coluna.
- **P:** O que é uma CTE (WITH)? / **R:** Um resultado intermediário nomeado; melhora legibilidade em consultas de várias etapas.
- **P:** Window function vs GROUP BY? / **R:** GROUP BY colapsa grupos em uma linha; window (`OVER`) calcula sobre o grupo mantendo todas as linhas.
- **P:** ROW_NUMBER vs RANK? / **R:** ROW_NUMBER = 1,2,3 sem empate; RANK empata e pula (1,1,3); DENSE_RANK empata sem pular (1,1,2).
- **P:** Como pegar "top 1 por grupo" com window? / **R:** ROW_NUMBER() OVER (PARTITION BY grupo ORDER BY metrica DESC) numa CTE e filtrar = 1.
- **P:** O que é um índice e seu custo? / **R:** Acelera leituras por uma coluna (evita full scan) ao custo de escritas mais lentas e espaço; use seletivamente.
- **P:** Para que serve EXPLAIN? / **R:** Mostra o plano de execução (scan vs índice, joins, custos) para diagnosticar/otimizar.
- **P:** O que é ACID? / **R:** Atomicidade, Consistência, Isolamento, Durabilidade — garantias das transações relacionais.
- **P:** Quando usar NoSQL? / **R:** Quando o caso pede escala horizontal, schema flexível ou padrões de acesso específicos — aceitando trade-off no ACID (teorema CAP).

---
**Revisado em:** 2026-08-22
