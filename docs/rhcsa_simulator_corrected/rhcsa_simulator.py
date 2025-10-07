from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import subprocess
import random
import os
import traceback
import logging
import time
from collections import defaultdict
from datetime import datetime, timedelta
from weasyprint import HTML

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'rhcsa_simulator_key'
app.debug = True

# Configurações do Timer de Prova
EXAM_DURATION_MINUTES = 150  # 2h30min como no exame RHCSA real
WARNING_TIMES = [30, 15, 5]  # Avisos em minutos restantes
AUTO_SAVE_INTERVAL = 60  # Auto-save a cada minuto
TIMER_UPDATE_INTERVAL = 1  # Atualizar timer a cada segundo

# Configurações
SUBNETS = list(range(1, 51))
PORTS = [82, 8080, 8888]
USERS = ["natasha", "harry", "sarah", "bob", "alice", "fred"]
GROUPS = ["sysadm", "sharegrp", "admin", "devops"]
FILESYSTEMS = ["ext4", "xfs", "vfat"]
PASSWORDS = ["trootent", "redhat2025", "ablerate", "password"]
CRON_SCHEDULES = [
    {"type": "daily", "hour": 14, "minute": 23, "desc_en": "daily at 14:23", "desc_pt": "diário às 14:23", "command": '/usr/bin/echo "welcome"'},
    {"type": "every_n_minutes", "n": 2, "desc_en": "every 2 minutes", "desc_pt": "a cada 2 minutos", "command": '/bin/bash'},
    {"type": "daily", "hour": 10, "minute": 0, "desc_en": "daily at 10:00", "desc_pt": "diário às 10:00", "command": '/bin/echo "Test"'}
]
MOUNT_POINTS = ["/mnt/wshare", "/mnt/engine", "/mnt/database"]
REPO_URLS = [
    "http://content.example.com/rhel9.0/x86_64/dvd/BaseOS",
    "http://content.example.com/rhel9.0/x86_64/dvd/AppStream"
]
DISKS = ["/dev/vdb", "/dev/sdb"]
SIZES = [512, 1024, 2048]
UIDS = [2001, 3000, 4000]
PROFILES = ["virtual-guest", "balanced"]
CONTAINER_URLS = ["docker://nginx", "docker://apache"]
CONTAINER_NAMES = ["myapp", "webapp", "sql"]
STRINGS = ["root", "nobody", "bash"]
PATHS = ["/home", "/usr", "/var"]
FILES = ["/etc/passwd", "/usr/share/dict/words"]
DESTINATIONS = ["/tmp/result.txt", "/mnt/output.txt"]

# Categorias de questões
CATEGORIES = {
    "Network": [3, 4, 24],
    "Users": [2, 6, 8, 16],
    "Storage": [9, 10, 11, 12, 13],
    "Security": [1, 5, 14, 15, 17, 18, 19, 23],
    "Automation": [7, 20],
    "Containers": [21, 22]
}

