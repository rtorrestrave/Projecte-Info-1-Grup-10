from airport import *
airports = LoadAirports("ResultsSchengen.txt")
lista = airports
print(len(lista))

print("Prueba. Vamos a añadir un aeropuerto. El aeropuerto CYYZ")
CYYZ = Airport(icao="CYYZ",lat=10,lon=10)
airports = AddAirport(airports, CYYZ)

print(len(lista))

print("Ahora mostraremos el aeropuerto CYYZ con la fx PrintAirport")
PrintAirport(CYYZ)
print("Ahora vamos a quitarlo")
airports = RemoveAirports(airports, "CYYZ")

print(len(lista))

print("y vamos a Guardar la lista en el archivo")
SaveAirportList(airports, "ResultsSchengen.txt")
print(len(lista))

print("Vamos a volver a añadirlo. Va a preguntarnos si queremos sobreescribirlo")
airports = AddAirport(airports, CYYZ)
print(len(lista))

print("y finalmente vamos a generar un plot de los aeropuertos schengen.")
#primero generamos atributos schengen para toda la lista
for i in range(len(airports)):
    airports[i].schengen = IsSchengen(airports[i].icao)

print(len(lista))
PlotAirports(airports)

