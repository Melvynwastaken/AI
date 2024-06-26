from flask import Flask, request, jsonify
import requests
import wikipedia
from datetime import datetime
from transformers import pipeline

app = Flask(__name__)

# pre trained cause why not
nlp = pipeline("text-generation", model="gpt2")

# get ur api key first
def get_weather(location):
    api_key = 'your_openweathermap_api_key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    else:
        return {'error': 'Location not found'}

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_quote():
    response = requests.get('https://quotes.rest/qod?language=en')
    if response.status_code == 200:
        return response.json()['contents']['quotes'][0]['quote']
    else:
        return 'Could not retrieve quote at this time.'

def get_wikipedia_info(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f'There are multiple results for "{query}". Please be more specific.'
    except wikipedia.exceptions.PageError:
        return 'No results found for your query.'

# GPT-2
def generate_response(prompt):
    responses = nlp(prompt, max_length=50, num_return_sequences=1)
    return responses[0]['generated_text']

def handle_query(query):
    query = query.lower()

    if 'weather' in query:
        location = query.split("in")[-1].strip()
        weather_info = get_weather(location)
        if 'error' in weather_info:
            return weather_info['error']
        return f"The weather in {location} is {weather_info['description']} with a temperature of {weather_info['temperature']}°C."
    elif 'time' in query or 'date' in query:
        return f"The current time is {get_time()}."
    elif 'quote' in query:
        return get_quote()
    elif 'who is' in query or 'tell me about' in query or 'summary of' in query:
        topic = query.replace('who is', '').replace('tell me about', '').replace('summary of', '').strip()
        return get_wikipedia_info(topic)
    elif 'when was' in query:
        topic = query.replace('when was', '').replace('born', '').strip()
        return get_wikipedia_info(topic)
    else:
        return generate_response(query)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')
    response = handle_query(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
