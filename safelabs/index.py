import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from flask import Flask, jsonify, request

from safelabs.model.expense import Expense, ExpenseSchema
from safelabs.model.income import Income, IncomeSchema
from safelabs.model.transaction_type import TransactionType

from random import randint, shuffle

app = Flask(__name__)

@app.route('/weatherplaylist', methods=['POST'])
def weather_playlist():
    data = request.get_json()

    #validate request for necessary fields
    status = validate_request(data)
    if status is False :
        #else return error
        return "Invalid Request Format", 400

    current_temperature = query_temperature_location(data)
    #check if we got a valid response from OpenWeatherAPI
    if current_temperature is False:
        return "City not found or OpenWeatherAPI service is down", 404

    recommendedCategory = get_recommended_song_category(current_temperature)
    song_names_list = query_spotify_playlist(recommendedCategory)

    return json.dumps([song_names_list])

def validate_request(data):
    #checking the request fields if it was provided either a cityname or lat, long coordinates
    if not ('city' in data) and not ('lat' in data and 'long' in data):
        return False
    else:
        return True

def query_temperature_location(data):

    responseOpenWeather = ""
    if 'city' in data:
        cidade = data.get('city', '')
        responseOpenWeather = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+cidade+"&appid=b77e07f479efe92156376a8b07640ced")
    else:
        gpslat = data.get('lat', '')
        gpslong = data.get('long', '')
        responseOpenWeather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+gpslat+"&lon="+gpslong+"&appid=b77e07f479efe92156376a8b07640ced")

    #if invalid city coordinates or city name is provided at the request
    if int(responseOpenWeather.json()['cod']) == 404:
        return False

    temp_current = responseOpenWeather.json()['main']['temp']
    tempCelsius = temp_current - 273.15

    return tempCelsius

def get_recommended_song_category(temperature):
    if temperature > 30:
        recommendedCategory = "party"
    elif temperature > 15 and temperature <= 30:
        recommendedCategory = "pop"
    elif temperature > 10 and temperature <= 15:
        recommendedCategory = "rock"
    else:
        recommendedCategory = "classic"

    return recommendedCategory

def query_spotify_playlist(recommendedCategory):
    spotify_error = ""
    try:
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        #for most of the categories the category id matches the recommendedCategory (pop, rock, party) so we can query directly
        if recommendedCategory != "classic":
            playlists = spotify.category_playlists(recommendedCategory)

            size_list_result = len(playlists['playlists']['items'])

            #get a random result index to randomize the playlists a bit otherwise every query from that city will always return same list
            randomPos = randint(0, size_list_result - 1)

            playlist_id = playlists['playlists']['items'][randomPos]["id"]
        #the category id for classical music is 0JQ5DAqbMKFPrEiAOxgac3 but querying it doesn't the normal way specified at the API doesn't seem to work out
        #then let's get songs directly from a fingerpicked classical playlist with id 1h0CEZCm6IbFTbxThn6Xcs
        else:
            #playlist with best classical music on Spotify
            playlist_id = "1h0CEZCm6IbFTbxThn6Xcs"

        #query 20 songs of the selected playlist
        songs = spotify.playlist_items(playlist_id, None, 20)

        song_names_list = []
        for x in songs['items']:
            song_names_list.append(x['track']['name'])

        #random sort the list of song names
        shuffle(song_names_list)
        return song_names_list
    #catches any communications errors with Spotify
    except spotipy.exceptions.SpotifyException as e:
        spotify_error = "Error while querying Spotify. Details: " + str(e)
        return spotify_error

if __name__ == "__main__":
    app.run()
