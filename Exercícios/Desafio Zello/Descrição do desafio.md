## Etapa 1:

* Criar um contêiner com o banco de dados MongoDB;
* Criar um contêiner com a aplicação NestJs disponivel em "fontes/frontend";
* Criar um contêiner com a aplicação SpringBoot disponivel em "fontes/backend";

### Criar um contêiner com o banco de dados MongoDB;

Para contêiner foi utilizado a imagem padrão do mongo DB e adicionado variaveis(Comentadas) para com usuário e senha utilizada pelo backend para conectar com o banco

```bash
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
```

### Comando para buildar o a imagem
```bash
docker build -f DockerFile-backend.dockerfile -t img-mongo-zello .
```

---

### Criar um contêiner com a aplicação feita em NestJs disponivel em "fontes/frontend";
Esse docker file ele usa a imagem do node 20 cria o container, copia os arquivo do fontes/frontend para dentro do container e instalar "npm install" a dependencia que incluem o nestjs e declara a URL do backend como uma variavel e expoem a porta.

DOCKERFILE:
```bash
# Primeiro escolho a imagem a ser utilizada
FROM node:20

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
```
### Comando para buildar o container
```bash
docker build -f DockerFile-Frontend.dockerfile -t img-frontend-zello .
```


### Criar um contêiner com a aplicação SpringBoot disponivel em "fontes/backend";
* Como o projeto não estava compilado foi necessário realizar a instalação do maven e compilar o arquivo .jar e antes tive que atualizar alguns dependencia para que sejam compativeis com a imagem, pois estavam desatualizadas como o lombok, "<version>1.18.32</version>"

Depois de compilado utilizei a imagem do eclipse copiando o .jar para dentro do container e executando.

DOCKERFILE-Backend:
```bash
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```


### Build da imagem
```bash
docker build  -f DockerFile-Backend.dockerfile -t img-backend-zello .
```

## Agora com as imagens buildadas vamos apenas usar o compose.yaml para subir nosso containers e acessar a aplicação
```bash
docker compose up -d
```

## Etapa 4:

Colocar a aplicação para funcionar no Kubernetes, no namespace "challenge";

Entregável: Os objetos yaml - deployment, service, volume, volumeclaim, ingress - e os comandos kubectl


```yaml
# deployment.yaml
apiVersion: apps/v1       # Versão da API
kind: Deployment          # Tipo de recurso
metadata:
  name: minha-aplicacao   # Nome do Deployment
  namespace: challenge    # Namespace onde será criado
  labels:
    app: minha-aplicacao
spec:
  replicas: 3             # Número de Pods desejados
  selector:
    matchLabels:
      app: minha-aplicacao
  template:
    metadata:
      labels:
        app: minha-aplicacao
    spec:
      containers:
        - name: minha-aplicacao-container
          image: minha-imagem:latest  # Imagem do contêiner
          ports:
            - containerPort: 80       # Porta exposta pelo contêiner
          env:                        # Variáveis de ambiente (opcional)
            - name: AMBIENTE
              value: "producao"
```

Explicação dos principais campos:

apiVersion: Versão da API do Kubernetes para o Deployment (apps/v1 é a mais usada atualmente).

kind: Tipo de recurso (Deployment).

metadata: Informações do Deployment, como nome, namespace e labels.

spec: Especificações do Deployment.

  replicas: Quantos Pods você quer executar.

  selector: Define como o Deployment encontra os Pods gerenciados.

  template: Modelo de Pod que será criado.

  metadata: Labels do Pod.

  spec: Especificações do Pod, incluindo contêineres, imagens, portas e variáveis de ambiente.