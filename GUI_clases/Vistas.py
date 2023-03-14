import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END
from datetime import datetime
from calendar import Calendar 
from tkcalendar import Calendar as tkCalendar
class Calendario(Calendar):

    def __init__(self):
        super().__init__(firstweekday=6)
        self.__strMesLargo = ('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
        self.__strMesCorto = ('Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic')
        self.__strDiaLargo = ('Lúnes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
        self.__strDiaCorto = ('Lu','Ma','Mi','Ju','Vi','Sa','Do')

    def nombreDelMes(self, mes, tipo=0):
        if tipo == 0:
            cad = self.__strMesCorto[mes-1]
        else:
            cad = self.__strMesLargo[mes-1]
        return cad
    
    def nombreDelDia(self, dia, tipo=0):
        if tipo == 0:
            cad = self.__strDiaCorto[dia-1]
        else:
            cad = self.__strDiaLargo[dia-1]
        return cad
    
    def matrizMensual(self, anio, mes):
        """Retorna una matriz con los días del mes y año pasados por parámetro. Cada fila de la matriz
        representa una semana, cuyos días son valores enteros y los días fuera del mes se representan con un 0."""
        return self.monthdatescalendar(anio, mes)

    def listaDeSemanas(self, anio, mes):
        """"Retorna una lista cuyos elementos son listas de valores del tipo datetime.date(), las cuales
        representan cada semana del mes. La primer y ultima lista puede contener los ultimos días del mes
        anterior y/o los primeros días posterior que se incluyen en la primer y ultima semana respectivamente."""
        iterableDias = list(self.itermonthdates(anio,mes))
        listaSemanas = []
        ini = 0; fin = 7
        for i in range(6): 
            if len(iterableDias[ini:fin]) != 0:
                listaSemanas.append(iterableDias[ini:fin])
                ini += 7; fin += 7
        return listaSemanas
    
    pass

class VistaSemanal(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent, padding=(5))
        self.__parent = parent
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1) 
        self.__cal = Calendario()
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__semanaActual = None

        self.__cargarComponentes()
        
    def __cargarComponentes(self):
        ttk.Button(self,text="Anterior",command=self.__retroceder).grid(column=0,row=0,pady=5,padx=5)
        ttk.Button(self,text="Siguiente",command=self.__avanzar).grid(column=2,row=0,pady=5,padx=5)
        
        self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
        
        for week in self.__semanas:
            if self.__fechaActualDT.date() in week:
                self.__semanaActual = self.__semanas.index(week)
                break

        self.__lblMes = ttk.Label(self,text=self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual),font='Helvetica 12 bold',padding=5)
        self.__lblMes.grid(column=1,row=0,columnspan=1,pady=5)
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)

    def __mostrarSemana(self,semana):
        weekFrame = ttk.Frame(self)
        # for col,dia in enumerate():
        #     ttk.Label(weekFrame,text=dia,padding=5,borderwidth=2, relief="solid").grid(column=col,row=1,pady=5,padx=5)
        for col, dia in enumerate(semana):
            eventFrame = ttk.Frame(weekFrame,borderwidth=2,relief="solid")
            lblDia = ttk.Label(eventFrame,text=self.__cal.nombreDelDia(col,1)+'  '+dia.strftime('%d/%m'),font='Helvetica 12 bold',padding=5)
            lblDia.grid(column=0,row=0,pady=5,padx=0)
            if col == 0:
                lblDia['foreground'] = 'red'
            if col == 6:
                lblDia['foreground'] = 'blue'
            if dia == self.__fechaActualDT.date():
                lblDia['background'] = 'yellow'
            eventFrame.grid(column=col,row=1,pady=5,padx=0)
            ttk.Label(eventFrame,text="SIN EVENTOS",padding=5,font='Helvetica 12',background='white').grid(column=0,row=1,pady=5,padx=0)
        return weekFrame

    def __retroceder(self):
        self.__frameWeek.destroy()
        if self.__semanaActual-1 < 0:
            if self.__mesActual-1 < 1:
                self.__anioActual -= 1
                self.__mesActual = 12
            else:
                self.__mesActual -= 1
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = len(self.__semanas)-2
        else:
            self.__semanaActual -= 1
        self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)
        
    def __avanzar(self):
        self.__frameWeek.destroy()
        if self.__semanaActual+1 >= len(self.__semanas)-1:
            if self.__mesActual+1 > 12:
                self.__anioActual += 1
                self.__mesActual = 1
            else:
                self.__mesActual += 1
            self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = 0
        else:
            self.__semanaActual += 1
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)
    
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

