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

    def __len__(self):
        return self.hooked.__len__()


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
            match len(node):
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


def expand_corner(corner: LinkedTableNode) -> list[LinkedTableNode]:
    new_corner = LinkedTableNode()
    new_intermediary_edge_0 = LinkedTableNode()
    new_intermediary_edge_1 = LinkedTableNode()
    new_final_edge_0 = LinkedTableNode()
    new_final_edge_1 = LinkedTableNode()

    edges_to_hook_intermediary: list[LinkedTableNode] = []
    for potential_edge in corner.hooked:
        if len(potential_edge) == 5:
            edges_to_hook_intermediary.append(potential_edge)

    edges_to_hook_final: list[LinkedTableNode] = []
    for intermediary in edges_to_hook_intermediary:
        for node in intermediary.hooked:
            if len(node) == 5 and node not in edges_to_hook_intermediary:
                edges_to_hook_final.append(node)
                break

    new_corner.hook(corner)
    new_corner.hook(new_intermediary_edge_0)
    new_corner.hook(new_intermediary_edge_1)
    new_intermediary_edge_0.hook(corner)
    new_intermediary_edge_1.hook(corner)
    new_intermediary_edge_0.hook(edges_to_hook_intermediary[0])
    new_intermediary_edge_1.hook(edges_to_hook_intermediary[1])
    new_intermediary_edge_0.hook(new_final_edge_0)
    new_intermediary_edge_1.hook(new_final_edge_1)

    new_final_edge_0.hook(corner)
    new_final_edge_1.hook(corner)
    new_final_edge_0.hook(edges_to_hook_intermediary[0])
    new_final_edge_1.hook(edges_to_hook_intermediary[1])
    new_final_edge_0.hook(edges_to_hook_final[0])
    new_final_edge_1.hook(edges_to_hook_final[1])
    # I know this can be done with a loop, but it makes more sense in my mind like this,
    # and I would certainly make dumb mistakes if I made it a loop

    return [new_corner, new_final_edge_0, new_final_edge_1]


def expand_along(edge: LinkedTableNode) -> Optional[set[LinkedTableNode]]:
    node_under_current: Optional[LinkedTableNode] = None
    node_under_next: Optional[LinkedTableNode] = None
    if 4 not in {len(x) for x in edge.hooked}:
        for node in edge.hooked:
            if len(node) == 7:
                if node_under_current is not None:
                    raise ValueError("base structure invalid: too many 7-neighbour adjacencies")
                node_under_current = node
            if len(node) == 6:
                if node_under_next is not None:
                    raise ValueError("base structure invalid: too many 6-neighbour adjacencies")
                node_under_next = node
            if node_under_next is not None and node_under_current is not None:
                break

        node_after_next: Optional[LinkedTableNode] = None
        for node in node_under_next.hooked:
            if len(node) == 5:
                node_after_next = node
                break
        if node_after_next is None:
            for node in node_under_next.hooked:
                if len(node) == 6:
                    node_after_next = node
                    break
            else:
                raise ValueError("Invalid links in base table.")

            node_under_other_end: Optional[LinkedTableNode] = None
            node_other_end: Optional[LinkedTableNode] = None
            for node in node_after_next.hooked:
                if len(node) == 7:
                    node_under_other_end = node
                if len(node) == 4:
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
            return {adjacent_node, closing_node}
        else:
            return {LinkedTableNode(hooked={edge, node_under_current, node_under_next, node_after_next})}
    else:  # the current edge has a 4-adjacency neighbour, meaning it is at the end of the line.
        for node in edge.hooked:
            if len(node) == 7:
                if node_under_current is not None:
                    raise ValueError("base structure invalid: too many 7-neighbour adjacencies")
                node_under_current = node
            if len(node) == 4:
                if node_under_next is not None:
                    raise ValueError("base structure invalid: too many 6-neighbour adjacencies")
                node_under_next = node
            if node_under_next is not None and node_under_current is not None:
                break
        LinkedTableNode(hooked={edge, node_under_current, node_under_next})
        return None


def expand(base: set[LinkedTableNode]) -> set[LinkedTableNode]:
    corners: set[LinkedTableNode] = set()
    for potential_corner in base:
        if len(potential_corner) == 3:
            corners.add(potential_corner)
    if len(corners) != 4:
        raise ValueError("Provided base is invalid: does not have exactly 4 corners")

    start_corner = next(iter(corners))
    start_expanded = expand_corner(start_corner)

    pass  # TODO Expansion logic, must stop right on top of the 2 corners that are nearest to start_corner.


if __name__ == "__main__":
    a = create_odd_base()
    print(len(a))
    b = expand(a)
    print(len(a), len(b))
