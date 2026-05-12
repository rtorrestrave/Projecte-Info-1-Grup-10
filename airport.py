########################################################################################################################
#####################################       DEFINICION CLASE Y LIBRERÍAS         #######################################
########################################################################################################################

import matplotlib.pyplot as plt

class Airport:
    def __init__(self, icao, lat, lon):
        self.icao = icao
        self.latitude = lat
        self.longitude = lon
        self.schengen = False

########################################################################################################################
################################ INTRODUCIR UN AEROPUERTO EN LISTA  ####################################################
########################################################################################################################

def AddAirport(lista, nuevoaeropuerto):
    icao = nuevoaeropuerto.icao
    #latitud = nuevoaeropuerto.latitude
    #longitud = nuevoaeropuerto.longitude

    indice_existente = -1
    i = 0
    while i < len(lista):
        if lista[i].icao == icao:
            indice_existente = i
        i += 1

    if indice_existente != -1:
        opcion = input(f"El aeropuerto {icao} ya existe. ¿Sobreescribir? (Y/N): ").upper()
        if opcion != "Y":
            print("Operación cancelada.")
            return

    if indice_existente != -1:
        lista[indice_existente] = nuevoaeropuerto
        print("Aeropuerto Sobreescrito.")
    else:
        lista.append(nuevoaeropuerto)
        print("Nuevo Aeropuerto Añadido")

    return lista

########################################################################################################################
#################################### QUITAR UN AEROPUERTO EN LISTA  ####################################################
########################################################################################################################

def RemoveAirports(airports, icao_a_borrar):
    nueva_lista = []

    i = 0
    encontrado = False

    while i < len(airports) and not encontrado:         # primer bucle para QUITAR el aeropuerto deseado

        if airports[i].icao.upper() != icao_a_borrar.upper():
            nueva_lista.append(airports[i])
            print("Buscando...")
        else:
            encontrado = True
            print(f"Aeropuerto {icao_a_borrar} eliminado de la lista.")
        i += 1

    while i < len(airports) and encontrado:              # segundo bucle para continuar con los demas

        nueva_lista.append(airports[i])
        i += 1

    if not encontrado:
        print("No se encontró el aeropuerto para eliminar.")

    return nueva_lista

########################################################################################################################
################################  GUARDAR LA LISTA EN FICHERO TXT   ####################################################
########################################################################################################################

def SaveAirportList(airports, filename):
    F = open(filename, "w")
    F.write("CODE LAT LON\n")

    i = 0
    while i < len(airports):

        lat = airports[i].latitude      #conversor latitudes a formato
        if lat >= 0:
            lat_dir = "N"
        else:
            lat_dir = "S"
            lat = -lat

        lat_grados = int(lat)
        lat_minutos = int((lat - lat_grados) * 60)
        lat_segundos = int((((lat - lat_grados) * 60) - lat_minutos) * 60)

        lat_str = lat_dir + f"{lat_grados:02d}{lat_minutos:02d}{lat_segundos:02d}"

        lon = airports[i].longitude    #conversor longitudes a formato
        if lon >= 0:
            lon_dir = "E"
        else:
            lon_dir = "W"
            lon = -lon

        lon_grados = int(lon)
        lon_minutos = int((lon - lon_grados) * 60)
        lon_segundos = int((((lon - lon_grados) * 60) - lon_minutos) * 60)

        lon_str = lon_dir + f"{lon_grados:03d}{lon_minutos:02d}{lon_segundos:02d}"


        F.write(airports[i].icao + " " + lat_str + " " + lon_str + "\n")            #escribimos!
        i += 1
    F.close()

########################################################################################################################
#####################################       IS SCHENGEN  ????       ####################################################
########################################################################################################################

def IsSchengen(icao):
    F = open("SchengenList.txt", "r")
    linea = F.readline()
    while linea != "":
        if icao[:2] == linea.strip().upper():
            F.close()
            return True
        linea = F.readline()

    F.close()
    return False

########################################################################################################################
#####################################       SET SCHENGEN            ####################################################
########################################################################################################################
def SetSchengen(icao):
    if IsSchengen(icao) == True:
        Airport.schengen = True                 # Hay que REVISAR LA FUNCION
    else:
        Airport.schengen = False

##################### SUBRUTINA PRINT-AIRPORT ###################

def PrintAirport(airport):

    lista_aeropuertos = LoadAirports("airports.txt")
    i = 0
    Encontrado = False
    CodigoBuscado = airport.icao.upper()

    while i < len(lista_aeropuertos) and Encontrado == False:

        if lista_aeropuertos[i].icao == CodigoBuscado:
            print("Codigo ICAO: ", lista_aeropuertos[i].icao)
            print("Latitude: ", lista_aeropuertos[i].latitude)
            print("Longitude: ", lista_aeropuertos[i].longitude)
            print("Schengen: ", lista_aeropuertos[i].schengen)
            Encontrado = True

        i += 1

    if Encontrado == False:
        print("No se ha encontrado el aeropuerto")

