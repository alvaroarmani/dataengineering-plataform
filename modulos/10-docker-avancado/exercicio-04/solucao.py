"""Exercício 04 (M10) — Rede do Compose: quem alcança quem (e em qual porta).

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def alcanca(servicos: dict, origem: str, endereco: str) -> tuple:
    """servicos = {nome: {"redes": [...], "porta": porta interna, "publica": [porta_host, ...]}}.
    origem = "host" (o seu computador) ou o nome de um serviço. endereco = "nome_ou_localhost:porta".
    Retorne (True, destino) ou (False, motivo), com motivo em:
      "localhost_no_container"  origem é container e o endereço é localhost (aponta para ele mesmo;
                                a menos que ele mesmo escute nessa porta: aí (True, origem))
      "sem_rede_em_comum"       container -> container sem rede compartilhada
      "porta_errada"            porta diferente da interna (container->container) ou não publicada (host)
      "host_nao_resolve_nome"   do host, nomes de serviço não resolvem (use localhost + porta publicada)
      "servico_inexistente"
    Do host: "localhost:P" alcança o serviço que publica P."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
