import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from airport import *
from aircraft import *

ToggleAutosave = False
airports = []
aircrafts = []

############################### GUI AUTOSAVE ###########################################################################

def autosave():
    global ToggleAutosave
    if ToggleAutosave:
        global airports
        SaveAirportList(airports, "ResultsSchengen.txt")
        global aircrafts
        SaveFlights(aircrafts, "Arrivals2PROV.txt")

def toggle_autosave():
    global ToggleAutosave
    if btn_autosave.config('text')[-1] == "Autosave: NO":
        btn_autosave.config(text="Autosave: SI", bg="#4CAF50", fg="white")
        ToggleAutosave = True
    else:
        btn_autosave.config(text="Autosave: NO", bg="#f44336", fg="white")
        ToggleAutosave = False

############################### GUI ADDAIRPORT #########################################################################

def add_airport():
    win = tk.Toplevel(root)
    win.title("Añadir Aeropuerto")
    win.geometry("300x300")
    tk.Label(win, text="ICAO").pack(pady=5)
    entry_icao = tk.Entry(win)
    entry_icao.pack()
    tk.Label(win, text="Latitud (decimal)").pack(pady=5)
    entry_lat = tk.Entry(win)
    entry_lat.pack()
    tk.Label(win, text="Longitud (decimal)").pack(pady=5)
    entry_lon = tk.Entry(win)
    entry_lon.pack()

    def guardar():
        try:
            icao = entry_icao.get().upper()
            lat = float(entry_lat.get())
            lon = float(entry_lon.get())
            nuevo = Airport(icao, lat, lon)
            AddAirport(airports, nuevo)
            autosave()
            messagebox.showinfo("Correcto", "Aeropuerto añadido a la lista")
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Latitud y longitud deben ser decimales")

    tk.Button(win, text="Guardar", command=guardar).pack(pady=20)

############################### GUI REMOVEAIRPORT ######################################################################

def remove_airport():
    win = tk.Toplevel(root)
    win.title("Quitar Aeropuerto")
    win.geometry("300x300")
    tk.Label(win, text="ICAO a eliminar").pack(pady=10)
    entry_icao = tk.Entry(win)
    entry_icao.pack()

    def eliminar():
        icao = entry_icao.get().upper()
        global airports
        airports = RemoveAirports(airports, icao)
        autosave()
        messagebox.showinfo("Correcto", "Aeropuerto eliminado")
        win.destroy()

    tk.Button(win, text="Eliminar", command=eliminar).pack(pady=20)

############################### GUI LOADFILE / EXPORTFILE ##############################################################

def load_file():
    lista = LoadAirports("ResultsSchengen.txt")
    messagebox.showinfo("Cargar", "Archivo cargado correctamente.")
    global airports
    airports = lista

def export_file():
    global airports
    SaveAirportList(airports, "ResultsSchengen.txt")
    messagebox.showinfo("Exportar", "Archivo exportado correctamente.")

############################### GUI PLOTS (AIRPORTS / AIRLINES) ########################################################

def plot_airports():
    global airports
    if airports == []:
        messagebox.showinfo("Error al graficar aeropuertos", "Error: No existen aeropuertos cargados.")
    else:
        lista = airports
        i = 0
        while i < len(lista):
            lista[i].schengen = IsSchengen(lista[i].icao)
            i = i + 1
        PlotAirports(lista)


def plot_airlines():
    if aircrafts == []:
        messagebox.showinfo("Error al graficar aerolíneas", "Error: No existen vuelos cargados.")
    else:
        PlotAirlines(aircrafts)

def plot_arrival_time():
    if aircrafts == []:
        messagebox.showinfo("Error al graficar vuelos", "Error: No existen vuelos cargados.")
    else:
        PlotArrivals(aircrafts)

def plot_flight_type():
    if aircrafts == []:
        messagebox.showinfo("Error al graficar tipos de vuelo", "Error: No existen vuelos cargados.")
    else:
        PlotFlightsType(aircrafts)

############################### GUI LOAD AIRCRAFT #####################################################################

def load_arrivals():
    lista = LoadArrivals("Arrivals2PROV.txt")
    messagebox.showinfo("Cargar", "Archivo cargado correctamente.")
    global aircrafts
    aircrafts = lista

def export_arrivals():
    global aircrafts
    SaveFlights(aircrafts, "Arrivals2PROV.txt")
    messagebox.showinfo("Exportar", "Archivo exportado correctamente.")

############################### GUI MAPAIRPORTS ########################################################################
def map_airports():
    global airports
    if airports == []:
        messagebox.showinfo("Error al exportar mapa", "Error: No existen aeropuertos cargados.")
    else:
        MapAirports(airports)
        messagebox.showinfo("Exportar mapa", "Archivo KML exportado correctamente.")
def map_flights():
    global aircrafts
    if aircrafts == []:
        messagebox.showinfo("Error al exportar mapa", "Error: No existen vuelos cargados.")
    else:
        MapFlights(aircrafts,airports)
        messagebox.showinfo("Exportar mapa", "Archivo KML exportado correctamente.")

############################### GUI BUSCAR AEROPUERTO ##################################################################

