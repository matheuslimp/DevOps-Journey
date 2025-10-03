# DevOps-Journey
Um roteiro de estudos em tecnologias voltadas para **DevOps** e automação.

---

## Legenda dos conteúdos

- 🟣 **Fundamental** – Essencial para dominar o tema.
- 🟢 **Opcional** – Complementar, útil para aprofundar.
- 🟡 **Proativo** – Conteúdo extra para quem quer ir além.

---

## 1 - Sistemas Operacionais / CLI
- 🟣 Debian
- 🟣 RHEL e derivados
- 🟣 RockyLinux / CentOS
- 🟢 Windows

---

## 2 - Linguagens de Programação e Scripts
- 🟣 Bash (Monitoramento de processos, desempenho, ferramentas de rede, manipulação de texto)
- 🟣 PowerShell
- 🟢 GoLang
- 🟢 Python
- 🟡 Rust

---

## 3 - Editores de texto
- 🟣 Nano
- 🟣 Vim
- 🟣 VSCode

---

## 4 - Versionamento de código
- 🟣 Git (branch, merge, tags, GitFlow)
- 🟢 SVN

### 4.1 - Hospedagem de Repositório
- 🟣 GitLab CI/CD
- 🟣 GitHub

---

## 5 - Containers
- 🟣 Docker
- 🟣 LXC

### Orquestradores de Containers
- 🟣 Kubernetes
  - 🟣 Rancher (orquestrador de clusters)
  - 🟣 OpenShift (Kubernetes + extras Red Hat)
    - 🟣 Operadores
    - 🟣 Templates
    - 🟣 Security Context Constraints
- **Containerd** (runtime de containers)
- **CRI-O** (runtime usado em OpenShift/Kubernetes)

---

## 6 - Provisionamento e IaC
- 🟣 Kubespray (provisionamento de clusters Kubernetes com Ansible)
- 🟣 RKE / RKE2 (Rancher Kubernetes Engine)
- 🟣 Terraform (IaC, usado junto com Kubernetes)
- 🟣 Ansible
- 🟣 Helm (gerenciador de pacotes para Kubernetes, fundamental para deploys)
- 🟣 Pulumi

---

## 7 - Rede e Configuração
- 🟣 DNS
- 🟣 HTTP/HTTPS
- 🟣 SSL/TLS
- 🟣 SSH
- 🟢 Modelo OSI

### Configuração de rede
- 🟣 Proxy de encaminhamento / reverso
- 🟣 Balanceador de carga
- 🟣 Firewall
- 🟣 Servidor de cache
- 🟣 Servidor web

---

## 8 - Pipelines

### 🔹 Testes e Validações
- Unit tests / Integration tests (rodar testes automáticos dentro do pipeline)
- Linting (ESLint, Pylint, etc.)
- DAST (Dynamic Application Security Testing – segurança em execução)

### 🔹 Segurança de Imagens e Dependências
- Image Scanning (ex: Trivy, Clair, Anchore)
- Dependency Scanning (checagem de vulnerabilidades em libs e pacotes)
- Secret Detection (evitar credenciais expostas – GitLeaks, GitLab Secret scanning)

### 🔹 Build & Deploy
- Build de Containers (Docker / Buildah / Kaniko)
- Helm Charts (deploy padronizado em Kubernetes)
- ArgoCD / FluxCD (GitOps)
- Blue/Green e Canary Deployments

### 🔹 Infraestrutura
- Terraform Pipelines (IaC automatizado)
- Provisionamento dinâmico de ambientes para testes (Ephemeral Environments)

### 🔹 Observabilidade no Pipeline
- Métricas e logs do pipeline
- Notificações (Slack, Teams, e-mail)

---

## 9 - Observabilidade
- Prometheus + Grafana (monitoramento e visualização)
- ELK / EFK (Elasticsearch, Fluentd, Kibana)
- Jaeger (tracing distribuído)

---

## 10 - Rede e Segurança em Kubernetes
- CNI Plugins (Calico, Flannel, Cilium)
- Service Mesh (Istio, Linkerd)
- RBAC (Role-Based Access Control)
- Pod Security Standards (PSS) / Policies
