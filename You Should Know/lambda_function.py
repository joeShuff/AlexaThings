from __future__ import print_function
import random
import json
import urllib2
import urllib

info = "Your home of interesting things you should know, on Amazon Alexa."

intro = "Welcome to 'You Should Know' right here on Amazon Alexa, would you like to learn how to use this skill?"

how_to = "To ask for something interesting say, Alexa, ask you should know for something"

background_images = ['https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/bg1.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/bg2.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/you+should+know/bg3.jpg']

has_screen = False

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
                'title': "You Should Know",
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
            'directives':[
                {
                    "type": "Display.RenderTemplate",
                    "template": {
                        "type": "BodyTemplate2",
                        "token": "movie",
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
                                                                       "Would you like to learn how to use the 'You Should Know' skill?",
                                                                       "The place to go for a lot of useless knowledge!", False))

def dont_recognise(session):
    return build_response(session, build_speechlet_response_no_card("I don't recognise your request, please try again",
                                                                    "I was unable to recognise your last request. Please repeat yourself",
                                                                    False))

def get_something_i_should_know(intent, session, has_screen=False, loaded_json=None, count = 1):
    print(str(count))
    try:
        jsonresponse = loaded_json

        if jsonresponse is None:
            request = urllib2.Request("https://www.reddit.com/r/youshouldknow/hot/.json?limit=100&t=all", headers={'User-Agent': 'User-Agent: python:discord_joebot:1.0 (by /u/_shuffles)'})
            response = urllib2.urlopen(request)
            received = response.read()

            jsonresponse = json.loads(received)

        loaded_json = jsonresponse

        child_count = len(jsonresponse['data']['children'])

        selected_child = random.randint(0, child_count - 1)

        url = str(jsonresponse['data']['children'][selected_child]['data']['url'])
        title = str(jsonresponse['data']['children'][selected_child]['data']['title'])
        author = str(jsonresponse['data']['children'][selected_child]['data']['author'])
        subreddit = str(jsonresponse['data']['children'][selected_child]['data']['subreddit_name_prefixed'])
        nsfw = str(jsonresponse['data']['children'][selected_child]['data']['over_18'])

        if 'YSK:' in title:
            title = title.replace('YSK:', '')

        if 'YSK :' in title:
            title = title.replace('YSK :', '')

        if 'YSK' in title:
            title = title.replace('YSK', '')

        title = title.strip()

        return build_response({},build_speechlet_response("You Should Know", "You should know " + title, "", title, True, has_screen, "", ""))
    except Exception as e:
        print(e)
        if (count >= 100):
            return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the knowledge server. Sorry", "", True))
        else:
            return get_something_i_should_know(intent, session, has_screen, loaded_json=loaded_json, count=count + 1)

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
    elif intent_name == "SomethingIShouldKnow":
        return get_something_i_should_know(intent, session, has_screen=has_screen)
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

# print(get_something_i_should_know({}, {}, True))