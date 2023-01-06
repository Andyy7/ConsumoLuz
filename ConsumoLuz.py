from datetime import datetime
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


    def agregar_lectura(self):
        fecha=self.verificar_vacio(self.caja_fecha.get())
        if fecha==True:
            lectura=self.verificar_vacio(self.caja_lectura.get())
            if lectura==True:
                conn=sqlite3.connect(f'registo_luz.db')
                cursor=conn.cursor()
                cursor.execute("INSERT INTO consumoLuz VALUES (?, ?)", (fecha, lectura))
                conn.commit()
                conn.close()                

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