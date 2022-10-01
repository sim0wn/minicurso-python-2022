"""
author: tyl3rsec
"""

import sys
import random
import pygame

# constant variables
CAPTION = 'Jogo da cobrinha'
SCREEN_SIZE = (720, 480)
BLOCK_SIZE = 20

# functions
def game_over():
    """
    this functions prints a game over message
    """
    print("Game Over!")


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION) # set the window's title
    screen = pygame.display.set_mode(SCREEN_SIZE) # set the window's size
    clock = pygame.time.Clock() # to control game's speed later
    # snake is iniatilly positioned in the middle
    snake_position = [
        screen.get_rect().center[0]-screen.get_rect().center[0]%20,
        screen.get_rect().center[1]-screen.get_rect().center[1]%20
    ]
    snake_body = [
        [*snake_position],
        [snake_position[0]-BLOCK_SIZE, snake_position[1]],
        [snake_position[0]-BLOCK_SIZE*2, snake_position[1]],
        [snake_position[0]-BLOCK_SIZE*3, snake_position[1]]
    ]
    snake_size = BLOCK_SIZE
    direction = "RIGHT" # start moving to the right
    fruit_position = [0, 0]
    game_score = 0 # track user score
    while True:
        screen.fill((0, 0, 0))
        # event handling
        for event in pygame.event.get():
            match event.type:
                # stop the application if user tries to quit
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        case pygame.K_LEFT:
                            if direction != "RIGHT":
                                direction = "LEFT"
                        case pygame.K_UP:
                            if direction != "DOWN":
                                direction = "UP"
                        case pygame.K_DOWN:
                            if direction != "UP":
                                direction = "DOWN"
                        case pygame.K_RIGHT:
                            if direction != "LEFT":
                                direction = "RIGHT"
        # scoreboard
        score = pygame.font.Font(None, 32).render(
            f'Pontuação: {game_score}',
            True,
            pygame.Color(255, 255, 255)
        )
        screen.blit(score, (0,0))
        # game logic
        match direction:
            case "LEFT":
                snake_position[0] = snake_position[0]-BLOCK_SIZE
            case "UP":
                snake_position[1] = snake_position[1]-BLOCK_SIZE
            case "DOWN":
                snake_position[1] = snake_position[1]+BLOCK_SIZE
            case "RIGHT":
                snake_position[0] = snake_position[0]+BLOCK_SIZE
                if snake_position[0] > SCREEN_SIZE[0]:
                    game_over()
        if not all(fruit_position):
            fruit_position[0] = random.randrange(
                0, screen.get_width()+1, BLOCK_SIZE
            )
            fruit_position[1] = random.randrange(
                0, screen.get_height()+1, BLOCK_SIZE
            )
        snake_body.insert(0, list(snake_position))
        if (
            snake_position[0] == fruit_position[0] and
            snake_position[1] == fruit_position[1]
        ):
            fruit_position = [0, 0]
            game_score += 1
            snake_size += BLOCK_SIZE
        else:
            snake_body.pop()
        for block in snake_body[1:]:
            if(
                snake_position[0] == block[0] and
                snake_position[1] == block[1]
            ):
                game_over()
        # game elements
        pygame.draw.rect(
            screen,
            pygame.Color(0, 255, 0),
            pygame.Rect(*fruit_position, BLOCK_SIZE, BLOCK_SIZE)
        )
        for block in snake_body:
            pygame.draw.rect(
                screen,
                pygame.Color(0, 0, 255),
                pygame.Rect(*block, BLOCK_SIZE, BLOCK_SIZE)
            )
        # update objects
        pygame.display.flip()
        clock.tick(10)
