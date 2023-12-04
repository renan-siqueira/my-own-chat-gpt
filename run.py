# main Flask application
from flask import Flask, render_template, request, session, redirect, url_for
from model.gpt_interpreter import GPTInterpreter
from googletrans import Translator
from utils.languages import LANGUAGES


app = Flask(__name__)
app.secret_key = 'gpt-test'
interpreter = GPTInterpreter('gpt2')
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        original_question = request.form['question']
        target_language = request.form.get('language', None)

        translated_question = translator.translate(original_question, src=target_language, dest='en').text if target_language != 'en' else original_question
        print(translated_question)
        
        answer = interpreter.interpret_text(translated_question)

        print(answer)

        translated_answer = translator.translate(answer, src='en', dest=target_language).text if target_language != 'en' else answer

        session['chat_history'].append({'question': original_question, 'answer': translated_answer})
        session.modified = True
        return render_template('index.html', chat_history=session['chat_history'], languages=LANGUAGES, selected_language=target_language)

    return render_template('index.html', chat_history=session['chat_history'], languages=LANGUAGES, selected_language='en')


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
