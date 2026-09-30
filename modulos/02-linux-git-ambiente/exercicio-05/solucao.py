"""Exercício 05 (M2) — Imagem, container e volume: o que sobrevive? (simulador).

Você vai simular uma sequência de comandos no estilo Docker e responder, no fim, o que existe
e ONDE cada arquivo foi parar. Rode `pytest -q`.

Comandos (strings, separadas por espaço):
    "pull IMG"                       -> a imagem passa a existir localmente
    "run CONT IMG"                   -> cria o container CONT a partir de IMG
    "run CONT IMG -v VOL:/dados"     -> idem, montando o volume VOL em /dados (cria VOL se não existir)
    "escrever CONT CAMINHO"          -> o processo do container grava um arquivo em CAMINHO
    "rm CONT"                        -> remove o container
    "rmi IMG"                        -> remove a imagem
    "volume rm VOL"                  -> remove o volume
"""


def simular(comandos: list) -> dict:
    """Execute os comandos em ordem e retorne:
        {"imagens": [...], "containers": [...],            # listas ordenadas
         "volumes": {VOL: [arquivos...]},                  # arquivos ordenados
         "camadas": {CONT: [arquivos...]}}                 # camada gravável de cada container vivo

    Regras:
      - run: a imagem precisa existir; o nome do container precisa ser novo.
      - escrever: se o container tem volume e CAMINHO começa com "/dados/", o arquivo vai para o
        VOLUME; caso contrário, vai para a CAMADA do container.
      - rm: remove o container e a camada dele (o volume continua existindo, com os arquivos).
      - rmi: proibido se algum container existente usa a imagem.
      - volume rm: proibido se algum container existente monta o volume.
      - Qualquer violação, comando desconhecido ou alvo inexistente -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
