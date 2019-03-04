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

#import the example.csv and output as ???
def import_csv():
    with open('example.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        fields = csvreader.fieldnames
        payload = [row for row in csvreader]
    return payload, fields

#controller which function should be use
def csv_controller():
    payload, field_name = import_csv()
    print(field_name)
    for payload_dict in payload:
        print(payload_dict)
        print(payload_dict['type'].lower())        
        
        #types = payload_dict['type'].lower()
        # if types == 'intent':
        #     intent_value = [{'text':payload_dict['intent_value']}] 
        #     create_intent(payload_dict['intent_name'],intent_value)
        # if types == 'entity':
        #     create_entity()
        # if types == 'synonym':
        #     create_synonym()
        # if types == 'node':
        #     create_synonym()
        


#create connection to watson server
def create_connection():
    global assistantV1
    assistantV1=AssistantV1(
        iam_apikey=ASSISTANT_APIKEY,
        version='2018-09-20',
        url=ASSISTANT_URL
    )
    print("Connected")

#list all the existing intent
def list_intent():
    response=assistantV1.list_intents(
        workspace_id=WORKSPACE_ID
    ).get_result()
    print(json.dumps(response, indent=2))

#get the selected intent
def get_intent(intent):
    response=assistantV1.get_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        export=True
    ).get_result()
    print(json.dumps(response, indent=2))

#create a new intent
def create_intent(intent,new_examples):
    response=assistantV1.create_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        examples= new_examples
    ).get_result()
    print(json.dumps(response, indent=2))

#update the whole intent
def update_intent(intent,new_examples):
    response=assistantV1.update_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        new_examples=new_examples,
        new_description='Updated intent'
    ).get_result()
    print(json.dumps(response, indent=2))

#list all the existing entity
def list_entity():
    response=assistantV1.list_entities(
        workspace_id=WORKSPACE_ID
    ).get_result()
    print(json.dumps(response, indent=2))

#get the selected intent
def get_entity(entity):
    response=assistantV1.get_entity(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        export=True
    ).get_result()
    print(json.dumps(response, indent=2))

#create a new entity
def create_entity(entity,values):
    response=assistantV1.create_entity(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        values=values
    ).get_result()
    print(json.dumps(response, indent=2))

#update the whole entity list
def update_entity():
    response=assistantV1.update_entity(
        workspace_id=WORKSPACE_ID,
        entity='beverage',
        new_values=[
            {'value': 'water'},
            {'value': 'orange juice'},
            {'value': 'soda'}
        ]
    ).get_result()
    print(json.dumps(response, indent=2))


#create a new synonym for entity
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

#create a new dialog node
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

#update the selected dialog node
def update_node():
    response=assistant.update_dialog_node(
        workspace_id='{workspace_id}',
        dialog_node='greeting',
        new_output={
            'text': 'Hello! What can I do for you?'
        }
    ).get_result()
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    try:
        #create_connection()
        #create_entity()
        #update_intent('hello',[{'text':'good evening'}] )
        #update_entity()
        #create_node()
        #get_synonym()
        #create_synonym()
        csv_controller()
    except Exception as e:
        print(e)