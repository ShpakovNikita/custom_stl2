from field import  Field as SuperField
from field_adapter import *
from types import *
import os


GLOBAL_UID = None
CONNECTION_PORT = None
PLAYER_NO = [None]


def not_main():
    new_game = SuperField(3)
    q = False
    while not q:
        new_game.print()

        os.system('clear')
        new_game.make_turn(int(input('type number, player %s: '
                                     % new_game.current_player)))
        if new_game.is_win():
            cond = input('type [y] to play again')
            if not cond.upper() == 'Y':
                q = True
            else:
                new_game = SuperField(3)


def int_input():
    while True:
        try:
            return int(input('input number'))
        except:
            print('retype number')


def game_actions(query):
    print_field(GLOBAL_UID)
    while True:
        char = input('type [y] to end session. \n'
                     'type num to see make_turn. \n'
                     'type [u] to update (not to do anything) \n')
        os.system('clear')
        if char.lower() == 'u':
            pass
        elif char.lower() == 'y':
            print('Leaving the game')
            del query[-1]
            return
        else:
            try:
                cell = int(char)
            except:
                print('retype number')
                cell = int_input()

            make_turn(cell, PLAYER_NO, GLOBAL_UID)

        print_field(GLOBAL_UID)


def menu(query):
    char = input('type [y] to end session. \n'
                 'type [s] to see players. \n'
                 'type pid to request.     \n'
                 'type [l] to see requests.\n'
                 'type anything to update  \n')
    os.system('clear')
    if char.lower() == 'y':
        return True

    elif char.lower() == 's':
        print('You are %s' % GLOBAL_UID)
        see_players()

    elif char.lower() == 'l':
        see_requests(GLOBAL_UID)
        pass

    else:
        try:
            char = int(char)
            send_request(GLOBAL_UID, char)

        except:
            pass

    global CONNECTION_PORT
    global PLAYER_NO
    CONNECTION_PORT = check_for_connection(GLOBAL_UID, PLAYER_NO)
    if CONNECTION_PORT != 0:
        query.append(game_actions)

    return False


def main():
    q = False
    global GLOBAL_UID
    GLOBAL_UID = start_session()
    query = [menu]
    while not q:
        try:
            q = query[-1](query)
        except:
            end_session(GLOBAL_UID)
            raise KeyboardInterrupt()

    end_session(GLOBAL_UID)


if __name__ == '__main__':
    not_main()
