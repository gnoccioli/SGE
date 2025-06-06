import sqlite3

def conectar():
    con = sqlite3.connect('sge.db')
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    try:
        con = conectar()
        cur = con.cursor()

        # Criação das tabelas
        cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            senha TEXT,
            tipo TEXT CHECK(tipo IN ('Admin', 'Professor', 'Secretaria')),
            ativo INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT UNIQUE,
            email TEXT,
            telefone TEXT,
            data_nascimento DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            carga_horaria INTEGER,
            professor_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professor_id) REFERENCES usuarios(id)
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            curso_id INTEGER,
            data_matricula DATE,
            status TEXT CHECK(status IN ('ativo', 'concluído', 'cancelado')),
            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS frequencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            curso_id INTEGER,
            data DATE,
            presenca INTEGER,  -- 1 = presente, 0 = ausente
            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS certificados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            curso_id INTEGER,
            data_emissao DATE DEFAULT CURRENT_DATE,
            codigo_verificacao TEXT UNIQUE,
            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
        ''')

        # Tabela para armazenar dados importados
        cur.execute('''
            CREATE TABLE IF NOT EXISTS dados_importados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tabela TEXT NOT NULL,
                conteudo_json TEXT NOT NULL,
                data_importacao DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        con.commit()
        print("Banco de dados inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
    finally:
        con.close()

if __name__ == '__main__':
    init_db()
