# Usa a imagem oficial do MongoDB
FROM mongo:7.0

# Define usuário e senha root variaveis comentadas pois deve ser incluida apenas na hora de inicar o container
#ENV MONGO_INITDB_ROOT_USERNAME=usr_challenge
#ENV MONGO_INITDB_ROOT_PASSWORD=123456

# Cria o banco "admin" automaticamente
ENV MONGO_INITDB_DATABASE=admin

# Copia script de inicialização (opcional, caso queira mais customização)
# Arquivos em /docker-entrypoint-initdb.d/ são executados na primeira vez que o container roda
COPY init.js /docker-entrypoint-initdb.d/