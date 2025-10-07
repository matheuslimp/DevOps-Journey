# 1️⃣ Fundamentos de Sistemas Operacionais

**Objetivo:** entender como o SO funciona para depois automatizar, monitorar e gerenciar sistemas.

## Conceitos básicos
- O que é SO, kernel, shell, processos, threads
- Espaço de usuário vs. espaço de kernel
- Sistemas de arquivos (ext4, xfs, ntfs)
- Permissões e usuários
- Estruturas de diretórios Linux e Windows

## Comandos essenciais (Linux)
- **Navegação:** `ls`, `cd`, `pwd`
- **Manipulação de arquivos:** `cp`, `mv`, `rm`, `mkdir`, `touch`
- **Gerenciamento de pacotes:** `apt`, `yum`, `dnf`
- **Processos:** `ps`, `top`, `htop`, `kill`

## Conceitos de rede
- TCP/IP, portas, IPs, subnets
- **Comandos:** `ping`, `netstat`, `ss`, `ifconfig`, `ip`


# 2️⃣ Administração de Sistemas

**Objetivo:** administrar servidores de forma eficiente, essencial em DevOps.

- Gestão de usuários e permissões
- Crontab / agendadores de tarefas
- Serviços e daemons: `systemd`, `service`, `journalctl`
- Logs do sistema e análise: `/var/log/`
- Monitoramento básico: `top`, `htop`, `vmstat`, `iostat`, `free`
- Backup e restore: `tar`, `rsync`, snapshots (ZFS/Btrfs)
- SSH e chaves públicas/privadas para acesso seguro
- Segurança básica: firewall (`ufw`, `firewalld`), SELinux/AppArmor


# 3️⃣ Shell Scripting e Automação

**Objetivo:** criar scripts que automatizem tarefas de infraestrutura.

## Bash scripting básico
- Variáveis, loops, condicionais
- Funções e argumentos
- Manipulação de arquivos e strings

## Ferramentas comuns
- `awk`, `sed`, `grep`, `cut`, `sort`
- Redirecionamento e pipes

- Automatizando deploys e rotinas de manutenção


# 4️⃣ Virtualização e Containers

**Objetivo:** entender a camada de abstração usada em DevOps moderno.

## Virtualização
- Conceitos: VM vs Container
- Hypervisors: KVM, VirtualBox

## Containers
- Docker (imagens, containers, volumes, redes)
- Podman (alternativa ao Docker)
- Conceito de OCI

## Orquestração
- Kubernetes (pods, nodes, deployments, services)
- Kind e Minikube para lab local
- Helm para gerenciamento de charts


# 5️⃣ Redes, Armazenamento e Cloud

**Objetivo:** dominar integração entre sistemas e nuvem.

## Redes avançadas
- NAT, Port forwarding, VPNs
- Load balancers e proxies

## Armazenamento
- Sistemas de arquivos distribuídos (GlusterFS, Ceph)
- NFS e SMB

## Cloud
- AWS, GCP, Azure – foco em instâncias Linux
- Infraestrutura como código (`Terraform`, `CloudFormation`)


# 6️⃣ Observabilidade e Debug

**Objetivo:** monitorar e resolver problemas em produção.

- **Logs centralizados:** ELK stack (Elasticsearch, Logstash, Kibana)
- **Métricas:** Prometheus + Grafana
- **Alertas e notificações:** Alertmanager

## Debug de performance
- CPU, memória, disco e rede
- `strace`, `lsof`, `tcpdump`, `perf`
