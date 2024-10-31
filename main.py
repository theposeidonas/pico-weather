import time
from datetime import set_rtc, get_time
from wifi import connect_wifi
from weather import get_weather
from machine import Pin, SoftI2C
from pico_i2c_lcd import I2cLcd

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def format_date(date_str):
    year, month, day = date_str.split('-')
    return f"{day}/{month}/{year}"

def load_weather_characters(lcd, weather_character):
    lcd.custom_char(0, weather_character)
    
def main():
    connect_wifi()
    set_rtc()
    previous_hour = None
    weather_data = None
    lcd.backlight_off()
    
    while True:
        current_time = get_time()
        current_hour_minute = current_time.split()[1][:5]
        current_hour = current_time.split()[1][:2]
        
        if current_hour != previous_hour:
            previous_hour = current_hour
            weather_data = get_weather(current_hour)
            load_weather_characters(lcd, weather_data[0])
        
        lcd.clear()
        
        date_temp = f"{format_date(current_time.split()[0])} {weather_data[1]}C"
        lcd.putstr(date_temp[:16])
        
        lcd.move_to(0, 1)
        lcd.putstr(f"{current_hour_minute} ")
        lcd.putchar(chr(0))
        weather_str = f"      %{weather_data[2]}"
        lcd.putstr(weather_str[:15 - len(current_hour_minute) - 2])
        time.sleep(60)

if __name__ == "__main__":
    main()
