# Proyecto Final - Sistema de navegación del campus universitario

# Descripcion 
Este es un proyecto final para Matematicas Discretas. Este proyecto proporciona un sistema de navegación para el campus universitario, utilizando el algoritmo de Dijkstra para calcular las rutas más cortas entre las ubicaciones del campus. Visualiza el mapa del campus y las rutas entre las ubicaciones, lo que permite a los usuarios navegar fácilmente por el campus. Se incluirá una interfaz visual que muestre el mapa del campus con las rutas generadas, donde los nodos representan ubicaciones, los pesos las distancias y los bordes las trayectorias.

## Características

- **Cálculo de la ruta más corta**: utiliza el algoritmo de Dijkstra para calcular la ruta más corta entre dos ubicaciones especificadas por el usuario.
- **Ruta alternativa**: proporciona una ruta más corta alternativa excluyendo ciertos nodos a lo largo de la primera ruta.
- **Mapa interactivo**: muestra el mapa del campus con marcadores para cada ubicación y las rutas calculadas. Las rutas se muestran en azul y rojo para la primera ruta y las rutas alternativas, respectivamente.
- **Cálculo de distancia**: muestra las distancias entre las ubicaciones en la ruta y calcula la distancia total de ambas rutas.

## Requisitos

- Python 3.x
- `folium` para mapeo y visualizaciones
- `geopy` para calcular distancias geográficas
- `heapq` para implementar la cola de prioridad en el algoritmo de Dijkstra

Puede instalar las bibliotecas necesarias usando:

```bash
pip install folium geopy

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/melll-13/proyectofinal.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd proyectofinal
    ```

3. Instala las dependencias (si es necesario):
    ```bash
    npm install
    ```

## Uso
1. Ejecutar el script en python:
    ```bash
    python udlapApp.py
    ```
2. Ingresar ubicaciones:
     El script pedirá que ingreses la ubicación de inicio y la ubicación de destino. Asegúrate de que las ubicaciones que ingreses sean parte de las ubicaciones predefinidas en el código.Navega al directorio del proyecto:

3. Ver resultados:
   - Después de calcular las rutas más cortas, el script:
   - Muestra las distancias entre las ubicaciones de la ruta.
   - Calcula la distancia total de ambas rutas.
   - Genera y guarda un mapa interactivo (udlap_paths_combined.html) que muestra ambas rutas y los marcadores de ubicación.