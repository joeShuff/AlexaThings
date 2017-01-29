"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import urllib2
from datetime import datetime

APP_KEY = "APP_KEY"
APP_ID = "APP_ID"

'''
These are the constants that decide what stage of conversation they are in.
'''
CHOOSING_FAV = 0


STATE = {0: "CHOOSING_FAV"}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Bus Buddy - " + title,
            'content': output
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

# --------------- Functions for the Functionality of the Skill -----------------

def diff_times(time1, time2):
    FMT = '%H:%M'
    diff = datetime.strptime(time1, FMT) - datetime.strptime(time2, FMT)

    diff = str(int(str(diff)[2:4]))

    if (diff == "0"):
        return "now"
    
    return diff

def get_stop_name(stop):
    name = stop['name']
    indicator = stop['indicator']

    return str(indicator + " " + name).strip()

def get_time(expected, aimed):
    if (expected == None):
        return "at " + aimed
    else:
        current = str(datetime.now().time())[:5]
        diff = str( diff_times(expected, current))
        if (diff == "now"):
            return diff
        
        return "in " + diff + " mins"

def get_next_bus(stop):
    response = str(urllib2.urlopen("http://transportapi.com/v3/uk/bus/stop/" + stop['atcocode'] + "/live.json?app_id=" + APP_ID + "&app_key=" + APP_KEY).read())

    d = json.loads(response)

    ##This makes the dictionary look pretty
    js = json.dumps(d,indent=2)

    stop_name = d['stop_name']
    bearing = d['bearing']
    departures = d['departures']

    indicator = stop['indicator']

    departure_numbers = list(departures.keys())

    to_speak = "The next buses at stop " + get_stop_name(stop) " are.\n"
    to_speak = to_speak.replace("adj ", "adjacent ").replace("opp ", "opposite ")

    i = 0

    for key in departure_numbers:
        next_buses = departures[key]

        for bus in next_buses:
            i = i + 1

            if i >= 4:
                return to_speak
            
            number = bus['line']
            expected = bus['expected_departure_time']
            aimed = bus['aimed_departure_time']
            
            result = "The number " + number + ", due " + get_time(expected, aimed) + ".\n"

            to_speak = to_speak + result

    return to_speak

def get_nearest_stops():
    postcode = "POSTCODE"
    response = str(urllib2.urlopen("http://api.postcodes.io/postcodes?q=[%22" + postcode.replace(" ","%20") + "%22]").read())

    d = json.loads(response)

    ##This makes the dictionary look pretty
    ##js = json.dumps(d,indent=2)

    result = d['result'][0]
    
    lon = str(result['longitude'])
    lat = str(result['latitude'])

    near_response = str(urllib2.urlopen("http://transportapi.com/v3/uk/bus/stops/near.json?&app_id=" + APP_ID + "&app_key=" + APP_KEY + "&lon=" + lon + "&lat=" + lat).read())

    near_response = near_response.replace("\\","")

    near_dict = json.loads(near_response)

    stops = near_dict['stops']

    nearest = []

    for i in range(len(stops)):
        stop = stops[i]
    
        nearest.append(stop) 

    return nearest

def get_nearest_recent():
    stops = get_nearest_stops()

    atco = stops[0]['atcocode']
    
    return get_next_bus(atco)
    
def get_live_from_atco(atco):
    return get_next_bus(atco)

def get_live_from_name(ind, name):
    stops = get_nearest_stops()

    for stop in stops:
        if ((str(stop['name']) == name) & (str(stop['indicator']) == ind)):
            return get_next_bus(stop)

def get_nearest_stops_result():
    stops = get_nearest_stops()

    result = "There are " + str(len(stops)) + " near you. Here are the closest 3. "

    i = 0
    
    for stop in stops:

        i = i + 1

        if i >= 4:
            return result.replace("adj ", "adjacent ").replace("opp ", "opposite ")
        
        result = result + "stop " + stop['indicator'] + " " + stop['name'] + ". "

    return result.replace("adj ", "adjacent ").replace("opp ", "opposite ")

# --------------- Intent Functions --------------------------------------------

def next_bus_intent(intent, session):
    return build_response({}, build_speechlet_response_no_card(get_live_from_name("opp", "Moorlands Close"), "", True))

def stops_near_intent(intent, session):
    return build_response({}, build_speechlet_response_no_card(get_nearest_stops_result(), "", True))

def set_postcode_intent(intent, session):    
    return build_response({}, build_speechlet_response_no_card("So you set your postcode", "", True))

def set_favouirite_intent(intent, session):
    pass

def yes_intent(intent, session):
    return build_response({}, build_speechlet_response_no_card("This is a yes intent", "", True))

def no_intent(intent, session):
    return build_response({}, build_speechlet_response_no_card("This is a no intent", "", True))

def dont_recognise(intent, session):
    return build_response(session, build_speechlet_response_no_card("Sorry, I didn't understand that, please try again", "", False))
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    speech_output = "Hi, Welcome to Bus Buddy";
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response_no_card(speech_output, "", should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response_no_card(speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetPostcode":
        return set_postcode_intent(intent, session)
    elif intent_name = "SetFavourite":
        return set_favourite_intent()
    elif intent_name == "NextBus":
        return next_bus_intent(intent, session)
    elif intent_name == "StopsNear":
        return stops_near_intent(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return yes_intent(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return no_intent(intent, session)
    else:
        return dont_recognise(intent, session)

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
