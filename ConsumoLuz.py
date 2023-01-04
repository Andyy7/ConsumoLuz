from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox








class NuevoConsumo(tk.Toplevel):
    en_uso=False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=800,height=800)
        self.title("Nuevo Consumo")


        self.boton_cerrar=tk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.boton_cerrar.place(x=210,y=270)
        self.__class__.en_uso=True

        self.etiqueta_lectura=ttk.Label(
            self,
            text="Lectura:"
        )
        self.caja_lectura=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_numeros),"%P")
        )
        self.caja_lectura.place(x=150,y=70,width=142 ,height=20)

    # def validar_numeros(self, texto):
    #     return texto.isdigit()

    def validar_numeros(self, texto):
            if texto=="":
                return True
            else:
                try:
                    float(texto)
                except ValueError:
                    return False
                return True

    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=800,height=300)
        self.title("Registro Consumo Luz")
        
        self.boton_nuevo_consumo=ttk.Button(
            self,
            text="Nuevo Consumo",
            command=self.abrir_nuevo_consumo
            )
        self.boton_nuevo_consumo.place(x=270,y=45,width=110, height=25)

    def abrir_nuevo_consumo(self):
        if not NuevoConsumo.en_uso:
            self.nuevo_consumo=NuevoConsumo()

ventana_principal=VentanaPrincipal()
ventana_principal.mainloop()