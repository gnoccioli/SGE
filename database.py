import sqlite3
import json

def conectar():
    con = sqlite3.connect('sge.db')
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

# ---------------- USUÁRIOS ----------------

def validar_usuario(email, senha):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cur.fetchone()
    con.close()
    return usuario

def listar_usuarios():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    con.close()
    return usuarios

def adicionar_usuario(nome, email, senha, tipo):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO usuarios (nome, email, senha, tipo, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    ''', (nome, email, senha, tipo))
    con.commit()
    con.close()

def buscar_usuario(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cur.fetchone()
    con.close()
    return usuario

def atualizar_usuario(id, nome, email, senha, tipo):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE usuarios
        SET nome = ?, email = ?, senha = ?, tipo = ?
        WHERE id = ?
    ''', (nome, email, senha, tipo, id))
    con.commit()
    con.close()

def alternar_status_usuario(id, status_atual):
    novo_status = 0 if status_atual else 1
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE usuarios SET ativo = ? WHERE id = ?", (novo_status, id))
    con.commit()
    con.close()

# ---------------- ALUNOS ----------------

def listar_alunos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM alunos")
    alunos = cur.fetchall()
    con.close()
    return alunos

def adicionar_aluno(nome, cpf, email, telefone, data_nascimento):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO alunos (nome, cpf, email, telefone, data_nascimento, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    ''', (nome, cpf, email, telefone, data_nascimento))
    con.commit()
    con.close()

def excluir_aluno(aluno_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    con.commit()
    con.close()

def buscar_aluno(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM alunos WHERE id = ?", (id,))
    aluno = cur.fetchone()
    con.close()
    return aluno

def atualizar_aluno(id, nome, cpf, email, telefone, data_nascimento):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE alunos SET nome = ?, cpf = ?, email = ?, telefone = ?, data_nascimento = ?
        WHERE id = ?
    ''', (nome, cpf, email, telefone, data_nascimento, id))
    con.commit()
    con.close()

# ---------------- CURSOS ----------------

def listar_cursos():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT cursos.*, usuarios.nome AS instrutor_nome
        FROM cursos
        LEFT JOIN usuarios ON cursos.instrutor_id = usuarios.id
    ''')
    cursos = cur.fetchall()
    con.close()
    return cursos

def adicionar_curso(nome, descricao, carga_horaria, instrutor_id):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO cursos (nome, descricao, carga_horaria, instrutor_id, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    ''', (nome, descricao, carga_horaria, instrutor_id))
    con.commit()
    con.close()

def excluir_curso(curso_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE id = ?", (curso_id,))
    con.commit()
    con.close()

def buscar_curso(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM cursos WHERE id = ?", (id,))
    curso = cur.fetchone()
    con.close()
    return curso

def atualizar_curso(id, nome, descricao, carga_horaria, instrutor_id):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE cursos SET nome = ?, descricao = ?, carga_horaria = ?, instrutor_id = ?
        WHERE id = ?
    ''', (nome, descricao, carga_horaria, instrutor_id, id))
    con.commit()
    con.close()

# ---------------- MATRÍCULAS ----------------

def listar_matriculas():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT m.*, a.nome AS aluno_nome, c.nome AS curso_nome
        FROM matriculas m
        JOIN alunos a ON m.aluno_id = a.id
        JOIN cursos c ON m.curso_id = c.id
    ''')
    matriculas = cur.fetchall()
    con.close()
    return matriculas

def adicionar_matricula(aluno_id, curso_id, data_matricula, status):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO matriculas (aluno_id, curso_id, data_matricula, status)
        VALUES (?, ?, ?, ?)
    ''', (aluno_id, curso_id, data_matricula, status))
    con.commit()
    con.close()

def excluir_matricula(matricula_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM matriculas WHERE id = ?", (matricula_id,))
    con.commit()
    con.close()

def buscar_matricula(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM matriculas WHERE id = ?", (id,))
    matricula = cur.fetchone()
    con.close()
    return matricula

def atualizar_matricula_status(id, status):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE matriculas SET status = ?
        WHERE id = ?
    ''', (status, id))
    con.commit()
    con.close()

# ---------------- FREQUÊNCIAS ----------------

def listar_frequencias():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT f.*, a.nome AS aluno_nome, c.nome AS curso_nome
        FROM frequencias f
        JOIN alunos a ON f.aluno_id = a.id
        JOIN cursos c ON f.curso_id = c.id
    ''')
    frequencias = cur.fetchall()
    con.close()
    return frequencias

def adicionar_frequencia(aluno_id, curso_id, data, presenca):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO frequencias (aluno_id, curso_id, data, presenca)
        VALUES (?, ?, ?, ?)
    ''', (aluno_id, curso_id, data, presenca))
    con.commit()
    con.close()

