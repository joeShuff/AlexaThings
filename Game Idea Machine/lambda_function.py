from __future__ import print_function
import random
import string
import time
import boto3
import json
import urllib2
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

info = "Random Game idea Generator for Alexa. "

intro = "Welcome to Game idea generator for Alexa. Would you like to learn how to use this skill?"

how_to = "Simply say. Alexa, ask game idea machine for an idea"

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Game Idea Machine - " + title,
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
    
    return build_response(session_attributes, build_speechlet_response("Welcome", intro , "Would you like to learn how to use Game idea machine?", "", False))

def sign_request():
    from hashlib import sha1
    import hmac

    # key = CONSUMER_SECRET& #If you dont have a token yet
    key = "MAHGFksAMniWbyD2lO0a0EILpT1A4M80zQ5Y1Hrr9k2A3TijFn&oYvGSW2EiqxptW8E5psGkNAE8MMX1ZpyxaZlTTRPsxNYz"


    # The Base String as specified here:
    raw = "BASE_STRING" # as specified by oauth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return hashed.digest().encode("base64").rstrip('\n')

def get_idea(intent, session):

    nonce = ""
    for i in range(11):
        nonce = nonce + random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)

    # timestamp = datetime.timestamp()
    timestamp = int(time.time())

    header = 'OAuth oauth_consumer_key="J4jPr12aTGg9kyFTm816ozhaZ",oauth_token="394949955-30slTLhJwI7Rd7YQt27fvHzdV5YyGpcA1FqeesMb",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1503359243",oauth_nonce="2RSZBO2xZCf",oauth_version="1.0",oauth_signature="XlqG7%2F1NPVI2adG8O%2B2FhUPtSEE%3D"'
    # header = header.replace('NONCE', str(nonce))
    # header = header.replace('STAMP', str(timestamp))
    # header = header.replace('SIG', str(auth))
    print(header)

    req = urllib2.Request("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=gameideamachine")
    req.add_header('Authorization', header)
    response = str(urllib2.urlopen(req).read())

    d = json.loads(response)

    ideas = []

    ##Get all required values from response
    for obj in d:
        ideas.append(obj["text"])

    print(ideas)

    chosen = random.choice(ideas)

    return build_response({}, build_speechlet_response("Game Idea", chosen, "", chosen, True))

def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again", "I was unable to recognise your last request. Please repeat yourself", False))
    
def how_to_play(question = False):
    res = how_to
    re_prompt = None
    close = True

    if (question):
        res = how_to + ". Do you understand?"
        re_prompt = "Do you understand how to use this skill?"
        close = False

    return build_response({'UNDERSTAND': 'True'}, build_speechlet_response("How to Use, Game Idea Machine", res, re_prompt,res, close))

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
    elif intent_name == "GetIdea":
        return get_idea(intent, session)
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