########################################################################################################################
#####################################       IS SCHENGEN  ????       ####################################################
########################################################################################################################
def LoadAirports(filename):
    lista_aeropuertos = []

    try:
        f = open(filename, "r")

        f.readline()
        linea = f.readline()

        while linea != "":
            datos = linea.strip().split()

            # Filtro de seguridad
            if len(datos) < 3:
                linea = f.readline()
                continue

            icao = datos[0]             ### sacar datos del archivo por posición
            lat_str = datos[1]
            lon_str = datos[2]

            lat_dec = float(lat_str[1:3]) + (float(lat_str[3:5]) / 60) + (float(lat_str[5:7]) / 3600)
            if lat_str[0] == 'S':
                lat_dec = lat_dec * -1   #### conversor latitudes


            lon_dec = float(lon_str[1:4]) + (float(lon_str[4:6]) / 60) + (float(lon_str[6:8]) / 3600)
            if lon_str[0] == 'W':
                lon_dec = lon_dec * -1   #### conversor longitudes


            nuevo_aeropuerto = Airport(icao, lat_dec, lon_dec)
            lista_aeropuertos.append(nuevo_aeropuerto)

            linea = f.readline()
        f.close()

    except FileNotFoundError:
        print("Archivo NO Encontrado")
        return []

    return lista_aeropuertos

########################################################################################################################
#####################################    SAVE SCHENGEN AIRPORTS     ####################################################
########################################################################################################################

def SaveSchengenAirports(airports, filename):
    F = open(filename, "w")
    F.write("CODE LAT LON\n")

    i = 0
    while i < len(airports):
        airports[i].schengen = IsSchengen(airports[i].icao)

        if airports[i].schengen == True:
            lat = airports[i].latitude      #conversor Latitudes
            if lat >= 0:
                lat_dir = "N"
            else:
                lat_dir = "S"
                lat = -lat
            lat_grados = int(lat)
            lat_minutos = int((lat - lat_grados) * 60)
            lat_segundos = int((((lat - lat_grados) * 60) - lat_minutos) * 60)
            lat_str = lat_dir + f"{lat_grados:02d}{lat_minutos:02d}{lat_segundos:02d}"

            lon = airports[i].longitude     #conversor Longitudes
            if lon >= 0:
                lon_dir = "E"
            else:
                lon_dir = "W"
                lon = -lon
            lon_grados = int(lon)
            lon_minutos = int((lon - lon_grados) * 60)
            lon_segundos = int((((lon - lon_grados) * 60) - lon_minutos) * 60)
            lon_str = lon_dir + f"{lon_grados:03d}{lon_minutos:02d}{lon_segundos:02d}"


            F.write(airports[i].icao + " " + lat_str + " " + lon_str + "\n")    #escritura final!

        i += 1

    F.close()


########################################################################################################################
#####################################       PLOT       AIRPORTS     ####################################################
########################################################################################################################


def PlotAirports(airports):
    is_schengen = 0
    no_schengen = 0
    i = 0
    while i < len(airports):
        if airports[i].schengen == True:
            is_schengen += 1
        else:
            no_schengen += 1
        i += 1


    labels = ['Aeropuertos']
    plt.bar(labels, [no_schengen], color='red', label='Non-Schengen')
    plt.bar(labels, [is_schengen], bottom=[no_schengen], color='blue', label='Schengen')

    plt.ylabel('Cantidad')
    plt.title('Distribución de Aeropuertos')
    plt.legend()

    print(f"Mostrando gráfico: {is_schengen} Schengen, {no_schengen} No Schengen")
    plt.show()


# 2. No existe pintar los aeropuertos en google earth.
# 3. PrintAirport!

########################################################################################################################
#####################################    GOOGLE EARTH AIRPORTS      ####################################################
########################################################################################################################

def MapAirports(lista):
    F = open("mapairports.kml", "w", encoding="utf-8")

    F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    F.write('<Document>\n')
    F.write('<name>Airports Map</name>\n')

    i = 0
    while i < len(lista):
        icao = lista[i].icao
        lat = lista[i].latitude
        lon = lista[i].longitude

        F.write('<Placemark>\n')
        F.write(f'<name>{icao}</name>\n')
        F.write('<Point>\n')
        F.write(f'<coordinates>{lon},{lat},0</coordinates>\n')
        F.write('</Point>\n')
        F.write('</Placemark>\n')

        i += 1

    F.write('</Document>\n')
    F.write('</kml>\n')

    F.close()







