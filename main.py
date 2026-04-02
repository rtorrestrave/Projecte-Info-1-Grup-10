import tkinter as tk
from tkinter import messagebox
from airport import *

airports = []

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

            messagebox.showinfo("Correcto", "Aeropuerto añadido a la lista")
            win.destroy()

        except ValueError:
            messagebox.showerror("Error", "Latitud y longitud deben ser decimales")

    tk.Button(win, text="Guardar", command=guardar).pack(pady=20)



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
        messagebox.showinfo("Correcto", "Aeropuerto eliminado")
        win.destroy()

    tk.Button(win, text="Eliminar", command=eliminar).pack(pady=20)

def load_file():
    lista = LoadAirports("ResultsSchengen.txt")
    messagebox.showinfo("Cargar", "Archivo cargado correctamente.")
    global airports
    airports = lista


def export_file():
    global airports
    lista = airports
    SaveAirportList(lista,"ResultsSchengen.txt")
    messagebox.showinfo("Exportar", "Archivo exportado correctamente.")


def plot_airports():
    ##messagebox.showinfo("Plot", "Función Plot Airports activada")
    global airports
    lista = airports
    i = 0
    while i < len(lista):
        lista[i].schengen = IsSchengen(lista[i].icao)
        i=i+1
    PlotAirports(lista)

def map_airports():
    global airports
    MapAirports(airports)
    messagebox.showinfo("Exportar mapa", "Archivo KML exportado correctamente.")

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


# Ventana Principal
root = tk.Tk()
root.title("AirportManager v1.0")
root.geometry("1000x500")  # Tamaño de pantalla grande

# Frame
frame_main = tk.Frame(root, bg="lightgray")
frame_main.pack(fill=tk.BOTH, expand=True)

# Botonera
frame_botones = tk.Frame(frame_main, bg="darkgray", height=150)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X)

# Botones principales de la botonera
btn_plot = tk.Button(frame_botones, text="Graficar Aeropuertos Schengen", width=30, height=3, command=plot_airports)
btn_plot.pack(side=tk.LEFT, padx=10, pady=10)

btn_plot = tk.Button(frame_botones, text="Mapa Aeropuertos", width=30, height=3, command=map_airports)
btn_plot.pack(side=tk.LEFT, padx=10, pady=10)

btn_plot = tk.Button(frame_botones, text="Informacion Aeropuerto", width=30, height=3, command=buscar_airport)
btn_plot.pack(side=tk.LEFT, padx=10, pady=10)



# Botones de management
btn_add = tk.Button(frame_botones, text="Añadir", width=15, height=2, command=add_airport)
btn_add.pack(padx=10, pady=5)

btn_remove = tk.Button(frame_botones, text="Quitar", width=15, height=2, command=remove_airport)
btn_remove.pack(padx=10, pady=5)

btn_load = tk.Button(frame_botones, text="Cargar archivo", width=15, height=2, command=load_file)
btn_load.pack(padx=10, pady=5)

btn_export = tk.Button(frame_botones, text="Exportar archivo", width=15, height=2, command=export_file)
btn_export.pack(padx=10, pady=5)

#Ejecutar (y disfrutar)
root.mainloop()
