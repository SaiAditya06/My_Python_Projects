import requests

def weather():
    try:
        api_key = #enter your openweathermap api code in string type
        lat = str(input("Enter the Latitude: "))
        lon = str(input("Enter the Longitude: "))
        url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api_key
        request = requests.get(url)
        json = request.json()
        decs = json.get("weather")[0].get("description")
        temp_min0 = json.get("main").get("temp_min")
        temp_max0 = json.get("main").get("temp_max")
        temp_max = round(temp_max0 - 273.15)
        temp_min = round(temp_min0 - 273.15)
        city = json.get("name")
        humidity = json.get("main").get("humidity")

        return {"description": decs,"temp_min": temp_min,"temp_max": temp_max,"name": city,"humidity": humidity}

    except:
        print("There was an error while getting the information")


def main():
    weather_o_matic = weather()

    print("Today's forcast for",weather_o_matic.get("name"),"is",weather_o_matic.get("description"))

    if weather_o_matic.get("temp_min") == weather_o_matic.get("temp_max"):
        print("The exact temperature in celsius is",weather_o_matic.get("temp_min"))
        print("The humidity is",weather_o_matic.get("humidity"))
        print("")
    else:
        print("The minimum temperature in celsius is",weather_o_matic.get("temp_min"))
        print("The maximum temperature in celsius is",weather_o_matic.get("temp_max"))
        print("The humidity is",weather_o_matic.get("humidity"))
        print("")


while True:
    if __name__ == "__main__":
        main()