# root = tk.Tk()
# VistaSemanal(root,2023,3,1).grid(column=0,row=1,columnspan=2,pady=5,padx=5)
# root.mainloop()

class VistaMensual(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent, padding=(20))
        self.__parent = parent
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        
        self.__cal = Calendario()
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)

        self.__cargarComponentes()

    def __cargarComponentes(self):
        ttk.Button(self,text="Anterior",command=self.__anterior).grid(column=0,row=0,pady=5,padx=(5,0),)
        ttk.Button(self,text="Siguiente",command=self.__siguiente).grid(column=2,row=0,pady=5,padx=(0,5))
        self.__lblNombreMes = ttk.Label(self,text=self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual),font='Helvetica 12 bold',padding=5,borderwidth=2,relief="sunken")
        self.__lblNombreMes.grid(column=1,row=0,columnspan=1,padx=0,pady=5)
        self.__mesFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=5,padx=5)

    def __mostrarMes(self,frame, mes):
        monthFrame = ttk.Frame(frame)
        
        #dates = self.monthdatescalendar(year, month)

        self.labels = []
        dias = []
        for m in range(7):
            labelDay = ttk.Label(monthFrame,text=self.__cal.nombreDelDia(m),font='Helvetica 12 bold',padding=5,borderwidth=2,relief='solid')
            labelDay.grid(column=m,row=0)
            dias.append(labelDay)
        self.labels.append(dias)
        for week in self.__mes:
            labels_row = []
            for c, date in enumerate(week):
                txt = str(date.day)
                if date.day < 10:
                    txt = ' '+txt+' '
                
                label = ttk.Label(monthFrame,text=txt,font='Helvetica 12 bold',padding=5,background='white',borderwidth=2,relief='solid')
                label.grid(row=self.__mes.index(week)+1, column=c)
                
                if date.month != mes:
                    label['background'] = '#aaa'
                if c == 6:
                    label['foreground'] = 'blue'
                if c == 0:
                    label['foreground'] = 'red'
                if date == self.__fechaActualDT.date():
                    label['background'] = 'yellow'
        
                labels_row.append(label)
            self.labels.append(labels_row)

        return monthFrame

    def __anterior(self):
        self.__mesFrame.destroy()
        if self.__mesActual-1 < 1:
            self.__anioActual -= 1
            self.__mesActual = 12
        else:
            self.__mesActual -= 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=5,padx=5)
    
    def __siguiente(self):
        self.__mesFrame.destroy()
        if self.__mesActual+1 > 12:
            self.__anioActual += 1
            self.__mesActual = 1
        else:
            self.__mesActual += 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=5,padx=5)
       
