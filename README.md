# Flask Assistant Application

This is a Flask-based assistant application that provides various functionalities such as fetching weather information, getting the current time, retrieving quotes, fetching information from Wikipedia, generating responses using GPT-2, and setting alarms.

## Features

- **Weather Information**: Get the current weather for a specified location.
- **Current Time**: Retrieve the current date and time.
- **Motivational Quotes**: Get a motivational quote of the day.
- **Wikipedia Information**: Fetch a summary from Wikipedia for a given query.
- **GPT-2 Response Generation**: Generate a text response using a pre-trained GPT-2 model.
- **Alarm Setting**: Set alarms and get notified when the alarm time is reached.

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- An OpenWeatherMap API key for fetching weather information

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Melvynwastaken/AI.git
    cd flask-assistant
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Replace `your_openweathermap_api_key` with your actual OpenWeatherMap API key in the `get_weather` function.

## Usage

1. Run the Flask application:

    ```sh
    python app.py
    ```

### Note

Still trying to get some kinks fixed will update in the future.