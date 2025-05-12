[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19473344&assignment_repo_type=AssignmentRepo)
# Lab06: Proyecto 2da. entrega

## Integrantes
Roland Lara 
Jairo Casallas
Nicolas Cuartas
## Documentación
## Conexión de la bomba con el módulo L298N

A continuación se muestra el diagrama de conexión entre la Raspberry Pi Pico y el módulo puente H L298N, que controla dos motores (o bombas):

![Diagrama de conexión](C:\Users\jairo\github-classroom\ECCI-Sistemas-Digitales-3\lab06-proyecto-2da-entrega-g7\Puente_H_raspberry.png)

> ⚠️ **Importante:**  
> El módulo L298N **no activa las salidas hacia las bombas** si no se aplica voltaje en **ambas entradas de alimentación**:  
> - **+12V** (alimentación principal para los motores)  
> - **5V o 12V en el pin de `VCC` interno**, dependiendo de si se está usando o no el jumper de regulación.  
>
> Asegúrate de:
> - Aplicar el voltaje de motor en el pin `+12V`.
> - Proporcionar tierra común (`GND`) entre la fuente, la Raspberry Pi y el L298N.
> - Verificar que el jumper de 5V esté bien colocado si usas el regulador interno del módulo.