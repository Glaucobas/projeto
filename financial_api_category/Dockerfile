# Use uma imagem base Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o contêiner
COPY . .

# Exponha a porta em que sua aplicação Flask será executada
EXPOSE 5001

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
