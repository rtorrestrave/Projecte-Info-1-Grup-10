# ======================================================================================================================
#
#                  __  ___ ___     ____  _   __      ______ ____   _   __ ______ ____   ____   __
#                 /  |/  //   |   /  _/ / | / /     / ____// __ \ / | / //_  __// __ \ / __ \ / /
#                / /|_/ // /| |   / /  /  |/ /     / /    / / / //  |/ /  / /  / /_/ // / / // /
#               / /  / // ___ | _/ /  / /|  /     / /___ / /_/ // /|  /  / /  / _, _// /_/ // /___
#              /_/  /_//_/  |_|/___/ /_/ |_/      \____/ \____//_/ |_/  /_/  /_/ |_| \____//_____/
#
#
# ======================================================================================================================




import tkinter as tk
from tkinter import messagebox, ttk
from funcionesv4 import *
from airport import *
from aircraft import *
from LEBL import *
from datetime import datetime
import os
import sys

# Variables globals de l'aplicació
airports = []
aircrafts = []
bcn_airport = None
autosave = False
dark_mode = False
frame_grafic_actiu = None
idioma_actual = "ca"
# =======================================================================================================================
#                                    DICCIONARIO GLOBAL DE TRADUCCIONES (i18n)
# =======================================================================================================================
TEXTOS = {
    "ca": {
        "titulo": "AIRPORT MANAGER", "subtitulo": "CENTRE D'OPERACIONS v4.0",
        "btn_dark_l": "MODE CLAR", "btn_dark_d": "MODE FOSC", "btn_idioma": "IDIOMA: CA",
        "management": " GESTIÓ D'AEROPORTS ", "maps": " MAPES KML ", "analytics": " ANÀLISI DE DADES ",
        "import": " IMPORTAR DADES ", "export": " EXPORTACIÓ I AJUSTOS ",
        "info_aero": " INFORMACIÓ AERONÀUTICA EN TEMPS REAL ",
        "btn_add": "Afegir Aeroport", "btn_remove": "Treure Aeroport", "btn_info": "Informació Aeroport",
        "btn_map_ap": "Mapa Aeroports", "btn_map_fl": "Mapa Vols", "btn_plot_sch": "Graficar Schengen",
        "btn_plot_air": "Vols per Aerolínia", "btn_plot_arr": "Hores d'Arribada", "btn_plot_type": "Tipus de Vol",
        "btn_plot_gates": "Mapa Estat de Portes", "btn_plot_evo": "Evolució Portes 24h", "btn_load_all": "CARREGAR TOT",
        "btn_load_ap": "Carregar Aeroports", "btn_load_st": "Carregar Estructura LEBL",
        "btn_load_arr": "Carregar Vols",
        "btn_exp_ap": "Exportar Aeroports", "btn_exp_arr": "Exportar Vols",
        "btn_acars": "Despatxo ACARS", "btn_meteo": "Dades METEO", "btn_aodb": "Informe AODB",
        "auto_on": "Autosave: ACTIVAT", "auto_off": "Autosave: DESACTIVAT",
        "msg_err_ap": "Error: No hi ha aeroports carregats.", "msg_err_fl": "Error: No hi ha vols carregats.",
        "msg_err_both": "Es necessiten vols i aeroports carregats per generar les rutes.",
        "msg_load_ap_ok": "S'han carregat {} aeroports correctament.",
        "msg_load_ap_er": "No s'ha pogut carregar el fitxer d'aeroports.",
        "msg_load_st_ok": "Estructura de l'aeroport LEBL carregada correctament.",
        "msg_load_st_er": "No s'ha pogut carregar l'estructura de LEBL.txt",
        "msg_load_all_ok": "¡Tot carregat correctament!\n\n• {} Aeroports\n• Estructura LEBL\n• {} Vols (Arribades + Sortides Fusionades)",
        "msg_load_all_wa": "S'ha intentat carregar tot, però algun dels fitxers ha fallat.",
        "msg_load_arr_ok": "S'han processat {} vols (Arribades i Sortides fusionades) correctament.",
        "msg_load_arr_er": "No s'ha pogut carregar el fitxer de vols.",
        "msg_exp_ap_ok": "Llista d'aeroports guardada en 'ResultsAirports.txt'.",
        "msg_exp_fl_ok": "Llista de vols guardada en 'ResultsFlights.txt'.",
        "msg_wa_title": "Advertència", "msg_ok_title": "Càrrega Exitosa", "msg_er_title": "Error",
        "tab_schengen": "Schengen", "tab_airlines": "Aerolínies", "tab_hours": "Hores Arribada",
        "tab_types": "Tipus de Vol", "tab_gates": "Mapa Portes", "tab_evo": "Evolució 24h",
        "plot_arr_x": "Hora del dia", "plot_arr_y": "Aterratges", "plot_arr_t": "Aterratges per hora",
        "plot_air_t": "Vols Actius per Aerolínia", "plot_air_y": "Quantitat de Vols", "plot_air_x": "Línies Aèries",
        "plot_type_t": "Tipus de Vol", "plot_type_y": "Quantitat", "plot_lebl_t": "Diagrama de Portes LEBL",
        "lbl_area": "Àrea ",
        "plot_ap_x": "Aeroports", "plot_ap_y": "Quantitat", "plot_ap_t": "Distribució d'Aeroports",
        "pop_title": "Com vols visualitzar les aerolínies?",
        "pop_all": "Veure TOTES (Ordenades de + a -)",
        "pop_high": "Només alta freqüència (>= 5 vols)",
        "pop_group": "Agrupar minoritàries (< 3) a 'ALTRES'",
        "pop_error": "No hi ha cap companyia amb aquest volum de vols.",
        "btn_plot_night": "Mapa Portes en Nocturnitat", "lbl_nocturnitat": "Nocturnitat",
        "msg_open_ge_title": "Obrir a Google Earth",
        "msg_open_ge_body": "El fitxer KML s'ha generat amb èxit. Vols obrir-lo directament a Google Earth?"
    },

    "es": {
        "titulo": "AIRPORT MANAGER", "subtitulo": "CENTRO DE OPERACIONES v4.0",
        "btn_dark_l": "MODE CLARO", "btn_dark_d": "MODE OSCURO", "btn_idioma": "IDIOMA: ES",
        "management": " GESTIÓN DE AEROPUERTOS ", "maps": " MAPAS KML ", "analytics": " DATA ANALYTICS ",
        "import": " IMPORT DATA ", "export": " EXPORT & SETTINGS ",
        "info_aero": " INFORMACIÓN AERONÁUTICA EN TIEMPO REAL",
        "btn_add": "Añadir Aeropuerto", "btn_remove": "Quitar Aeropuerto", "btn_info": "Información Aeropuerto",
        "btn_map_ap": "Mapa Aeropuertos", "btn_map_fl": "Mapa Vuelos", "btn_plot_sch": "Graficar Schengen",
        "btn_plot_air": "Vuelos por Aerolínea", "btn_plot_arr": "Horas de Llegada", "btn_plot_type": "Tipos de Vuelo",
        "btn_plot_gates": "Mapa Estado de Puertas", "btn_plot_evo": "Evolución Puertas 24h", "btn_load_all": "CARGAR TODO",
        "btn_load_ap": "Cargar Aeropuertos", "btn_load_st": "Cargar Estructura LEBL",
        "btn_load_arr": "Cargar Vuelos (Fusión)",
        "btn_exp_ap": "Exportar Aeropuertos", "btn_exp_arr": "Exportar Vuelos",
        "btn_acars": "Despacho ACARS", "btn_meteo": "Datos METEO", "btn_aodb": "Informe AODB",
        "auto_on": "Autosave: ACTIVADO", "auto_off": "Autosave: DESACTIVADO",
        "msg_err_ap": "Error: No existen aeropuertos cargados.", "msg_err_fl": "Error: No existen vuelos cargados.",
        "msg_err_both": "Se necesitan vuelos y aeropuertos cargados para generar las rutas.",
        "msg_load_ap_ok": "Se han cargado {} aeropuertos correctamente.",
        "msg_load_ap_er": "No se pudo cargar el archivo de aeropuertos.",
        "msg_load_st_ok": "Estructura del aeropuerto LEBL cargada correctamente.",
        "msg_load_st_er": "No se pudo cargar la estructura de LEBL.txt",
        "msg_load_all_ok": "¡Todo cargado correctamente!\n\n• {} Aeropuertos\n• Estructura LEBL\n• {} Vuelos (Arribadas + Salidas Fusionadas)",
        "msg_load_all_wa": "Se intentó cargar todo, pero algún archivo falló.",
        "msg_load_arr_ok": "Se han procesado {} vuelos (Llegadas y Salidas fusionadas) correctamente.",
        "msg_load_arr_er": "No se pudo cargar el archivo de vuelos.",
        "msg_exp_ap_ok": "Lista de aeropuertos guardada en 'ResultsAirports.txt'.",
        "msg_exp_fl_ok": "Lista de vuelos guardada en 'ResultsFlights.txt'.",
        "msg_wa_title": "Advertencia", "msg_ok_title": "Carga Exitosa", "msg_er_title": "Error",
        "tab_schengen": "Schengen", "tab_airlines": "Aerolíneas", "tab_hours": "Horas Llegada",
        "tab_types": "Tipos de Vuelo", "tab_gates": "Mapa Puertas", "tab_evo": "Evolución 24h",
        "plot_arr_x": "Hora del día", "plot_arr_y": "Aterrizajes", "plot_arr_t": "Aterrizajes por hora",
        "plot_air_t": "Vuelos Activos por Aerolínea", "plot_air_y": "Cantidad de Vuelos", "plot_air_x": "Líneas Aéreas",
        "plot_type_t": "Tipos de Vuelo", "plot_type_y": "Cantidad", "plot_lebl_t": "Diagrama de Puertas LEBL",
        "lbl_area": "Area ",
        "plot_ap_x": "Aeropuertos", "plot_ap_y": "Cantidad", "plot_ap_t": "Distribución de Aeropuertos",
        "pop_title": "¿Cómo deseas visualizar las aerolíneas?",
        "pop_all": "Ver TODAS (Ordenadas de + a -)",
        "pop_high": "Solo alta frecuencia (>= 5 vuelos)",
        "pop_group": "Agrupar minoritarias (< 3) en 'ALTRES'",
        "pop_error": "No hay ninguna compañía con ese volumen de vuelos.",
        "btn_plot_night": "Mapa Puertas en Nocturnidad", "lbl_nocturnitat": "Nocturnidad",
        "msg_open_ge_title": "Abrir en Google Earth",
        "msg_open_ge_body": "El archivo KML se ha generado con éxito. ¿Deseas abrirlo directamente en Google Earth?"
    },

    "en": {
        "titulo": "AIRPORT MANAGER", "subtitulo": "OPERATIONS CENTER v4.0",
        "btn_dark_l": "LIGHT MODE", "btn_dark_d": "DARK MODE", "btn_idioma": "LANGUAGE: EN",
        "management": " AIRPORT MANAGEMENT ", "maps": " KML MAPS ", "analytics": " DATA ANALYTICS ",
        "import": " IMPORT DATA ", "export": " EXPORT & SETTINGS ",
        "info_aero": " REAL-TIME AERONAUTICAL INFO ",
        "btn_add": "Add Airport", "btn_remove": "Remove Airport", "btn_info": "Airport Info",
        "btn_map_ap": "Airport Map", "btn_map_fl": "Flights Map", "btn_plot_sch": "Plot Schengen",
        "btn_plot_air": "Flights by Airline", "btn_plot_arr": "Arrival Hours", "btn_plot_type": "Flight Types",
        "btn_plot_gates": "Gate Map", "btn_plot_evo": "Gate Evolution 24h", "btn_load_all": "LOAD ALL DATA",
        "btn_load_ap": "Load Airports", "btn_load_st": "Load LEBL Structure", "btn_load_arr": "Load Flights (Merge)",
        "btn_exp_ap": "Export Airports", "btn_exp_arr": "Export Flights",
        "btn_acars": "ACARS Dispatch", "btn_meteo": "METEO Data", "btn_aodb": "AODB Report",
        "auto_on": "Autosave: ENABLED", "auto_off": "Autosave: DISABLED",
        "msg_err_ap": "Error: No airports loaded.", "msg_err_fl": "Error: No flights loaded.",
        "msg_err_both": "Flights and airports must be loaded to generate routes.",
        "msg_load_ap_ok": "{} airports loaded successfully.", "msg_load_ap_er": "Could not load airports file.",
        "msg_load_st_ok": "LEBL airport structure loaded successfully.",
        "msg_load_st_er": "Could not load LEBL.txt structure.",
        "msg_load_all_ok": "All data loaded successfully!\n\n• {} Airports\n• LEBL Structure\n• {} Flights (Merged Arrivals + Departures)",
        "msg_load_all_wa": "Attempted to load everything, but some files failed. Check files.",
        "msg_load_arr_ok": "{} flights (Arrivals and Departures merged) processed successfully.",
        "msg_load_arr_er": "Could not load flights file.",
        "msg_exp_ap_ok": "Airport list saved in 'ResultsAirports.txt'.",
        "msg_exp_fl_ok": "Flights list saved in 'ResultsFlights.txt'.",
        "msg_wa_title": "Warning", "msg_ok_title": "Load Successful", "msg_er_title": "Error",
        "tab_schengen": "Schengen", "tab_airlines": "Airlines", "tab_hours": "Arrival Hours",
        "tab_types": "Flight Types", "tab_gates": "Gate Map", "tab_evo": "24h Evolution",
        "plot_arr_x": "Hour of the day", "plot_arr_y": "Landings", "plot_arr_t": "Landings per hour",
        "plot_air_t": "Active Flights by Airline", "plot_air_y": "Number of Flights", "plot_air_x": "Airlines",
        "plot_type_t": "Flight Types", "plot_type_y": "Quantity", "plot_lebl_t": "Barcelona Airport Gate Diagram",
        "lbl_area": "Area ",
        "plot_ap_x": "Airports", "plot_ap_y": "Quantity", "plot_ap_t": "Airport Distribution",
        "pop_title": "How do you want to visualize the airlines?",
        "pop_all": "Show ALL (Sorted from + to -)",
        "pop_high": "High frequency only (>= 5 flights)",
        "pop_group": "Group minor airlines (< 3) into 'ALTRES'",
        "pop_error": "There are no companies with that amount of flights.",
        "btn_plot_night": "Night Gate Map", "lbl_nocturnitat": "Night Stay",
        "msg_open_ge_title": "Open in Google Earth",
        "msg_open_ge_body": "The KML file has been successfully generated. Do you want to open it directly in Google Earth?"
    }
}
# =======================================================================================================================
#                                    FUNCIONES DE INTERFAZ (LOGICA DE BOTONES)
# =======================================================================================================================
def load_file():
    global airports
    t = TEXTOS[idioma_actual]
    airports = LoadAirports("airports.txt")
    if airports:
        messagebox.showinfo(t["msg_ok_title"], t["msg_load_ap_ok"].format(len(airports)))
    else:
        messagebox.showerror(t["msg_er_title"], t["msg_load_ap_er"])

