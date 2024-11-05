from Player import Player
from Food import Food
from constants import *

class Game:
    def __init__(self, draw, display, image):
        self.score = 0
        self.player = Player(draw, display, image)
        self.food = Food(draw, display, image)

    def get_coord_status(self, x, y):
        for x in range(
            HALF_SCALE,
            DISPLAY_WIDTH + HALF_SCALE, # Not minus, or it'd stop at 122, 122
            SCALE
        ):
            for y in range(
                HALF_SCALE,
                DISPLAY_HEIGHT + HALF_SCALE, # Not minus for reasons above
                SCALE
            ):
                if self.player.does_coord_have_body(x, y) == True:
                    return 1
                elif self.food.does_coord_have_food(x, y) == True:
                    return 2
                else:
                    return 0

    def send_collision_status(self):
        print("sending...")
        
        collision_type = self.get_coord_status(self.player.body[0][0], self.player.body[0][1])
        self.player.handle_collision(collision_type)
