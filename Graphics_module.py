import time
import tkinter as tk
import Logic_module
import Controls_module_KB

window = tk.Tk()
window.configure(background='#000')
table_frames: list[list[tk.Frame]] = []
pad_x: int
pad_y: int
pad_x = pad_y = 1


cell_height: int
cell_width: int
cell_height = cell_width = 20

COLOR_ON: str = '#00FF00'
COLOR_OFF: str = '#007000'
COLOR_ON_SELECTOR: str = '#FF0000'
COLOR_OFF_SELECTOR: str = '#700000'


def create_tile(x: int, y: int, is_on: bool):
    current_frame: tk.Frame = tk.Frame(window,
                                       background=COLOR_ON if is_on else COLOR_OFF,
                                       width=cell_width,
                                       height=cell_height
                                       )
    current_frame.pack_propagate(False)
    table_frames[x].append(current_frame)
    current_frame.grid(column=x, row=y, padx=pad_x, pady=pad_y)


def create_grid(table: list[list[bool]]):
    for x, column in enumerate(table):
        table_frames.append([])
        for y, cell in enumerate(column):
            create_tile(x, y, cell)


def update_tile(x: int, y: int, is_on: bool):
    current_frame = table_frames[x][y]
    current_frame['background'] = COLOR_ON if is_on else COLOR_OFF


def update_grid(table: list[list[bool]], update: bool = True):
    for x, column in enumerate(table):
        for y, cell in enumerate(column):
            try:
                update_tile(x, y, cell)
            except IndexError:
                raise Exception("Table size is inconsistent.")
    if update:
        window.update()


# TODO: do the legend (population, generation and mode)

def run_loop(table: list[list[bool]]):
    controls = Controls_module_KB.keys_to_API('RUN')
    auto_run = False
    gen = 0
    while 'quit' not in controls:
        if auto_run:
            table, gen, pop = Logic_module.life_step(table, gen)
            update_grid(table)
        elif 'step' in controls:
            table, gen, pop = Logic_module.life_step(table, gen)
            update_grid(table)
        if 'autorun' in controls:
            auto_run = not auto_run
            time.sleep(.2)
        if 'change_mode' in controls:
            edit_loop(table)
        controls = Controls_module_KB.keys_to_API('RUN')


def edit_loop(table: list[list[bool]]):
    controls = Controls_module_KB.keys_to_API('EDIT')
    selector = [0, 0]
    while 'quit' not in controls:
        for key in controls:
            match key:
                case 'up': selector[1] -= 1
                case 'left': selector[0] -= 1
                case 'down': selector[1] += 1
                case 'right': selector[0] += 1
                case 'change':
                    table[selector[0]][selector[1]] = not table[selector[0]][selector[1]]
                case 'change_mode': run_loop(table)
        controls = Controls_module_KB.keys_to_API('EDIT')
        update_grid(table, False)
        draw_selector(selector, table[selector[0]][selector[1]])
        window.update()


def draw_selector(selector: list[int], is_on: bool):
    x, y = selector
    current_frame = table_frames[x][y]
    current_frame['background'] = COLOR_ON_SELECTOR if is_on else COLOR_OFF_SELECTOR


if __name__ == "__main__":
    create_grid(Logic_module.empty_table(40, 40))
    edit_loop(Logic_module.empty_table(40, 40))

    window.mainloop()
