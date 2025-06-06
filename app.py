from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from database import *
from init_db import init_db
import os, json, zipfile, tempfile, shutil, requests

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

def gerar_codigo_certificado():
    from datetime import datetime
    import uuid
    ano = datetime.now().year
    return f"CERT-{ano}-{uuid.uuid4().hex[:8].upper()}"

@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = validar_usuario(email, senha)
        if usuario:
            session['usuario'] = usuario['nome']
            session['usuario_id'] = usuario['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.')

    banco_vazio = banco_esta_vazio()
    return render_template('login.html', banco_vazio=banco_vazio)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# ---------------- USUÁRIOS ----------------
@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuarios = listar_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
def usuarios_novo():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']
        adicionar_usuario(nome, email, senha, tipo)
        flash('Usuário adicionado com sucesso')
        return redirect(url_for('usuarios'))
    
    return render_template('usuarios_novo.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']
        # Chamar função update
        atualizar_usuario(id, nome, email, senha, tipo)
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('usuarios'))
    usuario = buscar_usuario(id)
    return render_template('usuarios_editar.html', usuario=usuario)

@app.route('/usuarios/alternar/<int:id>', methods=['POST'])
def alternar_status_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if id == session.get('usuario_id'):
        flash('Você não pode alterar seu próprio status.')
        return redirect(url_for('usuarios'))

    usuario = buscar_usuario(id)
    if usuario:
        alternar_status_usuario_db(id, usuario['ativo'])
        flash(f"Usuário {'ativado' if not usuario['ativo'] else 'inativado'} com sucesso!")
    else:
        flash("Usuário não encontrado.")

    return redirect(url_for('usuarios'))


# ---------------- ALUNOS ----------------
@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento']
        adicionar_aluno(nome, cpf, email, telefone, data_nascimento)
        flash('Aluno cadastrado com sucesso')
    alunos = listar_alunos()
    return render_template('alunos.html', alunos=alunos)

@app.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento']
        atualizar_aluno(id, nome, cpf, email, telefone, data_nascimento)
        flash('Aluno atualizado com sucesso!')
        return redirect(url_for('alunos'))
    aluno = buscar_aluno(id)
    return render_template('alunos_editar.html', aluno=aluno)

@app.route('/alunos/excluir/<int:id>', methods=['POST'])
def excluir_aluno_view(id):  # nome da função no app.py é diferente
    excluir_aluno(id)        # função de database.py permanece como está
    flash('Aluno excluído com sucesso!')
    return redirect(url_for('alunos'))

# ---------------- CURSOS ----------------
@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        professor_id = request.form['professor_id']
        adicionar_curso(nome, descricao, carga_horaria, professor_id)
        flash('Curso cadastrado com sucesso')

    cursos = listar_cursos()
    professores = [u for u in listar_usuarios() if u['tipo'] == 'Professor']
    return render_template('cursos.html', cursos=cursos, professores=professores)

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = int(request.form['carga_horaria'])
        professor_id = int(request.form['professor_id'])
        atualizar_curso(id, nome, descricao, carga_horaria, professor_id)
        flash('Curso atualizado com sucesso!')
        return redirect(url_for('cursos'))

    curso = buscar_curso(id)
    professores = [u for u in listar_usuarios() if u['tipo'] == 'Professor']
    return render_template('cursos_editar.html', curso=curso, professores=professores)



# ---------------- MATRÍCULAS ----------------
@app.route('/matriculas', methods=['GET', 'POST'])
def matriculas():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']
        data_matricula = request.form['data_matricula']
        status = request.form['status']
        adicionar_matricula(aluno_id, curso_id, data_matricula, status)
        flash('Matrícula realizada com sucesso')

    matriculas = listar_matriculas()
    alunos = listar_alunos()
    cursos = listar_cursos()
    return render_template('matriculas.html', matriculas=matriculas, alunos=alunos, cursos=cursos)

@app.route('/matriculas/editar/<int:id>', methods=['GET', 'POST'])
def editar_matricula_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        status = request.form['status']
        atualizar_matricula_status(id, status)
        flash('Status da matrícula atualizado!')
        return redirect(url_for('matriculas'))

    matricula = buscar_matricula(id)
    return render_template('matriculas_editar.html', matricula=matricula)

