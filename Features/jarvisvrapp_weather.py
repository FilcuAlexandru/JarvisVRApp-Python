from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QTextOption

import requests
from datetime import datetime

class WeatherDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Check Weather")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        font = QFont("Roboto", 12, QFont.Normal)

        self.city_field = QLineEdit()
        self.city_field.setFont(font)
        self.city_field.setPlaceholderText("Enter the name of the city")
        self.city_field.setStyleSheet(
            "QLineEdit { border: 2px solid #CCCCCC; border-radius: 10px; padding: 10px; }"
            "QLineEdit:focus { border-color: #007AFF; }"
        )
        layout.addWidget(self.city_field)

        self.check_button = QPushButton("Check Weather")
        self.check_button.setFont(font)
        self.check_button.setStyleSheet(
            "QPushButton { background-color: #007AFF; color: white; border-radius: 10px; padding: 10px; }"
            "QPushButton:hover { background-color: #0056B3; }"
        )
        self.check_button.clicked.connect(self.check_weather)
        layout.addWidget(self.check_button)

        self.weather_text = QTextEdit()
        self.weather_text.setFont(font)
        layout.addWidget(self.weather_text)

    def check_weather(self):
        api_key = "YourAPIKey"
        city_name = self.city_field.text().strip()

        if city_name:
            try:
                # Get current weather
                current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
                current_weather_response = requests.get(current_weather_url)
                current_weather_data = current_weather_response.json()

                # Get 3-day forecast
                forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}'
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()

                if current_weather_response.status_code == 200 and forecast_response.status_code == 200:
                    # Display current weather
                    current_weather_description = current_weather_data['weather'][0]['description']
                    current_temperature = current_weather_data['main']['temp']
                    current_temperature_celsius = current_temperature - 273.15  # Convert temperature to Celsius

                    # Display 2-day forecast
                    forecast_text = "3-Day Forecast:\n"
                    for entry in forecast_data['list'][:8 * 2]:
                        forecast_time = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')
                        forecast_description = entry['weather'][0]['description']
                        forecast_text += f"{forecast_time}: {forecast_description}\n"

                    self.weather_text.setPlainText(f"Current Weather:\nDescription: {current_weather_description}\nTemperature: {current_temperature_celsius:.2f} °C\n\n{forecast_text}")
                else:
                    QMessageBox.critical(self, "Error", "Failed to fetch weather data.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "No City Entered", "Please enter the name of the city.")
