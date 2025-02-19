import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
import numpy as np
import time


cred = credentials.Certificate("ruta/al/archivo.json")  # Ubicacion
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tu-proyecto.firebaseio.com'  # Link
})

ref = db.reference('/historial')

def guardar_operacion(operacion, resultado):
    """Guarda una operación en Firebase."""
    timestamp = int(time.time() * 1000)
    nueva_operacion_ref = ref.push({
        'operacion': operacion,
        'resultado': resultado,
        'timestamp': timestamp
    })
    print(f"Operación guardada con ID: {nueva_operacion_ref.key}")

#Funciones
def abrir_calculadora_basica():
    """Calculadora con operaciones básicas."""
    def click_boton(valor):
        entrada.set(entrada.get() + str(valor))

    def calcular():
        try:
            operacion = entrada.get()
            resultado = eval(operacion)
            resultado_var.set(resultado)
            guardar_operacion(operacion, resultado)
        except:
            messagebox.showerror("Error", "Operación no válida")

    ventana = tk.Toplevel(root)
    ventana.title("Calculadora Básica")
    entrada = tk.StringVar()
    resultado_var = tk.StringVar()

    tk.Entry(ventana, textvariable=entrada, font=("Arial", 18), width=15, justify="right").grid(row=0, column=0, columnspan=4)
    tk.Label(ventana, textvariable=resultado_var, font=("Arial", 18), bg="lightgray", width=15).grid(row=1, column=0, columnspan=4)

    botones = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
    ]

    for text, row, col in botones:
        tk.Button(ventana, text=text, font=("Arial", 14), width=5, height=2,
                  command=lambda t=text: click_boton(t) if t != "=" else calcular()).grid(row=row, column=col)

def abrir_calculadora_cientifica():
    """Calculadora científica con funciones avanzadas."""
    def calcular():
        try:
            operacion = entrada.get()
            resultado = eval(operacion, {"math": math})
            resultado_var.set(resultado)
            guardar_operacion(operacion, resultado)
        except:
            messagebox.showerror("Error", "Operación no válida")

    ventana = tk.Toplevel(root)
    ventana.title("Calculadora Científica")
    entrada = tk.StringVar()
    resultado_var = tk.StringVar()

    tk.Entry(ventana, textvariable=entrada, font=("Arial", 18), width=15, justify="right").grid(row=0, column=0, columnspan=4)
    tk.Label(ventana, textvariable=resultado_var, font=("Arial", 18), bg="lightgray", width=15).grid(row=1, column=0, columnspan=4)

    funciones = {
        "sin": "math.sin(", "cos": "math.cos(", "tan": "math.tan(",
        "√": "math.sqrt(", "^": "**", "log": "math.log10("
    }

    def insertar_funcion(func):
        entrada.set(entrada.get() + funciones[func])

    botones = [
        ('7', '8', '9', '/'), ('4', '5', '6', '*'),
        ('1', '2', '3', '-'), ('0', '.', '=', '+'),
        ('sin', 'cos', 'tan', '√'), ('^', 'log', '(', ')')
    ]

    for i, fila in enumerate(botones):
        for j, text in enumerate(fila):
            comando = lambda t=text: entrada.set(entrada.get() + t) if t not in funciones else insertar_funcion(t)
            if text == "=":
                comando = calcular
            tk.Button(ventana, text=text, font=("Arial", 14), width=5, height=2, command=comando).grid(row=i + 2, column=j)

def abrir_calculadora_grafica():
    """Calculadora para graficar funciones."""
    def graficar():
        try:
            expresion = entrada.get()
            x = np.linspace(-10, 10, 400)
            y = [eval(expresion, {"x": val, "math": math}) for val in x]

            plt.figure()
            plt.plot(x, y, label=f"y = {expresion}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Gráfica de la función")
            plt.legend()
            plt.grid()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Expresión no válida: {e}")

    ventana = tk.Toplevel(root)
    ventana.title("Calculadora Gráfica")

    tk.Label(ventana, text="Ingrese una función de x:").pack(pady=5)
    entrada = tk.StringVar()
    tk.Entry(ventana, textvariable=entrada, font=("Arial", 14), width=20).pack(pady=5)
    tk.Button(ventana, text="Graficar", font=("Arial", 14), command=graficar).pack(pady=10)

