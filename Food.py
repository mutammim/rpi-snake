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

    def generate_food(self, quantity):
        for _ in range(quantity):
            self.locations.append((
                self.get_nearest_valid_coord(random.randint(0, DISPLAY_WIDTH)),
                self.get_nearest_valid_coord(random.randint(0, DISPLAY_HEIGHT))
            ))

            self.draw.rectangle(
                (
                    self.locations[-1][0] - HALF_SCALE,
                    self.locations[-1][1] - HALF_SCALE,
                    self.locations[-1][0] + HALF_SCALE,
                    self.locations[-1][1] + HALF_SCALE,
                ),
                fill=0xff00ff,
                outline=0xff00ff,
                width=HALF_SCALE,
            )

    def add_food(self, x, y):
        self.locations.append((x, y))
