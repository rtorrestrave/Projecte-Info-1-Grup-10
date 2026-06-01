# ======================================================================================================================
#
#     ______ __     ____   ______ __  __ ______      ______ ____   ___   ______ __ __  _____ ____
#    / ____// /    /  _/  / ____// / / //_  __/     /_  __// __ \ /   | / ____// //_/ / ___// __ \
#   / /_   / /     / /   / / __ / /_/ /  / /         / /  / /_/ // /| |/ /    / ,<   / __/ / /_/ /
#  / __/  / /___ _/ /   / /_/ // __  /  / /         / /  / _, _// ___// /___ / /| | / /___/ _, _/
# /_/    /_____//___/   \____//_/ /_/  /_/         /_/  /_/ |_|/_/  |_|\____//_/ |_|/_____//_/ |_|
#
#
# ======================================================================================================================

################################################################################################################********
#####################       DEFINICIÓ CLASSE I LLIBRERIES       ########################################################
################################################################################################################********
import math
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from airport import IsSchengen

class Aircraft:
    def __init__(self, id, company, origin=None, landtime=None, destination=None, departuretime=None):
        self.id = id
        self.company = company
        self.origin = origin if origin != "-" else None
        self.landtime = landtime if landtime != "-" else None
        self.destination = destination if destination != "-" else None
        self.departuretime = departuretime if departuretime != "-" else None

################################################################################################################********
#################################       CÀRREGA D'ARRIBADES (LOADARRIVALS)      ########################################
################################################################################################################********
def LoadArrivals(filename):
    lista_aircraft = []
    try:
        f = open(filename, "r")
        f.readline()  # Saltem la capçalera
        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) != 4:
                linea = f.readline()
                continue
            id = datos[0]
            origin = datos[1]
            landtime = datos[2]
            company = datos[3]

            lista_aircraft.append(Aircraft(id, company, origin=origin, landtime=landtime))
            linea = f.readline()
        f.close()
    except FileNotFoundError:
        print("Fitxer d'arribades NO trobat.")
        return []
    return lista_aircraft

################################################################################################################********
#################################       CÀRREGA DE SORTIDES (LOADDEPARTURES)    ########################################
################################################################################################################********
def LoadDepartures(filename):
    lista_departures = []
    try:
        f = open(filename, "r")
        f.readline()  # Saltem capçalera
        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) != 4:
                linea = f.readline()
                continue
            id = datos[0]
            destination = datos[1]
            departuretime = datos[2]
            company = datos[3]

            lista_departures.append(Aircraft(id, company, destination=destination, departuretime=departuretime))
            linea = f.readline()
        f.close()
        return lista_departures, 0
    except FileNotFoundError:
        print("Fitxer de sortides NO trobat.")
        return [], -1

################################################################################################################********
################################  GUARDAR LA LLISTA EN FITXER TXT       ################################################
################################################################################################################********
def SaveFlights(aircrafts, filename):
    try:
        F = open(filename, "w")
        F.write("AIRCRAFT ORIGIN ARRIVAL DEPARTURE DESTINATION AIRLINE\n")
        i = 0
        while i < len(aircrafts):
            ac = aircrafts[i]
            fid = ac.id if ac.id else "-"
            forigen = ac.origin if ac.origin else "-"
            farr = ac.landtime if ac.landtime else "-"
            fdep = ac.departuretime if ac.departuretime else "-"
            fdest = ac.destination if ac.destination else "-"
            fcomp = ac.company if ac.company else "-"

            F.write(f"{fid} {forigen} {farr} {fdep} {fdest} {fcomp}\n")
            i += 1
        F.close()
    except Exception as e:
        print("Error al guardar vols:", e)

################################################################################################################********
################################      LLISTA DE VOLS LLARGS (MÉS DE 2000KM)     ########################################
################################################################################################################********
def LongDistanceArrivals(aircrafts, airports_list):
    from airport import Airport
    i = 0
    LongAircraftFlights = []
    Final = Airport(icao="LEBL", lat=41.29666, lon=2.07833)

    while i < len(aircrafts):
        ICAOorigen = aircrafts[i].origin
        if not ICAOorigen or ICAOorigen == "-":
            i += 1
            continue
        Encontrado = False
        j = 0
        Origen = None
        while j < len(airports_list) and not Encontrado:
            if airports_list[j].icao == ICAOorigen:
                Encontrado = True
                Origen = airports_list[j]
            j += 1

        if Origen and HaversineDistance(Origen, Final) > 2000:
            LongAircraftFlights.append(aircrafts[i])
        i += 1
    return LongAircraftFlights

