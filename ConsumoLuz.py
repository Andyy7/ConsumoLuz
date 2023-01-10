from datetime import datetime, timedelta
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os
import os.path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=1040,height=720)
        self.title("Registro Consumo Luz")
        
        #Verifica que exista la base de datos, de lo contrario llama a la funcion que se ocupa de crearla.
        if os.path.isfile("registo_luz.db")==False:
            self.crear_base_datos()

        #Sección para agregar lecturas nuevas

        self.etiqueta_lectura=ttk.Label(
            self,
            text="Lectura:"
        )
        self.etiqueta_lectura.place(x=20,y=45)

        self.caja_lectura=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_numeros),"%P")
        )
        self.caja_lectura.place(x=80,y=45,width=142 ,height=20)
    
        self.etiqueta_fecha=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.etiqueta_fecha.place(x=230,y=45)

        self.caja_fecha=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_fecha),"%P")
        )
        self.caja_fecha.place(x=355,y=45,width=142 ,height=20)    

        self.boton_agregar_lectura=tk.Button(
            self,
            text="Agregar",
            command=self.agregar_lectura
        )
        self.boton_agregar_lectura.place(x=550,y=45,width=70, height=20)

        #Sección para calcular el consumo del periodo actual y el promedio de consumo por día. Se puede ver de agregar tambien un estimativo en base a las estadísticas.

        conn=sqlite3.connect(f'registo_luz.db')
        cursor=conn.cursor()
        cursor.execute(F"SELECT fecha FROM consumoLuz")
        todas_las_fechas=cursor.fetchall()
        conn.close()
        fechas=[]
        for fecha in todas_las_fechas:
            fechas.append(fecha[0])

        fecha_inicio=fechas[0]        
        fecha_fin=self.calcular_fecha_fin(fecha_inicio)
        año_fecha_int=int(fecha_fin[:4])     
        mes_fecha_str=fecha_fin[5:7]
        promedios={}

        consumos_mensuales_2=[]
        consumos_año_periodo={}
        if mes_fecha_str!="02":
            cantidad=int(int(mes_fecha_str)/2)-1
            for i in range(cantidad):
                consumos_mensuales_2.append(0)

        ######## Calculo los bimestres que se cerraron#########
        while fecha_fin in fechas:
            if mes_fecha_str=="02":
                periodo=1
            elif mes_fecha_str=="04":
                periodo=2
            elif mes_fecha_str=="06":
                periodo=3
            elif mes_fecha_str=="08":
                periodo=4
            elif mes_fecha_str=="10":
                periodo=5
            else:
                periodo=6
            

            conn=sqlite3.connect(f'registo_luz.db')
            cursor=conn.cursor()
            cursor.execute(F"SELECT fecha, lectura FROM consumoLuz WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'")
            lecturas=cursor.fetchall()
            conn.close()
            consumos=[]

            for i in range(len(lecturas)):
                
                if i<len(lecturas)-1:
                    consumo=round(lecturas[i+1][1]-lecturas[i][1],1)
                    consumos.append(consumo)

            dias=(datetime.strptime(fecha_fin, '%Y-%m-%d')-datetime.strptime(fecha_inicio, '%Y-%m-%d')).days 
            promedio=round(sum(consumos)/dias,1)
            
            if promedio!=0:          
                promedios[f'{año_fecha_int}-{periodo}']=promedio
                consumo_bimestral=round(sum(consumos))
                consumos_mensuales_2.append(consumo_bimestral)
            
            if periodo==6:
               consumos_año_periodo[f'año_{año_fecha_int}']=consumos_mensuales_2
               consumos_mensuales_2=[]

            fecha_inicio=fecha_fin          
            fecha_fin=self.calcular_fecha_fin(fecha_inicio)
            año_fecha_int=int(fecha_fin[:4])     
            mes_fecha_str=fecha_fin[5:7]

        ########### Fin del cálculo de los bimestres cerrados.

        ########### Calculo el bimestre actual.############
        if mes_fecha_str=="01" or mes_fecha_str=="02":
            periodo=1
        elif mes_fecha_str=="03" or mes_fecha_str=="04":
            periodo=2
        elif mes_fecha_str=="05" or mes_fecha_str=="06":
            periodo=3
        elif mes_fecha_str=="07" or mes_fecha_str=="08":
            periodo=4
        elif mes_fecha_str=="09" or mes_fecha_str=="10":
            periodo=5
        else:
            periodo=6        
        fecha_fin=fechas[-1]
        dias=(datetime.strptime(fecha_fin, '%Y-%m-%d')-datetime.strptime(fecha_inicio, '%Y-%m-%d')).days

        conn=sqlite3.connect(f'registo_luz.db')
        cursor=conn.cursor()
        cursor.execute(F"SELECT fecha, lectura FROM consumoLuz WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'")
        lecturas=cursor.fetchall()
        conn.close()
        consumo_actual=[]

        for i in range(len(lecturas)):
            if i<len(lecturas)-1:
                consumo=round(lecturas[i+1][1]-lecturas[i][1],1)
                consumo_actual.append(consumo)
            
        promedio_actual=round(sum(consumo_actual)/(dias+1),1)
        consumos_mensuales_2.append(round(sum(consumo_actual),1))
        

        if promedio!=0:     
            promedios[f'{año_fecha_int}-{periodo}']=promedio_actual  
            consumo_bimestral=round(sum(consumos)) 
        
        if periodo!=6:
            print(periodo)
            cantidad=6-periodo
            print(cantidad)
            for i in range(cantidad):
                consumos_mensuales_2.append(0)
        
        consumos_año_periodo[f'año_{año_fecha_int}']=consumos_mensuales_2

        ############### Fin del calculo del bimestre actual.

        self.etiqueta_consumo_actual=ttk.Label(
            self,
            text=f"El consumo actual es de {sum(consumo_actual)} kWh"
        )
        self.etiqueta_consumo_actual.place(x=20, y=120)

        self.etiqueta_promedio_actual=ttk.Label(
            self,
            text=f"El promedio actual diario es de {promedio_actual} kWh"
        )
        self.etiqueta_promedio_actual.place(x=20, y=150)
        print(consumos_año_periodo)
       #Sección para realizar el gráfico de barra del consumo bimestral. 
    
        clave=list(consumos_año_periodo.keys())

        data = pd.DataFrame(consumos_año_periodo,
                    index=('1', '2', '3', '4', '5', '6'))

        n = len(data.index)
        x = np.arange(n)+1
        width = 0.2
        f=Figure(figsize=(10,5), dpi=100)
        a=f.add_subplot()
        a.bar(x - width*(1+1/2), data.año_2020, width=width, label=clave[0][4:])
        a.bar(x - width/2, data.año_2021, width=width, label=clave[1][4:])
        a.bar(x + width/2, data.año_2022, width=width, label=clave[2][4:])
        a.bar(x + width*(1+1/2), data.año_2023, width=width, label=clave[3][4:])
        a.legend(loc='best')
        a.set_xlabel('Período')
        a.set_ylabel('Consumo en kWh')
        
        canvas=FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().place(x=20,y=200)   

        ############### FIN SECCION GRAFICO ################

 
    def calcular_fecha_fin(self,dato):
        # La fecha esta en formato str, realizo un slicing y obtengo los días que inician las lecturas, las cuales coiciden con el corte bimestral de los consumos.
        dia_fecha=dato[8:]
        mes_fecha_int=int(dato[5:7])
        año_fecha_int=int(dato[:4])
        
        if mes_fecha_int<12:
            mes_fecha_int+=2
            mes_fecha_str=str(mes_fecha_int)
            if mes_fecha_int<10:
                mes_fecha_str="0"+str(mes_fecha_int)
        else:
            mes_fecha_str="02"
            año_fecha_int+=1
        
        return f"{año_fecha_int}-{mes_fecha_str}-{dia_fecha}"

    def validar_numeros(self, texto):
        if texto=="":
            return True
        else:
            try:
                float(texto)
            except ValueError:
                return False
            return True

    def validar_fecha(self, fecha):
        if len(fecha)>10:
            return False
        chequeo=[]
        for i, letra in enumerate(fecha):
            if i in (4,7):
                chequeo.append(letra=="-")
            else:
                chequeo.append(letra.isdecimal())
        return all(chequeo)

    def verificar_vacio(self, dato):
        dato_verificar=dato
        if dato_verificar=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor es necesario ingresar un valor."
            )
            return False
        else:
            return dato_verificar

    def verificar_fecha(self,fecha):
        fecha_verificar=fecha
        try:
            datetime.strptime(fecha_verificar, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor ingrese una fecha correcta del tipo 'aaaa-mm-dd'"
            )
        else:
            return fecha_verificar

    def agregar_lectura(self):
        lectura=self.verificar_vacio(self.caja_lectura.get())
        if lectura!=False:
            fecha=self.verificar_fecha(self.caja_fecha.get())
            if fecha!=None:
                conn=sqlite3.connect(f'registo_luz.db')
                cursor=conn.cursor()
                cursor.execute("INSERT INTO consumoLuz VALUES (?, ?)", (fecha, lectura))
                conn.commit()
                conn.close() 

                self.caja_fecha.delete(0,tk.END)
                self.caja_lectura.delete(0,tk.END)               

    def crear_base_datos(self):
        conn=sqlite3.connect(f'registo_luz.db')
        cursor=conn.cursor()

        try:
            cursor.execute("CREATE TABLE consumoLuz (fecha DATE, lectura FLOAT)")
        except sqlite3.OperationalError:
            # silenciar la excepción
            pass
        conn.close()

ventana_principal=VentanaPrincipal()
ventana_principal.mainloop()