# 🤖✨ Gerador de Templates Handlebars com IA Generativa

Este projeto utiliza a API de IA Generativa do Google Gemini para criar templates Handlebars dinamicamente. A aplicação é capaz de aprender com exemplos de templates existentes e gerar novos templates com base nas necessidades especificadas pelo usuário.

## 🎯 Finalidade

O objetivo principal é automatizar e simplificar a criação de templates Handlebars. Ao fornecer um exemplo de entrada de dados e a saída desejada, o sistema utiliza um modelo de IA para gerar um template Handlebars que realiza essa transformação, agilizando o desenvolvimento e reduzindo o trabalho manual.

## 🛠️ Tecnologias e Bibliotecas

🐍 Linguagem: Python 3.10+

🚀 Framework: FastAPI, Uvicorn

🧠 IA Generativa: google-generativeai (API do Gemini)

📦 Banco de Dados: MongoDB

📊 Qualidade de Código: autopep8, pylint, black, flake8, bandit

🔬 Computação Científica: numpy, scikit-learn

⚙️ Gerenciamento de Ambiente: python-dotenv

## ✅ Pré-requisitos

Para executar este projeto, você precisará ter as seguintes ferramentas instaladas em sua máquina.

### 🐳 Ambiente de Desenvolvimento (Dev Container - Recomendado)

A forma mais simples de rodar o projeto é utilizando o Dev Container, que encapsula todas as dependências.

- Docker
- Docker Compose
- Visual Studio Code
- Extensão **Dev Containers** da Microsoft para VS Code.

## 🚀 Como Começar

#### 1. Clonar o Repositório

```bash
git clone /python-ai-template-handler.git
cd  python-ai-template-handler
```

#### 2. Configurar Variáveis de Ambiente

Crie um arquivo chamado **.env** na raiz do projeto, seguindo o modelo:

```
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/embedding-001
```

🔒 Precisa gerar sua chave api do gemini. **SEMPRE** a mantenha segura e não a compartilhe!

#### 3. Executando com Dev Container (Recomendado)

1. Abra a pasta do projeto no Visual Studio Code.

2. O VS Code irá detectar a presença do arquivo .devcontainer/devcontainer.json e sugerir reabrir o projeto em um container. Clique em "Reopen in Container".

3. Aguarde o Docker construir e iniciar o container. O processo pode levar alguns minutos na primeira vez.

4. O ambiente de desenvolvimento estará pronto, com todas as dependências instaladas e os serviços (como o MongoDB) em execução.

## ▶️ Executando a Aplicação

#### Rodando normalmente

```bash
make run-api
```

#### 🐞 Debug

O projeto já vem configurado para debug no Visual Studio Code através do arquivo **.vscode/launch.json**. Para iniciar uma sessão de debug:

1. Abra o painel "Run and Debug" (ícone de play com um inseto) na barra lateral do VS Code.

2. Selecione a configuração "Python: FastAPI" no menu suspenso.

3. Pressione F5 ou clique no ícone de play verde para iniciar o debug.

Isso iniciará o servidor Uvicorn com o debugger do VS Code anexado, permitindo que você adicione breakpoints e inspecione o código em tempo de execução.

## 💡 Casos de Uso e Exemplos

A aplicação expõe endpoints para interagir com o modelo de IA.

#### Gerar exemplo de template:

Endpoint: **POST** _/template/example_

Finalidade: Fornece um exemplo de entrada para saída desejada bem como o template handlebars responsável por realizar a conversão.

#### Gerar template:

Endpoint: POST /template/generate

Finalidade: Fornece uma entrada bem como sua saída esperada. A api deverá fornecer as informações necessárias para que o agente generativo possa gerar o template com base na documentação oficial do handlebars e possíveis exemplos previamente cadastrados na api.

#### 📚 Para exemplos práticos de como chamar esses endpoints, consulte os arquivos na pasta /requests do projeto.
