import urequests

LATITUDE = 10.1010
LONGITUDE = 10.1010

def get_weather(hour):
    url = f"http://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,weathercode,precipitation_probability"
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            return parse_weather_data(data, hour)
        else:
            return [["API hatası"], 0, 0]
    except:
        return [["Bağlantı hatası"], 0, 0]

def parse_weather_data(data, hour):
    hourly = data['hourly']
    times = hourly['time']
    temperatures = hourly['temperature_2m']
    weather_codes = hourly['weathercode']
    precipitation_probabilities = hourly['precipitation_probability']
    for i, time_str in enumerate(times):
        if time_str[11:13] == hour:
            temperature = temperatures[i]
            weather_code = weather_codes[i]
            precipitation_probability = precipitation_probabilities[i]
            weather_description = interpret_weather_code(weather_code)
            return [weather_description, temperature, precipitation_probability]
    return [["Veri bulunamadı"], 0, 0]

def interpret_weather_code(code):
    weather_dict = {
        0: [0b01010, 0b00100, 0b11111, 0b00100, 0b01010, 0b00000, 0b00000, 0b00000],
        1: [0b01010, 0b00100, 0b01110, 0b00100, 0b01010, 0b00000, 0b00000, 0b00000],
        2: [0b00000, 0b01110, 0b10101, 0b11111, 0b00100, 0b00000, 0b00000, 0b00000],
        3: [0b00000, 0b01110, 0b10101, 0b11111, 0b01110, 0b00000, 0b00000, 0b00000],
        45: [0b01110, 0b00000, 0b11111, 0b01010, 0b11111, 0b00000, 0b01110, 0b00000],
        48: [0b01110, 0b00000, 0b11111, 0b01010, 0b11111, 0b00000, 0b10101, 0b00000],
        51: [0b00100, 0b00000, 0b11111, 0b10101, 0b00000, 0b00100, 0b00000, 0b00000],
        53: [0b00100, 0b00000, 0b11111, 0b10101, 0b00000, 0b00100, 0b00100, 0b00000],
        55: [0b00100, 0b00000, 0b11111, 0b10101, 0b00000, 0b00100, 0b00100, 0b00100],
        61: [0b00000, 0b00100, 0b01110, 0b11111, 0b00100, 0b01010, 0b00000, 0b00000],
        63: [0b00000, 0b00100, 0b01110, 0b11111, 0b00100, 0b01010, 0b00100, 0b00000],
        65: [0b00000, 0b00100, 0b01110, 0b11111, 0b00100, 0b01010, 0b00100, 0b00100],
        71: [0b00100, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0b00100, 0b00000],
        73: [0b00100, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0b00100, 0b00100],
        75: [0b00100, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0b00100, 0b10101],
        80: [0b00000, 0b01010, 0b00000, 0b11111, 0b00100, 0b01010, 0b00000, 0b00000],
        81: [0b00000, 0b01010, 0b00000, 0b11111, 0b00100, 0b01010, 0b00100, 0b00000],
        82: [0b00000, 0b01010, 0b00000, 0b11111, 0b00100, 0b01010, 0b00100, 0b01010]
    }
    return weather_dict.get(code, [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b00100, 0b00000, 0b00100])