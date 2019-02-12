# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:38:11 2019

@author: Kenny
"""
#Import all the lib
from flask import Flask,request,make_response,render_template,redirect,json,session
from dotenv import load_dotenv
from datetime import timedelta
from watson_developer_cloud import WatsonApiException, AssistantV2,LanguageTranslatorV3, SpeechToTextV1
import urllib,os

global watsonAssistant
#init variable
app = Flask(__name__)
app.secret_key = 'ITU-helpdesk'
load_dotenv('.env')
ASSISTANT_APIKEY = os.getenv("ASSISTANT_APIKEY")
ASSISTANT_URL = os.getenv("ASSISTANT_URL")
ASSISTANT_VERSION = os.getenv("ASSISTANT_VERSION")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
LANGUAGE_TRANSLATOR_APIKEY = os.getenv("LANGUAGE_TRANSLATOR_APIKEY")
LANGUAGE_TRANSLATOR_URL = os.getenv("LANGUAGE_TRANSLATOR_URL")
LANGUAGE_TRANSLATOR_VERSION = os.getenv("LANGUAGE_TRANSLATOR_VERSION")

#This should set the session timeout limited to 5mins, which is same with IBM assistant
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/createConnection')
def createConnection():
    try:
        global watsonAssistant
        watsonAssistant=AssistantV2(
            iam_apikey=ASSISTANT_APIKEY,
            version=ASSISTANT_VERSION,
            url=ASSISTANT_URL
        )
        print("Connected")
        return watsonAssistant
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service Unavalible (Connection)"

@app.route('/',methods=['GET'])
def home():
    resp = redirect('/index')
    return resp

@app.route('/index',methods=['GET'])
def index():
    global watsonAssistant
    resp = make_response(render_template("chatbot.html"))
    if not 'session_id' in session:
        session['session_id'] = createSession(watsonAssistant)
    return resp 

@app.route('/createSession')
def createSession(watsonAssistant):
    try:
        response = watsonAssistant.create_session(
            assistant_id=ASSISTANT_ID
        ).get_result()
        session_id = response['session_id']
        print("Created Session:"+session_id)
        return session_id
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return "Service Unavalible (Session)"


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
    if request.method == 'POST':
        return ("Doing")

@app.route('/voiceToText',methods=['POST'])
def voiceTotext():
    return("Working in Progress")

@app.route('/input',methods=['GET','POST'])
def userInput():
    try:
        global watsonAssistant
        if request.method == 'POST':
            if not 'session_id' in request.cookies:
                session['session_id'] = createSession(watsonAssistant)
            else:
                session['session_id'] = request.cookies['session_id']
            input_data = request.get_json()
            print(input_data)
            input_text = input_data['user_input']
            print(input_text)
            #initalize-welcome
            if (input_text=='initalize-welcome'):
                response = watsonAssistant.message(
                    assistant_id=ASSISTANT_ID,
                    session_id= session['session_id'],
                    input={}
                ).get_result()
            #Normal input
            else:
                response = watsonAssistant.message(
                    assistant_id=ASSISTANT_ID,
                    session_id= session['session_id'],
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
        return "Service Unavalible (Connection)"
        


if __name__== '__main__':
    try:
        watsonAssistant = createConnection()
        app.run(
            host = '127.0.0.1',
            port = 80,
            debug = True
        )
    except Exception as e:
        print(e)