from flask import Flask, request, jsonify
import requests
import wikipediaapi
from datetime import datetime,timedelta
from transformers import pipeline
import threading
import time
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# pre trained cause why not
nlp = pipeline("text-generation", model="gpt-3.5-turbo")

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
    
def get_page_html(title):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=parse&section=0&prop=text&format=json&page={title}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        html_content = data['parse']['text']['*']
        return html_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        return None
    except KeyError as e:
        print(f"KeyError: {e}. JSON response does not contain expected structure.")
        return None

def get_first_infobox(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_='infobox')
    if not results:
        raise LookupError('Page has no infobox')
    return results[0]

def clean_text(text):
    only_ascii = ''.join([char if char in string.printable else ' ' for char in text])
    no_dup_spaces = re.sub(' +', ' ', only_ascii)
    no_dup_newlines = re.sub('\n+', '\n', no_dup_spaces)
    return no_dup_newlines

def get_first_infobox_text(title):
    html = get_page_html(title)
    if html is None:
        return "Failed to retrieve Wikipedia page."
    
    try:
        infobox = get_first_infobox(html)
        infobox_text = clean_text(infobox.text)
        return infobox_text
    except Exception as e:
        print(f"Error processing infobox: {e}")
        return "An error occurred while processing the Wikipedia page."
# GPT
openai.api_key = '' # put your key here

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


alarms = []

def check_alarms():
    while True:
        current_time = datetime.now()
        for alarm in alarms:
            if current_time >= alarm['time'] and not alarm['triggered']:
                print(f"Alarm: {alarm['message']}")
                alarm['triggered'] = True
        time.sleep(1)

threading.Thread(target=check_alarms, daemon=True).start()

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    data = request.json
    alarm_time_str = data.get('time')
    alarm_message = data.get('message', 'Alarm!')

    try:
        alarm_time = datetime.strptime(alarm_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid time format. Use YYYY-MM-DD HH:MM:SS"}), 400

    alarms.append({
        'time': alarm_time,
        'message': alarm_message,
        'triggered': False
    })

    return jsonify({"status": "Alarm set", "time": alarm_time_str, "message": alarm_message})
