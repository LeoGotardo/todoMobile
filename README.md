TodoMobile
Um aplicativo de gerenciamento de tarefas (Todo List) completo com backend em Python e frontend em React Native.
📱 Sobre o Projeto
O TodoMobile é uma aplicação full-stack que permite aos usuários criar, editar, excluir e gerenciar suas tarefas diárias. O projeto consiste em:

Backend: API em Python com Flask e comunicação via Socket
Frontend: Aplicativo móvel em React Native com TypeScript
Banco de Dados: SQLite com SQLAlchemy ORM
Autenticação: Sistema de login/registro com criptografia bcrypt

🚀 Funcionalidades
Autenticação

✅ Registro de novos usuários
✅ Login com validação de credenciais
✅ Criptografia de senhas com bcrypt
✅ Persistência de sessão

Gerenciamento de Tarefas

✅ Criar novas tarefas
✅ Editar tarefas existentes
✅ Marcar tarefas como concluídas/pendentes
✅ Excluir tarefas individuais
✅ Limpar todas as tarefas concluídas
✅ Visualizar estatísticas (total, pendentes, concluídas)

Interface

✅ Design responsivo e intuitivo
✅ Modal de edição de tarefas
✅ Indicadores de loading
✅ Confirmações de ações destrutivas

🛠️ Tecnologias Utilizadas
Backend

Python 3.x
Flask - Framework web
SQLAlchemy - ORM para banco de dados
SQLite - Banco de dados
bcrypt - Criptografia de senhas
Socket - Comunicação em tempo real
python-dotenv - Gerenciamento de variáveis de ambiente

Frontend

React Native - Framework mobile
TypeScript - Tipagem estática
AsyncStorage - Armazenamento local
React Navigation (implícito)

📋 Pré-requisitos
Backend

Python 3.7+
pip (gerenciador de pacotes Python)

Frontend

Node.js 14+
npm ou yarn
React Native CLI
Android Studio (para Android) ou Xcode (para iOS)

🔧 Instalação e Configuração
1. Clone o repositório
bashgit clone https://github.com/seu-usuario/todomobile.git
cd todomobile

2. Configuração do Backend
Instale as dependências:
pip install -r requirements.txt

Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto:

envDB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_db

Execute o servidor:
python __main__.py
O servidor Socket estará rodando em xxx.xxx.x.x:8080

Execute o servidor HTTP (opcional):
python server.py
O servidor HTTP estará rodando em 0.0.0.0:5000

3. Configuração do Frontend
Instale as dependências:
npm install
ou
yarn install

Configure o IP do servidor:
No arquivo services/SocketClient.ts, ajuste o IP do servidor:
typescriptconstructor(host: string = 'xxx.xxx.x.x', port: number = 5000) {

Execute o aplicativo:
npx react-native run-android
ou
npx react-native run-ios
