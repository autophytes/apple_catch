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
    starting_width = int(width/2)
    starting_height = int(height - 50)

    # Variables
    level = 1
    lives_remaining = 3
    game_length = 31        # Set at 31 so the display starts at 30 and ends at 0.
    has_extra_jump = False
    has_speed_boost = False
    has_turtle = False
    player_victory = False

    # Time Counters
    next_apple_time = time.time()
    next_worm_time = time.time() + 2
    next_poison_time = time.time() + random.randint(10, 40)
    next_golden_apple = time.time() + random.randint(25, 55) # make this much longer
    next_extra_jump = time.time() + random.randint(25, 55)
    next_speed_boost = time.time() + random.randint(1, 2) # make this much longer
    next_extra_lives_time = time.time() + random.randint(2, 4)
    next_turtle_time = time.time() + random.randint(5,10)
    extra_jump_ending_time = 0
    speed_boost_ending_time = 0
    turtle_ending_time = 0

    # Setting up the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Apple Catch')
    clock = pygame.time.Clock()

    # Initialize Sounds NOTE: Find and set up sounds.
    # --- Insert Code ---

    # Initializing Text
    font = pygame.font.Font(None, 30)
    victory_message = font.render('Level Won! Press ENTER to continue', True, (255, 255, 255))
    victory_rect = victory_message.get_rect(center=(int(width/2), int(height/2)))
    loss_message = font.render('You lost! To play again, press ENTER', True, (255, 255, 255))
    loss_rect = loss_message.get_rect(center=(int(width/2), int(height/2)))
    game_won_message = font.render('Congratulations! You Won! To play again, press ENTER', True, (255, 255, 255))
    game_won_rect = game_won_message.get_rect(center=(int(width/2), int(height/2)))

    # Create All Sprite Groups
    all_catchables = pygame.sprite.Group()
    all_avoidables = pygame.sprite.Group()
    all_falling = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Load images into memory
    bg_image = pygame.image.load('images/background_cropped.png')
    bg_image = pygame.transform.scale(bg_image, (600, 600)).convert()



    # * * * * * * * * * * * * *
    # * * *    CLASSES    * * *
    # * * * * * * * * * * * * *
    
    class Player(pygame.sprite.Sprite):
        # Initialize
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((255, 255, 255))
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

            if self.rect.right > width-40:
                self.rect.right = width-40
            elif self.rect.left < 40:
                self.rect.left = 40  

            # Extra Jump
            if has_extra_jump:
                self.velocity_reset = 9
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
                self.force = self.momentum * self.velocity

                self.rect.move_ip(0, -self.force)

                self.velocity -= .4

                if self.rect.bottom >= starting_height + 15:
                    self.rect.bottom = starting_height + 15
                    self.isJump = False
                    self.velocity = self.velocity_reset
            print(has_turtle)
            print(self.speed)

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
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))
                
            # Add to Group
            all_catchables.add(self)

    class Golden_Apple(Falling_Object):
        def __init__(self):
            super(Golden_Apple, self).__init__()

            # Object surface properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((212, 175, 55))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Add to Group
            all_catchables.add(self)

    class Worm(Falling_Object):
        # Costs the player one life
        def __init__(self, level):
            super(Worm, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((0, 0, 0))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int(random.randint(1, 3) * ( 1 + self.level / 5 ) ) #NOTE: Need to convert this to just Random() like the other one

            # Add to Group
            all_avoidables.add(self)

    class Poison_Apple(Falling_Object):
        # An instant game over
        def __init__(self, level):
            super(Poison_Apple, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((148, 178, 28))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int(random.randint(1, 3) * ( 1 + self.level / 5 ) ) #NOTE: Need to convert this to just Random() like the other one

            # Add to Group
            all_avoidables.add(self)

    class Extra_Jump(Falling_Object):
        # Gives an X second boost to jump height
        def __init__(self):
            super(Extra_Jump, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((20, 20, 210))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Add to Group
            all_catchables.add(self)

    class Speed_Boost(Falling_Object):
        # Gives an X second boost to walking speed
        def __init__(self):
            super(Speed_Boost, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((175, 55, 212))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.speed = random.randint(1, 3)

            # Add to Groups
            all_catchables.add(self)

    class Extra_Lives(Falling_Object):
        def __init__(self):
            super(Extra_Lives, self).__init__()

            self.surf = pygame.Surface((10, 10))
            self.surf.fill((240, 180, 240))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            all_catchables.add(self)

    class Turtle(Falling_Object):
        # Slows the player for X seconds
        def __init__(self, level):
            super(Turtle, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((240, 94, 35))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))

            # Variables
            self.level = level
            self.speed = int(random.randint(1, 3) * ( 1 + self.level / 5 ) ) #NOTE: Need to convert this to just Random() like the other one

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
    # * * * OUTER GAME LOOP * * *
    # * * * * * * * * * * * * * *
    
    # OUTER LOOP - New Levels & New Games
    repeat_game = True
    while repeat_game:

        # Level Increment
        if player_victory and level < 10:
            level += 1
        else: # New Game
            level = 1
            lives_remaining = 3

        # Variable Resets
        stop_game = False
        player_victory = False
        player_loss = False
        end_time = time.time() + game_length
        apples_caught = 0
        apples_needed = 10  # NOTE: change this to level based

        # Worm Time - Toggles based on level. NOTE: need to fine tune. Probably reduce time. Exponential?
        min_worm_time = max(2.15 - level * 0.2, 0.5)
        max_worm_time = max(4.9 - level * 0.4, 1)
        print(min_worm_time)
        print(max_worm_time)

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
            #   APPLE
            if time.time() > next_apple_time:
                Apple()
                next_apple_time = time.time() + random.randint(0, 3)
            #   WORM
            if time.time() > next_worm_time:
                Worm(level)
                next_worm_time = time.time() + random.random() * (max_worm_time - min_worm_time) + min_worm_time
            #   POISON APPLE
            if time.time() > next_poison_time:
                Poison_Apple(level)
                next_poison_time = time.time() + random.random() * random.randint(10, 40)
            #   GOLDEN APPLE
            if time.time() > next_golden_apple:
                Golden_Apple()
                next_golden_apple = time.time() + random.random() * random.randint(25, 55)
            #   EXTRA JUMP
            if time.time() > next_extra_jump:
                Extra_Jump()
                next_extra_jump = time.time() + random.random() * random.randint(25, 55)
            #   SPEED BOOST
            if time.time() > next_speed_boost:
                Speed_Boost()
                next_speed_boost = time.time() + random.random() * random.randint(25, 55)
            #   EXTRA LIVES
            if time.time() > next_extra_lives_time:
                Extra_Lives()
                next_extra_lives_time = time.time() + random.randint(2, 4)
            #   TURTLE
            if time.time() > next_turtle_time:
                Turtle(level)
                next_turtle_time = time.time() + random.randint(5,10)

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
                    if pygame.sprite.collide_rect(player, catchable):
                        catchable.kill()
                        catchable.rect.top = height + 100
                        if type(catchable) == Apple:
                            apples_caught += 1
                        elif type(catchable) == Golden_Apple:
                            apples_caught += 5
                        elif type(catchable) == Extra_Jump:
                            has_extra_jump = True
                            extra_jump_ending_time = time.time() + 10
                        elif type(catchable) == Speed_Boost:
                            has_speed_boost = True
                            has_turtle = False
                            speed_boost_ending_time = time.time() + 10
                        elif type(catchable) == Extra_Lives:
                            lives_remaining += 1
                # For the BAD items
                for avoidable in all_avoidables:
                    if pygame.sprite.collide_rect(player, avoidable):
                        avoidable.kill()
                        avoidable.rect.top = height + 100
                        if type(avoidable) == Worm:
                            lives_remaining -= 1
                        elif type(avoidable) == Poison_Apple:
                            lives_remaining = 0
                            player_loss = True
                        elif type(avoidable) == Turtle:
                            has_turtle = True
                            has_speed_boost = False
                            turtle_ending_time = time.time() + 10

            # TIME UP: Win or Lose
            if apples_caught >= apples_needed:
                player_victory = True
            elif time.time() > end_time:
                player_loss = True

            # LIVES: Win or Lose
            if lives_remaining <= 0:
                player_loss = True

            # * * * * * * * * * * * * * * * *
            # * * * DRAW OBJECTS / TEXT * * *
            # * * * * * * * * * * * * * * * *

            # Draw Background
            screen.fill(blue_color)
            # *** THIS WILL BE CHANGED WITH THE IMAGES ***
            screen.blit(bg_image, (0, 0))

            # Draw All Objects
            for entity in all_falling:
                screen.blit(entity.surf, entity.rect)
            screen.blit(player.surf, player.rect)

            # Draw Victory/Loss Message
            if player_victory and level == 10:
                screen.blit(game_won_message, game_won_rect)
            elif player_victory:
                screen.blit(victory_message, victory_rect)
            elif player_loss:
                screen.blit(loss_message, loss_rect)
            
            # Calculate & Print Time Remaining
            if not player_victory and not player_loss:
                time_remaining = max(int(end_time - time.time()), 0)
            time_message = font.render('Time Remaining: {}'.format(time_remaining), True, (255, 255, 255))
            time_rect = time_message.get_rect(topright=(width - 20, 20))
            screen.blit(time_message, time_rect)
            
            # Print Apples Caught
            apple_message = font.render('Apples: {} / {}'.format(apples_caught, apples_needed), True, (255, 255, 255))
            apple_rect = apple_message.get_rect(topright=(time_rect.right, time_rect.bottom + 5))
            screen.blit(apple_message, apple_rect)

            # Print Lives Remaining
            lives_message = font.render('Lives: {}'.format(lives_remaining), True, (255, 255, 255))
            lives_rect = lives_message.get_rect(topright=(apple_rect.right, apple_rect.bottom + 5))
            screen.blit(lives_message, lives_rect)

            if lives_remaining == 5:

            # Print Level
            level_message = font.render('Level {}'.format(level), True, (255, 255, 255))
            level_rect = level_message.get_rect(topleft=(20, 20))
            screen.blit(level_message, level_rect)

            # Refresh Game Display
            pygame.display.update()
            clock.tick(60)
            print(clock.get_fps())

    pygame.quit()

if __name__ == '__main__':
    main()