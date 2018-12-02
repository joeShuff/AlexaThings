from __future__ import print_function
import random
import json
import urllib2
import urllib
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

info = "Play your favourite game of cards against humanity on Amazon Alexa."

intro = "Welcome to 'Cards Against' right here on Amazon Alexa, would you like to learn how to use this skill?"

how_to = "To ask for a black card, say, Alexa, ask cards against for a card"

background_images = ['https://s3.eu-west-2.amazonaws.com/shuffskills/cards_against/cah.jpg']

has_screen = False

cwd = os.getcwd()

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session, has_screen=False, image_url = None, background_image_url=""):

    if has_screen and image_url is not None:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Standard',
                'title': "Cards Against",
                'text': card_text
                # 'image': {
                #     'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/720.jpg',
                #     'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/1200.jpg'
                # }
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'directives':[
                {
                    "type": "Display.RenderTemplate",
                    "template": {
                        "type": "BodyTemplate2",
                        "title": title,
                        "backButton":"HIDDEN",
                        "backgroundImage": {
                            "sources": [
                                {
                                    "url": random.choice(background_images),
                                    "size": "X_LARGE"
                                }
                            ]
                        },
                        "textContent": {
                            "primaryText": {
                                "type": "RichText",
                                "text": card_text
                            }
                        }
                    }
                }
            ],
            'shouldEndSession': should_end_session
        }

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': title,
            'text': card_text,
            'image': {
                'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/720.jpg',
                'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/1200.jpg'
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
                                                                       "Would you like to learn how to use the 'Cards Against' skill?",
                                                                       "Fun for all!", False))

def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again",
                                                                    "I was unable to recognise your last request. Please repeat yourself",
                                                                    False))

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('CardsAgainstMemory')
response = table.scan()

def store_card(card, id):
    try:
        response = table.update_item(Key={'userId': id},
                                     UpdateExpression="set recent = :t",
                                     ExpressionAttributeValues={
                                         ':t': card
                                     },
                                     ReturnValues="UPDATED_NEW"
                                     )
    except Error as e:
        response = table.put_item(Key={'userId': id, 'recent': card})

def load_card(id):
    try:
        response = table.get_item(Key={'userId': id})
        return response['Item']['recent']
    except:
        return None

def get_black_card(intent, session, has_screen=False):
    json_stuff = json.loads(open(cwd + "/black_cards_json.json",'r').read())

    cards = json_stuff['blackCards']
    card = random.choice(cards)

    pick = card['pick']

    to_return = card['text']

    if pick > 1:
        to_return = "Pick " + str(pick) + ". " + to_return

    store_card(to_return, session['user']['userId'])

    to_read = to_return.replace("_", "BLANK")

    return build_response({}, build_speechlet_response("Your black card", to_read, None, to_return, True, has_screen=has_screen))


def repeat_black_card(intent, session, has_screen=False):
    previous_card = load_card(session['user']['userId'])

    if (previous_card is not None):
        to_read = previous_card.replace("_", "BLANK")

        return build_response({}, build_speechlet_response("Your last black card", "Your last card was. " + to_read, None, previous_card, True, has_screen=has_screen))
    else:
        return build_response({},
                              build_speechlet_response_no_card("I don't believe I have given you anything yet.", None,
                                                               True))

def how_to_play(question=False):
    res = how_to
    re_prompt = None
    close = True

    if (question):
        res = how_to + ". Do you understand?"
        re_prompt = "Do you understand how to use this skill?"
        close = False

    return build_response({'UNDERSTAND': 'True'},
                          build_speechlet_response("How to Use", res, re_prompt, how_to, close))

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

def on_intent(intent_request, session, has_screen=False):
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
    elif intent_name == "GetBlackCard":
        return get_black_card(intent, session, has_screen=has_screen)
    elif intent_name == "RepeatBlackCard":
        return repeat_black_card(intent, session, has_screen=has_screen)
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
    try:
        has_screen = event['context']['System']['device']['supportedInterfaces']['Display'] != {}
    except:
        has_screen = False

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], has_screen=has_screen)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# print(get_black_card({}, {}, True))