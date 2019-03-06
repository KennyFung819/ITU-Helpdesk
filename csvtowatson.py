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
def list_intent(intent_index):
    response=assistantV1.list_intents(
        workspace_id=WORKSPACE_ID
    ).get_result()
    for item in response['intents']:
        #put intent name into dict
        intent_index.update({item['intent']:{}})
    #return the dict   
    print('Initalize the intent_list') 
    return intent_index

#*add text to intent
def add_intent_text(intent,text):
    print("Add the text:", text , "to intent:" , intent)    
    response=assistantV1.create_example(
        workspace_id=WORKSPACE_ID,
        intent='hello',
        text=text
    ).get_result()
    print(json.dumps(response, indent=2))

#get the selected intent
def get_intent(intent,intent_dict):
    response=assistantV1.get_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        export=True
    ).get_result()
    intent_dict.update({intent:response['examples']})
    print('Updated dict with ',intent)
    return intent_dict

#*create a new intent
def create_intent(intent,new_examples):
    response=assistantV1.create_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        examples= new_examples
    ).get_result()
    print(json.dumps(response, indent=2))

#update the whole intent
def update_intent(intent,updated_dict):
    new_examples = updated_dict[intent]
    response=assistantV1.update_intent(
        workspace_id=WORKSPACE_ID,
        intent=intent,
        new_examples=new_examples
    ).get_result()
    print(json.dumps(response, indent=2))

#*Initalize entities dict
def list_entity(entities_index):
    response=assistantV1.list_entities(
        workspace_id=WORKSPACE_ID
    ).get_result()
    for item in response['entities']:
        #put intent name into dict
        entities_index.update({item['entity']:{}})
    #return the dict   
    print('Initalize the entities_list') 
    return entities_index

#get the selected entity
def get_entity(entity,entities_dict):
    response=assistantV1.get_entity(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        export=True
    ).get_result()
    print(json.dumps(response, indent=2))
    entities_dict.update({entity:response['values']})
    """
    "values": [
    {
      "type": "synonyms",
      "value": "water",
      "synonyms": []
    }]
    """
    print("Updating entity",entity)
    return entities_dict

#*create a new entity
def create_entity(entity,values):
    response=assistantV1.create_entity(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        values=values
    ).get_result()
    print(json.dumps(response, indent=2))

#*add value to entity
def add_entity_value(entity,value):
    print("Adding value:% into entity: %",value , entity)
    response=assistantV1.create_value(
        workspace_id=WORKSPACE_ID,
        entity=entity,
        value=value
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

#*create a new synonym for entity
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

#*create a new dialog node
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

#*update the selected dialog node
def update_node():
    response=assistantV1.update_dialog_node(
        workspace_id='{workspace_id}',
        dialog_node='greeting',
        new_output={
            'text': 'Hello! What can I do for you?'
        }
    ).get_result()
    print(json.dumps(response, indent=2))

#sample 2
def update_intent_sample_2():
    #variable
    intent_name = 'General_About_You'
    text = 'Easier Method!!!'
    add_intent_text(intent_name,text)
  
#controller example for intent
def update_intent_sample():
    #variable
    intent_name = 'General_About_You'
    exist_intent_dict = {}
    # initalize the list
    exist_intent_dict = list_intent(exist_intent_dict)
    # get the select intent from Watson
    exist_intent_dict = get_intent(intent_name,exist_intent_dict)
    # update the list of that intent
    update_list = exist_intent_dict[intent_name]
    update_list.append({'text':'Test About You!!!'})
    exist_intent_dict.update({intent_name:update_list})
    print('Updating the list')
    #Update on Watson
    update_intent(intent_name,exist_intent_dict)
    exist_intent_dict.clear()
    
if __name__ == "__main__":
    try:
        create_connection()
        update_intent_sample_2()
        #create_entity()
        #update_intent('hello',[{'text':'good evening'}] )
        #update_entity()
        #create_node()
        #get_synonym()
        #create_synonym()
        #csv_controller()
    except Exception as e:
        print(e)