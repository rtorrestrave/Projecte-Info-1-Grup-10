# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


i=0
encontrado= False

while i < len(airports) and not encontrado:
    if airports[i].schengen == True:
        encontrado=True
    if not encontrado:
        i= i +1
if encontrado:
    print("Primer aeropuerto en Germany:", airports[i].icao)
else:
    print("No hay aeropuertos en Germany en la lista.")
neg = []
i = 0
for i in range( len(airports)):
    if airports[i].longuitude < 0 :
        neg.append(airports[i])

print("Los siguientes aeropuertos tiene longitud negativa")
i = 0
for i in range( len(neg)):
    print(neg[i].icao)
