Instalação:

git clone https://github.com/gnoccioli/SGE.git
cd SGE
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python.exe .\app.py


# Python - Sistema de Gestão Escolar

Tópicos Especiais em Informática
Prof. Fabrício G. Henrique  
  
## Projeto Prático  
- Desenvolver uma aplicação utilizando a linguagem de programação Python de acordo com o tema escolhido em Sala de Aula.  

## Requisitos  
- Implementar uma aplicação que contenha pelo menos dez interfaces gráficas (UI).  
	O tipo de UI pode ser definido pelos integrantes: Console, Formulário ou Web.  
- Armazenar dados de maneira persistente utilizando o SGBD da sua preferência.  
	Os dados precisam ser armazenados em pelo menos três tabelas.  
	Para cada tabela codificar na UI no mínimo três operações, dentre elas: Insert, Update, Delete e/ou Select.  
- Elaborar, necessariamente, as seguintes UI:  
	Login: em que o usuário deverá fornecer um nome de usuário e uma senha. O acesso as funcionalidades do sistema ocorrem apenas para usuários previamente cadastrados.  
	Sobre: que apresente dados do projeto {tema escolhido e objetivo} e dos desenvolvedores: {nome completo e código de matrícula}.  
	Menu: em que o usuário poderá escolher a opção desejada da aplicação.  
- Implementar uma funcionalidade que exporta todos os dados da aplicação no formato JSON. O arquivo deve ser compactado no formato zip.  
- Implementar uma funcionalidade para importa dados.  
	Os dados devem ser disponibilizados em um endereço da web.  
	Usar o módulo Requests ou URLlib.  
	Armazenar os dados importados em uma tabela.  
	Apresentar os dados importados em uma UI da aplicação.  
  
Critérios de Avaliação  
Pontos			Descrição  
[3.0 pontos] 	Implementação de pelo menos dez UI.  
[3.0 pontos] 	Modelagem do número mínimo de tabelas e implementação das operações.  
[2.0 pontos] 	Codificação da funcionalidade para exportação de dados no formato JSON.  
[2.0 pontos] 	Implementação da funcionalidade para importação dos dados.  