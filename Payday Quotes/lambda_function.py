from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "Payday Quotes for Alexa."

intro = "Welcome to Payday Quotes for Alexa. Would you like to learn how to use this skill?"

how_to = "To use, simply say. Alexa, ask payday quotes for a quote"

folders = ["bain", "bulldozer", "chains", "dallas", "elephant", "guard", "hector", "houston", "hoxton", "wolf"]

amount = {"bain":369,
          "bulldozer":281,
          "chains":391,
          "dallas":363,
          "elephant":34,
          "guard":584,
          "hector":26,
          "houston":282,
          "hoxton":95,
          "wolf":250}

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Payday Quotes - " + title,
            'text': card_text,
            'image': {
                'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/payday_quotes/720_Icon.png',
                'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/payday_quotes/1200_Icon.png'
            }
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
                                                                       "Would you like to learn how to use Payday quotes?",
                                                                       "", False))


def get_quote_no_char(intent, session):
    chosen_char = random.choice(folders)
    return get_quote(intent, session, chosen_char)

def get_quote(intent, session, character):

    selected_id = random.randint(1, amount[character])
    print("Selcted int " + str(selected_id))

    try:
        return {
            "response": {
                "directives": [
                    {
                        "type": "AudioPlayer.Play",
                        "playBehavior": "REPLACE_ALL",
                        "audioItem": {
                            "stream": {
                                "token": "12345",
                                "url": "https://s3.eu-west-2.amazonaws.com/shuffskills/payday_quotes/" + character + "/" + str(selected_id) + ".mp3",
                                "offsetInMilliseconds": 0
                            }
                        }
                    }
                ],
                "shouldEndSession": True
            }
        }
    except Exception:
        return build_response(session, build_speechlet_response_no_card("I appear to be having trouble connecting to the payday gang. They're probably doing a heist. Sorry", "", True))

def character_not_recognized(intent, session, char):
    return build_response(session, build_speechlet_response("Character List", "I can't find the character " + char + ". I've sent the list to your Alexa app.", None, "I can't find the character " + char + ". The following are valid characters:\n" +
                                                                                                                                                                                                             "- Bain\n" + "- Bulldozer\n" + "- Guard\n" +
                                                                                                                                                                                                             "- Chains\n" + "- Dallas\n" + "- Elephant\n" +
                                                                                                                                                                                                             "- Hector\n" + "- Houston\n" + "- Hoxton\n" +
                                                                                                                                                                                                             "- Wolf", True))

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
                          build_speechlet_response("How to Use, Payday Quotes", res, re_prompt, res, close))


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
    elif intent_name == "HowToUse":
        return how_to_play(True)
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
        return build_response({}, build_speechlet_response_no_card("", None, True))
    elif intent_name == "GetQuote":
        return get_quote_no_char(intent, session)
    elif intent_name == "GetCharacterQuote":
        character = intent['slots']['Char']['value']

        if not character.lower() in folders:
            return character_not_recognized(intent, session, character)

        return get_quote(intent, session, character.lower())
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
