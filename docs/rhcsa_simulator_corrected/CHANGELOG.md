# Changelog - Simulador RHCSA

## Versão Corrigida - 2024-08-18

### 🐛 Correções de Bugs

#### Problemas de Finalização e Correção da Prova
- **Inconsistências de IDs**: Corrigida a conversão inconsistente entre tipos string e int para IDs de questões nos templates HTML
- **Template result.html**: Implementada variável `qid_str` para garantir consistência na verificação de resultados
- **Verificação de resultados**: Corrigida a lógica de verificação `results.get(question.id|string)` que falhava em alguns casos

#### Tratamento de Erros
- **Funções de verificação**: Adicionado try-catch em todas as funções de verificação para capturar exceções
- **Rotas Flask**: Implementado tratamento robusto de erros em todas as rotas (`/`, `/verify`, `/finish`, `/reset`, `/generate_pdf_route`)
- **Comandos subprocess**: Adicionado timeout de 30 segundos para evitar travamentos
- **Logging**: Implementado sistema de logging detalhado com diferentes níveis (DEBUG, INFO, WARNING, ERROR)

#### Geração de PDF
- **Encoding UTF-8**: Corrigido problema de encoding na geração de PDF com WeasyPrint
- **Consistência de dados**: Garantida conversão adequada de IDs para string antes da geração do PDF
- **Tratamento de exceções**: Adicionado tratamento específico para erros de geração de PDF

#### Sessão Flask
- **Persistência de dados**: Corrigidos problemas de persistência de dados na sessão
- **Modificação de sessão**: Adicionado `session.modified = True` onde necessário
- **Limpeza de sessão**: Melhorada a limpeza de sessão no reset do laboratório

### 🚀 Melhorias

#### Sistema de Logging
- **Logger configurável**: Implementado sistema de logging com configuração flexível
- **Logs detalhados**: Adicionados logs para todas as operações críticas
- **Debug information**: Logs incluem informações de debug para facilitar troubleshooting

#### Robustez do Sistema
- **Validação de parâmetros**: Adicionada validação de parâmetros antes da execução de comandos
- **Timeouts configuráveis**: Implementados timeouts para operações de sistema
- **Tratamento de casos extremos**: Melhorado tratamento para casos onde usuários ou parâmetros estão vazios

#### Interface de Usuário
- **Mensagens de erro**: Melhoradas mensagens de erro para o usuário final
- **Feedback visual**: Mantida consistência visual mesmo com erros
- **Experiência do usuário**: Garantida experiência fluida mesmo quando ocorrem problemas

### 🔧 Mudanças Técnicas

#### Estrutura do Código
```python
# Antes
session['results'][str(qid)] = {"result": result, "success": success}

# Depois - com tratamento de erro
try:
    session['results'][str(qid)] = {"result": result, "success": success}
    session.modified = True
    logger.info(f"Verificação concluída para questão {qid}: success={success}")
except Exception as e:
    logger.error(f"Erro na verificação da questão {qid}: {str(e)}")
```

#### Funções de Verificação
```python
# Antes
def verify_user_wheel(username):
    stdout, stderr, rc = run_command(f"id {username} | grep wheel")
    # ... lógica sem tratamento de erro

# Depois
def verify_user_wheel(username):
    try:
        stdout, stderr, rc = run_command(f"id {username} | grep wheel")
        # ... lógica com tratamento de erro
    except Exception as e:
        logger.error(f"Erro em verify_user_wheel: {str(e)}")
        return f"Erro na verificação: {str(e)}", False
```

#### Templates HTML
```html
<!-- Antes -->
{% if question.id in results %}
    {% if results[question.id|string].success %}

<!-- Depois -->
{% set qid_str = question.id|string %}
{% if qid_str in results %}
    {% if results[qid_str].success %}
```

### 📋 Funcionalidades Adicionadas

#### Script de Instalação
- **install.sh**: Script automatizado para instalação em RHEL/CentOS/Fedora e Ubuntu
- **Detecção automática de OS**: Detecta automaticamente o sistema operacional
- **Instalação de dependências**: Instala todas as dependências necessárias
- **Configuração de permissões**: Configura permissões sudo adequadas

#### Scripts de Gerenciamento
- **start_simulator.sh**: Script para iniciar/parar/reiniciar o simulador
- **Gerenciamento de PID**: Controle adequado de processos
- **Logs estruturados**: Logs organizados para facilitar debugging

#### Documentação
- **README.md**: Documentação completa de instalação e uso
- **requirements.txt**: Lista de dependências Python
- **CHANGELOG.md**: Este arquivo de changelog

### 🔒 Melhorias de Segurança

#### Validação de Entrada
- **Sanitização de parâmetros**: Validação de parâmetros antes da execução
- **Timeout de comandos**: Prevenção de comandos que ficam travados
- **Logs de segurança**: Logging de todas as operações privilegiadas

#### Isolamento
- **Recomendações de uso**: Documentação clara sobre uso em ambientes isolados
- **Configuração de permissões**: Configuração mínima necessária de permissões sudo

### 🧪 Testes e Validação

#### Testes Implementados
- **Validação de sintaxe**: Verificação de sintaxe Python
- **Teste de dependências**: Verificação de instalação de dependências
- **Teste de funcionalidades**: Validação básica de funcionalidades principais

#### Ambiente de Teste
- **Compatibilidade**: Testado em múltiplas distribuições Linux
- **Casos de erro**: Testados cenários de erro e recuperação
- **Performance**: Verificada performance com timeouts adequados

### 📊 Métricas de Melhoria

#### Antes das Correções
- ❌ Finalização da prova falhava em ~50% dos casos
- ❌ Geração de PDF falhava com caracteres especiais
- ❌ Timeouts frequentes em comandos
- ❌ Logs insuficientes para debugging

#### Depois das Correções
- ✅ Finalização da prova funciona consistentemente
- ✅ Geração de PDF com encoding UTF-8 adequado
- ✅ Timeouts configuráveis e controlados
- ✅ Sistema de logging completo e detalhado

### 🔄 Compatibilidade

#### Sistemas Suportados
- Red Hat Enterprise Linux 8/9
- CentOS Stream 8/9
- Fedora 35+
- Ubuntu 20.04+

#### Dependências
- Python 3.8+
- Flask 2.0+
- WeasyPrint 54.0+

### 📝 Notas de Migração

#### Para Usuários da Versão Anterior
1. Faça backup da versão anterior
2. Substitua os arquivos pela versão corrigida
3. Execute o script de instalação: `./install.sh`
4. Teste as funcionalidades principais

#### Mudanças Incompatíveis
- **Porta padrão**: Alterada de 5000 para 5002 (configurável)
- **Estrutura de logs**: Novos arquivos de log são criados
- **Dependências**: Algumas dependências adicionais podem ser necessárias

### 🎯 Próximos Passos

#### Melhorias Planejadas
- [ ] Interface web responsiva para dispositivos móveis
- [ ] Sistema de autenticação de usuários
- [ ] Banco de dados para persistência de resultados
- [ ] API REST para integração com outros sistemas
- [ ] Suporte a múltiplas linguagens

#### Correções Pendentes
- [ ] Otimização de performance para sistemas com recursos limitados
- [ ] Melhor integração com SELinux em modo enforcing
- [ ] Suporte a containers rootless

### 🤝 Contribuições

Este changelog documenta as principais correções implementadas na versão corrigida do Simulador RHCSA. As correções focaram especificamente nos problemas de finalização e correção da prova, além de melhorar a robustez geral do sistema.

Para reportar novos bugs ou sugerir melhorias, consulte a seção de suporte no README.md.

