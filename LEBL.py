# ======================================================================================================================
#
#                    __     ______ ____   __          ______ ____   ____   _____
#                   / /    / ____// __ \ / /         / ____// __ \ / __ \ / ___/
#                  / /    / __/  / /_/ // /         / /    / / / // /_/ // __/
#                 / /___ / /___ / /_  // /___      / /___ / /_/ // _, _// /___
#                /_____//_____//_____//_____/      \____/ \____//_/ |_|/_____/
#
#
# ======================================================================================================================


import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import copy
from airport import *
from aircraft import *

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = None

class BoardingArea:
    def __init__(self, name, type_schengen):
        self.name = name
        self.type = type_schengen  # True per Schengen, False per non-Schengen
        self.gates = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate: return -1
    area.gates = []
    i = init_gate
    while i <= end_gate:
        area.gates.append(Gate(f"{prefix}{i}"))
        i += 1
    return 0

def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    try:
        f = open(filename, "r")
        terminal.airlines = []
        linea = f.readline()
        while linea != "":
            datos = linea.strip().split("\t")
            if len(datos) >= 2:
                terminal.airlines.append(datos[1].strip().upper())
            linea = f.readline()
        f.close()
        return 0
    except FileNotFoundError:
        return -1

def GateOccupancy(bcn):
    gates_info = []
    for term in bcn.terminals:
        for area in term.boarding_areas:
            for gate in area.gates:
                gates_info.append({
                    "terminal": term.name,
                    "boarding_area": area.name,
                    "type": "Schengen" if area.type else "non-Schengen",
                    "gate": gate.name,
                    "occupied": gate.occupied,
                    "aircraft_id": gate.aircraft_id
                })
    return gates_info

def IsAirlineInTerminal(terminal, name):
    if not name: return False
    name_clean = name.strip().upper()
    for airline in terminal.airlines:
        if airline.strip().upper() == name_clean: return True
    return False

def SearchTerminal(bcn, name):
    for term in bcn.terminals:
        if IsAirlineInTerminal(term, name): return term.name
    return None

def AssignGate(bcn, aircraft):
    if aircraft is None: return -1
    aeropuerto_referencia = aircraft.origin if (aircraft.origin and aircraft.origin != "-") else aircraft.destination
    if not aeropuerto_referencia or aeropuerto_referencia == "-": return -1

    schengen = IsSchengen(aeropuerto_referencia)
    terminal_name = SearchTerminal(bcn, aircraft.company.strip())
    if terminal_name is None: return -1

    for terminal in bcn.terminals:
        if terminal.name == terminal_name:
            for area in terminal.boarding_areas:
                if area.type == schengen:
                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0
    return -1

def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
    except:
        return -1
    linies = f.readlines()
    f.close()
    if len(linies) == 0 or len(linies[0].split()) < 2: return -1

    primera_linea = linies[0].split()
    LEBL = BarcelonaAP(primera_linea[0])
    Nlinea = 0

    for i in range(int(primera_linea[1])):
        Nlinea += 1
        lineaactual = linies[Nlinea].strip().split(" ")
        terminal = Terminal(lineaactual[1])
        LoadAirlines(terminal, terminal.name)
        LEBL.terminals.append(terminal)

        Nboardingareas = int(lineaactual[2])
        for j in range(Nboardingareas):
            Nlinea += 1
            lineaactual = linies[Nlinea].strip().split(" ")
            is_sch = "Schengen" in lineaactual
            boardingarea = BoardingArea(lineaactual[1], is_sch)
            terminal.boarding_areas.append(boardingarea)

            gates_idx = [k for k, x in enumerate(lineaactual) if x.isdigit()]
            if len(gates_idx) >= 2:
                gateinicio = int(lineaactual[gates_idx[0]])
                gatefinal = int(lineaactual[gates_idx[1]])
                SetGates(boardingarea, gateinicio, gatefinal, lineaactual[1])
    return LEBL

