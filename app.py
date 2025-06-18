from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'secret123'

# 問題を読み込み・構造化
def load_questions():
    questions = []
    with open('questions.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    blocks = data.strip().split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        question = lines[0]
        options = []
        correct_index = -1
        for i, line in enumerate(lines[1:]):
            option = line.replace('*', '').strip()
            options.append(option)
            if '*' in line:
                correct_index = i
        questions.append({
            'question': question,
            'options': options,
            'answer': correct_index
        })
    return questions

QUESTIONS = load_questions()

@app.route('/')
def index():
    session['answers'] = []
    return render_template('index.html')

@app.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if request.method == 'POST':
        choice = int(request.form['choice'])
        session['answers'].append(choice)
        if qid + 1 < len(QUESTIONS):
            return redirect(url_for('question', qid=qid+1))
        else:
            return redirect(url_for('result'))

    return render_template('question.html', qid=qid, question=QUESTIONS[qid])

@app.route('/result')
def result():
    answers = session.get('answers', [])
    correct = 0
    for user_ans, q in zip(answers, QUESTIONS):
        if user_ans == q['answer']:
            correct += 1
    return render_template('result.html', total=len(QUESTIONS), correct=correct)

if __name__ == '__main__':
    app.run(debug=True)