def load_file_structure():
    global bcn_airport
    t = TEXTOS[idioma_actual]
    bcn_airport = LoadAirportStructure("LEBL.txt")
    if bcn_airport != -1 and bcn_airport is not None:
        messagebox.showinfo(t["msg_ok_title"], t["msg_load_st_ok"])
    else:
        messagebox.showerror(t["msg_er_title"], t["msg_load_st_er"])

def load_arrivals():
    global aircrafts
    t = TEXTOS[idioma_actual]
    arr_raw = LoadArrivals("Arrivals.txt")
    dep_raw, code = LoadDepartures("Departures.txt")

    # Executem la unió dinàmica dissenyada per en Joan
    aircrafts, code_m = MergeMovements(arr_raw, dep_raw)
    if code_m == 0 and aircrafts:
        messagebox.showinfo(t["msg_ok_title"], t["msg_load_arr_ok"].format(len(aircrafts)))
    else:
        messagebox.showerror(t["msg_er_title"], t["msg_load_arr_er"])

def load_all_data():
    global airports, bcn_airport, aircrafts
    t = TEXTOS[idioma_actual]
    airports = LoadAirports("airports.txt")
    bcn_airport = LoadAirportStructure("LEBL.txt")
    arr_raw = LoadArrivals("Arrivals.txt")
    dep_raw, code = LoadDepartures("Departures.txt")
    aircrafts, code_m = MergeMovements(arr_raw, dep_raw)

    if airports and (bcn_airport != -1 and bcn_airport is not None) and code_m == 0:
        messagebox.showinfo(t["msg_ok_title"], t["msg_load_all_ok"].format(len(airports), len(aircrafts)))
    else:
        messagebox.showwarning(t["msg_wa_title"], t["msg_load_all_wa"])