def buscar_airport():
    global airports
    win = tk.Toplevel(root)
    win.title("Buscar Aeropuerto por ICAO")
    win.geometry("300x200")
    tk.Label(win, text="Introduce ICAO").pack(pady=10)
    entry_icao = tk.Entry(win)
    entry_icao.pack()

    def buscar():
        icao = entry_icao.get().upper()
        i = 0
        encontrado = False
        while i < len(airports) and not encontrado:
            if airports[i].icao == icao:
                print_airport(airports[i])
                encontrado = True
            i += 1
        if not encontrado:
            messagebox.showerror("Error", "Aeropuerto no encontrado")

    tk.Button(win, text="Buscar", command=buscar).pack(pady=20)


def print_airport(airport):
    win = tk.Toplevel()
    win.title("Información del Aeropuerto")
    win.geometry("350x250")
    airport.schengen = IsSchengen(airport.icao)
    tk.Label(win, text="Datos del Aeropuerto", font=("Arial", 14)).pack(pady=10)
    tk.Label(win, text=f"ICAO: {airport.icao}").pack(pady=5)
    tk.Label(win, text=f"Latitud: {airport.latitude}").pack(pady=5)
    tk.Label(win, text=f"Longitud: {airport.longitude}").pack(pady=5)
    tk.Label(win, text=f"Schengen: {airport.schengen}").pack(pady=5)
    tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=15)

############################### GUI CONFIGURACION VENTANA ##############################################################

root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("AirportManager v2.0")
root.geometry("1100x500")

frame_header = tk.Frame(root, bg="#2c3e50", height=50)
frame_header.pack(side=tk.TOP, fill=tk.X)

frame_central = tk.Frame(root, bg="lightgray")
frame_central.pack(fill=tk.BOTH, expand=True)

frame_inferior = tk.Frame(root, bg="darkgray", height=200)
frame_inferior.pack(side=tk.BOTTOM, fill=tk.X)

# FRAME AIRPORT MANAGEMENT

frame_AirportManagement = tk.LabelFrame(frame_inferior, text="Airport Management", bg="darkgray")
frame_AirportManagement.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

tk.Button(frame_AirportManagement, text="Añadir Aeropuerto", command=add_airport).pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=2)
tk.Button(frame_AirportManagement, text="Quitar Aeropuerto", command=remove_airport).pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=2)
tk.Button(frame_AirportManagement, text="Informacion Aeropuerto", command=buscar_airport).pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=2)

# FRAME MAPS

frame_Maps = tk.LabelFrame(frame_inferior, text="Mapas", bg="darkgray")
frame_Maps.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

tk.Button(frame_Maps, text="Mapa Aeropuertos", command=map_airports).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
tk.Button(frame_Maps, text="Mapa Vuelos", command=map_flights).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# FRAME PLOTS

frame_Plots = tk.LabelFrame(frame_inferior, text="Plots", bg="darkgray")
frame_Plots.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

tk.Button(frame_Plots, text="Graficar Schengen", command=plot_airports).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
tk.Button(frame_Plots, text="Graficar Llegadas por Aerolínea", command=plot_airlines).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
tk.Button(frame_Plots, text="Graficar Horas de Llegada", command=plot_arrival_time).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
tk.Button(frame_Plots, text="Graficar Tipos de Vuelo", command=plot_flight_type).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# FRAME FILE MANAGEMENT

frame_FileManagement = tk.LabelFrame(frame_inferior, text="File Management", bg="darkgray")
frame_FileManagement.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

tk.Button(frame_FileManagement, text="Cargar Archivo Aeropuertos", command=load_file).pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
tk.Button(frame_FileManagement, text="Exportar Archivo Aeropuertos", command=export_file).pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
tk.Button(frame_FileManagement, text="Cargar Archivo Llegadas", command=load_arrivals).pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
tk.Button(frame_FileManagement, text="Exportar Archivo Llegadas", command=export_arrivals).pack(fill=tk.BOTH, expand=True, padx=5, pady=2)


# HEADER CONFIG

img_logo = tk.PhotoImage(file="logo.png")
img_logo = img_logo.subsample(13, 13)
lbl_logo = tk.Label(frame_header, image=img_logo, bg="#2c3e50")
lbl_logo.pack(side=tk.LEFT, padx=20, pady=10)


btn_autosave = tk.Button(
    frame_FileManagement,
    text="Autosave: NO",
    bg="#f44336",
    fg="white",
    font=("Calibri", 10, "bold"),
    command=toggle_autosave)
btn_autosave.pack(pady=5)

lbl_titulo = tk.Label(
    frame_header,
    text="AirportManager",
    font=("Helvetica", 22, "bold"),
    bg="#2c3e50",
    fg="white"
)
lbl_titulo.pack(side=tk.LEFT, padx=10)

lbl_version = tk.Label(
    frame_header,
    text="v2.0",
    font=("Arial", 10),
    bg="#2c3e50",
    fg="#bdc3c7"
)
lbl_version.pack(side=tk.RIGHT, padx=20, pady=(30, 0))

root.mainloop()


# ==== NOS FALLA =====
# PLOT TIPOS DE VUELO
# KML VUELOS LLEGADAS
# TEST SECTION of aircraft.py de totes les funcions
