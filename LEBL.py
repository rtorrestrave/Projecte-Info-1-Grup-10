########################################################################################################################
#####################################        DEFINICION CLASE Y LIBRERÍAS    #######################################
########################################################################################################################
import matplotlib.pyplot as plt

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = None  # Si no està ocupat, és None


class BoardingArea:
    def __init__(self, name, type_schengen):
        self.name = name
        self.type = type_schengen  # "Schengen" o "non-Schengen"
        self.gates = []  # Llista d'objectes de classe Gate


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []  # Llista d'objectes de classe BoardingArea
        self.airlines = []  # Llista de codis ICAO de les aerolínies (strings)


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []  # Llista d'objectes de classe Terminal


########################################################################################################################
#####################################              def SetGates                #########################################
########################################################################################################################

def SetGates(area, init_gate, end_gate, prefix):
    # Validació d'error segons l'enunciat
    if end_gate <= init_gate:
        return -1

    # Buidar la llista anterior (drop)
    area.gates = []

    # Crear les noves portes
    i = init_gate
    while i <= end_gate:
        nom_porta = f"{prefix}{i}"
        nueva_gate = Gate(nom_porta)
        area.gates.append(nueva_gate)
        i += 1

    return 0  # Tot correcte


########################################################################################################################
#####################################              def LoadAirlines                #####################################
########################################################################################################################

def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"

    try:
        f = open(filename, "r")

        # Si el fitxer existeix: buidem la llista actual
        terminal.airlines = []

        linea = f.readline()
        while linea != "":
            # L'enunciat diu que estan separats per un tabulador (\t)

            datos = linea.strip().split("\t")

            if len(datos) >= 2:
                # El segon element és el codi ICAO (ADR, AEE, etc.)
                icao_airline = datos[1]
                terminal.airlines.append(icao_airline)

            linea = f.readline()

        f.close()
        return 0  # Èxit

    except FileNotFoundError:
        print(f"Error: Fitxer {filename} no trobat.")
        return -1  # Codi d'error si el fitxer no existeix


########################################################################################################################
#####################################         def GateOccupancy    (JOAN)     ##########################################
########################################################################################################################
def GateOccupancy(bcn):
    gates_info = []
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas):
            boarding_area = terminal.boarding_areas[j]
            k = 0
            while k < len(boarding_area.gates):
                gate = boarding_area.gates[k]
                gates_info.append({
                    "terminal": terminal.name,
                    "boarding_area": boarding_area.name,
                    "type": boarding_area.type,
                    "gate": gate.name,
                    "occupied": gate.occupied,
                    "aircraft_id": gate.aircraft_id
                })
                k += 1
            j += 1
        i += 1
    return gates_info

import matplotlib.pyplot as plt

def PlotGates(gates_info):

    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = 0
    labels = []

    i = 0
    while i < len(gates_info):
        info = gates_info[i]
        if info["occupied"]:
            color = 'red'
        else:
            color = 'green'
        ax.barh(y_pos, 1, color=color)
        label = ("Terminal " + info["terminal"] +
                 " | Area " + info["boarding_area"] +
                 " | Gate " + info["gate"])
        labels.append(label)
        # Mostrar aircraft si está ocupado
        if info["occupied"]:
            ax.text(0.5, y_pos, info["aircraft_id"],
                    va='center', ha='center',
                    color='white', fontsize=8)
        y_pos += 1
        i += 1

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xticks([])

    ax.set_title("Barcelona Airport Gate Occupancy")
    plt.tight_layout()
    plt.show()

#’’’ Given bcn of class BarcelonaAP, this function returns a list of gates with
#their names, their status (free of occupied) and the id of the aircraft in
#case of occupied.


#INTERESTING ADDITION: Use the returning list, with gate occupancy, to call a
#new function to build a plot showing the airport terminals, boarding areas and
#gates, with the state of each gate. The figure in page 10 can be a simple
#example of the type of plot that would be very appreciated by the user. This
#would be considered as a nice extra functionality (see grading criteria for
#final version).



########################################################################################################################
#####################################              def AssignGate   (JOAN)               #####################################
########################################################################################################################

########################################################################################################################
#####################################           def LoadAirportStrutcure           #####################################
########################################################################################################################

def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
    except:
        return -1

    linies=f.readlines()
    f.close()
    if len(linies) == 0:
        return -1
    primera_linea = linies[0].split()
    if len(primera_linea) < 2:
        return -1

    airport_code = primera_linea[0]
    nombre_terminals = int(primera_linea[1])
    airport = BoardingArea(airport_code)

    i = 1

    for j in range(nombre_terminals):
        while i < len(linies) and linies[i].strip == "":
            i +=1
        if i >= len(linies):
            return -1
        linia_terminal = linies[i].split()
        if len(linia_terminal) < 3:
            return -1
        nom_terminal = linia_terminal[1]
        nombre_arees = int(linia_terminal[2])
        terminal = Terminal(nom_terminal)

        i += 1

        for a in range(nombre_arees):
            while i < len(linies) and linies[i].strip() == "":
                i +=1
            if i >= len(linies):
                return -1
            linia_area = linies[i].split()
            if len(area_linia) < 7:
                return -1
            lletra_area = area_linia[1]
            tipus_area = linia_area[2]
            init_gate = int(linia_area[4])
            end_gate = int(linia_area[6])
            area_name = nom_terminal + "BA" + lletra_area.lower()
            area = BoardingArea(area_name, tipus_area)
            prefix = area_name + "G"
            result = SetGates(area, init_gate, end_gate, prefix)
            if result == -1:
                return -1
            terminal.boarding_areas.append(area)
            i += 1
        result = LoadAirlines(terminal, nom_terminal)
        if result == -1:
            result -1
        airport.terminals.append(terminal)
    return airport

########################################################################################################################
#####################################           def IsAirlineInTerminal            #####################################
########################################################################################################################

def IsAirlineInTerminal (terminal, name):
    if name == "":
        return False
    if name in terminal.airlines:
        return True
    else:
        return False

########################################################################################################################
#####################################              def SearchTerminal              #####################################
########################################################################################################################

def SearchTerminal(bcn, name)
    i=0
    while i < len(bcn.terminals):
        j = bcn.terminals[i]
        if IsAirlineInTerminal(j, name):
            return j.name
        i += 1
    return ""










#### MODIFY UserInterface

if __name__ == "__main__":
    LEBL = BarcelonaAP.mro()
    gates = GateOccupancy(LEBL)
    PlotGates(gates)