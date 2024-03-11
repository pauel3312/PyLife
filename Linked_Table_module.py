from typing import Optional


class LinkedTableNode:
    def __init__(self, state: bool = False, hooked: Optional[set["LinkedTableNode"]] = None) -> None:
        if hooked is None:
            self.hooked: set["LinkedTableNode"] = set()
        elif len(hooked) <= 8:
            self.hooked: set["LinkedTableNode"] = hooked
        else:
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

    def __getitem__(self, item: tuple[int] | slice) -> LinkedTableNode:
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
        if i == 3:
            current_corner.hook(edges[0])
    surroundings: set[LinkedTableNode] = set(edges).union(set(corners))
    center = LinkedTableNode(hooked=surroundings)
    surroundings.add(center)
    return surroundings


def create_square(side_length: int) -> LinkedTableCoordSystem:
    if side_length % 2 == 0:
        base: set[LinkedTableNode] = create_even_base()
        origin: LinkedTableNode = next(iter(base))  # select an element from the base set
        up: LinkedTableNode = next(iter(origin.hooked))
        left: LinkedTableNode = next(iter(origin.hooked.intersection(up.hooked)))
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

    # TODO expand the base
    return LinkedTableCoordSystem(origin, up, left)


if __name__ == "__main__":
    pass
