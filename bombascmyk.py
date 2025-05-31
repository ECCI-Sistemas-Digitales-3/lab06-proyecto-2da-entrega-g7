import RPi.GPIO as GPIO
import time

# Pines asignados a cada color
pin_map = {
    'cian': 17,
    'magenta': 18,
    'amarillo': 19,
    'negro': 21,
    'blanco': 22,
}

GPIO.setmode(GPIO.BCM)
bombas = {}
frecuencia = 1000

for color, pin in pin_map.items():
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, frecuencia)
    pwm.start(0)
    bombas[color] = pwm

ruta_archivo = '/home/jairo/Documents/color.txt'

def leer_rgb(ruta=ruta_archivo):
    try:
        with open(ruta, 'r') as archivo:
            linea = archivo.readline().strip().replace(" ", "")
            partes = linea.split(',')
            if len(partes) != 3:
                raise ValueError("Se esperaban 3 componentes: R, G, B.")
            r = int(partes[0].split(':')[1])
            g = int(partes[1].split(':')[1])
            b = int(partes[2].split(':')[1])
            return r, g, b
    except Exception as error:
        print("Error al leer el archivo:", error)
        return 0, 0, 0

def rgb_a_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r_, g_, b_)
    c = (1 - r_ - k) / (1 - k) if (1 - k) != 0 else 0
    m = (1 - g_ - k) / (1 - k) if (1 - k) != 0 else 0
    y = (1 - b_ - k) / (1 - k) if (1 - k) != 0 else 0
    return c, m, y, k

def calcular_blanco(r, g, b):
    r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
    blanco = min(r_, g_, b_)  # Lo que se puede simular como blanco puro
    return blanco

try:
    r, g, b = leer_rgb()
    c, m, y, k = rgb_a_cmyk(r, g, b)
    w = calcular_blanco(r, g, b)

    # Normalizar todos los valores entre 0-100 para duty cycle
    bombas['cian'].ChangeDutyCycle(c * 100)
    bombas['magenta'].ChangeDutyCycle(m * 100)
    bombas['amarillo'].ChangeDutyCycle(y * 100)
    bombas['negro'].ChangeDutyCycle(k * 100)
    bombas['blanco'].ChangeDutyCycle(w * 100)

    print(f"RGB({r}, {g}, {b}) → CMYK({c:.2f}, {m:.2f}, {y:.2f}, {k:.2f}) + W({w:.2f})")
    time.sleep(6)

except Exception as error:
    print("Error:", error)

finally:
    for pwm in bombas.values():
        pwm.ChangeDutyCycle(0)
        pwm.stop()
    GPIO.cleanup()
    print("Bombas apagadas. Mezcla finalizada.")


