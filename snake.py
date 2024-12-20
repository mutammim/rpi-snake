# -*- coding:utf-8 -*-
import time
import LCD_1in44

from PIL import Image, ImageDraw, ImageFont, ImageColor
from Game import Game

display = LCD_1in44.LCD()
scan_direction = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
display.LCD_Init(scan_direction)
display.LCD_Clear()

image = Image.new('RGB', (display.width, display.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
display.LCD_ShowImage(image, 0, 0)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 6)

    title = "Snake"
    subtitle = "Press up to start..."

    draw.rectangle((0, 0, display.width, display.height), outline=0, fill="gray")
    draw.text((72, 60), title, font=title_font, fill="white", anchor="mm")
    draw.text((72, 78), subtitle, font=subtitle_font, fill="white", anchor="mm")
    display.LCD_ShowImage(image, 0, 0)

    waiting = True
    while waiting:
        if (display.digital_read(display.GPIO_KEY_UP_PIN)) != 0:
            waiting = False

except Exception as e:
    print(f"An error occurred: {e}")

try:
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    game = Game(draw, display, image)
    game.player.show()
    game.food.generate_food(3, game.player.body)

    last_move_time = time.time()
    move_interval = 0.15 + (0.025 * game.score)

    while not game.over:
        if display.digital_read(display.GPIO_KEY_UP_PIN) != 0:
            if game.player.dir == [-1, 0] or game.player.dir == [1, 0]:
                game.player.set_up()

        if display.digital_read(display.GPIO_KEY_DOWN_PIN) != 0:
            if game.player.dir == [-1, 0] or game.player.dir == [1, 0]:
                game.player.set_down()
        
        if display.digital_read(display.GPIO_KEY_LEFT_PIN) != 0:
            if game.player.dir == [0, -1] or game.player.dir == [0, 1]:        
                game.player.set_left()

        if display.digital_read(display.GPIO_KEY_RIGHT_PIN) != 0:
            if game.player.dir == [0, -1] or game.player.dir == [0, 1]:
                game.player.set_right()

        # -------------------------------- Move snake -------------------------------- #

        current_time = time.time()
        if current_time - last_move_time >= move_interval:
            game.iterate()
            last_move_time = current_time

        # ------------------------------ Show new image ------------------------------ #

        display.LCD_ShowImage(image, 0, 0)
        time.sleep(0.005)

    # --------------------------------- Game over -------------------------------- #

    while True:
        draw.rectangle((0, 0, display.width, display.height), outline=0, fill="gray")
        draw.text((72, 60), "Game over!", font=title_font, fill="white", anchor="mm")
        draw.text((72, 78), str(game.score), font=subtitle_font, fill="white", anchor="mm")
        display.LCD_ShowImage(image, 0, 0)

except Exception as e:
    print(f"An error occurred: {e}")

display.module_exit()
