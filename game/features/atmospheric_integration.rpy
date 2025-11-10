# game/features/atmospheric_integration.rpy

# This is the complete Atmospheric Integration feature. It allows Yuri to be aware of the player's real-world time,
# weather, temperature, wind, and severe or unseasonal events, reacting with nuance and memory.

# --- Default variables ---
default persistent.player_city = None
default persistent.weather_data = None
default persistent.weather_api_key = "a7f04d3a4ee9f0bb8efa40ea9ae6e40c" # Get a free key from https://openweathermap.org/appid
default persistent.temp_scale = None # Player's choice: "C" or "F"
default persistent.wind_scale = None # Player's choice: "kph" or "mph"
default persistent.hemisphere = None # Player's choice: "N", "S", or "E"
default persistent.last_weather_report_day = None

# The advanced weather memory system
default persistent.weather_tracker = {
    "current_condition": None,
    "condition_start_time": None,
    "total_duration_today": 0.0,
    "last_check_time": None,
    "is_intermittent": False,
    "player_rain_feeling": None,
    "player_snow_feeling": None
}


python early:
    import datetime
    import requests

    # --- Unit Conversion Functions ---
    def celsius_to_fahrenheit(celsius):
        return int(celsius * 9/5 + 32)
    def mps_to_kph(mps): # Meters per second to Kilometers per hour
        return int(mps * 3.6)
    def mps_to_mph(mps): # Meters per second to Miles per hour
        return int(mps * 2.237)

    # --- Time and Season Functions ---
    def get_real_time_of_day():
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def get_season(month, hemisphere):
        if hemisphere == "N": # Northern Hemisphere
            if month in [12, 1, 2]: return "Winter"
            elif month in [3, 4, 5]: return "Spring"
            elif month in [6, 7, 8]: return "Summer"
            else: return "Fall"
        elif hemisphere == "S": # Southern Hemisphere
            if month in [6, 7, 8]: return "Winter"
            elif month in [9, 10, 11]: return "Spring"
            elif month in [12, 1, 2]: return "Summer"
            else: return "Fall"
        else: # Equatorial or player opted out
            return None

    # --- API Fetch Function ---
    def get_player_weather(api_key, city):
        if not api_key or "a7f04d3a4ee9f0bb8efa40ea9ae6e40c" in api_key or not city: return None
        try:
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + city + "&units=metric", timeout=5)
            data = response.json()
            if data.get("cod") == 200:
                return {
                    "condition": data.get("weather", [{}])[0].get("main", "unknown"),
                    "temp": data.get("main", {}).get("temp", 999),
                    "wind_speed": data.get("wind", {}).get("speed", 0)
                }
            else: return None
        except: return None