def HaversineDistance(AirportA, AirportB):
    lat1, lon1 = AirportA.latitude, AirportA.longitude
    lat2, lon2 = AirportB.latitude, AirportB.longitude
    phi1 = lat1 * math.pi / 180
    phi2 = lat2 * math.pi / 180
    R = 6371
    incr_phi = (lat2 - lat1) * math.pi / 180
    incr_lambda = (lon2 - lon1) * math.pi / 180
    a = math.sin(incr_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(incr_lambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

################################################################################################################********
#################################       AVIONS NOCTURNS (NIGHTAIRCRAFT)         ########################################
################################################################################################################********
def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return [], -1
    night_list = []
    for avio in aircrafts:
        if avio.departuretime is not None and (avio.landtime is None or avio.landtime == "-"):
            night_list.append(avio)
    return night_list, 0

################################################################################################################********
#################################       FUSIÓ DE MOVIMENTS (MERGEMOVEMENTS)     ########################################
################################################################################################################********
def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 and len(departures) == 0:
        return [], -1
    merged_list = []
    vols_sortida = list(departures)

    for arr in arrivals:
        if arr.landtime is None or arr.landtime == "-":
            merged_list.append(arr)
            continue
        try:
            arr_horas, arr_mins = map(int, arr.landtime.split(":"))
            temps_arribada = arr_horas * 60 + arr_mins
        except:
            merged_list.append(arr)
            continue

        encontrado = False
        for dep in vols_sortida:
            if dep.id == arr.id:
                if dep.departuretime is None or dep.departuretime == "-":
                    continue
                try:
                    dep_horas, dep_mins = map(int, dep.departuretime.split(":"))
                    temps_sortida = dep_horas * 60 + dep_mins
                except:
                    continue

                if temps_arribada < temps_sortida:
                    fusionat = Aircraft(id=arr.id, company=arr.company, origin=arr.origin,
                                        landtime=arr.landtime, destination=dep.destination,
                                        departuretime=dep.departuretime)
                    merged_list.append(fusionat)
                    vols_sortida.remove(dep)
                    encontrado = True
                    break
        if not encontrado:
            merged_list.append(arr)

    for dep_restant in vols_sortida:
        merged_list.append(dep_restant)

    return merged_list, 0

################################################################################################################********
#################################   INTERFACES INTEGRADAS EN EL FRAME CENTRAL   ########################################
################################################################################################################********
def PlotArrivals(aircrafts, frame_central):
    for widget in frame_central.winfo_children(): widget.destroy()
    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False;
        textos = {"plot_arr_t": "Aterratges per hora", "plot_arr_x": "Hora", "plot_arr_y": "Vols"}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"

    horas = [0] * 24
    for avion in aircrafts:
        if avion.landtime:
            try:
                horas[int(avion.landtime.split(":")[0])] += 1
            except:
                pass

    fig = Figure(figsize=(6, 4), dpi=100, facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)
    ax.bar(range(24), horas, color="#3182ce" if is_dark else "#0056b3")
    ax.set_title(textos["plot_arr_t"], color=fg_color, fontweight='bold')
    ax.set_xlabel(textos["plot_arr_x"], color=fg_color)
    ax.set_ylabel(textos["plot_arr_y"], color=fg_color)
    ax.tick_params(colors=fg_color)
    for spine in ax.spines.values(): spine.set_color(fg_color)

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def PlotAirlines(aircrafts, frame_central, filtro=None):
    for widget in frame_central.winfo_children(): widget.destroy()
    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False;
        textos = {"plot_air_t": "Vols per Aerolínia", "plot_air_x": "CIA", "plot_air_y": "Quantitat"}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"

    cia_map = {}
    for a in aircrafts:
        if a.company: cia_map[a.company] = cia_map.get(a.company, 0) + 1

    nombres, contadores = [], []
    for cia, v in cia_map.items():
        if filtro == "mayor" and v < 5: continue
        if filtro == "menor" and v >= 5: continue
        nombres.append(cia)
        contadores.append(v)

    fig = Figure(figsize=(7, 4), dpi=100, facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)
    if nombres:
        ax.bar(nombres, contadores, color="#38a169" if is_dark else "#2e7d32")
        ax.set_xticklabels(nombres, rotation=90, ha='right', fontsize=8)

    titulo = textos["plot_air_t"]
    if filtro == "mayor":
        titulo += " (>= 5)"
    elif filtro == "menor":
        titulo += " (< 5)"

    ax.set_title(titulo, color=fg_color, fontweight='bold')
    ax.set_ylabel(textos["plot_air_y"], color=fg_color)
    ax.tick_params(colors=fg_color)
    for spine in ax.spines.values(): spine.set_color(fg_color)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def PlotFlightsType(aircrafts, frame_central):
    for widget in frame_central.winfo_children(): widget.destroy()
    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False;
        textos = {"plot_type_t": "Tipus de Vol", "plot_type_y": "Quantitat"}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"

    schengen, no_schengen = 0, 0
    for ac in aircrafts:
        orig_dest = ac.origin if ac.origin else ac.destination
        if orig_dest:
            if IsSchengen(orig_dest):
                schengen += 1
            else:
                no_schengen += 1

    fig = Figure(figsize=(5, 4), dpi=100, facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)

    ax.bar(["Llegadas"], [schengen], color="#3182ce" if is_dark else "#0056b3", label="Schengen")
    ax.bar(["Llegadas"], [no_schengen], bottom=[schengen], color="#e53e3e" if is_dark else "#dc3545",
           label="No-Schengen")

    ax.set_title(textos["plot_type_t"], color=fg_color, fontweight='bold')
    ax.set_ylabel(textos["plot_type_y"], color=fg_color)
    ax.tick_params(colors=fg_color)
    for spine in ax.spines.values(): spine.set_color(fg_color)

    leg = ax.legend(facecolor=bg_color, edgecolor=fg_color)
    for text in leg.get_texts(): text.set_color(fg_color)

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
