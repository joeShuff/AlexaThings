from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "Relationship Tester for Alexa"

intro = "Welcome to relationship tester for Alexa. Would you like to learn how to use this skill?"

how_to = "Simply say. Alexa, ask relationship tester to test me"

tests = ["Where did the 2 of you first meet?",
         "If you and your partner have a song, what is it? and Why is that your song?",
         "What do you love most about your partner?",
         "What is your partners favourite movie?",
         "What is your partners favourite music artist?",
         "What is your partners favourite meal?",
         "What is the most interesting thing about your parner?",
         "What would your partners perfect day consist of?",
         "What do you think is the greatest accomplishment of your partners life?",
         "What do you think is your partners favourite thing about you?",
         "Who, other than you, is your partners best friend?",
         "What is your partners favourite activity they do in their spare time?"]

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Relationship Tester - " + title,
            'text': card_text
            # 'image': {
            #     'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/MC_720.png',
            #     'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/MC_1200.png'
            # }
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
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {
        'START': True
    }
    speech_output = intro

    return build_response(session_attributes, build_speechlet_response("Welcome", intro,
                                                                       "Would you like to learn how to use relationship tester?",
                                                                       "", False))


dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('ReltestTable')
response = table.scan()


def store_thing(thing, id):
    try:
        response = table.update_item(Key={'userId': id},
                                     UpdateExpression="set recent = :t",
                                     ExpressionAttributeValues={
                                         ':t': thing
                                     },
                                     ReturnValues="UPDATED_NEW"
                                     )
    except Error as e:
        response = table.put_item(Key={'userId': id, 'recent': thing})

def load_thing(id):
    try:
        response = table.get_item(Key={'userId': id})
        return str(response['Item']['recent'])
    except:
        return None

def get_test(intent, session):
    test = random.choice(tests)
    store_thing(test, session['user']['userId'])
    return build_response({}, build_speechlet_response_no_card(test, "", True))


def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again", "I was unable to recognise your last request. Please repeat yourself", False))

def how_to_play(question=False):
    res = how_to
    re_prompt = None
    close = True

    if (question):
        res = how_to + ". Do you understand?"
        re_prompt = "Do you understand how to use this skill?"
        close = False

    return build_response({'UNDERSTAND': 'True'},
                          build_speechlet_response("How to Use, Relationship Tester", res, re_prompt, res, close))

def how_to_instr():
    return build_response({}, build_speechlet_response_no_card("Okay, enjoy using this skill!", None, True))

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
                return how_to_play(True)
            elif intent_name == "AMAZON.NoIntent":
                return how_to_instr()
    except:
        pass

    try:
        if session['attributes']['UNDERSTAND']:
            if intent_name == "AMAZON.YesIntent":
                return build_response({}, build_speechlet_response_no_card("Okay, enjoy this skill!", None, True))
            elif intent_name == "AMAZON.NoIntent":
                return how_to_play(True)
    except:
        pass

    if intent_name == "AMAZON.HelpIntent":
        return how_to_play(True)
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
        return build_response({}, build_speechlet_response_no_card("", None, True))
    elif intent_name == "GetTest":
        return get_test(intent, session)
    elif intent_name == "HowToUse":
        return how_to_play(True)
    elif intent_name == "RepeatTest":
        try:
            return build_response(session, build_speechlet_response_no_card("The last thing I told you was. " + load_thing(session['user']['userId']), "", True))
        except:
            return build_response(session, build_speechlet_response_no_card("There is no previous test for this account. Ask for a test first.", "", True))
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
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
