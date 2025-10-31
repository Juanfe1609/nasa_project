from .star import Star

class Constellation:
    """
    Represents a constellation that groups a set of stars and the paths between them.
    Each constellation will have its own color when drawn on the map.
    """

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stars = []           # List of Star objects
        self.edges = []           # List of tuples (origin_id, dest_id, distance)

    def add_star(self, star):
        """Adds a Star object to the constellation."""
        if isinstance(star, Star):
            self.stars.append(star)
        else:
            raise TypeError("Only Star objects can be added to the constellation.")

    def add_edge(self, origin_id, dest_id, distance):
        """Adds a bidirectional edge between two stars."""
        self.edges.append((origin_id, dest_id, distance))
        self.edges.append((dest_id, origin_id, distance))

    def get_star(self, star_id):
        """Returns a star object by its ID."""
        for star in self.stars:
            if star.id == star_id:
                return star
        return None

    def to_dict(self):
        """Returns a JSON-serializable dictionary of the constellation."""
        return {
            "name": self.name,
            "color": self.color,
            "stars": [s.to_dict() for s in self.stars],
            "edges": self.edges
        }

    def __repr__(self):
        return f"Constellation({self.name}, stars={len(self.stars)})"
