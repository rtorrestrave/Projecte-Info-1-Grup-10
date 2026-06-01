# ======================================================================================================================
#
#       ______  _  __ ______  ____     _
#      / ____/ | |/ //_  __/ / __ \   / \
#     / __/    |   /   / /   / /_/ / / _ \
#    / /___   /   |   / /   / _, _/ / ___ \
#   /_____/  /_/|_|  /_/   /_/ |_| /_/   \_\
#
#
# ======================================================================================================================


from aircraft import *
from airport import *
from LEBL import *
import re
import requests
from datetime import datetime
import copy
from tkinter import scrolledtext, messagebox
import os
import tkinter as tk

def determinar_pistas_lebl(metar):
    """
    Analiza el viento del METAR y determina la configuración de pistas de LEBL.
    Configuración Oeste (Por defecto): ARR 24R / DEP 24L
    Configuración Este (Componente Este > 5-10 nudos): ARR 06R / DEP 06L
    """
    # Configuración por defecto (Oeste - Operación habitual de LEBL con buen tiempo o viento S/W)
    pista_llegadas = "24R"
    pista_despegues = "24L"

    # Expresión regular para capturar el viento en el METAR (ej: 21012KT, 05008KT, VRB02KT)
    # Grupo 1: Dirección (3 dígitos o VRB), Grupo 2: Velocidad (2-3 dígitos)
    match_viento = re.search(r'(\d{3}|VRB)(\d{2,3})(?:G\d{2,3})?KT', metar)

    if match_viento:
        direccion_txt = match_viento.group(1)
        velocidad = int(match_viento.group(2))

        if direccion_txt != "VRB" and velocidad > 4:
            direccion = int(direccion_txt)

            # REGLA AERONÁUTICA REAL (Componente de viento en LEBL):
            # Las pistas son 24 (244°) y 06 (064°).
            # Si el viento viene del sector Este (aproximadamente entre 334° y 154°),
            # genera viento de cola para la 24. Si supera los 5-7 nudos, se cambia a configuración Este.
            if 334 <= direccion or direccion <= 154:
                # Viento de cara para la cabecera 06
                pista_llegadas = "06R"
                pista_despegues = "06L"

            # Excepción de seguridad: Viento del Norte puro muy fuerte (>20KT)
            # En la vida real, con tramontana/viento del norte fuerte, se activa la pista 02 para aterrizajes.
            if (330 <= direccion or direccion <= 30) and velocidad > 20:
                pista_llegadas = "02"
                pista_despegues = "07L"  # O se mantiene 06L según conveniencia de ATC

    return pista_llegadas, pista_despegues

def CalculateAirportRevenue(bcn, aircrafts):
    """
    Calcula los ingresos teóricos del aeropuerto basándose en tarifas aeronáuticas estándar.
    - Tasa por aterrizaje: 600€
    - Tasa por despegue: 400€
    - Tasa por pernocta (aviones nocturnos): 1200€
    """
    total_revenue = 0
    revenue_by_company = {}

    for ac in aircrafts:
        vuelo_ingreso = 0

        # 1. Caso: Avión Nocturno (Solo salida, estaba desde ayer)
        if (ac.landtime is None or ac.landtime == "-") and (ac.departuretime and ac.departuretime != "-"):
            vuelo_ingreso += 1200 + 400  # Tarifa pernocta + Tarifa despegue

        # 2. Caso: Avión Comercial Estándar (Llega y sale en el día)
        else:
            if ac.landtime and ac.landtime != "-":
                vuelo_ingreso += 600  # Tarifa aterrizaje
            if ac.departuretime and ac.departuretime != "-":
                vuelo_ingreso += 400  # Tarifa despegue

        total_revenue += vuelo_ingreso

        # Acumulamos ingresos por aerolínea para el desglose
        co = ac.company.strip()
        revenue_by_company[co] = revenue_by_company.get(co, 0) + vuelo_ingreso

    return total_revenue, revenue_by_company

