from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "CryptoPal for Alexa. "

intro = "Welcome to CryptoPal for Alexa. Would you like to learn how to use this skill?"

how_to = "Crypto pal can get values for 4 different crypto currencies in 4 different global currencies. Ask, Alexa, ask crypto pal for the value of bitcoin in dollars"

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "CryptoPal - " + title,
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
                                                                       "Would you like to learn how to use crypto pal?",
                                                                       "To learn how to use, say, Alexa, ask crypto pal for help", False))

def get_crypto(intent, session):
    try:
        chosen_crypto = "NONE"
        try:
            chosen_crypto = intent['slots']['CryptoCurrency']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        except Exception as e:
            print(e)

        if (chosen_crypto == "NONE"):
            return build_response({}, build_speechlet_response_no_card("I can't seem to figure out that crypto currency. Please try again!", "", True))

        chosen_cur = "GBP"
        try:
            chosen_cur = intent['slots']['Currency']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        except Exception as e:
            print(e)

        req = urllib2.Request("https://api.coinbase.com/v2/prices/" + str(chosen_crypto) + "-" + str(chosen_cur) + "/buy", headers={'Authorization': "Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c", "CB-VERSION":"2018-3-05"})
        response = str(urllib2.urlopen(req).read())

        d = json.loads(response)
        value = d['data']['amount']
        cur = d['data']['currency']

        return build_response({}, build_speechlet_response("CryptoPal", str(chosen_crypto) + " has a value of " + str(value) + " " + str(cur), "", str(chosen_crypto) + " has a value of " + str(value) + " " + str(cur), True))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the crypto server. Sorry", "", True))


def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again",
                                                                    "I was unable to recognise your last request. Please repeat yourself",
                                                                    False))


def how_to_play(question=False):
    res = how_to
    re_prompt = None
    close = True

    if (question):
        res = how_to + ". Do you understand?"
        re_prompt = "Do you understand how to use this skill?"
        close = False

    return build_response({'UNDERSTAND': 'True'},
                          build_speechlet_response("How to Use, CryptoPal", res, re_prompt, res, close))


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

    if intent_name == "AMAZON.HelpIntent" or intent_name == "HowToUse":
        return how_to_play(True)
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
        return build_response({}, build_speechlet_response_no_card("", None, True))
    elif intent_name == "GetCrypto":
        return get_crypto(intent, session)
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
