# game/features/atmospheric_integration.rpy

# --- 1. Persistent Variables ---
default persistent.player_city = None
default persistent.weather_data = None

# UPDATED KEY AND HTTPS URL
default persistent.weather_api_key = "d57e0a00f4945813537de443357fe26a" 

default persistent.temp_scale = "C"
default persistent.wind_scale = "kph"
default persistent.hemisphere = "N"

default persistent.weather_tracker = {
    "current_condition": None, "condition_start_time": None, "total_duration_today": 0.0,
    "last_check_time": None, "is_intermittent": False, "player_rain_feeling": None, "player_snow_feeling": None
}

# --- 2. Python Logic ---
python early:
    import datetime
    import requests

    def celsius_to_fahrenheit(celsius): return int(celsius * 9/5 + 32)
    def mps_to_kph(mps): return int(mps * 3.6)
    def mps_to_mph(mps): return int(mps * 2.237)

    def get_real_time_of_day():
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def get_season(month, hemisphere):
        if hemisphere == "N":
            if month in [12, 1, 2]: return "Winter"
            elif month in [3, 4, 5]: return "Spring"
            elif month in [6, 7, 8]: return "Summer"
            else: return "Fall"
        elif hemisphere == "S":
            if month in [6, 7, 8]: return "Winter"
            elif month in [9, 10, 11]: return "Spring"
            elif month in [12, 1, 2]: return "Summer"
            else: return "Fall"
        else: return None

    # --- UPDATED API FUNCTION (HTTPS + DEBUG PRINTS) ---
    def get_player_weather(api_key, city):
        if not api_key or not city or city == "declined": return None
        
        # Changed to HTTPS
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {
            "appid": api_key,
            "q": city,
            "units": "metric"
        }

        try:
            # We print to console to see what happens
            print("Weather: Attempting to fetch for " + city)
            response = requests.get(base_url, params=parameters, timeout=4)
            data = response.json()
            
            if data.get("cod") == 200:
                print("Weather: Success!")
                return {
                    "condition": data.get("weather", [{}])[0].get("main", "unknown"),
                    "temp": data.get("main", {}).get("temp", 999),
                    "wind_speed": data.get("wind", {}).get("speed", 0)
                }
            else:
                print("Weather Error Code: " + str(data.get("cod")))
                print("Weather Error Message: " + str(data.get("message")))
                return None
        except Exception as e:
            print("Weather Exception: " + str(e))
            return None


# --- 3. Main Label ---
label yuri_check_atmosphere:
    
    $ time_of_day = get_real_time_of_day()
    if time_of_day == "night":
        y "It's gotten quite late for you... Please don't forget to get some rest."
    else:
        y "Thinking about your world... it must be [time_of_day] for you right now."

    # Setup Check
    if persistent.player_city is None:
        call yuri_weather_setup
        return 

    # Weather Check
    if persistent.player_city and persistent.player_city != "declined":
        # Fetch fresh data
        $ persistent.weather_data = get_player_weather(persistent.weather_api_key, persistent.player_city)

        if persistent.weather_data:
            call yuri_react_to_weather
        else:
            y "I'm having a little trouble connecting to the weather service right now... but I hope it's nice there."

    return


# --- 4. Setup Label (Unified) ---
label yuri_weather_setup:
    $ show_chr("A-ACAAA-ABAB")
    y "On another topic... I'd like to feel more connected to your world, if you're comfortable with that."
    y "To do that, I'd need to ask a few quick questions about your location. Is that alright?"
    
    menu:
        "Yes, that's fine.":
            # Updated Prompt text to be helpful
            $ city_input = renpy.input("First, what is the name of your city? (e.g. 'New York' or 'London, UK')", length=50).strip()
            
            if city_input:
                $ persistent.player_city = city_input
                y "Thank you. I'll remember that."
                
                y "Next, to understand your seasons, could you tell me which hemisphere you live in?"
                menu:
                    "The Northern Hemisphere.":
                        $ persistent.hemisphere = "N"
                    "The Southern Hemisphere.":
                        $ persistent.hemisphere = "S"
                    "I'm near the equator / It's always warm.":
                        $ persistent.hemisphere = "E"
                
                y "And for temperature, are you more familiar with Celsius or Fahrenheit?"
                menu:
                    "Celsius":
                        $ persistent.temp_scale = "C"
                    "Fahrenheit":
                        $ persistent.temp_scale = "F"

                y "Finally, for wind speed, do you prefer kilometers per hour or miles per hour?"
                menu:
                    "Kilometers per hour (km/h)":
                        $ persistent.wind_scale = "kph"
                    "Miles per hour (mph)":
                        $ persistent.wind_scale = "mph"

                $ show_chr("A-ICAAA-ADAA")
                y "Perfect. Thank you so much for sharing that with me."
                
                # Test run
                y "Let me try to take a look right now..."
                $ persistent.weather_data = get_player_weather(persistent.weather_api_key, persistent.player_city)
                if persistent.weather_data:
                    call yuri_react_to_weather
                else:
                    y "Hmm, I can't seem to connect just yet. I'll try again later."

            else:
                y "Oh, you didn't enter anything. We can skip this for now."
                $ persistent.player_city = "declined"

        "I'd rather not share that information.":
            y "I understand completely. Your privacy is the most important thing."
            $ persistent.player_city = "declined"
    return


