import matplotlib.pyplot as plt

class Airport:
    def __init__(self, icao, lat, lon):
        self.icao = icao          # Guardamos el valor que entra
        self.latitude = lat
        self.longitude = lon
        self.schengen = False

###### INTRODUIR AEROPORT A LA LLISTA ######



def AddAirport():
    lista = LoadAirports("airports.txt")

    print("--- Introduce los datos del nuevo aeropuerto ---")
    icao = input("Código ICAO: ").upper()


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
            return  # Salimos sin hacer nada

    lat = float(input("Latitude: "))
    lon = float(input("Longitude: "))

    nuevo = Airport(icao, lat, lon)
    nuevo.schengen = IsSchengen(nuevo)

    if indice_existente != -1:
        lista[indice_existente] = nuevo
    else:
        lista.append(nuevo)

    F = open("ResultsSchengen.txt", "w")
    F.write("CODE LAT LON SCHENGEN\n")
    i = 0
    while i < len(lista):
        a = lista[i]
        F.write(f"{a.icao} {a.latitude} {a.longitude} {a.schengen}\n")
        i += 1
    F.close()
    print("Aeropuerto guardado correctamente.")


##################################### REMOVE AIRPORT ########################33

def RemoveAirports():
    nueva_lista = []
    lista_original = LoadAirports("airports.txt")
    icao_a_borrar = input("Introduce el ICAO a borrar: ")
    i = 0
    encontrado = False

    while i < len(lista_original) and not encontrado:

        if lista_original[i].icao.upper() != icao_a_borrar.upper():
            nueva_lista.append(lista_original[i])
        else:
            encontrado = True  # Lo hemos saltado, por lo tanto, "borrado"
        i += 1

    if encontrado:
        F = open("Airports.txt", "w")
        F.write("CODE LAT LON\n")

        j = 0
        while j < len(nueva_lista):
            a = nueva_lista[j]
            # Escribimos cada objeto de la nueva lista
            F.write(f"{a.icao} {a.latitude} {a.longitude}\n")
            j += 1

        F.close()

        print(f"Aeropuerto {icao_a_borrar} eliminado de la lista.")

    else:
        print("No se encontró el aeropuerto para eliminar.")





    return nueva_lista  # Devolvemos la lista limpia



###### BUSCAR SCHENGEN #######
def IsSchengen(airport):
    F = open("SchengenList.txt", "r")
    pais_icao = airport.icao[:2].upper()

    linea = F.readline()
    while linea != "":
        if pais_icao == linea.strip().upper():
            F.close()  # Importante cerrar antes de salir
            return True
        linea = F.readline()

    F.close()
    return False

##################### SUBRUTINA SET-SCHENGEN ###################
def SetSchengen(icao):
    if IsSchengen(icao) == True:
        Airport.schengen = True
    else:
        Airport.schengen = False

##################### SUBRUTINA PRINT-AIRPORT ###################

def PrintAirport(airport):
    print("entro a PrintAirport")
    F = open("airports.txt", "r")
    linea= F.readline()
    FinaldeLinea = False
    Encontrado = False
    CodigoBuscado = airport.icao.upper()

    while FinaldeLinea == False and Encontrado == False:
        elements = linea.strip().split(" ")
        if len(elements) < 3:
            linea = F.readline()        # Salto de linea si esta incompleta
            continue

        if elements[0] == CodigoBuscado:
            print("Codigo ICAO: ", elements[0])
            print("Latitude: ", elements[1])
            print("Longitude: ", elements[2])
            #print("Schengen: ", elements[3])               #Hay que adecuar la lista a schengens
            Encontrado = True

        elif linea == "":
            print("No se ha encontrado el aeropuerto")
            FinaldeLinea = True

        linea = F.readline()
    F.close()

############################# LOAD AIRPORTS #######################
def LoadAirports(origen):
    lista_aeropuertos = []

    try:
        f = open(origen, "r")

        f.readline()
        linea = f.readline()

        while linea != "":
            datos = linea.strip().split()

            # Filtro de seguridad
            if len(datos) < 3:
                linea = f.readline()
                continue

            icao = datos[0]
            lat_str = datos[1]
            lon_str = datos[2]

            lat_dec = float(lat_str[1:3]) + (float(lat_str[3:5]) / 60) + (float(lat_str[5:7]) / 3600)
            if lat_str[0] == 'S':
                lat_dec = lat_dec * -1   #### conversor latitudes


            lon_dec = float(lon_str[1:4]) + (float(lon_str[4:6]) / 60) + (float(lon_str[6:8]) / 3600)
            if lon_str[0] == 'W':
                lon_dec = lon_dec * -1   #### conversor longitudes



            nuevo_aeropuerto = Airport(icao, lat_dec, lon_dec)

            nuevo_aeropuerto.schengen = IsSchengen(nuevo_aeropuerto)

            lista_aeropuertos.append(nuevo_aeropuerto)

            linea = f.readline()

        f.close()

    except FileNotFoundError:
        return []  # Si no existe, lista vacía como pide la consigna

    return lista_aeropuertos

def SaveSchengenAirports(filename):
    F = open(filename, "r")
    R = open("ResultsSchengen.txt","w")
    linea = F.readline()

    while linea != "":
        elements = linea.split(" ")
        schengen = elements[2].strip()[0]           ############################################## Cuidao Index
        icao = elements[0]

        if schengen == True:
            R.write(str(icao))
            R.write("\n")
        linea = F.readline()


##################### PLOTS ###################


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






