from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os
import os.path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from base64 import b64decode

icono_chico_datos="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADr0AAA69AUf7kK0AAAI6SURBVDhPfZJNaBNBFMffbJakbrJJGk3jNmHX3cav4NfBYz2kFhs8tFfx4MGDhV4riCdPHkTw7MWDiKLgoVAqIlbBY6QIoi1KSEyItTWNSWzTxG12pjvTSdm1oT+Ynfm/L968WdgPPaBfMALGMJc9EfjOUENqvy5p17kETLBoEUvkEgy/elGX9WNcMlwFSo1Szd5iqqQqVLeb7azZNLP0rIAiEUCZwnrhO9VdEP0kA8lobiNXYRYAD/3ofj3t85I0PZsmfpdvlt4nIOErQ7lFbYPy4MHl9eUqK2C3NkIImiAYPSBtspo6S57fnOpMnEhimH3jAZ8P4MWMZyb32XsF9+EYEaxpQMJsoVl4ywpwPElIioeOmHdfPjKn44cJM9b/IprMijx8LN7/WbTu2F1s2a4O9TtnYMUhbo2PWTe6yZRwkMDktQ78riAYS1uTzmSKa4j5A/kBLQEyly7On8MgIAjaA45yE8NVQG7Ja79WgQ3pf0aGLQj4YTO6GV3jJoarwCIsmq/mhSf1hnM0O1DbnO1bgAV6hV3Ykznx4IEPS99IZvySpSBeB2OAqdveT0s56Wq1VTV3rPugSVom+1Qh5GuMrY/PFGJI2mXudrG3Vxujz1BH01tfjg5h5s/lBfJ6XjhT/Ff8wQIc7LkCJSJGgr5I6lStfby8UtdKlXqoUF35M1fr1Bo8ZJeeHWghLSx0hHsIEYNq+y/NYxHfKjaKdRbgwPUKXWhgMBwMnTydGqUrFJb7eyUDAGwDiJrU0NO+Hg8AAAAASUVORK5CYII="
icono_grande_datos="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADr0AAA69AUf7kK0AAASoSURBVFhHpZdtbBRFGMefmbtr73avb1EEyt3tvdHW0xRNAU2t1ITwoYkSTGMiRCPV+lZFCQYMiR/84AejEROiUUNiPxgsfABfwIYrsVaFxpcaBA562vaud1ypoFBqb+/au90dZ3tDw8nd3m75JZOd5z8zO88+8+zsLNwKHl54zcsL25m5KDC7LpZqQgurLwpNBwROuNfNu19lpmE8vKeRlg3MLIimAxZsSQAhu32cq4lJ/4cQgmgQbkYAwUpbDyCkVDCpIJoOjCZH/wZAuxSE97VCq5nJC2BQDhJMDjIzD8zDm9S/UCQZO8ykxUOTLejm3E8xsySCXWjw8O6Lfrt/CZNujcCSgH05LOeYeR2Tw+ZY4bQ5a9V6TsrhAIfNV+nzM1MTxK5QZ6+7fY7M3R0TYwNMKgT22D3tRFGeRQg9WFlBrKr47wxK03D/CHSposnoISoVzAsVX4WrOYthOD4dn1LtBQfUsCEFHaXVGCb49Ug6MpRryeG3+R0SyvYE6khL5xMSPNSsQE1Vbp6pawgGBjHs22+G8J/oBzORt4ykExPzjQz6Rt2DEbxNqw0KgrZYMjas6gtJSIUwl+IC9Mm+UJB8lK75G6wJvFavS8bZwe3PyS1ffzYHj7bJ85Mf+NIMd7bY4MmXy2DyEoKejzKwrVNeJ2HTSZ/V52TDwcMJu+mT9tFq0CRa6q9PrrIQgRupv62+QhKl6rHZsQvUNLl5YXBnl7S2a6uU63ADKRr8c39g+PywGX79HcPH72Rg4CSGPZ9YfoqK4y20i+wsd/osnOWfyFRkOjfKAB7O9cxjzS6ihJYSck679O6tJWucAon1LSPt97sIDftWdpuilNyKCcIvvNQhASoYq3za1svQ8bgEb+2xQFduzIusqSiaDriqXDWcjTQ9sFZmSmme3izB0BkMfo8CtnJY7a3xVrGmgmhvxVnwCg6CzDftgcUpLwdYs0qBUBiDawXB8pzsYU0F0XRAISZsztti9HFXgwKq0/MFiOYdNB2QkZyYmET0m8IEnbzSKcGGdTJM/EXHIrP6JhVF04F4Kj559RqMqOE0ytlhDNPTKBwRI5eZVJCSd6bJ3/1pj4EkYKhjaOC6mVmUkg6U2awffHUMx/tP6E8Gte+RoGk8nUp/yKSilLzrlfSVTJWp+udvT5g239ekWGqXaifE0GkMz+8sS2Yz+OGElBhnclF0bC851KPVsjuUY/2HZrGVvmqFmJ0DWN9uJRcvobbx1HiQyZrozq6oGD0+eRn19g0UD9rx701A+wT1Tq5iKL0RoOAvp4oPUT9GChDdk6sYcgCIHI1dwHB1ChUssQQGeqaIsN660J0DKvSMsIp+YHpptZjjCibKxrFU/Ddml8SQAwEIlImcuIUeWiqZlAc9o8/wKX7/eTifYVJJjEWAd29b2bByb+PqRqbkc2boNIyGR3ZExdj7TCqJMQfs7lb6G/INjQDPpDxoBESahI/Qg+13TCqJIQdU1CO3xW7qIArK++NBmMxkk3J3AhL0kKYfww7Qn5QddYH69xqb8pchdCoEw2fDu+ge8C6TdGHYAXUZ6EHhCF2GvAioCYgR2RQR4/1M0gHAf/9Vtp77nCX7AAAAAElFTkSuQmCC"
class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=1040,height=670)
        self.title("Registro Consumo Luz")
        icono_chico=tk.PhotoImage(data=b64decode(icono_chico_datos))
        icono_grande=tk.PhotoImage(data=b64decode(icono_grande_datos))
        self.iconphoto(True,icono_grande,icono_chico)
        
        #Verifica que exista la base de datos, de lo contrario llama a la funcion que se ocupa de crearla.
        if os.path.isfile("Registro_luz.db")==False:
            self.crear_base_datos()

        #Sección para agregar lecturas nuevas

        self.etiqueta_lectura=ttk.Label(
            self,
            text="Lectura:"
        )
        self.etiqueta_lectura.place(x=20,y=20)

        self.caja_lectura=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_numeros),"%P")
        )
        self.caja_lectura.place(x=80,y=20,width=142 ,height=20)
    
        self.etiqueta_fecha=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.etiqueta_fecha.place(x=230,y=20)

        self.caja_fecha=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_fecha),"%P")
        )
        self.caja_fecha.place(x=355,y=20,width=142 ,height=20)    
        
        self.boton_agregar_lectura=tk.Button(
            self,
            text="Agregar",
            command=self.agregar_lectura
        )
        self.boton_agregar_lectura.place(x=520,y=20,width=70, height=20)

        consumo_actual=self.calcular_bimestres()[0]
        promedio_actual=self.calcular_bimestres()[1]

        registros=self.consultar_bd(f"fecha, lectura FROM consumoLuz")
        ultima_lectura=registros[-1][1]
        ultima_fecha=registros[-1][0]
        
        self.etiqueta_ultima_lectura=ttk.Label(
            self,
            text=f"La última lectura registrada es {ultima_lectura} con fecha del {ultima_fecha}."
        )
        self.etiqueta_ultima_lectura.place(x=20, y=55)

        self.etiqueta_consumo_actual=ttk.Label(
            self,
            text=f"El consumo actual es de {consumo_actual} kWh."
        )
        self.etiqueta_consumo_actual.place(x=20, y=80)

        self.etiqueta_promedio_actual=ttk.Label(
            self,
            text=f"El promedio actual es de {promedio_actual} kWh."
        )
        self.etiqueta_promedio_actual.place(x=20, y=105)

    def graficar(self,consumos_año_periodo):
        claves=list(consumos_año_periodo.keys())

        n = 6       # Cantidad de bimestres
        x = np.arange(n)+1
        width = 0.2
        f=Figure(figsize=(10,5), dpi=100)
        a=f.add_subplot()
        a.bar(x - width*(1+1/2), consumos_año_periodo[claves[-4]], width=width, label=claves[-4])
        a.bar(x - width/2, consumos_año_periodo[claves[-3]], width=width, label=claves[-3])
        a.bar(x + width/2, consumos_año_periodo[claves[-2]], width=width, label=claves[-2])
        a.bar(x + width*(1+1/2), consumos_año_periodo[claves[-1]], width=width, label=claves[-1])
        a.legend(loc='best')
        a.set_xlabel('Período')
        a.set_ylabel('Consumo en kWh')
        
        canvas=FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().place(x=20,y=150)   

    def calcular_bimestres(self):
        consulta="fecha FROM consumoLuz"
        todas_las_fechas=self.consultar_bd(consulta)
        fechas=[]
        for fecha in todas_las_fechas:
            fechas.append(fecha[0])

        fecha_inicio=fechas[0]        
        fecha_fin=self.calcular_fecha_fin(fecha_inicio)
        año_fecha_int=int(fecha_fin[:4])     
        mes_fecha_str=fecha_fin[5:7]
        promedios={}

        consumos_bimestrales=[]
        consumos_año_periodo={}
        if mes_fecha_str!="02":
            cantidad=int(int(mes_fecha_str)/2)-1
            for i in range(cantidad):
                consumos_bimestrales.append(0)

        ######## Inicio de la sección para calcular el consumo de los bimestres  cerrados o finalizados #########
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
            
            consulta=f"fecha, lectura FROM consumoLuz WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
            lecturas=self.consultar_bd(consulta)
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
                consumos_bimestrales.append(consumo_bimestral)
            
            if periodo==6:
               consumos_año_periodo[f'{año_fecha_int}']=consumos_bimestrales
               consumos_bimestrales=[]

            fecha_inicio=fecha_fin          
            fecha_fin=self.calcular_fecha_fin(fecha_inicio)
            año_fecha_int=int(fecha_fin[:4])     
            mes_fecha_str=fecha_fin[5:7]
        ######## Fin de la sección para calcular el consumo de los bimestres  cerrados o finalizados#########

        ######## Inicio de la sección para calcular el consumo del bimestre actual #########
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

        consulta=f"fecha, lectura FROM consumoLuz WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
        lecturas=self.consultar_bd(consulta)

        consumo_actual=[]

        for i in range(len(lecturas)):
            if i<len(lecturas)-1:
                consumo=round(lecturas[i+1][1]-lecturas[i][1],1)
                consumo_actual.append(consumo)
            
        promedio_actual=round(sum(consumo_actual)/(dias+1),1)
        consumos_bimestrales.append(round(sum(consumo_actual)))

        if promedio!=0:     
            promedios[f'{año_fecha_int}-{periodo}']=promedio_actual 
            consumo_bimestral_actual=round(sum(consumo_actual)) 
        
        if periodo!=6:
            cantidad=6-periodo
            for i in range(cantidad):
                consumos_bimestrales.append(0)

        consumos_año_periodo[f'{año_fecha_int}']=consumos_bimestrales
        self.graficar(consumos_año_periodo)
        datos=[consumo_bimestral_actual,promedio_actual]
        return datos

    def consultar_bd(self,consulta):
        conn=sqlite3.connect(f'Registro_luz.db')
        cursor=conn.cursor()
        cursor.execute(F"SELECT {consulta}")
        salida=cursor.fetchall()
        conn.close()
        return salida
 
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

    def validar_sucesion_lectura(self,dato):
        # Se realiza una prueba para saber si la lectura cumple con la sucesión de lecturas anteriores.
        registros=self.consultar_bd(f"fecha, lectura FROM consumoLuz")
        ultima_lectura=float(registros[-1][1])

        if ultima_lectura>=float(dato):
            messagebox.showwarning(
                title="Advertencia",
                message="Ingreso de lectura no válido. Se esta ingresando un valor inferior a la última lectura registrada."
            )
            return False
        else:
            return dato

    def validar_sucesion_fecha(self,dato):
        # Se realiza una prueba para saber si la fecha cumple con la sucesión de fechas anteriores.
        registros=self.consultar_bd(f"fecha, lectura FROM consumoLuz")
        ultima_fecha=datetime.strptime(registros[-1][0], '%Y-%m-%d')
        dato=datetime.strptime(dato, '%Y-%m-%d')

        if ultima_fecha>=dato:
            messagebox.showwarning(
                title="Advertencia",
                message="Ingreso de fecha no válido. Se esta ingresando una fecha inferior a la última registrada."
            )
            return False
        else:
            dato=dato.date()
            return dato
        
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

    def agregar_lectura(self,*args):
        lectura=self.verificar_vacio(self.caja_lectura.get())
        if lectura!=False:
            lectura=self.validar_sucesion_lectura(lectura)
            if lectura!=False:
                fecha=self.verificar_fecha(self.caja_fecha.get())
                if fecha!=None:
                    fecha=self.validar_sucesion_fecha(fecha)
                    if fecha!=False:
                        conn=sqlite3.connect(f'Registro_luz.db')
                        cursor=conn.cursor()
                        cursor.execute("INSERT INTO consumoLuz VALUES (?, ?)", (fecha, lectura))
                        conn.commit()
                        conn.close() 

                        self.caja_fecha.delete(0,tk.END)
                        self.caja_lectura.delete(0,tk.END)     

                        consumo_actual=self.calcular_bimestres()[0]
                        promedio_actual=self.calcular_bimestres()[1]
                
                        self.etiqueta_ultima_lectura.config(
                            text=f"La última lectura registrada es {lectura} con fecha del {fecha}."
                        )
                        self.etiqueta_consumo_actual.config(
                            text=f"El consumo actual es de {consumo_actual} kWh."
                        )
                        self.etiqueta_promedio_actual.config(
                            text=f"El promedio actual es de {promedio_actual} kWh."
                        )

    def crear_base_datos(self):
        conn=sqlite3.connect(f'Registro_luz.db')
        cursor=conn.cursor()

        try:
            cursor.execute("CREATE TABLE consumoLuz (fecha DATE, lectura FLOAT)")
        except sqlite3.OperationalError:
            # silenciar la excepción
            pass
        conn.close()

ventana_principal=VentanaPrincipal()
ventana_principal.mainloop()