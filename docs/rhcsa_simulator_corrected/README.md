# Simulador RHCSA - Versão Corrigida com Cronômetro

## Descrição

Este é um simulador para o exame Red Hat Certified System Administrator (RHCSA) que permite praticar questões típicas do exame em um ambiente web interativo. Esta versão inclui todas as correções anteriores MAIS um cronômetro completo que simula a experiência real dos exames Red Hat.

## 🆕 NOVA FUNCIONALIDADE: Cronômetro de Prova

### ⏱️ Características do Timer:
- **Duração real**: 2h30min (150 minutos) como no exame RHCSA oficial
- **Contagem regressiva**: Mostra tempo restante em tempo real (HH:MM:SS)
- **Avisos automáticos**: Alertas aos 30min, 15min e 5min restantes
- **Auto-finalização**: Finaliza automaticamente quando o tempo acaba
- **Interface visual**: Cronômetro sempre visível no topo com mudança de cores
- **Controles**: Pausar/retomar e estender tempo (para laboratório)
- **Auto-save**: Salva progresso automaticamente a cada minuto
- **Persistência**: Mantém tempo mesmo se recarregar a página

### 🎨 Interface do Cronômetro:
- **Verde**: Tempo normal (>30min)
- **Amarelo**: Atenção (30-15min)
- **Laranja**: Aviso (15-5min)  
- **Vermelho piscante**: Crítico (<5min)
- **Barra de progresso**: Indicação visual do tempo restante
- **Notificações pop-up**: Avisos não intrusivos
- **Responsivo**: Adapta-se a desktop, tablet e mobile

## Correções Implementadas

### Problemas Corrigidos:

1. **Inconsistências de IDs**: Corrigida a conversão inconsistente entre tipos string e int para IDs de questões
2. **Tratamento de Erros**: Implementado tratamento robusto de exceções em todas as funções
3. **Geração de PDF**: Melhorado o processo de geração de PDF com encoding UTF-8 adequado
4. **Sessão Flask**: Corrigidos problemas de persistência de dados na sessão
5. **Timeout de Comandos**: Adicionado timeout para comandos subprocess para evitar travamentos
6. **Logging**: Implementado sistema de logging detalhado para debug
7. **Template HTML**: Corrigidas inconsistências no template de resultados

### Melhorias Adicionais:

- Tratamento de erros mais robusto em todas as rotas Flask
- Validação de parâmetros antes da execução de comandos
- Logs detalhados para facilitar debugging
- Encoding UTF-8 consistente em todo o sistema
- Timeouts configuráveis para operações de sistema

## Requisitos do Sistema

### Sistema Operacional
- Red Hat Enterprise Linux 8/9 ou CentOS Stream 8/9
- Fedora 35+ 
- Ubuntu 20.04+ (para desenvolvimento)

### Dependências Python
- Python 3.8+
- Flask 2.0+
- WeasyPrint 54.0+

### Dependências do Sistema
- Ferramentas administrativas do Linux (systemctl, nmcli, etc.)
- Podman (para questões de containers)
- Tuned (para questões de performance)
- Chrony (para questões de NTP)

## Instalação

### Passo 1: Preparar o Ambiente

```bash
# Atualizar o sistema
sudo dnf update -y  # Para RHEL/CentOS/Fedora
# ou
sudo apt update && sudo apt upgrade -y  # Para Ubuntu

# Instalar Python e pip
sudo dnf install python3 python3-pip -y  # Para RHEL/CentOS/Fedora
# ou
sudo apt install python3 python3-pip -y  # Para Ubuntu
```

### Passo 2: Instalar Dependências Python

```bash
# Instalar dependências Python
pip3 install flask weasyprint

# Ou usando requirements.txt (se disponível)
pip3 install -r requirements.txt
```

### Passo 3: Instalar Dependências do Sistema

```bash
# Para RHEL/CentOS/Fedora
sudo dnf install -y podman tuned chrony NetworkManager firewalld selinux-policy-targeted

# Para Ubuntu
sudo apt install -y podman tuned chrony network-manager ufw
```

### Passo 4: Configurar Permissões

```bash
# Adicionar usuário ao grupo wheel (se necessário)
sudo usermod -aG wheel $USER

# Configurar sudo sem senha para comandos específicos (opcional, para desenvolvimento)
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/firewall-cmd, /usr/sbin/semanage" | sudo tee /etc/sudoers.d/rhcsa-simulator
```

## Execução

### Método 1: Execução Direta

```bash
# Navegar para o diretório do simulador
cd /caminho/para/rhcsa_simulator_corrected

# Executar o simulador
python3 rhcsa_simulator.py
```

### Método 2: Usando Script de Inicialização

```bash
# Tornar o script executável
chmod +x start_simulator.sh

# Executar o script
./start_simulator.sh
```

### Método 3: Como Serviço Systemd (Produção)

```bash
# Copiar arquivo de serviço
sudo cp rhcsa-simulator.service /etc/systemd/system/

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar e iniciar o serviço
sudo systemctl enable rhcsa-simulator
sudo systemctl start rhcsa-simulator
```

## Uso do Simulador

### Acessando o Simulador

1. Abra um navegador web
2. Acesse: `http://localhost:5002?user=seu_nome&lang=pt`
3. Substitua `seu_nome` pelo seu nome de usuário
4. Use `lang=en` para inglês ou `lang=pt` para português

