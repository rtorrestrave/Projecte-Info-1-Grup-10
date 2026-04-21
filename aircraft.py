########################################################################################################################
#####################################       DEFINICION CLASE Y LIBRERÍAS         #######################################
########################################################################################################################
import  math
from airport import *
import matplotlib.pyplot as plt


class Aircraft:
    def __init__(self, id, company, origin, landtime):
        self.id= id
        self.company = company
        self.origin = origin
        self.landtime = landtime

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
            if len(datos[0]) < 3 and len(datos[1]) != 4 and len(datos[2]) != 5 and len(datos[3]) != 3:
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


########################################################################################################################
################################  GUARDAR LA LISTA EN FICHERO TXT   ####################################################
########################################################################################################################
#DALEC EBBR 3:14 BCS

def SaveFlights (aircrafts, filename):
    F = open(filename, "w")
    F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
    i = 0
    while i < len(aircrafts):

        id = aircrafts[i].id
        company = aircrafts[i].company
        origin = aircrafts[i].origin
        landtime = aircrafts[i].landtime

        if id == "":            # Si hay vacío, escribir un guión
            id = "-"
        if origin == "":
            origin = "-"
        if landtime == "":
            landtime = "-"
        if company == "":
            company = "-"

        F.write(id + " " + origin + " " + landtime + " " + company + "\n")            #escribimos!
        i += 1
    F.close()
########################################################################################################################
################################      Lista de Vuelos LARGOS        ####################################################
########################################################################################################################

def LongDistanceArrivals(aircrafts):
    global airports
    i=0
    LongAircraftFlights = []
    while i < len(aircrafts):
        print("debug1")#Bucle que pasa por cada avion
        ICAOorigen = aircrafts[i].origin
        Final = Airport(icao="LEBL",lat=41.29666,lon=2.07833)
        Encontrado = False
        j=0
        while j < len(airports) and not Encontrado:     # Bucle que BUSCA el aeropuerto para extraer el aeropuerto
            if airports[j].icao == ICAOorigen:          # con todos sus atributos
                Encontrado = True
                Origen = airports[j]
                print("debug2")
            j += 1

        if HaversineDistance(Origen,Final) > 2000:
            LongAircraftFlights.append(aircrafts[i])
            print("debug3")
        i += 1

    return LongAircraftFlights


