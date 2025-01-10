import sys
import requests
from PyQt6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QLineEdit,
                             QWidget, QLabel, QPushButton)
from PyQt6.QtCore import Qt 
from dotenv import load_dotenv
import os
import speech_recognition as sr  # Import speech_recognition directly

# Load API key from .env file
load_dotenv()
weather_api_key = os.getenv("weather_api_key")

# Define the main WeatherApp class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the widgets for each element
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.country_label = QLabel("Country: ", self)  # New country label
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.voice_recognition_btn = QPushButton("Use Voice Recognition", self)  # New button for voice recognition
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.humidity_label = QLabel(self)
        self.initUI()

    # Initialize the user interface
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        # Set the initial size of the window
        self.resize(800, 600)

        # Set up the layout
        qvbox = QVBoxLayout()
        qvbox.addWidget(self.city_label)
        qvbox.addWidget(self.city_input)
        qvbox.addWidget(self.country_label)  # Add country label to layout
        qvbox.addWidget(self.get_weather_btn)
        qvbox.addWidget(self.voice_recognition_btn)  # Add voice recognition button to layout
        qvbox.addWidget(self.temp_label)
        qvbox.addWidget(self.emoji_label)
        qvbox.addWidget(self.description_label)
        qvbox.addWidget(self.humidity_label)

        self.setLayout(qvbox)

        # Align the widgets
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.country_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align country label
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.country_label.setObjectName("country_label")  # Set object name for country label
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.voice_recognition_btn.setObjectName("voice_recognition_btn")  # Set object name for voice recognition button
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.humidity_label.setObjectName("humidity_label")

        # Apply modern styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            
            QLabel, QPushButton {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 20px;
                color: #333;
            }
            
            QLabel#city_label, QLabel#country_label {
                font-size: 40px;
                color: #444;
            }
            
            QLineEdit#city_input {
                font-size: 30px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }

            QPushButton#get_weather_btn {
                font-size: 30px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }

            QPushButton#voice_recognition_btn {
                font-size: 30px;
                background-color: #007BFF;  /* Blue */
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }    
                           
            QLabel#temp_label {
                font-size: 60px;
                color: #333;
            }
                           
            QLabel#emoji_label {
                font-size: 60px;
                font-family: 'Segoe UI Emoji';
            }
                           
            QLabel#description_label {
                font-size: 30px;
                color: #666;
            }

            QLabel#humidity_label {
                font-size: 30px;
                color: #666;
            }
        """)

        # Connect the buttons to their respective methods
        self.get_weather_btn.clicked.connect(self.get_weather)
        self.voice_recognition_btn.clicked.connect(self.use_voice_recognition)  # Connect voice recognition button

    # Fetch weather data from the API
    def get_weather(self):
        city = self.city_input.text()
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=imperial"

        try:
            response = requests.get(weather_url)
            response.raise_for_status()

            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.display_weather(weather_data)
                self.country_label.setText(f"Country: {weather_data['sys']['country']}")  # Update country label
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request. Please check input")
                case 401:
                    self.display_error("API key is invalid")
                case 403:
                    self.display_error("Access to the API is forbidden")
                case 404:
                    self.display_error("City not found")
                case 500:
                    self.display_error("Internal server error, try again later")
                case 502:
                    self.display_error("Bad gateway")
                case 503:
                    self.display_error("Service unavailable")
                case 504:
                    self.display_error("Gateway timeout")
                case _:
                    self.display_error(f"An error occurred: {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("A connection error occurred")

        except requests.exceptions.Timeout:
            self.display_error("The request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"An error occurred: {req_error}")

    # Use voice recognition to get the city name
    def use_voice_recognition(self):
        city = self.recognize()
        if city:
            self.city_input.setText(city)
            self.get_weather()

    # Listen for voice input
    def listen(self):
      r = sr.Recognizer()
      with sr.Microphone() as source:
          self.voice_recognition_btn.setText("Listening...")
          self.voice_recognition_btn.setStyleSheet("background-color: #4CAF50; color: white;")  # Green
          QApplication.processEvents()  # Update the button text and color immediately
          audio_text = r.listen(source)
          self.voice_recognition_btn.setText("Use Voice Recognition")
          self.voice_recognition_btn.setStyleSheet("background-color: #007BFF; color: white;")  # Blue
          try:
              audio_text = r.listen(source)
              return r.recognize_google(audio_text)
          except sr.UnknownValueError:
              return "Sorry, I couldn't understand the audio."
          except sr.RequestError:
              return "Sorry, there was an issue connecting to the recognition service."

    # Recognize the city name from voice input
    def recognize(self):
        command = listen().lower()
        
        weather_keywords = ['weather', 'temperature', 'forecast', 'climate', 'how is the weather', 'what is the weather', 'how’s the weather']
        
        if any(keyword in command for keyword in weather_keywords):
            if "in" in command:
                location = command.split("in")[-1].strip() #extract location from command
                return location
            else:
                print("No specific location mentioned in the command.")
                return "No location specified"
        else:
            print("No weather-related command detected.")
            return None

    # Display error messages
    def display_error(self, message):
        self.temp_label.setStyleSheet("color: red; font-size: 30px;")
        self.temp_label.setText(message)

    # Get emoji based on weather description
    def get_emoji(self, description):
        description = description.lower()
        if "clear" in description:
            return "☀️"
        elif "cloud" in description:
            return "☁️"
        elif "rain" in description:
            return "🌧️"
        elif "snow" in description:
            return "❄️"
        elif "thunderstorm" in description:
            return "⛈️"
        elif "mist" in description or "fog" in description:
            return "🌫️"
        else:
            return "🌈"

    # Display weather data
    def display_weather(self, weather_data):
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        emoji = self.get_emoji(description)
        humidity = weather_data["main"]["humidity"]

        # Round the temperature to one decimal place
        rounded_temp = round(temp, 1)

        self.temp_label.setText(f"{rounded_temp}°F")
        self.temp_label.setStyleSheet("color: black; font-size: 30px;")
        self.emoji_label.setText(emoji)
        self.description_label.setText(description)
        self.humidity_label.setText(f"Humidity: {humidity}%")

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
