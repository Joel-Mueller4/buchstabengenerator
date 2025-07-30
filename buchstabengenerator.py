import random
import itertools
import tkinter as tk

# Großbuchstaben von A bis X
letters = [chr(i) for i in range(ord('A'), ord('X') + 1)]
combinations = list(itertools.product(letters, repeat=2))

# Fenster erstellen
fenster = tk.Tk()
fenster.title("Buchstabenpaar-Generator")
fenster.geometry("400x300")
fenster.resizable(True, True)

# Auswahl-Logik
auswahl = {buchstabe: tk.BooleanVar(value=False, master=fenster) for buchstabe in letters}
alle_var = tk.BooleanVar(value=True, master=fenster)

# Funktion zum Generieren von Buchstabenpaaren
def generiere_buchstabenpaar():
    if alle_var.get():
        start_buchstaben = letters
    else:
        start_buchstaben = [b for b in letters if auswahl[b].get()]
    if not start_buchstaben:
        return "❌"
    erster = random.choice(start_buchstaben)
    zweiter = random.choice(letters)
    return erster + zweiter

# Anzeige aktualisieren
def aktualisiere_label(event=None):
    buchstabenpaar = generiere_buchstabenpaar()
    label.config(text=buchstabenpaar)

# Fenster immer im Vordergrund toggeln
def toggle_topmost():
    global topmost_state
    topmost_state = not topmost_state
    fenster.attributes("-topmost", topmost_state)
    button_toggle.config(text="Immer im Vordergrund: AN" if topmost_state else "Immer im Vordergrund: AUS")

# Tasteneingaben abfangen
def taste_gedrueckt(event):
    if event.keysym in ("Return"):
        aktualisiere_label()
    if event.keysym in ("plus"):
        toggle_topmost()

# "Alle" wurde ausgewählt
def alle_ausgewaehlt():
    if alle_var.get():
        for var in auswahl.values():
            var.set(False)

# Einzelbuchstabe wurde ausgewählt
def buchstabe_ausgewaehlt():
    alle_var.set(False)

# Menüfenster toggeln (Toplevel ohne Scrollbar)
dropdown_window = None

def close_menu(event):
    global dropdown_window
    if dropdown_window and tk.Toplevel.winfo_exists(dropdown_window):
        if event.widget not in dropdown_window.winfo_children() and event.widget != dropdown_button:
            dropdown_window.destroy()
            dropdown_window = None

def toggle_menu():
    global dropdown_window
    if dropdown_window and tk.Toplevel.winfo_exists(dropdown_window):
        dropdown_window.destroy()
        dropdown_window = None
    else:
        x = fenster.winfo_rootx() + dropdown_button.winfo_x()
        y = fenster.winfo_rooty() + dropdown_button.winfo_y() + dropdown_button.winfo_height()

        dropdown_window = tk.Toplevel(fenster)
        dropdown_window.wm_overrideredirect(True)
        dropdown_window.wm_geometry(f"+{x}+{y}")
        dropdown_window.attributes("-topmost", True)
        dropdown_window.configure(bg="white", bd=1, relief="solid")

        fenster.bind("<Button-1>", close_menu)

        alle_checkbox = tk.Checkbutton(dropdown_window, text="Alle", variable=alle_var, command=alle_ausgewaehlt, bg="white")
        alle_checkbox.pack(anchor="w")
        tk.Label(dropdown_window, text="", bg="white").pack()

        for buchstabe in letters:
            cb = tk.Checkbutton(dropdown_window, text=buchstabe, variable=auswahl[buchstabe], command=buchstabe_ausgewaehlt, bg="white")
            cb.pack(anchor="w")

# Dropdown-Menü Button
dropdown_button = tk.Button(fenster, text="Buchstabenauswahl", command=toggle_menu)
dropdown_button.pack(pady=5)

# Anzeige-Frame
anzeige_frame = tk.Frame(fenster)
anzeige_frame.pack(fill="both", expand=True)

label = tk.Label(anzeige_frame, text="", font=("Helvetica", 60, "bold"), pady=10)
label.pack(expand=True)

# Buttons
button_neu = tk.Button(anzeige_frame, text="Neues Paar", command=aktualisiere_label, font=("Helvetica", 12))
button_neu.pack(pady=5)

button_toggle = tk.Button(anzeige_frame, text="Immer im Vordergrund: AN", command=toggle_topmost, font=("Helvetica", 10))
button_toggle.pack(pady=5)

# Initialer Topmost-Zustand
topmost_state = True
fenster.attributes("-topmost", topmost_state)

# Tastaturbindung
fenster.bind("<Key>", taste_gedrueckt)
fenster.focus_force()

# Erstes Paar anzeigen
aktualisiere_label()

fenster.mainloop()
