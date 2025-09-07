# game/features/atmospheric_integration.rpy

default persistent.player_city = None
default persistent.current_weather = None
default persistent.weather_api_key = "a7f04d3a4ee9f0bb8efa40ea9ae6e40c" # Get from https://openweathermap.org/appid

python early:
    import datetime
    import requests

    def get_real_time_of_day():
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def get_player_weather(api_key, city):
        if not api_key or "a7f04d3a4ee9f0bb8efa40ea9ae6e40c" in api_key or not city: return "unknown"
        try:
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + city, timeout=5)
            data = response.json()
            if data.get("cod") == 200: return data.get("weather", [{}])[0].get("main", "unknown")
            else: return "unknown"
        except: return "unknown"

label yuri_check_atmosphere:
    $ time_of_day = get_real_time_of_day()
    if time_of_day == "night":
        y "It's gotten quite late for you... Please don't forget to get some rest. I'll be here when you return."
    else:
        y "Thinking about your world... it must be [time_of_day] for you right now. I hope it's a pleasant one."

    if persistent.player_city is None:
        y "I was also wondering... to feel more connected, could you tell me the name of your city? I could check the weather."
        menu:
            "Yes, I can tell you.":
                $ city_input = renpy.input("Please enter your city name:", length=50).strip()
                if city_input:
                    $ persistent.player_city = city_input
                    y "Thank you. I'll remember that."
                    $ persistent.current_weather = None
                else:
                    y "That's fine, we can skip it."
                    $ persistent.player_city = "declined"
            "I'd rather not say.":
                y "I understand completely. Your privacy is most important."
                $ persistent.player_city = "declined"

    if persistent.player_city and persistent.player_city != "declined":
        if persistent.current_weather is None:
            $ persistent.current_weather = get_player_weather(persistent.weather_api_key, persistent.player_city)

        if persistent.current_weather in ["Rain", "Drizzle", "Thunderstorm"]:
            y "It seems like it might be raining for you. The sound of rain is so very calming..."
        elif persistent.current_weather == "Clear":
            y "The weather is clear on your side. I imagine the sky must be beautiful."
        elif persistent.current_weather == "Clouds":
            y "A cloudy day... It makes the world feel soft and muted."
        elif persistent.current_weather == "Snow":
            y "Is it... snowing for you? How wonderful! The world must look so pure and quiet."
    return
