# Lab 01 — Kafka na bancada: produza e consuma eventos

**Onde roda:** 🐳 Bancada Docker (Kafka real, profile `kafka`). É o lab que dá corpo à
[teoria 02](teoria-02-kafka-topicos-particoes.md): tópicos, partições, offsets e consumer groups
com um broker de verdade.

> Pré-requisito: bancada de pé e engine estável (`bash ambiente/validar-bancada.sh`).

## 1. Suba o Kafka
```bash
cd ambiente
docker compose --profile kafka up -d
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## 2. Crie um tópico com 3 partições
```bash
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --create --topic pedidos --partitions 3 --replication-factor 1
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --describe --topic pedidos
```
✅ Você deve ver **3 partições** (0, 1, 2), cada uma com seu líder.

## 3. Produza eventos COM chave (ordem por cliente)
A chave decide a partição — a mesma chave cai sempre na mesma partição (ordem por cliente).
```bash
docker compose --profile kafka exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 --topic pedidos \
  --property parse.key=true --property key.separator=:
```
Digite (⏎ após cada linha; `Ctrl+C` para sair):
```
cliente-42:pedido 1001
cliente-7:pedido 1002
cliente-42:pedido 1003
```

## 4. Consuma do início (releitura do histórico)
```bash
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic pedidos --from-beginning \
  --property print.key=true --property print.partition=true --timeout-ms 5000
```
✅ Observe que **os dois eventos do `cliente-42` saem na mesma partição** (ordem preservada),
enquanto o `cliente-7` pode cair em outra. Ler **não apaga** — é um log, não uma fila.

## 5. Consumer group: paralelismo e lag
```bash
# consome como grupo "faturamento" (deixe rodando alguns segundos e Ctrl+C)
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic pedidos --group faturamento --timeout-ms 5000

# inspecione offsets e LAG por partição do grupo
docker compose --profile kafka exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 --describe --group faturamento
```
✅ A saída mostra, por partição, `CURRENT-OFFSET`, `LOG-END-OFFSET` e **`LAG`** — exatamente o que
você calculou no [Exercício 04](exercicio-04.md). Um segundo `--group antifraude` receberia **todos**
os eventos de novo (grupos diferentes são independentes).

## 6. Derrube
```bash
docker compose --profile kafka down    # (ou `down -v` para apagar os dados do Kafka)
```

## O que você praticou
- Criou um **tópico particionado** e viu a ordem **por partição**.
- Produziu com **chave** e confirmou `chave → mesma partição` (ordem por entidade).
- Releu o **log** do início e mediu o **lag** de um **consumer group**.

---
**Revisado em:** 2026-08-31