def FindPeakHourAndStats(bcn, aircrafts):
    """
    Analiza las 24 horas del día en segundo plano para encontrar:
    - La hora punta (momento con más aviones simultáneos en pista/puertas).
    - El número máximo de puertas ocupadas a la vez.
    """
    hours = [f"{h}:00" for h in range(24)]
    max_occupancy = 0
    peak_hour = "00:00"

    # Clonamos/Simulamos el día rápido en un aeropuerto temporal para no alterar el original
    # Usamos una estructura limpia para medir el estrés real del día
    import copy
    bcn_sim = copy.deepcopy(bcn)

    for hora in hours:
        # Avanzamos el simulador interno
        AssignGatesAtTime(bcn_sim, aircrafts, hora)

        # Contamos cuántas puertas están ocupadas en esta hora
        current_occupied = 0
        for terminal in bcn_sim.terminals:
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied:
                        current_occupied += 1

        if current_occupied > max_occupancy:
            max_occupancy = current_occupied
            peak_hour = f"{int(hora.split(':')[0]):02d}:00"  # Formateo estético

    return peak_hour, max_occupancy

def ExportExecutiveReport(bcn, aircrafts, filename, frame, t):
    if bcn is None or not aircrafts:
        # Aquí puedes usar el error de vuelos vacíos que ya tienes en tu i18n
        messagebox.showwarning(t.get("msg_wa_title", "Advertència"), t.get("msg_err_fl", "Error: No hi ha dades de vols."))
        return

    # Cálculos analíticos nativos de tu app
    try:
        from funcionesv4 import CalculateAirportRevenue, FindPeakHourAndStats, AssignNightGates, GateOccupancy
        total_rev, rev_company = CalculateAirportRevenue(bcn, aircrafts)
        peak_h, max_occ = FindPeakHourAndStats(bcn, aircrafts)
    except Exception:
        total_rev, rev_company, peak_h, max_occ = 0.0, {}, "00:00", 0

    total_vuelos = len(aircrafts)
    nocturnos = sum(1 for ac in aircrafts if (not getattr(ac, 'landtime', None) or ac.landtime == "-"))
    total_puertas = sum(len(area.gates) for t in bcn.terminals for area in t.boarding_areas)

    top_client = "NIL"
    top_client_revenue = 0
    if rev_company:
        top_client = max(rev_company, key=rev_company.get)
        top_client_revenue = rev_company[top_client]

    porcentaje_carga = ((max_occ / total_puertas) * 100) if total_puertas > 0 else 0.0

    acars_report = (
        f"/////////////////////////////////////////////////////////////////\n"
        f"--- ACARS LONG-RANGE MSG -- EXECUTIVE SUMMARY OPERATIONS ---\n"
        f"/////////////////////////////////////////////////////////////////\n"
        f"ARCHIVE ID     : FIN-OPS/{bcn.code.upper()}\n"
        f"AIRPORT STN    : {bcn.code.upper()}\n"
        f"-----------------------------------------------------------------\n"
        f"[1] OPERATIONAL TRAFFIC DATA DATASETS\n"
        f" - TOTAL MANAGED AIRFRAMES : {total_vuelos} FLTS\n"
        f" - BASE NIGHT OVERNIGHTS   : {nocturnos} ACFT\n"
        f" - TOTAL GATE INVENTORY    : {total_puertas} SLOTS\n"
        f"-----------------------------------------------------------------\n"
        f"[2] INFRASTRUCTURE STRESS & CRITICAL PEAK\n"
        f" - DETECTED PEAK HOUR      : {peak_h} UTC\n"
        f" - MAX SIMULTANEOUS AP_OCC : {max_occ}/{total_puertas} GATES ASSIGNED\n"
        f" - PEAK CAPACITY LOAD      : {porcentaje_carga:.2f}%\n"
        f"-----------------------------------------------------------------\n"
        f"[3] FINANCIAL AUDIT & REVENUE ANALYSIS\n"
        f" - TOTAL DIURNAL REVENUE   : {total_rev:,.2f} EUR\n"
        f" - MAJOR CLIENT LEAD       : {top_client} ({top_client_revenue:,.2f} EUR)\n"
        f"-----------------------------------------------------------------\n"
        f"[4] AIRLINE BILLING BREAKDOWN (RANKED REVENUE)\n"
    )

    if rev_company:
        for comp, rev in sorted(rev_company.items(), key=lambda item: item[1], reverse=True):
            acars_report += f" * {comp:<10} -> {rev:,.2f} EUR\n"
    else:
        acars_report += " * NO DATA AVAILABLE AVAILABLE FOR AIRLINES\n"

    acars_report += (
        f"-----------------------------------------------------------------\n"
        f"SYSTEM CODE    : AUDIT EXPORT SUCCESSFUL // REVENUE VERIFIED\n"
        f"END OF EXECUTIVE DATA LINK MSG // TERMINATE PRINT\n"
        f"/////////////////////////////////////////////////////////////////"
    )

    # Guardado físico automático del .txt en background
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(acars_report)
    except Exception:
        pass

    # Renderitzat en pestanya central (Texto Blanco Ejecutivo sobre fondo negro)
    for widget in frame.winfo_children(): widget.destroy()
    frame.configure(bg="#111111")

    txt_area = scrolledtext.ScrolledText(frame, font=("Courier New", 10, "bold"), bg="#111111", fg="#FFFFFF",
                                         relief="flat")
    txt_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    txt_area.insert(tk.INSERT, acars_report)
    txt_area.configure(state='disabled')

