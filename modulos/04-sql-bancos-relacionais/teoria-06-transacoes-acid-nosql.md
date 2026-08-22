# Transações, ACID e NoSQL: garantias e alternativas

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Imagine transferir dinheiro: debitar de uma conta e creditar em outra. Se o sistema cair
**no meio**, o dinheiro não pode sumir nem duplicar. Bancos relacionais resolvem isso com
**transações** e as garantias **ACID**. E, para casos onde o modelo relacional não é ideal,
existe o mundo **NoSQL**. Entender essas garantias (e quando abrir mão delas) é fundamento de
engenharia de dados.

## 💡 Conceito (o porquê)

### Transação: tudo ou nada
Uma **transação** agrupa operações que devem acontecer **juntas**:
```sql
BEGIN;
UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
UPDATE contas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;   -- confirma as duas; ROLLBACK desfaz tudo
```
Se algo falhar antes do `COMMIT`, um `ROLLBACK` volta tudo ao estado inicial — nunca fica "pela metade".

### ACID — as quatro garantias
- **A — Atomicidade:** tudo ou nada (a transação inteira ou nenhuma parte).
- **C — Consistência:** a transação leva o banco de um estado válido a outro (respeita regras/constraints).
- **I — Isolamento:** transações concorrentes não se atrapalham (como se fossem sequenciais).
- **D — Durabilidade:** depois do `COMMIT`, o dado sobrevive a quedas de energia/falhas.

Isso é o que torna o banco relacional confiável para dados críticos (a fonte da verdade
transacional — o **OLTP** do M01).

### NoSQL — quando e por quê
"NoSQL" reúne bancos **não relacionais**, cada um para um formato/uso:
- **Documento** (MongoDB): JSON flexível, schema livre.
- **Chave-valor** (Redis): acesso ultrarrápido por chave (cache, sessões).
- **Colunar wide** (Cassandra): escrita massiva distribuída.
- **Grafo** (Neo4j): relações complexas (redes, recomendações).

O trade-off central: muitos NoSQL trocam parte das garantias ACID por **escala horizontal**
e **flexibilidade de schema** (o teorema **CAP**: sob partição de rede, escolhe-se entre
consistência e disponibilidade). Não é "melhor" nem "pior" — é **adequação ao caso**.

## 🔎 Exemplo — rollback salva o dia
```sql
BEGIN;
INSERT INTO pedidos VALUES (99, 'SP', 'livros', 10, 1);
-- opa, valor errado!
ROLLBACK;   -- o pedido 99 nunca existiu
```

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann analisa em profundidade as garantias transacionais e os níveis de isolamento,
mostrando que "ACID" tem nuances (especialmente o **I**) e que sistemas distribuídos fazem
trade-offs explícitos entre consistência e disponibilidade. — *Designing Data-Intensive Applications*, cap. 7.
:::

## ⚠️ Erros comuns
- Achar que operações soltas são atômicas — sem transação, uma pode falhar e a outra não.
- Confundir **consistência** do ACID (regras do banco) com a "consistência" do teorema CAP (distribuída).
- Escolher NoSQL "porque é moderno", sem necessidade real de escala/flexibilidade — perdendo ACID à toa.
- Ignorar **isolamento** e ter condições de corrida entre transações concorrentes.

## 💼 O que o mercado espera
Saber explicar ACID, quando usar transações, e ter noção de **quando** um NoSQL faz sentido
(e o que se troca). Perguntas conceituais assim são comuns em entrevistas.

:::{admonition} ✨ Em resumo
:class: resumo
- **Transação** = tudo ou nada (`BEGIN … COMMIT`/`ROLLBACK`).
- **ACID** = Atomicidade, Consistência, Isolamento, Durabilidade — confiabilidade do relacional.
- **NoSQL** (documento/chave-valor/colunar/grafo) troca parte do ACID por escala/flexibilidade.
- Escolha pela **adequação ao caso**, não pela moda (lembre do teorema CAP).
:::

## 🧠 Quiz de recall
1. O que significa a "Atomicidade" do ACID?
   :::{dropdown} Resposta
   Uma transação é indivisível: ou todas as suas operações se aplicam, ou nenhuma (via `COMMIT`/`ROLLBACK`). Nunca fica "pela metade".
   :::
2. Cite dois tipos de banco NoSQL e um uso típico de cada.
   :::{dropdown} Resposta
   Ex.: documento (MongoDB) para dados JSON flexíveis; chave-valor (Redis) para cache/sessões; colunar wide (Cassandra) para escrita distribuída; grafo (Neo4j) para relações complexas.
   :::
3. Qual o trade-off central ao escolher muitos bancos NoSQL?
   :::{dropdown} Resposta
   Trocar parte das garantias ACID (sobretudo consistência forte) por escala horizontal e flexibilidade de schema — decisão guiada pelo caso de uso (e pelo teorema CAP sob partição).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "O que são as propriedades ACID?"
  :::{dropdown} Resposta modelo
  Atomicidade (tudo ou nada), Consistência (respeita as regras do banco), Isolamento (transações concorrentes não interferem) e Durabilidade (após COMMIT, o dado persiste mesmo com falha). São as garantias que tornam o relacional confiável para dados críticos.
  :::
- **P:** "Quando você escolheria um banco NoSQL em vez de um relacional?"
  :::{dropdown} Resposta modelo
  Quando o caso pede escala horizontal massiva, schema muito flexível/variável, ou padrões de acesso específicos (cache por chave, grafo de relações) que o relacional não atende bem — aceitando conscientemente o trade-off nas garantias. Para dados transacionais críticos com relações, o relacional (ACID) costuma vencer.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications**, cap. 7 (transações) e cap. 9 (consistência/consenso).
- **Docs do PostgreSQL** — Transactions; e material introdutório sobre o teorema CAP.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (O'Reilly, 2017) — cap. 7 e 9. <!-- @kleppmann2017 -->
- PostgreSQL. *Documentação oficial* — [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html). <!-- @docs-postgres -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
