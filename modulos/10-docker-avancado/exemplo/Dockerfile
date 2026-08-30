# Multi-stage: instala deps num builder e copia só o necessário para a imagem final (slim).
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/inst -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /inst /usr/local
COPY . .                       # código por último (aproveita o cache das deps)
CMD ["python", "main.py"]
