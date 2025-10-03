# Estrutura de Cluster OpenShift OKD (Recursos Mínimos)

Este documento descreve a estrutura mínima de máquinas recomendada para criar um cluster OpenShift OKD para testes ou laboratório.

---

## 1. Estrutura Básica de Cluster

### 1.1 Nó de Controle (Master)
- Responsáveis pelo controle do cluster, agendamento e gerenciamento.  
- **Quantidade mínima recomendada:** 3 nós  
- **Recursos mínimos (por nó):**
  - CPU: 2 vCPUs  
  - RAM: 8 GB  
  - Storage: 20–50 GB  

### 1.2 Nó de Worker
- Onde os pods e aplicativos do usuário são executados.  
- **Quantidade mínima:** 1 nó (para testes simples)  
- **Recursos mínimos (por nó):**
  - CPU: 2 vCPUs  
  - RAM: 8 GB  
  - Storage: 20–50 GB  

### 1.3 Nó de Infraestrutura (opcional)
- Para serviços como routers, registries e load balancers internos.  
- Pode ser combinado com os nós master ou worker.  
- **Recursos mínimos:** CPU 2 vCPUs, RAM 8 GB, Storage 20–50 GB  

---

## 2. Requisitos de Rede

- IPs fixos para todos os nós.  
- Firewall liberando portas padrão do OpenShift: `6443`, `22623`, `22624`, `2379-2380`, `10250`, `10255` etc.  
- DNS interno configurado para os serviços do cluster.  
- Load balancer (HAProxy ou Nginx) para distribuir tráfego para os masters e ingressos (pode ser um nó dedicado ou combinado com master/infra).

---

## 3. Storage

- Armazenamento persistente mínimo para **etcd** e pods que usam PVCs.  
- Pode usar NFS, GlusterFS, Ceph, ou armazenamento local.  
- Para laboratório, **storage local nos masters e workers já é suficiente**.

---

## 4. Exemplo de Cluster de Teste (3+1)

| Tipo de nó       | Quantidade | CPU     | RAM    | Storage   |
|-----------------|------------|--------|-------|-----------|
| Master           | 3          | 2 vCPUs | 8 GB  | 20–50 GB |
| Worker           | 1          | 2 vCPUs | 8 GB  | 20–50 GB |
| Infra / Opcional | 0 ou 1     | 2 vCPUs | 8 GB  | 20–50 GB |

> Esta configuração é voltada para testes ou laboratório. Para produção, recomenda-se recursos maiores e nós adicionais.
