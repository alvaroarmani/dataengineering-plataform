# Exercício 06 — Revisar um documento de design: as correntes de fundo

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No system design (teoria 03), quem só desenha as caixas (fonte → Kafka → Spark → warehouse) deixa de
fora o que diferencia um sênior: as **correntes de fundo** — qualidade, segurança, observabilidade,
custo e idempotência. O entrevistador vai perguntar sobre elas; melhor já trazê-las.

Você vai escrever um revisor de documentos de design: ele procura sinais de cada corrente no texto
(sinônimos, com e sem acento) e, para cada uma que falta, devolve a **pergunta** que o entrevistador
faria.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `revisar_design(texto)`.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — normalize
Tire acentos e passe para minúsculas antes de procurar — `validação` precisa casar com `validacao`.
:::
:::{dropdown} Dica 2 — começo de palavra
`re.search(r"\\b" + re.escape(sinal), texto)` exige que o sinal comece numa fronteira de palavra: `log` casa `logs`, mas não `catalogo`.
:::
:::{dropdown} Dica 3 — montar a saída
Percorra `SINAIS` na ordem para manter a ordem das listas; as perguntas vêm do dict `PERGUNTAS`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re
import unicodedata

SINAIS = {
    "qualidade": ["teste", "validacao", "contrato", "great expectations", "dbt test", "qualidade"],
    "seguranca": ["iam", "criptografia", "acesso", "lgpd", "mascaramento", "segredo", "seguranca"],
    "observabilidade": ["alerta", "monitoramento", "log", "metrica", "freshness", "observabilidade"],
    "custo": ["custo", "finops", "orcamento", "particionamento", "bytes"],
    "idempotencia": ["idempot", "reprocess", "backfill", "upsert", "merge", "exactly-once"],
}
PERGUNTAS = {
    "qualidade": "Como você garante que o dado que chega está correto?",
    "seguranca": "Quem pode acessar esses dados e como os dados pessoais são protegidos?",
    "observabilidade": "Como você fica sabendo que o pipeline quebrou ou atrasou?",
    "custo": "Quanto isso custa por mês e como você controla o custo?",
    "idempotencia": "O que acontece se o job rodar duas vezes ou precisar reprocessar um dia?",
}


def revisar_design(texto: str) -> dict:
    norm = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    cobertas = [c for c, sins in SINAIS.items()
                if any(re.search(r"\b" + re.escape(s), norm) for s in sins)]
    faltando = [c for c in SINAIS if c not in cobertas]
    return {"cobertas": cobertas, "faltando": faltando, "perguntas": [PERGUNTAS[c] for c in faltando]}
```
O primeiro design é o que aparece em muita entrevista: tecnicamente correto e sem **nenhuma** corrente
de fundo. Repare que ele menciona "catálogo" — e o revisor **não** confunde isso com "log": a fronteira
de palavra evita o falso positivo.

As cinco perguntas são praticamente o roteiro de *follow-up* de um entrevistador. Treine respondendo-as
em uma frase cada para o seu projeto de TCC (M16) — e coloque essas frases no README (exercício 01).
:::

---
**Revisado em:** 2026-09-30