def HaversineDistance (AirportA, AirportB):

    lat1 = AirportA.latitude
    lon1 = AirportA.longitude
    lat2 = AirportB.latitude
    lon2 = AirportB.longitude

    φ1 = lat1 * math.pi / 180  # Conversión a Radianes de los angulos de la Latitud
    φ2 = lat2 * math.pi / 180
    R = 6371  # Radio de la tierra en KM
    incrφ = (lat2 - lat1) * math.pi / 180
    incrλ = (lon2 - lon1) * math.pi / 180

    a = math.sin(incrφ / 2) * math.sin(incrφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(incrλ / 2) * math.sin(incrλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # Uso Formula de Haversine
    return R * c  # Retorno el valor d = R*c



########################################################################################################################
#################################       PLOT LLEGADAS      #############################################################
########################################################################################################################

def PlotArrivals(aircrafts):

    # Comprova si la llista està buida
    if not aircrafts:
        print("Error: Archivo NO Encontrado")
        return

    # Crea una llista de 24 posicions (una per cada hora)
    horas = [0] * 24

    # Recorre tots els avions de la llista
    for avion in aircrafts:
        try:
            # Separa hora i minuts (format H:MM o HH:MM)
            partes = avion.landtime.split(":")
            hora = int(partes[0])

            # Comprova que la hora sigui vàlida
            if 0 <= hora < 24:
                # Suma un aterratge en aquella hora
                horas[hora] += 1

        except:
            # Si hi ha error en el format de la hora, ignora aquest avió
            continue

    # Crea el gràfic de barres
    plt.figure()
    plt.bar(range(24), horas)

    # Etiquetes dels eixos
    plt.xlabel("Hora del dia")
    plt.ylabel("Nombre d'aterratges")

    # Títol del gràfic
    plt.title("Aterratges per hora")

    # Mostrar totes les hores a l'eix X
    plt.xticks(range(24))

    plt.grid(axis='y')
    plt.show()

########################################################################################################################
#################################       PLOT AEROLINEAS       ##########################################################
########################################################################################################################

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("No hay aviones para graficar")
        return

    # Listas paralelas (Estructura clásica)
    nombres_cia = []
    contadores = []

    i = 0
    while i < len(aircrafts):
        cia_actual = aircrafts[i].company

        # Lógica de búsqueda manual
        encontrado = False
        j = 0
        while j < len(nombres_cia):
            if nombres_cia[j] == cia_actual:
                contadores[j] = contadores[j] + 1
                encontrado = True
                break
            j = j + 1

        if not encontrado:
            nombres_cia.append(cia_actual)
            contadores.append(1)

        i = i + 1

    plt.figure(figsize=(10, 6))

    # Creación del gráfico de barras con las listas procesadas
    plt.bar(nombres_cia, contadores, color='skyblue', edgecolor='navy')

    # Títulos y etiquetas
    plt.title("Vuelos Activos por Aerolínea")
    plt.xlabel("Compañía")
    plt.ylabel("Número de Vuelos")

    # Giro de los nombres de abajo (eje X) para evitar colisiones
    # rotation=45 gira el texto, ha='right' alinea el final del texto con la marca
    plt.xticks(rotation=45, ha='right')

    # Ajuste automático para que no se corten las etiquetas al girarlas
    plt.tight_layout()

    # Mostrar resultado
    plt.show()

########################################################################################################################
#################################       KML VUELOS            ##########################################################
########################################################################################################################

def MapFlights(aircrafts):
    F = open("routes.kml", "w", encoding="utf-8")

    F.write('<?kml version="1.0" encoding="UTF-8"?>\n')
    F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    F.write('<Document>\n')
    F.write('<name> Vols a LEBL </name>\n')

    i=0

    while i < len(aircrafts):

        icao = aircrafts[i].icao
        lat_origen= aircrafts[i].latitude
        lon_origen = aircrafts[i].longitude

        if aircrafts[i].is_schengen == True:
            color = 'ffff0000'
        else:
            color = "ff0000ff"

        F.write('<Placemark>\n')
        F.write(f'  <name>Flight {icao}</name>\n')

        F.write('  <Style>\n')
        F.write('    <LineStyle>\n')
        F.write(f'      <color>{color}</color>\n')
        F.write('      <width>2</width>\n')
        F.write('    </LineStyle>\n')
        F.write('  </Style>\n')

        F.write('  <LineString>\n')
        F.write(f'    <coordinates>{lon_ori},{lat_ori},0 2.1089,41.2974,0</coordinates>\n')
        F.write('  </LineString>\n')
        F.write('</Placemark>\n')

        i += 1

    F.write('</Document>\n')
    F.write('</kml>\n')
    F.close()


#######20
########################################################################################################################
#################################       PLOT TIPOS VUELO      ##########################################################
########################################################################################################################
# Grafica de vols schengen i no schengen
def PlotFlightsType (aircrafts):
    if len(aircrafts)==0:
        print("Error, the list is EMPTY")
        return
    schengen = []
    no_schengen = []
    tots=[]
    for plane in aircrafts:
        nom= plane['tipus']
        if name not in tots:
            tots.append(nom)
            schengen[nom]=0
            no_schengen[nom] = 0
        if plane['is schengen']==True:
            schengen[nom]+=1
        else:
            no_schengen[nom]+=1

    slist = [schengen[n] for n in tots]
    noslist = [no_schengen[n] for n in tots]

    plt.bar(tots, noslist, lebel="no schengen", color='orange')
    plt.bar(tots, slist, bottom=noslist, lebel = "schengen" , color='blue')
    plt.legend()
    plt.show()



#TEST PGM PRINCIPAL

if __name__ == "__main__":
    aircrafts = LoadArrivals("Arrivals.txt")
    PlotArrivals (aircrafts)

