import time
from .graph import Graph
from .donkey import Donkey
from .json_manager import JsonManager

class Simulator:
    """
    Central controller that manages the donkey's journey through the galaxy.
    It connects the Donkey, the Graph, and the JsonManager.
    """

    def __init__(self, graph: Graph, donkey: Donkey, json_manager: JsonManager):
        self.graph = graph
        self.donkey = donkey
        self.json_manager = json_manager

        self.current_path = []       # List of star IDs in the current route
        self.visited_stars = []      # History of visited stars
        self.running = False
        self.logs = []               # Stores messages for the report

    # -------------------------------------------------
    #  Simulation control
    # -------------------------------------------------
    def start_simulation(self, start_id, mode="max_stars"):
        """
        Starts the simulation from a given star.
        mode can be 'max_stars' or 'optimal_route'.
        """
        start_star = self.graph.get_star(start_id)
        if not start_star:
            self.log(f"Start star '{start_id}' not found.")
            return

        self.donkey.current_star = start_star
        self.visited_stars.append(start_star.id)
        self.running = True
        self.log(f"Simulation started from {start_star.name}.")

        # Determine route based on mode
        if mode == "max_stars":
            self.calculate_route_max_stars()
        elif mode == "optimal_route":
            self.calculate_route_optimal()
        else:
            self.log("Invalid mode specified.")
            return

        self.follow_route()

    def stop_simulation(self):
        """Stops the simulation."""
        self.running = False
        self.log("Simulation stopped manually.")

    # -------------------------------------------------
    #  Route calculations
    # -------------------------------------------------
    def calculate_route_max_stars(self):
        """
        Calculates a route that tries to visit the maximum number of stars
        before the donkey dies. (Simple heuristic for now)
        """
        self.current_path = [self.donkey.current_star.id]

        # Basic greedy approach: always go to the nearest unvisited star
        current = self.donkey.current_star.id
        while self.donkey.is_alive():
            neighbors = self.graph.get_neighbors(current)
            unvisited = [(v, d) for v, d in neighbors if v not in self.visited_stars]
            if not unvisited:
                break

            next_star, dist = min(unvisited, key=lambda x: x[1])
            self.current_path.append(next_star)
            self.visited_stars.append(next_star)
            current = next_star

        self.log(f"Route calculated (max stars): {self.current_path}")

    def calculate_route_optimal(self):
        """
        Calculates the route that visits the most stars with the least cost
        using Dijkstra algorithm.
        """
        start_id = self.donkey.current_star.id
        dist, pred, path = self.graph.dijkstra(start_id)
        self.current_path = list(path) if path else [start_id]
        self.log(f"Optimal route calculated: {self.current_path}")

    # -------------------------------------------------
    #  Route following
    # -------------------------------------------------
    def follow_route(self):
        """Simulates the donkey traveling along the calculated route."""
        for star_id in self.current_path[1:]:
            if not self.running or not self.donkey.is_alive():
                break

            star = self.graph.get_star(star_id)
            prev_star = self.donkey.current_star
            distance = self.get_distance(prev_star.id, star.id)

            moved = self.donkey.move_to(star, distance)
            self.log(f"Moved from {prev_star.name} to {star.name} (distance {distance})")

            if not moved:
                self.log("The donkey died during travel.")
                break

            self.handle_star_interaction(star)

            # Optional delay for animations later
            time.sleep(0.5)

        self.log("Simulation finished.")
        self.generate_report()

    # -------------------------------------------------
    #  Star interactions
    # -------------------------------------------------
    def handle_star_interaction(self, star):
        """Simulates what happens when the donkey reaches a star."""
        if not self.donkey.is_alive():
            return

        # Eat if energy < 50%
        if self.donkey.energy < 50 and self.donkey.grass_kg > 0:
            self.donkey.eat_grass(1)
            self.log(f"Donkey ate grass. Energy: {self.donkey.energy:.1f}%")

        # Research actions
        alive = self.donkey.research_at_star(star)
        self.log(f"Research at {star.name}. Life left: {self.donkey.life_left:.1f}ly, Energy: {self.donkey.energy:.1f}%")

        # Hypergiant effect
        if star.is_hypergiant:
            self.donkey.recharge_on_hypergiant()
            self.log(f"Hypergiant star {star.name} recharged the donkey!")

        # Save JSON state after each visit
        self.json_manager.save_json(self.graph)

        if not alive:
            self.log(f"The donkey died at {star.name}.")
            self.running = False

    # -------------------------------------------------
    #  Utility
    # -------------------------------------------------
    def get_distance(self, origin_id, dest_id):
        """Returns the distance between two stars if connected."""
        for v, d in self.graph.get_neighbors(origin_id):
            if v == dest_id:
                return d
        return 0

    def log(self, message):
        """Stores a message in the simulation log."""
        print(message)
        self.logs.append(message)

    def generate_report(self):
        """Generates a summary of the journey."""
        report = {
            "visited_stars": self.visited_stars,
            "total_visited": len(self.visited_stars),
            "final_status": self.donkey.to_dict(),
            "log": self.logs
        }
        self.log("=== Simulation Report ===")
        for key, value in report.items():
            self.log(f"{key}: {value}")
        return report
