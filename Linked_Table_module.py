from typing import Optional
from functools import partial


class LinkedTableNode:
    def __init__(self, state: bool = False, hooked: Optional[set["LinkedTableNode"]] = None) -> None:
        self.hooked: set["LinkedTableNode"] = set()
        if hooked is not None and len(hooked) <= 8:
            for node in hooked:
                node.hook(self)
        elif hooked is not None:
            raise ValueError("The set of hooked nodes is too large")
        self.state: bool = state

    def hook(self, new: "LinkedTableNode") -> None:
        self.hooked.add(new)
        new.hooked.add(self)

    def __int__(self):
        return len(self.hooked)


class LinkedTableCoordSystem:
    def __init__(self,
                 origin: LinkedTableNode,
                 up: LinkedTableNode,
                 left: LinkedTableNode):
        self.up: LinkedTableNode = up
        self.left: LinkedTableNode = left
        self.origin: LinkedTableNode = origin

    def __getitem__(self, coordinates: tuple[int]) -> LinkedTableNode:
        pass  # TODO coordinate getter system


def create_even_base() -> set[LinkedTableNode]:
    base_tiles = []
    for i in range(4):
        base_tiles.append(LinkedTableNode())
    for i in range(1, 4):
        base_tiles[0].hook(base_tiles[i])
    for i in (1, 2):
        base_tiles[3].hook(base_tiles[i])
    base_tiles[1].hook(base_tiles[2])
    return set(base_tiles)


def create_odd_base() -> set[LinkedTableNode]:
    edges = []
    corners = []
    for i in range(4):
        current_edge = LinkedTableNode()
        current_corner = LinkedTableNode()
        current_corner.hook(current_edge)
        if i > 0:
            current_edge.hook(corners[i - 1])
            current_edge.hook(edges[i-1])
        if i == 3:
            current_corner.hook(edges[0])
            current_edge.hook(edges[0])
        edges.append(current_edge)
        corners.append(current_corner)
    surroundings: set[LinkedTableNode] = set(edges).union(set(corners))
    center = LinkedTableNode(hooked=surroundings)
    surroundings.add(center)
    return surroundings


def create_square(side_length: int) -> tuple[LinkedTableCoordSystem, set[LinkedTableNode]]:
    if side_length % 2 == 0:
        base: set[LinkedTableNode] = create_even_base()
        origin: LinkedTableNode = next(iter(base))  # select an element from the base set
        up: LinkedTableNode = next(iter(origin.hooked))
        left: LinkedTableNode = next(iter(origin.hooked.intersection(up.hooked)))
        side_length -= 2

    else:
        base: set[LinkedTableNode] = create_odd_base()
        edges: set[LinkedTableNode] = set()
        for node in base:
            match int(node):
                case 8:
                    origin: LinkedTableNode = node
                case 5:
                    edges.add(node)
        up: LinkedTableNode = next(iter(edges))
        left: LinkedTableNode = next(iter(edges.intersection(up.hooked)))
        side_length -= 3

    while side_length > 0:
        expand(base)
        side_length -= 2

    # TODO Link edges

    return LinkedTableCoordSystem(origin, up, left), base


def expand(base: set[LinkedTableNode]) -> set[LinkedTableNode]:
    # TODO fix even base bug
    corners: set[LinkedTableNode] = set()
    edges_to_do = set()
    for potential_corner in base:
        if int(potential_corner) == 3:
            corners.add(potential_corner)
            potential_corner.hook(LinkedTableNode())
            for potential_edge in potential_corner.hooked:
                if int(potential_edge) == 5:
                    edges_to_do.add(potential_edge)

    if len(corners) != 4:
        raise ValueError('Invalid input base: does not have 4 corners.')

    edges_done = set()
    hooks_to_do: set[tuple[LinkedTableNode, LinkedTableNode]] = set()
    while len(edges_to_do) != 0:
        current_edge = next(iter(edges_to_do))
        edges_to_do.remove(current_edge)
        edges_done.add(current_edge)
        adjacent_edges = set()
        for potential_edge in current_edge.hooked:
            if int(potential_edge) >= 5:
                adjacent_edges.add(potential_edge)
                if potential_edge not in edges_done:
                    edges_to_do.add(potential_edge)
            new_edge = LinkedTableNode(hooked=adjacent_edges)
            hooks_to_do.add((new_edge, current_edge))
            edges_done.add(new_edge)
            base.add(new_edge)
    for htd in hooks_to_do:
        htd[0].hook(htd[1])
    return base


if __name__ == "__main__":
    a = create_odd_base()
    print(len(a))
    b = expand(a)
    print(len(a), len(b))