### Funcionalidades Principais

#### 1. Verificação de Questões
- Clique em "Verificar" para cada questão após implementar a solução
- O sistema executará comandos de verificação automaticamente
- Resultados são exibidos em tempo real

#### 2. Finalização da Prova
- Clique em "Finalizar Simulação" quando terminar todas as questões
- Visualize seus resultados por categoria
- Veja sua pontuação geral e recomendações

#### 3. Geração de Relatório PDF
- Clique em "Gerar Relatório PDF" para baixar um relatório completo
- O PDF inclui todas as questões, resultados e estatísticas

#### 4. Reset do Laboratório
- Use "Zerar Laboratório" para limpar todas as configurações
- Retorna o sistema ao estado inicial para nova simulação

### Categorias de Questões

O simulador inclui questões nas seguintes categorias:

1. **Network** (Rede)
   - Configuração TCP/IP
   - Hostname
   - NTP
   - SSH

2. **Users** (Usuários)
   - Criação de usuários e grupos
   - Políticas de senha
   - Sudo/wheel

3. **Storage** (Armazenamento)
   - LVM
   - Partições
   - Swap
   - Repositórios YUM
   - Arquivos TAR

4. **Security** (Segurança)
   - SELinux
   - Firewall
   - Permissões especiais (SUID/SGID)
   - Autofs
   - Busca de arquivos

5. **Automation** (Automação)
   - Cron jobs
   - Tuned profiles

6. **Containers** (Contêineres)
   - Podman
   - Imagens de contêiner
   - Serviços de contêiner

## Solução de Problemas

### Problema: Servidor não inicia

**Sintomas**: Erro "Address already in use"

**Solução**:
```bash
# Verificar portas em uso
netstat -tlnp | grep :5002

# Matar processos na porta
sudo fuser -k 5002/tcp

# Ou alterar a porta no arquivo rhcsa_simulator.py
```

### Problema: Comandos de verificação falham

**Sintomas**: Todas as verificações retornam erro

**Solução**:
```bash
# Verificar permissões sudo
sudo -l

# Verificar se serviços necessários estão instalados
systemctl status NetworkManager
systemctl status firewalld
```

### Problema: PDF não é gerado

**Sintomas**: Erro ao gerar relatório PDF

**Solução**:
```bash
# Instalar dependências do WeasyPrint
sudo dnf install -y pango cairo-gobject-devel  # RHEL/Fedora
# ou
sudo apt install -y libpango-1.0-0 libcairo2  # Ubuntu

# Verificar instalação do WeasyPrint
python3 -c "import weasyprint; print('WeasyPrint OK')"
```

### Problema: Timeout em comandos

**Sintomas**: Comandos demoram muito para executar

**Solução**:
- Verificar se o sistema não está sobrecarregado
- Aumentar timeout no código se necessário
- Verificar conectividade de rede para comandos que precisam de internet

## Configuração Avançada

### Personalização de Questões

Para adicionar novas questões, edite o array `QUESTIONS` no arquivo `rhcsa_simulator.py`:

```python
{
    "id": 25,
    "category": "Custom",
    "en": "Your question in English",
    "pt": "Sua questão em português",
    "params": {"param1": "value1"},
    "verify": lambda params: verify_custom_function(params)
}
```

### Configuração de Logging

Para alterar o nível de logging, modifique no início do arquivo:

```python
logging.basicConfig(level=logging.INFO)  # ou DEBUG, WARNING, ERROR
```

### Configuração de Timeout

Para alterar o timeout dos comandos, modifique na função `run_command`:

```python
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
```

## Segurança

### Considerações Importantes

1. **Ambiente de Desenvolvimento**: Este simulador é destinado a ambientes de laboratório e desenvolvimento
2. **Comandos Privilegiados**: O simulador executa comandos com privilégios elevados
3. **Acesso de Rede**: Mantenha o simulador em rede isolada ou confiável
4. **Backup**: Faça backup do sistema antes de usar o simulador

### Recomendações

- Use em máquinas virtuais dedicadas
- Não execute em sistemas de produção
- Monitore logs de segurança durante o uso
- Revise comandos executados pelo simulador

## Suporte e Contribuição

### Reportar Problemas

Para reportar bugs ou problemas:

1. Verifique os logs em `/tmp/reset_log.txt`
2. Inclua informações do sistema operacional
3. Descreva os passos para reproduzir o problema
4. Inclua mensagens de erro completas

### Contribuir

Para contribuir com melhorias:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Implemente testes para novas funcionalidades
4. Envie pull request com descrição detalhada

## Licença

Este projeto é distribuído sob licença MIT. Veja o arquivo LICENSE para detalhes.

## Changelog

### Versão Corrigida (2024)

- ✅ Corrigidos problemas de finalização e correção da prova
- ✅ Implementado tratamento robusto de erros
- ✅ Melhorada geração de PDF
- ✅ Corrigidas inconsistências de IDs
- ✅ Adicionado sistema de logging
- ✅ Implementados timeouts para comandos
- ✅ Melhorado encoding UTF-8

### Versão Original

- ✅ Simulador básico com 24 questões
- ✅ Interface web com Flask
- ✅ Verificação automática de questões
- ✅ Geração de relatórios
- ✅ Reset de laboratório