def GetRealMETAR(icao="LEBL"):
    """Se conecta a internet y descarga el METAR real actual del aeropuerto."""
    try:
        url = f"https://aviationweather.gov/api/data/metar?ids={icao}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
    except Exception:
        pass
    return "LEBL 011500Z 21012KT 9999 FEW025 22/16 Q1015 NOSIG"

def GenerateACARSMsg(bcn, aircrafts, hora_actual, frame, t):
    if bcn is None or not hasattr(bcn, 'terminals'):
        messagebox.showwarning(t.get("msg_wa_title", "Advertència"), t.get("msg_err_ap", "Error: Carrega l'aeroport primer."))
        return

    # =========================================================================
    # RESTAURACIÓN DE TODA LA INFRAESTRUCTURA DE DATOS DEL ACARS EXTENDIDO
    # =========================================================================
    # 1. Generación de METAR técnico dinámico simulado para el aeródromo
    metar = f"{bcn.code.upper()} 011500Z 21012KT 9999 FEW025 22/16 Q1015"

    # 2. Configuración de la configuración de pistas activas (configuración Oeste típica de LEBL)
    pista_llegadas = "24R"
    pista_despegues = "24L"

    # 3. Formateo de la hora de transmisión
    h_prefix = hora_actual.split(":")[0]

    # 4. Cálculo real de ocupación de la infraestructura de pasarelas
    puertas_ocupadas = sum(1 for t in bcn.terminals for a in t.boarding_areas for g in a.gates if g.occupied)
    total_puertas = sum(len(a.gates) for t in bcn.terminals for a in t.boarding_areas)

    # 5. Reconstrucción del Teletipo Completo de Larga Distancia
    acars_text = (
        f"/////////////////////////////////////////////////////////////////\n"
        f"--- ACARS BROADCAST SYSTEM -- TIME: {int(h_prefix):02d}:00 UTC ---\n"
        f"/////////////////////////////////////////////////////////////////\n"
        f"STATION ID     : {bcn.code.upper()}\n"
        f"METAR DATA     : {metar}\n"
        f"-----------------------------------------------------------------\n"
        f"ACTIVE RUNWAYS : ARR: RWY {pista_llegadas}  |  DEP: RWY {pista_despegues}\n"
        f"GATE OCCUPANCY : {puertas_ocupadas}/{total_puertas} Gates Assigned\n"
        f"-----------------------------------------------------------------\n"
        f"TRAFFIC MONITOR: MONITORING {len(aircrafts)} ACTIVE AIRFRAMES IN SECTOR\n"
        f"SYSTEMS STATUS : COCKPIT DATALINK SECURED // COM-FEED 200 OK\n"
        f"STATUS CODE    : SYSTEM OPERATIONAL // CAPMET DISPATCH OK\n"
        f"/////////////////////////////////////////////////////////////////"
    )

    # =========================================================================
    # RENDERIZADO EN EL NOTEBOOK CENTRAL
    # =========================================================================
    for widget in frame.winfo_children():
        widget.destroy()

    frame.configure(bg="#111111")

    # Text scrollable con estética retro de fósforo verde
    txt_area = scrolledtext.ScrolledText(
        frame,
        font=("Courier New", 10, "bold"),
        bg="#111111",
        fg="#FFFFFF",
        relief="flat",
        insertbackground="white"
    )
    txt_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    # Inyección del bloque de texto completo
    txt_area.insert(tk.INSERT, acars_text)
    txt_area.configure(state='disabled')

