from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extras


CREATE_PESSOA_TABLE = (
    "CREATE TABLE IF NOT EXISTS pessoa(id SERIAL PRIMARY KEY, nome TEXT, sobrenome TEXT);"
)
INSERT_PESSOA_RETURN_ID = "INSERT INTO pessoa (nome, sobrenome) VALUES (%s, %s) RETURNING id;" 


load_dotenv()
url = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.secret_key="paulo"
#configurações do banco de dados
db_connection = psycopg2.connect(url)
   
  # dbname = "mydb01",
  #  user = "postgres",
  #  password = "admin",
  #  host = "localhost"
    
   

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_form", methods=["POST"])
def subtmit_form():
    if request.method == "POST":
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        cursor = db_connection.cursor()
        cursor.execute(CREATE_PESSOA_TABLE)
        cursor.execute(INSERT_PESSOA_RETURN_ID, (nome, sobrenome))
        db_connection.commit()
        cursor.close()
        flash("Formulario enviado com sucesso!")
        return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug=True)