def export_file():
    global airports
    t = TEXTOS[idioma_actual]
    if not airports:
        messagebox.showwarning(t["msg_wa_title"], t["msg_err_ap"])
    else:
        SaveAirportList(airports, "ResultsAirports.txt")
        messagebox.showinfo(t["msg_ok_title"], t["msg_exp_ap_ok"])

def export_arrivals():
    global aircrafts
    t = TEXTOS[idioma_actual]
    if not aircrafts:
        messagebox.showwarning(t["msg_wa_title"], t["msg_err_fl"])
    else:
        SaveFlights(aircrafts, "ResultsFlights.txt")
        messagebox.showinfo(t["msg_ok_title"], t["msg_exp_fl_ok"])

def toggle_autosave():
    global autosave
    t = TEXTOS[idioma_actual]
    autosave = not autosave
    if autosave:
        btn_autosave.config(text=t["auto_on"], bg="#2e7d32")
    else:
        btn_autosave.config(text=t["auto_off"], bg="#4a5568" if not dark_mode else "#2d3748")

def add_airport():
    global airports

    # Diàleg interactiu per no deixar els botons com a simples simulacres vacis
    def guardar():
        try:
            ap = Airport(e_icao.get(), float(e_lat.get()), float(e_lon.get()))
            AddAirport(airports, ap)
            win.destroy()
        except:
            messagebox.showerror("Error", "Dades incorrectes.")

    win = tk.Toplevel(root);
    win.title("Add Airport");
    win.geometry("300x200")
    tk.Label(win, text="ICAO:").pack();
    e_icao = tk.Entry(win);
    e_icao.pack()
    tk.Label(win, text="Latitud:").pack();
    e_lat = tk.Entry(win);
    e_lat.pack()
    tk.Label(win, text="Longitud:").pack();
    e_lon = tk.Entry(win);
    e_lon.pack()
    tk.Button(win, text="Afegir", command=guardar, bg="#4a5568", fg="white").pack(pady=10)

def remove_airport():
    global airports
    win = tk.Toplevel(root);
    win.title("Remove Airport");
    win.geometry("300x120")
    tk.Label(win, text="ICAO a esborrar:").pack()
    e_icao = tk.Entry(win);
    e_icao.pack()

    def esborrar():
        global airports
        airports = RemoveAirports(airports, e_icao.get())
        win.destroy()

    tk.Button(win, text="Eliminar", command=esborrar, bg="#c62828", fg="white").pack(pady=10)

def buscar_airport():
    global airports
    win = tk.Toplevel(root);
    win.title("Info Airport");
    win.geometry("300x150")
    tk.Label(win, text="ICAO a buscar:").pack()
    e_icao = tk.Entry(win);
    e_icao.pack()

    def cercar():
        for ap in airports:
            if ap.icao == e_icao.get().upper():
                messagebox.showinfo("Airport Encontrado",
                                    f"ICAO: {ap.icao}\nLat: {ap.latitude}\nLon: {ap.longitude}\nSchengen: {ap.schengen}")
                return
        messagebox.showwarning("Error", "No s'ha trobat l'aeroport.")

    tk.Button(win, text="Cercar", command=cercar).pack(pady=10)