class FiltroDeEventos(ttk.Frame):

    def __init__(self,parent):
        super().__init__(parent, padding=(5))
        #self.__parent = parent
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__inputTitulo = tk.StringVar()
        self.__inputEtiqueta = tk.StringVar()
        self.__checkValueTitulo = tk.StringVar()
        self.__checkValueEtiqueta = tk.StringVar()

        self.__cargarComponentes()
        # self.__frameResultados = ttk.Frame(self,padding=5,borderwidth=2,relief='sunken')
        # ttk.Label(self.__frameResultados,text="LABEL DE PRUEBA").grid(column=0,row=0)
        # self.__frameResultados.grid(column=0,row=0)

    def __cargarComponentes(self):

        ttk.Checkbutton(self,text="Filtrar por Título:",padding=5,command=self.__filtrarPorTitulo,variable=self.__checkValueTitulo).grid(column=0,row=0,columnspan=1,sticky=tk.W)
        ttk.Checkbutton(self,text="Filtrar por Etiquetas:",padding=5,command=self.__filtrarPorEtiqueta,variable=self.__checkValueEtiqueta).grid(column=0,row=1,columnspan=1,sticky=tk.W)
        self.__inputTit = ttk.Entry(self,width=30,textvariable=self.__inputTitulo,state='disabled')
        self.__inputTit.grid(column=1,row=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
        self.__inputTag = ttk.Entry(self,width=30,textvariable=self.__inputEtiqueta,state='disabled')
        self.__inputTag.grid(column=1,row=1,columnspan=1,padx=5,pady=5,sticky=tk.W)
        self.__btnBuscar = ttk.Button(self,text='Buscar',command=self.__buscar)
        self.__btnBuscar.grid(column=0,row=2,columnspan=3,pady=5,padx=5)
        
        self.__frameResultados = ttk.Labelframe(self,text='Resultados',padding=5,borderwidth=2,relief='sunken')
        
        columnas = ('fe','ho','ti','im','et')
        self.__trvwResultados = ttk.Treeview(self.__frameResultados,columns=columnas,show='headings')
       
        self.__trvwResultados.column('fe',width=55,anchor=tk.CENTER)
        self.__trvwResultados.column('ho',width=50,anchor=tk.CENTER)
        self.__trvwResultados.column('ti',width=200,anchor=tk.CENTER)
        self.__trvwResultados.column('im',width=80,anchor=tk.CENTER)
        self.__trvwResultados.column('et',width=300,anchor=tk.CENTER)

        self.__trvwResultados.heading("fe",text="Fecha",anchor=tk.CENTER)
        self.__trvwResultados.heading("ho",text="Hora",anchor=tk.CENTER)
        self.__trvwResultados.heading("ti",text="Título",anchor=tk.CENTER)
        self.__trvwResultados.heading("im",text="Importancia",anchor=tk.CENTER)
        self.__trvwResultados.heading("et",text="Etiquetas",anchor=tk.CENTER)

        #Para insertar elementos:
        self.__trvwResultados.insert('',tk.END,values=('13/03/2023','9:00','Examen de Ingles','Importante', 'teste, examen, prueba, ingles, estudiar'))
        
        self.__sclBar = ttk.Scrollbar(self.__frameResultados,orient=tk.VERTICAL,command=self.__trvwResultados.yview)
        self.__sclBar.grid(column=1,row=0,sticky=tk.NS)
        self.__trvwResultados.configure(yscroll=self.__sclBar.set)
        self.__trvwResultados.grid(column=0,row=0)
        self.__frameResultados.grid(column=0,row=3,columnspan=3)
    
    def __buscar(self, archivo):
        pass

    def __filtrarPorTitulo(self):
        self.__inputTit['state'] = 'enabled'
        pass

    def __filtrarPorEtiqueta(self):
        self.__inputTag['state'] = 'enabled'
        pass

class CalendarException(TypeError):
    def __init__(self, message, *args):         
        super(CalendarException, self).__init__(message, *args)

class NuevoEventoVista(ttk.Frame):

    def __init__(self, parent, parenFrame):
        
        super().__init__(parent,padding=(20))
        self.__parent = parent
        self.__parentFrame = parenFrame
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        #parent.resizable(False, False)
        self.__tamTag = 0
        self.__rowTag = 0
        self.__columnTag = -1
        self.__listaEtiquetas = []

        self.__titulo = tk.StringVar()
        self.__descripcion = tk.StringVar()
        self.__importancia = tk.StringVar()
        self.__fecha = tk.StringVar()
        self.__fechaRecor = tk.StringVar()
        self.__duracion = tk.StringVar()
        self.__hHora = tk.StringVar()
        self.__mHora = tk.StringVar()
        self.__hRecor = tk.StringVar()
        self.__mRecor = tk.StringVar()
        self.__etiqueta = tk.StringVar()
        self.__checkValue = tk.StringVar()

        self.__cargarComponentes()
        
    def __cargarComponentes(self):
        self.__mainBlock = ttk.Frame(self)
        self.__mainBlock.grid_columnconfigure(0, weight=1)
        self.__block1 = ttk.Frame(self.__mainBlock,padding=10)
        self.__block1.grid_columnconfigure(0, weight=1)
        self.__block2 = ttk.Frame(self.__mainBlock,padding=10)
        self.__block2.grid_columnconfigure(0, weight=1)

        #TITULO
        ttk.Label(self.__block1,text="Título: ",justify='left',width=6).grid(column=0,row=0,columnspan=1,sticky=(tk.W),pady=5)
        self.__inputTit = ttk.Entry(self.__block1,width=35,textvariable=self.__titulo,justify='right')
        self.__inputTit.grid(column=1,row=0,columnspan=1,sticky=(tk.W),pady=5)
        
        #DESCRIPCIÓN
        ttk.Label(self.__block1,text="Descripción:",justify='left').grid(column=0,row=1,columnspan=3,sticky=(tk.W),pady=5)
        self.__inputDesc = tk.Text(self.__block1, height=10, width=40)
        self.__inputDesc.grid(column=0,row=2,columnspan=2,sticky=(tk.E),pady=5)
        
        #IMPORTANCIA
        ttk.Label(self.__block1,text="Importancia:",justify='left').grid(column=0,row=4,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputImp = ttk.Combobox(self.__block1,textvariable=self.__importancia,values=['Importante','Normal'],justify='center')
        self.__inputImp.config(state='readonly',width=12)
        self.__inputImp.grid(column=1,row=4,columnspan=1,sticky=(tk.E),pady=5)
        
        #ETIQUETAS
        self.__tagFrame = ttk.Labelframe(self.__block1,text="Tags",borderwidth=6,relief='sunken')
        self.__tagFrame.grid(column=0,row=6,columnspan=2)
        self.__btnAddTag = ttk.Button(self.__block1,text="Agregar Etiqueta:",command=self.__agregarEtiqueta)
        self.__btnAddTag.grid(column=0,row=5,columnspan=1,sticky=(tk.W),pady=5)
        self.__inputTag = ttk.Entry(self.__block1,width=35,textvariable=self.__etiqueta,justify='right')        
        self.__inputTag.grid(column=1,row=5,columnspan=1,sticky=(tk.E),pady=5)
        
 #_______________________________________________________________________________________________________________________________________________________________       
        
        #FECHA
        ttk.Label(self.__block2,text="Fecha:",justify='left',textvariable=self.__fecha).grid(column=0,row=0,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputFecha = ttk.Entry(self.__block2)
        self.__inputFecha.config(justify='center',width=15)
        self.__inputFecha.grid(column=1,row=0,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputFecha.insert(0,datetime.today().strftime('%d/%m/%y'))
        self.__inputFecha.bind("<ButtonPress-1>", self.__seleccionarFechaEvento)

        #HORA
        hora=ttk.Label(self.__block2,text="Hora:",justify="left")
        hora.grid(column=0,row=1,columnspan=1,sticky=(tk.E),pady=5)

        self.__inputHora = ttk.Labelframe(self.__block2)
        diezHoras = list(map(lambda x:'0'+str(x),range(10)))
        self.__horas = diezHoras.copy()
        self.__horas.extend(map(lambda x:str(x),range(10,24)))
        self.__min = diezHoras
        self.__min.extend(map(lambda x:str(x),range(10,60)))
        comboHora = ttk.Combobox(self.__inputHora, textvariable=self.__hHora,values=self.__horas,width=3,state='readonly',justify='right')
        comboHora.set(datetime.now().strftime('%H'))
        comboHora.grid(column=0,row=0,columnspan=1,sticky=(tk.N))
        comboMin = ttk.Combobox(self.__inputHora, textvariable=self.__mHora,values=self.__min,width=3,state='readonly',justify='right')
        comboMin.set(datetime.now().strftime('%M'))
        comboMin.grid(column=2,row=0,columnspan=1,sticky=(tk.N))
        self.__inputHora.grid(column=1,row=1,sticky=(tk.E),pady=0)
        ttk.Label(self.__inputHora,text=":",font=('Arial',14),justify='left').grid(column=1,row=0,columnspan=1,sticky=(tk.N),padx=2)

        #DURACIÓN
        ttk.Label(self.__block2,text="Duración:",justify='left').grid(column=0,row=2,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputDura = ttk.Combobox(self.__block2,textvariable=self.__duracion,values=['1 hora','3 horas','6 horas','8 horas','12 horas','Todo el día'],justify='center')
        self.__inputDura.set("1 hora")
        self.__inputDura.config(state='readonly',width=12)
        self.__inputDura.grid(column=1,row=2,columnspan=1,sticky=(tk.E),pady=5)

        #AGREGAR RECORDATORIO
        canvas= tk.Canvas(self.__block2, width= 50, height= 50)
        canvas.grid(column=0,row=3,columnspan=1,sticky=(tk.E),pady=5)
        #Load an image in the script
        img= (Image.open("GUI_clases\\bell.png"))
        #Resize the Image using resize method
        resized_image= img.resize((30,30), Image.LANCZOS)
        new_image= ImageTk.PhotoImage(resized_image)
        #Add image to the Canvas Items
        canvas.create_image(10,10, anchor=tk.NW, image=new_image)
        canvas.image = new_image

        self.__recorChBx = ttk.Checkbutton(self.__block2,text="Recordatorio",command=self.__agregarRecor,variable=self.__checkValue)
        self.__recorChBx.grid(column=1,row=3,columnspan=1,sticky=(tk.W),pady=5,padx=(5,0))
        self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")

        #BOTONES ACEPTAR Y CANCELAR
        btnFrame = ttk.Labelframe(self.__block2)
        btnFrame.grid(column=1,row=5,pady=5,columnspan=2,sticky=tk.E,)
        btnAceptar = ttk.Button(btnFrame,text="Aceptar",command=self.__enviarEvento)
        btnAceptar.grid(column=0,row=0,padx=(0,3))
        btnCancelar = ttk.Button(btnFrame,text="Cancelar",command=self.__parent.destroy)
        btnCancelar.grid(column=1,row=0,padx=(3,0))

        self.__block1.grid(column=0,row=0,rowspan=2)
        separator = ttk.Separator(self, orient='vertical',)
        separator.grid(column=1,row=0,rowspan=2, padx=5,sticky=tk.EW)
        self.__block2.grid(column=2,row=0,rowspan=2)
        self.__mainBlock.grid(column=0,row=0)

    def __agregarRecor(self):
        if self.__checkValue.get() == '1':
            #FECHA
            ttk.Label(self.__inputRecor,text="Fecha:",justify='left').grid(column=0,row=0,columnspan=1,sticky=(tk.E),pady=5,padx=(0,5))
            self.__inputFechaRecor = ttk.Entry(self.__inputRecor,textvariable=self.__fechaRecor)
            self.__inputFechaRecor.config(justify='center',width=15)
            self.__inputFechaRecor.grid(column=1,row=0,columnspan=1,sticky=(tk.W),pady=5)
            self.__inputFechaRecor.insert(0,datetime.today().strftime('%d/%m/%y'))
            self.__inputFechaRecor.bind("<ButtonPress-1>", self.__seleccionarFechaRecor)
            #HORA
            ttk.Label(self.__inputRecor,text="Hora:",justify="left").grid(column=0,row=1,columnspan=1,sticky=(tk.E),pady=5,padx=(0,5))
            self.__inputHoraRecor = ttk.Labelframe(self.__inputRecor)
            comboRecorHora = ttk.Combobox(self.__inputHoraRecor, textvariable=self.__hRecor,values=self.__horas,width=3,state='readonly',justify='right')
            comboRecorHora.set(datetime.now().strftime('%H'))
            comboRecorHora.grid(column=0,row=0,columnspan=1,sticky=(tk.N))
            comboRecorMin = ttk.Combobox(self.__inputHoraRecor, textvariable=self.__mRecor,values=self.__min,width=3,state='readonly',justify='right')
            comboRecorMin.set(datetime.now().strftime('%M'))
            comboRecorMin.grid(column=2,row=0,columnspan=1,sticky=(tk.N))
            ttk.Label(self.__inputHoraRecor,text=":",font=('Arial',14),justify='left').grid(column=1,row=0,columnspan=1,sticky=(tk.N),padx=2)
            self.__inputHoraRecor.grid(column=1,row=1,sticky=(tk.E),pady=0)
            self.__inputRecor.grid(column=1,row=4,sticky=(tk.E),pady=0)
        else:
            self.__cerrarCal()
            self.__inputRecor.destroy()
            self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")

    
    
    def __seleccionarFechaRecor(self,event):
       self.__desplegarCalendarioSeleccionable(self.__obtenerFechaRecor)

    def __seleccionarFechaEvento(self,event):
        self.__desplegarCalendarioSeleccionable(self.__obtenerFechaEvento)
    
    def __desplegarCalendarioSeleccionable(self,tipo):
        self.__ventanaCal = tkCalendar(self.__mainBlock, selectmode="day", date_pattern="dd/mm/y")
        self.__ventanaCal.grid(column=3,row=0,columnspan=2,padx=5,pady=5,sticky=tk.S)
        self.__btnSel = ttk.Button(self.__mainBlock, text="Seleccionar", command=tipo)
        self.__btnSel.grid(column=3,row=1,pady=5,padx=5,sticky=tk.NE)
        self.__btnCan = ttk.Button(self.__mainBlock, text="Cerrar", command=self.__cerrarCal)
        self.__btnCan.grid(column=4,row=1,pady=5,padx=5,sticky=tk.NW)
    
    def __cerrarCal(self):
        self.__ventanaCal.destroy()
        self.__btnSel.destroy()
        self.__btnCan.destroy()

    def __obtenerFechaRecor(self):
        self.__inputFechaRecor.delete(0,tk.END)
        self.__inputFechaRecor.insert(0, self.__ventanaCal.get_date())
        self.__cerrarCal()
       
    def __obtenerFechaEvento(self):
        self.__inputFecha.delete(0,END)
        self.__inputFecha.insert(0, self.__ventanaCal.get_date())
        self.__cerrarCal()    
    

    def __enviarEvento(self):
        datos = {
                 'titulo':self.__titulo.get(),
                 'descripcion':self.__descripcion.get(),
                 'importancia':self.__importancia.get(),
                 'fecha':self.__fecha.get(),
                 'hora':self.__hora.get(),
                 'duracion':self.__duracion.get()
                 }
        return datos
    
    def __agregarEtiqueta(self):

        deleteTag = lambda tag: self.__listaEtiquetas.remove(tag)
        
        def modificar1(self):
            tagLabel['relief']='raised'
        def modificar2(self):
            tagLabel['relief']='ridge'
        def eliminar(self):
            deleteTag(tagLabel["text"])
            tagLabel.destroy()

        if self.__etiqueta != "":
            if self.__etiqueta.get() not in self.__listaEtiquetas:
                self.__listaEtiquetas.append(self.__etiqueta.get())
                tagLabel = ttk.Label(self.__tagFrame,text=self.__etiqueta.get(),relief='ridge',padding=3)
                tagLabel.bind("<Enter>",modificar1)
                tagLabel.bind("<Leave>",modificar2)
                tagLabel.bind("<ButtonPress-1>",eliminar)
                if self.__tamTag+tagLabel.winfo_reqwidth() < 270:
                    self.__columnTag += 1
                    self.__tamTag += tagLabel.winfo_reqwidth()
                else:
                    self.__tamTag = 0
                    self.__columnTag = 0
                    self.__rowTag += 1
                tagLabel.grid(column=self.__columnTag,row=self.__rowTag,pady=5,padx=5)
                if len(self.__tagFrame.winfo_children()) >= 5:    #Deshabilita el botón si se llegó al máximo de 5 etiquetas
                    self.__btnAddTag.state(['disabled'])
            self.__inputTag.delete(0,END)
        else:
            raise CalendarException("La etiqueta no puede ser vacía.")
    
    

# root = tk.Tk()
# NuevoEventoVista(root,"Agregar Evento").grid()
# root.mainloop()