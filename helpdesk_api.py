# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:38:11 2019

@author: Kenny
"""
# Import all the lib
from flask import Flask, request, make_response, render_template, redirect, json, session
from dotenv import load_dotenv
from datetime import timedelta
from watson_developer_cloud import WatsonApiException, AssistantV2, LanguageTranslatorV3
import os

global watsonAssistant
# Init variable
app = Flask(__name__)
app.secret_key = 'ITU-helpdesk'
# This should set the session timeout limited to 5 mins, which is same with IBM assistant
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

try:
    load_dotenv('.env')
    ASSISTANT_APIKEY = os.getenv("ASSISTANT_APIKEY")
    ASSISTANT_URL = os.getenv("ASSISTANT_URL")
    ASSISTANT_VERSION = os.getenv("ASSISTANT_VERSION")
    ASSISTANT_ID = os.getenv("ASSISTANT_ID")
    LANGUAGE_TRANSLATOR_APIKEY = os.getenv("LANGUAGE_TRANSLATOR_APIKEY")
    LANGUAGE_TRANSLATOR_URL = os.getenv("LANGUAGE_TRANSLATOR_URL")
    LANGUAGE_TRANSLATOR_VERSION = os.getenv("LANGUAGE_TRANSLATOR_VERSION")
except RuntimeError as e:
    print("File '.env' doesn't exist")


@app.route('/createConnection')
def create_connection():
    try:
        global watsonAssistant
        watsonAssistant = AssistantV2(
            iam_apikey=ASSISTANT_APIKEY,
            version=ASSISTANT_VERSION,
            url=ASSISTANT_URL
        )
        print("Connected To IBM server")
        return watsonAssistant
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service unavailable (connection)"


@app.route('/', methods=['GET'])
def home():
    resp = redirect('/index')
    return resp


@app.route('/index', methods=['GET'])
def index():
    global watsonAssistant
    resp = make_response(render_template("chatbot.html"))
    if not ('session_id' in session):
        print("Session Request by index")
        session['session_id'] = create_session(watsonAssistant)
    return resp


@app.route('/createSession')
def create_session(watson_assistant):
    try:
        session.permanent = True
        response = watson_assistant.create_session(
            assistant_id=ASSISTANT_ID
        ).get_result()
        session_id = response['session_id']
        print("Generating Session...")
        print("Created Session:" + session_id)
        return session_id
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service unavailable (Session)"


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        try:
            before_translate_text = request.get_json()
            print(before_translate_text)
            target = before_translate_text['text']
            model_id = before_translate_text['model_id']
            print(target)
            print(model_id)
            helpdesk_translator = LanguageTranslatorV3(
                iam_apikey=LANGUAGE_TRANSLATOR_APIKEY,
                url=LANGUAGE_TRANSLATOR_URL,
                version=LANGUAGE_TRANSLATOR_VERSION
            )
            print("Connected To Translator")
            translation = helpdesk_translator.translate(
                text=target,
                model_id=model_id).get_result()
            print(json.dumps(translation, indent=2, ensure_ascii=False))
            translate_lists = translation["translations"][0]
            output_text = translate_lists["translation"]
            print(output_text)
            return output_text
        except WatsonApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    else:
        return 'Translation service not available yet!'
        
@app.route('/detect_language',method=['POST'])
def identify_language():
    helpdesk_translator = LanguageTranslatorV3(
        iam_apikey=LANGUAGE_TRANSLATOR_APIKEY,
        url=LANGUAGE_TRANSLATOR_URL,
        version=LANGUAGE_TRANSLATOR_VERSION
    )
    language = helpdesk_translator.identify(
    'Language translator translates text from one language to another').get_result()
    print(json.dumps(language, indent=2))

@app.route('/cantoneseTranslate', methods=['GET', 'POST'])
def cantonese_translate():
    if request.method == 'POST':
        return "Doing"

@app.route('/input', methods=['GET', 'POST'])
def user_input():
    try:
        global watsonAssistant
        if request.method == 'POST':
            if not ('session_id' in session):
                session['session_id'] = create_session(watsonAssistant)
                print("Generating Session in /input")
            else:
                session['session_id'] = session['session_id']
                print('Session renew by user iput.')
                print('ID:' + session['session_id'])
            input_data = request.get_json()
            print(input_data)
            input_text = input_data['user_input']
            print(input_text)
            # Initalize welcome
            if input_text == 'initalize-welcome':
                if not ('Greeting' in session):
                    response = watsonAssistant.message(
                        assistant_id=ASSISTANT_ID,
                        session_id=session['session_id'],
                        input={}
                    ).get_result()
                    session['Greeting'] = True
                else:
                    welcome_back = [{'response_type': 'text', 'text': 'Welcome Back.'}]
                    resp = json.jsonify(welcome_back)
                    return resp
            # Normal input
            else:
                response = watsonAssistant.message(
                    assistant_id=ASSISTANT_ID,
                    session_id=session['session_id'],
                    input={
                        'message_type': 'text',
                        'text': "'" + input_text + "'"
                    }
                ).get_result()
            print(json.dumps(response, indent=2))
            response_lists = response['output']['generic']
            print(response_lists)
            resp = json.jsonify(response_lists)
            return resp
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service unavailable (Connection)"


if __name__ == '__main__':
    try:
        watsonAssistant = create_connection()
        app.run(
            host='127.0.0.1',
            port=1234,
            debug=True
        )
    except Exception as e:
        print(e)
