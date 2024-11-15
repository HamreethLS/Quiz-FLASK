from flask import Flask, render_template, request, redirect, url_for, session
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Change this to a random secret key

# Sample quiz data
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Madrid', 'Paris', 'Lisbon'],
        'answer': 'Paris'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'options': ['Atlantic', 'Indian', 'Arctic', 'Pacific'],
        'answer': 'Pacific'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    random.shuffle(questions)  # Shuffle questions for each quiz attempt
    session['score'] = 0
    session['question_index'] = 0
    return render_template('quiz.html', question=questions[0], question_index=0)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_option = request.form.get('option')
    question_index = session['question_index']
    
    if selected_option == questions[question_index]['answer']:
        session['score'] += 1
    
    session['question_index'] += 1
    
    if session['question_index'] < len(questions):
        return render_template('quiz.html', question=questions[session['question_index']], question_index=session['question_index'])
    else:
        score = session['score']
        session.clear()  # Clear session after quiz
        return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)