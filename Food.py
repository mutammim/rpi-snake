from constants import *
from PIL import Image, ImageDraw
from LCD_1in44 import LCD
import random

class Food:
    def __init__(self, draw: ImageDraw.ImageDraw, display: LCD, image: Image):
        self.locations = []

        self.draw = draw
        self.display = display
        self.image = image

    def does_coord_have_food(self, x, y):
        for location in self.locations:
            if location == (x, y):
                return True

    def get_nearest_valid_coord(self, value):
        valid_coords = range(HALF_SCALE, DISPLAY_WIDTH + HALF_SCALE, SCALE)
        return min(valid_coords, key=lambda x: abs(x - value))

    def generate_food(self, quantity, blocked_coords):
        for _ in range(quantity):
            location_is_valid = False

            while location_is_valid == False:
                new_location = (
                    self.get_nearest_valid_coord(random.randint(0, DISPLAY_WIDTH)),
                    self.get_nearest_valid_coord(random.randint(0, DISPLAY_HEIGHT))
                )

                if new_location not in blocked_coords:
                    location_is_valid = True

            self.locations.append(new_location)
            self.draw.rectangle(
                (
                    self.locations[-1][0] - HALF_SCALE,
                    self.locations[-1][1] - HALF_SCALE,
                    self.locations[-1][0] + HALF_SCALE - 1,
                    self.locations[-1][1] + HALF_SCALE - 1,
                ),
                fill=0xff00ff,
                outline=0xff00ff,
                width=HALF_SCALE,
            )

    def add_food(self, x, y):
        self.locations.append((x, y))
