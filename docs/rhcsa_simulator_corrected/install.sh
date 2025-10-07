#!/bin/bash

# Script de Instalação do Simulador RHCSA - Versão Corrigida
# Autor: Assistente IA
# Data: $(date +%Y-%m-%d)

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para detectar o sistema operacional
detect_os() {
    if [ -f /etc/redhat-release ]; then
        OS="rhel"
        if command -v dnf &> /dev/null; then
            PKG_MANAGER="dnf"
        else
            PKG_MANAGER="yum"
        fi
    elif [ -f /etc/debian_version ]; then
        OS="debian"
        PKG_MANAGER="apt"
    else
        print_error "Sistema operacional não suportado"
        exit 1
    fi
    
    print_status "Sistema detectado: $OS com $PKG_MANAGER"
}

# Função para verificar se o script está sendo executado como root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Executando como root. Recomenda-se executar como usuário normal."
        read -p "Continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Função para instalar dependências do sistema
install_system_deps() {
    print_status "Instalando dependências do sistema..."
    
    if [ "$OS" = "rhel" ]; then
        sudo $PKG_MANAGER update -y
        sudo $PKG_MANAGER install -y \
            python3 \
            python3-pip \
            podman \
            tuned \
            chrony \
            NetworkManager \
            firewalld \
            selinux-policy-targeted \
            policycoreutils-python-utils \
            pango \
            cairo-gobject-devel \
            libffi-devel \
            gcc \
            python3-devel
    elif [ "$OS" = "debian" ]; then
        sudo $PKG_MANAGER update
        sudo $PKG_MANAGER install -y \
            python3 \
            python3-pip \
            podman \
            tuned \
            chrony \
            network-manager \
            ufw \
            libpango-1.0-0 \
            libcairo2 \
            libffi-dev \
            gcc \
            python3-dev
    fi
    
    print_success "Dependências do sistema instaladas"
}

# Função para instalar dependências Python
install_python_deps() {
    print_status "Instalando dependências Python..."
    
    # Atualizar pip
    python3 -m pip install --upgrade pip
    
    # Instalar dependências principais
    python3 -m pip install flask weasyprint
    
    # Verificar instalação
    python3 -c "import flask; print('Flask:', flask.__version__)" || {
        print_error "Falha na instalação do Flask"
        exit 1
    }
    
    python3 -c "import weasyprint; print('WeasyPrint: OK')" || {
        print_error "Falha na instalação do WeasyPrint"
        exit 1
    }
    
    print_success "Dependências Python instaladas"
}

# Função para configurar permissões
setup_permissions() {
    print_status "Configurando permissões..."
    
    # Adicionar usuário ao grupo wheel (RHEL) ou sudo (Debian)
    if [ "$OS" = "rhel" ]; then
        sudo usermod -aG wheel $USER
        GROUP="wheel"
    else
        sudo usermod -aG sudo $USER
        GROUP="sudo"
    fi
    
    print_success "Usuário $USER adicionado ao grupo $GROUP"
    
    # Configurar sudoers para comandos específicos (opcional)
    read -p "Configurar sudo sem senha para comandos do simulador? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SUDOERS_FILE="/etc/sudoers.d/rhcsa-simulator"
        echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/firewall-cmd, /usr/sbin/semanage, /usr/bin/nmcli, /usr/sbin/tuned-adm" | sudo tee $SUDOERS_FILE
        sudo chmod 440 $SUDOERS_FILE
        print_success "Configuração sudo criada em $SUDOERS_FILE"
    fi
}

# Função para criar script de inicialização
create_start_script() {
    print_status "Criando script de inicialização..."
    
    cat > start_simulator.sh << 'EOF'
#!/bin/bash

# Script de Inicialização do Simulador RHCSA

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/rhcsa_simulator.py"
PID_FILE="$SCRIPT_DIR/simulator.pid"

start_simulator() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Simulador já está executando (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "Iniciando simulador RHCSA..."
    cd "$SCRIPT_DIR"
    nohup python3 "$PYTHON_SCRIPT" > simulator.log 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 2
    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "Simulador iniciado com sucesso!"
        echo "Acesse: http://localhost:5002?user=seu_nome&lang=pt"
        echo "Logs: $SCRIPT_DIR/simulator.log"
    else
        echo "Falha ao iniciar o simulador. Verifique os logs."
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_simulator() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Parando simulador (PID: $PID)..."
            kill $PID
            rm -f "$PID_FILE"
            echo "Simulador parado."
        else
            echo "Simulador não está executando."
            rm -f "$PID_FILE"
        fi
    else
        echo "Arquivo PID não encontrado. Simulador pode não estar executando."
    fi
}

status_simulator() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Simulador está executando (PID: $PID)"
            echo "URL: http://localhost:5002"
        else
            echo "Simulador não está executando (PID file órfão)"
            rm -f "$PID_FILE"
        fi
    else
        echo "Simulador não está executando"
    fi
}

