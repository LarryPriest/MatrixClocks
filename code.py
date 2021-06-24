'''code.py
June 20, 2021 - Larry Priest
priestlt@protonmail.com
Starter for a multi clock on Matrix Portal.  Will eventually loop through the
various clock and billboard screens. The plan is to start by class-ifing the
original samples and then having each run through a short internal loop then
loop to the next one.
'''
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from ScrollingClock import myclock
from QuoteBoard import QuoteBoard

print('Hello World!')
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
# Set the time to local time
matrixportal.get_local_time()
matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
        scrolling=True,)
my_time = myclock(matrixportal)
quoteboard = QuoteBoard(matrixportal)

while True:
    my_time.displayClock()
    quoteboard.ScrollQuote()
    
    
import MoonClock