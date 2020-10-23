import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    city_name = request.form['city']

    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = "{}".format(data["main"]["temp"])
    feels_like = "{}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    wind_speed = data["wind"]["speed"]
    
    

    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather, wind_speed=wind_speed)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['OPENWEATHERMAP']['api']

def get_weather_results(city_name, api_key):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()

print(get_weather_results('Glasgow', get_api_key()))

if __name__ == '__main__':
    app.run()