# Guia Prático: Cloud-init no Ubuntu Server com Proxmox e Terraform

Perfeito! Vamos detalhar como usar o **cloud-init** no Ubuntu Server, pensando no seu uso com **Proxmox** e **Terraform**.  

Dividido em explicação prática e exemplos.

---

## 1️⃣ O que é Cloud-init

O **cloud-init** é uma ferramenta que automatiza a configuração inicial de VMs. Ele permite definir:

- Usuários e senhas / SSH keys  
- Hostname  
- Configuração de rede (DHCP ou IP fixo)  
- Scripts de inicialização (instalação de pacotes, updates, etc.)

No **Proxmox**, você pode usar o cloud-init para criar **templates** e depois cloná-los, configurando cada VM automaticamente.

---

## 2️⃣ Como habilitar cloud-init no Proxmox

Na VM que será template:

1. Vá em **Hardware → Add → Cloud-init Drive**.  
2. Configure como disco **IDE** ou **SCSI**, geralmente 4-8MB é suficiente.  

O **cloud-init** cria uma interface entre o Proxmox e a VM para passar dados de configuração.

---

## 3️⃣ Configurações básicas no Ubuntu Server

No Ubuntu, o cloud-init lê arquivos YAML em `/etc/cloud/cloud.cfg.d/`. Você pode criar um arquivo, por exemplo:

```yaml
# /etc/cloud/cloud.cfg.d/99-custom.cfg
system_info:
  default_user:
    name: ubuntu
    lock_passwd: false
    gecos: Ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
```
# hostname será definido via Proxmox ou Terraform
preserve_hostname: false

# pacotes extras a instalar na primeira inicialização
packages:
  - vim
  - git
  - curl
  - net-tools

## 4️⃣ Passando dados do Proxmox para a VM via cloud-init

No **Proxmox**:

1. Selecione a VM (ou template)  
2. Vá em **Cloud-Init → User & Password / SSH Keys / Network**  
3. Configure:

   - **Username:** ubuntu  
   - **Password:** (opcional, se usar SSH key)  
   - **SSH Public Key:** sua chave pública  
   - **Hostname:** será aplicado na primeira inicialização  

Depois, quando a VM for clonada, o **Terraform** ou **Proxmox** pode sobrescrever esses dados via cloud-init.

---

## 5️⃣ Configuração de rede via cloud-init

### Exemplo para IP estático:

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.101/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4
]
```
### Usando DHCP

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
```
###Testando cloud-init na VM

  Para testar se o cloud-init está funcionando:
```yaml
    sudo cloud-init status
    sudo cloud-init clean    # limpa configurações antigas
    sudo cloud-init init     # aplica novas configurações
    sudo cloud-init status --long
```
