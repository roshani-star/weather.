from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# Get API Key
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        else:

            url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

            try:

                response = requests.get(url, timeout=10)

                print("STATUS:", response.status_code)
                print("RESPONSE:", response.text)

                if response.status_code == 200:

                    data = response.json()

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temp": round(data["main"]["temp"]),
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "description": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"],
                    }

                elif response.status_code == 404:
                    error = "City not found."

                elif response.status_code == 401:
                    error = "Invalid API Key."

                else:
                    error = f"Error: {response.status_code}"

            except Exception as e:
                error = str(e)

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)