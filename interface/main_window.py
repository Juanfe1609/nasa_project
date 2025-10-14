import tkinter as tk
from tkinter import ttk, messagebox
from classes.json_manager import JsonManager
from classes.graph import Graph
from classes.donkey import Donkey
from classes.simulator import Simulator
from interface.map_canvas import MapCanvas
from interface.controls import ControlPanel
from interface.final_report import FinalReport


class MainWindow(tk.Tk):
    """
    Main application window for the NASA Donkey Graph Simulator.
    Handles UI layout, JSON loading, and simulation control.
    """

    def __init__(self):
        super().__init__()
        self.title("NASA Donkey Graph Simulator")
        self.geometry("1000x700")
        self.configure(bg="#101010")

        # Core components
        self.json_manager = JsonManager()
        self.graph = Graph()
        self.donkey = None
        self.simulator = None

        # UI setup
        self.create_menu()
        self.create_main_layout()

    # -------------------------------------------------
    #  UI Layout
    # -------------------------------------------------
    def create_menu(self):
        """Creates the top menu bar."""
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load JSON", command=self.load_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        sim_menu = tk.Menu(menubar, tearoff=0)
        sim_menu.add_command(label="Start Simulation", command=self.start_simulation)
        sim_menu.add_command(label="Stop Simulation", command=self.stop_simulation)
        menubar.add_cascade(label="Simulation", menu=sim_menu)

        self.config(menu=menubar)

    def create_main_layout(self):
        """Creates the main frames and widgets."""
        self.left_frame = tk.Frame(self, bg="#202020", width=250)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self, bg="#101010")
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.canvas = MapCanvas(self.canvas_frame, self.graph)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Control panel on the left
        self.controls = None  # We'll create it after loading JSON

    # -------------------------------------------------
    #  Core functionalities
    # -------------------------------------------------
    def load_json(self):
        """Loads the constellation data and draws it."""
        constellations = self.json_manager.load_json()
        if not constellations:
            return

        for c in constellations:
            self.graph.add_constellation(c)

        #self.status_label.config(text=f"Loaded {len(constellations)} constellations.")
        self.draw_graph()

        # Initialize the donkey and simulator
        self.donkey = Donkey(health="excellent", age=5, energy=100, grass_kg=10, life_left=100)
        self.simulator = Simulator(self.graph, self.donkey, self.json_manager)

        # Add control panel (now that simulator exists)
        if not self.controls:
            from interface.controls import ControlPanel
            self.controls = ControlPanel(self.left_frame, self.simulator, self.json_manager, self.canvas)
            self.controls.pack(fill=tk.Y)

    def draw_graph(self):
        """Draws all constellations using MapCanvas."""
        self.canvas.draw_constellations()

    def start_simulation(self):
        """Starts the simulation if data is loaded."""
        if not self.simulator:
            messagebox.showwarning("Warning", "Load a JSON file first.")
            return

        # Start simulation from first star (later user can pick one)
        start_id = list(self.graph.nodes.keys())[0]
        self.simulator.start_simulation(start_id, mode="max_stars")

        
        report_data = self.simulator.generate_report()
        FinalReport(self, report_data)

        # Update interface with donkey data
        self.update_status()

    def stop_simulation(self):
        if self.simulator:
            self.simulator.stop_simulation()
            messagebox.showinfo("Simulation", "Simulation stopped.")

    def update_status(self):
        """Refreshes UI with the donkey’s state."""
        if not self.donkey:
            return

        self.health_label.config(text=f"Health: {self.donkey.health}")
        self.energy_label.config(text=f"Energy: {self.donkey.energy:.1f}%")
