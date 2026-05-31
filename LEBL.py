########################################################################################################################
#####################################        DEFINICION CLASE Y LIBRERÍAS    #######################################
########################################################################################################################
from airport import *
from aircraft import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
#####################################              def GateOccupancy               #####################################
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

########################################################################################################################
#####################################              def PlotGatesMap                #####################################
########################################################################################################################
def PlotGatesMap(gates_info):

    fig, ax = plt.subplots(figsize=(18, 12))

    gate_w = 0.6
    gate_h = 0.6
    sep_gate = 0.15
    sep_area_x = 3.5

    current_terminal = ""
    current_area = ""

    y_terminal = 0
    x_area = 2

    i = 0
    max_area_height = 0

    while i < len(gates_info):

        info = gates_info[i]

        # ---------- CAMBIO TERMINAL ----------
        if info["terminal"] != current_terminal:

            y_terminal -= (max_area_height + 3)
            max_area_height = 0

            current_terminal = info["terminal"]
            current_area = ""
            x_area = 2

            ax.plot([1, 22], [y_terminal, y_terminal], linewidth=4)
            ax.text(0.3, y_terminal, "T" + current_terminal,
                    va='center', fontsize=16)

        # ---------- CAMBIO AREA ----------
        if info["boarding_area"] != current_area:
            current_area = info["boarding_area"]
            x_area += sep_area_x

            count = 0
            j = i
            while j < len(gates_info) and gates_info[j]["boarding_area"] == current_area:
                count += 1
                j += 1

            per_side = (count + 1) // 2
            area_height = per_side * (gate_h + sep_gate)

            if area_height > max_area_height:
                max_area_height = area_height

            ax.plot([x_area, x_area],
                    [y_terminal, y_terminal - area_height],
                    linewidth=2)

            ax.text(x_area, y_terminal + 0.6,
                    "Area " + current_area,
                    ha='center', fontsize=11)

            y_left = y_terminal - gate_h - 0.2
            y_right = y_terminal - gate_h - 0.2
            side = "left"

        # ---------- COLOR ----------
        if info["occupied"]:
            color = "red"
        else:
            color = "green"

        # ---------- GUARDAMOS EL LADO REAL DEL GATE ----------
        gate_side = side

        # ---------- POSICIÓN GATE ----------
        if side == "left":
            x_gate = x_area - gate_w - 0.2
            y_gate = y_left
            y_left -= gate_h + sep_gate
            side = "right"
        else:
            x_gate = x_area + 0.2
            y_gate = y_right
            y_right -= gate_h + sep_gate
            side = "left"

        rect = Rectangle((x_gate, y_gate),
                         gate_w, gate_h,
                         facecolor=color)
        ax.add_patch(rect)

        # ---------- TEXTO GATE ----------
        ax.text(x_gate + gate_w / 2,
                y_gate + gate_h / 2,
                info["gate"],
                ha='center', va='center',
                fontsize=8, color='white')

        # ---------- TEXTO AVIÓN ----------
        if info["occupied"] and info.get("aircraft_id"):

            aircraft_text = info["aircraft_id"]

            if gate_side == "left":
                # avión va fuera del gate, hacia la izquierda
                x_text = x_gate - 0.15
                ha = "right"
            else:
                # avión va fuera del gate, hacia la derecha
                x_text = x_gate + gate_w + 0.15
                ha = "left"

            ax.text(
                x_text,
                y_gate + gate_h / 2,
                aircraft_text,
                va='center',
                ha=ha,
                fontsize=7,
                color="black",
            )

        i += 1

    ax.set_xlim(0, 24)
    ax.set_ylim(y_terminal - max_area_height - 5, 2)
    ax.axis('off')
    ax.set_title("Barcelona Airport Gate Diagram", fontsize=18)

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

def AssignGate(bcn, aircraft):

    # 1️⃣ Buscar terminal por aerolínea (company)
    terminal_name = SearchTerminal(bcn, aircraft.company)
    if terminal_name is None:
        return -1

    # 2️⃣ Obtener objeto terminal
    terminal_obj = None
    i = 0
    while i < len(bcn.terminals):
        if bcn.terminals[i].name == terminal_name:
            terminal_obj = bcn.terminals[i]
            break
        i += 1

    if terminal_obj is None:
        return -1

    # 3️⃣ Determinar si el vuelo es Schengen o no según ORIGIN
    schengen = IsSchengen(aircraft.origin)

    # 4️⃣ Buscar boarding area compatible
    j = 0
    while j < len(terminal_obj.boarding_areas):
        area = terminal_obj.boarding_areas[j]

        if area.type == schengen:   # coincide Schengen / No Schengen

            # 5️⃣ Buscar primera gate libre
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]

                if gate.occupied == False:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.id
                    return 0

                k += 1
        j += 1

    return -1


"""Given bcn of class BarcelonaAP and an aircraft of class Aircraft this
function looks for the first gate that is not occupied in the correct boarding
area. To decide the correct boarding area the function must check the airline terminal
assignment (using the SearchTerminal function defined above) and the
Schengen/non-Schengen type of flight-boarding area. The gate assignment
consists in updating the occupancy boolean and the aircraft field of the
chosen gate inside the bcn parameter. If there is not more free gates of the
correct type, an error code shall be returned and no modification of the bcn
parameter shall be done.
"""

########################################################################################################################
#####################################           def LoadAirportStrutcure           #####################################
########################################################################################################################

def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
    except:
        return -1

    linies = f.readlines()
    f.close()
    if len(linies) == 0:
        return -1
    primera_linea = linies[0].split()
    if len(primera_linea) < 2:
        return -1

    airport_code = primera_linea[0]
    nombre_terminals = int(primera_linea[1])
    LEBL = BarcelonaAP(airport_code)

    Nlinea = 0

    for i in range(nombre_terminals):
        Nlinea += 1
        lineaactual = linies[Nlinea].split(" ")     # Terminal T1 5 boarding areas
        terminal = Terminal(lineaactual[1])
        LEBL.terminals.append(terminal)

        Nboardingareas = int(lineaactual[2])
        for j in range(Nboardingareas):
            Nlinea += 1
            lineaactual = linies[Nlinea].split(" ") # Area A Schengen Gates 1 - 11
            boardingarea = BoardingArea(lineaactual[1], lineaactual[2]=="Schengen")
            terminal.boarding_areas.append(boardingarea)
            gateinicio = int(lineaactual[4])
            gatefinal = int(lineaactual[6])
            SetGates(boardingarea, gateinicio, gatefinal,lineaactual[1])

    return LEBL

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

def SearchTerminal(bcn, name):
    i=0
    while i < len(bcn.terminals):
        j = bcn.terminals[i]
        if IsAirlineInTerminal(j, name):
            return j.name
        i += 1
    return


if __name__ == "__main__":

    LEBL = LoadAirportStructure("LEBL.txt")

    i = 0
    while i < len(LEBL.terminals):
        LoadAirlines(LEBL.terminals[i], LEBL.terminals[i].name)
        i += 1

    arrivals = LoadArrivals("Arrivals.txt")

    print("Total aircraft arrivals:", len(arrivals))

    i = 0
    while i < len(arrivals):
        aircraft = arrivals[i]
        result = AssignGate(LEBL, aircraft)
        if result == 0:
            print("Aircraft", aircraft.id, "assigned correctly")
        else:
            print("Aircraft", aircraft.id, "could NOT be assigned")
        i += 1

    gates = GateOccupancy(LEBL)
    PlotGatesMap(gates)



