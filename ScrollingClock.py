import time
import random
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

colors = []
# colors.append(0x000000)  # black background
colors.append(0xFF0000)  # red
colors.append(0xCC4000)  # amber
colors.append(0x85FF00)  # greenish

SCROLL_SPEED = 0.025  # lower is faster, delay between refreshes


class myclock():
    def __init__(self, portal):
        self.last_color = 1
        # --- Display setup ---
        self.matrixportal = portal
       

    def my_time(self):
        colon = ':'
        time_data = time.localtime()
        is_dst = time_data[8]
        year = time_data[0]
        month = time_data[1]
        day = time_data[2]
        hour = time_data[3]
        minute = time_data[4]
        second = time_data[5]
        hourtext =  '{}{}{:02d}{}{:02d} - {:02d}{}{:02d}{}{:02d} '.format(
            year, colon, month, colon, day, hour, colon, minute, colon, second)
        return hourtext      

    def displayClock(self):
        timeStr = self.my_time()
        # Set the text
        self.matrixportal.set_text(timeStr)
        # Set the text color
        color_index = 0
        # Choose a random color from colors
        if len(colors) > 1 and self.last_color is not None:
            while color_index == self.last_color:
                color_index = random.randrange(0, len(colors))
        else:
            color_index = random.randrange(0, len(colors))
        self.last_color = color_index
        self.matrixportal.set_text_color(colors[color_index])
        # Scroll it
        self.matrixportal.scroll_text(SCROLL_SPEED)
        
if __name__ == '__main__':
    matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
    matrixportal.get_local_time()
     # Create a new label with the color and text selected
    matrixportal.add_text(
            text_font=terminalio.FONT,
            text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
            scrolling=True,)
    # Set the time to local time
    my_time = myclock(matrixportal)
    
    while True:
        my_time.displayClock()
