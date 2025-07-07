# Define a imagem base Alpine do nginx
FROM nginx:latest

# O nginx é um servidor leve e de código fonte aberto
# Como nossa aplicação irá consultar requisições HTTP, então usaremos uma imagem do Ngnix
# Use uma imagem base com um servidor web (por exemplo, Nginx)
# O nginx é um servidor leve e de código fonte aberto para realizar requisições HTTP

# Copia os arquivos de código-fonte para o diretório de trabalho do ngnix
COPY . /usr/share/nginx/html

# O Nginx expõe a porta 80 por padrão, onde o servidor web irá rodar
EXPOSE 80