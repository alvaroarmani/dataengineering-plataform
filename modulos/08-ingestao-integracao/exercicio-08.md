# Exercício 08 — Consumo por offset: lotes, retenção e auto.offset.reset

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um consumidor de Kafka (teoria 04) lê um log a partir de um **offset** e avança. Na prática, três
detalhes aparecem logo: ele lê em **lotes** (`max.poll.records`), o log tem **retenção** — mensagens
antigas são apagadas, e o log passa a começar num offset maior que zero — e, se o consumidor ficou parado
tempo demais, o offset salvo dele **não existe mais**. O que fazer aí é configuração:
`auto.offset.reset = earliest` (volta para a mais antiga disponível, perdendo o que foi apagado),
`latest` (pula para o fim, perdendo tudo que estava pendente) ou `none` (erro — alguém decide).

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `poll(log, inicio_log, offset, max_msgs, reset)`.

```bash
cd modulos/08-ingestao-integracao/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — offsets absolutos
A mensagem de offset `o` está em `log[o - inicio_log]`. O fim do log é `inicio_log + len(log)`.
:::
:::{dropdown} Dica 2 — o reset
Só entra em cena se `offset < inicio_log`. Calcule as perdidas como a distância entre o offset pedido e o ponto de onde a leitura vai continuar.
:::
:::{dropdown} Dica 3 — o lote
Fatie no máximo `max_msgs` a partir do ponto de leitura; o próximo offset avança pelo número de mensagens lidas.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def poll(log: list, inicio_log: int, offset: int, max_msgs: int = 500, reset: str = "earliest") -> dict:
    if max_msgs < 1:
        raise ValueError("max_msgs deve ser >= 1")
    fim = inicio_log + len(log)
    if offset > fim:
        raise ValueError(f"offset {offset} além do fim do log ({fim})")
    perdidas = 0
    if offset < inicio_log:
        if reset == "earliest":
            perdidas, offset = inicio_log - offset, inicio_log
        elif reset == "latest":
            perdidas, offset = fim - offset, fim
        else:
            raise ValueError(f"offset {offset} fora da retenção (início {inicio_log})")
    ini = offset - inicio_log
    msgs = log[ini:ini + max_msgs]
    return {"mensagens": msgs, "proximo_offset": offset + len(msgs), "perdidas": perdidas}
```
O consumidor que parou no offset 95 perdeu 5 mensagens para a retenção — e com `latest` perderia 15,
incluindo as 10 que **ainda estavam** no log. Nenhuma das duas perdas gera erro: o consumidor
simplesmente segue. Por isso, em pipelines de dados, `auto.offset.reset = none` (ou monitorar o lag
contra a retenção, M17) costuma ser a escolha mais segura: melhor um alerta que uma lacuna silenciosa.

O `max_msgs` é o que mantém cada iteração do consumidor previsível: se o processamento de um lote passar
do `max.poll.interval.ms`, o broker considera o consumidor morto e rebalanceia o grupo — lotes menores
evitam esse ciclo de rebalanceamentos.
:::

---
**Revisado em:** 2026-09-30
