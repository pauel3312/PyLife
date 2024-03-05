import pygame as pg
import Logic_module as Logics

padding: tuple[int, int] = (1, 1)
cell_size: tuple[int, int] = (20, 20)
total_cell_size: tuple[int, int] = (cell_size[0] + padding[0], cell_size[1] + padding[1])
cell_grid_geometry: tuple[int, int] = (50, 50)
cell_grid_size: tuple[int, int] = (cell_grid_geometry[0] * total_cell_size[0],
                                   cell_grid_geometry[1] * total_cell_size[1])
cell_grid_surface = pg.Surface(cell_grid_size)

MODE_STOPPED = 0
MODE_BUILD = 1
MODE_RUN = 2

COLOR_ON: pg.Color = pg.Color("#00FF00")
COLOR_OFF: pg.Color = pg.Color("#007000")
COLOR_ON_SELECTED: pg.Color = pg.Color("#FF0000")
COLOR_OFF_SELECTED: pg.Color = pg.Color("#700000")

current_mode = MODE_STOPPED


def get_window_size() -> tuple[int, int]:
    return cell_grid_size[0], cell_grid_size[1]  # TODO: add labels when implemented


class GridTile:
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 state: bool = False,
                 selected: bool = False,
                 ):
        self.x: int = x
        self.y: int = y
        self.GUI_x = x*total_cell_size[0]
        self.GUI_y = y*total_cell_size[1]
        self.w: int = w
        self.h: int = h
        self.state: bool = state
        self.selected: bool = selected
        self.color: pg.Color = self.get_color()
        self.box: pg.Rect = pg.draw.rect(cell_grid_surface, self.color, (self.GUI_x, self.GUI_y, w, h))

    def get_color(self) -> pg.Color:
        state = "ON" if self.state else "OFF"
        selection = "_SELECTED" if self.selected else ""
        return eval(f'COLOR_{state}{selection}')

    def hovered(self, end_hover: bool = False):
        self.selected = not end_hover

    def clicked(self):
        self.state = not self.state

    def __bool__(self):
        return self.state

    def __str__(self):
        return f'({self.x}, {self.y})'


def create_tiles(starting_grid: list[list[bool]]) -> list[list[GridTile]]:
    tile_array = []
    for x, line in enumerate(starting_grid):
        tile_array.append([])
        for y, cell in enumerate(line):
            tile_array[x].append(GridTile(x, y, cell_size[0], cell_size[1], starting_grid[x][y]))
    return tile_array


if __name__ == "__main__":
    current_mode = MODE_BUILD
    pg.init()
    pg.display.set_mode(get_window_size())
    table = Logics.empty_table(cell_grid_geometry[0], cell_grid_geometry[1])
    tiles_array = create_tiles(table)

