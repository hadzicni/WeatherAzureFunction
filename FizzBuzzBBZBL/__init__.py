import logging
import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Stadt aus Query oder Body holen
    city = req.params.get('city')
    if not city:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        city = req_body.get('city')

    if not city:
        return func.HttpResponse(
            "Bitte geben Sie eine Stadt (city) an, z. B. ?city=Zürich",
            status_code=400
        )

    # API-Key aus Umgebungsvariable lesen (z. B. in Azure hinterlegen)
    api_key = os.environ.get("OPENWEATHER_API_KEY", "cb8db7cef5d9c6cc4a3079bc4109c793")

    # URL für OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=de&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Temperatur oder andere Daten aus dem JSON extrahieren
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]

        return func.HttpResponse(
            f"Das Wetter in {city}: {temp} °C, {description}",
            status_code=200
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Abrufen der Wetterdaten: {e}")
        return func.HttpResponse(
            "Es gab ein Problem beim Abrufen der Wetterdaten.",
            status_code=500
        )
