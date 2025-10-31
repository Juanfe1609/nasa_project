import json
from tkinter import filedialog
from .constellation import Constellation
from .star import Star
from .donkey import Donkey

class JsonManager:
    """
    Handles loading and saving constellation data from/to JSON files.
    Keeps the file synchronized with any runtime modifications.
    """

    def __init__(self, graph=None):
        self.graph = graph
        self.file_path = None

    # -------------------------------------------------
    #  Load and Save
    # -------------------------------------------------
    def load_json(self):
        """
        Opens a file dialog for the user to select a JSON file,
        reads it, fills the existing graph, and returns constellations.
        """
        self.file_path = filedialog.askopenfilename(
            title="Select constellation JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not self.file_path:
            print("No file selected.")
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        constellations = []
        for c in data.get("constellations", []):
            const = Constellation(c["name"], c.get("color", "#FFFFFF"))

            # Crear estrellas
            for s in c.get("starts", []):
                star = Star(
                    s["id"], s["label"], s["coordenates"]["x"], s["coordenates"]["y"],
                    galaxy=s.get("galaxy"),
                    is_hypergiant=s.get("hypergiant", False),
                    life_delta=s.get("timeToEat", 0),
                    investigation_time=s.get("timeToEat", 0),
                    energy_cost=s.get("amountOfEnergy", 0)
                )
                const.add_star(star)
                if hasattr(self, "graph") and self.graph:
                    self.graph.add_star(star)

            # Crear conexiones (edges) desde linkedTo
            if hasattr(self, "graph") and self.graph:
                for s in c.get("starts", []):
                    links = s.get("linkedTo", [])
                    for link in links:
                        origin_id = s["id"]
                        dest_id = link["starId"]
                        distance = float(link["distance"])
                        # Solo agregamos si ambos nodos existen
                        if self.graph.get_star(origin_id) and self.graph.get_star(dest_id):
                            self.graph.add_edge(origin_id, dest_id, distance)

            constellations.append(const)

        from .donkey import Donkey
        burro = Donkey(
            health=data.get("estadoSalud", "good").lower(),
            energy=data.get("burroenergiaInicial", 100),
            grass_kg=data.get("pasto", 0)
        )

        self.burro = burro

        # --- Verificación opcional ---
        if hasattr(self, "graph") and self.graph and hasattr(self.graph, "nodes"):
            print("=== Graph Loaded ===")
            for node_id, node in self.graph.nodes.items():
                print(f"Star {node_id}: connected to {list(node.connections.keys())}")
        return constellations




    def save_json(self, graph):
        """
        Saves the current graph state back to the same JSON file.
        """
        if not self.file_path:
            print("No JSON file loaded yet.")
            return

        data = {
            "constellations": [c.to_dict() for c in graph.constellations]
        }

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ JSON updated: {self.file_path}")

    # -------------------------------------------------
    #  Runtime update methods
    # -------------------------------------------------
    def update_star(self, graph, star_id, new_data):
        """
        Updates a star in the graph and automatically writes changes to the JSON.
        new_data is a dict like {"energy_cost": 5, "life_delta": 2}.
        """
        star = graph.get_star(star_id)
        if star:
            star.update_data(**new_data)
            self.save_json(graph)

    def update_connection(self, graph, origin_id, dest_id, new_distance):
        """
        Updates an existing connection between stars.
        """
        # Remove old edge
        graph.remove_edge(origin_id, dest_id)
        # Add new one
        graph.add_edge(origin_id, dest_id, new_distance)
        self.save_json(graph)

    def update_donkey(self, donkey, new_data):
        """
        Updates donkey attributes (if we later decide to store them in JSON too).
        """
        for key, value in new_data.items():
            if hasattr(donkey, key):
                setattr(donkey, key, value)
