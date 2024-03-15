from typing import Optional


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
        right: LinkedTableNode = next(iter(origin.hooked.intersection(up.hooked)))
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
        right: LinkedTableNode = next(iter(edges.intersection(up.hooked)))
        side_length -= 3

    while side_length > 0:
        expand(base)
        side_length -= 2

    # TODO Link edges

    return LinkedTableCoordSystem(origin, up, right), base


def expand_corner(corner: LinkedTableNode) -> set[LinkedTableNode]:
    new_corner = LinkedTableNode()
    new_edge_0 = LinkedTableNode()
    new_edge_1 = LinkedTableNode()

    edges_to_hook: list[LinkedTableNode] = []
    for potential_edge in corner.hooked:
        if int(potential_edge) == 5:
            edges_to_hook.append(potential_edge)

    new_corner.hook(corner)
    new_corner.hook(new_edge_0)
    new_corner.hook(new_edge_1)
    new_edge_0.hook(corner)
    new_edge_1.hook(corner)
    new_edge_0.hook(edges_to_hook[0])
    new_edge_1.hook(edges_to_hook[1])
    return set(edges_to_hook)


def expand_along(edge: LinkedTableNode) -> Optional[LinkedTableNode]:
    node_under_current: Optional[LinkedTableNode] = None
    node_under_next: Optional[LinkedTableNode] = None
    for node in edge.hooked:
        if int(node) == 7:
            if node_under_current is not None:
                raise ValueError("base structure invalid: too many 7-neighbour adjacencies")
            node_under_current = node
        if int(node) == 6:
            if node_under_next is not None:
                raise ValueError("base structure invalid: too many 6-neighbour adjacencies")
            node_under_next = node
        if node_under_next is not None and node_under_current is not None:
            break

    node_after_next: Optional[LinkedTableNode] = None
    for node in node_under_next.hooked:
        if int(node) == 5:
            node_after_next = node
            break
    if node_after_next is None:
        for node in node_under_next.hooked:
            if int(node) == 6:
                node_after_next = node
                break
        else:
            raise ValueError("Invalid links in base table.")

        node_under_other_end: Optional[LinkedTableNode] = None
        node_other_end: Optional[LinkedTableNode] = None
        for node in node_after_next.hooked:
            if int(node) == 7:
                node_under_other_end = node
            if int(node) == 4:
                node_other_end = node
            if node_under_other_end is not None and node_other_end is not None:
                break
        else:
            raise ValueError("Invalid links in base table")

        adjacent_node = LinkedTableNode(hooked={node_under_current,
                                                node_under_next,
                                                node_after_next,
                                                edge})
        closing_node = LinkedTableNode(hooked={node_under_next,
                                               node_after_next,
                                               node_under_other_end,
                                               node_other_end,
                                               adjacent_node})
        return None
    else:
        return LinkedTableNode(hooked={edge, node_under_current, node_under_next, node_after_next})


def expand(base: set[LinkedTableNode]) -> set[LinkedTableNode]:
    # TODO fix even base bug/corner bug
    start_corner: LinkedTableNode
    for potential_corner in base:
        if int(potential_corner) == 3:
            start_corner = potential_corner
            break
    try:
        new_corner = LinkedTableNode(hooked={start_corner})
    except NameError:
        raise ValueError("Provided base is invalid: has no corners.")

    next_edge: LinkedTableNode
    for potential_next_edge in start_corner.hooked:
        if int(potential_next_edge) == 5:
            next_edge = potential_next_edge
            break
    pass  # TODO


"""        if int(potential_corner) == 3:
            corners.add(potential_corner)
            new_corner = LinkedTableNode()
            potential_corner.hook(new_corner)
            near_edges = 
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
    return base"""


if __name__ == "__main__":
    a = create_odd_base()
    print(len(a))
    b = expand(a)
    print(len(a), len(b))