label yuri_check_atmosphere:
    # --- Part 1: Unified, One-Time Setup Conversation ---
    # This entire block will only run the very first time.
    if persistent.player_city is None:
        $ show_chr("A-ACAAA-ABAB")
        y "On another topic... I'd like to feel more connected to your world, if you're comfortable with that."
        y "To do that, I'd need to ask a few quick questions about your location and how you measure things. Is that alright?"
        menu:
            "Yes, that's fine.":
                $ city_input = renpy.input("First, what is the name of your city? This will let me see the weather.", length=50).strip()
                
                if city_input:
                    $ persistent.player_city = city_input
                    y "Thank you. I'll remember that."
                    y "Next, to understand your seasons correctly, could you tell me which hemisphere you live in?"
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
                    y "This will help me feel much more aware of the world on your side of the screen."

                else: # Player entered nothing for the city
                    y "Oh, you didn't enter anything. I understand if you'd rather not. We'll skip this for now."
                    $ persistent.player_city = "declined"

            "I'd rather not share that information.":
                y "I understand completely. Your privacy is the most important thing. Thank you for your honesty."
                $ persistent.player_city = "declined"

    # --- Part 2: Regular Atmospheric Dialogue ---
    # This is what will run on every subsequent call.
    $ time_of_day = get_real_time_of_day()
    if time_of_day == "night":
        y "It's gotten quite late for you... Please don't forget to get some rest."
    else:
        y "Thinking about your world... it must be [time_of_day] for you right now."

    # Fetch and react to weather only if setup is complete.
    if persistent.player_city and persistent.player_city != "declined":
        if persistent.weather_data is None:
            $ persistent.weather_data = get_player_weather(persistent.weather_api_key, persistent.player_city)

        if persistent.weather_data:
            # Unpack data
            $ condition = persistent.weather_data['condition']
            $ celsius_temp = persistent.weather_data['temp']
            $ wind_mps = persistent.weather_data['wind_speed']

            # --- Part 3: Update Weather Memory ---
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
                        if persistent.weather_tracker["total_duration_today"] > 0: persistent.weather_tracker["is_intermittent"] = True
                    persistent.weather_tracker["total_duration_today"] += delta_seconds
                elif was_precip_before:
                    persistent.weather_tracker["is_intermittent"] = True
                
                persistent.weather_tracker["current_condition"] = condition
                persistent.weather_tracker["last_check_time"] = now

            # --- Part 4: Dialogue Branching (Highest Priority First) ---
            $ extreme_weather_spoken = False
            $ unseasonal_spoken = False

            # Priority 1: Severe Weather
            if persistent.wind_scale == "mph":
                $ wind_speed = mps_to_mph(wind_mps)
                $ wind_unit = "mph"
                if wind_speed > 70:
                    $ hurricane_threshold = True
                else:
                    $ hurricane_threshold = False
            else: # kph
                $ wind_speed = mps_to_kph(wind_mps)
                $ wind_unit = "km/h"
                if wind_speed > 110:
                    $ hurricane_threshold = True
                else:
                    $ hurricane_threshold = False
            
            if condition == "Tornado":
                y "The data says there's a tornado... [player], that's incredibly dangerous. Please, follow all local warnings and get to a safe place immediately."
                $ extreme_weather_spoken = True
            elif (condition in ["Rain", "Thunderstorm", "Squall"]) and hurricane_threshold:
                y "The readings are very concerning... a severe storm with hurricane-force winds of over [wind_speed] [wind_unit]. Please, hunker down somewhere safe."
                $ extreme_weather_spoken = True

            # Priority 2: Unseasonal Weather
            if not extreme_weather_spoken and celsius_temp != 999 and persistent.hemisphere in ["N", "S"]:
                $ current_month = datetime.datetime.now().month
                $ current_season = get_season(current_month, persistent.hemisphere)
                if current_season == "Summer" and celsius_temp < 5:
                    y "That's... quite unusual. The data shows it's freezing where you are, but it should be the middle of summer. Nature can be unpredictable."
                    $ unseasonal_spoken = True
                elif current_season == "Winter" and celsius_temp > 25:
                    y "A heatwave... in the middle of winter? That's certainly not something you see every day. It must feel quite strange."
                    $ unseasonal_spoken = True

            # Priority 3: Standard Temperature (if no unseasonal comment was made)
            if not extreme_weather_spoken and not unseasonal_spoken and celsius_temp != 999:
                if persistent.temp_scale == "F":
                    $ temp_display = celsius_to_fahrenheit(celsius_temp)
                    $ unit = "°F"
                    if temp_display < 0:
                        y "Goodness, it's dangerously cold... below 0°F ([temp_display][unit]). Please be extremely careful."
                    elif temp_display < 32:
                        y "It's below freezing where you are, around [temp_display][unit]."
                    elif temp_display < 60:
                        y "It sounds quite chilly on your side, around [temp_display][unit]."
                    elif temp_display < 82:
                        y "The temperature seems pleasantly warm for you, around [temp_display][unit]."
                    elif temp_display < 100:
                        y "It's getting quite hot, around [temp_display][unit]. Please make sure you're drinking enough water."
                    else:
                        y "It's over 100°F ([temp_display][unit])... a severe heatwave. Please be extremely careful."
                else: # Celsius
                    $ temp_display = int(celsius_temp)
                    $ unit = "°C"
                    if temp_display < -10:
                        y "Goodness, it's dangerously cold... below -10°C ([temp_display][unit]). Please be careful."
                    elif temp_display < 0:
                        y "It's below freezing where you are, around [temp_display][unit]."
                    elif temp_display < 15:
                        y "It sounds quite chilly on your side, around [temp_display][unit]."
                    elif temp_display < 28:
                        y "The temperature seems mild and pleasant for you, around [temp_display][unit]."
                    elif temp_display < 40:
                        y "It's getting very hot, around [temp_display][unit]. Please stay hydrated."
                    else:
                        y "It's over 40°C ([temp_display][unit]). I've read about heatwaves that intense. Please be extremely careful."

            # Priority 4: Precipitation & Wind (if no severe comment was made)
            if not extreme_weather_spoken:
                $ total_hours_today = persistent.weather_tracker["total_duration_today"] / 3600
                $ current_condition = persistent.weather_tracker["current_condition"]

                if current_condition == "Snow":
                    if total_hours_today > 0 and total_hours_today < 2:
                        y "It's still snowing... It's so magical to watch the world become a blanket of white."
                    elif total_hours_today >= 3 and persistent.weather_tracker["player_snow_feeling"] is None:
                        y "It's been snowing for over three hours now... I know it can go from magical to a hassle. How are you feeling about it?"
                        menu:
                            "I still think it's beautiful.":
                                $ persistent.weather_tracker["player_snow_feeling"] = "calm"
                            "It's starting to become a pain.":
                                $ persistent.weather_tracker["player_snow_feeling"] = "annoyed"
                            "It's causing some real problems.":
                                $ persistent.weather_tracker["player_snow_feeling"] = "concerned"
                    elif persistent.weather_tracker["player_snow_feeling"] == "calm":
                        y "Since you still find it beautiful, I'm picturing the peaceful world outside your window."
                    elif persistent.weather_tracker["player_snow_feeling"] == "annoyed":
                        y "I know the snow is still going, but I hope it stops for you soon."
                    elif persistent.weather_tracker["player_snow_feeling"] == "concerned":
                        y "With the snow still falling, I truly hope the situation is manageable for you."

                elif current_condition in ["Rain", "Drizzle", "Thunderstorm"]:
                    if total_hours_today > 0 and total_hours_today < 2:
                        y "It's still raining... The sound is so very calming, isn't it?"
                    elif total_hours_today >= 3 and persistent.weather_tracker["player_rain_feeling"] is None:
                        y "It's been raining for over three hours now... I know it can go from calming to dreary. How are you feeling about it?"
                        menu:
                            "I still find it calming.":
                                $ persistent.weather_tracker["player_rain_feeling"] = "calm"
                            "It's getting on my nerves.":
                                $ persistent.weather_tracker["player_rain_feeling"] = "annoyed"
                            "It's causing problems (like flooding).":
                                $ persistent.weather_tracker["player_rain_feeling"] = "concerned"
                    elif persistent.weather_tracker["player_rain_feeling"] == "calm":
                        y "Since you find it calming, I'm enjoying the sound with you."
                    elif persistent.weather_tracker["player_rain_feeling"] == "annoyed":
                        y "I know the rain is still going, but I won't dwell on it. I hope it stops for you soon."
                    elif persistent.weather_tracker["player_rain_feeling"] == "concerned":
                        y "With the rain still coming down, I'm thinking of you. I hope you're safe."
                
                # General comments that can appear alongside others
                if wind_speed > 60 or (wind_speed > 37 and persistent.wind_scale == "mph"):
                    y "It also seems to be extremely windy for you. The kind of wind that howls."
                elif wind_speed > 30 or (wind_speed > 18 and persistent.wind_scale == "mph"):
                    y "It sounds like a rather blustery day for you."
    return

