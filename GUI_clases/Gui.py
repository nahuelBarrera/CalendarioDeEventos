import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
import Vistas

class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent,padding=(10))
        self.__parent = parent # referencia a la ventana ppal
        parent.title("Calendario de Eventos")
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.geometry("1100x420+60+60") 
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)
        self.cargarMenuLateral()
        self.cargarComponentes()
        
    def cargarComponentes(self):
        self.__rightFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__cargarVistaSemanal()
        self.__rightFrame.grid(column=1,row=0,padx=5,pady=5)

    def cargarMenuLateral(self):
        self.__menuFrame = ttk.Labelframe(self,text="Menu",padding=5,borderwidth=2, relief="groove")
        self.__btnModif = ttk.Button(self.__menuFrame,text="Modificar Evento",width=15,command=self.__nuevoEvento,padding=5,state='disabled')
        self.__btnModif.grid(column=0,row=4,padx=5,pady=5)
        self.__btnVistaSem = ttk.Button(self.__menuFrame,text="Vista Semanal",width=15,command=self.__cargarVistaSemanal,padding=5)
        self.__btnVistaSem.grid(column=0,row=0,padx=5,pady=5)
        self.__btnVistaMen = ttk.Button(self.__menuFrame,text="Vista Mensual",width=15,command=self.__cargarVistaMensual,padding=5)
        self.__btnVistaMen.grid(column=0,row=1,padx=5,pady=5)
        ttk.Button(self.__menuFrame,text="Nuevo Evento",command=self.__nuevoEvento,padding=5,width=15,).grid(column=0,row=2,pady=5,padx=5)
        self.__btnBuscar = ttk.Button(self.__menuFrame,text="Buscar Evento",width=15,command=self.__buscar,padding=5)
        self.__btnBuscar.grid(column=0,row=3,padx=5,pady=5)
        self.__btnElim = ttk.Button(self.__menuFrame,text="Eliminar Evento",width=15,command=self.__eliminar,padding=5,state='disabled')
        self.__btnElim.grid(column=0,row=5,padx=5,pady=5)
        self.__menuFrame.grid(column=0,row=0,padx=5,pady=5,sticky=tk.N)
       
    def __cargarVistaSemanal(self):
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        Vistas.VistaSemanal(self.__rightFrame)
        self.__rightFrame.grid(column=1,row=0,padx=5,pady=5)
        self.__btnVistaSem['state'] = 'disabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state']='enabled'

    def __cargarVistaMensual(self):
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        Vistas.VistaMensual(self.__rightFrame)
        self.__rightFrame.grid(column=1,row=0,padx=5,pady=5)
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'disabled'

    def __nuevoEvento(self):
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        #self.calFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        Vistas.NuevoEventoVista(self.__rightFrame,self).grid()
        #self.calFrame.grid(column=2,row=0)
        self.__rightFrame.grid(column=1,row=0,rowspan=2,padx=5,pady=5)
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'disabled'
        
    def __buscar(self):
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        Vistas.FiltroDeEventos(self.__rightFrame)
        self.__rightFrame.grid(column=1,row=0,padx=5,pady=5)
        self.__btnBuscar['state'] = 'disabled'

    def __eliminar(self):
        pass
    
    # def slicing(self,iterable,nro):
    #     lista = list(iterable)
    #     result = []
    #     if nro == 1:
    #         result.extend(iterable[:7])
    #     elif nro == 2:
    #         result.extend(iterable[7:14])
    #     elif nro == 3:
    #         result.extend(iterable[14:21])
    #     else:
    #         result.extend(iterable[21:])
    #     return result

    # def generarListaDeSemanas(self,iterable):
    #     listaSemanas = []
    #     ini = 0; fin = 7
    #     for i in range(6):
    #         if len(iterable[ini:fin]) != 0:
    #             listaSemanas.append(iterable[ini:fin])
    #             ini += 7; fin += 7
    #     return listaSemanas
    

root = tk.Tk()
App(root).grid()
root.mainloop()