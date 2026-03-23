from airport import *
print("Prueba. Vamos a añadir un aeropuerto.")
##AddAirport()
print("Ahora mostraremos el aeropuerto EGKK con la fx PrintAirport")
airport = Airport("EGKK", 41.297445, 2.0832941)
PrintAirport(airport)

print("Ahora vamos a quitar un aeropuerto.")
##RemoveAirports()

PlotAirports(LoadAirports("airports.txt"))