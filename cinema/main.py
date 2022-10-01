#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Imports
from hashlib import md5
from operator import itemgetter
import re
import sys
import os


# Códigos ANSI
BLACK_FG = '\033[1;30m'
BLUE_FG = '\033[1;34m'
CYAN_FG = '\033[1;36m'
GREEN_FG = '\033[1;32m'
RED_FG = '\033[1;31m'
WHITE_FG = '\033[1;37m'
YELLOW_FG = '\033[1;33m'
YELLOW_UL = '\033[4;33m'
WHITE_BG = '\033[47m'
RESET = '\033[0m'

# Artes ASCII
BANNER_ART = f'''{CYAN_FG}  _____ _
 / ____(_)                        /\\
| |     _ _ __   ___ _ __ ___    /  \\   _ __  _ __
| |    | | '_ \\ / _ \\ '_ ` _ \\  / /\\ \\ | '_ \\| '_ \\
| |____| | | | |  __/ | | | | |/ ____ \\| |_) | |_) |
 \\_____|_|_| |_|\\___|_| |_| |_/_/    \\_\\ .__/| .__/
                                       | |   | |
                                       |_|   |_|{RESET}'''
CHAIR_ART = f'''{BLUE_FG}        .............
      .'             '.
     : '.           .' :
     :  :           :  :
     :  :           :  :
     :  :           :  :
     :  :           :  :
    .'  :           :  '.
 _.'    lc..........:    '._
(     .'             '.     )
 '._.'                 '._.'
   (.....................)
    \\___________________/
     (. . . . . . . . .)
      \\  /_/     \\_\\  /
       ||           ||
       )|           |(
      (_/           \\_){RESET}
'''


# Type hinting
ChairHint = list[str, int]
TicketHint = tuple[int, ChairHint]


# Funções auxiliares
def warn(message: str) -> str:
    return f'{BLUE_FG}[{RED_FG}!{BLUE_FG}]{RESET} {message}'


def question(message: str) -> str:
    return f'{BLUE_FG}[{YELLOW_FG}*{BLUE_FG}]{RESET} {message}'


def info(message: str) -> str:
    return f'{BLUE_FG}[{WHITE_FG}%{BLUE_FG}]{RESET} {message}'


def option(index: int, title: str) -> str:
    return f'{BLUE_FG}[{YELLOW_FG}{index}{BLUE_FG}]{RESET} {title}'


def title(*path: tuple[str]) -> str:
    return '/'.join(
        (f'{BLACK_FG}{WHITE_BG}{directory}{RESET}' for directory in path)
    )


def chair_icon(position: int, status=True) -> str:
    return (
        f'{YELLOW_UL}{RED_FG}[{position:02d}]{RESET}' if status
        else f'{YELLOW_UL}{GREEN_FG}[{position:02d}]{RESET}'
    )


def list_item(label) -> str:
    return (
        f'{YELLOW_FG}[{WHITE_FG}-{RESET}{YELLOW_FG}]{RESET} {label}'
    )


def get_chair(coordinates: tuple[int, int]):
    row, position = coordinates
    return room[row][1][position]


def get_chair_coordinates(coordinates: ChairHint):
    # Percorre a "sala" em busca de localizar a poltrona através do caractere
    # que corresponde à fileira e sua posição na coluna
    for row_index, (row, column) in enumerate(room):
        for chair_position, chair in enumerate(column):
            if (row, chair_position) == coordinates:
                return (row_index, chair_position)


def full_chairs():
    return [chair for _, column in room for chair in column if chair]


def check_CPF(cpf: str) -> str:
    return re.match(r'\d{3}\.\d{3}\.\d{3}-\d{1,2}', cpf)


def check_CGM(cgm: str) -> str:
    return re.match(r'\d+', cgm)


