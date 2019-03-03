import json
import csv
from watson_developer_cloud import AssistantV1,WatsonApiException
from dotenv import load_dotenv
import os

global assistantV1
try:
    load_dotenv('test.env')
    ASSISTANT_APIKEY = os.getenv("ASSISTANT_APIKEY")
    ASSISTANT_URL = os.getenv("ASSISTANT_URL")
    ASSISTANT_VERSION = os.getenv("ASSISTANT_VERSION")
    WORKSPACE_ID = os.getenv("WORKSPACE_ID")
    print(ASSISTANT_APIKEY)
except RuntimeError as e:
    print("File '.env' doesn't exist")

def import_csv():
    with open('watson.csv', newline='') as csvfile:
        watsonreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in watsonreader:
            print(', '.join(row))

def create_connection():
    global assistantV1
    assistantV1=AssistantV1(
        iam_apikey=ASSISTANT_APIKEY,
        version='2018-09-20',
        url=ASSISTANT_URL
    )
    print("Connected")

def create_intent():
    response=assistantV1.create_intent(
        workspace_id=WORKSPACE_ID,
        intent='hello',
        examples=[
            {'text': 'Good morning'},
            {'text': 'Hi there'}
        ]
    ).get_result()
    print(json.dumps(response, indent=2))

def update_intent():
    response=assistantV1.update_intent(
        workspace_id=WORKSPACE_ID,
        intent='hello',
        new_examples=[
            {'text': 'Good afternoon'}
        ],
        new_description='Updated intent'
    ).get_result()
    print(json.dumps(response, indent=2))

def create_entity():
    response=assistantV1.create_entity(
        workspace_id=WORKSPACE_ID,
        entity='beverage',
        values=[
            {'value': 'water'},
            {'value': 'orange juice'},
            {'value': 'soda'}
        ]
    ).get_result()
    print(json.dumps(response, indent=2))

def get_synonym():
    response=assistantV1.list_synonyms(
        workspace_id=WORKSPACE_ID,
        entity='beverage',
        value='soda'
    ).get_result()
    print('Synonym List:')
    print(json.dumps(response, indent=2))

def create_synonym():
    try:
        response=assistantV1.create_synonym(
            workspace_id=WORKSPACE_ID,
            entity='beverage',
            value='orange juice',
            synonym='OJ'
        ).get_result()
        print("Synonym creating:")
        print(json.dumps(response, indent=2))
    except WatsonApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)

        


def create_node():
    response=assistantV1.create_dialog_node(
        workspace_id=WORKSPACE_ID,
        dialog_node='greeting',
        conditions='#hello',
        output={
            'text': 'Hi! How can I help you?'
        },
        title='Greeting'
    ).get_result()
    print(json.dumps(response, indent=2))



if __name__ == "__main__":
    try:
        create_connection()
        #create_entity()
        #create_intent()
        #create_node()
        get_synonym()
        create_synonym()
    except Exception as e:
        print(e)