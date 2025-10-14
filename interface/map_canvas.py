import tkinter as tk
import random

class MapCanvas(tk.Canvas):
    """
    Custom canvas to visualize constellations, stars, and donkey routes.
    """

    def __init__(self, parent, graph, **kwargs):
        super().__init__(parent, bg="black", **kwargs)
        self.graph = graph
        self.colors = {}  # Constellation name -> color
        self.route = []   # List of star IDs in the current path

    # -------------------------------------------------
    #  Drawing methods
    # -------------------------------------------------
    def draw_constellations(self):
        """Draws all stars and connections grouped by constellation."""
        self.delete("all")
        used_colors = set()

        for const in self.graph.constellations:
            # Assign a unique color to each constellation
            if const.name not in self.colors:
                color = const.color
                if not color or color in used_colors:
                    color = self._random_color()
                self.colors[const.name] = color
                used_colors.add(color)

            # Draw edges
            for (origin, dest, dist) in const.edges:
                star1 = self.graph.get_star(origin)
                star2 = self.graph.get_star(dest)
                if star1 and star2:
                    self.create_line(
                        star1.x * 3, star1.y * 3,
                        star2.x * 3, star2.y * 3,
                        fill=self.colors[const.name],
                        width=1.2
                    )

        # Draw stars
        for star in self.graph.nodes.values():
            color = "red" if star.is_hypergiant else "white"
            # If star belongs to multiple constellations -> highlight red
            const_count = sum(
                1 for c in self.graph.constellations if star in c.stars
            )
            if const_count > 1:
                color = "red"
            self.create_oval(
                star.x * 3 - 4, star.y * 3 - 4,
                star.x * 3 + 4, star.y * 3 + 4,
                fill=color, outline=""
            )

    def draw_route(self, path):
        """Draws the donkey's route as a highlighted line."""
        if not path or len(path) < 2:
            return
        self.route = path

        for i in range(len(path) - 1):
            s1 = self.graph.get_star(path[i])
            s2 = self.graph.get_star(path[i + 1])
            if s1 and s2:
                self.create_line(
                    s1.x * 3, s1.y * 3,
                    s2.x * 3, s2.y * 3,
                    fill="cyan", width=2.5
                )

    # -------------------------------------------------
    #  Utility
    # -------------------------------------------------
    def _random_color(self):
        """Generates a random bright color for constellations."""
        r = lambda: random.randint(80, 255)
        return f'#{r():02x}{r():02x}{r():02x}'
