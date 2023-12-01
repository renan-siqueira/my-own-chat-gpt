from flask import Flask, render_template, request, session
from model.gpt_interpreter import GPTInterpreter

app = Flask(__name__)
app.secret_key = 'gpt-test'
interpreter = GPTInterpreter('gpt2')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    print(session['chat_history'])

    if request.method == 'POST':
        question = request.form['question']
        answer = interpreter.interpret_text(question)
        session['chat_history'].append({'question': question, 'answer': answer})
        session.modified = True
        return render_template('index.html', chat_history=session['chat_history'])
    
    return render_template('index.html', chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)
