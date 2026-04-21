import tkinter as tk
from time import strftime

def actualizar_reloj():
    # Obtiene la hora actual en formato H:M:S
    string = strftime('%H:%M:%S %p')
    # Actualiza el texto de la etiqueta
    label.config(text=string)
    # Llama a la función de nuevo después de 1 segundo
    label.after(1000, actualizar_reloj)

# Configuración de la ventana
root = tk.Tk()
root.title("Reloj Digital")

# Configuración de la etiqueta (fuente, colores)
label = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
label.pack(anchor='center')

# Iniciar el reloj
actualizar_reloj()
root.mainloop()

