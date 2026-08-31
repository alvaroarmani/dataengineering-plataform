# Lab 01 — MongoDB na bancada: documentos e agregação

**Onde roda:** 🐳 Bancada Docker (MongoDB real, profile `nosql`). Dá corpo à
[teoria 02](teoria-02-documento-keyvalue.md): documentos, consulta e o pipeline de agregação.

> Pré-requisito: engine estável (`bash ambiente/validar-bancada.sh`).

## 1. Suba o MongoDB (e o Redis)
```bash
cd ambiente
docker compose --profile nosql up -d
docker compose --profile nosql exec mongo mongosh --quiet --eval "db.runCommand({ ping: 1 })"
```

## 2. Abra o shell e insira documentos
```bash
docker compose --profile nosql exec mongo mongosh loja
```
No `mongosh` (banco `loja`):
```javascript
db.produtos.insertMany([
  { nome: "Camiseta", categoria: "roupas", preco: 49.9, tamanhos: ["P","M","G"] },
  { nome: "Caneca",   categoria: "casa",   preco: 29.9 },
  { nome: "Boné",     categoria: "roupas", preco: 39.9, cor: "azul" }
])
```
Note que os documentos têm **campos diferentes** (esquema flexível): `tamanhos`, `cor` só onde fazem sentido.

## 3. Consulte (find) — inclusive por subestrutura
```javascript
db.produtos.find({ categoria: "roupas" })              // todos de roupas
db.produtos.find({ preco: { $lt: 40 } })               // preço < 40
db.produtos.find({ tamanhos: "G" })                    // que têm tamanho G (dentro do array)
```

## 4. Índice (NoSQL também precisa!)
```javascript
db.produtos.createIndex({ categoria: 1 })
db.produtos.find({ categoria: "roupas" }).explain("executionStats").executionStats.totalDocsExamined
```
✅ Com o índice, a consulta por `categoria` não varre a coleção inteira.

## 5. Pipeline de agregação (o "GROUP BY" do documento)
Preço médio por categoria:
```javascript
db.produtos.aggregate([
  { $group: { _id: "$categoria", preco_medio: { $avg: "$preco" }, itens: { $sum: 1 } } },
  { $sort: { preco_medio: -1 } }
])
```
✅ É o análogo de `SELECT categoria, AVG(preco), COUNT(*) ... GROUP BY categoria ORDER BY 2 DESC` —
o estágio `$group` faz o papel do `GROUP BY` (compare com o [Exercício 02](exercicio-02.md)).

## 6. (Opcional) Redis: cache com TTL
```bash
docker compose --profile nosql exec redis redis-cli SET sessao:42 "carrinho" EX 30
docker compose --profile nosql exec redis redis-cli TTL sessao:42   # segundos restantes
docker compose --profile nosql exec redis redis-cli GET sessao:42
```
✅ A chave `sessao:42` **expira sozinha** em 30s (TTL) — o comportamento do [Exercício 03](exercicio-03.md).

## 7. Derrube
```bash
docker compose --profile nosql down     # (ou `down -v` para apagar os dados)
```

## O que você praticou
- Inseriu **documentos** com esquema flexível e consultou por campo/array.
- Criou **índice** e viu o efeito no plano de execução.
- Rodou um **pipeline de agregação** (o GROUP BY do documento).
- Usou **TTL** no Redis (cache que expira sozinho).

---
**Revisado em:** 2026-08-31
