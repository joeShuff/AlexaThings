from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "Ninja Fortnite Stats for Alexa. "

intro = "Welcome to ninja stats for Alexa. Would you like to learn how to use this skill?"

how_to = "Simply say. Alexa, ask ninja stats for his stats"

background_images = ['https://s3.eu-west-2.amazonaws.com/shuffskills/ninja_stats/1.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/ninja_stats/2.jpg',
                     'https://s3.eu-west-2.amazonaws.com/shuffskills/ninja_stats/3.jpg']

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
                'title': "Ninja Fortnite Stats - " + title,
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
                                "text": output
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
            'title': "Ninja Fortnite Stats - " + title,
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
                                                                       "Would you like to learn how to use ninja fornite stats?",
                                                                       "", False))

def get_recent_game(intent, session):
    pass

def get_total_wins(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/wins", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has a total of " + response + " wins"
        return build_response({}, build_speechlet_response("Ninja Fortnite Wins", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))

def get_total_games(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/matches", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has played a total of " + response + " games"
        return build_response({}, build_speechlet_response("Ninja Fortnite Games", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))

def get_total_kills(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/kills", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has a total of " + response + " kills"
        return build_response({}, build_speechlet_response("Ninja Fortnite Kills", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))


def get_win_percentage(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/winsPercent", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has a win percentage of " + response
        return build_response({}, build_speechlet_response("Ninja Fortnite Win Percentage", output, "", output, True))
    except Exception:
        return build_response({}, build_speechlet_response_no_card(
            "I appear to be having trouble connecting to the ninja server. Sorry", "", True, has_screen=has_screen))

def get_kd(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/kd", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has a kill death ratio of " + response
        return build_response({}, build_speechlet_response("Ninja Fortnite K/D Ratio", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))


def get_survival_time(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/survivalTime", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has an average survive time of " + response
        return build_response({}, build_speechlet_response("Ninja Fortnite Survival Time", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))

def get_total_time(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/totalTime", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has played for " + response
        return build_response({}, build_speechlet_response("Ninja Fortnite Total Time", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))

def get_kpm(intent, session, has_screen):
    try:
        req = urllib2.Request("http://api.joeshuff.co.uk/ninja/kpm", headers={'User-Agent': "Magic Browser"})
        response = str(urllib2.urlopen(req).read())

        output = "Ninja has " + response + " kills per minute"
        return build_response({}, build_speechlet_response("Ninja Fortnite KPM", output, "", output, True, has_screen=has_screen))
    except Exception:
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the ninja server. Sorry", "", True))

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
                          build_speechlet_response("How to Use, Ninja Fortnite Stats", res, re_prompt, res, close))


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
    elif intent_name == "GetRecentGame":
        return get_recent_game(intent, session, has_screen)
    elif intent_name == "GetTotalWins":
        return get_total_wins(intent, session, has_screen)
    elif intent_name == "GetTotalMatches":
        return get_total_games(intent, session, has_screen)
    elif intent_name == "GetTotalKills":
        return get_total_kills(intent, session, has_screen)
    elif intent_name == "GetWinPercent":
        return get_win_percentage(intent, session, has_screen)
    elif intent_name == "GetKD":
        return get_kd(intent, session, has_screen)
    elif intent_name == "GetSurvivalTime":
        return get_survival_time(intent, session, has_screen)
    elif intent_name == "GetTotalPlayTime":
        return get_total_time(intent, session, has_screen)
    elif intent_name == "GetKillsPerMinute":
        return get_kpm(intent, session, has_screen)
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