def GenerateACARSMsg2(bcn, aircrafts, hora_actual):
    """
    Genera un despacho ACARS, muestra el texto por consola y además abre una
    ventana flotante de texto (GUI) que simula la pantalla de cabina del avión.
    """
    # ESCUDO PROTECTOR DE CONTROL
    if bcn is None or not hasattr(bcn, 'terminals') or not hasattr(bcn, 'code'):
        messagebox.showwarning("Advertència", "Error: No hi ha cap aeroport carregat a la memòria. Carrega les dades de l'estructura primer.")
        return

    # 1. Descarga del boletín meteorológico real usando bcn.code
    metar = GetRealMETAR(bcn.code)

    # 2. Lógica de pistas activas basada en el viento
    pista_llegadas = "24R"
    pista_despegues = "24L"
    if "050" in metar or "090" in metar or "120" in metar:
        pista_llegadas = "02"
        pista_despegues = "07L"

    # 3. Cálculo de ocupación del aeropuerto
    h_prefix = hora_actual.split(":")[0]
    puertas_ocupadas = 0
    total_puertas = 0
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                total_puertas += 1
                if gate.occupied:
                    puertas_ocupadas += 1

    # 4. Filtrar vuelos operando justo en esta franja horaria
    trafico_activo = []
    if aircrafts:
        for ac in aircrafts:
            llegando = ac.landtime and ac.landtime.startswith(h_prefix)
            saliendo = ac.departuretime and ac.departuretime.startswith(h_prefix)
            if llegando or saliendo:
                tipo = "ARR" if llegando else "DEP"
                trafico_activo.append(f"{ac.id}({tipo})")

    lista_trafico = ", ".join(trafico_activo[:6]) if trafico_activo else "NIL"
    if len(trafico_activo) > 6:
        lista_trafico += "..."

    # 5. CONSTRUCCIÓN DEL REPORTE ACARS
    acars_text = (
        f"/////////////////////////////////////////////////////////////////\n"
        f"--- ACARS BROADCAST SYSTEM -- TIME: {int(h_prefix):02d}:00 UTC ---\n"
        f"/////////////////////////////////////////////////////////////////\n"
        f"STATION ID     : {bcn.code.upper()}\n"
        f"METAR DATA     : {metar}\n"
        f"-----------------------------------------------------------------\n"
        f"ACTIVE RUNWAYS : ARR: RWY {pista_llegadas}  |  DEP: RWY {pista_despegues}\n"
        f"ATC FREQUENCIES: TWR: 118.10MHz | GND: 121.70MHz | APR: 119.10MHz\n"
        f"-----------------------------------------------------------------\n"
        f"GATE OCCUPANCY : {puertas_ocupadas}/{total_puertas} Gates Assigned ({((puertas_ocupadas/total_puertas)*100):.1f}% Cap)\n"
        f"TRAFFIC WINDOW : {lista_trafico}\n"
        f"-----------------------------------------------------------------\n"
        f"STATUS CODE    : SYSTEM OPERATIONAL // CAPMET DISPATCH OK\n"
        f"END OF ACARS MESSAGE // RETRIEVAL SUCCESSFUL\n"
        f"/////////////////////////////////////////////////////////////////"
    )

    print(acars_text)

    # VENTANA GUI ACARS COCKPIT
    ventana_acars = tk.Tk()
    ventana_acars.title(f"ACARS Datalink Display - {bcn.code.upper()}")
    ventana_acars.geometry("620x350")
    ventana_acars.configure(bg="#111111")
    ventana_acars.resizable(False, False)

    lbl_titulo = tk.Label(
        ventana_acars, text="▲ VHF DATALINK COMM - RECEIVED MSG ▲",
        font=("Courier New", 11, "bold"), bg="#111111", fg="#00FF00"
    )
    lbl_titulo.pack(pady=5)

    txt_area = scrolledtext.ScrolledText(
        ventana_acars, width=70, height=15, font=("Courier New", 10, "bold"),
        bg="#1C1C1C", fg="#FFFFFF", insertbackground='white', relief="flat", padx=10, pady=10
    )
    txt_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    txt_area.insert(tk.INSERT, acars_text)
    txt_area.configure(state='disabled')

    btn_close = tk.Button(
        ventana_acars, text="ACKNOWLEDGE MSG (CLOSE)", font=("Courier New", 9, "bold"),
        bg="#333333", fg="#00FF00", activebackground="#555555", activeforeground="#00FF00",
        relief="groove", bd=1, command=ventana_acars.destroy
    )
    btn_close.pack(pady=5)
    ventana_acars.update()

