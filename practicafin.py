import tkinter as tk
from tkinter import messagebox
import serial
import threading

# Configuración inicial
fuente = "Consolas 11 bold"
arduino = None
puerto_arduino = "COM8"
baudrate = 9600

# Función para conectar con Arduino y manejar errores
def conectar():
    global arduino
    try:
        arduino = serial.Serial(puerto_arduino, baudrate)
        etiqueta_estado.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Estado de la conexión", "Conexión establecida")
    except:
        etiqueta_estado.config(text="Estado: No conectado", fg="red")
        messagebox.showerror("Advertencia", "No se pudo conectar con el dispositivo Arduino. ¡Revisa los puertos!")

# Función para desconectar Arduino
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        etiqueta_estado.config(text="Estado: No conectado", fg="red")
        messagebox.showinfo("Conexión", "Conexión terminada")
    else:
        messagebox.showwarning("Advertencia", "No hay ninguna conexión activa")

# Función para enviar un límite de temperatura a Arduino
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = entrada_limite.get()
            if limite.isdigit():  # Verifica que sea un número
                arduino.write(f"{limite}\n".encode())
                messagebox.showinfo("Enviado", f"El límite de temperatura ({limite} grados) ha sido enviado")
                arduino.flush()
            else:
                messagebox.showerror("Error", "Introduce un valor numérico para el límite")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el límite: {e}")
    else:
        messagebox.showwarning("Advertencia", "No hay una conexión activa")

# Función para leer datos desde Arduino
def leer_desde_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            datos = arduino.readline().decode().strip()
            if datos:
                temperatura = datos.split(":")[1].strip()
                etiqueta_temperatura.config(text=f"Temperatura: {temperatura} °C")
        except Exception as e:
            print(f"Error al leer datos: {e}")
            break

# Iniciar un hilo para la lectura de datos
def iniciar_lectura():
    global hilo
    hilo = threading.Thread(target=leer_desde_arduino)
    hilo.daemon = True
    hilo.start()

# Configuración de la interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Interfaz para monitoreo de temperatura")
ventana.geometry("400x300")

# Etiqueta de temperatura actual
etiqueta_principal = tk.Label(ventana, text="Temperatura actual", font=(fuente, 13))
etiqueta_principal.pack(pady=10)

etiqueta_temperatura = tk.Label(ventana, text="-- °C", font=(fuente, 20))
etiqueta_temperatura.pack(pady=5)

# Etiqueta de estado de conexión
etiqueta_estado = tk.Label(ventana, text="Estado: No conectado", fg="red", font=(fuente, 13))
etiqueta_estado.pack(pady=5)

# Entrada para el límite de temperatura
entrada_limite = tk.Entry(ventana)
entrada_limite.pack(pady=5)
entrada_limite.config(width=10)

# Botón para enviar el límite
boton_enviar = tk.Button(ventana, text="Enviar límite", command=enviar_limite, font=(fuente, 13))
boton_enviar.pack(pady=5)

# Botón para conectar
boton_conectar = tk.Button(ventana, text="Conectar", command=conectar, font=(fuente, 13))
boton_conectar.pack(pady=5)

# Botón para desconectar
boton_desconectar = tk.Button(ventana, text="Desconectar", command=desconectar, font=(fuente, 13))
boton_desconectar.pack(pady=5)

# Iniciar la interfaz gráfica
ventana.mainloop()
