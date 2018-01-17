from __future__ import print_function
import random
import boto3
import json
import urllib2
from boto3.dynamodb.conditions import Key, Attr

info = "Minecraft Status for Alexa was developed my Joe Shuff. Latest release is "

intro = "Welcome to Minecraft Status for Alexa. Would you like to learn how to use this skill?"

how_to = "Simply say. Alexa, ask minecraft status for an update"

# --------------- Helpers that build all of the responses ----------------


def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Minecraft Status - " + title,
            'text': card_text,
            'image': {
                'smallImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/MC_720.png',
                'largeImageUrl': 'https://s3.eu-west-2.amazonaws.com/shuffskills/MC_1200.png'
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


# --------------- Functions that control the skill's behavior ------------
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {
        'START': True
    }
    speech_output = intro

    return build_response(session_attributes, build_speechlet_response("Welcome", intro, "Would you like to learn how to use Minecraft Status?", "", False))


def get_status(intent, session):
    response = str(urllib2.urlopen("https://status.mojang.com/check").read())
    d = json.loads(response)

    # This makes the dictionary look pretty
    # js = json.dumps(d, indent=2)
    # print(js)

    serviceName = {"minecraft.net": "Minecraft Website",
                   "session.minecraft.net": "Minecraft Login Servers",
                   "account.mojang.com": "Mojang Account Servers",
                   "auth.mojang.com": "Authentication Servers",
                   "skins.minecraft.net": "Skins servers",
                   "textures.minecraft.net": "Textures servers",
                   "mojang.com": "Mojang website"}

    results = {"minecraft.net": "",
               "session.minecraft.net": "",
               "account.mojang.com": "",
               "auth.mojang.com": "",
               "skins.minecraft.net": "",
               "textures.minecraft.net": "",
               "mojang.com": ""}

    issues = {"green": "No Issues",
              "yellow": "Some Issues",
              "red": "Service Unavailable"}

    # Get all required values from response
    for obj in d:
        for key in obj.keys():
            if key in results.keys():
                results[key] = obj[key]

    allGreen = True
    allRed = True
    allYellow = True

    for key in results.keys():
        if results[key] != 'green':
            allGreen = False

        if results[key] != 'red':
            allRed = False

        if results[key] != 'yellow':
            allYellow = False

    toReply = ""

    if allGreen:
        toReply = "All servers are up and running. Have fun."
    elif allRed:
        toReply = "All servers are currently down. Check Mojang twitter for updates."
    elif allYellow:
        toReply = "All servers are having some issues. Check Mojang twitter for updates"
    else:
        toReply = "Some servers are having more troubles than others. Check your Alexa app for a full description."

    cardText = "Here is a debrief of all servers.\n"

    for key in results.keys():
        cardText += serviceName[key] + ": " + issues[results[key]] + "\n"

    cardText += "\nPlease check @MojangStatus on twitter for more updates."

    return build_response({}, build_speechlet_response("Status Update", toReply, "", cardText, True))


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

    return build_response({'UNDERSTAND': 'True'}, build_speechlet_response("How to Use, Minecraft Status", res, re_prompt, res, close))


def how_to_instr():
    return build_response({}, build_speechlet_response_no_card("Okay, enjoy using this skill!", None, True))

# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    return get_welcome_response()


def on_launch(launch_request, session):
    return get_status("", session)


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
    elif intent_name == "GetStatus":
        return get_status(intent, session)
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
