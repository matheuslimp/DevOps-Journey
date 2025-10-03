# Estrutura de Cluster OpenShift OKD

Este documento descreve a estrutura de máquinas recomendada para criar um cluster OpenShift OKD (OpenShift Community).

---

## 1. Estrutura Básica de Cluster

Um cluster OpenShift/OKD é composto por três tipos de nós:

### 1.1 Nó de Controle (Master)
- Responsáveis pelo controle do cluster, agendamento e gerenciamento.  
- **Quantidade mínima recomendada:** 3 nós (para alta disponibilidade).  
- **Recursos sugeridos (por nó):**
  - CPU: 4–8 vCPUs  
  - RAM: 16–32 GB  
  - Storage: 50–100 GB (para etcd e logs)  

### 1.2 Nó de Worker
- Onde os pods e aplicativos do usuário são executados.  
- **Quantidade mínima:** 2 nós (para resiliência).  
- **Recursos sugeridos (por nó):**
  - CPU: 4–16 vCPUs  
  - RAM: 16–64 GB  
  - Storage: 100–200 GB ou mais, dependendo dos containers e logs.  

### 1.3 Nó de Infraestrutura (opcional)
- Para serviços específicos como routers, registries e load balancers internos.  
- Pode ser combinado com os nós master ou worker em clusters pequenos.  
- **Recursos sugeridos:** similares aos nós master.  

---

## 2. Requisitos de Rede

- IPs fixos para todos os nós.  
- Firewall liberando portas padrão do OpenShift: `6443`, `22623`, `22624`, `2379-2380`, `10250`, `10255` etc.  
- DNS interno configurado para os serviços do cluster.  
- Load balancer (HAProxy ou Nginx) para distribuir tráfego para os masters e ingressos.

---

## 3. Storage

- Armazenamento persistente para **etcd** e para os pods que usam PVCs.  
- Pode usar NFS, GlusterFS, Ceph, ou soluções em cloud (EBS, Azure Disk, etc.).  
- Para produção, **etcd deve ter storage rápido e redundante**.

---

## 4. Exemplo de Cluster Pequeno (3+2+1)

| Tipo de nó       | Quantidade | CPU       | RAM        | Storage       |
|-----------------|------------|----------|-----------|---------------|
| Master           | 3          | 4–8 vCPUs | 16–32 GB  | 50–100 GB     |
| Worker           | 2          | 8 vCPUs  | 32–64 GB  | 100–200 GB    |
| Infra / Opcional | 1          | 4–8 vCPUs | 16–32 GB  | 50–100 GB     |

> Para laboratórios ou testes, é possível rodar tudo em VMs menores, mas em produção é recomendável seguir os padrões acima.

