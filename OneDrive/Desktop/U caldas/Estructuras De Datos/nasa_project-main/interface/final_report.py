import tkinter as tk
from tkinter import ttk

class FinalReport(tk.Toplevel):
    """
    Displays a final report window after the simulation ends.
    """

    def __init__(self, parent, report_data):
        super().__init__(parent)
        self.title("Simulation Report")
        self.geometry("600x500")
        self.configure(bg="#101010")

        tk.Label(
            self, text="NASA Donkey Mission Report", 
            font=("Segoe UI", 14, "bold"), fg="white", bg="#101010"
        ).pack(pady=10)

        # Scrollable frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg="#101010", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fill report data
        self._fill_report(scroll_frame, report_data)

        ttk.Button(
            self, text="Close", command=self.destroy
        ).pack(pady=10)

    # -------------------------------------------------
    #  Internal helpers
    # -------------------------------------------------
    def _fill_report(self, frame, report_data):
        """Adds the formatted data to the scrollable frame."""
        for key, value in report_data.items():
            section_title = tk.Label(
                frame, text=str(key).replace("_", " ").capitalize(),
                font=("Segoe UI", 12, "bold"), fg="#00ffff", bg="#101010"
            )
            section_title.pack(anchor="w", pady=(10, 2))

            if isinstance(value, (list, dict)):
                text = tk.Text(frame, height=6, wrap="word", bg="#181818", fg="white")
                text.insert("1.0", str(value))
                text.config(state="disabled")
                text.pack(fill="x", padx=10, pady=2)
            else:
                tk.Label(
                    frame, text=str(value), bg="#101010", fg="white", wraplength=550, justify="left"
                ).pack(anchor="w", padx=20)
