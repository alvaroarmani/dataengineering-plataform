# Metodologia e Avaliação

## Metodologia

O curso adota uma abordagem **ativa e prática**, orientada a competências. Cada unidade
segue o ciclo:

**problema motivador → teoria (o *porquê*) → lab guiado → exercício autocorrigível →
solução comentada → reflexão (Feynman).**

Recursos pedagógicos:

- **Aprender fazendo:** labs e exercícios com datasets reais desde o início.
- **Fontes primárias:** livros-âncora, papers e documentação oficial (ver [Bibliografia](bibliografia-geral.md)).
- **Notebooks interativos** no navegador (fundamentos) e **bancada Docker** (engenharia real).
- **Revisão espaçada e interleaving** (flashcards e checkpoints cumulativos) para retenção.
- **IA como tutor Socrático** em checkpoints: destrava sem entregar a resposta.

Detalhes em [Método de Aprendizado](../metodo-de-aprendizado.md).

## Sistema de avaliação (progressão por maestria)

A avaliação **não é por tempo, mas por domínio**. Cada módulo define um **critério de
maestria** objetivo; só se avança ao cumpri-lo.

Critério de maestria padrão de um módulo:

- ✅ **Exercícios** com `pytest` verde (todas as suítes passando).
- ✅ **Quiz de recall** ≥ **80%** de acerto.
- ✅ **Projeto/lab** do módulo entregue conforme a **rubrica**.

### Rubrica genérica de projeto (0–100)

| Critério | Peso | O que avalia |
|---|---|---|
| Corretude | 30 | Faz o que foi pedido; resultados corretos e reproduzíveis |
| Qualidade de código/modelagem | 25 | Legibilidade, estrutura, escolhas de modelagem |
| Robustez | 15 | Tratamento de erros, idempotência, casos de borda |
| Testes | 15 | Cobertura e relevância dos testes |
| Documentação | 15 | README claro, decisões registradas, reprodutível |

Conceito: **90–100** Excelente · **75–89** Bom · **60–74** Suficiente · **<60** Refazer.

## Diagnóstico e "testar para pular"

Antes de cada módulo há um **check de pré-requisitos**. Quem já domina um tema pode fazer
o **diagnóstico** e, se atingir a maestria, pular direto para o próximo — o percurso se
adapta ao seu ponto de partida.

## Certificação interna

Ao concluir cada **eixo** por maestria, emite-se um **certificado interno** (autoemitido,
sem validade legal — ver [Apresentação](apresentacao.md)), como marco de progresso.

---
**Revisado em:** 2026-08-20