# Banco de questões completo
QUESTIONS = [
    {
        "id": 1,
        "category": "Security",
        "en": "Reset root user password and set it to '{password}'.",
        "pt": "Redefinir a senha do usuário root e defini-la como '{password}'.",
        "params": {"password": random.choice(PASSWORDS)},
        "verify": lambda params: ("Cannot verify password directly. Confirm manually.", False)
    },
    {
        "id": 2,
        "category": "Users",
        "en": "Create account '{user}' and add to wheel group. Verify wheel group is enabled in /etc/sudoers.",
        "pt": "Criar conta '{user}' e adicionar ao grupo wheel. Verificar se o grupo wheel está habilitado em /etc/sudoers.",
        "params": {"user": "thiago-madeira"},
        "verify": lambda params: verify_user_wheel(params["user"])
    },
    {
        "id": 3,
        "category": "Network",
        "en": "Configure TCP/IP and hostname: IP=172.25.{subnet}.11, Netmask=255.255.255.0, Gateway=172.25.{subnet}.254, DNS=172.25.254.254, Hostname=server{subnet}.example.com.",
        "pt": "Configurar TCP/IP e hostname: IP=172.25.{subnet}.11, Máscara=255.255.255.0, Gateway=172.25.{subnet}.254, DNS=172.25.254.254, Hostname=server{subnet}.example.com.",
        "params": {"subnet": random.choice(SUBNETS)},
        "verify": lambda params: verify_network_hostname(params["subnet"])
    },
    {
        "id": 4,
        "category": "Network",
        "en": "Configure system to synchronize time from classroom.example.com.",
        "pt": "Configurar o sistema para sincronizar o tempo com classroom.example.com.",
        "params": {},
        "verify": lambda params: verify_ntp()
    },
    {
        "id": 5,
        "category": "Security",
        "en": "Web server on port {port} is not serving content from /var/www/html. Debug, enable at boot, configure firewall and SELinux.",
        "pt": "Servidor web na porta {port} não está servindo conteúdo de /var/www/html. Depurar, habilitar na inicialização, configurar firewall e SELinux.",
        "params": {"port": random.choice(PORTS)},
        "verify": lambda params: verify_web_server(params["port"])
    },
    {
        "id": 6,
        "category": "Users",
        "en": "Create group '{group}', users '{user1}', '{user2}', '{user3}'. '{user1}' and '{user2}' in '{group}', '{user3}' without shell. Password '{password}'. '{user3}' has read-only on /test owned by '{user1}'.",
        "pt": "Criar grupo '{group}', usuários '{user1}', '{user2}', '{user3}'. '{user1}' e '{user2}' em '{group}', '{user3}' sem shell. Senha '{password}'. '{user3}' tem leitura em /test de '{user1}'.",
        "params": {"group": random.choice(GROUPS), "user1": "", "user2": "", "user3": "", "password": random.choice(PASSWORDS)},
        "verify": lambda params: verify_users_groups(params)
    },
    {
        "id": 7,
        "category": "Automation",
        "en": "Configure cron job for '{user}' to run '{command}' at {schedule}.",
        "pt": "Configurar tarefa cron para '{user}' executar '{command}' às {schedule}.",
        "params": {"user": "", "schedule": "", "command": ""},
        "verify": lambda params: verify_cron(params["user"], params["command"])
    },
    {
        "id": 8,
        "category": "Users",
        "en": "Create user '{user}' with UID {uid}, password '{password}'.",
        "pt": "Criar usuário '{user}' com UID {uid}, senha '{password}'.",
        "params": {"user": "", "uid": random.choice(UIDS), "password": random.choice(PASSWORDS)},
        "verify": lambda params: verify_user_uid(params["user"], params["uid"])
    },
    {
        "id": 9,
        "category": "Storage",
        "en": "Configure repository with URLs {url_baseos} and {url_appstream}.",
        "pt": "Configurar repositório com URLs {url_baseos} e {url_appstream}.",
        "params": {"url_baseos": REPO_URLS[0], "url_appstream": REPO_URLS[1]},
        "verify": lambda params: verify_yum_repo()
    },
    {
        "id": 10,
        "category": "Storage",
        "en": "Create tar archive at {dest} containing {src}.",
        "pt": "Criar arquivo tar em {dest} contendo {src}.",
        "params": {"dest": random.choice(DESTINATIONS), "src": random.choice(PATHS)},
        "verify": lambda params: verify_tar(params["dest"])
    },
    {
        "id": 11,
        "category": "Storage",
        "en": "Create swap partition of {size}MB on {disk}.",
        "pt": "Criar partição swap de {size}MB em {disk}.",
        "params": {"size": random.choice(SIZES), "disk": random.choice(DISKS)},
        "verify": lambda params: verify_swap(params["disk"])
    },
    {
        "id": 12,
        "category": "Storage",
        "en": "Create LVM '{lv}' in '{vg}', {size} extents, PE {pe_size}MB, filesystem {fs}, mount at {mount_point}, auto-mount.",
        "pt": "Criar LVM '{lv}' em '{vg}', {size} extents, PE {pe_size}MB, sistema de arquivos {fs}, montar em {mount_point}, automontar.",
        "params": {"lv": "data", "vg": "vgdata", "size": random.choice([50, 100]), "pe_size": 8, "fs": random.choice(FILESYSTEMS), "mount_point": random.choice(MOUNT_POINTS)},
        "verify": lambda params: verify_lvm(params["vg"], params["lv"])
    },
    {
        "id": 13,
        "category": "Storage",
        "en": "Resize LVM '{lv}' in '{vg}' to {size}MB.",
        "pt": "Redimensionar LVM '{lv}' em '{vg}' para {size}MB.",
        "params": {"lv": "data", "vg": "vgdata", "size": random.choice(SIZES)},
        "verify": lambda params: verify_lvm_resize(params["vg"], params["lv"])
    },
    {
        "id": 14,
        "category": "Security",
        "en": "Find all files with SUID bit in {path} and save to {dest}.",
        "pt": "Encontrar todos os arquivos com bit SUID em {path} e salvar em {dest}.",
        "params": {"path": random.choice(PATHS), "dest": random.choice(DESTINATIONS)},
        "verify": lambda params: verify_suid(params["dest"])
    },
    {
        "id": 15,
        "category": "Security",
        "en": "Find all directories with SGID bit in {path} and save to {dest}.",
        "pt": "Encontrar todos os diretórios com bit SGID em {path} e salvar em {dest}.",
        "params": {"path": random.choice(PATHS), "dest": random.choice(DESTINATIONS)},
        "verify": lambda params: verify_sgid(params["dest"])
    },
    {
        "id": 16,
        "category": "Users",
        "en": "Configure password expiration policy for {days} days for user '{user}'.",
        "pt": "Configurar política de expiração de senha para {days} dias para usuário '{user}'.",
        "params": {"days": random.choice([30, 90]), "user": ""},
        "verify": lambda params: verify_passwd_expiry(params["user"])
    },
    {
        "id": 17,
        "category": "Security",
        "en": "Configure autofs to mount home directories from {nfs_server}:{nfs_path}.",
        "pt": "Configurar autofs para montar diretórios de /home em {nfs_server}:{nfs_path}.",
        "params": {"nfs_server": "nfs.example.com", "nfs_path": "/export/home"},
        "verify": lambda params: verify_autofs()
    },
    {
        "id": 18,
        "category": "Security",
        "en": "Configure collaborative directory at {path} for group '{group}' with SGID permissions.",
        "pt": "Configurar diretório colaborativo em {path} para grupo '{group}' com permissões SGID.",
        "params": {"path": "/share", "group": random.choice(GROUPS)},
        "verify": lambda params: verify_collaborative_dir(params["path"])
    },
    {
        "id": 19,
        "category": "Security",
        "en": "Search for string '{string}' in {file} and save to {dest}.",
        "pt": "Buscar string '{string}' em {file} e salvar em {dest}.",
        "params": {"string": random.choice(STRINGS), "file": random.choice(FILES), "dest": random.choice(DESTINATIONS)},
        "verify": lambda params: verify_string_search(params["dest"])
    },
    {
        "id": 20,
        "category": "Automation",
        "en": "Configure tuned profile '{profile}'.",
        "pt": "Configurar perfil tuned '{profile}'.",
        "params": {"profile": random.choice(PROFILES)},
        "verify": lambda params: verify_tuned(params["profile"])
    },
    {
        "id": 21,
        "category": "Containers",
        "en": "Build container image from {url} with name '{image_name}'.",
        "pt": "Construir imagem de container a partir de {url} com nome '{image_name}'.",
        "params": {"url": random.choice(CONTAINER_URLS), "image_name": random.choice(CONTAINER_NAMES)},
        "verify": lambda params: verify_container_image(params["image_name"])
    },
    {
        "id": 22,
        "category": "Containers",
        "en": "Configure container service '{service_name}' with volume at {volume}.",
        "pt": "Configurar serviço de container '{service_name}' com volume em {volume}.",
        "params": {"service_name": random.choice(CONTAINER_NAMES), "volume": random.choice(MOUNT_POINTS)},
        "verify": lambda params: verify_container_service(params["service_name"])
    },
    {
        "id": 23,
        "category": "Security",
        "en": "Reset the root password using single-user mode. Set it to '{password}'. Follow these steps: 1) Reboot and enter GRUB; 2) Edit the boot entry, replace 'ro' with 'rw' and add 'init=/bin/bash'; 3) Boot and run 'passwd' to set the password; 4) Run 'sync' and reboot.",
        "pt": "Redefinir a senha do root usando o modo de usuário único. Defina como '{password}'. Siga estes passos: 1) Reinicie e entre no GRUB; 2) Edite a entrada de boot, substitua 'ro' por 'rw' e adicione 'init=/bin/bash'; 3) Inicie e execute 'passwd' para definir a senha; 4) Execute 'sync' e reinicie.",
        "params": {"password": random.choice(PASSWORDS)},
        "verify": lambda params: ("Cannot verify root password reset directly. Confirm manually.", False)
    },
    {
        "id": 24,
        "category": "Network",
        "en": "Configure the system to allow SSH login as root. Ensure 'PermitRootLogin yes' is set in /etc/ssh/sshd_config and the sshd service is active.",
        "pt": "Configurar o sistema para permitir login SSH como root. Garanta que 'PermitRootLogin yes' esteja definido em /etc/ssh/sshd_config e que o serviço sshd esteja ativo.",
        "params": {},
        "verify": lambda params: verify_ssh_root()
    }
]

