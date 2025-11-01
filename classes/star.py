class Star:
    """
    Represents a single star in the galaxy map.
    Each star is a node in the graph and may belong to one or more constellations.
    """

    def __init__(self, star_id, name, x, y, galaxy=None, is_hypergiant=False, life_delta=0, investigation_time=0, energy_cost=0):
        self.id = star_id
        self.name = name
        self.x = x
        self.y = y
        self.galaxy = galaxy
        self.is_hypergiant = is_hypergiant
        self.life_delta = life_delta          # Life gained or lost when visited
        self.investigation_time = investigation_time
        self.energy_cost = energy_cost
        self.visited = False

    def update_data(self, **kwargs):
        """Allows updating attributes dynamically from the interface."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        """Returns a dictionary representation of the star."""
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "galaxy": self.galaxy,
            "is_hypergiant": self.is_hypergiant,
            "life_delta": self.life_delta,
            "investigation_time": self.investigation_time,
            "energy_cost": self.energy_cost,
            "visited": self.visited
        }

    def __repr__(self):
        return f"Star({self.name}, pos=({self.x}, {self.y}))"
