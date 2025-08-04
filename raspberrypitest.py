#!/usr/bin/env python3
import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from rss_parser import RSSParser
from requests import get  # noqa


#01 rss functionality
rss_url = "https://www.dr.dk/nyheder/service/feeds/senestenyt"
response = get(rss_url)

rss = RSSParser.parse(response.text)

# Print out rss meta data
print("Language", rss.channel.language)
print("RSS", rss.version)



#03 I2C and OLED setup
# I2C-opsætning
i2c = busio.I2C(board.SCL, board.SDA)

# OLED-skærm (SSD1306) 128×64
WIDTH = 128
HEIGHT = 64
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Ryd skærm
display.fill(0)
display.show()

# Lav et Pillow-billede til at tegne på
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Vælg font (indbygget)
font = ImageFont.load_default()

#02 display_text function
def display_text(text, x=0, y=0, font=font, duration=2):
    """
    Display text on the OLED screen at the specified position.

    Args:
        text (str): The text to display.
        x (int): X-coordinate for the text (default 0).
        y (int): Y-coordinate for the text (default 0).
        font (ImageFont): Font to use (default is global font).
        duration (float): Time in seconds to display the text (default 2).
    """
    # Clear the image
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    # Draw the text
    draw.text((x, y), text, font=font, fill=255)
    # Display the image
    display.image(image)
    display.show()
    # Wait for the specified duration
    time.sleep(duration)

latest_heading = rss.channel.items[0].title
display_text(latest_heading)