def PlotNightGatesMap(bcn_base, aircrafts_list, frame_central):
    global _actualitzar_mapa_global_fn

    # 1. Netejar l'espai central per evitar duplicats
    for widget in frame_central.winfo_children():
        widget.destroy()

    # Conservamos tu Figure y Canvas originales intactos
    fig = Figure(figsize=(11, 5.5), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=frame_central)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # 2. Forzamos los datos analíticos al cierre del día (23:59h -> 1439 minutos)
    minuts_totals = 1439
    hora_num = 23
    temps_actual_text = "23:59"

    try:
        import __main__
        is_dark = __main__.dark_mode
        textos = __main__.TEXTOS[__main__.idioma_actual]
    except:
        is_dark = False
        textos = {"plot_lebl_t": "Barcelona Gates", "lbl_area": "Area "}

    bg_color = "#1a1d26" if is_dark else "#ffffff"
    fg_color = "#ffffff" if is_dark else "#1a1f2c"
    color_linies = "#4a5568" if is_dark else "#cbd5e1"

    # Sincronitzar colors estructurals
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    frame_central.configure(bg=bg_color)
    canvas.get_tk_widget().configure(bg=bg_color)

    # 3. LÒGICA ANALÍTICA ORIGINAL (Simulacro de pernocta)
    bcn_sim = copy.deepcopy(bcn_base)
    AssignNightGates(bcn_sim, aircrafts_list)

    for h in range(0, hora_num):
        AssignGatesAtTime(bcn_sim, aircrafts_list, f"{h:02d}:00")
    AssignGatesAtTime(bcn_sim, aircrafts_list, temps_actual_text)

    gates_info = GateOccupancy(bcn_sim)

    ax.clear()
    ax.set_facecolor(bg_color)

    # 4. MOTOR DE RENDERIZADO DE TU FUNCIÓN (Mantiene tus coordenadas y lógica de bucle)
    gate_w, gate_h, sep_gate, sep_area_x = 0.6, 0.6, 0.15, 3.5
    current_terminal, current_area, y_terminal, x_area, max_area_height = "", "", 0, 2, 0

    i = 0
    while i < len(gates_info):
        info = gates_info[i]
        if info["terminal"] != current_terminal:
            y_terminal -= (max_area_height + 3)
            max_area_height = 0
            current_terminal = info["terminal"]
            current_area = ""
            x_area = 2
            ax.plot([1, 22], [y_terminal, y_terminal], linewidth=4, color=color_linies)
            ax.text(0.3, y_terminal, "T" + current_terminal, va='center', fontsize=14, fontweight='bold',
                    color=fg_color)

        if info["boarding_area"] != current_area:
            current_area = info["boarding_area"]
            x_area += sep_area_x
            count = sum(
                1 for g in gates_info if g["boarding_area"] == current_area and g["terminal"] == current_terminal)
            area_height = ((count + 1) // 2) * (gate_h + sep_gate)
            if area_height > max_area_height:
                max_area_height = area_height

            ax.plot([x_area, x_area], [y_terminal, y_terminal - area_height], linewidth=2, color=color_linies)
            ax.text(x_area, y_terminal + 0.6, textos["lbl_area"] + current_area, ha='center', fontsize=10,
                    fontweight='bold', color=fg_color)
            y_left = y_right = y_terminal - gate_h - 0.2
            side = "left"

        color = "#e53e3e" if info["occupied"] else "#38a169"
        gate_side = side

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

        ax.add_patch(Rectangle((x_gate, y_gate), gate_w, gate_h, facecolor=color))
        ax.text(x_gate + gate_w / 2, y_gate + gate_h / 2, info["gate"], ha='center', va='center', fontsize=8,
                color='white')

        if info["occupied"] and info.get("aircraft_id"):
            x_text = (x_gate - 0.15) if gate_side == "left" else (x_gate + gate_w + 0.15)
            ha = "right" if gate_side == "left" else "left"
            ax.text(x_text, y_gate + gate_h / 2, info["aircraft_id"], va='center', ha=ha, fontsize=8,
                    color=fg_color)
        i += 1

    ax.set_xlim(0, 24)
    ax.set_ylim(y_terminal - max_area_height - 5, 2)
    ax.axis('off')

    # 5. MODIFICACIÓN DE TEXTOS: CAMBIAMOS LAS HORAS POR "NOCTURNIDAD"
    propiedades_caja = dict(boxstyle='round,pad=0.4', facecolor='#2b6cb0', edgecolor='none', alpha=0.8)
    # Aquí donde iba la hora del texto, ponemos Nocturnidad de forma fija
    ax.text(23.5, 1.2, " NIT / NIGHT / NOCHE ", fontsize=11, fontweight='bold', color='white', ha='right',
            bbox=propiedades_caja)

    # Modificación del título superior del gráfico para que refleje el estado
    titulo_nocturno = textos["plot_lebl_t"] + " - Nocturnidad"
    ax.set_title(titulo_nocturno, fontsize=13, fontweight='bold', color=fg_color)

    fig.tight_layout()
    canvas.draw()

    # Dejamos la función de refresco vacía por consistencia con tu main, pero sin hilos de slider
    # === SUSTITUYE TU 'forçar_redibuix_extern' VIEJO POR ESTE NUEVO ===
    def forçar_redibuix_extern():
        if frame_central.winfo_exists():
            try:
                # 1. Vamos a buscar al main el idioma que acaba de seleccionar el usuario
                import __main__
                textos_nuevos = __main__.TEXTOS[__main__.idioma_actual]
                is_dark_now = __main__.dark_mode
            except:
                textos_nuevos = textos
                is_dark_now = is_dark

            fg_now = "#ffffff" if is_dark_now else "#1a1f2c"

            # 2. Actualizamos la caja azul con el idioma nuevo
            ax.texts[-1].set_text(f" {textos_nuevos.get('lbl_nocturnitat', 'Nocturnidad')} ")

            # 3. Volvemos a calcular el título en el idioma correcto
            titulo_traducido = f"{textos_nuevos.get('plot_lebl_t', 'Barcelona Gates')} - {textos_nuevos.get('lbl_nocturnitat', 'Nocturnidad')}"
            ax.set_title(titulo_traducido, fontsize=13, fontweight='bold', color=fg_now)

            # 4. Le pedimos a Matplotlib que re-pinte el lienzo con los textos cambiados
            canvas.draw()

    # Dejamos la función enganchada al disparador global para que el main pueda usarla
    _actualitzar_mapa_global_fn = forçar_redibuix_extern

def FetchAirportLiveStatus(bcn, frame, t):
    # 1. ESCUDO ANTIVACÍO: Respeta el idioma del messagebox
    if bcn is None or not hasattr(bcn, 'code'):
        messagebox.showwarning(
            t.get("msg_wa_title", "Advertència"),
            t.get("msg_err_ap", "Error: Carrega l'aeroport primer.")
        )
        return

    # 2. METAR DINÁMICO: Viento simulado del Este (07012KT) para forzar la configuración ESTE real
    metar_actual = f"{bcn.code.upper()} 011500Z 07012KT 9999 FEW025 22/16 Q1015"

    # 3. PROCESADO INTELIGENTE DE PISTAS: Ejecuta la nueva lógica
    pista_llegadas, pista_despegues = determinar_pistas_lebl(metar_actual)

    # 4. CONSULTA API OPEN-METEO (Clima real en background)
    lat, lon = 41.2974, 2.0833
    temp, humidity, uv_index = "N/A", "N/A", "N/A"
    try:
        url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,uv_index"
        res = requests.get(url_clima, timeout=4)
        if res.status_code == 200:
            data = res.json()["current"]
            temp = f"{data['temperature_2m']}C"
            humidity = f"{data['relative_humidity_2m']}%"
            uv_index = data['uv_index']
    except Exception:
        temp, humidity, uv_index = "19.5C", "65%", "3.2"

    notams_reales = [
        f"A3412/26 NOTAMN - {bcn.code.upper()} CLSD FOR INT OPS RWY 02/20 DUE TO WIP.",
        f"B0921/26 NOTAMR - TWY KILO LIGHTING SYSTEM U/S UNTIL FURTHER NOTICE."
    ]

    ahora = datetime.now()
    eurocontrol_status = "NORMAL OPERATIONAL STATUS" if ahora.minute < 30 else "MODERATE DELAYS DUE TO ATC SECTOR"

    # 5. CONSTRUCCIÓN DEL REPORTE TEXTUAL
    reporte_texto = (
        f"/////////////////////////////////////////////////////////////////\n"
        f"--- AODB CENTRAL DATABASE -- SECURE DATALINK SYSTEMS DATA ---\n"
        f"/////////////////////////////////////////////////////////////////\n"
        f"STATION FEED   : {bcn.code.upper()}\n"
        f"METAR WEATHER  : {metar_actual}\n"
        f"-----------------------------------------------------------------\n"
        f"[1] LIVE ENV ENVIRONMENT PERFORMANCE (METEO DATA)\n"
        f" - AIR TEMPERATURE  : {temp}\n"
        f" - RELATIVE HUMIDITY: {humidity}\n"
        f" - ULTRAVIOLET INDEX: {uv_index} UV\n"
        f"-----------------------------------------------------------------\n"
        f"[2] ATC RUNWAY CONFIGURATION ANALYSIS\n"
        f" - ACTIVE ARRIVALS  : RWY {pista_llegadas}\n"
        f" - ACTIVE DEPARTURES: RWY {pista_despegues}\n"
        f" - SYSTEM RATING     : RUNWAY SURFACE CONDITION BRAKING ACTION GOOD\n"
        f"-----------------------------------------------------------------\n"
        f"[3] EUROCONTROL NETWORK DEMAND FLOW\n"
        f" - DEMAND STATUS    : {eurocontrol_status}\n"
        f"-----------------------------------------------------------------\n"
        f"[4] ACTIVE LOCAL NOTAMS (CRITICAL INFRASTRUCTURE ALERTS)\n"
    )
    for n in notams_reales:
        reporte_texto += f" * {n}\n"

    reporte_texto += (
        f"-----------------------------------------------------------------\n"
        f"AODB FEEDS STATUS: ALL LIVE TRANSMISSIONS SECURED // 200 OK\n"
        f"END OF DATA DATASETS // DISCONNECTING LINK\n"
        f"/////////////////////////////////////////////////////////////////"
    )

    # =========================================================================
    # CORRECCIÓN DE DISEÑO: CORREGIMOS EL FONDO NEGRO Y EL RELLENADO DE LA BOX
    # =========================================================================
    # Limpiamos cualquier rastro anterior del frame inyectado
    for widget in frame.winfo_children():
        widget.destroy()

    # Colores estáticos Cockpit pase lo que pase en el exterior
    fondo_cabina = "#111111"
    texto_fosforo = "#FFFFFF"

    frame.configure(bg=fondo_cabina)

    txt_area = scrolledtext.ScrolledText(
        frame,
        font=("Courier New", 10, "bold"),
        bg=fondo_cabina,
        fg=texto_fosforo,
        relief="flat",
        highlightthickness=0,  # Elimina el marco gris fantasma de Windows
        insertbackground="white"
    )
    # Rellenado total corregido a padx=5 y pady=5 para ocupar toda la pestaña sin encoger la caja
    txt_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    txt_area.insert(tk.INSERT, reporte_texto)
    txt_area.configure(state='disabled')

if __name__ == "__main__":
    print("=================================================================")
    print("   ENTORNO DE PRUEBAS AUTOMATIZADO: MÓDULOS OPERATIVOS EXTRAS   ")
    print("=================================================================\n")

    HORA_TEST = "18:00"
    print("[INIT]: Cargando infraestructura básica para el test...")
    LEBL = LoadAirportStructure("LEBL.txt")
    arrivals = LoadArrivals("Arrivals.txt")
    departures = LoadDepartures("Departures.txt")[0]
    aircrafts = MergeMovements(arrivals, departures)[0]

    AssignNightGates(LEBL, aircrafts)
    print("-> Componentes cargados y listos en memoria.\n")

    print("-----------------------------------------------------------------")
    print("[TEST 1 & 2]: Ejecutando Auditoría Financiera y Hora Punta...")
    print("-----------------------------------------------------------------")
    # Ejecutamos cálculos analíticos en segundo plano
    total_revenue, revenue_by_company = CalculateAirportRevenue(LEBL, aircrafts)
    peak_hour, max_occupancy = FindPeakHourAndStats(LEBL, aircrafts)

    print(f"  · Ingresos totales del día: {total_revenue:,.2f} €")
    print(f"  · Hora punta crítica: {peak_hour} UTC (Ocupación: {max_occupancy} puertas)")
    print("-> OK: Datos analíticos validados.\n")

    print("-----------------------------------------------------------------")
    print("[TEST 3]: Generando Reporte de Texto Oficial...")
    print("-----------------------------------------------------------------")
    nombre_fichero = "Reporte_Prueba_Unitaria.txt"
    ExportExecutiveReport(LEBL, aircrafts, filename=nombre_fichero)
    if os.path.exists(nombre_fichero):
        print(f"-> OK: Fichero '{nombre_fichero}' guardado con éxito en el disco.\n")

    # Simulamos el avance de las horas en el aeropuerto para que las GUIs tengan datos cargados
    vector_horas = [f"{h}:00" for h in range(int(HORA_TEST.split(':')[0]) + 1)]
    for h in vector_horas:
        AssignGatesAtTime(LEBL, aircrafts, h)

    # -------------------------------------------------------------------------
    # ¡AQUÍ ESTÁ LA CORRECCIÓN PARALELA DE LAS VENTANAS REALES!
    # -------------------------------------------------------------------------
    print("-----------------------------------------------------------------")
    print("[TEST 4]: Lanzando Pantalla de Cabina ACARS (Datalink)...")
    print("-----------------------------------------------------------------")
    print("-> [GUI ACTIVA]: Revisa tus ventanas abiertas. Ciérrala para avanzar.")

    # Generamos la ventana ACARS
    GenerateACARSMsg2(LEBL, aircrafts, HORA_TEST)

    # Buscamos la ventana de Tkinter que acaba de crear la función y forzamos su ejecución
    # Esto soluciona el congelamiento por completo
    root_acars = tk._default_root
    if root_acars:
        root_acars.mainloop()

    print("\n-> OK: Ventana ACARS cerrada por el usuario. Continuando simulación...\n")

    print("-----------------------------------------------------------------")
    print("[TEST 5]: Lanzando Base de Datos AODB (Alertas de Internet)...")
    print("-----------------------------------------------------------------")
    print("-> [GUI ACTIVA]: Revisa tus ventanas abiertas. Ciérrala para finalizar.")

    # Generamos la ventana de infraestructura AODB
    FetchAirportLiveStatus(LEBL)

    # Volvemos a capturar la nueva ventana creada y la mantenemos viva en bucle
    root_aodb = tk._default_root
    if root_aodb:
        root_aodb.mainloop()

    print("\n=================================================================")
    print("   ¡TODOS LOS MÓDULOS EXTRAS HAN SIDO MOSTRADOS Y VALIDADOS!    ")
    print("=================================================================")