@app.route('/matriculas/excluir/<int:id>', methods=['POST'])
def excluir_matricula_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    excluir_matricula(id)
    flash('Matrícula excluída com sucesso!')
    return redirect(url_for('matriculas'))


# ---------------- FREQUÊNCIAS ----------------
@app.route('/frequencias', methods=['GET', 'POST'])
def frequencias():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']
        data = request.form['data']
        presenca = int(request.form['presenca'])  # 1 ou 0
        adicionar_frequencia(aluno_id, curso_id, data, presenca)
        flash('Frequência registrada com sucesso')

    frequencias = listar_frequencias()
    alunos = listar_alunos()
    cursos = listar_cursos()
    return render_template('frequencias.html', frequencias=frequencias, alunos=alunos, cursos=cursos)

@app.route('/frequencias/editar/<int:id>', methods=['GET', 'POST'])
def editar_frequencia_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['data']
        presenca = int(request.form.get('presenca', 0))  # checkbox → 0 ou 1
        atualizar_frequencia(id, data, presenca)
        flash('Frequência atualizada com sucesso!')
        return redirect(url_for('frequencias'))

    frequencia = buscar_frequencia(id)
    return render_template('frequencias_editar.html', frequencia=frequencia)


@app.route('/frequencias/excluir/<int:id>', methods=['POST'])
def excluir_frequencia_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    excluir_frequencia(id)
    flash('Frequência excluída com sucesso!')
    return redirect(url_for('frequencias'))

# ---------------- CERTIFICADOS ----------------

@app.route('/certificados', methods=['GET', 'POST'])
def certificados():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']
        codigo_verificacao = gerar_codigo_certificado()
        emitir_certificado(aluno_id, curso_id, codigo_verificacao)
        flash(f'Certificado emitido com sucesso! Código: {codigo_verificacao}')
        return redirect(url_for('certificados'))

    certificados = listar_certificados()
    alunos = listar_alunos()
    cursos = listar_cursos()
    return render_template('certificados.html', certificados=certificados, alunos=alunos, cursos=cursos)


@app.route('/certificados/editar/<int:id>', methods=['GET', 'POST'])
def editar_certificado_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']
        data_emissao = request.form['data_emissao']
        codigo_verificacao = request.form['codigo_verificacao']

        atualizar_certificado(id, aluno_id, curso_id, data_emissao, codigo_verificacao)
        flash(f'Certificado atualizado com novo código: {codigo_verificacao}')
        return redirect(url_for('certificados'))

    certificado = buscar_certificado(id)
    alunos = listar_alunos()
    cursos = listar_cursos()

    # 🆕 Gera novo código automático e substitui no dicionário
    novo_codigo = gerar_codigo_certificado()
    certificado = dict(certificado)  # converter sqlite3.Row em dict editável
    certificado['codigo_verificacao'] = novo_codigo

    return render_template(
        'certificados_editar.html',
        certificado=certificado,
        alunos=alunos,
        cursos=cursos
    )



@app.route('/certificados/excluir/<int:id>', methods=['POST'])
def excluir_certificado_view(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    excluir_certificado(id)
    flash('Certificado excluído com sucesso!')
    return redirect(url_for('certificados'))

# ---------------- MANUTENÇÃO ----------------


@app.route('/manutencao', methods=['GET', 'POST'])
def manutencao():
    dados_importados = None
    pode_inserir = False

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'url':
            url = request.form['url']
            try:
                resposta = requests.get(url)
                resposta.raise_for_status()
                dados_importados = resposta.json()
            except Exception as e:
                flash(f"Erro ao importar da URL: {e}")
                return redirect(url_for('manutencao'))

        elif acao == 'arquivo':
            arquivo = request.files['arquivo']
            if arquivo.filename.endswith('.json'):
                dados_importados = json.load(arquivo)
            elif arquivo.filename.endswith('.zip'):
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = os.path.join(tmpdir, 'arquivo.zip')
                    arquivo.save(zip_path)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir)
                    dados_json_path = os.path.join(tmpdir, 'dados.json')
                    with open(dados_json_path, 'r', encoding='utf-8') as f:
                        dados_importados = json.load(f)
            else:
                flash("Formato de arquivo não suportado.")
                return redirect(url_for('manutencao'))

        elif acao == 'inserir':
            dados_importados = json.loads(request.form['dados_para_inserir'])
            importar_para_tabelas_principais(dados_importados)
            flash("Dados inseridos com sucesso nas tabelas principais.")
            return redirect(url_for('manutencao'))

        if dados_importados:
            for tabela, conteudo in dados_importados.items():
                if isinstance(conteudo, list):
                    inserir_dado_importado(tabela, conteudo)
            pode_inserir = banco_esta_vazio()

    return render_template("manutencao.html", dados_importados=dados_importados, pode_inserir=pode_inserir)


