# Gabaritos dos graders

`scripts/verificar-graders.py` (roda no CI) garante, para cada exercício, que o template vazio
**reprova** e que a resposta de referência **aprova**. A resposta de referência é, por padrão, a
própria **"Solução comentada"** do `exercicio-NN.md` — assim a solução que o aluno vê é a que foi
testada. Ela é extraída automaticamente quando é inequívoca:

- `solucao.py`: o bloco ` ```python ` que define funções/classes (preenche o template);
- `solucao.py` com SQL em strings (`CONSULTA`, `CONSULTA_A`...): o bloco ` ```sql `, dividido pelos
  rótulos `-- CONSULTA_A` / `-- A)`;
- `consulta_a.sql`, `consulta_b.sql`: idem, pela letra do arquivo;
- arquivo único (`.sql`, `.yml`, `Dockerfile`): o único bloco da mesma linguagem.

Quando isso não dá (a solução publicada é um trecho, não o arquivo), o gabarito mora **aqui**,
espelhando o caminho do exercício: `gabaritos/<modulo>/<exercicio>/<mesmo caminho do arquivo>`.
Os arquivos daqui são sobrepostos a uma cópia do exercício antes do `pytest`.

Um arquivo `BANCADA` na pasta do exercício marca um grader que só pode ser verificado na bancada
(ele lê o que uma ferramenta real construiu, ex.: `dbt build`); o arquivo diz como verificar.
