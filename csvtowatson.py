import json
import csv
from watson_developer_cloud import AssistantV1,WatsonApiException
from dotenv import load_dotenv
import os
global assistantV1
global csv_file
csv_file = 'example.csv'
try:
    load_dotenv('.env')
    ASSISTANT_APIKEY = os.getenv("ASSISTANT_APIKEY")
    ASSISTANT_URL = os.getenv("ASSISTANT_URL")
    ASSISTANT_VERSION = os.getenv("ASSISTANT_VERSION")
    WORKSPACE_ID = os.getenv("WORKSPACE_ID")
    print(ASSISTANT_APIKEY)
except RuntimeError as e:
    print("File '.env' doesn't exist")

#**create connection to watson server
def create_connection():
    global assistantV1
    assistantV1=AssistantV1(
        iam_apikey=ASSISTANT_APIKEY,
        version='2018-09-20',
        url=ASSISTANT_URL
    )
    print("Connected")

#*list all the existing intent
def list_intent():
    intent_index = []
    response=assistantV1.list_intents(
        workspace_id=WORKSPACE_ID
    ).get_result()
    for item in response['intents']:
        intent_index.append(item['intent'])
    #return the dict   
    print('Initalize the intent_list') 
    return intent_index

#*add text to intent
def add_intent_text(intent,text):
    print("Add the text:", text , "to intent:" , intent)    
    response=assistantV1.create_example(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        text=text
    ).get_result()
    print(json.dumps(response, indent=2))

#*create a new intent
def create_intent(intent,new_examples):
    try:
        response=assistantV1.create_intent(
            workspace_id=WORKSPACE_ID,
            intent=intent,
            examples= [{'text':new_examples}]
        ).get_result()
        print(json.dumps(response, indent=2))
    except WatsonApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)

#*Initalize entities dict
def list_entity():
    entities_index = []
    response=assistantV1.list_entities(
        workspace_id=WORKSPACE_ID
    ).get_result()
    for item in response['entities']:
        entities_index.append(item['entity'])
    #return the dict   
    print('Initalize the entities_list') 
    return entities_index

#*create a new entity
def create_entity(entity,values):
    response=assistantV1.create_entity(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        values=[{'value':values}]
    ).get_result()
    print(json.dumps(response, indent=2))

#*add value to entity
def add_entity_value(entity,value):
    print("Adding value:{0} into entity: {1}".format(value,entity))
    response=assistantV1.create_value(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        value=value
    ).get_result()
    print(json.dumps(response, indent=2))   

#*create a new synonym for entity 
def create_synonym(entity,value,synonym):
    response=assistantV1.create_synonym(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        value=value,
        synonym=synonym
    ).get_result()
    print("Synonym created:")
    print(json.dumps(response, indent=2))

#*create a new dialog node
def create_node(condition,node_name,title,node_value):
    response=assistantV1.create_dialog_node(
        workspace_id=WORKSPACE_ID,
        dialog_node=node_name,
        conditions= '#'+condition,
        output={
            'text': node_value
        },
        title=title
    ).get_result()
    print("Respone",json.dumps(response, indent=2))

#Intent Controller
def intent_controller(intent_name,text,intent_index):
    #variable
    if intent_name in intent_index:
        print('Existing Intent:{0} ,insert Text: "{1}"'.format(intent_name,text))
        add_intent_text(intent_name,text)
    else:
        print('New Intent:{0} ,with Text: "{1}"'.format(intent_name,text))
        create_intent(intent_name,text)
        intent_index.append(intent_name)
    return intent_index

#entity Controller
def entity_controller(entity_name,value,entity_index):
    #variable
    if entity_name in entity_index:
        print('Existing Entity:{0} ,insert value: "{1}"'.format(entity_index,value))
        add_entity_value(entity_name,value)
    else:
        print('New Entity:{0} ,with value: "{1}"'.format(entity_index,value))        
        create_entity(entity_name,value)
        entity_index.append(entity_name)
    return entity_index
    
#import the example.csv and output as ???
def import_csv(file_path):
    with open(file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        fields = csvreader.fieldnames
        payload = [row for row in csvreader]
        print(type(payload))
    return payload, fields

#controller which function should be use
def csv_controller():
    payload, field_name = import_csv(csv_file)
    exist_intent_index = list_intent()
    exist_entity_index= list_entity()
    print("Header: ",field_name)
    for payload_dict in payload:
        try:
            types = payload_dict['type'].lower()
            print('Types:',types)   
            if types == 'intent':
                intent_name = payload_dict['intent_name']
                intent_value = payload_dict['value']
                exist_intent_index = intent_controller(intent_name,intent_value,exist_intent_index)
            if types == 'entity':
                entity_name = payload_dict['entity_name']
                entity_value = payload_dict['value']
                exist_entity_index = entity_controller(entity_name,entity_value,exist_entity_index)
            if types == 'synonym':
                entity_name = payload_dict['entity_name']
                entity_value = payload_dict['entity_value']
                synoym_value = payload_dict['value']
                create_synonym(entity_name,entity_value,synoym_value)
            if types == 'node':
                print("Node function")
                condition = payload_dict['intent_name']
                node_name = payload_dict['node_name']
                title = payload_dict['node_title']
                node_value= payload_dict['value']
                print("Condition: {0}; Entity: {1}; synonym: {2}; Value: {3}".format(condition,node_name,title,node_value))
                create_node(condition,node_name,title,node_value)
        except WatsonApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + ex.message)


if __name__ == "__main__":
    try:
        while "the answer is invalid":
            print("Please comfirm that {0} is the file you want to insert!".format(csv_file))
            reply = str(input('Comfirm to insert data into Watson Assistant? (y/n): ')).lower().strip()
            if reply[0] == 'y':
                create_connection()
                csv_controller()
            if reply[0] == 'n':
                print("This program is shutting down!")
                break
    except Exception as e:
        print(e)