# Lógica
# _Valor do ingresso
TICKET_VALUE = 20.00
# _Armazena o número total de cadeiras
TOTAL_ENTRIES = 0
# _Armazena o número de meia-entradas fornecidas
HALF_ENTRIES = 0
# _Limite de meia-entradas
HALF_ENTRY_LIMIT = 40


# Gera uma matriz contendo a estrutura da sala, como:
'''
[
    ('A', [0, 0, 0...]),
    ('B', [0, 0, 0...]),
    ('C', [0, 0, 0...]),
    ...
]
'''


def room() -> list:
    room = []
    global TOTAL_ENTRIES
    for row in ['A', 'B', 'C']:
        room.append((row, [0]*15))
    for row in ['D', 'E']:
        room.append((row, [0]*20))
    for row in ['F', 'G', 'H', 'I', 'J']:
        room.append((row, [0]*27))
    # Inicializa a variável TOTAL_ENTRIES com o número total de poltronas
    # disponíveis
    TOTAL_ENTRIES = sum([column.count(0) for row, column in room])
    return room


def chair_suggestion(room: list[ChairHint],
                     chosen: ChairHint) -> ChairHint:
    row, column, chair = [
        (row, column, index) for row, column in
        room for index, chair in enumerate(column)
        if (row, index) == chosen
    ][0]
    # Busca todas as cadeiras disponíveis na fileira informada pelo usuário
    empty = [
        (row, index) for row, column in room
        for index, chair in enumerate(column)
        if (row == chosen[0] and not chair)
    ]
    # Verifica se há alguma cadeira disponível na fileira informada
    if len(empty) > 0:
        # Se houver, busca por todas as cadeiras e encontra a distância que há
        # entre ela e a cadeira informada
        closest = [
            (
                index, (chair-index if chair-index > 0 else index-chair)
            ) for _, index in empty if index != chair
        ]
        # Ordena da mais mais próxima à mais distante
        closest.sort(key=itemgetter(1))
        # Retorna a mais próxima
        return row, closest[0][0]
    else:
        # Caso não haja nenhuma cadeira disponível, utiliza-se o método de
        # recursão, desta vez passando como argumento para a função a próxima
        # fileira (ou a anterior no caso de a próxima fileira ser a última da
        # sala) e a cadeira informada
        row_index = [index for index, (r, _) in enumerate(room) if r == row][0]
        return chair_suggestion(
            room,
            (
                (
                    room[row_index+1][0]
                    if row_index+1 <= len(room) else room[row_index-1][0]
                ),
                chair
            )
        )
    return


def check_ticket(room: list[ChairHint],
                 position: ChairHint,
                 half=False) -> bool:
    position = get_chair_coordinates(position)
    # Verifica se a poltrona escolhida está vazia
    if get_chair(position):
        return 1
    # Verifica se o desejado é uma meia-entrada
    if half:
        # Verifica a disponibilidade de ingressos de meia-entrada
        if 100*HALF_ENTRIES/TOTAL_ENTRIES >= HALF_ENTRY_LIMIT:
            # Caso tenha ultrapassado o limite de meia-entradas,
            # retorne o código de erro "1"
            return 2
        return False
    return False


def buy_ticket(room: list[ChairHint],
               position: ChairHint,
               half=False) -> TicketHint:
    global HALF_ENTRIES
    coordinates = get_chair_coordinates(position)
    row, chair = coordinates
    # Verifica se o desejado é uma meia-entrada
    if half:
        room[row][1][chair] = TICKET_VALUE/2
        HALF_ENTRIES += 1
    else:
        room[row][1][chair] = TICKET_VALUE
    return (
        f'{room[row][0]}{chair+1}',
        f'{get_chair(coordinates):5.2f} reais'
    )
    return False


def auth(username: str, password: str) -> bool:
    return (
        md5(
            username.encode()
        ).hexdigest() == '1d0258c2440a8d19e716292b231e3190' and
        md5(
            password.encode()
        ).hexdigest() == '07477dc8fc9c370ad440fe3ff46e140f'
    )


