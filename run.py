# main Flask application
from flask import Flask, render_template, request, session, jsonify
from model.gpt_interpreter import GPTInterpreter
from googletrans import Translator
from utils.languages import LANGUAGES


app = Flask(__name__)
app.secret_key = 'gpt-test'
interpreter = GPTInterpreter('gpt2')
translator = Translator()

@app.route('/', methods=['GET'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', chat_history=session['chat_history'], languages=LANGUAGES, selected_language='en')


@app.route('/ask', methods=['POST'])
def ask():
    original_question = request.form.get('question')
    target_language = request.form.get('language', 'en')
    translated_question = translator.translate(original_question, src=target_language, dest='en').text if target_language != 'en' else original_question

    answer = interpreter.interpret_text(translated_question)
    translated_answer = translator.translate(answer, src='en', dest=target_language).text if target_language != 'en' else answer

    session['chat_history'].append({'question': original_question, 'answer': translated_answer})
    session.modified = True
    
    return jsonify({'question': original_question, 'answer': translated_answer})


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    session.modified = True
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
