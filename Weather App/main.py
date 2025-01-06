import sys
import requests
from PyQt6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QLineEdit,
                             QWidget, QLabel, QPushButton)
from PyQt6.QtCore import Qt 
from dotenv import load_dotenv
import os

load_dotenv()
weather_api_key = os.getenv("weather_api_key")

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Weather App")

        qvbox = QVBoxLayout()
        qvbox.addWidget(self.city_label)
        qvbox.addWidget(self.city_input)
        qvbox.addWidget(self.get_weather_btn)
        qvbox.addWidget(self.temp_label)
        qvbox.addWidget(self.emoji_label)
        qvbox.addWidget(self.description_label)

        self.setLayout(qvbox)

        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Arial;
                font-size: 20px;
            }
            
            QLabel#city_label {
                font-size: 40px;
            }
            
            QLineEdit#city_input {
                font-size: 30px
            }

            QPushButton#get_weather_btn {
                font-size: 30px;
                background-color: #4CAF50;  /* Green */
                font-weight: bold;
            }    
                           
            QLabel#temp_label {
                font-size: 60px;
            }
                           
            QLabel#emoji_label {
                font-size: 60px;
                font-family: 'Segoe UI Emoji';
            }
                           
            QLabel#description_label {
                font-size: 30px;
            }
        """)

        self.get_weather_btn.clicked.connect(self.get_weather)

    def get_weather(self):
        print("Getting weather...")

        city = self.city_input.text()
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=imperial"

        try:
            response = requests.get(weather_url)
            response.raise_for_status()

            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.display_weather(weather_data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    print("Bad request. Please check input")
                case 401:
                    print("API key is invalid")
                case 403:
                    print("Access to the API is forbidden")
                case 404:
                    print("City not found")
                case 500:
                    print("Internal server error, try again later")
                case 502:
                    print("Bad gateway")
                case 503:
                    print("Service unavailable")
                case 504:
                    print("Gateway timeout")
                case _:
                    print(f"An error occurred: {http_error}")

        except requests.exceptions.ConnectionError:
            print("A connection error occurred")

        except requests.exceptions.Timeout:
            print("The request timed out")

        except requests.exceptions.TooManyRedirects:
            print("Too many redirects")

        except requests.exceptions.RequestException as req_error:
            print(f"An error occurred: {req_error}")

    def display_error(self, message):
        pass

    def display_weather(self, weather_data):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())