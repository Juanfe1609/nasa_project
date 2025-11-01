import tkinter as tk
from tkinter import ttk, messagebox

class ControlPanel(tk.Frame):
    """
    Side panel with controls to manage the donkey and simulation state.
    """

    def __init__(self, parent, simulator, json_manager, canvas):
        super().__init__(parent, bg="#202020", width=250)
        self.simulator = simulator
        self.json_manager = json_manager
        self.canvas = canvas

        self.pack_propagate(False)
        self.create_controls()

    # -------------------------------------------------
    #  UI Elements
    # -------------------------------------------------
    def create_controls(self):
        tk.Label(self, text="Donkey Controls", bg="#202020", fg="white",
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))

        # Health selector
        tk.Label(self, text="Health:", bg="#202020", fg="white").pack(anchor="w", padx=10)
        self.health_var = tk.StringVar(value="excellent")
        health_menu = ttk.Combobox(self, textvariable=self.health_var,
                                   values=["excellent", "good", "regular", "bad", "dying"],
                                   state="readonly")
        health_menu.pack(fill="x", padx=10, pady=5)

        # Energy slider
        tk.Label(self, text="Energy (%):", bg="#202020", fg="white").pack(anchor="w", padx=10)
        self.energy_var = tk.DoubleVar(value=100)
        energy_slider = ttk.Scale(self, from_=0, to=100, variable=self.energy_var, orient="horizontal")
        energy_slider.pack(fill="x", padx=10, pady=5)

        # Grass slider
        tk.Label(self, text="Grass (kg):", bg="#202020", fg="white").pack(anchor="w", padx=10)
        self.grass_var = tk.DoubleVar(value=10)
        grass_slider = ttk.Scale(self, from_=0, to=50, variable=self.grass_var, orient="horizontal")
        grass_slider.pack(fill="x", padx=10, pady=5)

        # Buttons
        ttk.Button(self, text="Apply Changes", command=self.apply_changes).pack(pady=8)
        ttk.Button(self, text="Block Path", command=self.block_path).pack(pady=4)
        ttk.Button(self, text="Unblock Path", command=self.unblock_path).pack(pady=4)
        ttk.Button(self, text="Redraw Graph", command=self.redraw).pack(pady=8)

    # -------------------------------------------------
    #  Button Actions
    # -------------------------------------------------
    def apply_changes(self):
        """Applies the UI changes to the donkey and updates the JSON."""
        donkey = self.simulator.donkey
        donkey.health = self.health_var.get()
        donkey.energy = float(self.energy_var.get())
        donkey.grass_kg = float(self.grass_var.get())

        # Update the JSON (if you later decide to store donkey info there)
        self.json_manager.update_donkey(donkey, {
            "health": donkey.health,
            "energy": donkey.energy,
            "grass_kg": donkey.grass_kg
        })

        messagebox.showinfo("Update", "Donkey data updated successfully!")

    def block_path(self):
        """Blocks a connection between two stars (example)."""
        from_id = self._ask_star("Origin star ID to block:")
        to_id = self._ask_star("Destination star ID to block:")
        if from_id and to_id:
            self.simulator.graph.block_path(from_id, to_id)
            self.json_manager.save_json(self.simulator.graph)
            messagebox.showinfo("Blocked", f"Path {from_id} ↔ {to_id} blocked.")
            self.redraw()

    def unblock_path(self):
        """Unblocks a previously blocked connection."""
        from_id = self._ask_star("Origin star ID to unblock:")
        to_id = self._ask_star("Destination star ID to unblock:")
        if from_id and to_id:
            distance = 5.0  # placeholder; later you can ask user for real distance
            self.simulator.graph.unblock_path(from_id, to_id, distance)
            self.json_manager.save_json(self.simulator.graph)
            messagebox.showinfo("Unblocked", f"Path {from_id} ↔ {to_id} restored.")
            self.redraw()

    def redraw(self):
        """Redraws the graph canvas."""
        self.canvas.draw_constellations()
        if self.simulator and self.simulator.current_path:
            self.canvas.draw_route(self.simulator.current_path)

    def _ask_star(self, prompt):
        """Simple dialog to ask for a star ID."""
        popup = tk.Toplevel(self)
        popup.title("Enter Star ID")
        popup.geometry("250x100")
        tk.Label(popup, text=prompt).pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack(pady=5)
        result = {}

        def confirm():
            result["value"] = entry.get().strip()
            popup.destroy()

        ttk.Button(popup, text="OK", command=confirm).pack()
        popup.wait_window()
        return result.get("value")