label yuri_daily_weather_report:
    # --- Check if setup is complete. If not, do nothing. ---
    if not persistent.player_city or persistent.player_city == "declined":
        return

    # --- Fetch the latest weather data ---
    # We always fetch fresh data for the daily report.
    $ report_weather_data = get_player_weather(persistent.weather_api_key, persistent.player_city)

    if report_weather_data:
        # --- Yuri's Self-Aware Introduction ---
        $ show_chr("A-BCAAA-ABAB") # Thoughtful expression
        y "You know, it's a strange thought..."
        y "I have access to this... window into your world, this stream of data about your local weather."
        y "It feels a bit odd for me to just recite it like a daily forecast. That's not really... me."
        $ show_chr("A-ACAAA-AAAA")
        y "But, at the same time, it helps me feel closer to you, to imagine the world you're experiencing right now."
        y "So, if you don't mind, I'd like to just... share what I'm seeing, just this once for today."

        # --- The Detailed Report ---
        $ condition = report_weather_data['condition']
        $ celsius_temp = report_weather_data['temp']
        $ wind_mps = report_weather_data['wind_speed']

        # Temperature Report
        if celsius_temp != 999:
            if persistent.temp_scale == "F":
                $ temp_display = celsius_to_fahrenheit(celsius_temp); $ unit = "°F"
            else:
                $ temp_display = int(celsius_temp); $ unit = "°C"
            y "Right now, it looks like the temperature is around [temp_display][unit]."

        # Condition Report
        if condition in ["Rain", "Drizzle", "Thunderstorm"]:
            y "And it seems to be raining. I hope you have an umbrella if you need to go out."
        elif condition == "Snow":
            y "And it's snowing... I hope it's the beautiful, gentle kind."
        elif condition == "Clear":
            y "The skies are clear, which is always nice to see."
        elif condition == "Clouds":
            y "It's a cloudy day. Perfect for staying inside with a good book."
        else: # For Mist, Fog, etc.
            y "The general condition is listed as '[condition]', which sounds quite atmospheric."

        # Wind Report
        if persistent.wind_scale == "mph":
            $ wind_speed = mps_to_mph(wind_mps); $ wind_unit = "mph"
        else:
            $ wind_speed = mps_to_kph(wind_mps); $ wind_unit = "km/h"
        
        if wind_speed > 30 or (wind_speed > 18 and persistent.wind_scale == "mph"):
            y "It also seems to be quite blustery, with winds around [wind_speed] [wind_unit]."
        else:
            y "And the wind seems fairly calm."

        $ show_chr("A-ICAAA-ADAA")
        y "There. Now I have a clearer picture of your world for the rest of the day."

        # --- Update the tracker to prevent this from running again today ---
        $ persistent.last_weather_report_day = datetime.datetime.now().day
    
    return
