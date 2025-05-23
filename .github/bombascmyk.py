from machine import Pin, PWM
import utime

bombas = {
    'cian': PWM(Pin(17), freq=1000),
    'magenta': PWM(Pin(18), freq=1000),
    'amarillo': PWM(Pin(19), freq=1000),
    'negro': PWM(Pin(21), freq=1000),
    'blanco': PWM(Pin(22), freq=1000),
}

ruta_archivo = '/home/jairo/Documents/color.txt'

for bomba in bombas.values():
    bomba.duty(0)

def leer_colores(ruta=ruta_archivo):
    try:
        with open(ruta, 'r') as archivo:
            linea = archivo.readline().strip().replace(" ", "")
            partes = linea.split(',')
            if len(partes) != 5:
                raise ValueError("Se esperaban 5 componentes: C, M, Y, K, W.")
            cian = int(partes[0].split(':')[1])
            magenta = int(partes[1].split(':')[1])
            amarillo = int(partes[2].split(':')[1])
            negro = int(partes[3].split(':')[1])
            blanco = int(partes[4].split(':')[1])
            return cian, magenta, amarillo, negro, blanco
    except Exception as error:
        print("Error al leer el archivo:", error)
        return 0, 0, 0, 0, 0

def normalizar_colores(c, m, a, n, b):
    total = c + m + a + n + b
    if total == 0:
        return 0, 0, 0, 0, 0
    return c / total, m / total, a / total, n / total, b / total

try:
    cian, magenta, amarillo, negro, blanco = leer_colores()
    pc, pm, pa, pn, pb = normalizar_colores(cian, magenta, amarillo, negro, blanco)
    bombas['cian'].duty(int(pc * 1023))
    bombas['magenta'].duty(int(pm * 1023))
    bombas['amarillo'].duty(int(pa * 1023))
    bombas['negro'].duty(int(pn * 1023))
    bombas['blanco'].duty(int(pb * 1023))
    tiempo_mezcla = 6
    utime.sleep(tiempo_mezcla)

except Exception as error:
    print("Error:", error)

finally:
    for bomba in bombas.values():
        bomba.duty(0)
    print("Bombas apagadas. Mezcla finalizada.")
