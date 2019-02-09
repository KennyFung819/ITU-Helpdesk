# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:38:11 2019

@author: Kenny
"""
#Import all the lib
from flask import Flask
from flask import request
from flask import make_response
from dotenv import load_dotenv
from watson_developer_cloud import WatsonApiException
from watson_developer_cloud import AssistantV2
from watson_developer_cloud import LanguageTranslatorV3
from watson_developer_cloud import SpeechToTextV1
import urllib.request,json,os

global assistant,session_id
session_id = ''
#init variable
app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__), '..') 
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
ASSISTANT_APIKEY = os.getenv("ASSISTANT_APIKEY")
ASSISTANT_URL = os.getenv("ASSISTANT_URL")
ASSISTANT_VERSION = os.getenv("ASSISTANT_VERSION")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
LANGUAGE_TRANSLATOR_APIKEY = os.getenv("LANGUAGE_TRANSLATOR_APIKEY")
LANGUAGE_TRANSLATOR_URL = os.getenv("LANGUAGE_TRANSLATOR_URL")
LANGUAGE_TRANSLATOR_VERSION = os.getenv("LANGUAGE_TRANSLATOR_VERSION")



@app.route('/')
def index():
    return 'Hello, World!' 

@app.route('/createConnection')
def createConnection():
    try:
        global assistant
        assistant=AssistantV2(
            iam_apikey=ASSISTANT_APIKEY,
            version=ASSISTANT_VERSION,
            url=ASSISTANT_URL
        )
        print("Connected")

    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)

@app.route('/createSession')
def createSession():
    try:
        global assistant,session_id
        response = assistant.create_session(
            assistant_id=ASSISTANT_ID
        ).get_result()
        session_id = response['session_id']
        print("Created Session:"+session_id)
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)

@app.route('/translate',methods=['GET','POST'])
def translate():
    if request.method == 'POST':
        try:
            beforeTranslateText = request.form['translateText']
            helpdesk_translator = LanguageTranslatorV3(
                iam_apikey= LANGUAGE_TRANSLATOR_APIKEY,
                url= LANGUAGE_TRANSLATOR_URL,
                version= LANGUAGE_TRANSLATOR_VERSION
            )
            translation = helpdesk_translator.translate(
                text=beforeTranslateText,
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
	    return 'Translation Service Not avaiable Yet!'

@app.route('/cantoneseTranslate',methods=['GET','POST'])
def cantoneseTranslate():
    if request_method == 'POST':
        return ("Doing")

@app.route('/voiceToText',methods=['POST'])
def voiceTotext():
    return("Working in Progress")

@app.route('/input',methods=['GET','POST'])
def userInput():
    try:
        if request.method == 'POST':
            input_text = request.form['user_input']
            global assistant,session_id
            response = assistant.message(
                assistant_id=ASSISTANT_ID,
                session_id= session_id,
                input={
                    'message_type': 'text',
                    'text': input_text
                }
            ).get_result()
            print(json.dumps(response, indent=2))
            response_lists = response['output']['generic']
            for oneList in response_lists:
                output_text = oneList["text"] 
            return output_text
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        
                
if __name__== '__main__':
    try:
        createConnection()
        #resp = make_response(render_template(...))
        #resp.set_cookie('session_id', session_id)
        if not 'session_id' in request.cookies:
            createSession()
        app.run(
            host = '127.0.0.1',
            port = 3001,
            debug = True
        )
    except Exception as e:
        print(e)