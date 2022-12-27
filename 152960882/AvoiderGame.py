import pygame
import sys
import random

# Starter code for an adventure game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors:
# Duke Nguyen (u1445624)
# My Dinh Ly (u1417560)

# All images are credited to Canva Image Stock.


def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one mask contacts the other.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap is not None


def main():

    # Initialize pygame
    pygame.init()

    message_screen = pygame.image.load("_Resources/StartScreen/StartScreen.png")
    # Store window width and height in different forms for easy access
    message_screen_size = message_screen.get_size()
    message_screen_rect = message_screen.get_rect()

    # Create the window based on the map size
    screen = pygame.display.set_mode(message_screen_size)

    # Create the Start button
    start_button = pygame.image.load("_Resources/StartScreen/StartButton.png")
    start_button_rect = start_button.get_rect()
    start_button_rect.center = (640, 340)
    start_button_mask = pygame.mask.from_surface(start_button)

    # Create the player data
    player = pygame.image.load("_Resources/cursor-close.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (60, 60))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create the fish
    fish = pygame.image.load("_Resources/blue_fish.png").convert_alpha()
    fish = pygame.transform.smoothscale(fish, (48, 31))
    fish_rect = fish.get_rect()
    fish_mask = pygame.mask.from_surface(fish)

    # Create the door
    door = pygame.image.load("_Resources/door.png").convert_alpha()
    door_rect = door.get_rect()
    door_mask = pygame.mask.from_surface(door)

    # Create the key
    key = pygame.image.load("_Resources/key.png").convert_alpha()
    key_rect = key.get_rect()
    key_mask = pygame.mask.from_surface(key)

    # Create the Level 1 map
    current_map = pygame.image.load("_Resources/Level1/map.png").convert_alpha()
    current_map.set_colorkey((255, 255, 255))
    current_map_rect = current_map.get_rect()
    current_map_mask = pygame.mask.from_surface(current_map)

    # Create the game over message:
    game_over = pygame.image.load("_Resources/game_over.png")
    game_over_rect = game_over.get_rect()

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Create variables to make changes throughout the game
    app_running = True      # The app_running variable records if the quit button is clicked or not.
    is_playing = False      # The is_playing variable records if the player starts a level.
    fish_found = False      # The fish_found variable records if a fish has been eaten by the player.
    is_alive = True         # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.).
    key_found = False       # The key_found variable records if a key is collided by the player.
    door_unlocked = False   # The door_unlocked variable records if the door is disappeared when the key is found.
    pop_up_open = False     # The pop_up_open variable records if a pop-up message is displayed.
    full = False            # The full variable records if the progress bar reaches 100%.

    # Create a list of fish appeared in the Level 3
    fish_list = []
    # Create an initial score before starting Level 3
    progress = 20

    # Level number
    level = 0

    # Get a font for displaying
    my_font = pygame.font.SysFont('arial', 24)

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop.
    while app_running:
        # Check if a mouse is clicked
        mouse_click = False

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:             # When the user clicks the [X] button
                app_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # When there is a right-click
                mouse_click = True

        # Draw the starting screen
        screen.fill((255, 255, 255))                  # Draw the color background
        screen.blit(current_map, current_map_rect)    # Draw the map background

        # Draw the message pop-up box before a level is played
        if not is_playing:
            screen.blit(message_screen, message_screen_rect)    # Draw the pop-up message box
            if is_alive and not level == 3:
                screen.blit(start_button, start_button_rect)    # Draw the START button

        # Draw the game over message if the player is disqualified
        if not is_alive:
            screen.fill((255, 255, 255))
            screen.blit(current_map, current_map_rect)
            screen.blit(game_over, game_over_rect)

        # Draw the cursor
        player_rect.center = pygame.mouse.get_pos()
        screen.blit(player, player_rect)

        # Check if we touch and click the start button
        if pixel_collision(player_mask, player_rect, start_button_mask, start_button_rect) and mouse_click is True:
            if level == 0:
                message_screen = pygame.image.load("_Resources/Level1/message.png")
                message_screen_rect = message_screen.get_rect()
                start_button_rect.center = (620, 550)

                if pixel_collision(player_mask, player_rect, start_button_mask, start_button_rect) and mouse_click is True:
                    level += 1

        # Level 1 starting
        if level == 1:
            is_playing = True
            if is_alive:
                if not fish_found:
                    screen.blit(fish, fish_rect)
                    fish_rect.center = (1200, 100)
                    if pixel_collision(player_mask, player_rect, fish_mask, fish_rect):
                        fish_found = True

                if pixel_collision(player_mask, player_rect, current_map_mask, current_map_rect) and is_playing and not fish_found:
                    is_playing = False
                    is_alive = False
                    level = -1

                if fish_found:
                    is_playing = False

                    message_screen = pygame.image.load("_Resources/Level2/message.png")
                    message_screen_rect = message_screen.get_rect()
                    start_button_rect.center = (620, 550)

                    if pixel_collision(player_mask, player_rect, start_button_mask, start_button_rect) and mouse_click is True:
                        current_map = pygame.image.load("_Resources/Level2/map_locked.png").convert_alpha()
                        current_map.set_colorkey((255, 255, 255))
                        current_map_rect = current_map.get_rect()
                        current_map_mask = pygame.mask.from_surface(current_map)
                        level += 1
                        fish_found = False

        # Level 2 starting
        if level == 2:
            fish = pygame.image.load("_Resources/nemo_fish.png").convert_alpha()
            fish_rect = fish.get_rect()
            fish_mask = pygame.mask.from_surface(fish)

            # Check if the "Warning" pop-up is displayed
            if not pop_up_open:
                is_playing = True

            if is_alive:
                if not key_found and not door_unlocked and not pop_up_open:
                    screen.blit(key, key_rect)
                    screen.blit(door, door_rect)
                    if pixel_collision(player_mask, player_rect, key_mask, key_rect) and not pop_up_open:
                        door_unlocked = True
                        key_found = True

                if not door_unlocked:
                    if pixel_collision(player_mask, player_rect, door_mask, door_rect) and not pop_up_open:
                        pop_up_open = True

                        # Create close button of the pop-up
                        start_button = pygame.image.load("_Resources/Level2/close_icon.png")
                        start_button_rect = start_button.get_rect()
                        start_button_mask = pygame.mask.from_surface(start_button)

                        message_screen = pygame.image.load("_Resources/Level2/door_locked_warning.png")
                        message_screen_rect = message_screen.get_rect()

                        is_playing = False

                    if pop_up_open:
                        if pixel_collision(player_mask, player_rect, start_button_mask, start_button_rect) and mouse_click is True:
                            is_playing = True
                            pop_up_open = False

                            start_button = pygame.image.load("_Resources/StartScreen/StartButton.png")
                            start_button_rect = start_button.get_rect()
                            start_button_mask = pygame.mask.from_surface(start_button)
                            start_button_rect.center = (620, 550)

                if door_unlocked:
                    current_map = pygame.image.load("_Resources/Level2/map_unlocked.png").convert_alpha()
                    current_map.set_colorkey((255, 255, 255))
                    current_map_rect = current_map.get_rect()
                    current_map_mask = pygame.mask.from_surface(current_map)

                if key_found and not fish_found:
                    fish_rect.center = (100, 50)
                    screen.blit(fish, fish_rect)
                    if pixel_collision(player_mask, player_rect, fish_mask, fish_rect):
                        fish_found = True

                if pixel_collision(player_mask, player_rect, current_map_mask, current_map_rect) and is_playing and not fish_found:
                    is_playing = False
                    is_alive = False
                    level = -1

                if fish_found:
                    is_playing = False

                    message_screen = pygame.image.load("_Resources/Level3/message.png")
                    message_screen_rect = message_screen.get_rect()

                    if pixel_collision(player_mask, player_rect, start_button_mask, start_button_rect) and mouse_click is True:
                        current_map = pygame.image.load("_Resources/Level3/map.png").convert_alpha()
                        current_map.set_colorkey((255, 255, 255))
                        current_map_rect = current_map.get_rect()
                        current_map_mask = pygame.mask.from_surface(current_map)
                        level += 1
                        fish_found = False

        # Level 3 starting
        if level == 3:
            is_playing = True

            fish = pygame.image.load("_Resources/yellow_fish.png").convert_alpha()
            fish = pygame.transform.smoothscale(fish, (48, 31))
            fish_rect = fish.get_rect()
            fish_mask = pygame.mask.from_surface(fish)

            if not full:
                progress_text = str(progress) + '%'
                progress_stat = my_font.render(progress_text, True, (0, 0, 0))
                screen.blit(progress_stat, (765, 16))

            if is_alive:
                if not full:
                    # Adjust overvalued percentage to the maximum of 100%
                    if progress > 100:
                        progress = 100

                    if progress > 20:
                        player_scale = progress // 10
                        player = pygame.transform.smoothscale(player, (60 + 2 * player_scale, 60 + 2 * player_scale))

                    # Time for each fish is randomly display
                    if frame_count % 50 == 0:
                        fish_position = (random.randrange(0, 1280), random.randrange(72, 649))
                        fish_list.append(fish_position)

                    # Time for each 1% deduced in the stomach storage
                    if frame_count % 30 == 0:
                        progress -= 1

                    # Display all fish not yet eaten
                    for fish_display in fish_list:
                        fish_position_X = fish_display[0]
                        fish_position_y = fish_display[1]
                        fish_rect.center = (fish_position_X, fish_position_y)
                        screen.blit(fish, fish_rect)

                        # Remove the fish when it is eaten
                        if pixel_collision(player_mask, player_rect, fish_mask, fish_rect):
                            fish_list.remove((fish_position_X, fish_position_y))
                            progress += 10

                if progress == 100:
                    full = True
                    is_playing = False
                    message_screen = pygame.image.load("_Resources/you_win.png")
                    message_screen_rect = message_screen.get_rect()

                if pixel_collision(player_mask, player_rect, current_map_mask, current_map_rect) and not full or progress == 0:
                    is_playing = False
                    is_alive = False
                    level = -1

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(33)

    pygame.quit()
    sys.exit()


# Start the program
if __name__ == '__main__':
    main()
