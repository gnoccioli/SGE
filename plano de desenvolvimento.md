# Plano de Desenvolvimento — Sistema Web de Gestão Escolar

## ✅ 1. Definição Inicial
- **Tema**: Sistema Web para Gestão Escolar de Cursos Livres
- **Linguagem**: Python com Flask (backend) e HTML/CSS/JavaScript (frontend)
- **Banco de Dados**: SQLite ou PostgreSQL
- **Hospedagem**: Plataforma gratuita como Render, Railway ou Heroku

---

## ✅ 2. Formação da Equipe
- Dividir as funções entre os membros:
  - **Backend**: APIs, banco de dados, autenticação
  - **Frontend**: HTML, CSS, interação via JS
  - **Documentação e Testes**
  - **Gerência e Organização do Projeto**

---

## ✅ 3. Requisitos Obrigatórios do Projeto

| Item                         | Descrição                                                                 |
|-----------------------------|---------------------------------------------------------------------------|
| UIs                         | Mínimo de 10 interfaces: Login, Menu, Sobre, Aluno, Curso, Frequência, etc. |
| Tabelas                     | Mínimo de 3 (Ex: alunos, cursos, matrículas)                             |
| Operações CRUD              | Cada tabela deve permitir pelo menos 3 operações (Insert, Update, Delete, Select) |
| Exportação de Dados         | Exportar todos os dados em `.json` compactado em `.zip`                  |
| Importação de Dados via Web | Baixar dados externos com `requests` ou `urllib`, armazenar e exibir     |

---

## ✅ 4. Interfaces já prototipadas

- Tela de **Login**
- Tela de **Sobre**
- Tela de **Menu Principal**
- Cadastro de **Alunos**
- Cadastro de **Cursos**
- Frequência de **Instrutores**
- Frequência de **Alunos**
- Gerenciamento **Financeiro**
- **Emissão de Certificados**
- **Relatório de Aprovações**

---

## ✅ 5. Etapas de Desenvolvimento (por Sprint)

### Sprint 1 – Infraestrutura e Login
- Configuração do ambiente
- Criação do banco de dados
- Implementação da API de autenticação
- Tela de login com validação

### Sprint 2 – Módulos Básicos
- Cadastro de alunos e cursos
- Tela de permissões
- Tela de menu e sobre

### Sprint 3 – Módulos de Gerenciamento
- Gerenciamento de frequência (alunos e instrutores)
- Emissão de certificados
- Relatório de aprovações

### Sprint 4 – Extras e Integrações
- Exportação para `.json` com `zipfile`
- Importação de dados com `requests`
- Finalização e testes

---

## ✅ 6. Boas Práticas em Equipe
- **Controle de Versão**: usar Git e GitHub (com branches para cada feature)
- **Kanban ou Scrum Board**: Trello ou GitHub Projects
- **Daily Meetings**: reuniões curtas para alinhar progresso
- **Revisões de Código**: Pull requests com revisão por outro membro
- **Documentação**: README com instruções, documentação de API e modelo do banco

---

## ✅ 7. Exportação e Importação

### Exportar
- Gerar JSON com todos os dados e compactar com `zipfile`

### Importar
- URL de exemplo com dados JSON
- Usar `requests.get()` para capturar e importar
- Exibir os dados em uma nova UI

---

## ✅ 8. Testes
- **Unitários**: funções e endpoints
- **Integração**: banco + API + frontend
- **Usabilidade**: facilidade de uso para personas

---

## ✅ 9. Publicação
- Hospedar o sistema gratuitamente
- Subir o repositório no GitHub
- Criar um vídeo demonstrando o sistema
- Preparar apresentação para a banca (com foco em personas, objetivos e solução)