case "$1" in
    start)
        start_simulator
        ;;
    stop)
        stop_simulator
        ;;
    restart)
        stop_simulator
        sleep 1
        start_simulator
        ;;
    status)
        status_simulator
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status}"
        echo
        echo "Comandos:"
        echo "  start   - Iniciar o simulador"
        echo "  stop    - Parar o simulador"
        echo "  restart - Reiniciar o simulador"
        echo "  status  - Verificar status do simulador"
        exit 1
        ;;
esac
EOF

    chmod +x start_simulator.sh
    print_success "Script de inicialização criado: start_simulator.sh"
}

# Função para criar arquivo de serviço systemd
create_systemd_service() {
    read -p "Criar serviço systemd para execução automática? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Criando serviço systemd..."
        
        CURRENT_DIR=$(pwd)
        SERVICE_FILE="rhcsa-simulator.service"
        
        cat > $SERVICE_FILE << EOF
[Unit]
Description=RHCSA Simulator
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 $CURRENT_DIR/rhcsa_simulator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        print_success "Arquivo de serviço criado: $SERVICE_FILE"
        print_status "Para instalar o serviço, execute:"
        print_status "  sudo cp $SERVICE_FILE /etc/systemd/system/"
        print_status "  sudo systemctl daemon-reload"
        print_status "  sudo systemctl enable rhcsa-simulator"
        print_status "  sudo systemctl start rhcsa-simulator"
    fi
}

# Função para verificar instalação
verify_installation() {
    print_status "Verificando instalação..."
    
    # Verificar Python e dependências
    python3 -c "import flask, weasyprint; print('Dependências Python: OK')" || {
        print_error "Dependências Python não estão funcionando"
        return 1
    }
    
    # Verificar arquivo principal
    if [ ! -f "rhcsa_simulator.py" ]; then
        print_error "Arquivo rhcsa_simulator.py não encontrado"
        return 1
    fi
    
    # Verificar templates
    if [ ! -d "templates" ]; then
        print_error "Diretório templates não encontrado"
        return 1
    fi
    
    # Verificar permissões
    if ! groups $USER | grep -q -E "(wheel|sudo)"; then
        print_warning "Usuário não está no grupo wheel/sudo. Algumas funcionalidades podem não funcionar."
    fi
    
    print_success "Verificação concluída com sucesso!"
}

# Função para mostrar informações finais
show_final_info() {
    print_success "Instalação concluída!"
    echo
    echo "=== COMO USAR ==="
    echo "1. Para iniciar o simulador:"
    echo "   ./start_simulator.sh start"
    echo
    echo "2. Para acessar o simulador:"
    echo "   http://localhost:5002?user=seu_nome&lang=pt"
    echo
    echo "3. Para parar o simulador:"
    echo "   ./start_simulator.sh stop"
    echo
    echo "4. Para verificar status:"
    echo "   ./start_simulator.sh status"
    echo
    echo "=== DOCUMENTAÇÃO ==="
    echo "Leia o arquivo README.md para informações detalhadas"
    echo
    echo "=== SUPORTE ==="
    echo "Em caso de problemas, verifique:"
    echo "- Logs em simulator.log"
    echo "- Permissões sudo"
    echo "- Dependências instaladas"
    echo
    print_warning "IMPORTANTE: Este simulador deve ser usado apenas em ambientes de laboratório!"
}

# Função principal
main() {
    echo "=== INSTALADOR DO SIMULADOR RHCSA - VERSÃO CORRIGIDA ==="
    echo
    
    check_root
    detect_os
    
    print_status "Iniciando instalação..."
    
    install_system_deps
    install_python_deps
    setup_permissions
    create_start_script
    create_systemd_service
    verify_installation
    
    show_final_info
}

# Executar função principal
main "$@"