# Funções de verificação com tratamento de erros melhorado
def run_command(cmd):
    """Executa comando com tratamento de erro melhorado"""
    try:
        logger.debug(f"Executando comando: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        logger.debug(f"Resultado: stdout={result.stdout}, stderr={result.stderr}, rc={result.returncode}")
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout ao executar comando: {cmd}")
        return "", "Command timeout", 1
    except Exception as e:
        logger.error(f"Erro ao executar comando {cmd}: {str(e)}")
        return "", str(e), 1

def verify_user_wheel(username):
    """Verifica se usuário está no grupo wheel"""
    try:
        stdout, stderr, rc = run_command(f"id {username} | grep wheel")
        if rc == 0:
            stdout, stderr, rc = run_command("grep '^%wheel' /etc/sudoers")
            return "User in wheel group and sudoers configured.", rc == 0
        return "User not in wheel group.", False
    except Exception as e:
        logger.error(f"Erro em verify_user_wheel: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_network_hostname(subnet):
    """Verifica configuração de rede e hostname"""
    try:
        stdout, stderr, rc = run_command("nmcli con show | grep enp0s3")
        result = []
        success = True
        if rc == 0:
            result.append("Network connection enp0s3 exists.")
        else:
            result.append("Error: enp0s3 not found.")
            success = False
        stdout, stderr, rc = run_command(f"hostname | grep server{subnet}.example.com")
        if rc == 0:
            result.append("Hostname correct.")
        else:
            result.append("Error: Hostname incorrect.")
            success = False
        return "\n".join(result), success
    except Exception as e:
        logger.error(f"Erro em verify_network_hostname: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_ntp():
    """Verifica configuração NTP"""
    try:
        stdout, stderr, rc = run_command("grep classroom.example.com /etc/chrony.conf")
        if rc == 0:
            stdout, stderr, rc = run_command("systemctl is-active chronyd")
            return "NTP configured and active.", "active" in stdout
        return "NTP not configured.", False
    except Exception as e:
        logger.error(f"Erro em verify_ntp: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_web_server(port):
    """Verifica configuração do servidor web"""
    try:
        stdout, stderr, rc = run_command(f"semanage port -l | grep http_port_t.*{port}")
        result = []
        success = True
        if rc == 0:
            result.append("SELinux port configured.")
        else:
            result.append("Error: SELinux port not configured.")
            success = False
        stdout, stderr, rc = run_command(f"firewall-cmd --list-ports | grep {port}/tcp")
        if rc == 0:
            result.append("Firewall port open.")
        else:
            result.append("Error: Firewall port not open.")
            success = False
        stdout, stderr, rc = run_command("systemctl is-active httpd")
        if "active" in stdout:
            result.append("HTTPD active.")
        else:
            result.append("Error: HTTPD not active.")
            success = False
        return "\n".join(result), success
    except Exception as e:
        logger.error(f"Erro em verify_web_server: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_users_groups(params):
    """Verifica configuração de usuários e grupos"""
    try:
        group, user1, user2, user3 = params["group"], params["user1"], params["user2"], params["user3"]
        result = []
        success = True
        stdout, stderr, rc = run_command(f"getent group {group}")
        if rc == 0:
            result.append(f"Group {group} exists.")
        else:
            result.append(f"Error: Group {group} not found.")
            success = False
        for user in [user1, user2]:
            if user:  # Verificar se o usuário não está vazio
                stdout, stderr, rc = run_command(f"id {user} | grep {group}")
                if rc == 0:
                    result.append(f"User {user} in {group}.")
                else:
                    result.append(f"Error: User {user} not in {group}.")
                    success = False
        if user3:
            stdout, stderr, rc = run_command(f"getent passwd {user3} | grep nologin")
            if rc == 0:
                result.append(f"User {user3} has no shell.")
            else:
                result.append(f"Error: User {user3} has shell.")
                success = False
            stdout, stderr, rc = run_command(f"ls -ld /test | grep {user1}.*{group}.*rwx.*r-x")
            if rc == 0:
                result.append(f"User {user3} has read-only access to /test.")
            else:
                result.append(f"Error: Incorrect permissions on /test for {user3}.")
                success = False
        return "\n".join(result), success
    except Exception as e:
        logger.error(f"Erro em verify_users_groups: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_cron(user, command):
    """Verifica configuração de cron"""
    try:
        if not user or not command:
            return "Usuário ou comando não especificado.", False
        stdout, stderr, rc = run_command(f"crontab -u {user} -l | grep '{command}'")
        return "Cron job configured.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_cron: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_user_uid(user, uid):
    """Verifica UID do usuário"""
    try:
        if not user:
            return "Usuário não especificado.", False
        stdout, stderr, rc = run_command(f"id {user} | grep uid={uid}")
        return f"User {user} has UID {uid}.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_user_uid: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_yum_repo():
    """Verifica configuração de repositório"""
    try:
        stdout, stderr, rc = run_command("yum repolist | grep BaseOS")
        return "Repository configured.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_yum_repo: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_tar(dest):
    """Verifica arquivo tar"""
    try:
        stdout, stderr, rc = run_command(f"ls {dest}")
        return f"Tar archive {dest} exists.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_tar: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_swap(disk):
    """Verifica configuração de swap"""
    try:
        stdout, stderr, rc = run_command(f"swapon --show | grep {disk}")
        return "Swap configured.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_swap: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_lvm(vg, lv):
    """Verifica configuração LVM"""
    try:
        stdout, stderr, rc = run_command(f"lvdisplay /dev/{vg}/{lv}")
        return "LVM exists.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_lvm: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_lvm_resize(vg, lv):
    """Verifica redimensionamento LVM"""
    try:
        stdout, stderr, rc = run_command(f"lvdisplay /dev/{vg}/{lv}")
        return "LVM resized.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_lvm_resize: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_suid(dest):
    """Verifica lista de arquivos SUID"""
    try:
        stdout, stderr, rc = run_command(f"ls {dest}")
        return f"SUID list saved to {dest}.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_suid: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_sgid(dest):
    """Verifica lista de diretórios SGID"""
    try:
        stdout, stderr, rc = run_command(f"ls {dest}")
        return f"SGID list saved to {dest}.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_sgid: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_passwd_expiry(user):
    """Verifica política de expiração de senha"""
    try:
        if not user:
            return "Usuário não especificado.", False
        stdout, stderr, rc = run_command(f"chage -l {user}")
        return "Password expiry configured.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_passwd_expiry: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_autofs():
    """Verifica configuração autofs"""
    try:
        stdout, stderr, rc = run_command("systemctl is-active autofs")
        return "Autofs active.", "active" in stdout
    except Exception as e:
        logger.error(f"Erro em verify_autofs: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_collaborative_dir(path):
    """Verifica diretório colaborativo"""
    try:
        stdout, stderr, rc = run_command(f"ls -ld {path} | grep drwxrws")
        return "Collaborative directory configured.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_collaborative_dir: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_string_search(dest):
    """Verifica busca de string"""
    try:
        stdout, stderr, rc = run_command(f"ls {dest}")
        return f"String search results saved to {dest}.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_string_search: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_tuned(profile):
    """Verifica perfil tuned"""
    try:
        stdout, stderr, rc = run_command(f"tuned-adm active | grep {profile}")
        return "Tuned profile active.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_tuned: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_container_image(image_name):
    """Verifica imagem de container"""
    try:
        stdout, stderr, rc = run_command(f"podman images | grep {image_name}")
        return "Container image exists.", rc == 0
    except Exception as e:
        logger.error(f"Erro em verify_container_image: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_container_service(service_name):
    """Verifica serviço de container"""
    try:
        stdout, stderr, rc = run_command(f"systemctl is-active podman-{service_name}")
        return "Container service active.", "active" in stdout
    except Exception as e:
        logger.error(f"Erro em verify_container_service: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def verify_ssh_root():
    """Verifica configuração SSH root"""
    try:
        stdout, stderr, rc = run_command("grep '^PermitRootLogin yes' /etc/ssh/sshd_config")
        if rc == 0:
            stdout, stderr, rc = run_command("systemctl is-active sshd")
            return "SSH root login enabled and active.", "active" in stdout
        return "SSH root login not enabled.", False
    except Exception as e:
        logger.error(f"Erro em verify_ssh_root: {str(e)}")
        return f"Erro na verificação: {str(e)}", False

def reset_lab():
    """Função para resetar o laboratório com tratamento de erros melhorado"""
    try:
        logger.info("Iniciando reset do laboratório")
        results = []
        questions = session.get('questions', [])
        
        with open('/tmp/reset_log.txt', 'w', encoding='utf-8') as log:
            log.write(f"[{datetime.now()}] Iniciando reset do laboratório.\n")
            
            for q in questions:
                try:
                    params = q.get("params", {})
                    qid = q["id"]
                    
                    if qid == 1:  # Reset root password
                        stdout, stderr, rc = run_command("echo 'root:redhat' | chpasswd")
                        results.append(f"Senha do root redefinida para 'redhat'. RC: {rc}")
                        log.write(f"Questão {qid}: Senha do root redefinida. RC: {rc}, Stderr: {stderr}\n")
                    
                    elif qid == 2:  # Remove user
                        user = params.get("user", "")
                        if user:
                            stdout, stderr, rc = run_command(f"userdel -r {user} 2>/dev/null")
                            results.append(f"Usuário {user} removido. RC: {rc}")
                            log.write(f"Questão {qid}: Usuário {user} removido. RC: {rc}, Stderr: {stderr}\n")
                    
                    elif qid == 3:  # Reset network
                        stdout, stderr, rc = run_command("nmcli con delete enp0s3 2>/dev/null")
                        results.append(f"Configuração de rede resetada. RC: {rc}")
                        log.write(f"Questão {qid}: Rede resetada. RC: {rc}, Stderr: {stderr}\n")
                    
                    elif qid == 4:  # Reset NTP
                        stdout, stderr, rc = run_command("sed -i '/classroom.example.com/d' /etc/chrony.conf")
                        run_command("systemctl restart chronyd")
                        results.append(f"Configuração NTP resetada. RC: {rc}")
                        log.write(f"Questão {qid}: NTP resetado. RC: {rc}, Stderr: {stderr}\n")
                    
                    elif qid == 5:  # Reset web server
                        port = params.get("port", "")
                        if port:
                            stdout, stderr, rc = run_command(f"semanage port -d -t http_port_t -p tcp {port} 2>/dev/null")
                            run_command(f"firewall-cmd --remove-port={port}/tcp --permanent 2>/dev/null")
                            run_command("firewall-cmd --reload 2>/dev/null")
                            run_command("systemctl stop httpd 2>/dev/null")
                            run_command("systemctl disable httpd 2>/dev/null")
                            results.append(f"Servidor web na porta {port} resetado. RC: {rc}")
                            log.write(f"Questão {qid}: Servidor web resetado. RC: {rc}, Stderr: {stderr}\n")
                    
                    # Continuar com outras questões...
                    # (Implementação similar para as demais questões)
                    
                except Exception as e:
                    error_msg = f"Erro ao resetar a questão {qid}: {str(e)}"
                    results.append(error_msg)
                    log.write(f"Questão {qid}: Erro: {str(e)}\n")
                    logger.error(error_msg)
            
            # Limpar sessão
            session.clear()
            session.modified = True
            log.write(f"[{datetime.now()}] Sessão limpa.\n")
        
        logger.info("Reset do laboratório concluído")
        return results
        
    except Exception as e:
        logger.error(error_msg)
        return [error_msg]

# Funções de gerenciamento do Timer de Prova
def init_exam_timer():
    """Inicializa o timer do exame"""
    try:
        current_time = datetime.now()
        session['exam_start_time'] = current_time.isoformat()
        session['exam_end_time'] = (current_time + timedelta(minutes=EXAM_DURATION_MINUTES)).isoformat()
        session['exam_paused'] = False
        session['exam_paused_duration'] = 0  # Tempo total pausado em segundos
        session['warnings_shown'] = []  # Lista de avisos já mostrados
        session.modified = True
        
        logger.info(f"Timer do exame inicializado: {EXAM_DURATION_MINUTES} minutos")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar timer: {str(e)}")
        return False

def get_exam_time_remaining():
    """Retorna o tempo restante do exame em segundos"""
    try:
        if 'exam_start_time' not in session:
            return None
        
        start_time = datetime.fromisoformat(session['exam_start_time'])
        current_time = datetime.now()
        
        # Calcular tempo decorrido
        elapsed_time = (current_time - start_time).total_seconds()
        
        # Subtrair tempo pausado
        paused_duration = session.get('exam_paused_duration', 0)
        effective_elapsed = elapsed_time - paused_duration
        
        # Calcular tempo restante
        total_exam_seconds = EXAM_DURATION_MINUTES * 60
        remaining_seconds = total_exam_seconds - effective_elapsed
        
        return max(0, int(remaining_seconds))
    except Exception as e:
        logger.error(f"Erro ao calcular tempo restante: {str(e)}")
        return None

def pause_exam_timer():
    """Pausa o timer do exame"""
    try:
        if session.get('exam_paused', False):
            return False  # Já pausado
        
        session['exam_paused'] = True
        session['exam_pause_start'] = datetime.now().isoformat()
        session.modified = True
        
        logger.info("Timer do exame pausado")
        return True
    except Exception as e:
        logger.error(f"Erro ao pausar timer: {str(e)}")
        return False

def resume_exam_timer():
    """Retoma o timer do exame"""
    try:
        if not session.get('exam_paused', False):
            return False  # Não está pausado
        
        pause_start = datetime.fromisoformat(session['exam_pause_start'])
        pause_duration = (datetime.now() - pause_start).total_seconds()
        
        session['exam_paused_duration'] = session.get('exam_paused_duration', 0) + pause_duration
        session['exam_paused'] = False
        session.pop('exam_pause_start', None)
        session.modified = True
        
        logger.info(f"Timer do exame retomado. Tempo pausado: {pause_duration:.1f}s")
        return True
    except Exception as e:
        logger.error(f"Erro ao retomar timer: {str(e)}")
        return False

def is_exam_time_expired():
    """Verifica se o tempo do exame expirou"""
    remaining = get_exam_time_remaining()
    return remaining is not None and remaining <= 0

def get_exam_status():
    """Retorna o status completo do exame"""
    try:
        if 'exam_start_time' not in session:
            return {
                'initialized': False,
                'remaining_seconds': None,
                'remaining_minutes': None,
                'remaining_formatted': None,
                'expired': False,
                'paused': False,
                'warnings': []
            }
        
        remaining_seconds = get_exam_time_remaining()
        remaining_minutes = remaining_seconds // 60 if remaining_seconds else 0
        
        # Formatar tempo restante
        if remaining_seconds:
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            seconds = remaining_seconds % 60
            remaining_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            remaining_formatted = "00:00:00"
        
        # Verificar avisos
        warnings_to_show = []
        warnings_shown = session.get('warnings_shown', [])
        
        for warning_time in WARNING_TIMES:
            if remaining_minutes <= warning_time and warning_time not in warnings_shown:
                warnings_to_show.append(warning_time)
                warnings_shown.append(warning_time)
        
        session['warnings_shown'] = warnings_shown
        session.modified = True
        
        return {
            'initialized': True,
            'remaining_seconds': remaining_seconds,
            'remaining_minutes': remaining_minutes,
            'remaining_formatted': remaining_formatted,
            'expired': is_exam_time_expired(),
            'paused': session.get('exam_paused', False),
            'warnings': warnings_to_show,
            'total_duration': EXAM_DURATION_MINUTES
        }
    except Exception as e:
        logger.error(f"Erro ao obter status do exame: {str(e)}")
        return {'initialized': False, 'error': str(e)}

def auto_finish_exam():
    """Finaliza automaticamente o exame quando o tempo expira"""
    try:
        if is_exam_time_expired():
            logger.info("Tempo do exame expirado - finalizando automaticamente")
            # Marcar como finalizado automaticamente
            session['exam_auto_finished'] = True
            session.modified = True
            return True
        return False
    except Exception as e:
        logger.error(f"Erro na finalização automática: {str(e)}")
        return False

def generate_pdf(user, lang, questions, results, category_results, overall_percentage):
    """Função para gerar PDF com tratamento de erros melhorado"""
    try:
        logger.info(f"Gerando PDF para usuário {user}")
        
        # Garantir que os IDs sejam consistentes como strings
        questions_for_template = []
        for q in questions:
            q_copy = q.copy()
            q_copy["id"] = str(q_copy["id"])  # Garantir que ID seja string
            questions_for_template.append(q_copy)
        
        # Garantir que as chaves dos resultados sejam strings
        results_for_template = {}
        for key, value in results.items():
            results_for_template[str(key)] = value
        
        rendered_html = render_template(
            'result.html',
            user=user,
            lang=lang,
            questions=questions_for_template,
            results=results_for_template,
            category_results=category_results,
            overall_percentage=overall_percentage,
            score=overall_percentage,
            correct=sum(1 for qid in results_for_template if results_for_template[qid]['success']),
            total=len(questions_for_template)
        )
        
        pdf_path = f"/tmp/results_{user}.pdf"
        
        # Configurar weasyprint com encoding UTF-8
        HTML(string=rendered_html, encoding='utf-8').write_pdf(pdf_path)
        
        logger.info(f"PDF gerado com sucesso em {pdf_path}")
        return pdf_path
        
    except Exception as e:
        error_msg = f"Erro ao gerar PDF: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise Exception(error_msg)

# Rotas Flask com tratamento de erros melhorado
@app.route('/')
def index():
    """Rota principal com tratamento de erros"""
    try:
        logger.info("Acessando rota /index")
        user = request.args.get('user', 'usuario')
        lang = request.args.get('lang', 'pt')
        
        session['user'] = user
        session['lang'] = lang
        session['results'] = {}
        
        # Inicializar timer do exame se não estiver inicializado
        if 'exam_start_time' not in session:
            init_exam_timer()
        
        questions = []
        used_users = set()
        used_cron = set()
        
        for q in QUESTIONS:
            q_copy = q.copy()
            q_copy["params"] = q["params"].copy()
            
            # Preencher parâmetros dinamicamente
            for k in q_copy["params"]:
                if k == "subnet":
                    q_copy["params"][k] = random.choice(SUBNETS)
                elif k == "port":
                    q_copy["params"][k] = random.choice(PORTS)
                elif k == "password":
                    q_copy["params"][k] = random.choice(PASSWORDS)
                elif k in ["user", "user1", "user2", "user3"]:
                    available_users = [u for u in USERS if u not in used_users]
                    if available_users:
                        q_copy["params"][k] = random.choice(available_users)
                        used_users.add(q_copy["params"][k])
                elif k == "group":
                    q_copy["params"][k] = random.choice(GROUPS)
                elif k == "schedule":
                    available_schedules = [s for s in CRON_SCHEDULES if s["command"] not in used_cron]
                    if available_schedules:
                        sched = random.choice(available_schedules)
                        q_copy["params"][k] = sched[f"desc_{lang}"]
                        q_copy["params"]["command"] = sched["command"]
                        used_cron.add(sched["command"])
            
            try:
                q_copy["text"] = q[lang].format(**{k: v for k, v in q_copy["params"].items() if v})
            except KeyError:
                q_copy["text"] = q[lang]
            
            # Remove 'verify' para evitar problemas de serialização
            q_copy.pop("verify", None)
            questions.append(q_copy)
        
        session['questions'] = questions
        logger.info(f"Sessão inicializada: user={user}, lang={lang}, questions={len(questions)}")
        
        return render_template('index.html', questions=questions, user=user, lang=lang)
        
    except Exception as e:
        logger.error(f"Erro na rota index: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Erro interno: {str(e)}", 500

@app.route('/verify/<int:qid>', methods=['POST'])
def verify(qid):
    """Rota de verificação com tratamento de erros melhorado"""
    try:
        logger.info(f"Verificando questão {qid}")
        
        questions = session.get('questions', [])
        question = next((q for q in questions if q["id"] == qid), None)
        
        if not question:
            logger.warning(f"Questão {qid} não encontrada na sessão")
            return jsonify({"result": "Questão não encontrada.", "success": False})
        
        original_question = next((q for q in QUESTIONS if q["id"] == qid), None)
        if not original_question:
            logger.warning(f"Questão original {qid} não encontrada")
            return jsonify({"result": "Questão original não encontrada.", "success": False})
        
        result, success = original_question["verify"](question["params"])
        
        # Garantir que a chave seja string para consistência
        session['results'][str(qid)] = {"result": result, "success": success}
        session.modified = True
        
        logger.info(f"Verificação concluída para questão {qid}: success={success}")
        return jsonify({"result": result, "success": success})
        
    except Exception as e:
        logger.error(f"Erro na verificação da questão {qid}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"result": f"Erro na verificação: {str(e)}", "success": False})

@app.route('/finish', methods=['POST'])
def finish():
    """Rota de finalização com tratamento de erros melhorado"""
    try:
        logger.info("Acessando rota /finish")
        
        user = session.get('user', 'usuario')
        lang = session.get('lang', 'pt')
        questions = session.get('questions', [])
        results = session.get('results', {})
        
        category_scores = defaultdict(lambda: {"correct": 0, "total": 0})
        total_correct = 0
        total_questions = len(questions)
        
        for q in questions:
            qid = str(q["id"])  # Garantir que seja string
            category = q["category"]
            category_scores[category]["total"] += 1
            
            if qid in results and results[qid]["success"]:
                category_scores[category]["correct"] += 1
                total_correct += 1
        
        category_results = [
            {
                "name": cat,
                "correct": scores["correct"],
                "total": scores["total"],
                "percentage": (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            }
            for cat, scores in sorted(category_scores.items())
        ]
        
        overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        # Preparar dados para o gráfico
        category_names = [cat["name"] for cat in category_results]
        category_percentages = [cat["percentage"] for cat in category_results]
        
        # Garantir que os IDs sejam strings para o template
        questions_for_template = [{**q, "id": str(q["id"])} for q in questions]
        
        logger.info(f"Finalizando: user={user}, total_correct={total_correct}, total_questions={total_questions}")
        
        return render_template(
            'result.html',
            user=user,
            lang=lang,
            questions=questions_for_template,
            results=results,
            category_results=category_results,
            category_names=category_names,
            category_percentages=category_percentages,
            overall_percentage=overall_percentage,
            score=overall_percentage,
            correct=total_correct,
            total=total_questions
        )
        
    except Exception as e:
        logger.error(f"Erro na rota finish: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Erro ao finalizar: {str(e)}", 500

@app.route('/reset', methods=['POST'])
def reset():
    """Rota de reset com tratamento de erros"""
    try:
        logger.info("Acessando rota /reset")
        
        results = reset_lab()
        user = session.get('user', 'usuario')
        lang = session.get('lang', 'pt')
        
        logger.info(f"Reset concluído: user={user}")
        return render_template('reset.html', results=results, user=user, lang=lang)
        
    except Exception as e:
        logger.error(f"Erro na rota reset: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Erro no reset: {str(e)}", 500

@app.route('/generate_pdf_route', methods=['POST'])
def generate_pdf_route():
    """Rota para geração de PDF com tratamento de erros melhorado"""
    try:
        logger.info("Acessando rota /generate_pdf_route")
        
        user = session.get('user', 'usuario')
        lang = session.get('lang', 'pt')
        questions = session.get('questions', [])
        results = session.get('results', {})
        
        category_scores = defaultdict(lambda: {"correct": 0, "total": 0})
        total_correct = 0
        total_questions = len(questions)
        
        for q in questions:
            qid = str(q["id"])  # Garantir que seja string
            category = q["category"]
            category_scores[category]["total"] += 1
            
            if qid in results and results[qid]["success"]:
                category_scores[category]["correct"] += 1
                total_correct += 1
        
        category_results = [
            {
                "name": cat,
                "correct": scores["correct"],
                "total": scores["total"],
                "percentage": (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            }
            for cat, scores in category_scores.items()
        ]
        
        overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        pdf_path = generate_pdf(user, lang, questions, results, category_results, overall_percentage)
        logger.info(f"Enviando PDF: {pdf_path}")
        
        return send_file(pdf_path, as_attachment=True, download_name=f"results_{user}.pdf")
        
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Erro ao gerar PDF: {str(e)}"}), 500

# Rotas do Timer de Prova
@app.route('/timer/status', methods=['GET'])
def timer_status():
    """Retorna o status atual do timer"""
    try:
        status = get_exam_status()
        
        # Verificar se o tempo expirou e finalizar automaticamente
        if status.get('expired', False) and not session.get('exam_auto_finished', False):
            auto_finish_exam()
            status['auto_finished'] = True
        
        return jsonify(status)
    except Exception as e:
        logger.error(f"Erro ao obter status do timer: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/timer/pause', methods=['POST'])
def timer_pause():
    """Pausa o timer do exame"""
    try:
        success = pause_exam_timer()
        return jsonify({"success": success, "paused": session.get('exam_paused', False)})
    except Exception as e:
        logger.error(f"Erro ao pausar timer: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/timer/resume', methods=['POST'])
def timer_resume():
    """Retoma o timer do exame"""
    try:
        success = resume_exam_timer()
        return jsonify({"success": success, "paused": session.get('exam_paused', False)})
    except Exception as e:
        logger.error(f"Erro ao retomar timer: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/timer/reset', methods=['POST'])
def timer_reset():
    """Reinicia o timer do exame"""
    try:
        # Limpar dados do timer da sessão
        timer_keys = ['exam_start_time', 'exam_end_time', 'exam_paused', 
                     'exam_paused_duration', 'exam_pause_start', 'warnings_shown', 
                     'exam_auto_finished']
        for key in timer_keys:
            session.pop(key, None)
        
        # Reinicializar timer
        success = init_exam_timer()
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Erro ao reiniciar timer: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/timer/extend', methods=['POST'])
def timer_extend():
    """Estende o tempo do exame (para ambiente de laboratório)"""
    try:
        minutes = request.json.get('minutes', 30)  # Padrão: 30 minutos
        
        if 'exam_end_time' in session:
            current_end = datetime.fromisoformat(session['exam_end_time'])
            new_end = current_end + timedelta(minutes=minutes)
            session['exam_end_time'] = new_end.isoformat()
            session.modified = True
            
            logger.info(f"Timer estendido em {minutes} minutos")
            return jsonify({"success": True, "extended_minutes": minutes})
        else:
            return jsonify({"success": False, "error": "Timer não inicializado"}), 400
    except Exception as e:
        logger.error(f"Erro ao estender timer: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