@app.route('/exportar_dados')
def exportar_dados():
    from database import listar_usuarios, listar_alunos, listar_cursos

    dados = {
        'usuarios': [dict(u) for u in listar_usuarios()],
        'alunos': [dict(a) for a in listar_alunos()],
        'cursos': [dict(c) for c in listar_cursos()],
        'matriculas': [dict(m) for m in listar_matriculas()],
        'frequencias': [dict(f) for f in listar_frequencias()],
        'certificados': [dict(c) for c in listar_certificados()],
    }

    # Cria o diretório temporário
    with tempfile.TemporaryDirectory() as tmpdirname:
        json_path = os.path.join(tmpdirname, 'dados.json')
        zip_path = os.path.join(tmpdirname, 'exportacao.zip')

        # Cria o JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        # Cria o ZIP
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(json_path, arcname='dados.json')

        # Caminho final no static
        final_zip_path = os.path.join('static', 'exportacao.zip')

        # Copia o ZIP para a pasta static
        shutil.copyfile(zip_path, final_zip_path)

    return send_file(final_zip_path, as_attachment=True)

@app.route('/resetar_sistema', methods=['POST'])
def resetar_sistema():
    if 'usuario' in session:
        from database import apagar_todos_os_dados

        apagar_todos_os_dados()
        session.clear()
        flash("Todos os dados foram apagados e a sessão foi encerrada.")
    
    return redirect(url_for('login'))

@app.route('/importar', methods=['GET', 'POST'])
def importar():
    dados_importados = None
    pode_inserir = False

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'url':
            url = request.form['url']
            try:
                resposta = requests.get(url)
                resposta.raise_for_status()
                dados_importados = resposta.json()
            except Exception as e:
                flash(f"Erro ao importar da URL: {e}")
                return redirect(url_for('importar'))

        elif acao == 'arquivo':
            arquivo = request.files['arquivo']
            if arquivo.filename.endswith('.json'):
                dados_importados = json.load(arquivo)
            elif arquivo.filename.endswith('.zip'):
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = os.path.join(tmpdir, 'arquivo.zip')
                    arquivo.save(zip_path)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir)
                    dados_json_path = os.path.join(tmpdir, 'dados.json')
                    with open(dados_json_path, 'r', encoding='utf-8') as f:
                        dados_importados = json.load(f)
            else:
                flash("Formato de arquivo não suportado.")
                return redirect(url_for('importar'))

        elif acao == 'inserir':
            print("Recebido:", request.form['dados_para_inserir'])          # Diagnóstico
            print("===== DEBUG =====")                                      # Diagnóstico
            print("Tipo:", type(request.form['dados_para_inserir']))        # Diagnóstico
            print("Conteúdo bruto:", request.form['dados_para_inserir'])    # Diagnóstico
            print("=================")                                      # Diagnóstico

            dados_importados = json.loads(request.form['dados_para_inserir'])
            importar_para_tabelas_principais(dados_importados)
            flash("Dados inseridos com sucesso nas tabelas principais.")
            return redirect(url_for('importar'))

        # Gravar em dados_importados
        if dados_importados:
            for tabela, conteudo in dados_importados.items():
                if isinstance(conteudo, list):
                    inserir_dado_importado(tabela, conteudo)
            pode_inserir = banco_esta_vazio()

    return render_template("importar.html", dados_importados=dados_importados, pode_inserir=pode_inserir)

# ---------------- SOBRE ----------------

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')



if __name__ == '__main__':

    if not os.path.exists('sge.db'):
        print("Arquivo sge.db não encontrado. Criando novo banco de dados...")
        init_db()


    app.run(debug=True)