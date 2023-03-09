def empty_table(width, length):
    empty_width_list = [False] * width
    table = []
    for i in range(length):
        table.append(empty_width_list.copy())
    return table


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


if __name__ == '__main__':
    print(life_step([[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]], 0))
