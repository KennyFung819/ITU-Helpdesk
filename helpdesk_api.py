# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:38:11 2019

@author: Kenny
"""
from flask import Flask
from flask import request
import urllib.request,json
import watson_developer_cloud
from watson_developer_cloud import WatsonApiException
import credentials
app = Flask(__name__)
global assistant
def connection():
    try:
        global assistant,session_id
        assistant=watson_developer_cloud.AssistantV2(
            iam_apikey=credentials.ASSISTANT_APIKEY,
            version=credentials.ASSISTANT_VERSION,
            url=credentials.ASSISTANT_URL
        )
        print("Connected")
        response = assistant.create_session(
            assistant_id=credentials.ASSISTANT_ID
        ).get_result()
        session_id = response['session_id']
        print(session_id)
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)


@app.route('/')
def index():
    return 'Hello, World!' 

	
@app.route('/translate',methods=['POST'])
def translate():
	return 'Translation Service Not avaiable Yet!'
	
@app.route('/input',methods=['POST'])
def userInput():
    try:
        if request.method == 'POST':
            input_text = request.form['user_input']
#            input_text = "Hello"
            global assistant,session_id
            response = assistant.message(
                assistant_id=credentials.ASSISTANT_ID,
                session_id= session_id,
                input={
                    'message_type': 'text',
                    'text': input_text
                }
            ).get_result()
            print(json.dumps(response, indent=2))
            output_text = response['text']
            return output_text
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        
                
if __name__== '__main__':
    try:
        connection()
        userInput()
#        app.run(
#            host = '0.0.0.0',
#            port = 3001
#        )
    except Exception as e:
        print(e)