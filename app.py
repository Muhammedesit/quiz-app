from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form
    score = 0
    conn = get_db_connection()
    for question_id, user_answer in answers.items():
        correct_answer = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (question_id,)).fetchone()
        if user_answer == correct_answer['correct_answer']:
            score += 1
    conn.close()
    return jsonify({'score': f'{score}/{len(answers)}'})

if __name__ == '__main__':
    app.run(debug=True)