# Interface
# _Estrutura dos menus
START_MENU = (
    'Comprar ingresso',
    'Acessar relatório (área restrita!)',
    'Sair'
)
HALF_ENTRY = (
    'Sim, sou menor que 12 anos ou maior que 60 anos',
    'Sim, sou estudante',
    'Não'
)
# _Títulos
HOME_TITLE = 'Cinema', 'Menu'
BUY_TICKET_TITLE = 'Cinema', 'Menu', 'Comprar Ingresso'
REPORT_TITLE = 'Cinema', 'Menu', 'Relatório'
HALF_ENTRY_TITLE = 'Cinema', 'Menu', 'Comprar Ingresso', 'Tipo'
HALF_ENTRY_CPF_TITLE = 'Cinema', 'Menu', 'Comprar Ingresso', 'Tipo', 'Idade'
HALF_ENTRY_CGM_TITLE = (
    'Cinema', 'Menu', 'Comprar Ingresso', 'Tipo', 'Estudante'
)
TICKET_BOUGHT_TITLE = 'Cinema', 'Menu', 'Ingresso'


def ticket_menu(room: list[ChairHint]):
    print(title(*BUY_TICKET_TITLE))
    # Exibe uma representação abstrata da sala de cinema
    print(*(
        '|'.join(
            (
                row,
                *(
                    chair_icon(index+1, chair)
                    for index, chair in enumerate(column)
                ), row
            )
        ) for row, column in reversed(room)),
        sep='\n'
    )
    row = input(question('Escolha uma fileira (ex: D): ')).upper()
    chair = input(question('Escolha uma poltrona (ex: 7): '))
    # Transforma a variável chair numa variável do tipo inteiro caso ela
    # corresponda à string de um número
    chair = int(chair) if chair.isdigit() else chair
    # Verifica se o usuário informou corretamente uma poltrona válida
    if get_chair_coordinates((row, chair)):
        position = row, int(chair)-1
        print(title(*HALF_ENTRY_TITLE))
        print(question('Possui um benefício de meia-entrada?'))
        print('\n'.join([
            option(index+1, operation)
            for index, operation in enumerate(HALF_ENTRY)])
        )
        half_entry = input(question('Selecione uma opção: '))
        half_entry = int(half_entry)-1 if half_entry.isdigit() else half_entry
        if half_entry in range(len(HALF_ENTRY)):
            if half_entry == 0:
                print(title(*HALF_ENTRY_CPF_TITLE))
                for attempt in range(1, 3+1):
                    half_entry = False
                    document = input(
                        question('Informe seu CPF(000.000.000-00): ')
                    )
                    if document:
                        if check_CPF(document):
                            print(info('Aprovado!'))
                            half_entry = True
                            break
                        print(warn(f'Erro! Tente novamente ({attempt}/3)'))
                if not half_entry:
                    print(warn('Não foi possível a validação!'))
            elif half_entry == 1:
                print(title(*HALF_ENTRY_CGM_TITLE))
                for attempt in range(1, 3+1):
                    half_entry = False
                    document = input(
                        question('Informe o seu CGM: ')
                    )
                    if check_CGM(document):
                        print(info('Aprovado!'))
                        half_entry = True
                        break
                    print(warn(f'Erro! Tente novamente ({attempt}/3)'))
                if not half_entry:
                    print(warn('Não foi possível a validação!'))
            else:
                half_entry = False
        else:
            print(
                warn(
                    'Opção inválida, prosseguindo sem o benefício da '
                    'meia-entrada'
                )
            )
            half_entry = False
        ticket = check_ticket(room, position, half_entry)
        if ticket == 1:
            suggestion = chair_suggestion(room, position)
            print(
                warn(
                    f'A poltrona {row}{chair} não está disponível, sugerimos '
                    f'a poltrona '
                    f'{"".join((suggestion[0], str(suggestion[1]+1)))}.'
                )
            )
            proceed = input(
                question(
                    'Deseja continuar? (S - Sim, N - Não)\n'
                )
            ).upper()
            if proceed == 'S':
                position = suggestion
            elif proceed == 'N':
                return
        elif ticket == 2:
            print(
                warn(
                    'Ingressos de meia-entrada não estão mais disponíveis!')
            )
            proceed = input(
                question(
                    'Deseja continuar? (S - Sim, N - Não)\n'
                )
            ).upper()
            if proceed == 'S':
                half_entry = False
            elif proceed == 'N':
                return
        ticket = buy_ticket(room, position, half_entry)
        print(
            title(*TICKET_BOUGHT_TITLE),
            CHAIR_ART,
            info(
                f'Poltrona {ticket[0]} reservada no valor de {ticket[1]}.'
            ),
            sep='\n'
        )
    else:
        print(warn('Poltrona inválida!'))
    input(question('Pressione ENTER para retornar ao menu'))
    return


