import csv
def cargarArchivo(ruta,arch):
    encabezado=("TITULO","FECHA","HORA","DESCRIPCION","IMPORTANCIA","ETIQUETA")

    with open (ruta, "a+", newline="") as archivo:
        escritor=csv.DictWriter(archivo, fieldnames=encabezado)
        escritor.writeheader()
        for i in arch:
            escritor.writerow(i)

def leerArchivo(ruta):
    encabezado=("TITULO","FECHA","HORA","DESCRIPCION","IMPORTANCIA","ETIQUETA")

    with open(ruta, "r", newline="") as archivo:
        lista=list(csv.DictReader(archivo, fieldnames=encabezado, delimiter=","))
    return lista

