from datetime import datetime as dt

class Evento:

    def __init__(self, titulo="", fechaYHora=dt.now(), descripcion="", importancia=None):
        self.__titulo = titulo
        self.__fechaYHora = fechaYHora
        self.__descripcion = descripcion
        self.__importancia = importancia
        self.__etiquetas = None

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, valor):
        self.__titulo = valor

    @property
    def fechaYHora(self):
        return self.__fechaYHora

    @fechaYHora.setter
    def fechaYHora(self, nuevo=dt.now()):
        self.__fechaYHora = nuevo

    @property
    def descripcion(self):
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, nuevo):
        self.__descripcion = nuevo

    @property
    def importancia(self):
        return self.__importancia

    @importancia.setter
    def importancia(self, nuevo):
        self.__importancia = nuevo

    @property
    def etiquetas(self):
        return self.__etiquetas

    @etiquetas.setter
    def etiquetas(self, nuevo):
        self.__etiquetas = nuevo

    def fechaFormateada(self):
        return self.__fechaYHora.strftime('%d/%m/%Y')

    def horaFormateada(self):
        return self.__fechaYHora.strftime('%H:%M')

    def mostrarRecordatorio(self):
        pass

    def agregarEtiquetas(self, etiquetas=enumerate):
        self.__etiquetas = etiquetas

