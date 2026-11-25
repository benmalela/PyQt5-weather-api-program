# Import the system module for command-line arguments and app exit handling
import sys

# Import the requests package for sending HTTP requests to the weather API
import requests

# Import the PyQt5 classes needed to create the window, labels, input, button, and layout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Import Qt tools for setting text alignment
from PyQt5.QtCore import Qt

# Define the weather app window by inheriting from QWidget
class WeatherApp(QWidget):
    def __init__(self):
        # Initialize the parent QWidget class
        super().__init__()

        # Create the label that prompts the user to enter a city
        self.city_label = QLabel("Enter city name: ", self)

        # Create a text box where the city name will be entered
        self.city_input = QLineEdit(self)

        # Create the button that starts the weather request
        self.get_weather_button = QPushButton("Get weather", self)

        # Create labels for the temperature, emoji, and weather description
        self.temperature_label = QLabel( self)
        self.emoji_label = QLabel( self)
        self.description_label = QLabel( self)

        # Call the method that creates and styles the user interface
        self.initUI()

    def initUI(self):
        # Set the title shown in the window's title bar
        self.setWindowTitle("Weather App")

        # Create a vertical layout to stack the interface elements
        vbox = QVBoxLayout()

        # Add the city prompt, input box, button, and weather labels to the layout
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        # Apply the vertical layout to this weather window
        self.setLayout(vbox)

        # Center the text inside each label and the city input box
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Give each widget a unique object name so its style can be targeted by CSS
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Apply CSS-like styling to the labels, input box, and button
        self.setStyleSheet("""
                    QLabel, QPushButton{
                        font-family: Arial;

                    }
                    QLabel#city_label{
                        font-size: 40px;
                        font-style: italic;
                    }
                    QLineEdit#city_input{
                        font-size: 40px;
                        padding: 5px;
                    }
                    QPushButton#get_weather_button{
                        font-size: 30px;
                        font-weight: bold;
                    }
                    QLabel#temperature_label{
                        font-size: 75px;
                    }
                    QLabel#emoji_label{
                        font-size: 100px;
                        font-family: Apple Color emoji;  /* change to 'Segoe UI emoji' if using Windows OS */
                    }
                    QLabel#description_label{
                        font-size: 50px;
                    }
                            """)

        # Connect the button click to the method that retrieves weather data
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # Store the API key used to authenticate with OpenWeatherMap
        api_key = "YOUR_API_KEY_HERE"

        # Read the city name entered by the user
        city = self.city_input.text()

        # Build the API URL using the city name and API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            # Send a GET request to the OpenWeatherMap API
            response = requests.get(url)

            # Raise an HTTPError if the response reports an unsuccessful status
            response.raise_for_status()

            # Convert the JSON response into a Python dictionary
            data = response.json()

            # The API uses the numeric code 200 for a successful response
            if data["cod"] ==  200:
                self.display_weather(data)

        # Handle unsuccessful HTTP responses and show the appropriate message
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        # Handle an internet or network connection failure
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        # Handle a request that takes too long to complete
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        # Handle a URL that repeatedly redirects to another location
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck URL")

        # Handle any other type of requests-related error
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")

    def display_error(self, message):
        # Use a smaller font for error messages
        self.temperature_label.setStyleSheet("font-size: 30px;")

        # Display the error in the temperature label
        self.temperature_label.setText(message)

        # Clear the emoji and description labels
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        # Restore the larger font used for successful temperature displays
        self.temperature_label.setStyleSheet("font-size: 75px;")

        # Read the temperature in Kelvin and convert it to Celsius and Fahrenheit
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9 / 5 ) - 459.67

        # Read the weather ID and human-readable description from the API response
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        # Display Fahrenheit temperature, matching emoji, and weather description
        self.temperature_label.setText(f"{temperature_f:.0f}℉")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        # Return a thunderstorm emoji for thunderstorm weather codes
        if 200 <= weather_id <= 232:
            return "⛈️"

        # Return a partly cloudy emoji for drizzle weather codes
        elif 300 <= weather_id <= 321:
            return "🌥️"

        # Return a rain emoji for rain weather codes
        elif 500 <= weather_id <= 531:
            return "🌧️"

        # Return a snow emoji for snow weather codes
        elif 600 <= weather_id <= 622:
            return "❄️"

        # Return a fog emoji for mist and haze weather codes
        elif 701 <= weather_id <= 741:
            return "🌫️"

        # Return a volcano emoji for volcanic ash
        elif weather_id == 762:
            return "🌋"

        # Return a wind emoji for squalls
        elif weather_id == 771:
            return "💨"

        # Return a tornado emoji for tornado conditions
        elif weather_id == 781:
            return "🌪️"

        # Return a sun emoji for clear weather
        elif weather_id == 800:
            return "☀️"

        # Return a cloud emoji for cloudy weather codes
        elif weather_id <= 804:
            return "☁️"

        # Return an empty string if no matching weather code is found
        else:
            return ""

# Ensure this code runs only when the script is executed directly
if __name__ == '__main__':
    # Create the main application object (required for every PyQt5 app)
    app = QApplication(sys.argv)

    # Create an instance of the WeatherApp window
    weather_app = WeatherApp()

    # Make the window visible on the screen
    weather_app.show()

    # Start the application's event loop and cleanly exit when the window closes
    sys.exit(app.exec_())