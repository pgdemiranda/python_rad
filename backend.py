import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect():
    """Conecta ao banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def read_students():
    """Lê todos os alunos da tabela 'alunos'."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos")
    rows = cur.fetchall()
    conn.close()
    return rows

def create_student(matricula, cpf, nome, idade, email, curso, ano_conclusao, 
                   periodo_conclusao, situacao, telefone_celular, sexo, raca):
    """Insere um novo aluno na tabela 'alunos'."""
    conn = connect()
    cur = conn.cursor()
    query = """
    INSERT INTO alunos (matricula, cpf, nome, idade, email, curso, ano_conclusao, 
                        periodo_conclusao, situacao, telefone_celular, sexo, raca) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (matricula, cpf, nome, idade, email, curso, ano_conclusao, 
                        periodo_conclusao, situacao, telefone_celular, sexo, raca))
    conn.commit()
    conn.close()

def delete_students(ids):
    """Exclui alunos da tabela 'alunos' com base em uma lista de IDs."""
    conn = connect()
    cur = conn.cursor()

    ids = [int(id) for id in ids]
    
    query = "DELETE FROM alunos WHERE id = ANY(%s)"
    cur.execute(query, (ids,))
    conn.commit()
    conn.close()

def update_student(id, matricula, cpf, nome, idade, email, curso, ano_conclusao, 
                   periodo_conclusao, situacao, telefone_celular, sexo, raca):
    """Atualiza os dados de um aluno na tabela 'alunos'."""
    conn = connect()
    cur = conn.cursor()
    query = """
    UPDATE alunos
    SET matricula = %s, cpf = %s, nome = %s, idade = %s, email = %s, curso = %s,
        ano_conclusao = %s, periodo_conclusao = %s, situacao = %s, telefone_celular = %s,
        sexo = %s, raca = %s
    WHERE id = %s
    """
    cur.execute(query, (matricula, cpf, nome, idade, email, curso, ano_conclusao, 
                        periodo_conclusao, situacao, telefone_celular, sexo, raca, id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(read_students())