def abrir_kml_en_google_earth(ruta_archivo, t):
    # Pregunta al usuario si quiere abrirlo (Sí/No) usando el idioma actual
    respuesta = messagebox.askyesno(t["msg_open_ge_title"], t["msg_open_ge_body"])

    if respuesta:  # Si el usuario pulsa "SÍ"
        try:
            if sys.platform == "win32":
                os.startfile(ruta_archivo)  # Comando para Windows
            elif sys.platform == "darwin":
                os.system(f"open {ruta_archivo}")  # Comando para Mac
            else:
                os.system(f"xdg-open {ruta_archivo}")  # Comando para Linux
        except Exception as e:
            messagebox.onerror("Error", f"No se pudo abrir Google Earth: {e}")

def map_airports():
    global airports
    t = TEXTOS[idioma_actual]
    if not airports:
        messagebox.showwarning(t["msg_wa_title"], t["msg_err_ap"])
    else:
        MapAirports(airports)
        # En vez del antiguo showinfo estático, ejecuta la lógica con la pregunta
        abrir_kml_en_google_earth("mapairports.kml", t)

def map_flights():
    global aircrafts, airports
    t = TEXTOS[idioma_actual]
    if not aircrafts or not airports:
        messagebox.showwarning(t["msg_wa_title"], t["msg_err_both"])
    else:
        MapFlights(aircrafts, airports)
        # En vez del antiguo showinfo estático, ejecuta la lógica con la pregunta
        abrir_kml_en_google_earth("routes.kml", t)

def plot_airports():
    global airports
    t = TEXTOS[idioma_actual]
    if not airports:
        messagebox.showinfo("Error al graficar", t["msg_err_ap"])
    else:
        afegir_pestanya(t["tab_schengen"], PlotAirports, airports)