def report(room: list[ChairHint]):
    print(title(*REPORT_TITLE))
    if auth(
        input(question('Informe seu nome de usuário: ')),
        input(question('Informe sua senha: '))
    ):
        print(
            info('Quantidade total de assentos vendidos: '),
            sum([1 for _ in full_chairs()])
        )
        print(
            info('Quantidade total de ingressos de meia-entrada vendidos: '),
            sum([1 for value in full_chairs() if value == TICKET_VALUE/2])
        )
        print(
            info('Quantidade total de ingressos convencionais vendidos: '),
            sum([1 for value in full_chairs() if value == TICKET_VALUE])
        )
        print(
            info('Valor total faturado: '),
            sum([value for value in full_chairs()])
        )
        print(
            info('Valor total faturado em ingresso de meia-entrada: '),
            sum([value for value in full_chairs() if value == TICKET_VALUE/2])
        )
        print(
            info('Valor total faturado em ingresso convencionais: '),
            sum([value for value in full_chairs() if value == TICKET_VALUE])
        )
        percentage = sorted((
            (row,
             '{:2.2f}%'.format(
                 100*sum([1 for _ in full_chairs()])/len(column))
             ) for row, column in room
            if sum(column) > 0
        ),
            key=itemgetter(1),
            reverse=True
        )[:3]
        print(
            info('Fileiras com a maior porcentagem de assentos ocupados'),
            '\n'.join([list_item(' - '.join(item)) for item in percentage]),
            sep='\n'
        )
        percentage = sorted(
            (
                (row, '{:2.2f}%'.format(
                    100*sum([1 for _ in full_chairs()])/len(column)
                )) for row, column in room
                if sum(column) > 0
            ),
            key=itemgetter(1)
        )[:3]
        print(
            info('Fileiras com a menor porcentagem de assentos ocupados'),
            '\n'.join([list_item(' - '.join(item)) for item in percentage]),
            sep='\n'
        )
        input(question('Pressione ENTER para retornar ao menu'))
    else:
        print(warn('Acesso negado!'))


def quit():
    confirm = input(
        question('Tem certeza de que quer sair? (S - Sim, N - Não)\n')
    ).upper()
    if confirm == 'S':
        print(info('Saindo...'))
        sys.exit()
    return


def start_menu(room: list[ChairHint]):
    print(title(*HOME_TITLE))
    print(*(
        option(index+1, operation) for index, operation
        in enumerate(START_MENU)),
        sep='\n'
    )
    operation = input(question('Informe uma operação: '))
    operation = int(operation)-1 if operation.isdigit() else operation
    # Confere se a entrada corresponde à uma opção válida
    if operation not in range(len(START_MENU)):
        input(warn('Operação inválida! Pressione ENTER para continuar'))
        return
    if operation == 0:
        ticket_menu(room)
    elif operation == 1:
        report(room)
    elif operation == 2:
        quit()


if __name__ == '__main__':
    room = room()
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print(BANNER_ART)
        start_menu(room)
