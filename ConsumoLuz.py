from datetime import datetime, timedelta
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os
import os.path


class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=800,height=300)
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
        # self.boton_agregar_lectura=tk.Button(
        #     self,
        #     text="Mostrar",
        #     command=self.mostrar
        # )
        # self.boton_agregar_lectura.place(x=550,y=70,width=70, height=20)
        conn=sqlite3.connect(f'registo_luz.db')
        cursor=conn.cursor()
        cursor.execute(F"SELECT fecha FROM consumoLuz")
        todas_las_fechas=cursor.fetchall()
        conn.close()
        fechas=[]
        for fecha in todas_las_fechas:
            fechas.append(fecha[0])

        fecha_inicio=fechas[0]
        fecha_fin=(datetime.strptime(fecha_inicio, '%Y-%m-%d')+ timedelta(61)).strftime('%Y-%m-%d')
        x=0
        promedios=[]
        while fecha_fin in fechas:


            conn=sqlite3.connect(f'registo_luz.db')
            cursor=conn.cursor()
            cursor.execute(F"SELECT fecha, lectura FROM consumoLuz WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'")
            lecturas=cursor.fetchall()
            conn.close()
            consumos=[]
            # print("############")
            # print(fecha_inicio)
            # print(fecha_fin)
            for i in range(len(lecturas)):
                
                if i<len(lecturas)-1:
                    consumo=round(lecturas[i+1][1]-lecturas[i][1],1)
                    consumos.append(consumo)
            
            # print(consumos)
                
            promedio=round(sum(consumos)/61,1)
            if promedio!=0:          
                promedios.append(promedio)
            
            fecha_inicio=fecha_fin
            fecha_fin=(datetime.strptime(fecha_fin, '%Y-%m-%d')+ timedelta(61)).strftime('%Y-%m-%d')
        
        # print(promedios)

        print(fecha_inicio)
        fecha_fin=fechas[-1]
        print(fecha_fin)
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
        
        print(consumo_actual)
            
        promedio_actual=round(sum(consumo_actual)/(dias+1),1)

        if promedio!=0:          
            promedios.append(promedio_actual)        

        print(promedio_actual)
        
        #Sección para calcular lo consumido por periodo mensual.

        #Sección para realizar el gráfico de barra del consumo mensual o bimestral.


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