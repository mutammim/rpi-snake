from Player import Player
from Food import Food
from constants import *

class Game:
    def __init__(self, draw, display, image):
        self.score = 0
        self.player = Player(draw, display, image)
        self.food = Food(draw, display, image)
        self.over = False

    def get_coord_status(self, x, y):
        if self.player.does_coord_have_body(x, y) == True:
            print("have body")
            return 1
        elif self.food.does_coord_have_food(x, y) == True:
            print("have food")
            return 2
        else:
            return 0

    def iterate(self):
        next_position = self.player.get_next_position()
        collision_type = self.get_coord_status(next_position[0], next_position[1])
        
        if collision_type == 1:
            self.over = True

        if collision_type == 0 or collision_type == 2:
            self.player.process_movement(collision_type)

        if collision_type == 2:
            self.score += 1
            print(self.score)

            self.food.remove_food(next_position[0], next_position[1])
            # TODO: This is after the player moves, so it should be OK to generate there?
            self.food.generate_food(1, self.player.body)
