import RPi.GPIO as GPIO
import time
import os

# Pines de control para las bombas (Rojo, Verde, Azul)
BOMBAS = {
    'rojo': (17, 27),
    'verde': (23, 24),
    'azul': (5, 6)
}

# Ruta del archivo con los valores RGB deseados
RUTA_COLOR = '/home/jairo/Documents/color.txt'

# Inicializacion de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin1, pin2 in BOMBAS.values():
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)

def activar_bomba(pin1, pin2, tiempo):
    print(f"Activando bomba: pin1={pin1}, pin2={pin2}, tiempo={tiempo:.2f}s")
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(tiempo)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)

def obtener_rgb(ruta=RUTA_COLOR):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()

        if len(lineas) == 1:
            # Formato tipo "R: 151, G: 104, B: 131"
            linea = lineas[0].strip().replace(" ", "")
            partes = linea.split(',')
            r = int(partes[0].split(':')[1])
            g = int(partes[1].split(':')[1])
            b = int(partes[2].split(':')[1])
        elif len(lineas) >= 3:
            # Formato tradicional: una linea por color
            r = int(lineas[0].strip())
            g = int(lineas[1].strip())
            b = int(lineas[2].strip())
        else:
            raise ValueError("El archivo debe tener 1 o al menos 3 lineas para representar R, G y B.")
        
    return r, g, b

def normalizar_rgb(r, g, b):
    total = r + g + b
    if total == 0:
        return 0, 0, 0
    return r / total, g / total, b / total

try:
    r, g, b = obtener_rgb()
    print(f"Color deseado: R={r}, G={g}, B={b}")

    nr, ng, nb = normalizar_rgb(r, g, b)
    print(f"Proporciones normalizadas: R={nr:.2f}, G={ng:.2f}, B={nb:.2f}")

    # Tiempo total de mezcla (ajustable segun volumen de pintura)
    tiempo_total = 6  # segundos

    if nr > 0:
        print("? Activando bomba ROJA")
        activar_bomba(*BOMBAS['rojo'], tiempo_total * nr)
    if ng > 0:
        print("? Activando bomba VERDE")
        activar_bomba(*BOMBAS['verde'], tiempo_total * ng)
    if nb > 0:
        print("? Activando bomba AZUL")
        activar_bomba(*BOMBAS['azul'], tiempo_total * nb)

except Exception as e:
    print(f"?? Error: {e}")

finally:
    GPIO.cleanup()
    print("GPIO limpio. Proceso finalizado.")