def AssignNightGates(bcn, aircrafts):
    if not aircrafts: return -1
    for ac in aircrafts:
        if (ac.landtime is None or ac.landtime == "-") and ac.departuretime:
            AssignGate(bcn, ac)
    return 0

def FreeGate(bcn, aircraft_id):
    for term in bcn.terminals:
        for area in term.boarding_areas:
            for gate in area.gates:
                if gate.occupied and gate.aircraft_id == aircraft_id:
                    gate.occupied = False
                    gate.aircraft_id = None
                    return 0
    return -1

def AssignGatesAtTime(bcn, aircrafts, time):
    if not aircrafts: return -1
    hour = time.split(":")[0].zfill(2)
    failed = 0

    for ac in aircrafts:
        if ac.departuretime and ac.departuretime.split(":")[0].zfill(2) == hour:
            FreeGate(bcn, ac.id)

    for ac in aircrafts:
        if ac.landtime and ac.landtime.split(":")[0].zfill(2) == hour:
            if AssignGate(bcn, ac) != 0:
                failed += 1
    return failed


_actualitzar_mapa_global_fn = None

def PlotGatesMap(bcn_base, aircrafts_list, frame_central):
    global _actualitzar_mapa_global_fn

    # Netejar l'espai central per evitar duplicats
    for widget in frame_central.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(11, 5.5), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Variables de control per al sistema de Debounce (anti-col·lapse)
    _after_id = None
    _ultims_minuts_dibuixats = -1

    # RE-DIBUIX REAL DE MATPLOTLIB (Només es crida quan l'usuari s'atura o decideix el minut)
    def dibuixar_grafic_real(minuts_totals):
        nonlocal _ultims_minuts_dibuixats
        _ultims_minuts_dibuixats = minuts_totals

        hora_num = minuts_totals // 60
        minut_num = minuts_totals % 60
        temps_actual_text = f"{hora_num:02d}:{minut_num:02d}"

        try:
            import __main__
            is_dark = __main__.dark_mode
            textos = __main__.TEXTOS[__main__.idioma_actual]
        except:
            is_dark = False
            textos = {"plot_lebl_t": "Barcelona Gates", "lbl_area": "Area "}

        bg_color = "#1a1d26" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#1a1f2c"
        color_linies = "#4a5568" if is_dark else "#cbd5e1"

        # Sincronitzar colors estructurals
        fig.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # LÒGICA OPTIMITZADA: Evitem clons continus si no és necessari
        bcn_sim = copy.deepcopy(bcn_base)
        AssignNightGates(bcn_sim, aircrafts_list)

        for h in range(0, hora_num):
            AssignGatesAtTime(bcn_sim, aircrafts_list, f"{h:02d}:00")
        AssignGatesAtTime(bcn_sim, aircrafts_list, temps_actual_text)

        gates_info = GateOccupancy(bcn_sim)

        ax.clear()
        ax.set_facecolor(bg_color)

        gate_w, gate_h, sep_gate, sep_area_x = 0.6, 0.6, 0.15, 3.5
        current_terminal, current_area, y_terminal, x_area, max_area_height = "", "", 0, 2, 0

        i = 0
        while i < len(gates_info):
            info = gates_info[i]
            if info["terminal"] != current_terminal:
                y_terminal -= (max_area_height + 3)
                max_area_height = 0
                current_terminal = info["terminal"]
                current_area = ""
                x_area = 2
                ax.plot([1, 22], [y_terminal, y_terminal], linewidth=4, color=color_linies)
                ax.text(0.3, y_terminal, "T" + current_terminal, va='center', fontsize=14, fontweight='bold',
                        color=fg_color)

            if info["boarding_area"] != current_area:
                current_area = info["boarding_area"]
                x_area += sep_area_x
                count = sum(
                    1 for g in gates_info if g["boarding_area"] == current_area and g["terminal"] == current_terminal)
                area_height = ((count + 1) // 2) * (gate_h + sep_gate)
                if area_height > max_area_height:
                    max_area_height = area_height

                ax.plot([x_area, x_area], [y_terminal, y_terminal - area_height], linewidth=2, color=color_linies)
                ax.text(x_area, y_terminal + 0.6, textos["lbl_area"] + current_area, ha='center', fontsize=10,
                        fontweight='bold', color=fg_color)
                y_left = y_right = y_terminal - gate_h - 0.2
                side = "left"

            color = "#e53e3e" if info["occupied"] else "#38a169"
            gate_side = side

            if side == "left":
                x_gate = x_area - gate_w - 0.2
                y_gate = y_left
                y_left -= gate_h + sep_gate
                side = "right"
            else:
                x_gate = x_area + 0.2
                y_gate = y_right
                y_right -= gate_h + sep_gate
                side = "left"

            ax.add_patch(Rectangle((x_gate, y_gate), gate_w, gate_h, facecolor=color))
            ax.text(x_gate + gate_w / 2, y_gate + gate_h / 2, info["gate"], ha='center', va='center', fontsize=8,
                    color='white')

            if info["occupied"] and info.get("aircraft_id"):
                x_text = (x_gate - 0.15) if gate_side == "left" else (x_gate + gate_w + 0.15)
                ha = "right" if gate_side == "left" else "left"
                ax.text(x_text, y_gate + gate_h / 2, info["aircraft_id"], va='center', ha=ha, fontsize=8,
                        color=fg_color)
            i += 1

        ax.set_xlim(0, 24)
        ax.set_ylim(y_terminal - max_area_height - 5, 2)
        ax.axis('off')

        propiedades_caja = dict(boxstyle='round,pad=0.4', facecolor='#2b6cb0', edgecolor='none', alpha=0.8)
        ax.text(23.5, 1.2, f" TIME: {temps_actual_text}h ", fontsize=11, fontweight='bold', color='white', ha='right',
                bbox=propiedades_caja)

        ax.set_title(textos["plot_lebl_t"], fontsize=13, fontweight='bold', color=fg_color)
        fig.tight_layout()
        canvas.draw()

    # CONTROLADOR INTEL·LIGENT DE L'SLIDER (Recepció contínua súper ràpida)
    def gestionar_moviment_slider(valor_minuts):
        nonlocal _after_id
        minuts_totals = int(valor_minuts)

        # 1. Actualitzar immediatament el text de l'etiqueta flotante i colors de Tkinter (això és instantani)
        try:
            import __main__
            is_dark = __main__.dark_mode
        except:
            is_dark = False

        bg_color = "#1a1d26" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#1a1f2c"

        hora_num = minuts_totals // 60
        minut_num = minuts_totals % 60
        lbl_info_temps.configure(text=f"Hora seleccionada: {hora_num:02d}:{minut_num:02d}h", fg=fg_color)

        frame_central.configure(bg=bg_color)
        canvas.get_tk_widget().configure(bg=bg_color)
        frame_slider.configure(bg=bg_color)
        lbl_slider.configure(bg=bg_color, fg=fg_color)
        slider_temps.configure(bg=bg_color, fg=fg_color, troughcolor="#4a5568" if is_dark else "#e2e8f0")

        # 2. SISTEMA DE SEGURETAT (Debounce): Si l'usuari està movent el ratolí molt ràpid,
        # cancel·lem el dibuix anterior i esperem que s'aturi per no congelar la pantalla.
        if _after_id is not None:
            frame_central.after_cancel(_after_id)

        # Si canvia molt poc a poc o s'atura durant 40ms, dibuixem el mapa de Matplotlib
        _after_id = frame_central.after(40, lambda: dibuixar_grafic_real(minuts_totals))

    # 3. Estructura de control inferior
    frame_slider = tk.Frame(frame_central)
    frame_slider.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=5)

    lbl_slider = tk.Label(frame_slider, text="Control Temporal:", font=("Segoe UI", 9, "bold"))
    lbl_slider.pack(side=tk.LEFT, padx=5)

    slider_temps = tk.Scale(
        frame_slider,
        from_=0, to=1439,
        orient=tk.HORIZONTAL,
        resolution=1,
        showvalue=False,  # Ocultem el valor numèric pur de minuts sota la barra
        highlightthickness=0,
        activebackground="#3182ce",
        command=gestionar_moviment_slider
    )
    slider_temps.set(420)  # 07:00 AM inicial
    slider_temps.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=10)

    # Afegim una etiqueta de text a sobre de la barra que respon al mil·lisegon sense retard
    lbl_info_temps = tk.Label(frame_central, text="Hora seleccionada: 07:00h", font=("Segoe UI", 10, "bold"))
    lbl_info_temps.pack(side=tk.BOTTOM, pady=2)

    def forçar_redibuix_extern():
        if frame_central.winfo_exists():
            dibuixar_grafic_real(slider_temps.get())

    _actualitzar_mapa_global_fn = forçar_redibuix_extern

    # Càrrega gràfica inicial
    dibuixar_grafic_real(420)