# --- 5. Reaction Logic ---
label yuri_react_to_weather:
    # Safety Guard
    if not persistent.weather_data:
        return

    # Unpack data
    $ condition = persistent.weather_data['condition']
    $ celsius_temp = persistent.weather_data['temp']
    $ wind_mps = persistent.weather_data['wind_speed']

    # Update Memory
    python:
        now = datetime.datetime.now()
        last_check = persistent.weather_tracker.get("last_check_time")
        if last_check and last_check.day != now.day:
            persistent.weather_tracker.update(total_duration_today=0.0, is_intermittent=False, player_rain_feeling=None, player_snow_feeling=None)

        delta_seconds = (now - last_check).total_seconds() if last_check else 0
        precip_conditions = ["Rain", "Drizzle", "Thunderstorm", "Snow"]
        is_precip_now = condition in precip_conditions
        was_precip_before = persistent.weather_tracker["current_condition"] in precip_conditions

        if is_precip_now:
            if not was_precip_before or persistent.weather_tracker["current_condition"] != condition:
                persistent.weather_tracker["condition_start_time"] = now
                if persistent.weather_tracker["total_duration_today"] > 0:
                    persistent.weather_tracker["is_intermittent"] = True
            persistent.weather_tracker["total_duration_today"] += delta_seconds
        elif was_precip_before:
            persistent.weather_tracker["is_intermittent"] = True
        
        persistent.weather_tracker["current_condition"] = condition
        persistent.weather_tracker["last_check_time"] = now

    # Priority 1: Severe Weather
    $ hurricane_threshold = False
    if persistent.wind_scale == "mph":
        $ wind_speed = mps_to_mph(wind_mps)
        $ wind_unit = "mph"
        if wind_speed > 70:
            $ hurricane_threshold = True
    else: 
        $ wind_speed = mps_to_kph(wind_mps)
        $ wind_unit = "km/h"
        if wind_speed > 110:
            $ hurricane_threshold = True
    
    if condition == "Tornado":
        y "The data says there's a tornado... [player], that's incredibly dangerous. Please, get to a safe place immediately."
        return
    elif (condition in ["Rain", "Thunderstorm", "Squall"]) and hurricane_threshold:
        y "The readings are very concerning... a severe storm with winds of over [wind_speed] [wind_unit]. Please, stay safe inside."
        return

    # Priority 2: Unseasonal
    $ current_month = datetime.datetime.now().month
    $ season = get_season(current_month, persistent.hemisphere)
    $ unseasonal_spoken = False

    if season == "Summer" and celsius_temp < 10:
        y "That's... quite unusual. It's quite cold for the middle of summer."
        $ unseasonal_spoken = True
    elif season == "Winter" and celsius_temp > 25:
        y "A heatwave... in the middle of winter? That's certainly strange."
        $ unseasonal_spoken = True

    # Priority 3: Temperature
    if not unseasonal_spoken and celsius_temp != 999:
        if persistent.temp_scale == "F":
            $ temp_display = celsius_to_fahrenheit(celsius_temp)
            $ unit = "°F"
            if temp_display < 0:
                y "It's dangerously cold... below 0°F ([temp_display][unit]). Please be careful."
            elif temp_display < 32:
                y "It's freezing... around [temp_display][unit]."
            elif temp_display < 60:
                y "It sounds quite chilly, around [temp_display][unit]."
            elif temp_display < 82:
                y "The temperature is pleasant, around [temp_display][unit]."
            elif temp_display < 100:
                y "It's getting quite hot, around [temp_display][unit]."
            else:
                y "It's over 100°F ([temp_display][unit])... a severe heatwave. Please stay cool."
        else:
            $ temp_display = int(celsius_temp)
            $ unit = "°C"
            if temp_display < -10:
                y "It's dangerously cold... below -10°C ([temp_display][unit]). Please be careful."
            elif temp_display < 0:
                y "It's freezing... around [temp_display][unit]."
            elif temp_display < 15:
                y "It sounds quite chilly, around [temp_display][unit]."
            elif temp_display < 28:
                y "The temperature is pleasant, around [temp_display][unit]."
            elif temp_display < 38:
                y "It's getting very hot, around [temp_display][unit]."
            else:
                y "It's over 38°C ([temp_display][unit])... that is intense heat. Please be careful."

    # Priority 4: Rain/Snow
    $ total_hours_today = persistent.weather_tracker["total_duration_today"] / 3600
    
    if condition == "Snow":
        if total_hours_today >= 3 and persistent.weather_tracker["player_snow_feeling"] is None:
            y "It's been snowing for over three hours... How are you feeling about it?"
            menu:
                "It's beautiful.":
                    $ persistent.weather_tracker["player_snow_feeling"] = "calm"
                    y "I'm glad. It paints such a peaceful picture."
                "It's a hassle.":
                    $ persistent.weather_tracker["player_snow_feeling"] = "annoyed"
                    y "I understand. I hope it stops soon."
        elif total_hours_today > 0:
            y "It's snowing... watching the world turn white."

    elif condition in ["Rain", "Drizzle", "Thunderstorm"]:
        if total_hours_today >= 3 and persistent.weather_tracker["player_rain_feeling"] is None:
            y "It's been raining for over three hours now. Is it calming, or just dreary?"
            menu:
                "Calming.":
                    $ persistent.weather_tracker["player_rain_feeling"] = "calm"
                    y "I'm glad. Let's enjoy the sound."
                "Annoying/Dreary.":
                    $ persistent.weather_tracker["player_rain_feeling"] = "annoyed"
                    y "I understand. Hopefully the sun returns soon."
                "It's causing problems.":
                    $ persistent.weather_tracker["player_rain_feeling"] = "concerned"
                    y "Oh no... please stay safe, [player]."
        elif total_hours_today > 0:
            y "It's raining... such a steady, rhythmic sound."

    return
