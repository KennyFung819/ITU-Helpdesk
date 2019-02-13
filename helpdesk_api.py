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

# This should set the session timeout limited to 5 mins, which is same with IBM assistant
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/createConnection')
def create_connection():
    try:
        global watsonAssistant
        watsonAssistant = AssistantV2(
            iam_apikey=ASSISTANT_APIKEY,
            version=ASSISTANT_VERSION,
            url=ASSISTANT_URL
        )
        print("Connected")
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
    if not('session_id' in session):
        session['session_id'] = create_session(watsonAssistant)
    return resp


@app.route('/createSession')
def create_session(watson_assistant):
    try:
        response = watson_assistant.create_session(
            assistant_id=ASSISTANT_ID
        ).get_result()
        session_id = response['session_id']
        print("Created Session:"+session_id)
        return session_id
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service unavailable (Session)"


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        output_text = []
        try:
            before_translate_text = request.form['translateText']
            helpdesk_translator = LanguageTranslatorV3(
                iam_apikey=LANGUAGE_TRANSLATOR_APIKEY,
                url=LANGUAGE_TRANSLATOR_URL,
                version=LANGUAGE_TRANSLATOR_VERSION
            )
            translation = helpdesk_translator.translate(
                text=before_translate_text,
                model_id='en-us').get_result()
            translate_lists = translation["translations"]
            for translate_list in translate_lists:
                output_text = translate_list["translation"]
                print(output_text)
            print(json.dumps(translation, indent=2, ensure_ascii=False))
            return output_text
        except WatsonApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    else:
        return 'Translation service not available yet!'


@app.route('/cantoneseTranslate', methods=['GET', 'POST'])
def cantonese_translate():
    if request.method == 'POST':
        return "Doing"


@app.route('/voiceToText', methods=['POST'])
def voice_to_text():
    return "Working in progress"


@app.route('/input', methods=['GET', 'POST'])
def user_input():
    try:
        global watsonAssistant
        if request.method == 'POST':
            if not('session_id' in session):
                session['session_id'] = create_session(watsonAssistant)
            else:
                session['session_id'] = session['session_id']
            input_data = request.get_json()
            print(input_data)
            input_text = input_data['user_input']
            print(input_text)
            # Initalize welcome
            if input_text == 'initalize-welcome':
                response = watsonAssistant.message(
                    assistant_id=ASSISTANT_ID,
                    session_id=session['session_id'],
                    input={}
                ).get_result()
            # Normal input
            else:
                response = watsonAssistant.message(
                    assistant_id=ASSISTANT_ID,
                    session_id=session['session_id'],
                    input={
                        'message_type': 'text',
                        'text': "'"+input_text+"'"
                    }
                ).get_result()
            print(json.dumps(response, indent=2))
            response_lists = response['output']['generic']
#           for oneList in response_lists:
#               output_text = oneList["text"] 
            resp = json.jsonify(response_lists)
            print(json.jsonify(response_lists))
            return resp
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service unavailable (Connection)"
        

if __name__ == '__main__':
    try:
        watsonAssistant = create_connection()
        app.run(
            host='127.0.0.1',
            port=80,
            debug=True
        )
    except Exception as e:
        print(e)
