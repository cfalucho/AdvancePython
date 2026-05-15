import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv
import os

# ---------------------------------------------------------
# Instrumentation Mixin
# ---------------------------------------------------------

class Instrumented:
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __repr__(self):
        return self.__str__()

    def _instrument(self):
        print(f"[INSTRUMENT] class={self.__class__.__name__}")
        print(f"[INSTRUMENT] str={str(self)}")
        print(f"[INSTRUMENT] repr={repr(self)}")


# ---------------------------------------------------------
# Polymorphic Base Class
# ---------------------------------------------------------

class CelestialObject(Instrumented):
    def __init__(self, name="", category=""):
        self.name = name
        self.category = category

    def info(self):
        return f"Name: {self.name}\nCategory: {self.category}"


# ---------------------------------------------------------
# Derived Classes
# ---------------------------------------------------------

class Star(CelestialObject):
    def __init__(self, name="", spectral_type=""):
        super().__init__(name, "Star")
        self.spectral_type = spectral_type

    def info(self):
        return f"Star: {self.name}\nSpectral Type: {self.spectral_type}"


class Planet(CelestialObject):
    def __init__(self, name="", orbital_period=""):
        super().__init__(name, "Planet")
        self.orbital_period = orbital_period

    def info(self):
        return f"Planet: {self.name}\nOrbital Period: {self.orbital_period}"


class DwarfPlanet(CelestialObject):
    def __init__(self, name="", discovery_year=""):
        super().__init__(name, "Dwarf Planet")
        self.discovery_year = discovery_year

    def info(self):
        return f"Dwarf Planet: {self.name}\nDiscovery Year: {self.discovery_year}"


class Moon(CelestialObject):
    def __init__(self, name="", host_planet=""):
        super().__init__(name, "Moon")
        self.host_planet = host_planet

    def info(self):
        return f"Moon: {self.name}\nOrbits: {self.host_planet}"


# ---------------------------------------------------------
# CSV Loader
# ---------------------------------------------------------

def csv_loader(filename="celestial_objects.csv"):
    if not os.path.exists(filename):
        print("[ERROR] CSV file not found.")
        return None

    rows = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            if not row:
                continue
            rows.append({
                "category": row[0].strip(),
                "name": row[1].strip(),
                "attr": row[2].strip()
            })

    print(pd.DataFrame(rows))
    return pd.DataFrame(rows)


# ---------------------------------------------------------
# Build Objects from DataFrame
# ---------------------------------------------------------

def df_builder(df):
    objects = []
    # print(df)

    for _, row in df.iterrows():
        category = row["category"].strip().lower()
        name = row["name"].strip()
        attr = row["attr"].strip()

        if category == "star":
            objects.append(Star(name, attr))
        elif category == "planet":
            objects.append(Planet(name, attr))
        elif category == "dwarfplanet":
            objects.append(DwarfPlanet(name, attr))
        elif category == "moon":
            objects.append(Moon(name, attr))

    return objects


# ---------------------------------------------------------
# Tkinter GUI Application
# ---------------------------------------------------------

class CelestialGUI:
    def __init__(self, root, objects):
        self.root = root
        self.root.title("Celestial Object Viewer")

        self.objects = objects
        self.filtered = []

        # Main layout: Left = radio buttons, Right = listbox + detail panel
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Radio button variable
        self.category_var = tk.StringVar(value="Star")

        # Vertical radio buttons
        categories = ["Star", "Planet", "Dwarf Planet", "Moon"]
        for i, cat in enumerate(categories):
            rb = ttk.Radiobutton(self.left_frame, text=cat, value=cat,
                                 variable=self.category_var, command=self.update_listbox)
            rb.grid(row=i, column=0, sticky="w", pady=3)

        # Listbox
        self.listbox = tk.Listbox(self.right_frame, width=30, height=12)
        self.listbox.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.listbox.bind("<<ListboxSelect>>", self.update_detail_panel)

        # Detail panel (same window)
        self.detail_label = tk.Label(self.right_frame, text="Select an object",
                                     justify="left", anchor="nw", font=("Arial", 12))
        self.detail_label.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        # Initial load
        self.update_listbox()

    def update_listbox(self):
        """Update the listbox based on selected category."""
        category = self.category_var.get()

        lookup = {
            "Star": "Star",
            "Planet": "Planet",
            "Dwarf Planet": "Dwarf Planet",
            "Moon": "Moon"
        }

        selected = lookup[category]

        self.filtered = [obj for obj in self.objects if obj.category == selected]

        self.listbox.delete(0, tk.END)
        for obj in self.filtered:
            self.listbox.insert(tk.END, obj.name)

        # Default selection: first item
        if self.filtered:
            self.listbox.select_set(0)
            self.update_detail_panel(None)

    def update_detail_panel(self, event):
        """Show details of the selected object in the same window."""
        if not self.listbox.curselection():
            return

        index = self.listbox.curselection()[0]
        obj = self.filtered[index]

        self.detail_label.config(text=obj.info())


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    df = csv_loader()
    objects = df_builder(df)

    root = tk.Tk()
    app = CelestialGUI(root, objects)
    root.mainloop()


if __name__ == "__main__":
    main()
