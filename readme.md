## Introducción

Este proyecto proporciona una solución de bajo costo para el seguimiento del movimiento de la pupila utilizando una cámara web estándar. El objetivo principal es controlar el cursor del ordenador mediante la detección de la dirección de la mirada del usuario, lo que puede ser particularmente útil para personas con limitaciones motoras severas. El sistema utiliza Python y varias bibliotecas de procesamiento de imágenes y visión por computadora para lograr la detección precisa de la pupila y su movimiento.

## Configuración del Proyecto

### Requisitos

Para ejecutar este proyecto, necesitarás lo siguiente:

- Python 3.10.11
- Cámara web
- Bibliotecas de Python: `opencv-python`, `cvzone`, `mediapipe`, `PyAutoGUI`, `numpy`, `pandas`, `scipy`
- IDE de tu elección, recomendamos Visual Studio Code

### Instalación

Clona el repositorio de GitHub:

```bash
git clone https://github.com/sergiosant02/TFG-pupil-detection.git
cd TFG-pupil-detection
```

Instala las dependencias necesarias:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements
```

### Ejecución del Proyecto

Para iniciar el proyecto, simplemente ejecuta el script principal desde la línea de comando:

```bash
python main.py
```

### Si aparece el error ImportError: No module named 'Tkinter'

He observado que en ciertas distribuciones de Linux Tkinter no esta presente, para instalarlo:

```bash
sudo apt-get install python3-tk
```

## Calibración del Sistema

Antes de comenzar a usar el sistema para controlar el cursor del ratón, es crucial realizar un proceso de calibración. Este proceso asegura que el sistema pueda interpretar correctamente hacia dónde está mirando el usuario basándose en la posición de la pupila.

### Pasos para la Calibración

1. Asegúrate de que estás en un entorno bien iluminado y que la cámara web está correctamente posicionada.
2. Abre el software y selecciona la opción de calibración desde el menú principal.
3. Se te pedirá que mires hacia varios puntos en la pantalla, aparecen inicialmnete 9 puntos. Debes ir mirando uno a uno y mientras miras cada uno pulsar "enter".
4. Repite el una segiunda vez, tras realizar dos vueltas, estará calibrado por completo. Es importante ir de izquierda a derecha, de arriba a abajo

## Uso del Proyecto para Mover el Ratón

Una vez calibrado el sistema, puedes comenzar a usarlo para mover el cursor del ratón con los movimientos de tu ojo derecho, para ello el izquierdo debe permanecer cerrado.

### Cómo Funciona

- El sistema rastrea el centro de tu pupila y calcula la dirección de tu mirada.
- Un algoritmo interpreta estos datos para mover el cursor del ratón en la pantalla de tu ordenador.
- Para hacer clic, realiza un parpadeo prolongado del ojo derecho durante menos de un segundo, el izquierdo debe permancecer abierto.

## Consideraciones Finales

- El rendimiento del sistema puede variar dependiendo de la iluminación, la calidad de la cámara web y otros factores ambientales.
- Es posible que necesites realizar calibraciones frecuentes para mantener la precisión del sistema.
