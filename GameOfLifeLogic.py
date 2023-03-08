import controlsAPI


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
    def __init__(self, width, length, table=None):
        self._table = empty_table(width, length) if table is None else table
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

    def get_table(self):
        return self._table

    def set_table(self, a):
        print("WARNING: Table not default")
        self._table = a

    def del_table(self):
        del self._table
        del self

    def exit_to_run_mode(self):
        return RunnerTable(self._table)

    table = property(get_table, set_table, del_table)

    def edit_loop(self, draw_callback=None):
        command_calls_mode_edit: set = controlsAPI.keys_to_API('EDIT')
        while 'quit' not in command_calls_mode_edit:
            if 'up' in command_calls_mode_edit:
                self.move_up()
            if 'left' in command_calls_mode_edit:
                self.move_left()
            if 'down' in command_calls_mode_edit:
                self.move_down()
            if 'right' in command_calls_mode_edit:
                self.move_right()
            if 'change' in command_calls_mode_edit:
                self.change_state()
            if 'change_mode' in command_calls_mode_edit:
                RunnerTable(table=self._table, draw_function=draw_callback).main_loop()
            if draw_callback is not None:
                draw_callback(self.table)


class RunnerTable:
    def __init__(self, table, draw_function=None):
        self._table = table
        self.generation = 0
        self.population = get_population(self._table)
        self.draw_function = draw_function

    def step(self):
        self._table, self.generation, self.population = life_step(self._table, self.generation)
        if self.draw_function is not None:
            self.draw_function(self)

    def autorun(self):
        while 'autorun' not in controlsAPI.keys_to_API('RUN'):
            self.step()

    def main_loop(self):
        commands = controlsAPI.keys_to_API('RUN')
        while 'quit' not in commands:
            for key in commands:
                match key:
                    case 'autorun': self.autorun()
                    case 'step': self.step()
                    case 'change_mode': SelectorTable(0, 0, table=self._table)\
                        .edit_loop(draw_callback=self.draw_function)


if __name__ == '__main__':
    print(life_step([[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]], 0))
