"""Exercício 03 (M1) — Validar a ordem das etapas de um pipeline.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


FASES = ["geracao", "ingestao", "armazenamento", "transformacao", "disponibilizacao"]
CORRENTES = {"seguranca", "gestao_de_dados", "dataops", "arquitetura", "orquestracao", "engenharia_de_software"}


def validar_pipeline(etapas: list) -> dict:
    """etapas = [(nome_da_etapa, fase)] na ordem em que o pipeline as executa.
    Retorne:
      {"ok": não há etapas fora de ordem nem fases faltando entre ingestao e disponibilizacao,
       "fora_de_ordem": [nomes das etapas cuja fase vem ANTES da fase de alguma etapa anterior],
       "fases_ausentes": [fases de ingestao até disponibilizacao sem nenhuma etapa, na ordem do ciclo],
       "ordem_correta": [nomes reordenados pela fase, mantendo a ordem original dentro da mesma fase]}
    Uma fase que é corrente de fundo -> ValueError com mensagem explicando; fase desconhecida -> ValueError.
    (geracao pode faltar: muitas vezes a fonte é de outro time.)"""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
