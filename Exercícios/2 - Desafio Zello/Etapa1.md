### Etapa 1:

## Criar um contêiner com o banco de dados MongoDB;

```bash
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=Senha@123 --name mongo-container mongo:7.0
```
    Esse comando executa um container docker com a imagem MongoDB7.0 do dockerHub com redirecionamento da por 27017, e fornece as variaveis de Username e Password. 

## Criar um contêiner com a aplicação feita em NestJs disponivel em "fontes/frontend";

DOCKERFILE:
```bash
# Primeiro escolho a iamgem a ser utilizada nesse caso vou usar uma imagem do node já pronta, dessa forma garanto que as dependencias serão instalada da mais nova versão
FROM node:20

#Aqui tenho metadados opcionais
LABEL maintainer="matheuslimp@outlook.com"
LABEL version="1.0"
LABEL description="Nestj com frontend do projeto Zello"

#Diretorio de trablho do container
WORKDIR /fontes/app/frontend

#Copia dos arquivos do projeto, nesse caso a pasta frontend está sendo copiada para dentro da imagem, e ficara na /app/frontend
COPY ./fontes/frontend/. /fontes/app/frontend
# npm para instalar a dependencias

RUN npm install
#Por fim executo o npm start que vai iniciar o servidor do nestjs
CMD ["npm", "start"]
# Aqui estou expondo a porta 3000(Padrão do nestjs segundo a documentação)
EXPOSE 3001


```
### Agora com o arquivo criado junto ao diretorio do projeto Frontend, executo o Build que cria minha imagem

```bash
docker build -t img-front-zello .
```


### Rodar o container expondo a porta:
```bash
docker run -d -p 3001:3001 --name frontend-zello img-front-zello
```

### Agora vamos roda um docker logs para saber o que está acontecendo no meu container
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




## Criar um contêiner com a aplicação SpringBoot disponivel em "fontes/backend";