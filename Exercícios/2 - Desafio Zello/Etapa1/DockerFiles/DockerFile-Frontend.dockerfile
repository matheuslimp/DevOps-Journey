# Primeiro escolho a imagem a ser utilizada
FROM node:20

# Metadados opcionais
LABEL maintainer="matheuslimp@outlook.com"
LABEL version="1.0"
LABEL description="Nestj com frontend do projeto Zello"

# Diretório de trabalho do container
WORKDIR /app/frontend

# Copia os arquivos do projeto para dentro da imagem
COPY ./fontes/frontend/. /app/frontend

# Instala as dependências
RUN npm install

# Declara a variável de ambiente (vai estar acessível via process.env.URL_BACKEND)
ENV URL_BACKEND=127.0.0.1:8080

# Por fim, executo o npm start que vai iniciar o servidor do NestJS
CMD ["npm", "start"]

# Exponho a porta 3001
EXPOSE 3001