def excluir_frequencia(frequencia_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM frequencias WHERE id = ?", (frequencia_id,))
    con.commit()
    con.close()


def buscar_frequencia(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM frequencias WHERE id = ?", (id,))
    frequencia = cur.fetchone()
    con.close()
    return frequencia

def atualizar_frequencia(id, data, presenca):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE frequencias SET data = ?, presenca = ?
        WHERE id = ?
    ''', (data, presenca, id))
    con.commit()
    con.close()
# ---------------- CERTIFICADOS ----------------

def listar_certificados():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT cert.*, a.nome AS aluno_nome, c.nome AS curso_nome
        FROM certificados cert
        JOIN alunos a ON cert.aluno_id = a.id
        JOIN cursos c ON cert.curso_id = c.id
    ''')
    certificados = cur.fetchall()
    con.close()
    return certificados

def emitir_certificado(aluno_id, curso_id, codigo_verificacao):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO certificados (aluno_id, curso_id, codigo_verificacao)
        VALUES (?, ?, ?)
    ''', (aluno_id, curso_id, codigo_verificacao))
    con.commit()
    con.close()

def buscar_certificado(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM certificados WHERE id = ?", (id,))
    certificado = cur.fetchone()
    con.close()
    return certificado

def atualizar_certificado(id, aluno_id, curso_id, data_emissao, codigo_verificacao):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        UPDATE certificados
        SET aluno_id = ?, curso_id = ?, data_emissao = ?, codigo_verificacao = ?
        WHERE id = ?
    ''', (aluno_id, curso_id, data_emissao, codigo_verificacao, id))
    con.commit()
    con.close()

def excluir_certificado(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM certificados WHERE id = ?", (id,))
    con.commit()
    con.close()

# ---------------- MANUTENÇÃO ----------------

def apagar_todos_os_dados():
    con = conectar()
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys = OFF")
    
    # Ordem correta para evitar violação de FK
    tabelas = ['certificados', 'frequencias', 'matriculas', 'cursos', 'alunos', 'usuarios', 'dados_importados']
    for tabela in tabelas:
        cur.execute(f'DELETE FROM {tabela}')
        cur.execute(f'DELETE FROM sqlite_sequence WHERE name="{tabela}"')  # Reset AUTOINCREMENT

    cur.execute("PRAGMA foreign_keys = ON")    

    con.commit()
    con.close()

def banco_esta_vazio():
    con = conectar()
    cur = con.cursor()
    tabelas = ['usuarios', 'alunos', 'cursos', 'matriculas', 'frequencias', 'certificados']
    for tabela in tabelas:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        if cur.fetchone()[0] > 0:
            con.close()
            return False
    con.close()
    return True

def inserir_dado_importado(tabela, conteudo_json):
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO dados_importados (tabela, conteudo_json)
        VALUES (?, ?)
    ''', (tabela, json.dumps(conteudo_json, ensure_ascii=False)))
    con.commit()
    con.close()

def importar_para_tabelas_principais(dados):
    con = conectar()
    cur = con.cursor()

    # USUÁRIOS
    for u in dados.get('usuarios', []):
        cur.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo, created_at, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (u['nome'], u['email'], u['senha'], u['tipo'], u.get('created_at', None), u.get('ativo', 1)))

    # ALUNOS
    for a in dados.get('alunos', []):
        cur.execute('''
            INSERT INTO alunos (nome, cpf, email, telefone, data_nascimento, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (a['nome'], a['cpf'], a.get('email'), a.get('telefone'), a['data_nascimento'], a.get('created_at', None)))

    # CURSOS
    for c in dados.get('cursos', []):
        cur.execute('''
            INSERT INTO cursos (nome, descricao, carga_horaria, instrutor_id, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (c['nome'], c.get('descricao'), c['carga_horaria'], c['instrutor_id'], c.get('created_at', None)))

    # MATRÍCULAS
    for m in dados.get('matriculas', []):
        cur.execute('''
            INSERT INTO matriculas (aluno_id, curso_id, data_matricula, status)
            VALUES (?, ?, ?, ?)
        ''', (m['aluno_id'], m['curso_id'], m['data_matricula'], m['status']))

    # FREQUÊNCIAS
    for f in dados.get('frequencias', []):
        cur.execute('''
            INSERT INTO frequencias (aluno_id, curso_id, data, presenca)
            VALUES (?, ?, ?, ?)
        ''', (f['aluno_id'], f['curso_id'], f['data'], f['presenca']))

    # CERTIFICADOS
    for cert in dados.get('certificados', []):
        cur.execute('''
            INSERT INTO certificados (aluno_id, curso_id, data_emissao, codigo_verificacao)
            VALUES (?, ?, ?, ?)
        ''', (cert['aluno_id'], cert['curso_id'], cert.get('data_emissao'), cert['codigo_verificacao']))

    con.commit()
    con.close()
