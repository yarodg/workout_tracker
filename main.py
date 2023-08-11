import requests
from datetime import datetime
import os

# Nutritionix id and key.
APP_ID = os.environ["NT_APP_ID"]

API_KEY = os.environ["NT_API_KEY"]

# Personal data.
GENDER = "male"
WEIGHT = 85
HEIGHT = 185
AGE = 36

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/b3c6bee23cb39c46b9930d53b4001ec1/myWorkouts/workouts"

exercise = input("Tell me which exercises you did? ")

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

params = {
    "query": exercise,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=params, headers=header)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Sheety Authentication.

    bearer_headers = {
        "Authorization": f"Bearer {os.environ['NT_TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(sheet_response.text)

