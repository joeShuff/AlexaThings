from __future__ import print_function
import random
import boto3
import json
import urllib2
import time
import urllib
from boto3.dynamodb.conditions import Key, Attr

info = "Your favourite game expert, right here, on Amazon Alexa."

intro = "Welcome to your local game expert for Amazon Alexa, would you like to learn how to use this skill?"

how_to = "To ask for more details about a game, say. Alexa, ask the game expert all about, then say your game name. I'll try my best to understand you and get the right game"

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
                'title': "The Game Expert - " + title,
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
                        "type": "BodyTemplate2",
                        "token": "game",
                        "title": title,
                        "backButton":"HIDDEN",
                        "image": {
                            "sources": [
                                {
                                    "url": image_url,
                                    "size": "LARGE"
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
            'title': "The Game Expert - " + title,
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
                                                                       "Would you like to learn how to use the game expert skill?",
                                                                       "Your number one source for all information about your favourite games!", False))

'''
This is called when we can't find a game based on their title, so just say sorry can't find that
'''
def no_game_found(game):
    game_doesnt_exist = "I'm sorry but I can't find the game, " + game + " on the records. Please try again"
    return build_response({}, build_speechlet_response_no_card(game_doesnt_exist, game_doesnt_exist, True))

'''
This is called when there is no game in the slot. Reprompting the user to repeat themselves
'''
def cant_find_game(session):
    game_doesnt_exist = "I'm sorry but I didn't catch that game. What game would you like information on?"

    session['GAME'] = 'True'

    return build_response(session, build_speechlet_response_no_card(game_doesnt_exist, game_doesnt_exist, False))

'''
This method is called when there isn't enough info on the game
'''
def not_enough_info(game):
    game_doesnt_exist = "I'm sorry but the game, " + game + ", doesn't have enough information on the records. Please try again"
    return build_response({}, build_speechlet_response_no_card(game_doesnt_exist, game_doesnt_exist, True))

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('GameExpertMemory')
response = table.scan()

def store_trailer(trailer_id, id):
    try:
        response = table.update_item(Key={'userId': id},
                                     UpdateExpression="set recent = :t",
                                     ExpressionAttributeValues={
                                         ':t': trailer_id
                                     },
                                     ReturnValues="UPDATED_NEW"
                                     )
    except Error as e:
        response = table.put_item(Key={'userId': id, 'recent': trailer_id})

def load_trailer(id):
    try:
        response = table.get_item(Key={'userId': id})
        return response['Item']['recent']
    except:
        return None

def get_game_from_id(id):
    try :
        req = urllib2.Request("https://api-endpoint.igdb.com/games/" + str(id),
                              headers={'User-Agent': "Magic Browser",
                              'Accept':"application/json",
                              'user-key':"4297d1dcb81e6e6b5c70d12f210884f9"})

        response = str(urllib2.urlopen(req).read())
        d = json.loads(response)
        results = d

        if (len(results) > 0):
            return results[0]

        return None
    except Exception as e:
        pass

def get_game_from_name(name):
    try :
        req = urllib2.Request("https://api-endpoint.igdb.com/games/?search=" + urllib.urlencode({'query': name}),
                              headers={'User-Agent': "Magic Browser",
                              'Accept':"application/json",
                              'user-key':"4297d1dcb81e6e6b5c70d12f210884f9"})

        response = str(urllib2.urlopen(req).read())
        d = json.loads(response)
        results = d

        if (len(results) > 0):
            return get_game_from_id(results[0]['id'])

        return None
    except Exception as e:
        pass

def get_game(intent, session, has_screen=False, game_name = None):
    try:
        if (game_name is None):
            try:
                game_name = intent['slots']['GameName']['value']
            except:
                return cant_find_game(session)

        the_game_i_want = get_game_from_name(game_name)

        if (the_game_i_want is None):
            return no_game_found(game_name)

        game_name = the_game_i_want['name']
        game_id = the_game_i_want['id']
        try:
            game_release_date = time.strftime('%d-%m-%Y', time.localtime(the_game_i_want['first_release_date'] / 1000))
            game_vote_average = str(int(the_game_i_want['aggregated_rating']))
            game_poster = "https://" + str(the_game_i_want['cover']['url']).replace('t_thumb', 't_1080p')[2:]
            game_overview = the_game_i_want['summary']
        except:
            return not_enough_info(game_name)


        trailer_id = None
        try:
            trailer_id = the_game_i_want['videos'][0]['video_id']
        except:
            pass

        if trailer_id is not None:
            store_trailer(trailer_id, session['user']['userId'])
        else:
            store_trailer(None, session['user']['userId'])

        output = str(game_name) + ", was released on " + game_release_date + " and has achieved an average rating of " + game_vote_average + "%. "
        output = output + "The summary is as follows. " + game_overview + " "

        if has_screen and trailer_id is not None:
            output = output + "If you would like to watch the trailer, say. Alexa, ask the game expert to show me the trailer"

        return build_response({}, build_speechlet_response(game_name, output, "", output, True, has_screen=has_screen, image_url=game_poster))
    except Exception as e:
        print(e)
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the game server. Sorry", "", True))

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
                          build_speechlet_response("How to Use, The Game Expert", res, re_prompt, how_to, close))

