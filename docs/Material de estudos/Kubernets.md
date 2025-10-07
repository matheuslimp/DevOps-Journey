# Arquitetura do Cluster

## Visão Geral
Os conceitos arquiteturais por trás do **Kubernetes**.

Um cluster Kubernetes consiste em um **control plane** mais um conjunto de máquinas trabalhadoras, chamadas de **nodes**, que executam aplicações containerizadas.  
Todo cluster precisa de pelo menos um **worker node** para executar **Pods**.

- Os **worker nodes** hospedam os Pods, que são os componentes da carga de trabalho da aplicação.  
- O **control plane** gerencia os worker nodes e os Pods no cluster.  
- Em ambientes de produção, o control plane geralmente executa em múltiplos computadores e o cluster executa múltiplos nodes, fornecendo **tolerância a falhas** e **alta disponibilidade**.

Este documento descreve os vários componentes que você precisa ter para um cluster Kubernetes completo e funcional:

- **Control plane:** kube-apiserver, etcd, kube-controller-manager, kube-scheduler  
- **Nodes:** kubelet, kube-proxy  

![](./imgs/kubernetes-cluster-architecture.svg)
---

## Sobre esta arquitetura

### Componentes do Control Plane
Os componentes do **control plane** tomam decisões globais sobre o cluster (ex.: agendamento), bem como detectam e respondem a eventos do cluster (ex.: iniciar um novo Pod quando o campo *replicas* de um Deployment não está satisfeito).

Eles podem ser executados em qualquer máquina do cluster.  
Por simplicidade, normalmente são iniciados na mesma máquina e não executam containers de usuário nela.  

#### kube-apiserver
- Exposição da **API do Kubernetes** (camada de gerenciamento).  
- É o **front-end** para a camada de gerenciamento.  
- Pode ser escalado horizontalmente executando múltiplas instâncias.

#### etcd
- Armazenamento **chave-valor consistente e altamente disponível**.  
- Usado como armazenamento de apoio do Kubernetes.  
- É necessário um **plano de backup** para proteger os dados do cluster.

#### kube-scheduler
- Observa **Pods recém-criados** sem nó atribuído.  
- Seleciona um nó para executá-los.  
- Considera fatores como:
  - Requisitos de recursos  
  - Restrições de hardware/software/política  
  - Afinidade/antiafinidade  
  - Localidade de dados  
  - Interferência entre cargas  
  - Prazos

#### kube-controller-manager
- Executa **processos de controladores**.  
- Agrupa múltiplos controladores em um **único binário**.  

Exemplos de controllers:
- **Node controller:** Detecta indisponibilidade de nodes.  
- **Job controller:** Gerencia objetos Job (tarefas pontuais).  
- **EndpointSlice controller:** Liga Services e Pods.  
- **ServiceAccount controller:** Cria contas padrão para novos namespaces.

#### cloud-controller-manager
- Incorpora lógica de controle específica da **nuvem**.  
- Conecta o cluster à API do provedor de nuvem.  
- Agrupa vários controladores em um único processo.  

Controllers dependentes da nuvem:
- **Node controller**  
- **Route controller**  
- **Service controller**

---

### Componentes do Node
Executam em cada node, mantendo Pods em execução e fornecendo o ambiente de runtime.

#### kubelet
- Agente executado em cada node.  
- Garante que containers definidos em **PodSpecs** estejam rodando.  
- Não gerencia containers fora do Kubernetes.

#### kube-proxy (opcional)
- Proxy de rede executado em cada node.  
- Mantém regras de rede que permitem comunicação entre Pods e serviços.  
- Pode delegar ao SO (iptables/ipvs) ou encaminhar tráfego diretamente.  
- Se usado um plugin de rede, o kube-proxy pode ser desnecessário.

#### Container Runtime
- Software responsável por executar containers.  
- Suporta: **Docker, containerd, CRI-O** e outros compatíveis com **CRI**.

---

### Addons
São recursos adicionais que expandem funcionalidades do cluster.  
Normalmente pertencem ao namespace `kube-system`.

#### DNS
- Essencial para todos os clusters Kubernetes.  
- Fornece registros DNS para services do Kubernetes.

#### Web UI (Dashboard)
- Interface gráfica baseada em navegador.  
- Permite gerenciar aplicações e o cluster.

#### Monitoramento de Recursos
- Coleta métricas de containers em banco de dados central.  
- Fornece UI para visualização.

#### Logging no Nível do Cluster
- Centraliza logs de containers em sistema de busca/navegação.

#### Plugins de Rede
- Implementam a especificação **CNI** (Container Network Interface).  
- Responsáveis por atribuir IPs e comunicação entre Pods.

---

## Variações de Arquitetura

Embora os componentes principais sejam consistentes, sua implantação e gerenciamento podem variar.

### Opções de Implantação do Control Plane
- **Implantação tradicional:** executa diretamente em máquinas ou VMs.  
- **Pods estáticos:** componentes como Pods gerenciados pelo kubelet.  
- **Auto-hospedado:** executa dentro do próprio cluster via Deployments/StatefulSets.  
- **Serviços gerenciados:** provedores de nuvem cuidam do control plane.

### Considerações de Posicionamento
- Clusters pequenos: control plane e workloads no mesmo node.  
- Produção: control plane em nodes dedicados.  
- Algumas organizações executam addons críticos nos nodes do control plane.

### Ferramentas de Gerenciamento
- **kubeadm**  
- **kops**  
- **Kubespray**

---

## Customização e Extensibilidade
A arquitetura do Kubernetes é altamente flexível:

- **Schedulers customizados** podem substituir ou complementar o scheduler padrão.  
- **CustomResourceDefinitions (CRDs)** e API Aggregation permitem estender a API.  
- **Cloud-controller-manager** integra provedores de nuvem.  

Essa flexibilidade permite que organizações adaptem seus clusters conforme suas necessidades, equilibrando **complexidade, desempenho e gerenciamento**.
