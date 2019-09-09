import pygame
from pygame.locals import *
import random
import time

def main():
    # Variables
    width = 600
    height = 600
    blue_color = (97, 159, 182)
    player_victory = False
    starting_width = int(width/2)
    starting_height = int(height - 50)
    next_apple_time = time.time()
    next_worm_time = time.time() + 5

    # Interactive Variables
    level = 1
    lives_remaining = 3
    game_length = 30


    # Setting up the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Apple Catch')
    clock = pygame.time.Clock()

    # Initialize Sounds
    # --- Insert Code ---

    # Initializing Text
    # --- Insert Code ---
    font = pygame.font.Font(None, 30)
    victory_message = font.render('Victory! To play again, press ENTER', True, (255, 255, 255))
    victory_rect = victory_message.get_rect(center=(int(width/2), int(height/2)))
    loss_message = font.render('Loser! To play again, press ENTER', True, (255, 255, 255))
    loss_rect = loss_message.get_rect(center=(int(width/2), int(height/2)))

    # Object Classes
    class Player(pygame.sprite.Sprite):
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

        # --- Insert Code ---

        def update(self, pressed_keys):
            if pressed_keys[K_LEFT]:                          # West
                self.rect.move_ip(-self.speed, 0)
            elif pressed_keys[K_RIGHT]:                         # East
                self.rect.move_ip(self.speed, 0)   

            if self.rect.right > width-50:
                self.rect.right = width-50
            elif self.rect.left < 50:
                self.rect.left = 50

            if pressed_keys[K_SPACE]:
                self.isJump = True        

            if self.isJump:
                self.force = self.momentum * self.velocity

                self.rect.move_ip(0, -self.force)

                self.velocity -= .4

                if self.rect.bottom >= starting_height + 15:
                    self.rect.bottom = starting_height + 15
                    self.isJump = False
                    self.velocity = self.velocity_reset

    class Falling_Object(pygame.sprite.Sprite):
        # --- Insert Code ---
        def __init__(self):
            super(Falling_Object, self).__init__()

            self.starting_x = self.calculate_x()
            all_sprites.add(self)
            all_falling.add(self)

        # Every Frame, Update Position
        def update(self):
            self.rect.move_ip(0, self.speed)

            # Remove When Off Screen
            if self.rect.top > height + 50:
                self.kill()

        def calculate_x(self):
            return random.randint(50, width - 50)

    class Apple(Falling_Object):  # NOTE: switch to Falling_Object eventually
        # --- Insert Code ---
        # NOTE: Perhaps add level as an argument and use that to adjust variables
        def __init__(self):
            super(Apple, self).__init__()
            
            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))
            self.speed = random.randint(1, 3)
                # self.test = self.calculate_x()
                # print("Starting x is {}".format(self.test))
                
            # Add to Groups
            all_catchables.add(self)

    class Worm(Falling_Object):
        def __init__(self):
            super(Worm, self).__init__()

            # Object Surface Properties
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((0, 0, 0))
            self.rect = self.surf.get_rect(center=(self.starting_x, -50))
                # self.test = self.calculate_x()
                # print("Starting x is {}".format(self.test))

            self.speed = random.randint(1, 3)
            # self.speed = int(random.randint(1, 3) * (level-1)/5) #NOTE: Need to convert this to just Random() like the other one
            print(self.speed)

            # Add to Groups
            all_avoidables.add(self)

    class Booster(Falling_Object):
        # --- Insert Code ---
        pass




    # *** MAIN GAME LOOP ***
    
    repeat_game = True
    while repeat_game:      # This outer loop is to play again on a win/loss

        # Groups
        all_catchables = pygame.sprite.Group()
        all_avoidables = pygame.sprite.Group()
        all_falling = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        # Level Increment
        if player_victory == True:
            level += 1
        else:
            level = 1
            lives_remaining = 3

        # Variable Resets
        # --- Insert Code ---
        stop_game = False
        player_victory = False
        player_loss = False
        end_time = time.time() + game_length
        apples_caught = 0
        apples_needed = 10  # NOTE: change this to level based

        # Worm Time - Toggles based on level. NOTE: need to fine tune
        min_worm_time = max(3.25 - level * 0.25, 0.5)
        max_worm_time = max(6.5 - level * 0.5, 1)
        print(min_worm_time)
        print(max_worm_time)

        # Create Our Player Object
        player = Player()


        # Current Game Loop
        while not stop_game:
            for event in pygame.event.get():

                # Event Handling
                if event.type == pygame.QUIT:  # Pygame is closed
                    stop_game = True
                    repeat_game = False
                elif event.type == KEYDOWN:  # Player hits ESC to quit
                    if event.key == K_ESCAPE:
                        stop_game = True
                        repeat_game = False
                    if (player_victory == True or player_loss == True) and event.key == K_RETURN:  # Player wants to play again
                        for entity in all_sprites:
                            entity.kill()
                            stop_game = True

            # Create Falling Objects
            if time.time() > next_apple_time:
                apple = Apple()
                next_apple_time = time.time() + random.randint(1, 3)
            if time.time() > next_worm_time:
                worm = Worm()
                next_worm_time = time.time() + random.random() * (max_worm_time - min_worm_time) + min_worm_time

            # Update Objects
            # --- Insert Code ---
            player.update(pygame.key.get_pressed())
            for entity in all_falling:
                entity.update()

            # Check for Collisions
            # --- Insert Code ---
            if player_loss == False and player_victory == False:
                for catchable in all_catchables:
                    if pygame.sprite.collide_rect(player, catchable):
                        catchable.kill()
                        catchable.rect.top = height + 100
                        apples_caught += 1
                for avoidable in all_avoidables:
                    if pygame.sprite.collide_rect(player, avoidable):
                        avoidable.kill()
                        avoidable.rect.top = height + 100
                        lives_remaining -= 1

            # TIME UP: Win or Lose
            if apples_caught >= apples_needed:
                player_victory = True
            elif time.time() > end_time:
                player_loss = True

            # LIVES: Win or Lose
            if lives_remaining <= 0:
                player_loss = True

            # Draw Background
            screen.fill(blue_color)
            # *** THIS WILL BE CHANGED WITH THE IMAGES ***
                # background = pygame.Surface(screen.get_size())
                # background.fill(blue_color)
                # screen.blit(background, (0, 0))
                # bg_image = pygame.image.load('image location')


            # Draw All Objects
            for entity in all_falling:
                screen.blit(entity.surf, entity.rect)
            # Done separate to ensure the player is drawn on top. If we want the player behind the falling objects, change the for loop to all_entities
            screen.blit(player.surf, player.rect)

            # Draw Victory/Loss Message
            if player_victory:
                screen.blit(victory_message, victory_rect)
            elif player_loss:
                screen.blit(loss_message, loss_rect)


            # Draw Text Overlay
            
            # Calculate & Print Time Remaining
            if not player_victory and not player_loss:
                time_remaining = max(int(end_time - time.time() + 1), 0)
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

            # Print Level
            level_message = font.render('Level {}'.format(level), True, (255, 255, 255))
            level_rect = level_message.get_rect(topleft=(20, 20))
            screen.blit(level_message, level_rect)


            # Refresh Game Display
            pygame.display.update()
            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()