from __future__ import print_function
import random
import boto3
import json
import urllib2
import urllib
from boto3.dynamodb.conditions import Key, Attr

info = "Your favourite movie expert, right here, on Amazon Alexa."

intro = "Welcome to your local movie expert for Amazon Alexa, would you like to learn how to use this skill?"

how_to = "To ask for more details about a movie, say. Alexa, ask the movie expert all about, then say your movie name. I'll try my best to understand you and get the right film"

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
                'title': "The Movie Expert - " + title,
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
                        "token": "movie",
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
            'title': "The Movie Expert - " + title,
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
                                                                       "Would you like to learn how to use the movie expert skill?",
                                                                       "Your number one source for all information about your favourite movies!", False))

'''
This is called when we can't find a movie based on their title, so just say sorry can't find that
'''
def no_movie_found(movie):
    movie_doesnt_exist = "I'm sorry but I can't find the movie, " + movie + " on the records. Please try again"
    return build_response({}, build_speechlet_response_no_card(movie_doesnt_exist, movie_doesnt_exist, True))

'''
This is called when there is no movie in the slot. Reprompting the user to repeat themselves
'''
def cant_find_movie(session):
    movie_doesnt_exist = "I'm sorry but I didn't catch that movie. What movie would you like information on?"

    session['MOVIE'] = 'True'

    return build_response(session, build_speechlet_response_no_card(movie_doesnt_exist, movie_doesnt_exist, False))

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('MovieExpertMemory')
response = table.scan()

def store_movie(movie_id, id):
    try:
        response = table.update_item(Key={'userId': id},
                                     UpdateExpression="set recent = :t",
                                     ExpressionAttributeValues={
                                         ':t': movie_id
                                     },
                                     ReturnValues="UPDATED_NEW"
                                     )
    except Error as e:
        response = table.put_item(Key={'userId': id, 'recent': movie_id})

def load_movie(id):
    try:
        response = table.get_item(Key={'userId': id})
        return response['Item']['recent']
    except:
        return None

def get_movie_from_name(name):
    try :
        req = urllib2.Request("https://api.themoviedb.org/3/search/movie?" + \
                              "api_key=2f35de043b8ec38c8a47271303d59169&" + \
                              "language=en-US&" + \
                              urllib.urlencode({'query': name}) + "&" + \
                              "page=1&" + \
                              "include_adult=false", headers={'User-Agent': "Magic Browser"})

        response = str(urllib2.urlopen(req).read())
        d = json.loads(response)
        results = d['results']

        if (len(results) > 0):
            return results[0]

        return None
    except Exception as e:
        pass

def get_movie(intent, session, has_screen=False, movie_name = None):
    try:
        if (movie_name is None):
            try:
                movie_name = intent['slots']['MovieName']['value']
            except:
                return cant_find_movie(session)

        the_movie_i_want = get_movie_from_name(movie_name)

        if (the_movie_i_want is None):
            return no_movie_found(movie_name)

        movie_title = the_movie_i_want['title']
        movie_id = the_movie_i_want['id']
        movie_release_date = the_movie_i_want['release_date']
        movie_vote_average = str(the_movie_i_want['vote_average'])
        movie_poster = the_movie_i_want['poster_path']
        movie_overview = the_movie_i_want['overview']
        movie_backdrop = the_movie_i_want['backdrop_path']

        store_movie(movie_id, session['user']['userId'])

        output = "The film " + movie_title + ", was released on " + movie_release_date + " and has achieved an average viewer rating of " + movie_vote_average + ". "
        output = output + "The overview is as follows. " + movie_overview + " "

        if has_screen:
            output = output + "If you would like to watch the trailer, say. Alexa, ask the movie expert to show me the trailer"

        return build_response({}, build_speechlet_response(movie_title, output, "", output, True, has_screen=has_screen, image_url="https://image.tmdb.org/t/p/w500" + movie_poster, background_image_url="https://image.tmdb.org/t/p/w500" + movie_backdrop))
    except Exception as e:
        print(e)
        return build_response({}, build_speechlet_response_no_card("I appear to be having trouble connecting to the Movie server. Sorry", "", True))

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
                          build_speechlet_response("How to Use, The Movie Expert", res, re_prompt, how_to, close))

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

def play_trailer_by_movie_id(id, has_screen=False):
    try:
        if not (has_screen):
            return build_response({}, build_speechlet_response_no_card("Unfortunately, this device doesn't support video playback", None, True))

        try:
            req = urllib2.Request("https://api.themoviedb.org/3/movie/" + str(id) + "/videos?api_key=2f35de043b8ec38c8a47271303d59169&language=en-US", headers={'User-Agent': "Magic Browser"})

            response = str(urllib2.urlopen(req).read())
            d = json.loads(response)
            results = d['results']

            if (len(results) <= 0):
                return build_response({}, build_speechlet_response_no_card("Unfortunately, the previous movie doesn't have a trailer according to our records.", None, True))

            trailer = None

            for video in results:
                if (video['type'] == 'Trailer'):
                    trailer = video
                    break

            if trailer is None:
                return build_response({}, build_speechlet_response_no_card("Unfortunately, the previous movie doesn't have a trailer according to our records.", None, True))

            youtube_link = get_stream_links(trailer['key'])

            if (len(youtube_link) <= 0):
                return build_response({}, build_speechlet_response_no_card("I had some trouble finding the trailer for this movie, please try again.", None, True))

            link = youtube_link[0]['url']

            return build_video(link, trailer['name'], "Trailer loaded from The Movie Database")
        except Exception as e:
            print(e)
            return build_response({}, build_speechlet_response_no_card("I had some trouble finding the trailer, please try again.", None, True))
    except Exception as oopsie:
        print(oopsie)
        return build_response({}, build_speechlet_response_no_card("I had some trouble finding the trailer, please try again.", None, True))

def play_trailer_by_movie(intent, session, has_screen=False):
    the_movie = get_movie_from_name(intent['slots']['TrailerMovieName']['value'])

    if the_movie is None:
        return build_response({},build_speechlet_response_no_card("I cannot find the movie " + intent['slots']['TrailerMovieName']['value'],None, True))

    return play_trailer_by_movie_id(the_movie['id'], has_screen)

def play_trailer(intent, session, has_screen=False):
    movie_id = load_movie(session['user']['userId'])

    if (movie_id is None):
        return build_response({} ,build_speechlet_response_no_card("Please request a film before you can see the trailer!", None, True))

    return play_trailer_by_movie_id(movie_id, has_screen)

def get_release_date(intent, session, has_screen=False):
    the_movie = get_movie_from_name(intent['slots']['ReleaseMovieName']['value'])

    if the_movie is None:
        return build_response({}, build_speechlet_response_no_card("I cannot find the movie " + intent['slots']['ReleaseMovieName']['value'], None, True))

    movie_title = the_movie['title']
    movie_id = the_movie['id']
    movie_release_date = the_movie['release_date']
    movie_vote_average = str(the_movie['vote_average'])
    movie_poster = the_movie['poster_path']
    movie_overview = the_movie['overview']

    store_movie(movie_id, session['user']['userId'])

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
    elif intent_name == "GetMovieInfo":
        return get_movie(intent, session, has_screen=has_screen)
    elif intent_name == "TrailerRequestIntent":
        return play_trailer(intent, session, has_screen=has_screen)
    elif intent_name == "GetMovieTrailer":
        return play_trailer_by_movie(intent, session, has_screen=has_screen)
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
