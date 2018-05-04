import os
import json


class _Dir:
    LEFT = 0
    LEFT_UP = 1
    UP = 2
    RIGHT_UP = 3


class Field:
    """
    Game class. 2 - nothing, 0 - zero, 1 - cross
    """
    def __init__(self, n, size=-1):
        """
        Constructor
        :param n: The size of the field
        :param size: size of the chain to win the game
        """
        self._size = n
        self._field = [2] * n * n
        self._current_player = 1
        if size == -1 or size > n:
            self._size_to_win = n
        else:
            self._size_to_win = size

    def print(self):
        """
        This function prints current field state
        :return: None
        """
        print(('+' + '-' * (len(str(self._size ** 2 - 1)))) * self._size, end='')
        print('+')
        for i in range(self._size):
            for j in range(self._size):
                char = Field._get_char(self._field[i * self._size +  j],
                                              i * self._size + j)
                print('|%s' % char + ' ' *
                      (len(str(self._size ** 2)) - len(str(char)) - 1),
                      end='')
            print('|')
            print(('+' + '-' * (len(str(self._size ** 2 - 1)))) * self._size,
                  end='')
            print('+')


    def is_win(self):
        """
        This function check if someone has won this battle and shows who.
        :return: bool
        """
        if self._check_winning(1):
            os.system('clear')
            print('The cross is winner!')
            self.print()
            return True
        elif self._check_winning(0):
            os.system('clear')
            print('The zero is winner!')
            self.print()
            return True
        elif not self._can_continue():
            os.system('clear')
            print('Nobody is winner!')
            self.print()
            return True

        return False

    def _can_continue(self):
        """
        This function checks the conditions for continuing the game, like free
        space on the field
        :return: bool
        """
        for i in range(self._size):
            for j in range(self._size):
                if self._field[i * self._size + j] == 2:
                    return True

        return False


    @staticmethod
    def _get_char(num, val):
        """
        This function gets the output character according to the number
        :return: String (single character)
        """
        return val if num == 2 else 'X' if num == 1 else 'O' if num == 0 else '*'


    def _check_winning(self, val):
        """
        This function checks is this player is winner
        :param val: player (it's mark on the field)
        :return: bool
        """
        for i in range(self._size):
            for j in range(self._size):
                if self._check_all_cell(i * self._size + j,
                                        val):
                    return True

        return False


    def _check_all_cell(self, n, val):
        """
        This function checks is current cell placed on the winning position for
        selected player
        :param n: The cell's index
        :param val: Current player's mark
        :return: bool
        """
        i, j = self._find_start(n, val, _Dir.LEFT)
        is_check, counter = False, 0
        while j < self._size and self._field[i * self._size + j] == val:
            counter += 1
            j += 1

        if counter >= self._size_to_win:
            return True

        i, j = self._find_start(n, val, _Dir.UP)
        is_check, counter = False, 0
        while i < self._size and self._field[i * self._size + j] == val:
            counter += 1
            i += 1

        if counter >= self._size_to_win:
            return True

        i, j = self._find_start(n, val, _Dir.LEFT_UP)
        is_check, counter = False, 0
        while (j < self._size and i < self._size and
               self._field[i * self._size + j] == val):
            counter += 1
            j += 1
            i += 1

        if counter >= self._size_to_win:
            return True

        i, j = self._find_start(n, val, _Dir.RIGHT_UP)
        is_check, counter = False, 0
        while (j >= 0 and i < self._size and
               self._field[i * self._size + j] == val):
            counter += 1
            j -= 1
            i += 1

        if counter >= self._size_to_win:
            return True

        return False


    def _find_start(self, n, val, dir):
        """
        This function returns the coordinates of start counter
        :param n: start cell
        :param val: value to check
        :param dir: direction:
        0 - left,
        1 - left up,
        2 - up,
        3 - right up
        :return: Tuple of coordinates
        """
        i, j = n // self._size, n % self._size
        if dir == 0:
            while j > 0 and self._field[i * self._size + j - 1] == val:
                j -= 1

            return (i, j)

        elif dir == 1:
            while i > 0 and j > 0 and \
                    self._field[(i - 1)* self._size + j - 1] == val:
                i -= 1
                j -= 1

            return (i, j)

        elif dir == 2:
            while i > 0 and self._field[(i - 1) * self._size + j] == val:
                i -= 1

            return (i, j)

        elif dir == 3:
            while i > 0 and j < self._size - 1 and \
                   self._field[(i - 1) * self._size + j + 1] == val:
                i -= 1
                j += 1

            return (i, j)


    def make_turn(self, n):
        """
        This function set the mark according to the current player or saying to
        remake turn because of some validation errors
        :param n: number of field
        :return: None
        """
        try:
            if n < 0 or n > self._size ** 2 or self._field[n] != 2:
                raise ValueError('invalid number')

            self._field[n] = self._current_player
            self._current_player ^= 1

        except ValueError:
            print('Remake your turn')



    @property
    def current_player(self):
        return self._current_player


    def return_field_json(self):
        return json.dumps(self._field)


    def load_field(self, field, win_param, current_player):
        self._field = json.loads(field)
        self._size_to_win = win_param
        self._size = int(len(self._field) ** (0.5))
        self._current_player = current_player