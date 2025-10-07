# Guia de Instalação e Configuração do MiniKube

## 🎯 Objetivo
- Criar um Cluster **MiniKube** e implantar um app de *Hello World*.  
- Instalar o **Kubectl**.  
- Expor o acesso da **Dashboard do MiniKube** na rede local.  

---

## 🔹 1. Provisione uma máquina com os seguintes requisitos

```yaml
CPU: 4 vCPUs ou mais
Memória RAM: 8 GB
Disco: 30–40 GB livres
SO: Ubuntu Server / Debian
Pacote instalados: Docker/SSH/
```

---

## 🔹 2. Instalação do MiniKube  
👉 Documentação oficial: [Instalação do minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)

No terminal, execute:  

```bash
sudo apt update && sudo apt upgrade -y
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
## 3. Inicie seu cluster
``` bash
minikube start
```
## 4. Instalação do Kubectl

👉 Documentação oficial: Instale o Kubectl

Passo a passo:

### Atualize os pacotes:
```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
```

### Baixe a chave de assinatura pública:

# Crie a pasta caso não exista
```bash
sudo mkdir -p -m 755 /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key | \
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```

### Adicione o repositório Kubernetes:
```bash
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /' | \
sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
```

### Instale o Kubectl:

```bash
sudo apt-get update
sudo apt-get install -y kubectl
```

⚠️ Observação: Para atualizar o kubectl para outra versão, altere o repositório no arquivo
/etc/apt/sources.list.d/kubernetes.list antes de rodar apt-get update && apt-get upgrade.

## 5. Interaja com seu cluster

Se o kubectl já estiver instalado:

```bash
kubectl get po -A
```

Ou utilize o kubectl disponibilizado pelo MiniKube:

```bash
minikube kubectl -- get po -A
```


## 6. Expondo a Dashboard do MiniKube na rede local (Port-forward) Não indicado para ambiente produtivos

### Ative a dashboard:
```bash
minikube dashboard --url
```

Este comando exibirá a URL que você pode acessar de outro computador na mesma rede.

A URL geralmente será algo como: http://<IP_DO_MINIKUBE>:<PORTA>

### Permita acesso externo (opcional, caso precise acessar fora da máquina host):

Descubra o serviço:

```bash
kubectl -n kubernetes-dashboard get svc
```

### Faça o forward para uma porta pública:
```bash
kubectl -n kubernetes-dashboard port-forward service/kubernetes-dashboar
```
### Para testar basta acessa de outro maquina 
    http://<IP DA MAQUINA>:8080/

```bash
minikube service kubernetes-dashboard --url
```
