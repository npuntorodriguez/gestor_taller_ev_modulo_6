import tkinter as tk
import time
import threading
import winsound

# --- 1. Mapeo de Colores y Frecuencias (Hz) ---
COLORES_FRECUENCIAS = {
    "Azul": 261,     # Do
    "Verde": 293,    # Re
    "Amarillo": 329, # Mi
    "Naranja": 349,  # Fa
    "Rojo": 392,     # Sol
    "Morado": 440,   # La
    "Celeste": 493,  # Si
    "Plomo": 277     # Do# o sostenido ejemplo
}

# --- 2. Colores Tkinter ---
COLORES_RGB = {
    "Azul": "#0000FF",
    "Verde": "#00FF00",
    "Amarillo": "#FFFF00",
    "Naranja": "#FFA500",
    "Rojo": "#FF0000",
    "Morado": "#800080",
    "Celeste": "#00BFFF",
    "Plomo": "#A0A0A0",
}

# --- 3. Partitura simplificada (tu canción original) ---
# Cada nota: color, duración en ms
PARTITURA = [
    {"color": "Azul", "dur": 500},     # Do
    {"color": "Verde", "dur": 500},    # Re
    {"color": "Amarillo", "dur": 500}, # Mi
    {"color": "Naranja", "dur": 500},  # Fa
    {"color": "Rojo", "dur": 500},     # Sol
    {"color": "Morado", "dur": 500},   # La
    {"color": "Celeste", "dur": 500},  # Si
    {"color": "Azul", "dur": 500},     # Do alta
    {"color": "Plomo", "dur": 500},    # Sostenido ejemplo
]

# --- 4. Configuración ventana ---
ANCHO = 800
ALTO = 400
ALTURA_NOTA = 40
FPS = 60

class Nota:
    def __init__(self, color, dur, x):
        self.color = color
        self.dur = dur
        self.x = x
        self.y = -ALTURA_NOTA
        self.rect = None

def tocar_nota(color, dur):
    freq = COLORES_FRECUENCIAS.get(color, 440)
    winsound.Beep(freq, dur)

def animar():
    global notas_vivas
    while True:
        for nota in notas_vivas:
            nota.y += 2
        dibujar()
        root.update()
        time.sleep(1/FPS)

def dibujar():
    canvas.delete("all")
    for nota in notas_vivas:
        canvas.create_rectangle(nota.x, nota.y, nota.x+60, nota.y+ALTURA_NOTA, fill=COLORES_RGB[nota.color], outline="black")

def reproducir_partitura():
    global notas_vivas
    x_pos = 50
    for nota_data in PARTITURA:
        color = nota_data["color"]
        dur = nota_data["dur"]
        nota = Nota(color, dur, x_pos)
        notas_vivas.append(nota)
        # Reproducir sonido en hilo separado
        threading.Thread(target=tocar_nota, args=(color, dur), daemon=True).start()
        time.sleep(dur/1000)  # Espera a la siguiente nota
        x_pos += 70
    # Limpieza al final
    time.sleep(1)
    notas_vivas.clear()

# --- 5. Inicializar Tkinter ---
root = tk.Tk()
root.title("Mini Piano Demo")
canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="black")
canvas.pack()

notas_vivas = []

# --- 6. Hilo de animación ---
threading.Thread(target=animar, daemon=True).start()

# --- 7. Hilo de reproducción de la partitura ---
threading.Thread(target=reproducir_partitura, daemon=True).start()

root.mainloop()
