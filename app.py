from flask import Flask, render_template, request
import mysql.connector
import bcrypt

app = Flask(__name__)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Preencha com os dados exatos da prova [cite: 11, 12]
db_config = {
    'user': 'useradmin',
    'password': 'admin@123',
    'host': 'serverdbp2.mysql.database.azure.com', 
    'database': 'db_giovannaitaliani',  # <--- TROQUE PELO NOME DO SEU BANCO
    'ssl_ca': 'DigiCertGlobalRootCA.crt.pem' 
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    # 1. Receber dados do HTML [cite: 26]
    nome = request.form.get('nome')
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    email = request.form.get('email')
    obs = request.form.get('observacao')

    # 2. Validação simples no Back-end [cite: 32]
    if not nome or not usuario or not senha or not email:
        return "<h1>Erro: Preencha todos os campos obrigatórios!</h1>"

    # 3. Criptografar a Senha (Hashing) 
    senha_bytes = senha.encode('utf-8') # Converte texto para bytes
    salt = bcrypt.gensalt()             # Gera o 'tempero' aleatório
    senha_hash = bcrypt.hashpw(senha_bytes, salt) # Cria o hash

    # 4. Conectar e Salvar no Banco [cite: 30, 33]
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """INSERT INTO alunos 
                 (nome_completo, usuario_acesso, senha_hash, email_aluno, observacao) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        # Atenção: senha_hash é bytes, precisamos salvar como string ou blob. 
        # O mysql-connector lida bem, mas vamos decodificar para garantir string no banco.
        valores = (nome, usuario, senha_hash.decode('utf-8'), email, obs)
        
        cursor.execute(sql, valores)
        conn.commit() # Confirma a gravação
        
        cursor.close()
        conn.close()
        
        return "<h1>Sucesso! Aluno cadastrado.</h1> <a href='/'>Voltar</a>"

    except mysql.connector.Error as err:
        return f"<h1>Erro no Banco de Dados:</h1> <p>{err}</p>"
    except Exception as e:
        return f"<h1>Erro Geral:</h1> <p>{e}</p>"

if __name__ == '__main__':
    app.run(debug=True)