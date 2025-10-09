# Etapa 1:

# Criar um contêiner com o banco de dados MongoDB;

### Observação: Foi necessário adicionar as variaveis de user e password para que o backend tenha acesso ao banco ADMIN.

```bash
# Usa a imagem oficial do MongoDB
FROM mongo:7.0

# Define usuário e senha root
ENV MONGO_INITDB_ROOT_USERNAME=usr_challenge
ENV MONGO_INITDB_ROOT_PASSWORD=123456

# Cria o banco "admin" automaticamente
ENV MONGO_INITDB_DATABASE=admin

# Copia script de inicialização (opcional, caso queira mais customização)
# Arquivos em /docker-entrypoint-initdb.d/ são executados na primeira vez que o container roda
COPY init.js /docker-entrypoint-initdb.d/

```

### Comando para buildar o container
```bash
docker build -t img-mongo-zello .
```

### Comando que executa o container.
```bash
docker run -d -p 27017:27017 --name mongo-container custom-mongo
```
---

# Criar um contêiner com a aplicação feita em NestJs disponivel em "fontes/frontend";
### Observação: Foi necessário informar o ENV contendo a URL do backend
DOCKERFILE:
```bash
# Primeiro escolho a imagem a ser utilizada
FROM node:20

# Metadados opcionais
LABEL maintainer="matheuslimp@outlook.com"
LABEL version="1.0"
LABEL description="Nestj com frontend do projeto Zello"

# Diretório de trabalho do container
WORKDIR /fontes/app/frontend

# Copia os arquivos do projeto para dentro da imagem
COPY ./fontes/frontend/. /fontes/app/frontend

# Instala as dependências
RUN npm install

# Declara a variável de ambiente (vai estar acessível via process.env.URL_BACKEND)
ENV URL_BACKEND=127.0.0.1:8080

# Por fim, executo o npm start que vai iniciar o servidor do NestJS
CMD ["npm", "start"]

# Exponho a porta 3001
EXPOSE 3001
```
### Comando para buildar o container
```bash
docker build -t img-front-zello .
```

### Comando para subir o container
```bash
docker run -d -p 3001:3001 --name frontend-zello img-front-zello
```
---


### Agora vamos rodar um docker logs para saber o que está acontecendo no container
```bash
    docker logs frontend-zello
```
### Saida

```bash
    ➜  devops git:(master) ✗ docker logs frontend-zello 

    > bola-de-cristal-frontend@1.0.0 start
    > nest start
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [NestFactory] Starting Nest application...
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [InstanceLoader] HttpModule dependencies initialized +26ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [InstanceLoader] ConfigHostModule dependencies initialized +1ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [InstanceLoader] ConfigModule dependencies initialized +0ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [InstanceLoader] AppModule dependencies initialized +0ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [RoutesResolver] AppController {/}: +4ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [RouterExplorer] Mapped {/, GET} route +2ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [RouterExplorer] Mapped {/resposta, GET} route +1ms
    [Nest] 31  - 10/08/2025, 5:34:49 PM     LOG [NestApplication] Nest application successfully started +2ms
    URL: http://127.0.0.1:3001

```

### Sendo assim se eu acessa http://127.0.0.1:3001 vou encontrar a seguinte pagina

![front](./Front.png)




# Criar um contêiner com a aplicação SpringBoot disponivel em "fontes/backend";
* Como o projeto não estava compilado foi necessário realizar a instalação do maven e compilar o arquivo .jar e antes tive que atualizar alguns dependencia par aque sejam compativeis com a imagem, pois estavam desatualizadas como o lombok, "<version>1.18.32</version>"

DOCKERFILE-Backend:
```bash
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```


### Build da imagem

    docker build -t minha-app-backend .


### Rodar o container

    docker run -d -p 8080:8080 --name backend minha-app-backend


### Ver logs em tempo real

    docker logs -f backend


### E acessar no navegador:

    http://localhost:8080
