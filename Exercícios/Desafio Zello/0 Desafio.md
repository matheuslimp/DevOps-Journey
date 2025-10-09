# Desafios
## SRE/DevOps

Desafio para inicio estudos devops.

Este desafio é válido tanto para junior, quanto para pleno ou sênior, porém os critérios de avaliação vão variar para cada um dos níveis de experiência.
Aplicação usa será uma app do https://gitlab.zello.services/tester.zello/devops/-/tree/master

* 1. Conhecimentos, habilidades e tecnologias necessárias
* 2. Premissas
* 3. Descrição do desafio
* 4. Como submeter o desafio para análise

### 1. Conhecimentos, habilidades e tecnologias necessárias

* [SRE](https://sre.google/)
* [Linux](https://www.guiafoca.org/)
* [Shell Script](https://www.telecom.uff.br/pet/petws/downloads/apostilas/LINUX.pdf)
* [NestJS](https://nestjs.com/)
* [SpringBoot](https://spring.io/projects/spring-boot)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Kubernetes](https://kubernetes.io/)
* [Git](https://git-scm.com/)
* [GitFlow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow)
* [Gitlab CI](https://docs.gitlab.com/ce/ci/)
* [Helm](https://helm.sh/docs/intro/)

### 2. Premissas

* Os fontes não devem ser alterados;
* As dúvidas, sugestões e problemas devem ser registrados [aqui](https://github.com/thiagoinacioalves/lab-devops/issues) e estarão disponíveis para todos, assim como as respostas;
* Você pode utilizar o [minikube](https://kubernetes.io/pt-br/docs/tutorials/hello-minikube/) na <b>Etapa 4</b>

### 3. Descrição do desafio

<b>Etapa 1:</b>
* Criar um contêiner com o banco de dados MongoDB; 
* Criar um contêiner com a aplicação NestJs disponivel em "fontes/frontend"; 
* Criar um contêiner com a aplicação SpringBoot disponivel em "fontes/backend"; 

_**Entregável:**_ Os Dockerfiles

<b>Etapa 2:</b> 
* Criar um pipeline que irá construir e registrar os contêineres na sua conta pessoal no Dockerhub a cada _**push**_ 

_**Entregável:**_ O gitlab-ci.yml

<b>Etapa 3:</b>
* Executar os contêineres via comando "docker-compose up"

_**Entregável:**_ O docker-compose.yml

<b>Etapa 4:<b>
* Colocar a aplicação para funcionar no Kubernetes, no namespace "desafio";

_**Entregável:**_ Os objetos yaml - deployment, service, volume, volumeclaim, ingress - e os comandos kubectl

<b>Etapa 5:</b>
* Criar um template com helm 

_**Entregável:**_ Diretório com template, charts e values do helm.

### 4. Como submeter o desafio para análise

* Basta criar um fork no github ou criar o repo no gitlab com os entregaveis.