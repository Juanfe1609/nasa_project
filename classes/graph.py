import math
from .constellation import Constellation
from .star import Star

class Graph:
    """
    Represents the entire galaxy graph containing multiple constellations.
    Manages all stars and the bidirectional connections between them.
    """

    def __init__(self):
        self.nodes = {}             # {star_id: Star}
        self.adjacency = {}         # {star_id: [(neighbor_id, distance), ...]}
        self.constellations = []    # List of Constellation objects

    # -----------------------------
    #  Add / Remove elements
    # -----------------------------
    def add_constellation(self, constellation):
        """Adds a new constellation to the graph."""
        if isinstance(constellation, Constellation):
            self.constellations.append(constellation)
            for star in constellation.stars:
                self.add_node(star)
            for origin, dest, dist in constellation.edges:
                self.add_edge(origin, dest, dist)

    def add_node(self, star):
        """Adds a new star node to the graph."""
        if isinstance(star, Star):
            self.nodes[star.id] = star
            if star.id not in self.adjacency:
                self.adjacency[star.id] = []

    def add_edge(self, origin_id, dest_id, distance):
        """Adds a bidirectional connection between two stars."""
        if origin_id not in self.adjacency:
            self.adjacency[origin_id] = []
        if dest_id not in self.adjacency:
            self.adjacency[dest_id] = []
        self.adjacency[origin_id].append((dest_id, distance))
        self.adjacency[dest_id].append((origin_id, distance))

    def remove_edge(self, origin_id, dest_id):
        """Removes a connection between two stars (both directions)."""
        if origin_id in self.adjacency:
            self.adjacency[origin_id] = [
                (nid, d) for nid, d in self.adjacency[origin_id] if nid != dest_id
            ]
        if dest_id in self.adjacency:
            self.adjacency[dest_id] = [
                (nid, d) for nid, d in self.adjacency[dest_id] if nid != origin_id
            ]

    # -----------------------------
    #  Utility methods
    # -----------------------------
    def get_star(self, star_id):
        """Returns a star object by ID."""
        return self.nodes.get(star_id, None)

    def get_neighbors(self, star_id):
        """Returns the list of neighbors for a star."""
        return self.adjacency.get(star_id, [])

    def block_path(self, origin_id, dest_id):
        """Temporarily blocks a path (used for meteor or comet events)."""
        self.remove_edge(origin_id, dest_id)

    def unblock_path(self, origin_id, dest_id, distance):
        """Restores a previously blocked path."""
        self.add_edge(origin_id, dest_id, distance)

    # ============================================================
    #  BELLMAN-FORD Algorithm
    # ============================================================
    def bellman_ford(self, start_id):
        """Computes the shortest paths from start_id using Bellman-Ford."""
        dist = {v: math.inf for v in self.nodes}
        pred = {v: None for v in self.nodes}
        dist[start_id] = 0
        pred[start_id] = start_id

        # Relax edges repeatedly
        for _ in range(len(self.nodes) - 1):
            updated = False
            for u in self.nodes:
                for v, weight in self.adjacency.get(u, []):
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
                        pred[v] = u
                        updated = True
            if not updated:
                break

        # Detect negative cycles
        for u in self.nodes:
            for v, weight in self.adjacency.get(u, []):
                if dist[u] + weight < dist[v]:
                    print("Warning: Negative weight cycle detected.")
                    return None, None

        return dist, pred

    # ============================================================
    #  DIJKSTRA Algorithm
    # ============================================================
    def dijkstra(self, start_id, target_id=None):
        """Computes the shortest path(s) from start_id using Dijkstra."""
        dist = {v: math.inf for v in self.nodes}
        pred = {v: None for v in self.nodes}
        dist[start_id] = 0
        unvisited = set(self.nodes.keys())

        while unvisited:
            u = min(unvisited, key=lambda v: dist[v])
            if dist[u] == math.inf:
                break

            unvisited.remove(u)
            if target_id and u == target_id:
                break

            for v, weight in self.adjacency.get(u, []):
                if v in unvisited:
                    new_dist = dist[u] + weight
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        pred[v] = u

        # Build shortest path if a target is given
        path = []
        if target_id:
            current = target_id
            while current is not None:
                path.insert(0, current)
                current = pred[current]

        return dist, pred, path

    # -----------------------------
    #  Representation
    # -----------------------------
    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, constellations={len(self.constellations)})"
