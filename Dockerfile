# Use official Node.js slim image
FROM node:slim

# Instala Python3 e pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Instala expo-cli globalmente
RUN npm install -g expo-cli

# Define diretório de trabalho para o frontend
WORKDIR /app/todo-mobile

# Copia manifestos do Node e instala dependências
COPY todo-mobile/package.json todo-mobile/package-lock.json ./
RUN npm install

# Copia todo o código do frontend (App Expo)
COPY todo-mobile/ ./

# Define diretório de trabalho para o backend Python
WORKDIR /app/python-socket

# Copia requirements e instala dependências Python
COPY python-socket/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Volta ao diretório raiz para expor portas
WORKDIR /app

# Exponha as portas do Expo e do backend (ajuste conforme necessário)
EXPOSE 19000 19001 19002 5000

# Executa o servidor Python e o Expo em paralelo
CMD ["sh", "-c", \
     "python3 python-socket/__main__.py & \
      cd todo-mobile && expo start --tunnel --non-interactive"]