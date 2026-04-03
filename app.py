from flask import Flask, render_template, request, redirect
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id SERIAL PRIMARY KEY,
            name TEXT
        )
    """)

    cur.execute("INSERT INTO students(name) VALUES(%s)", (name,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/students")

@app.route("/students")
def students():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("students.html", students=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))