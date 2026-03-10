# Biblioteca_Digital_python
CRUD Biblioteca Digital

Um sistema de cadastro e gerenciamento de livros, desenvolvido em Python + Tkinter + MySQL.

Funcionalidades
- Adicionar novos livros
- Buscar por registros
- Alterar informações existentes
- Excluir livros
- Interface gráfica simples e intuitiva
- Listagem organizada em tabela

Estrutura dos dados
- ID (chave primária)
- Título
- Gênero
- Autor
- Data de Publicação

Objetivo
Fornecer uma ferramenta prática e acessível para o gerenciamento de acervos digitais, com interface gráfica e armazenamento em banco de dados.

## Requisitos
- Python 3.8+ (recomendado 3.10+)
- MySQL Server
- pip

## Como rodar (Windows)

1. Clone o repositório:

	git clone https://github.com/hudalves/CRUD_python.git
	cd CRUD_python

2. Crie e ative um ambiente virtual (opcional, recomendado):

	python -m venv .venv; .\.venv\Scripts\Activate.ps1

3. Instale dependências:

	pip install -r requirements.txt

4. Copie o arquivo de exemplo de variáveis de ambiente e preencha os valores (credenciais do MySQL):

	copy .env.example .env

5. Crie a base de dados e a tabela `livros` no MySQL (exemplo):

	CREATE DATABASE nome_do_banco;
	USE nome_do_banco;
	CREATE TABLE livros (
	  IDLivros INT AUTO_INCREMENT PRIMARY KEY,
	  Titulos VARCHAR(255),
	  Genero VARCHAR(100),
	  Autor VARCHAR(255),
	  Dt_publi DATE
	);

6. Execute o programa:

	python CRUD.py

## Variáveis de ambiente
O aplicativo usa as variáveis listadas em `.env.example`:

- DB_USER
- DB_PASS
- DB_HOST
- DB_NAME

## Executáveis / Distribuição
A pasta `build/` contém artefatos gerados possivelmente por PyInstaller. Para gerar um executável localmente:

	pip install pyinstaller
	pyinstaller --onefile CRUD.py

Em Windows, o executável ficará em `dist\CRUD.exe` por padrão.

## Contribuição
Veja `CONTRIBUTING.md` para diretrizes de contribuição.

## Licença
MIT - veja `LICENSE`.
