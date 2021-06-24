# Quote board matrix display
# uses AdafruitIO to serve up a quote text feed and color feed
# random quotes are displayed, updates periodically to look for new quotes
# avoids repeating the same quote twice in a row

import time
import random
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
import gc

class QuoteBoard():
    def __init__(self, portal):
        self.matrixportal = portal
        self.QUOTES_FEED = "sign-quotes.signtext"
        self.COLORS_FEED = "sign-quotes.signcolor"
        self.SCROLL_DELAY = 0.02
        self.UPDATE_DELAY = 600

        self.quotes = []
        self.colors = []
        self.last_color = None
        self.last_quote = None
        self.last_update = time.monotonic()
        self.updated = False


    def update_data(self):
        print("Updating data from Adafruit IO")
        try:
            self.quotes_data = self.matrixportal.get_io_data(self.QUOTES_FEED)
            self.quotes.clear()
            for json_data in self.quotes_data:
                self.quotes.append(self.matrixportal.network.json_traverse(json_data, ["value"]))
        except Exception as error:
            print(error)

        try:
            self.color_data = self.matrixportal.get_io_data(self.COLORS_FEED)
            self.colors.clear()
            for json_data in self.color_data:
                self.colors.append(self.matrixportal.network.json_traverse(json_data, ["value"]))
        except Exception as error:
            print(error)

        if not self.quotes or not self.colors:
            raise RuntimeError("Please add at least one quote and color to your feeds")
            self.matrixportal.set_text(" ", 1)
        else:
            self.updated = True
        self.last_update = time.monotonic()

    def PickQuote(self):
        # Choose a random quote from quotes
        if len(self.quotes) > 1 and self.last_quote is not None:
            while self.quote_index == self.last_quote:
                self.quote_index = random.randrange(0, len(self.quotes))
        else:
            self.quote_index = random.randrange(0, len(self.quotes))
        self.last_quote = self.quote_index
        text = self.quotes[self.quote_index]

        # Choose a random color from colors
        if len(self.colors) > 1 and self.last_color is not None:
            while self.color_index == self.last_color:
                self.color_index = random.randrange(0, len(self.colors))
        else:
            self.color_index = random.randrange(0, len(self.colors))
        self.last_color = self.color_index
        color = self.colors[self.color_index]
        if time.monotonic() > self.last_update + self.UPDATE_DELAY:
            self.update_data()
            self.last_update = time.monotonic()
        gc.collect()
        return text, color

    def ScrollQuote(self):
        if not self.updated:
            self.update_data()
        text, color = self.PickQuote()        
        # Set the quote text
        self.matrixportal.set_text(text)
        # Set the text color
        self.matrixportal.set_text_color(color)
        # Scroll it
        self.matrixportal.scroll_text(self.SCROLL_DELAY)

        

if __name__ == '__main__':
    # --- Display setup ---
    matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
    matrixportal.get_local_time()
     # Create a new label with the color and text selected
    matrixportal.add_text(
            text_font=terminalio.FONT,
            text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
            scrolling=True,
        )
    QB = QuoteBoard(matrixportal)
#     QB.update_data()
    while True:
        QB.ScrollQuote()