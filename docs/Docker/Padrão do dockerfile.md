# 1. Imagem base
FROM <imagem-base>:<tag>

# 2. Metadados opcionais
LABEL maintainer="seu-email@exemplo.com"
LABEL version="1.0"
LABEL description="Descrição da sua aplicação"

# 3. Variáveis de ambiente (opcional)
ENV NOME_VARIAVEL=valor

# 4. Diretório de trabalho dentro do container
WORKDIR /apps

# 5. Copiar arquivos do host para o container
COPY ./caminho_local ./caminho_container
# ou
ADD ./caminho_local ./caminho_container  # aceita URLs e arquivos compactados

# 6. Instalar dependências
RUN comando_de_instalacao
# Ex: RUN apt-get update && apt-get install -y python3

# 7. Comandos que serão executados quando o container iniciar (opcional durante build)
CMD ["comando", "parametros"]
# ou
ENTRYPOINT ["comando", "parametros"]

# 8. Portas que serão expostas pelo container
EXPOSE 80

# 9. Comando para rodar quando o container iniciar (se não usar CMD ou ENTRYPOINT)
# Geralmente não é usado se CMD ou ENTRYPOINT já estiver definido
