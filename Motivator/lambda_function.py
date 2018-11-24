from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "Motivator for Alexa. "

intro = "Welcome to motivator for Alexa. Would you like to learn how to use this skill?"

how_to = "Simply say. Alexa, ask motivator to motivate me"

background_images = ['https://s3.eu-west-2.amazonaws.com/shuffskills/motivator/1.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/motivator/2.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/motivator/3.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/motivator/4.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/motivator/5.jpg']

has_screen = False

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session, has_screen = False):

    if has_screen:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Standard',
                'title': "Motivator - " + title,
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
            'directives':[
                {
                    "type": "Display.RenderTemplate",
                    "template": {
                        "type": "BodyTemplate1",
                        "token": "stats",
                        "title": title,
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
            'title': "Motivator - " + title,
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
                                                                       "Would you like to learn how to use motivator?",
                                                                       "", False))

def get_quote(intent, session, has_screen):
    try:
        req = urllib2.Request("https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json", headers={'User-Agent': "Magic Browser"})
        response = json.loads(str(urllib2.urlopen(req).read()))

        output = response['quoteText']
        author = ''
        try:
            author = response['quoteAuthor']
        except:
            pass

        return build_response({}, build_speechlet_response("", output, "", output + " \n- " + str(author), True, has_screen=has_screen))
    except Exception as e:
        print(e)
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the motivation center. Sorry", "", True))

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
                          build_speechlet_response("How to Use", res, re_prompt, res, close))


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


def on_intent(intent_request, session, has_screen= False):
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
    elif intent_name == "GetQuote":
        return get_quote(intent, session, has_screen)
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

    print("this screen = " + str(has_screen))

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], has_screen = has_screen)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
