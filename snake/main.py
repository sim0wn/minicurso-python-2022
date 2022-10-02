"""
author: tyl3rsec
"""

import sys
import random

try:
    import pygame
except ImportError as exception:
    raise ImportError(
        '[!] Não foi possível importar a biblioteca "pygame"!'
    ) from exception


# constant variables
CAPTION = 'Snake'
SCREEN_SIZE = (720, 480)
BLOCK_SIZE = 20
INITIAL_POSITION = (
    (SCREEN_SIZE[0]/2)-BLOCK_SIZE, (SCREEN_SIZE[1]/2)-BLOCK_SIZE
)
INITIAL_LENGTH = 5
SNAKE_COLOR = pygame.Color(0, 255, 0)
FRUIT_COLOR = pygame.Color(255, 0, 0)


class Snake():
    """
    Cobra
    """
    def __init__(
        self,
        initial_position,
        initial_length,
        block_size,
        play_area
    ):
        self._body = [(initial_position)]
        self._length = initial_length
        self._block_size = block_size
        for position in range(1, self._length+1):
            self._body.insert(
                0,
                (
                    initial_position[0]-(self._block_size*position),
                    initial_position[1]
                )
            )
        self._play_area = play_area
        self._direction = "RIGHT"

    def get_body(self):
        """ Retorna a estrutura atual da cobra """
        return self._body

    def get_position(self):
        """ Retorna as coordenadas da cabeça da cobra """
        return self._body[-1]

    def get_direction(self):
        """ Retorna a direção na qual a cobra está indo """
        return self._direction

    def is_colliding(self):
        """ Verifica se há colisão da cobra """
        x_coordinates, y_coordinates = zip(*self._body)
        itself = False
        print(x_coordinates, y_coordinates)
        if x_coordinates[-1] in x_coordinates[:-2]:
            if y_coordinates[-1] in y_coordinates[:-2]:
                itself = True
        return (
            itself or
            (self._body[-1][0] > self._play_area[0]) or
            (self._body[-1][0] < 0) or
            (self._body[-1][1] > self._play_area[1]) or
            (self._body[-1][1] < 0)
        )

    def change_direction(self, direction):
        """ Muda a orientação de movimento da cobra """
        match direction:
            case "LEFT":
                if self._direction != "RIGHT":
                    self._direction = "LEFT"
            case "UP":
                if self._direction != "DOWN":
                    self._direction = "UP"
            case "RIGHT":
                if self._direction != "LEFT":
                    self._direction = "RIGHT"
            case "DOWN":
                if self._direction != "UP":
                    self._direction = "DOWN"

    def grow(self):
        """ Faz a cobra crescer """
        self._length += 1

    def move(self):
        """ Faz com que a cobra se mova """
        x_coordinate = self._body[-1][0]
        y_coordinate = self._body[-1][1]
        match self._direction:
            case ("LEFT"):
                self._body.append(
                    (
                        x_coordinate - self._block_size,
                        y_coordinate
                    )
                )
                # del self._body[0]
            case ("UP"):
                self._body.append(
                    (
                        x_coordinate,
                        y_coordinate - self._block_size
                    )
                )
                # del self._body[0]
            case ("RIGHT"):
                self._body.append(
                    (
                        x_coordinate + self._block_size,
                        y_coordinate
                    )
                )
                # del self._body[0]
            case ("DOWN"):
                self._body.append(
                    (
                        x_coordinate,
                        y_coordinate + self._block_size
                    )
                )
                # del self._body[0]
        if len(self._body) > self._length:
            del self._body[0]

class Game:
    """
    Classe do jogo
    """
    def __init__(self):
        self._score = 0
        self._spawned_fruit = 0
        self._fruit_position = ()

    def get_score(self):
        """ Retorna a pontuação do jogo """
        return self._score

    def score(self):
        """ Faz com que o jogador pontue """
        self._score += 1
        self._spawned_fruit = 0

    def game_over(self):
        """ Acaba com o jogo """
        print("[!] Game over!")

    def spawn_fruit(self):
        """ Gera coordenadas para posicionar a fruta no mapa """
        if self._spawned_fruit == 0:
            position = (
                random.randrange(0, SCREEN_SIZE[0], BLOCK_SIZE),
                random.randrange(0, SCREEN_SIZE[1], BLOCK_SIZE)
            )
            if position not in snake.get_body():
                self._spawned_fruit = 1
                self._fruit_position = position
        return self._fruit_position


def draw_scoreboard(score):
    """ Desenha o placar na tela """
    screen.blit(
        pygame.font.Font(None, 32).render(
            f'Pontuação: {score}',
            True,
            pygame.Color(255, 255, 255)
        ),
        (0,0)
    )



if __name__ == '__main__':
    # PyGame setup
    pygame.init()
    pygame.display.set_caption(CAPTION) # altera o título da janela
    screen = pygame.display.set_mode(SCREEN_SIZE) # altera o tamanho da janela
    clock = pygame.time.Clock() # controle da velocidade do jogo
    # objetos
    snake = Snake(INITIAL_POSITION, INITIAL_LENGTH, BLOCK_SIZE, SCREEN_SIZE)
    game = Game()
    while True:
        screen.fill((0, 0, 0))
        # tratamento dos eventos
        for event in pygame.event.get():
            match event.type:
                # a aplicação deixa de executar se o usuário tentar fechar
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        # setinhas para controlar o jogo
                        case pygame.K_LEFT:
                            snake.change_direction("LEFT")
                        case pygame.K_UP:
                            snake.change_direction("UP")
                        case pygame.K_DOWN:
                            snake.change_direction("DOWN")
                        case pygame.K_RIGHT:
                            snake.change_direction("RIGHT")
        # elementos do jogo
        fruit = game.spawn_fruit()
        # caso aconteça de a fruta não ser gerada, executa o bloco acima
        # novamente
        if not fruit:
            continue
        draw_scoreboard(game.get_score())
        # _desenha a fruta
        pygame.draw.rect(
            screen,
            FRUIT_COLOR,
            pygame.Rect(*fruit, BLOCK_SIZE, BLOCK_SIZE)
        )
        # _desenha a cobra
        for block in snake.get_body():
            pygame.draw.rect(
                screen,
                pygame.Color(255, 255, 255),
                pygame.Rect(*block, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                screen,
                SNAKE_COLOR,
                pygame.Rect(block[0]+1, block[1]+1, BLOCK_SIZE-2, BLOCK_SIZE-2)
            )
        # atualiza a posição da cobra a cada execução
        snake.move()
        # verifica se há colisão entre a cobra e a fruta
        if snake.get_position() == fruit:
            game.score()
            snake.grow()
        print(snake.is_colliding())
        # atualiza a tela
        pygame.display.flip()
        clock.tick(15)
