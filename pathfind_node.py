from pygame.math import Vector2

class PathfindNode:
    """individual peice of the map that can be traversed"""
    def __init__(self, pos: tuple[int, int]):
        self.pos = Vector2(pos)                 # position of node on the map list (not true game pos)
        self.visited = False                    # whether the node's been visited
        self.distance_from_start = float("inf") # 'steps' from start node
        self.total_distance = float("inf")      # 'steps' + heuristic distance
        self.previous_node = None               # node that leads to this node
    
    def calculate_heuristic(self, target_node_pos: Vector2) -> None:
        """manhattan distance to target node"""
        self.heuristic = abs(self.pos.x-target_node_pos.x) + abs(self.pos.y-target_node_pos.y)