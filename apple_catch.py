import pygame
from pygame.locals import *
import random
import time

def main():
    # * * * * * * * * * * * * *
    # * * * INITIALIZING  * * *
    # * * * * * * * * * * * * *

    # Constants
    width = 600
    height = 600
    blue_color = (97, 159, 182)
    starting_width = int( width / 2)
    starting_height = int( height - 58 )

    # Variables
    level = 0
    level_reset = 1                         # Toggles starting level
    max_lives = 3                           # Toggles max lives
    apples_reset = 12                       # Toggles apples needed
    game_length = 31                        # Toggles time (seconds) per level. Add 1 to desired number.
    player_victory = False
    repeat_game = True
    show_title_screen = True
    fade_title_screen = False
    clock_tick_playing = False
    title_fade_index = 255

    next_apple_time = 0.0
    next_worm_time = 0.0
    next_speed_boost = 0.0
    next_turtle_time = 0.0
    next_extra_jump = 0.0
    next_poison_time = 0.0
    next_extra_lives_time = 0.0
    next_golden_apple = 0.0

    # Setting up the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hectic Harvest')
    clock = pygame.time.Clock()

    # Initialize Music
    pygame.mixer.music.load('sounds/music.wav')
    pygame.mixer.music.set_volume(.3)
    pygame.mixer.music.play(-1)

    # Initialize Sounds
    bite = pygame.mixer.Sound('sounds/bite.wav')
    good_sound = pygame.mixer.Sound('sounds/positive.wav')
    goldapple = pygame.mixer.Sound('sounds/gold_apple.wav')
    negative_sound = pygame.mixer.Sound('sounds/negative.wav')
    game_over = pygame.mixer.Sound('sounds/GameOver.wav')
    game_over.set_volume(0.3)
    jumpy = pygame.mixer.Sound('sounds/jumpy.wav')
    jumpy.set_volume(0.7)
    jumpy_louder = pygame.mixer.Sound('sounds/jumpy.wav')
    jumpy_louder.set_volume(1)
    victory = pygame.mixer.Sound('sounds/victory.wav')
    level_up = pygame.mixer.Sound('sounds/level_up.wav')
    level_up.set_volume(0.5)
    extra_life = pygame.mixer.Sound('sounds/1up.wav')
    tick = pygame.mixer.Sound('sounds/clock_10_sec.wav')
    tick_channel = pygame.mixer.Channel(0)

    # Initializing Text
    font = pygame.font.Font(None, 30)
    victory_message = font.render('Level Won! Press ENTER to continue', True, (255, 255, 255))
    victory_rect = victory_message.get_rect(center=(int(width/2), int(height/2)))
    loss_message = font.render('You lost! To play again, press ENTER', True, (255, 255, 255))
    loss_rect = loss_message.get_rect(center=(int(width/2), int(height/2)))
    game_won_message = font.render('Congratulations! You Won! To play again, press ENTER', True, (255, 255, 255))
    game_won_rect = game_won_message.get_rect(center=(int(width/2), int(height/2)))

    # Victory / Loss Overlay
    overlay_surf = pygame.Surface((width, height))
    overlay_surf.fill((0, 0, 0))
    overlay_surf.set_alpha(70)
    overlay_surf = overlay_surf.convert_alpha()
    overlay_rect = overlay_surf.get_rect()

    # Create All Sprite Groups
    all_catchables = pygame.sprite.Group()
    all_avoidables = pygame.sprite.Group()
    all_falling = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Load Health Images
    red_health_img = pygame.image.load('images/redheart.png')
    red_health_img = pygame.transform.scale(red_health_img, (25, 25)).convert_alpha()
    gray_health_img = pygame.image.load('images/grayheart.png')
    gray_health_img = pygame.transform.scale(gray_health_img, (25, 25)).convert_alpha()

    # Load Background Image
    bg_image = pygame.image.load('images/background_cropped.png')
    bg_image = pygame.transform.scale(bg_image, (600, 600)).convert()
    title_image = pygame.image.load('images/title_menu.png')
    title_image = pygame.transform.scale(title_image, (600, 600)).convert()

    #Load Class Images
    player_img = pygame.image.load('images/guy_with_basket.png')
    apple_img = pygame.image.load('images/goodapple.png')
    gold_apple_img = pygame.image.load('images/goldapple.png')
    worm_img = pygame.image.load('images/worm.png')
    bad_apple_img = pygame.image.load('images/badapple.png')
    extra_jump_img = pygame.image.load('images/extra_jump.png')
    speed_img = pygame.image.load('images/speed.png')
    red_heart_img = pygame.image.load('images/purpleheart.png')
    slow_img = pygame.image.load('images/slow.png')



    # * * * * * * * * * * * * *
    # * * *    CLASSES    * * *
    # * * * * * * * * * * * * *

    class Player(pygame.sprite.Sprite):
        # Initialize
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.transform.scale(player_img, (75, 75)).convert_alpha()
            # self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(starting_width, starting_height))
            self.speed = 5
            all_sprites.add(self)

            # Jump Variables
            self.isJump = False
            self.momentum = 3
            self.velocity_reset = 6
            self.velocity = self.velocity_reset

        # Update - Once per frame
        def update(self, pressed_keys, has_extra_jump, has_speed_boost):
            # Movement
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:         # West
                self.rect.move_ip(-self.speed, 0)
            elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:      # East
                self.rect.move_ip(self.speed, 0)   

            # Movement Boundaries
            if self.rect.right > width - 15:
                self.rect.right = width - 15
            elif self.rect.left < 15:
                self.rect.left = 15 

            # Extra Jump
            if has_extra_jump:
                if self.velocity == self.velocity_reset:
                    self.velocity_reset = 9
                    self.velocity = self.velocity_reset
            else:
                self.velocity_reset = 6

            # Turtle / Speed Boost
            if has_turtle:
                self.speed = 3
            elif has_speed_boost:
                self.speed = 9
            else:
                self.speed = 5

            # Calculate Jump
            if pressed_keys[K_SPACE] or pressed_keys[K_w] or pressed_keys[K_UP]:
                self.isJump = True 

            if self.isJump:
                
                # Select Correct Sound for Different Jumps
                if self.velocity == self.velocity_reset and self.velocity_reset == 6:
                    pygame.mixer.Sound.play(jumpy)
                elif self.velocity == self.velocity_reset and self.velocity_reset == 9:
                    pygame.mixer.Sound.play(jumpy_louder)

                # Calculate Force, Update Location, Decrement Velocity
                self.force = self.momentum * self.velocity
                self.rect.move_ip(0, -self.force)
                self.velocity -= .4
                
                # Jump Boundaries
                if self.rect.bottom >= starting_height + 37:
                    self.rect.bottom = starting_height + 37
                    self.isJump = False
                    self.velocity = self.velocity_reset

    class Falling_Object(pygame.sprite.Sprite):
        # Super class for falling objects
        def __init__(self):
            super(Falling_Object, self).__init__()

            self.starting_x = self.calculate_x()
            all_sprites.add(self)
            all_falling.add(self)

            # Default speed
            self.speed = random.randint(1, 3)

        # Every Frame, Update Position
        def update(self):
            self.rect.move_ip(0, self.speed)

            # Remove When Off Screen
            if self.rect.top > height + 50:
                self.kill()

        # Calculates a random starting X value
        def calculate_x(self):
            return random.randint(50, width - 50)

    class Apple(Falling_Object):
        # NOTE: Perhaps add level as an argument and use that to adjust variables
        def __init__(self):
            super(Apple, self).__init__()
            
            # Object Surface Properties

            self.surf = pygame.transform.scale(apple_img, (30, 30)).convert_alpha()


            # self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))
                
            # Add to Group
            all_catchables.add(self)

    class Golden_Apple(Falling_Object):
        def __init__(self):
            super(Golden_Apple, self).__init__()

            # Object surface properties
            self.surf = pygame.transform.scale(gold_apple_img, (30, 30)).convert_alpha()
            # self.surf.fill((212, 175, 55))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Add to Group
            all_catchables.add(self)

    class Worm(Falling_Object):
        # Costs the player one life
        def __init__(self, level):
            super(Worm, self).__init__()

            # Object Surface Properties
            self.surf = pygame.transform.scale(worm_img, (35, 35)).convert_alpha()
            # self.surf.fill((0, 0, 0))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int((random.random() * 2 + 1) * ( 1 + self.level / 5 ) )

            # Add to Group
            all_avoidables.add(self)

    class Poison_Apple(Falling_Object):
        # An instant game over
        def __init__(self, level):
            super(Poison_Apple, self).__init__()

            # Object Surface Properties
            self.surf = pygame.transform.scale(bad_apple_img, (30, 30)).convert_alpha()
            # self.surf.fill((148, 178, 28))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int((random.random() * 2 + 1) * ( 1 + self.level / 5 ) )

            # Add to Group
            all_avoidables.add(self)

    class Extra_Jump(Falling_Object):
        # Gives an X second boost to jump height
        def __init__(self):
            super(Extra_Jump, self).__init__()

            # Object Surface Properties
            self.surf = pygame.transform.scale(extra_jump_img, (30, 58)).convert_alpha()
            # self.surf.fill((20, 20, 210))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Add to Group
            all_catchables.add(self)

    class Speed_Boost(Falling_Object):
        # Gives an X second boost to walking speed
        def __init__(self):
            super(Speed_Boost, self).__init__()

            # Object Surface Properties
            self.surf = pygame.transform.scale(speed_img, (39, 30)).convert_alpha()
            # self.surf.fill((175, 55, 212))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.speed = random.randint(1, 3)

            # Add to Groups
            all_catchables.add(self)

    class Extra_Lives(Falling_Object):
        def __init__(self):
            super(Extra_Lives, self).__init__()

            self.surf = pygame.transform.scale(red_heart_img, (30, 30)).convert_alpha()
            # self.surf.fill((240, 180, 240))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            all_catchables.add(self)

    class Turtle(Falling_Object):
        # Slows the player for X seconds
        def __init__(self, level):
            super(Turtle, self).__init__()

            # Object Surface Properties
            self.surf = pygame.transform.scale(slow_img, (44, 25)).convert_alpha()
            # self.surf.fill((240, 94, 35))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int((random.random() * 2 + 1) * ( 1 + self.level / 5 ) )

            # Add to Group
            all_avoidables.add(self)

    class Booster(Falling_Object):
        # --- Insert Code ---
        # Should booster item types be a sub class, or just have different functions within this class?
        #  -  Extra Life
        #  -  Speed Boost
        #  -  Reduced Worms 
        #  -  Increased Apples / Apple Speed
        #  -  Invincibility
        #  -  Increased catch width
        #  -  Slow down time
        #  -  Bigger and Immune
        pass


    # * * * * * * * * * * * * * *
    # * * *    FUNCTIONS    * * *
    # * * * * * * * * * * * * * *

    # Next Falling Object Functions
    def calc_next_apple_time():
        next_apple_time = time.time() + random.randint(0, 3)
        return next_apple_time
    
    def calc_next_worm_time():
        next_worm_time = time.time() + random.random() * (max_worm_time - min_worm_time) + min_worm_time
        return next_worm_time
    
    def calc_next_speed_boost():
        next_speed_boost = time.time() + random.randint(1, 20)
        return next_speed_boost
    
    def calc_next_turtle_time():
        next_turtle_time = time.time() + random.randint(1,15)
        return next_turtle_time
    
    def calc_next_extra_jump():
        next_extra_jump = time.time() + random.randint(1, 30)
        return next_extra_jump
    
    def calc_next_poison_time():
        next_poison_time = time.time() + random.random() * (max_poison_time - min_poison_time) + min_poison_time
        return next_poison_time
    
    def calc_next_extra_lives_time():
        next_extra_lives_time = time.time() + random.randint(1, 90)
        return next_extra_lives_time
    
    def calc_next_golden_apple():
        next_golden_apple = time.time() + random.randint(1, 90)
        return next_golden_apple


    # * * * * * * * * * * * * * *
    # * * *  TITLE SCREEN   * * *
    # * * * * * * * * * * * * * *

    # Display / Fade Out Title Screen
    while show_title_screen or fade_title_screen:
                # Event Handling
        for event in pygame.event.get():
            # Player Closed Pygame
            if event.type == pygame.QUIT:
                repeat_game = False
                show_title_screen = False
            elif event.type == KEYDOWN:
                # Player Hit ESC to Quit
                if event.key == K_ESCAPE:
                    repeat_game = False
                    show_title_screen = False
                # Player Hit ENTER to Continue / Restart
                if event.key == K_RETURN:
                    show_title_screen = False
                    fade_title_screen = True

        # Fades Out The Title Screen
        if fade_title_screen:
            title_fade_index -= 10
            title_fade_index = max(title_fade_index, 0)
            title_image.set_alpha(title_fade_index)
            if title_fade_index == 0:
                fade_title_screen = False
        
        # Displays the underlying background image and the title overay
        screen.blit(bg_image, (0, 0))
        screen.blit(title_image, (0, 0))

        pygame.display.update()
        clock.tick(60)


    # * * * * * * * * * * * * * *
    # * * * OUTER GAME LOOP * * *
    # * * * * * * * * * * * * * *
    
    # OUTER LOOP - New Levels & New Games
    
    while repeat_game:

        # Level Increment
        if player_victory and level < 10:
            level += 1
        else: # New Game
            level = level_reset
            lives_remaining = max_lives

        # Variable Resets
        stop_game = False
        player_victory = False
        player_loss = False
        has_extra_jump = False
        has_speed_boost = False
        has_turtle = False
        game_over_music_unplayed = True
        victory_music_unplayed = True
        level_up_music_unplayed = True
        end_time = time.time() + game_length
        apples_caught = 0
        apples_needed = apples_reset

        # # Resets Booster Clock Tick
        if clock_tick_playing:
            tick_channel.stop()
            clock_tick_playing = False

        # Resets Time Counters
        extra_jump_ending_time = 0
        speed_boost_ending_time = 0
        turtle_ending_time = 0

        # Worm Time - Toggles based on level
        min_worm_time = 2.25 - level * 0.2
        max_worm_time = 5.0 - level * 0.4
        min_poison_time = 12 - level * 1   # (Level 10: 2) (Level 4: 8)
        max_poison_time = 30 - level * 2.5     # (Level 10: 5) (Level 4: 20)

        # Generate Time Variables
        next_apple_time = time.time()           # Start every level with an apple
        next_worm_time = time.time() + 2        # Start every level with a worm after 2 seconds
        calc_next_speed_boost()
        calc_next_turtle_time()
        calc_next_extra_jump()
        calc_next_poison_time()
        calc_next_extra_lives_time()
        calc_next_golden_apple()

        # Create Our Player
        player = Player()



        # * * * * * * * * * * * * * *
        # * * * INNER GAME LOOP * * *
        # * * * * * * * * * * * * * *

        # INNER LOOP - Current Game
        while not stop_game:

            # Event Handling
            for event in pygame.event.get():
                # Player Closed Pygame
                if event.type == pygame.QUIT:
                    stop_game = True
                    repeat_game = False
                elif event.type == KEYDOWN:
                    # Player Hit ESC to Quit
                    if event.key == K_ESCAPE:
                        stop_game = True
                        repeat_game = False
                    # Player Hit ENTER to Continue / Restart
                    if (player_victory == True or player_loss == True) and event.key == K_RETURN:
                        for entity in all_sprites:
                            entity.kill()
                            stop_game = True

            # Create Falling Objects
            #   APPLE - Level 1
            if time.time() > next_apple_time:
                Apple()
                next_apple_time = calc_next_apple_time()
            #   WORM - Level 1
            if time.time() > next_worm_time:
                Worm(level)
                next_worm_time = calc_next_worm_time()
            if level >= 2:
                #   SPEED BOOST - Level 2
                if time.time() > next_speed_boost:
                    Speed_Boost()
                    next_speed_boost = calc_next_speed_boost()
                #   TURTLE - Level 2
                if time.time() > next_turtle_time:
                    Turtle(level)
                    next_turtle_time = calc_next_turtle_time()
            if level >= 3:
                #   EXTRA JUMP - Level 3
                if time.time() > next_extra_jump:
                    Extra_Jump()
                    next_extra_jump = calc_next_extra_jump()
            if level >= 4:
                #   POISON APPLE - Level 4
                if time.time() > next_poison_time:
                    Poison_Apple(level)
                    next_poison_time = calc_next_poison_time()
            if level >= 5:
                #   EXTRA LIVES - Level 5
                if time.time() > next_extra_lives_time:
                    Extra_Lives()
                    next_extra_lives_time = calc_next_extra_lives_time()
                #   GOLDEN APPLE - Level 5
                if time.time() > next_golden_apple:
                    Golden_Apple()
                    next_golden_apple = calc_next_golden_apple()

            # Checks and removes status effects
            if has_extra_jump:
                if time.time() > extra_jump_ending_time:
                    has_extra_jump = False
            if has_speed_boost:
                if time.time() > speed_boost_ending_time:
                    has_speed_boost = False
            if has_turtle:
                if time.time() > turtle_ending_time:
                    has_turtle = False

            # Update All Objects
            player.update(pygame.key.get_pressed(), has_extra_jump, has_speed_boost)
            for entity in all_falling:
                entity.update()

            # Check for Collisions
            if player_loss == False and player_victory == False:
                # For the GOOD items
                for catchable in all_catchables:
                    if pygame.sprite.collide_rect_ratio(0.6)(player, catchable):
                        catchable.kill()
                        catchable.rect.top = height + 100
                        if type(catchable) == Apple:
                            pygame.mixer.Sound.play(bite)
                            apples_caught += 1
                        elif type(catchable) == Golden_Apple:
                            pygame.mixer.Sound.play(goldapple)
                            apples_caught += 5
                        elif type(catchable) == Extra_Jump:
                            pygame.mixer.Sound.play(good_sound)
                            has_extra_jump = True
                            extra_jump_ending_time = time.time() + 10
                        elif type(catchable) == Speed_Boost:
                            pygame.mixer.Sound.play(good_sound)
                            has_speed_boost = True
                            has_turtle = False
                            speed_boost_ending_time = time.time() + 10
                        elif type(catchable) == Extra_Lives:
                            pygame.mixer.Sound.play(extra_life)
                            lives_remaining += 1
                            lives_remaining = min(lives_remaining, max_lives)
                # For the BAD items
                for avoidable in all_avoidables:
                    if pygame.sprite.collide_rect_ratio(0.6)(player, avoidable):
                        avoidable.kill()
                        avoidable.rect.top = height + 100
                        if type(avoidable) == Worm:
                            pygame.mixer.Sound.play(negative_sound)
                            lives_remaining -= 1
                        elif type(avoidable) == Poison_Apple:
                            lives_remaining = 0
                            player_loss = True
                        elif type(avoidable) == Turtle:
                            pygame.mixer.Sound.play(negative_sound)
                            has_turtle = True
                            has_speed_boost = False
                            turtle_ending_time = time.time() + 10

            # TIME UP: Win or Lose
            if apples_caught >= apples_needed:
                player_victory = True
            elif time.time() > end_time:
                player_loss = True
                if game_over_music_unplayed:
                    pygame.mixer.Sound.play(game_over)
                    game_over_music_unplayed = False

            # LIVES: Win or Lose
            if lives_remaining <= 0:
                player_loss = True
                if game_over_music_unplayed:
                    pygame.mixer.Sound.play(game_over)
                    game_over_music_unplayed = False

            # * * * * * * * * * * * * * * * *
            # * * * DRAW OBJECTS / TEXT * * *
            # * * * * * * * * * * * * * * * *

            # Draw Background
            screen.fill(blue_color)
            screen.blit(bg_image, (0, 0))

            # Draw All Objects
            for entity in all_falling:
                screen.blit(entity.surf, entity.rect)
            screen.blit(player.surf, player.rect)

            # Gray Overlay on Victory / Loss
            if player_victory or player_loss:
                screen.blit(overlay_surf, overlay_rect)

            # Draw Victory/Loss Message
            if player_victory and level == 10:
                screen.blit(game_won_message, game_won_rect)
                if victory_music_unplayed:
                    pygame.mixer.Sound.play(victory)
                    victory_music_unplayed = False
            elif player_victory:
                screen.blit(victory_message, victory_rect)
                if level_up_music_unplayed:
                    pygame.mixer.Sound.play(level_up)
                    level_up_music_unplayed = False
            elif player_loss:
                screen.blit(loss_message, loss_rect)
            
            # Calculate & Print Time Remaining
            if not player_victory and not player_loss:
                time_remaining = max(int(end_time - time.time()), 0)
            time_message = font.render('Time Remaining: {}'.format(time_remaining), True, (0, 0, 0))
            time_rect = time_message.get_rect(topright=(width - 20, 20))
            screen.blit(time_message, time_rect)
            
            # Print Apples Caught
            apple_message = font.render('Apples: {} / {}'.format(apples_caught, apples_needed), True, (0, 0, 0))
            apple_rect = apple_message.get_rect(topright=(time_rect.right, time_rect.bottom + 5))
            screen.blit(apple_message, apple_rect)

            # Draw Red Hearts for Lives Remaining
            if lives_remaining >= 1:
                health_rect = red_health_img.get_rect(topright=(apple_rect.right, apple_rect.bottom + 5))
                screen.blit(red_health_img, health_rect)
            i = 2
            while i <= lives_remaining:
                health_rect = red_health_img.get_rect(topright=(health_rect.left - 5, health_rect.top))
                screen.blit(red_health_img, health_rect)
                i += 1

            # Draw Gray Hearts for Lives Lost
            lives_lost = max_lives - lives_remaining
            if lives_lost == max_lives:
                gray_health_rect = gray_health_img.get_rect(topright=(apple_rect.right, apple_rect.bottom + 5))
                screen.blit(gray_health_img, gray_health_rect)
            if lives_lost > 0 and lives_lost < max_lives:
                gray_health_rect = gray_health_img.get_rect(topright=(health_rect.left - 5, health_rect.top))
                screen.blit(gray_health_img, gray_health_rect)
            i = 2
            while i <= lives_lost:
                gray_health_rect = red_health_img.get_rect(topright=(gray_health_rect.left - 5, gray_health_rect.top))
                screen.blit(gray_health_img, gray_health_rect)
                i += 1


            # TOP LEFT MESSAGES
            top_left_messages = []

            # Creates the Current Level Message
            level_message = font.render('Level {}'.format(level), True, (0, 0, 0))
            level_rect = level_message.get_rect(topleft=(20, 20))
            top_left_messages.append([level_message, level_rect])

            # Creates the Boost Messages
            if has_extra_jump:
                extra_jump_message = font.render('Jump Boost: {}'.format(int(extra_jump_ending_time - time.time())), True, (0, 0, 0))
                extra_jump_rect = extra_jump_message.get_rect(topleft=(20, 20))
                top_left_messages.append([extra_jump_message, extra_jump_rect])
            if has_speed_boost:
                speed_boost_message = font.render('Speed Boost: {}'.format(int(speed_boost_ending_time - time.time())), True, (0, 0, 0))
                speed_boost_rect = speed_boost_message.get_rect(topleft=(20, 20))
                top_left_messages.append([speed_boost_message, speed_boost_rect])
            if has_turtle:
                turtle_message = font.render('Slow-mo: {}'.format(int(turtle_ending_time - time.time())), True, (0, 0, 0))
                turtle_rect = turtle_message.get_rect(topleft=(20, 20))
                top_left_messages.append([turtle_message, turtle_rect])
            
            # Prints All Messages in Top Left Corner
            for i in range(len(top_left_messages)):
                if i != 0:
                    top_left_messages[i][1] = top_left_messages[i][0].get_rect(topleft=(top_left_messages[i-1][1].left, top_left_messages[i-1][1].bottom + 5))
                screen.blit(top_left_messages[i][0], top_left_messages[i][1])

            # Ticks if we've got Boost Messages
            if (extra_jump_ending_time > time.time() + 1 and extra_jump_ending_time < time.time() + 3.5) or (speed_boost_ending_time > time.time() + 1 and speed_boost_ending_time < time.time() + 3.5) or (turtle_ending_time > time.time() + 1 and turtle_ending_time < time.time() + 3.5):
                if not clock_tick_playing:
                    # pygame.mixer.Sound.play(tick)
                    tick_channel.play(tick)
                    clock_tick_playing = True
            elif clock_tick_playing:
                tick_channel.stop()
                clock_tick_playing = False
                

            # Refresh Game Display
            pygame.display.update()
            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()