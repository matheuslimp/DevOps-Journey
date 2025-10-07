/**
 * Simulador RHCSA - Timer de Prova
 * Sistema de cronômetro para simular exames reais da Red Hat
 */

class ExamTimer {
    constructor() {
        this.timerInterval = null;
        this.updateInterval = 1000; // Atualizar a cada segundo
        this.warningsShown = new Set();
        this.isInitialized = false;
        this.isPaused = false;
        this.autoFinishEnabled = true;
        
        // Elementos DOM
        this.timerDisplay = null;
        this.progressBar = null;
        this.pauseButton = null;
        this.statusIndicator = null;
        
        // Configurações
        this.warningTimes = [30, 15, 5]; // Avisos em minutos
        this.totalDuration = 150; // 2h30min em minutos
        
        this.init();
    }
    
    init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupDOM());
        } else {
            this.setupDOM();
        }
    }
    
    setupDOM() {
        // Encontrar elementos DOM
        this.timerDisplay = document.getElementById('timer-display');
        this.progressBar = document.getElementById('timer-progress');
        this.pauseButton = document.getElementById('timer-pause-btn');
        this.statusIndicator = document.getElementById('timer-status');
        
        // Configurar event listeners
        if (this.pauseButton) {
            this.pauseButton.addEventListener('click', () => this.togglePause());
        }
        
        // Iniciar timer
        this.startTimer();
        
        // Configurar auto-save
        this.setupAutoSave();
    }
    
    startTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        
        this.timerInterval = setInterval(() => {
            this.updateTimer();
        }, this.updateInterval);
        
        // Primeira atualização imediata
        this.updateTimer();
    }
    
    async updateTimer() {
        try {
            const response = await fetch('/timer/status');
            const status = await response.json();
            
            if (status.error) {
                console.error('Erro no timer:', status.error);
                return;
            }
            
            this.processTimerStatus(status);
            
        } catch (error) {
            console.error('Erro ao atualizar timer:', error);
        }
    }
    
    processTimerStatus(status) {
        if (!status.initialized) {
            this.displayError('Timer não inicializado');
            return;
        }
        
        // Atualizar display
        this.updateDisplay(status);
        
        // Verificar avisos
        this.checkWarnings(status);
        
        // Verificar expiração
        if (status.expired && this.autoFinishEnabled) {
            this.handleTimeExpired();
        }
        
        // Atualizar estado de pausa
        this.isPaused = status.paused;
        this.updatePauseButton();
    }
    
    updateDisplay(status) {
        // Atualizar display de tempo
        if (this.timerDisplay) {
            this.timerDisplay.textContent = status.remaining_formatted || '00:00:00';
            
            // Mudar cor baseado no tempo restante
            const minutes = status.remaining_minutes || 0;
            this.timerDisplay.className = this.getTimerColorClass(minutes);
        }
        
        // Atualizar barra de progresso
        if (this.progressBar) {
            const percentage = ((status.remaining_seconds || 0) / (this.totalDuration * 60)) * 100;
            this.progressBar.style.width = `${Math.max(0, percentage)}%`;
            this.progressBar.className = `timer-progress ${this.getProgressColorClass(percentage)}`;
        }
        
        // Atualizar indicador de status
        if (this.statusIndicator) {
            if (status.paused) {
                this.statusIndicator.textContent = '⏸️ PAUSADO';
                this.statusIndicator.className = 'timer-status paused';
            } else if (status.expired) {
                this.statusIndicator.textContent = '⏰ TEMPO ESGOTADO';
                this.statusIndicator.className = 'timer-status expired';
            } else {
                this.statusIndicator.textContent = '⏱️ EM ANDAMENTO';
                this.statusIndicator.className = 'timer-status active';
            }
        }
    }
    
    getTimerColorClass(minutes) {
        if (minutes <= 5) return 'timer-critical';
        if (minutes <= 15) return 'timer-warning';
        if (minutes <= 30) return 'timer-caution';
        return 'timer-normal';
    }
    
    getProgressColorClass(percentage) {
        if (percentage <= 10) return 'progress-critical';
        if (percentage <= 25) return 'progress-warning';
        if (percentage <= 50) return 'progress-caution';
        return 'progress-normal';
    }
    
    checkWarnings(status) {
        if (status.warnings && status.warnings.length > 0) {
            status.warnings.forEach(warningTime => {
                if (!this.warningsShown.has(warningTime)) {
                    this.showWarning(warningTime);
                    this.warningsShown.add(warningTime);
                }
            });
        }
    }
    
    showWarning(minutes) {
        const messages = {
            30: {
                title: '⚠️ Aviso de Tempo',
                message: 'Restam 30 minutos para o final do exame!',
                type: 'warning'
            },
            15: {
                title: '⚠️ Aviso Importante',
                message: 'Restam apenas 15 minutos! Finalize suas respostas.',
                type: 'warning'
            },
            5: {
                title: '🚨 Aviso Crítico',
                message: 'ÚLTIMOS 5 MINUTOS! O exame será finalizado automaticamente.',
                type: 'critical'
            }
        };
        
        const warning = messages[minutes];
        if (warning) {
            this.showNotification(warning.title, warning.message, warning.type);
            
            // Som de alerta (se disponível)
            this.playAlertSound();
        }
    }
    
    showNotification(title, message, type = 'info') {
        // Criar elemento de notificação
        const notification = document.createElement('div');
        notification.className = `exam-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-header">
                <strong>${title}</strong>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="notification-body">${message}</div>
        `;
        
        // Adicionar ao DOM
        document.body.appendChild(notification);
        
        // Remover automaticamente após 10 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
        
        // Animar entrada
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
    }
    
    playAlertSound() {
        try {
            // Tentar reproduzir som de alerta
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
            audio.volume = 0.3;
            audio.play().catch(() => {
                // Ignorar erro se não conseguir reproduzir
            });
        } catch (error) {
            // Ignorar erro de áudio
        }
    }
    
    async togglePause() {
        try {
            const endpoint = this.isPaused ? '/timer/resume' : '/timer/pause';
            const response = await fetch(endpoint, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.isPaused = result.paused;
                this.updatePauseButton();
                
                const action = this.isPaused ? 'pausado' : 'retomado';
                this.showNotification('Timer', `Exame ${action}`, 'info');
            }
        } catch (error) {
            console.error('Erro ao pausar/retomar timer:', error);
        }
    }
    
    updatePauseButton() {
        if (this.pauseButton) {
            if (this.isPaused) {
                this.pauseButton.textContent = '▶️ Retomar';
                this.pauseButton.className = 'btn btn-success';
            } else {
                this.pauseButton.textContent = '⏸️ Pausar';
                this.pauseButton.className = 'btn btn-warning';
            }
        }
    }
    
    handleTimeExpired() {
        // Parar timer
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        // Mostrar notificação final
        this.showNotification(
            '⏰ Tempo Esgotado',
            'O tempo do exame terminou. Redirecionando para os resultados...',
            'critical'
        );
        
        // Redirecionar para resultados após 3 segundos
        setTimeout(() => {
            window.location.href = '/finish';
        }, 3000);
    }
    
    async resetTimer() {
        try {
            const response = await fetch('/timer/reset', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.warningsShown.clear();
                this.showNotification('Timer', 'Timer reiniciado', 'info');
                this.startTimer();
            }
        } catch (error) {
            console.error('Erro ao reiniciar timer:', error);
        }
    }
    
    async extendTimer(minutes = 30) {
        try {
            const response = await fetch('/timer/extend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ minutes: minutes })
            });
            const result = await response.json();
            
            if (result.success) {
                this.showNotification(
                    'Timer Estendido',
                    `Tempo estendido em ${minutes} minutos`,
                    'info'
                );
            }
        } catch (error) {
            console.error('Erro ao estender timer:', error);
        }
    }
    
    setupAutoSave() {
        // Auto-save a cada minuto
        setInterval(() => {
            if (!this.isPaused) {
                this.autoSave();
            }
        }, 60000);
    }
    
    autoSave() {
        // Salvar progresso automaticamente
        const event = new CustomEvent('autoSave', {
            detail: { timestamp: new Date().toISOString() }
        });
        document.dispatchEvent(event);
    }
    
    displayError(message) {
        if (this.timerDisplay) {
            this.timerDisplay.textContent = 'ERRO';
            this.timerDisplay.className = 'timer-error';
        }
        console.error('Timer Error:', message);
    }
    
    destroy() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
}

// Inicializar timer quando a página carregar
let examTimer;
document.addEventListener('DOMContentLoaded', function() {
    examTimer = new ExamTimer();
});

// Limpar timer ao sair da página
window.addEventListener('beforeunload', function() {
    if (examTimer) {
        examTimer.destroy();
    }
});

// Expor funções globais para uso nos templates
window.ExamTimer = ExamTimer;
window.resetExamTimer = () => examTimer?.resetTimer();
window.extendExamTimer = (minutes) => examTimer?.extendTimer(minutes);
window.toggleExamTimer = () => examTimer?.togglePause();

