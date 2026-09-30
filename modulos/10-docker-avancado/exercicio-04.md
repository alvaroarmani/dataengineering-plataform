# Exercício 04 — Rede do Compose: quem alcança quem (e em qual porta)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
As duas confusões mais comuns com redes de containers (teoria 02):

1. **`localhost` dentro do container** é o próprio container, não o seu computador nem o banco. De um
   container, o banco se chama pelo **nome do serviço** (`postgres:5432`), desde que os dois estejam na
   **mesma rede**.
2. **Porta publicada x porta interna:** `5433:5432` publica o banco na porta 5433 **do host**. Do seu
   computador, você usa `localhost:5433`; de outro container da rede, continua sendo `postgres:5432`.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `alcanca(servicos, origem, endereco)`.

```bash
cd modulos/10-docker-avancado/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — separe nome e porta
`endereco.rsplit(":", 1)` e `int(porta)` (uma porta não numérica já levanta `ValueError`).
:::
:::{dropdown} Dica 2 — do host
Só `localhost` funciona, e a porta tem de ser uma das **publicadas** de algum serviço.
:::
:::{dropdown} Dica 3 — de um container
`localhost` é ele mesmo. Para outro serviço: precisa existir, ter rede em comum e a porta precisa ser a **interna**.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def alcanca(servicos: dict, origem: str, endereco: str) -> tuple:
    nome, porta = endereco.rsplit(":", 1)
    porta = int(porta)
    if origem == "host":
        if nome != "localhost":
            return (False, "host_nao_resolve_nome")
        for s, cfg in sorted(servicos.items()):
            if porta in cfg.get("publica", []):
                return (True, s)
        return (False, "porta_errada")
    if nome == "localhost":
        if servicos[origem]["porta"] == porta:
            return (True, origem)
        return (False, "localhost_no_container")
    if nome not in servicos:
        return (False, "servico_inexistente")
    if not set(servicos[origem]["redes"]) & set(servicos[nome]["redes"]):
        return (False, "sem_rede_em_comum")
    if servicos[nome]["porta"] != porta:
        return (False, "porta_errada")
    return (True, nome)
```
A linha `("airflow", "postgres:5433")` é o erro que todo mundo comete uma vez: copiar a porta do
`docker-compose.yml` (`5433:5432`) para a string de conexão do Airflow. Dentro da rede, a porta
publicada não existe — é a 5432, do próprio container.

Já o `metabase` não alcança o banco porque está só na rede `frontend`: é **segmentação** de propósito —
a ferramenta de BI fala com a API, e o banco fica isolado na rede de backend. Redes do Compose são a
versão de bancada do que no Kubernetes são as *NetworkPolicies* (M20) e, na nuvem, as sub-redes privadas.
:::

---
**Revisado em:** 2026-09-30
