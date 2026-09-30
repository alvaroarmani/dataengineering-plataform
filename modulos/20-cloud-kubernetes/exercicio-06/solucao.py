"""Exercício 06 (M20) — Service discovery: como o DNS do cluster resolve nomes.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


SUFIXO = "svc.cluster.local"


def resolver(nome: str, namespace_origem: str, servicos: dict) -> str:
    """servicos = {(servico, namespace): cluster_ip}. Regras (como o DNS do cluster):
      - "a.b.svc.cluster.local" (completo): serviço a no namespace b
      - "a.b" (dois rótulos): serviço a no namespace b
      - "a" (um rótulo): serviço a no namespace de ORIGEM (não procura em outros namespaces)
    Retorne o IP. Nome inexistente -> KeyError (NXDOMAIN); nome vazio ou com outro formato -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