def PlotDayOccupancy(bcn, aircrafts, frame_central):
    for widget in frame_central.winfo_children(): widget.destroy()
    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False;
        textos = {"plot_lebl_t": "Ocupació", "tab_hours": "Hores"}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"

    bcn_sim = copy.deepcopy(bcn)
    hours = [f"{h:02d}:00" for h in range(24)]
    terminal_names = [t.name for t in bcn_sim.terminals]
    terminal_history = {t_name: [] for t_name in terminal_names}
    failed_history = []

    AssignNightGates(bcn_sim, aircrafts)

    for hora in hours:
        failed_count = AssignGatesAtTime(bcn_sim, aircrafts, hora)
        failed_history.append(failed_count)

        current_occupancy = {t_name: 0 for t_name in terminal_names}
        for terminal in bcn_sim.terminals:
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied: current_occupancy[terminal.name] += 1
        for t_name in terminal_names:
            terminal_history[t_name].append(current_occupancy[t_name])

    fig = Figure(figsize=(10, 5), dpi=100, facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)

    for t_name in terminal_names:
        ax.plot(range(24), terminal_history[t_name], marker='o', linewidth=2, label=f"Ocupació {t_name}")
    ax.plot(range(24), failed_history, marker='x', color='red', linestyle='--', linewidth=2, label="No Asignados")

    ax.set_title("Evolució Dinàmica de Portes (24h)", color=fg_color, fontweight='bold')
    ax.set_xlabel("Hora del Dia", color=fg_color)
    ax.set_ylabel("Avions", color=fg_color)
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h:02d}" for h in range(24)], color=fg_color)
    ax.tick_params(colors=fg_color)
    ax.grid(True, linestyle=':', alpha=0.5)

    leg = ax.legend(facecolor=bg_color, edgecolor=fg_color)
    for text in leg.get_texts(): text.set_color(fg_color)
    for spine in ax.spines.values(): spine.set_color(fg_color)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

def MapFlights(aircrafts, airports_list):
    try:
        F = open("routes.kml", "w", encoding="utf-8")
        F.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<name>Vols a LEBL</name>\n')
        for ac in aircrafts:
            icao = ac.origin if ac.origin else ac.destination
            if not icao or icao == "-": continue

            encontrado = False
            lat_origen, lon_origen = 0.0, 0.0
            for ap in airports_list:
                if ap.icao == icao:
                    encontrado = True
                    lat_origen, lon_origen = ap.latitude, ap.longitude
                    break
            if encontrado:
                color = "ff00ff00" if IsSchengen(icao) else "ff0000ff"
                F.write(
                    f'<Placemark>\n  <name>Flight {ac.id} ({icao})</name>\n  <Style><LineStyle><color>{color}</color><width>2</width></LineStyle></Style>\n')
                F.write(
                    f'  <LineString><coordinates>{lon_origen},{lat_origen},0 2.07833,41.29666,0</coordinates></LineString>\n</Placemark>\n')
        F.write('</Document>\n</kml>\n')
        F.close()
    except Exception as e:
        print("Error en MapFlights:", e)
