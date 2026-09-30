# Exercício 05 — Roteamento de leitura: réplica ou líder?

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Replicação líder–seguidores (teoria 02) permite espalhar **leituras** pelas réplicas — mas elas
estão sempre um pouco atrasadas. O roteador de leitura precisa decidir, a cada consulta, se alguma
réplica serve: ela não pode estar atrasada demais (limite de lag) e, para a garantia
**read-your-writes**, precisa já ter recebido a última escrita **deste** cliente. Senão, o usuário
salva o perfil, recarrega a página e vê o dado antigo.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `escolher_no_de_leitura(offset_lider, replicas, lag_max, ultima_escrita_cliente)`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — lag
`lag = offset_lider - offset_replica`. Um offset maior que o do líder é impossível numa replicação saudável — trate como erro.
:::
:::{dropdown} Dica 2 — duas condições
Elegível: `lag <= lag_max` **e** `offset >= ultima_escrita_cliente`. A segunda é a garantia read-your-writes.
:::
:::{dropdown} Dica 3 — escolha e fallback
Guarde tuplas `(lag, nome)` e use `min` (desempata pelo nome). Lista vazia → `"lider"`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def escolher_no_de_leitura(offset_lider: int, replicas: dict, lag_max: int, ultima_escrita_cliente: int = 0) -> str:
    elegiveis = []
    for nome, off in replicas.items():
        if off > offset_lider:
            raise ValueError(f"réplica {nome} à frente do líder")
        lag = offset_lider - off
        if lag <= lag_max and off >= ultima_escrita_cliente:
            elegiveis.append((lag, nome))
    return min(elegiveis)[1] if elegiveis else "lider"
```
O teste de read-your-writes mostra que "a réplica menos atrasada" não basta: a `r1` está só 10
offsets atrás, mas ainda não tem a escrita 995 do próprio cliente. Mandar a leitura para ela
mostraria ao usuário o dado de antes do "salvar". O roteador cai no líder — mais carga nele, mas
correto.

Em bancos gerenciados, isso aparece como opções de consistência por sessão (sessões "causais" no
MongoDB, leitura no primário após escrita em proxies de Postgres). Em pipelines de dados, a mesma
ideia vale ao ler de uma réplica de leitura para extração: a extração incremental precisa saber
até que offset a réplica já chegou (M08, CDC).
:::

---
**Revisado em:** 2026-09-30