def plot_airlines(dades=None, frame=None):
    global aircrafts, idioma_actual, dark_mode
    t = TEXTOS[idioma_actual]

    # ===================================================================================
    # CAS A: REDIBUIX INSTANTANI (Invocat pel teu refrescar_grafico_actual)
    # ===================================================================================
    if frame is not None:
        # Recuperem el filtre guardat a la memòria de la funció (per defecte "totes")
        tipus_filtre = getattr(plot_airlines, "filtre", "totes")

        # Netejar completament el contingut del frame per evitar solapaments
        for widget in frame.winfo_children():
            widget.destroy()

        is_dark = dark_mode
        bg_color = "#1a1d26" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#1a1f2c"

        # Comptar i ordenar les companyies aèries
        companyies_comptat = {}
        for ac in aircrafts:
            comp = ac.company.strip().upper() if ac.company else "DESCONEGUDA"
            companyies_comptat[comp] = companyies_comptat.get(comp, 0) + 1

        ordenades = sorted(companyies_comptat.items(), key=lambda x: x[1], reverse=True)

        names = []
        counts = []
        extensio_titol = ""

        if tipus_filtre == "totes":
            names = [x[0] for x in ordenades]
            counts = [x[1] for x in ordenades]
            extensio_titol = " (All)" if idioma_actual == "en" else " (Totes)"
        elif tipus_filtre == "principals":
            limit_tall = 5
            for comp, num in ordenades:
                if num >= limit_tall:
                    names.append(comp)
                    counts.append(num)
            extensio_titol = f" (>={limit_tall})"
        elif tipus_filtre == "agrupar":
            limit_agrupacio = 3
            vols_altres = 0
            for comp, num in ordenades:
                if num >= limit_agrupacio:
                    names.append(comp)
                    counts.append(num)
                else:
                    vols_altres += num
            if vols_altres > 0:
                names.append("ALTRES")
                counts.append(vols_altres)
            extensio_titol = " (Grouped)" if idioma_actual == "en" else " (Agrupat)"

        # Renderitzat del gràfic Matplotlib amb els colors actualitzats
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig = Figure(figsize=(10, 5), dpi=100, facecolor=bg_color)
        ax = fig.add_subplot(111, facecolor=bg_color)

        bar_colors = ["#718096" if name == "ALTRES" else ("#3182ce" if not is_dark else "#63b3ed") for name in names]
        bars = ax.bar(names, counts, color=bar_colors)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.1, f'{int(yval)}',
                    ha='center', va='bottom', fontsize=8, color=fg_color, fontweight='bold')

        ax.set_title(t["btn_plot_air"] + extensio_titol, color=fg_color, fontweight='bold', fontsize=12)
        ax.set_ylabel(t["plot_air_y"], color=fg_color, fontweight='bold')

        ax.set_xticklabels(names, rotation=45, ha='right', color=fg_color, fontsize=9)
        ax.tick_params(colors=fg_color)
        for spine in ax.spines.values():
            spine.set_color(fg_color)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return

    # ===================================================================================
    # CAS B: PRIMERA OBERTURA (Quan l'usuari clica el botó del menú inferior)
    # ===================================================================================
    if not aircrafts:
        messagebox.showwarning(t["msg_wa_title"], t["msg_err_fl"])
        return

    # Generació de la finestra de filtre (Pop-up)
    win_pop = tk.Toplevel(root)
    win_pop.title("Filter")
    win_pop.resizable(False, False)

    bg_pop = "#1a1f2c" if dark_mode else "#f1f3f5"
    fg_pop = "#f8fafc" if dark_mode else "#1a1f2c"
    win_pop.configure(bg=bg_pop)

    win_pop.update_idletasks()
    amplada_pop = 420
    alçada_pop = 240
    pos_x = (win_pop.winfo_screenwidth() // 2) - (amplada_pop // 2)
    pos_y = (win_pop.winfo_screenheight() // 2) - (alçada_pop // 2)
    win_pop.geometry(f"{amplada_pop}x{alçada_pop}+{pos_x}+{pos_y}")

    win_pop.transient(root)
    win_pop.grab_set()

    lbl_titol = tk.Label(win_pop, text=t["pop_title"], font=("Segoe UI", 11, "bold"), bg=bg_pop, fg=fg_pop)
    lbl_titol.pack(pady=15)

    def aplicar_i_obrir(opcio):
        plot_airlines.filtre = opcio
        win_pop.destroy()
        # Obrim la pestanya demanant que s'auto-executi el Cas A passant-se el frame
        afegir_pestanya(t["tab_airlines"], lambda d, f: plot_airlines(d, f), None)

    tk.Button(win_pop, text=t["pop_all"], bg="#3182ce", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2",
              pady=6, command=lambda: aplicar_i_obrir("totes")).pack(fill=tk.X, padx=40, pady=6)

    tk.Button(win_pop, text=t["pop_high"], bg="#2e7d32", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2",
              pady=6, command=lambda: aplicar_i_obrir("principals")).pack(fill=tk.X, padx=40, pady=6)

    tk.Button(win_pop, text=t["pop_group"], bg="#dd6b20", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2",
              pady=6, command=lambda: aplicar_i_obrir("agrupar")).pack(fill=tk.X, padx=40, pady=6)

def plot_arrival_time():
    global aircrafts
    t = TEXTOS[idioma_actual]
    if not aircrafts:
        messagebox.showinfo("Error al graficar", t["msg_err_fl"])
    else:
        afegir_pestanya(t["tab_hours"], PlotArrivals, aircrafts)

def plot_flight_type():
    global aircrafts
    t = TEXTOS[idioma_actual]
    if not aircrafts:
        messagebox.showinfo("Error al graficar", t["msg_err_fl"])
    else:
        afegir_pestanya(t["tab_types"], PlotFlightsType, aircrafts)

def plot_gates_map():
    global bcn_airport, aircrafts
    t = TEXTOS[idioma_actual]

    # Validació de seguretat en cas de demanar el gràfic abans de polsar Cargar Tot
    if bcn_airport is None:
        bcn_airport = LoadAirportStructure("LEBL.txt")
    if bcn_airport == -1 or bcn_airport is None:
        messagebox.showerror("Error", "No es pot carregar l'estructura del fitxer LEBL.txt")
        return

    if not aircrafts:
        messagebox.showwarning("Avís", t["msg_err_fl"])
        return

    # Llançar la vista dinàmica on l'Slider s'auto-injecta a la part inferior
    afegir_pestanya(t["tab_gates"], lambda dades, f: PlotGatesMap(bcn_airport, aircrafts, f), None)

# =======================================================================================================================
#                                    LOGICA DE CAMBIO DE MODO (DARK / LIGHT)
# =======================================================================================================================
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    t = TEXTOS[idioma_actual]

    if dark_mode:
        bg_main, bg_card, fg_text, bg_btn, fg_btn = "#12141c", "#1a1d26", "#e2e8f0", "#2d3748", "#f8fafc"
        color_rellotge = "#00FF00"  # Verde fosforito radionavegación para modo oscuro
        btn_toggle_text = t["btn_dark_l"]
        style.configure('TNotebook', background=bg_main)
        style.configure('TNotebook.Tab', background='#2d3748', foreground='#a0aec0', bordercolor='#1a1d26')
        style.map('TNotebook.Tab', background=[('selected', '#1a1d26')], foreground=[('selected', '#ffffff')])
    else:
        bg_main, bg_card, fg_text, bg_btn, fg_btn = "#f1f3f5", "#ffffff", "#2d3748", "#4a5568", "#f8fafc"
        color_rellotge = "#1E3A8A"  # Azul marino corporativo para modo claro
        btn_toggle_text = t["btn_dark_d"]
        style.configure('TNotebook', background=bg_main)
        style.configure('TNotebook.Tab', background='#e9ecef', foreground='#495057', bordercolor='#dee2e6')
        style.map('TNotebook.Tab', background=[('selected', '#ffffff')], foreground=[('selected', '#1a1f2c')])

    root.configure(bg=bg_main)
    frame_central.configure(bg=bg_main)
    frame_inferior.configure(bg=bg_main)
    btn_dark_toggle.config(text=btn_toggle_text)

    # =========================================================================
    # MODIFICACIÓN: Inyectamos tu nuevo frame en la lista automatizada
    # =========================================================================
    seccions = [
        frame_AirportManagement,
        frame_Maps,
        frame_Plots,
        frame_FileManagement_Load,
        frame_FileManagement_Export,
        frame_InfoAeronautica  # <--- ¡Añadido aquí!
    ]

    for seccio in seccions:
        seccio.configure(bg=bg_card, fg=fg_text)
        for widget in seccio.winfo_children():
            if isinstance(widget, tk.Button) and widget != btn_autosave:
                widget.configure(bg=bg_btn, fg=fg_btn)

    # =========================================================================
    # MODIFICACIÓN: Forzamos al reloj a cambiar su color de fondo y de texto
    # =========================================================================
    try:
        lbl_rellotge_live.configure(bg=bg_card, fg=color_rellotge)
    except Exception:
        pass

    refrescar_grafico_actual()

    try:
        import LEBL
        if LEBL._actualitzar_mapa_global_fn is not None:
            LEBL._actualitzar_mapa_global_fn()
    except Exception as e:
        print("El mapa encara no s'ha creat o ha donat error:", e)

def refrescar_grafico_actual():
    try:
        pestanya_activa_id = notebook.select()
        if pestanya_activa_id and frame_grafic_actiu is not None:
            nom_pestanya_raw = notebook.tab(pestanya_activa_id, "text").strip()
            color_fons_marcs = "#1a1d26" if dark_mode else "white"
            color_barra_sup = "#12141c" if dark_mode else "#f8f9fa"
            color_text_sup = "#a0aec0" if dark_mode else "#6c757d"
            color_btn_tancar = "#2d3748" if dark_mode else "#e9ecef"
            color_fg_tancar = "#e2e8f0" if dark_mode else "#495057"

            frame_pestanya_actual = notebook.nametowidget(pestanya_activa_id)
            frame_pestanya_actual.configure(bg=color_fons_marcs)
            frame_grafic_actiu.configure(bg=color_fons_marcs)

            for fill in frame_pestanya_actual.winfo_children():
                if isinstance(fill, tk.Frame) and fill.pack_info().get('side') == 'top':
                    fill.configure(bg=color_barra_sup)
                    for subfill in fill.winfo_children():
                        if isinstance(subfill, tk.Label):
                            subfill.configure(bg=color_barra_sup, fg=color_text_sup)
                        elif isinstance(subfill, tk.Button):
                            subfill.configure(bg=color_btn_tancar, fg=color_fg_tancar)

            is_gates = any(nom_pestanya_raw == TEXTOS[lang]["tab_gates"] for lang in TEXTOS)
            is_schengen = any(nom_pestanya_raw == TEXTOS[lang]["tab_schengen"] for lang in TEXTOS)
            is_airlines = any(nom_pestanya_raw == TEXTOS[lang]["tab_airlines"] for lang in TEXTOS)
            is_hours = any(nom_pestanya_raw == TEXTOS[lang]["tab_hours"] for lang in TEXTOS)
            is_types = any(nom_pestanya_raw == TEXTOS[lang]["tab_types"] for lang in TEXTOS)
            is_evo = any(nom_pestanya_raw == TEXTOS[lang]["tab_evo"] for lang in TEXTOS)

            if is_gates and bcn_airport:
                import copy
                b_cp = copy.deepcopy(bcn_airport)
                AssignNightGates(b_cp, aircrafts)
                for h in range(9): AssignGatesAtTime(b_cp, aircrafts, f"{h:02d}:00")
                PlotGatesMap(GateOccupancy(b_cp), frame_grafic_actiu)
            elif is_schengen and airports:
                PlotAirports(airports, frame_grafic_actiu)
            elif is_airlines and aircrafts:
                plot_airlines(aircrafts, frame_grafic_actiu)
            elif is_hours and aircrafts:
                PlotArrivals(aircrafts, frame_grafic_actiu)
            elif is_types and aircrafts:
                PlotFlightsType(aircrafts, frame_grafic_actiu)
            elif is_evo and bcn_airport:
                PlotDayOccupancy(bcn_airport, aircrafts, frame_grafic_actiu)
    except Exception as e:
        print("Error refreshing live viewport canvas:", e)

# =======================================================================================================================
#                                    FUNCIÓN DE CAMBIO DE IDIOMA (MÈTODE DE COMMUTACIÓ)
# =======================================================================================================================
def toggle_language():
    global idioma_actual
    idioma_actual = "es" if idioma_actual == "ca" else ("en" if idioma_actual == "es" else "ca")
    t = TEXTOS[idioma_actual]

    lbl_titulo.config(text=t["titulo"])
    lbl_version.config(text=t["subtitulo"])
    btn_lang_toggle.config(text=t["btn_idioma"])
    btn_dark_toggle.config(text=t["btn_dark_l"] if dark_mode else t["btn_dark_d"])

    frame_AirportManagement.config(text=t["management"])
    frame_Maps.config(text=t["maps"])
    frame_Plots.config(text=t["analytics"])
    frame_FileManagement_Load.config(text=t["import"])
    frame_FileManagement_Export.config(text=t["export"])

    # Remapeig de botons de seccions per traducció directa
    for widget in frame_AirportManagement.winfo_children():
        if isinstance(widget, tk.Button):
            if "Añadir" in widget.cget("text") or "Afegir" in widget.cget("text") or "Add" in widget.cget("text"):
                widget.config(text=t["btn_add"])
            elif "Quitar" in widget.cget("text") or "Treure" in widget.cget("text") or "Remove" in widget.cget("text"):
                widget.config(text=t["btn_remove"])
            elif "Información" in widget.cget("text") or "Info" in widget.cget("text"):
                widget.config(text=t["btn_info"])
    for widget in frame_Maps.winfo_children():
        if isinstance(widget, tk.Button):
            if "Vuel" in widget.cget("text") or "Vols" in widget.cget("text") or "Flight" in widget.cget("text"):
                widget.config(text=t["btn_map_fl"])
            else:
                widget.config(text=t["btn_map_ap"])
    for widget in frame_Plots.winfo_children():
        if isinstance(widget, tk.Button):
            txt = widget.cget("text")
            if "Schen" in txt:
                widget.config(text=t["btn_plot_sch"])
            elif "Aerol" in txt or "Airline" in txt:
                widget.config(text=t["btn_plot_air"])
            elif "Hor" in txt or "Hours" in txt:
                widget.config(text=t["btn_plot_arr"])
            elif "Tip" in txt or "Type" in txt:
                widget.config(text=t["btn_plot_type"])

            elif "Night" in txt or "Nocturn" in txt or "Pernoct" in txt or "OVERNIGHTS" in txt:
                widget.config(text=t["btn_plot_night"])

            elif "Puert" in txt or "Porte" in txt or "Gate" in txt:
                widget.config(text=t["btn_plot_gates"])

            elif "Evol" in txt or "24h" in txt:
                widget.config(text=t["btn_plot_evo"])

    for widget in frame_FileManagement_Load.winfo_children():
        if isinstance(widget, tk.Button):
            txt = widget.cget("text")
            if "TODO" in txt or "TOT" in txt or "ALL" in txt:
                widget.config(text=t["btn_load_all"])
            elif "Estruct" in txt or "Struct" in txt:
                widget.config(text=t["btn_load_st"])
            elif "Lleg" in txt or "Arrib" in txt or "Arriv" in txt:
                widget.config(text=t["btn_load_arr"])
            else:
                widget.config(text=t["btn_load_ap"])
    for widget in frame_FileManagement_Export.winfo_children():
        if isinstance(widget, tk.Button):
            if "Aerop" in widget.cget("text") or "Airp" in widget.cget("text"):
                widget.config(text=t["btn_exp_ap"])
            elif "Lleg" in widget.cget("text") or "Arri" in widget.cget("text") or "Arriv" in widget.cget(
                "text") or "Vols" in widget.cget("text") or "Vuel" in widget.cget("text"):
                widget.config(text=t["btn_exp_arr"])


    btn_autosave.config(text=t["auto_on"] if autosave else t["auto_off"])
    try:
        for i in range(notebook.index("end")):
            txt_pestanya = notebook.tab(i, "text")

            if "Map" in txt_pestanya or "Nocturn" in txt_pestanya or "Pernoct" in txt_pestanya:
                notebook.tab(i, text=t.get("btn_plot_night", "Night Gates Map"))
    except Exception:
        pass
    refrescar_grafico_actual()
# ===========================================================# INYECCIÓN ADAPTADA PARA TU NUEVA SECCIÓN AERONÁUTICA

    frame_InfoAeronautica.config(text=t["info_aero"])
    for widget in frame_InfoAeronautica.winfo_children():
        if isinstance(widget, tk.Button):
            txt = widget.cget("text")

            if "ACARS" in txt:
                widget.config(text=t["btn_acars"])
            elif "METEO" in txt or "Dades" in txt or "Datos" in txt:
                widget.config(text=t["btn_meteo"])
            elif "AODB" in txt or "Informe" in txt or "Report" in txt:
                widget.config(text=t["btn_aodb"])

# =======================================================================================================================
#                                    RELLOTGE EN TEMPS REAL PER ACARS I AODB
# =======================================================================================================================


# Funció auxiliar que aconsegueix l'hora formatejada al vol quan es prem el botó
def obtenir_hora_actual_sim():
    # Retorna l'hora del sistema en format "HH:00" per no trencar la teva lògica de filtres
    return f"{datetime.now().hour}:00"
# =======================================================================================================================
#                                    DESPACHO ACARS EN TIEMPO REAL
# =======================================================================================================================

def executar_despatxo_acars_en_temps_real():
    # Conseguimos el diccionario del idioma que esté activo JUSTO AHORA
    t_actual = TEXTOS[idioma_actual]

    if bcn_airport is None:
        messagebox.showwarning(t_actual["msg_wa_title"], t_actual["msg_err_ap"])
        return

    hora_del_rellotge = obtenir_hora_actual_sim()
    try:
        AssignGatesAtTime(bcn_airport, aircrafts, hora_del_rellotge)
    except Exception:
        pass

    # Le pasamos t_actual a la función a través de la lambda
    afegir_pestanya(
        "ACARS Datalink",
        lambda d, f: GenerateACARSMsg(bcn_airport, aircrafts, hora_del_rellotge, frame=f, t=t_actual),
        None
    )

def executar_meteo_segura():
    t_actual = TEXTOS[idioma_actual]

    # El primer escudo por si acaso
    if bcn_airport is None:
        messagebox.showwarning(t_actual["msg_wa_title"], t_actual["msg_err_ap"])
        return

    afegir_pestanya(
        "METEO Live",
        lambda d, f: FetchAirportLiveStatus(bcn_airport, frame=f, t=t_actual),
        None
    )

def executar_aodb_segura():
    t_actual = TEXTOS[idioma_actual]

    if bcn_airport is None or not aircrafts:
        messagebox.showwarning(t_actual["msg_wa_title"], t_actual["msg_err_fl"])
        return

    nom_fitxer = f"Reporte_Estadisticas_{bcn_airport.code}.txt"

    afxer = afegir_pestanya("AODB Audit",lambda d, f: ExportExecutiveReport(bcn_airport, aircrafts, nom_fitxer, frame=f, t=t_actual),None)

# =======================================================================================================================
#                                    NOCTURNITATS A BARCELONA
# =======================================================================================================================
def executar_mapa_nocturn_gates():
    t_actual = TEXTOS[idioma_actual]
    if bcn_airport is None:
        messagebox.showwarning(t_actual["msg_wa_title"], t_actual["msg_err_ap"])
        return

    # Inyección directa a la nueva función sin slider y con textos fijos de Nocturnidad
    afegir_pestanya(
        "Night Gates Map",
        lambda d, f: PlotNightGatesMap(bcn_airport, aircrafts, frame_central=f),
        None
    )
# =======================================================================================================================
#                                    CONFIGURACIÓN DE L'ESTIL I FINESTRA PRINCIPAL
# =======================================================================================================================
root = tk.Tk()
root.title("AirportManager v4.0 - Operacions Integrades")
root.geometry("1280x720")
root.state('zoomed')
root.configure(bg="#f1f3f5")

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background='#f1f3f5', borderwidth=0)
style.configure('TNotebook.Tab', background='#e9ecef', foreground='#495057', padding=[18, 6],
                font=('Segoe UI', 9, 'bold'), borderwidth=1, bordercolor='#dee2e6')
style.map('TNotebook.Tab', background=[('selected', '#ffffff')], foreground=[('selected', '#1a1f2c')])

def on_enter(e):
    if e.widget['state'] != 'disabled' and e.widget['bg'] not in ["#2e7d32", "#c62828"]: e.widget[
        'bg'] = '#1a202c' if not dark_mode else '#4a5568'

def on_leave(e):
    if e.widget['state'] != 'disabled' and e.widget['bg'] not in ["#2e7d32", "#c62828"]: e.widget[
        'bg'] = '#4a5568' if not dark_mode else '#2d3748'

def crear_boto_modern(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, font=("Segoe UI", 9, "bold"), bg="#4a5568", fg="#f8fafc", bd=0,
                    relief="flat", activebackground="#1a202c", activeforeground="white", cursor="hand2", pady=5)
    btn.bind("<Enter>", on_enter);
    btn.bind("<Leave>", on_leave)
    return btn

# Layout Estructural
frame_header = tk.Frame(root, bg="#1a1f2c", height=60);
frame_header.pack(side=tk.TOP, fill=tk.X);
frame_header.pack_propagate(False)
frame_central = tk.Frame(root, bg="#ffffff");
frame_central.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
notebook = ttk.Notebook(frame_central, style='TNotebook');
notebook.pack(fill=tk.BOTH, expand=True)
frame_inferior = tk.Frame(root, bg="#f1f3f5");
frame_inferior.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

def afegir_pestanya(titol_pestanya, funcio_grafic, dades):
    global frame_grafic_actiu
    bg_pestanya = "#1a1d26" if dark_mode else "white"
    bg_barra = "#12141c" if dark_mode else "#f8f9fa"
    fg_barra = "#a0aec0" if dark_mode else "#6c757d"
    bg_boto_tancar = "#2d3748" if dark_mode else "#e9ecef"
    fg_boto_tancar = "#e2e8f0" if dark_mode else "#495057"

    frame_pestanya = tk.Frame(notebook, bg=bg_pestanya)
    barra_control = tk.Frame(frame_pestanya, bg=bg_barra, height=28);
    barra_control.pack(side=tk.TOP, fill=tk.X);
    barra_control.pack_propagate(False)
    lbl_titol = tk.Label(barra_control, text=titol_pestanya.upper(), bg=bg_barra, fg=fg_barra,
                         font=("Segoe UI", 8, "bold"));
    lbl_titol.pack(side=tk.LEFT, padx=12, pady=4)

    def tancar_pestanya():
        global frame_grafic_actiu
        frame_grafic_actiu = None
        notebook.forget(frame_pestanya)

    btn_tancar = tk.Button(barra_control, text="  ✕  ", bg=bg_boto_tancar, fg=fg_boto_tancar,
                           font=("Segoe UI", 7, "bold"), bd=0, cursor="hand2", activebackground="#c62828",
                           activeforeground="white", command=tancar_pestanya)
    btn_tancar.pack(side=tk.RIGHT, padx=6, pady=3)

    frame_contingut_grafic = tk.Frame(frame_pestanya, bg=bg_pestanya);
    frame_contingut_grafic.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    frame_grafic_actiu = frame_contingut_grafic

    notebook.add(frame_pestanya, text=titol_pestanya)
    notebook.select(frame_pestanya)
    funcio_grafic(dades, frame_contingut_grafic)

# Instanciació de panells de la graella de control inferior
estil_seccio = {"bg": "#ffffff", "fg": "#2d3748", "font": ("Segoe UI", 9, "bold"), "bd": 1, "relief": "solid",
                "padx": 10, "pady": 10}
t_init = TEXTOS[idioma_actual]

frame_AirportManagement = tk.LabelFrame(frame_inferior, text=t_init["management"], **estil_seccio);
frame_AirportManagement.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
crear_boto_modern(frame_AirportManagement, t_init["btn_add"], add_airport).pack(side=tk.TOP, fill=tk.X, pady=3)
crear_boto_modern(frame_AirportManagement, t_init["btn_remove"], remove_airport).pack(side=tk.TOP, fill=tk.X, pady=3)
crear_boto_modern(frame_AirportManagement, t_init["btn_info"], buscar_airport).pack(side=tk.TOP, fill=tk.X, pady=3)

frame_Maps = tk.LabelFrame(frame_inferior, text=t_init["maps"], **estil_seccio);
frame_Maps.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
crear_boto_modern(frame_Maps, t_init["btn_map_ap"], map_airports).pack(fill=tk.X, pady=4)
crear_boto_modern(frame_Maps, t_init["btn_map_fl"], map_flights).pack(fill=tk.X, pady=4)

frame_Plots = tk.LabelFrame(frame_inferior, text=t_init["analytics"], **estil_seccio);
frame_Plots.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
crear_boto_modern(frame_Plots, t_init["btn_plot_sch"], plot_airports).pack(fill=tk.X, pady=2)
crear_boto_modern(frame_Plots, t_init["btn_plot_air"], plot_airlines).pack(fill=tk.X, pady=2)
crear_boto_modern(frame_Plots, t_init["btn_plot_arr"], plot_arrival_time).pack(fill=tk.X, pady=2)
crear_boto_modern(frame_Plots, t_init["btn_plot_type"], plot_flight_type).pack(fill=tk.X, pady=2)
crear_boto_modern(frame_Plots, t_init["btn_plot_gates"], plot_gates_map).pack(fill=tk.X, pady=2)
crear_boto_modern(frame_Plots, t_init["btn_plot_night"], executar_mapa_nocturn_gates).pack(fill=tk.X, pady=3)

frame_InfoAeronautica = tk.LabelFrame(frame_inferior, text=t_init["info_aero"], **estil_seccio)
frame_InfoAeronautica.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

crear_boto_modern(frame_InfoAeronautica, t_init["btn_acars"], executar_despatxo_acars_en_temps_real).pack(fill=tk.X, pady=3)
crear_boto_modern(frame_InfoAeronautica, t_init["btn_meteo"], executar_meteo_segura).pack(fill=tk.X, pady=3)
crear_boto_modern(frame_InfoAeronautica, t_init["btn_aodb"], executar_aodb_segura).pack(fill=tk.X, pady=3)

frame_FileManagement_Load = tk.LabelFrame(frame_inferior, text=t_init["import"], **estil_seccio);
frame_FileManagement_Load.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
crear_boto_modern(frame_FileManagement_Load, t_init["btn_load_all"], load_all_data).pack(fill=tk.X, pady=4)
crear_boto_modern(frame_FileManagement_Load, t_init["btn_load_ap"], load_file).pack(fill=tk.X, pady=3)
crear_boto_modern(frame_FileManagement_Load, t_init["btn_load_st"], load_file_structure).pack(fill=tk.X, pady=3)
crear_boto_modern(frame_FileManagement_Load, t_init["btn_load_arr"], load_arrivals).pack(fill=tk.X, pady=3)

frame_FileManagement_Export = tk.LabelFrame(frame_inferior, text=t_init["export"], **estil_seccio);
frame_FileManagement_Export.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
crear_boto_modern(frame_FileManagement_Export, t_init["btn_exp_ap"], export_file).pack(fill=tk.X, pady=3)
crear_boto_modern(frame_FileManagement_Export, t_init["btn_exp_arr"], export_arrivals).pack(fill=tk.X, pady=3)

btn_autosave = tk.Button(frame_FileManagement_Export, text=t_init["auto_off"], bg="#4a5568", fg="white",
                         font=("Segoe UI", 8, "bold"), bd=0, cursor="hand2", pady=4, command=toggle_autosave);
btn_autosave.pack(fill=tk.X, pady=6)

# Elements del banner superior
img_logo = tk.PhotoImage(file="logowhite.png")
img_logo = img_logo.subsample(13, 13)
lbl_logo = tk.Label(frame_header, image=img_logo, bg="#1a1f2c")
lbl_logo.pack(side=tk.LEFT, padx=20, pady=10)

lbl_titulo = tk.Label(frame_header, text=t_init["titulo"], font=("Segoe UI", 15, "bold"), bg="#1a1f2c", fg="#f8fafc");
lbl_titulo.pack(side=tk.LEFT, padx=15, pady=16)
lbl_version = tk.Label(frame_header, text=t_init["subtitulo"], font=("Segoe UI", 8, "bold"), bg="#1a1f2c",
                       fg="#718096");
lbl_version.pack(side=tk.LEFT, padx=10, pady=22)

btn_lang_toggle = tk.Button(frame_header, text=t_init["btn_idioma"], font=("Segoe UI", 9, "bold"), bg="#2d3748",
                            fg="white", bd=0, relief="flat", cursor="hand2", padx=15, pady=6, command=toggle_language);
btn_lang_toggle.pack(side=tk.RIGHT, padx=10, pady=15)
btn_dark_toggle = tk.Button(frame_header, text=t_init["btn_dark_d"], font=("Segoe UI", 9, "bold"), bg="#2d3748",
                            fg="white", bd=0, relief="flat", cursor="hand2", padx=15, pady=6, command=toggle_dark_mode);
btn_dark_toggle.pack(side=tk.RIGHT, padx=20, pady=15)

lbl_rellotge_live = tk.Label(           # Rellotge en temps real
    frame_InfoAeronautica,
    text="ZULU TIME: 00:00:00 UTC",
    font=("Courier New", 10, "bold"),
    bg=frame_InfoAeronautica.cget("bg"),  # Copia el fons del teu frame actiu (clar/fosc)
    fg="#00FF00" if "fosg" in idioma_actual or "dark" in idioma_actual else "#1E3A8A"  # Color adaptatiu
)
lbl_rellotge_live.pack(fill=tk.X, pady=4)


# Funció recursiva en segon pla per actualitzar el rellotge
def actualitzar_rellotge_live():
    ara = datetime.now()
    # Format típic d'aviació (Hora Zulu / UTC real)
    text_hora = f"ZULU TIME: {ara.hour:02d}:{ara.minute:02d}:{ara.second:02d} UTC"
    lbl_rellotge_live.config(text=text_hora)

    # Trucada en bucle automàtica cada 1000 mil·lisegons (1 segon) de Tkinter
    lbl_rellotge_live.after(1000, actualitzar_rellotge_live)

root.iconbitmap("icon.ico")

if __name__ == "__main__":
    actualitzar_rellotge_live()
    root.mainloop()