#Historial
def mostrar_historial():
    """Muestra el historial de operaciones guardadas en Firebase."""
    ventana = tk.Toplevel(root)
    ventana.title("Historial de Operaciones")
    ventana.geometry("400x300")

    historial = ref.order_by_child('timestamp').limit_to_last(10).get()
    if historial and isinstance(historial, dict):
        for key, valor in historial.items():
            tk.Label(ventana, text=f"{valor.get('operacion', '?')} = {valor.get('resultado', '?')}", font=("Arial", 12)).pack()
    else:
        tk.Label(ventana, text="No hay historial reciente disponible.", font=("Arial", 12)).pack()

#Historial
root = tk.Tk()
root.title("Calculadoras con Firebase")
root.geometry("300x400")

ttk.Button(root, text="Calculadora Básica", command=abrir_calculadora_basica).pack(pady=10)
ttk.Button(root, text="Calculadora Científica", command=abrir_calculadora_cientifica).pack(pady=10)
ttk.Button(root, text="Calculadora Gráfica", command=abrir_calculadora_grafica).pack(pady=10)
ttk.Button(root, text="Ver Historial", command=mostrar_historial).pack(pady=10)

root.mainloop()

##2

import tkinter as tk 
from tkinter import ttk 

root = tk.Tk() 
root.title("Calculadora Tkinter") 
root.geometry("400x300") 

notebook = ttk.Notebook(root) 
notebook.pack(expand=True, fill="both") 

frame_calc = tk.Frame(notebook) 
frame_conv = tk.Frame(notebook) 
frame_hist = tk.Frame(notebook) 

notebook.add(frame_calc, text="Calculadora") 
notebook.add(frame_conv, text="Conversor") 
notebook.add(frame_hist, text="Historial") 

historial = [] 

tk.Label(frame_calc, text="Número 1:").pack() 
entry1 = tk.Entry(frame_calc)
entry1.pack()

tk.Label(frame_calc, text="Número 2:").pack() 
entry2 = tk.Entry(frame_calc) 
entry2.pack() 

label_resultado = tk.Label(frame_calc, text="Resultado:") 
label_resultado.pack() 

def calcular(operacion):
    try: 
        num1, num2 = float(entry1.get()), float(entry2.get())
        resultado = eval(f"{num1} {operacion} {num2}") if operacion != "/" or num2 != 0 else "Error"
        label_resultado.config(text=f"Resultado: {resultado}") 
        historial.append(f"{num1} {operacion} {num2} = {resultado}")
    except ValueError: 
        label_resultado.config(text="Ingrese valores válidos") 
for op in ["+", "-", "*", "/"]: 
    tk.Button(frame_calc, text=op, command=lambda o=op: calcular(o)).pack(side="left", padx=5) 
tk.Label(frame_conv, text="Metros:").pack() 
entry_metros = tk.Entry(frame_conv) 
entry_metros.pack() 
label_conversion = tk.Label(frame_conv, text="0 km") 
label_conversion.pack() 
def convertir(): 
    try: 
        km = float(entry_metros.get()) / 1000 
        label_conversion.config(text=f"{km} km") 
    except ValueError: label_conversion.config(text="Ingrese un número válido") 
tk.Button(frame_conv, text="Convertir", command=convertir).pack() 
tk.Label(frame_hist, text="Historial de operaciones:").pack() 
text_historial = tk.Text(frame_hist, height=10, width=40) 
text_historial.pack() 
def actualizar_historial(): 
    text_historial.delete("1.0", tk.END) 
    text_historial.insert(tk.END, "\n".join(historial)) 
tk.Button(frame_hist, text="Actualizar", command=actualizar_historial).pack()
root.mainloop() 
