# mapreduce-counting-triangles-in-graph-


Algorithmo utilizado: http://islab.kaist.ac.kr/chungcw/InterConfPapers/km0805-ha-myung.pdf

Existen 4 archivos .py, le explico que hace cada uno:


# start.py

Creamos este archivo para realizar todos los comando en un solo proceso(nos tomaba mucho tiempo realizar cada comando de hadoop, borrar carpeta output, copiar grafo, etc).
Solo debe asegurarse de tener el grafo(archivo .txt) y los archivos .py en el mismo directorio.

El comando es:

python start.py nombre_archivo_grafo.txt numero_particiones nombre_usuario_en_cluster

Ejemplo:

python start.py ca-HepTh.txt 4 cchacon

Y listo, esto ejecutará todos los comandos, también se encarga de borrar archivos y carpeta cada vez que se ejecuta(para que no tengan que borrar la carpeta output cada vez que quieran usar el mapreduce). 

# pre_processing.py

Este archivo asigna 2 nuevas columnas al archivo del grafo(.txt), que son el número de partición de cada vértice. Aumenta el tamaño del archivo pero disminuye el cómputo.


 Y para terminar el:
# mapper.py, reducer.py

Estos archivos realizan los algoritmos de los 2 papers.


Un grafo de ejemplo:
http://snap.stanford.edu/data/ca-HepTh.txt.gz



Además para el conteo final usamos un comando en AWK y creamos un archivo tarea.json(cuando termine de ejecutar el start.py) que nos da el total de triángulos y otra información extra del grafo.
