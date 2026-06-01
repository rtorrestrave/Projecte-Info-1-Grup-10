# ======================================================================================================================
#
#          ___     ____  ____    ____   ____    ____  ______      ___ ___   ____   ___   __  __   _      _____
#         /   |   /  _/ / __ \  / __ \ / __ \  / __ \/_  __/     /   |   | / __ \ / __ \ / / /   / /    / ___/
#        / /| |   / /  / /_/ / / /_/ // / / / / /_/ / / /       / /| /| |/ / / // / / // / / /  / /    / __/
#       / ___ | _/ /  / _, _/ / ____// /_/ / / _, _/ / /       / /  / / // /_/ // /_/ // /_/ / / /___ / /___
#      /_/  |_|/___/ /_/ |_| /_/     \____/ /_/ |_| /_/       /_/  /_/_/ \____/ \____/ \____/ /_____//_____/
#
#
# ======================================================================================================================


import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Airport:
    def __init__(self, icao, lat, lon):
        self.icao = icao.upper()
        self.latitude = lat
        self.longitude = lon
        self.schengen = False


def AddAirport(lista, nuevoaeropuerto):
    icao = nuevoaeropuerto.icao.upper()
    indice_existente = -1
    i = 0
    while i < len(lista):
        if lista[i].icao == icao:
            indice_existente = i
            break
        i += 1

    if indice_existente != -1:
        # Per evitar bloquejos a la UI, comprovem si estem en mode de consola o interfície
        lista[indice_existente] = nuevoaeropuerto
        print(f"Aeropuerto {icao} Sobreescrito.")
    else:
        lista.append(nuevoaeropuerto)
        print("Nuevo Aeropuerto Añadido.")
    return lista


def RemoveAirports(airports, icao_a_borrar):
    nueva_lista = []
    encontrado = False
    for ap in airports:
        if ap.icao.upper() != icao_a_borrar.upper():
            nueva_lista.append(ap)
        else:
            encontrado = True
    if encontrado: print(f"Aeropuerto {icao_a_borrar} eliminat.")
    return nueva_lista


def SaveAirportList(airports, filename):
    try:
        F = open(filename, "w")
        F.write("CODE LAT LON\n")
        for ap in airports:
            lat = ap.latitude
            lat_dir = "N" if lat >= 0 else "S"
            lat = abs(lat)
            lat_g = int(lat)
            lat_m = int((lat - lat_g) * 60)
            lat_s = int((((lat - lat_g) * 60) - lat_m) * 60)
            lat_str = f"{lat_dir}{lat_g:02d}{lat_m:02d}{lat_s:02d}"

            lon = ap.longitude
            lon_dir = "E" if lon >= 0 else "W"
            lon = abs(lon)
            lon_g = int(lon)
            lon_m = int((lon - lon_g) * 60)
            lon_s = int((((lon - lon_g) * 60) - lon_m) * 60)
            lon_str = f"{lon_dir}{lon_g:03d}{lon_m:02d}{lon_s:02d}"

            F.write(f"{ap.icao} {lat_str} {lon_str}\n")
        F.close()
    except Exception as e:
        print("Error al guardar aeroports:", e)


def IsSchengen(icao):
    if not icao: return False
    try:
        F = open("SchengenList.txt", "r")
        linea = F.readline()
        while linea != "":
            if icao[:2].upper() == linea.strip().upper():
                F.close()
                return True
            linea = F.readline()
        F.close()
    except:
        # Safetynet si el fitxer de text no existís a l'arrel
        pass
    return False


def SetSchengen(airport_obj):
    airport_obj.schengen = IsSchengen(airport_obj.icao)


def LoadAirports(filename):
    lista_aeropuertos = []
    try:
        f = open(filename, "r")
        f.readline()  # Capçalera
        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) < 3:
                linea = f.readline()
                continue
            icao = datos[0]
            lat_str, lon_str = datos[1], datos[2]

            try:
                lat_dec = float(lat_str[1:3]) + (float(lat_str[3:5]) / 60) + (float(lat_str[5:7]) / 3600)
                if lat_str[0] == 'S': lat_dec *= -1
                lon_dec = float(lon_str[1:4]) + (float(lon_str[4:6]) / 60) + (float(lon_str[6:8]) / 3600)
                if lon_str[0] == 'W': lon_dec *= -1

                ap = Airport(icao, lat_dec, lon_dec)
                ap.schengen = IsSchengen(icao)
                lista_aeropuertos.append(ap)
            except:
                pass
            linea = f.readline()
        f.close()
    except FileNotFoundError:
        print("Archivo de aeropuertos no encontrado.")
        return []
    return lista_aeropuertos


def SaveSchengenAirports(airports, filename):
    schengen_list = [a for a in airports if IsSchengen(a.icao)]
    SaveAirportList(schengen_list, filename)


def PlotAirports(airports, frame_central):
    for widget in frame_central.winfo_children(): widget.destroy()
    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False;
        textos = {"plot_ap_t": "Aeroports", "plot_ap_x": "Eix", "plot_ap_y": "Total"}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"

    is_schengen, no_schengen = 0, 0
    for a in airports:
        if IsSchengen(a.icao):
            is_schengen += 1
        else:
            no_schengen += 1

    fig = Figure(figsize=(5, 4), dpi=100, facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)

    labels = [textos["plot_ap_x"]]
    ax.bar(labels, [no_schengen], color="#e53e3e" if is_dark else "#dc3545", label='Non-Schengen')
    ax.bar(labels, [is_schengen], bottom=[no_schengen], color="#3182ce" if is_dark else "#0056b3", label='Schengen')

    ax.set_ylabel(textos["plot_ap_y"], color=fg_color)
    ax.set_title(textos["plot_ap_t"], color=fg_color, fontweight='bold', fontsize=12)
    ax.tick_params(colors=fg_color)
    for spine in ax.spines.values(): spine.set_color(fg_color)

    leg = ax.legend(facecolor=bg_color, edgecolor=fg_color)
    for text in leg.get_texts(): text.set_color(fg_color)

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def MapAirports(lista):
    try:
        F = open("mapairports.kml", "w", encoding="utf-8")
        F.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<name>Airports Map</name>\n')
        for ap in lista:
            F.write(
                f'<Placemark>\n<name>{ap.icao}</name>\n<Point>\n<coordinates>{ap.longitude},{ap.latitude},0</coordinates>\n</Point>\n</Placemark>\n')
        F.write('</Document>\n</kml>\n')
        F.close()
    except Exception as e:
        print("Error en MapAirports:", e)