def how_to_instr():
    return build_response({}, build_speechlet_response_no_card("Okay, enjoy using this skill!", None, True))

def get_stream_links(key):
    target_url = "http://www.youtube.com/get_video_info?video_id=" + str(key) + "&el=embedded&ps=default&eurl=&gl=US&hl=en"
    resp = ""

    try:
        for line in urllib2.urlopen(target_url):
            resp = line
    except:
        print("woopsie")
        return {}

    parts = resp.split("&")

    the_map = {}

    for part in parts:
        do_a_split = part.split("=")
        the_map[do_a_split[0]] = do_a_split[1]

    streams = str(urllib2.unquote(the_map['url_encoded_fmt_stream_map']).decode('utf8')).split(",")

    final_streams = []

    for stream in streams:
        this_stream = {}
        stream_attrs = stream.split("&")

        for attr in stream_attrs:
            key,val = attr.split("=")
            this_stream[key] = str(urllib2.unquote(val).decode('utf8'))

        final_streams.append(this_stream)

    return final_streams

def build_video(link, title, desc):
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": None,
            "card": None,
            "directives": [
                {
                    "type": "VideoApp.Launch",
                    "videoItem": {
                        "source": link,
                        "metadata": {
                            "title": title,
                            "subtitle": desc
                        }
                    }
                }
            ],
            "reprompt": None
        }
    }

def play_trailer_by_game(intent, session, has_screen=False):
    the_game = get_game_from_name(intent['slots']['TrailerGameName']['value'])

    if the_game is None:
        return build_response({},build_speechlet_response_no_card("I cannot find the game " + intent['slots']['TrailerGameName']['value'],None, True))

    try:
        trailer_id = the_game['videos'][0]['video_id']
        store_trailer(trailer_id, session['user']['userId'])
        return play_trailer(intent, session, has_screen)

    except:
        return build_response({}, build_speechlet_response_no_card("I cannot find a trailer for the game " + intent['slots']['TrailerGameName']['value'], None, True))

def play_trailer(intent, session, has_screen=False):
    video_id = load_trailer(session['user']['userId'])

    if (video_id is None):
        return build_response({} ,build_speechlet_response_no_card("You haven't searched a recent game, or your most recent game didn't have a trailer!", None, True))

    youtube_link = get_stream_links(video_id)

    if (len(youtube_link) <= 0):
        return build_response({}, build_speechlet_response_no_card("I had some trouble finding the trailer for this game, please try again.", None, True))

    link = youtube_link[0]['url']

    return build_video(link, "Game Trailer from The Game Expert", "Trailer loaded from Internet Game Database")

def get_release_date(intent, session, has_screen=False):
    the_movie = get_game_from_name(intent['slots']['ReleaseGameName']['value'])

    if the_movie is None:
        return build_response({}, build_speechlet_response_no_card("I cannot find the movie " + intent['slots']['ReleaseMovieName']['value'], None, True))

    movie_title = the_movie['title']
    movie_id = the_movie['id']
    movie_release_date = the_movie['release_date']
    movie_vote_average = str(the_movie['vote_average'])
    movie_poster = the_movie['poster_path']
    movie_overview = the_movie['overview']

    store_trailer(movie_id, session['user']['userId'])

    output = "The film " + movie_title + ", was released on " + movie_release_date + ". "

    if has_screen:
        output = output + "If you would like to watch the trailer, say. Alexa, ask the movie expert to show me the trailer"

    return build_response({}, build_speechlet_response(movie_title, output, "", output, True, has_screen=has_screen,
                                                       image_url="https://image.tmdb.org/t/p/w500" + movie_poster))

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
    elif intent_name == "GetGameInfo":
        return get_game(intent, session, has_screen=has_screen)
    elif intent_name == "TrailerRequestIntent":
        return play_trailer(intent, session, has_screen=has_screen)
    elif intent_name == "GetGameTrailer":
        return play_trailer_by_game(intent, session, has_screen=has_screen)
    elif intent_name == "GetMovieReleaseDate":
        return get_release_date(intent, session, has_screen=has_screen)
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

# get_game(None, {}, False, game_name="black ops 4")
