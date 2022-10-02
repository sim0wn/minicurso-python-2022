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


# variáveis constantes
# _pygame
CAPTION = 'Snake'
SCREEN_SIZE = (720, 480)
SNAKE_COLOR = pygame.Color(0, 255, 0)
FRUIT_COLOR = pygame.Color(255, 0, 0)
BACKGROUND_COLOR = pygame.Color(255, 210, 80)
# _jogo
BLOCK_SIZE = 20
PLAY_SURFACE = (SCREEN_SIZE[0]-BLOCK_SIZE, SCREEN_SIZE[1]-BLOCK_SIZE)
INITIAL_POSITION = (
    (SCREEN_SIZE[0]/2)-BLOCK_SIZE, (SCREEN_SIZE[1]/2)-BLOCK_SIZE
)
INITIAL_LENGTH = 5


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
        """ Retorna toda a estrutura da cobra """
        return self._body

    def get_position(self):
        """ Retorna as coordenadas da cabeça da cobra """
        return self._body[-1]

    def get_direction(self):
        """ Retorna a direção na qual a cobra está indo """
        return self._direction

    def is_colliding(self):
        """ Verifica se há colisão da cobra """
        head = self._body[-1]
        x_borders = self._play_area[0], SCREEN_SIZE[0]-self._play_area[0]
        y_borders = self._play_area[1], (SCREEN_SIZE[1]-self._play_area[1])*3
        # verifica se ela passou da área jogável
        if (
            head[0]+BLOCK_SIZE > x_borders[0] or
            head[0] < x_borders[1] or
            head[1]+BLOCK_SIZE > y_borders[0] or
            head[1]+BLOCK_SIZE < y_borders[1]
        ):
            return True
        # verifica se ela não atingiu a si mesma
        for body_part in self._body[:-1]:
            if head == body_part:
                return True
        return False

    def turn(self, direction):
        """
        Muda a orientação de movimento da cobra, verificando a direção
        atual para evitar que ela vire a 180 graus
        """
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
        """
        Reorganiza o posicionamento de seu corpo, fazendo com que ele se mova
        """
        head = self._body[-1]
        match self._direction:
            case ("LEFT"):
                self._body.append(
                    (
                        head[0] - self._block_size,
                        head[1]
                    )
                )
            case ("UP"):
                self._body.append(
                    (
                        head[0],
                        head[1] - self._block_size
                    )
                )
            case ("RIGHT"):
                self._body.append(
                    (
                        head[0] + self._block_size,
                        head[1]
                    )
                )
            case ("DOWN"):
                self._body.append(
                    (
                        head[0],
                        head[1] + self._block_size
                    )
                )
        # como um novo elemento é adicionado a lista com o append, é preciso
        # verificar o tamanho total dela e eliminar o último elemento caso seu
        # corpo ultrapasse o tamanho total
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
        self._running = True
        self._fps = 15

    def running(self):
        """ Retorna o status do jogo """
        return self._running

    def get_score(self):
        """ Retorna a pontuação do jogo """
        return self._score

    def get_fps(self):
        """ Retorna a velocidade do jogo """
        return self._fps

    def score(self):
        """ Faz com que o jogador pontue """
        self._score += 1
        self._spawned_fruit = 0
        self._fps *= 1.005

    def game_over(self):
        """ Acaba com o jogo """
        print("[!] Game over!")
        self._running = False

    def spawn_fruit(self):
        """ Gera coordenadas para posicionar a fruta no mapa """
        x_borders = PLAY_SURFACE[0], SCREEN_SIZE[0]-PLAY_SURFACE[0]
        y_borders = PLAY_SURFACE[1], (SCREEN_SIZE[1]-PLAY_SURFACE[1])*3
        if self._spawned_fruit == 0:
            position = (
                random.randrange(x_borders[1], x_borders[0], BLOCK_SIZE),
                random.randrange(y_borders[1], y_borders[0], BLOCK_SIZE)
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
            pygame.Color(0, 0, 0)
        ),
        (0, 0)
    )


if __name__ == '__main__':
    # PyGame setup
    pygame.init()
    pygame.display.set_caption(CAPTION)  # altera o título da janela
    screen = pygame.display.set_mode(SCREEN_SIZE)  # altera o tamanho da janela
    clock = pygame.time.Clock()  # controle da velocidade do jogo
    # objetos
    snake = Snake(INITIAL_POSITION, INITIAL_LENGTH, BLOCK_SIZE, PLAY_SURFACE)
    game = Game()
    # cria um loop que permanece até o status do jogo se alterar (game over)
    while game.running():
        # "limpa" a tela, preenchendo-a com a cor do plano de fundo
        screen.fill(BACKGROUND_COLOR)
        # quadro azul
        pygame.draw.rect(
            screen,
            (179, 119, 0),
                [0, BLOCK_SIZE, SCREEN_SIZE[0], SCREEN_SIZE[1]-BLOCK_SIZE],
                BLOCK_SIZE
        )
        # trata os eventos (interrupção, pressionamento de teclas, etc)
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
                            snake.turn("LEFT")
                            continue
                        case pygame.K_UP:
                            snake.turn("UP")
                            continue
                        case pygame.K_DOWN:
                            snake.turn("DOWN")
                            continue
                        case pygame.K_RIGHT:
                            snake.turn("RIGHT")
                            continue
        # elementos do jogo
        fruit = game.spawn_fruit()
        # _caso aconteça de a fruta não ser gerada, executa o bloco acima
        # _novamente, evitando que dê erro
        if not fruit:
            continue
        draw_scoreboard(game.get_score())
        # _desenha a fruta
        pygame.draw.circle(
            screen,
            FRUIT_COLOR,
            ((fruit[0])+BLOCK_SIZE/2, (fruit[1])+BLOCK_SIZE/2), BLOCK_SIZE//2,
            BLOCK_SIZE//2
        )
        # _desenha a cobra
        for block in snake.get_body():
            pygame.draw.rect(
                screen,
                pygame.Color(30, 200, 0),
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
        #
        if snake.is_colliding():
            game.game_over()
        # atualiza a tela
        pygame.display.flip()
        clock.tick(game.get_fps())
