from constants import *
from PIL import Image, ImageDraw
from LCD_1in44 import LCD

class Player:
    def __init__(self, draw: ImageDraw.ImageDraw, display: LCD, image: Image):
        self.dir = [0, 1]
        self.body = [(18, 18)]
        
        self.draw = draw
        self.display = display
        self.image = image

    def does_coord_have_body(self, x, y):
        for segment in self.body:
            if (segment[0] == x and segment[1] == y):
                return True

    def set_left(self):
        self.dir = [-1, 0]
    
    def set_right(self):
        self.dir = [1, 0]

    def set_up(self):
        self.dir = [0, -1]

    def set_down(self):
        self.dir = [0, 1]

    def show(self):
        for segment in self.body:
            self.draw.rectangle(
                (
                    segment[0] - (HALF_SCALE),
                    segment[1] - (HALF_SCALE),
                    segment[0] + (HALF_SCALE) - 1,
                    segment[1] + (HALF_SCALE) - 1,
                ),
                outline=0xffff00,
                fill=0xffff00
            )

        self.display.LCD_ShowImage(self.image, 0, 0)

    def move(self, did_grow=False):
        print(self.dir)
        
        # ------------------------------ Add new head :0 ----------------------------- #
        current_x = self.body[0][0]
        current_y = self.body[0][1]
        dir_x = self.dir[0]
        dir_y = self.dir[1]

        print(current_x, current_y)

        new_head = (
            (current_x + (dir_x * SCALE)),
            (current_y + (dir_y * SCALE))
        )

        self.body.insert(0, new_head)

        # ------------------------------- Draw new head ------------------------------ #
        
        self.draw.rectangle(
            (
                new_head[0] - (HALF_SCALE),
                new_head[1] - (HALF_SCALE),
                new_head[0] + (HALF_SCALE) - 1,
                new_head[1] + (HALF_SCALE) - 1,
            ),
            outline=0xffff00,
            fill=0xffff00
        )

        # --------------------------------- Cut tail? -------------------------------- #

        if did_grow == False:
            self.draw.rectangle(
                (
                    self.body[-1][0] - (HALF_SCALE),
                    self.body[-1][1] - (HALF_SCALE),
                    self.body[-1][0] + (HALF_SCALE) - 1,
                    self.body[-1][1] + (HALF_SCALE) - 1,
                ),
                outline=0x0,
                fill=0x0
            )

            self.body.pop()

        # ------------------------- Instantly update display ------------------------- #

        self.display.LCD_ShowImage(self.image, 0, 0)

    def handle_collision(self, collision_type):
        if (collision_type == 1):
            # Game over
            return
        
        if (collision_type == 2):
            # Grow a bit
            self.move(did_grow=True)

        if (collision_type == 0):
            # Do not grow
            self.move(did_grow=False)
