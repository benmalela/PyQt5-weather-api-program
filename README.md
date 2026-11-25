# PyQt5 Weather App

A desktop weather application built with Python and PyQt5. Enter a city name to retrieve the current weather from OpenWeatherMap.

## Features

- Search by city name
- Display temperature in Fahrenheit
- Display a weather description
- Display an emoji that matches the weather condition
- Show clear messages for API, network, timeout, and redirect errors

## Requirements

- Python 3.10 or newer
- PyQt5
- Requests

Install the required packages with:

```bash
pip install PyQt5 requests
```

## API Key Setup

This program uses the OpenWeatherMap API.

1. Create an account at <https://openweathermap.org/>.
2. Generate an API key.
3. Replace the `api_key` value in `main.py` with your API key.

## Running the App

Open a terminal in this folder and run:

```bash
python main.py
```

Enter a city name, such as `London`, and select **Get weather**.

## How It Works

1. The app reads the city name from the text box.
2. It sends a request to the OpenWeatherMap API.
3. It converts the temperature from Kelvin to Fahrenheit.
4. It maps the weather condition code to an emoji.
5. It displays the temperature, emoji, and description in the window.
