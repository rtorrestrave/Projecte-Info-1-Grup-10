########################################################################################################################
#####################################       DEFINICION CLASE Y LIBRERÍAS         #######################################
########################################################################################################################

class Aircraft:
    def __init__(self, id, company, origin, landtime):
        self.id= id
        self.company = company
        self.origin = origin
        self.landtime = landtime


#Opens the file with name received as input and with the format described
#below, and returns a list of aircraft initialized with the data found in the
#file. These are the flights that will arrive to LEBL at a given day. In the
#file you will not find all data defined in the structure Aircraft, so update
#only the fields of the structure you can. If the file does not exist the
#function returns an empty list. In case some of the aircraft lines do not have
#a correct time or the expected structure, then the function must skip this
#line and proceed with the rest of lines in the file. Note that the arrivals
#file is sorted by landing time.

#AIRCRAFT ORIGIN ARRIVAL AIRLINE
#ECMKV LYBE 0:04 VLG
#ECJGM EGCC 0:05 VLG
#ECLOB LMML 1:24 VLG
#ECLVC LGTS 2:28 VLG
#DALEC EBBR 3:14 BCS
#N327UP EDDK 3:17 UPS

aviones_llegadas = []

########################################################################################################################
#################################       CARGA DE LLEGADAS (LOADARRIVALS)         #######################################
########################################################################################################################
def LoadArrivals(filename):  # Carga llegadas
    lista_aircraft = []

    try:
        f = open(filename, "r")

        f.readline()
        linea = f.readline()

        while linea != "":
            datos = linea.strip().split()

            # Filtro de seguridad de línea incompleta
            if len(datos) != 4:
                linea = f.readline()
                continue

            # Filtro de seguridad de datos incompletos
            if len(datos[0]) < 3 and len(datos[1]) != 4 and len(datos[2]) < 4 and len(datos[3]) != 3:
                linea = f.readline()
                continue

            id = datos[0]  ### sacar datos del archivo por posición
            origin = datos[1]
            landtime = datos[2]
            company = datos[3]

            avion_a_anadir = Aircraft(id, company, origin, landtime)
            lista_aircraft.append(avion_a_anadir)

            linea = f.readline()
        f.close()

    except FileNotFoundError:
        print("Archivo NO Encontrado")
        return []

    return lista_aircraft


#TEST PGM Prueba
aviones_llegadas = LoadArrivals("Arrivals.txt")
print(aviones_llegadas)
print(aviones_llegadas[0].id)
print(aviones_llegadas[0].origin)
print(aviones_llegadas[0].company)
print(aviones_llegadas[0].landtime)


