# -*- coding:utf-8 -*-
import time
import LCD_1in44

from PIL import Image, ImageDraw, ImageFont, ImageColor

display = LCD_1in44.LCD()
scan_direction = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
display.LCD_Init(scan_direction)
display.LCD_Clear()

image = Image.new('RGB', (display.width, display.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
display.LCD_ShowImage(image, 0, 0)

# ---------------------------------------------------------------------------- #
#                                 Game function                                #
# ---------------------------------------------------------------------------- #

SCALE = 4 # Even numbers only
HALF_SCALE = int(SCALE / 2)

def get_coord_status(x, y):
    for x in range(
        HALF_SCALE,
        display.width - HALF_SCALE,
        SCALE
    ):
        for y in range(
            HALF_SCALE,
            display.height - HALF_SCALE,
            SCALE
        ):
            if player.is_coord_in_body(x, y) == True:
                return 1
            elif food.does_coord_have_food(x, y) == True:
                return 2
            else:
                return 0

class Player:
    def __init__(self):
        self.dir = [0, 1]
        self.body = [(72, 72)]

    def is_coord_in_body(self, x, y):
        for segment in self.body:
            if (segment[0] == x and segment[1] == y):
                return True

    def check_coord(x, y):
        # TODO
        # Do "Game Over" if you eat your tail
        # Remove the food & grow the snake if you eat food
        # Check the coordinate before at the beginning of move()
        # Maybe break up other parts of move()?
        # Create a way for the game to start with 3 pieces of food
        # Make a new piece of food generate every time a piece is eaten

        status = get_coord_status(x, y)

        if (status == 1):
            return
            # TODO — You ate your tail!
        
        if (status == 2):
            return
            # TODO — You should grow!

        # Check what you collided with
        # Where would we find these coordinates?
        # Coordinates of snake segments & coordinates of food
        return

    def set_left(self):
        self.dir = [-1, 0]
    
    def set_right(self):
        self.dir = [1, 0]

    def set_up(self):
        self.dir = [0, -1]

    def set_down(self):
        self.dir = [0, 1]

    def move(self, did_grow=False):
        # Add new head based on desired direction
        current_x = self.body[0][0]
        current_y = self.body[0][1]
        dir_x = self.dir[0]
        dir_y = self.dir[1]

        new_head = (
            (current_x + (dir_x * SCALE)),
            (current_y + (dir_y * SCALE))
        )

        self.body.insert(0, new_head)

        # Draw the head

        draw.rectangle(
            (
                new_head[0] - (HALF_SCALE),
                new_head[1] - (HALF_SCALE),
                new_head[0] + (HALF_SCALE),
                new_head[1] + (HALF_SCALE),
            ),
            outline=255,
            fill=0xff00
        )

        if did_grow == False:
            draw.rectangle(
                (
                    self.body[len(self.body) - 1][0] - (HALF_SCALE),
                    self.body[len(self.body) - 1][1] - (HALF_SCALE),
                    self.body[len(self.body) - 1][0] + (HALF_SCALE),
                    self.body[len(self.body) - 1][1] + (HALF_SCALE),
                ),
                outline=0,
                fill=0
            )

            self.body.pop()

        # Show the action

        display.LCD_ShowImage(image, 0, 0)

class Food:
    # Coordinates of the food
    # Function to find a random location for food that is not snake
    # Function to randomly add food

    def __init__(self):
        return

    def does_coord_have_food(self, x, y):
        return
        # for segment in self.body:
        #     if (segment[0] == x and segment[1] == y):
        #         return True

player = Player()
food = Food()

# ---------------------------------------------------------------------------- #
#                                   Game loop                                  #
# ---------------------------------------------------------------------------- #

try:
    last_move_time = time.time()
    move_interval = 1
    # TODO: Show player at beginning, before move

    while True:
        if display.digital_read(display.GPIO_KEY_UP_PIN) != 0:
            player.set_up()

        if display.digital_read(display.GPIO_KEY_DOWN_PIN) != 0:
            player.set_down()
        
        if display.digital_read(display.GPIO_KEY_LEFT_PIN) != 0:
            player.set_left()

        if display.digital_read(display.GPIO_KEY_RIGHT_PIN) != 0:
            player.set_right()

        # -------------------------------- Move snake -------------------------------- #

        current_time = time.time()
        if current_time - last_move_time >= move_interval:
            player.move()
            last_move_time = current_time

        # ------------------------------ Show new image ------------------------------ #

        display.LCD_ShowImage(image, 0, 0)
        time.sleep(0.01)

except Exception as e:
    print(f"An error occurred: {e}")

display.module_exit()
