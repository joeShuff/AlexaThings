"""
This code is for the Alexa skill
Interesting Computer Facts

created by Joseph Shufflebotham
"""

from __future__ import print_function
import random
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

facts = ["Only 10 percent of the worlds currency is in physical money. The rest is stored on computers",
         "The worst breach of U.S military computers in history happened when someone picked up a memory stick they found in the parking lot and plugged it into their computer, which was attached to United States Central Command.",
         "The first electronic computer, ENIAC, weighed more than 27 tons and took up 1800 square feet.",
         "TYPEWRITER is the longest word that you can write using the letters only on one row of the keyboard of your computer.",
         "Doug Engelbart invented the first computer mouse in around 1964 which was made of wood.",
         "There are more than 5000 new computer viruses released every month.",
         "Around 50 percent of all Wikipedia vandalism is caught by a single computer program with more than 90 percent accuracy.",
         "If there was a computer as powerful as the human brain, it would be able to do 38 thousand trillion operations per second and hold more than 3580 terabytes of memory.",
         "The password for the computer controls of nuclear tipped missiles of the U.S was 00000000 for eight years",
         "Approximately 70 percent of virus writers are said to work under contract for organized crime syndicates.",
         "HP, Microsoft and Apple have one very interesting thing in common. They were all started in a garage.",
         "An average person normally blinks 20 times a minute, but when using a computer they blink only 7 times a minute.",
         "The house where Bill Gates lives, was designed using a Macintosh computer.",
         "The first ever hard disk drive was made in 1979, and could hold only 5 megabytes of data.",
         "The first 1 gigabyte hard disk drive was announced in 1980 which weighed about 550 pounds, and had a price tag of 40,000 U.S dollars",
         "More than 80 percent of the emails sent daily are spams.",
         "A group of 12 engineers designed IBM PC and they were known as. The Dirty Dozen",
         "The original name of windows was Interface Manager.",
         "The first microprocessor created by Intel was the 4004. It was designed for a calculator, and in that time nobody imagined where it would lead.",
         "IBM 5120 from 1980 was the heaviest desktop computer ever made. It weighed about 105 pounds, not including the 130 pounds external floppy drive.",
         "QWERTY keyboard is not the most efficient keyboard layout. Instead, Dvorak keyboard is."]

info = "Computer Facts for Alexa was developed by Joe Shuff, and the latest update was released DATE"

how_to = "Simply ask. Alexa, ask computer facts for a fact"

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Computer Facts - " + title,
            'text': output,
##            'image': {
##                'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/720_Icon.png',
##                'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/1200_Icon.png'
##            }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_no_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('factsData')
response = table.scan()

def store_fact(fact, id):
    try:
        response = table.update_item(Key={'userId':id},
                                     UpdateExpression="set recent = :t",
                                     ExpressionAttributeValues={
                                         ':t': fact
                                     },
                                     ReturnValues="UPDATED_NEW"
                                     )
    except:
        response = table.put_item(Key={'userId':id, 'recent':fact})
        
def load_fact(id):
    try:
        response = table.get_item(Key={'userId':id})
        return response['Item']['recent']
    except:
        return None

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {
        'START': True
    }

    return build_response(session_attributes, build_speechlet_response_no_card("Welcome to Computer Facts, would you like to learn how to use this skill?", None, False))

def get_fact(intent, session):
    fact = random.choice(facts)
    store_fact(fact, session['user']['userId'])
    return build_response({}, build_speechlet_response("Here is a new fact", fact, None, True))

def get_info():
    return build_response({}, build_speechlet_response("Information", info, None, True))

def repeat_fact(intent, session):
    previous_fact = load_fact(session['user']['userId'])

    if (previous_fact is not None):
        return build_response({}, build_speechlet_response("Here is your fact again", "The last fact I told you was. " + previous_fact, None, True))
    else:
        return build_response({}, build_speechlet_response_no_card("I don't believe I have told you anything yet.", None, True))

def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again", "I was unable to recognise your last request. Please repeat yourself", False))
    
def how_to_use(leave_open = False):
    response = how_to
    session_attr = {}

    if (leave_open):
        session_attr = {
            "HOW": True
        }
        response = response + ". " + "Do you understand?"

    return build_response(session_attr, build_speechlet_response("How to Use Computer Facts", response, None, not leave_open))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
    
    return get_welcome_response()


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    try:
        if session['attributes']['START']:
            if intent_name == "AMAZON.YesIntent":
                return how_to_use(True)
            elif intent_name == "AMAZON.NoIntent":
                return build_speechlet_response_no_card("", None, True)
    except:
        pass

    try:
        if session['attributes']['HOW']:
            if intent_name == "AMAZON.YesIntent":
                return build_speechlet_response_no_card("", None, True)
            elif intent_name == "AMAZON.NoIntent":
                return how_to_use(True)
    except:
        pass

    if intent_name == "AMAZON.HelpIntent":
        return how_to_use(True)
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
        return build_response({}, build_speechlet_response_no_card("", None, True))
    elif intent_name == "GetFact":
        return get_fact(intent, session)
    elif intent_name == "RepeatFact":
        return repeat_fact(intent, session)
    elif intent_name == "HowToUse":
        return how_to_use()
    else:
        return dont_recognise(session)

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
   # if (event['session']['application']['applicationId'] !=
            # "amzn1.ask.skill.a93c342f-fb8d-499b-8c40-7fc1cd18cb79"):
       # raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
