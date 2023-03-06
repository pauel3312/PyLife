commands_calls = {'quit': False, 'up': False,  'left': False,  'down': False,  'right': False,  'change': False, }


def empty_table(width, length):
    return [[False] * width] * length


def get_number_of_live_neighbours(coordinates: tuple, table):
    length = len(table)
    width = len(table[0])
    x, y = coordinates
    number_of_live_neighbours = 0
    for x_offset in (-1, 0, 1):
        for y_offset in (-1, 0, 1):
            if table[(x+x_offset) % length][(y+y_offset) % width] and (0, 0) != (x_offset, y_offset):
                number_of_live_neighbours += 1
    return number_of_live_neighbours


def get_population(table):
    population_counter = 0
    for line in table:
        for cell in line:
            if cell:
                population_counter += 1
    return population_counter


def life_step(table, generation, rule=((3,), (2, 3))):
    new_table = []
    for x, line in enumerate(table):
        new_table.append([])
        for y, value in enumerate(line):
            number_of_live_neighbours = get_number_of_live_neighbours((x, y), table)
            if not value and number_of_live_neighbours in rule[0]:
                new_table[x].append(True)
            elif value and number_of_live_neighbours not in rule[1]:
                new_table[x].append(False)
            else:
                new_table[x].append(value)
    return new_table, generation + 1, get_population(new_table)


class SelectorTable:
    def __init__(self, width, length):
        self._table = empty_table(width, length)
        self.position = [0, 0]

    def move_up(self):
        self.position[1] -= 1

    def move_left(self):
        self.position[0] -= 1

    def move_down(self):
        self.position[1] += 1

    def move_right(self):
        self.position[0] += 1

    def change_state(self):
        self._table[self.position[0]][self.position[1]] = not self._table[self.position[0]][self.position[1]]

    # function to get value of _age
    def get_table(self):
        return self._table

    # function to set value of _age
    def set_table(self, a):
        print("WARNING: Table not default")
        self._table = a

    # function to delete _age attribute
    def del_table(self):
        del self._table
        del self

    table = property(get_table, set_table, del_table)

    def edit_loop(self, draw_callback=None):
        global commands_calls
        while not commands_calls['quit']:
            if commands_calls['up']:
                self.move_up()
            if commands_calls['left']:
                self.move_left()
            if commands_calls['down']:
                self.move_down()
            if commands_calls['right']:
                self.move_right()
            if commands_calls['change']:
                self.change_state()
            if draw_callback is not None:
                draw_callback(self.table)


if __name__ == '__main__':
    print(life_step([[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]], 0))
