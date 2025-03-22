import openpyxl
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class SistemaRestaurante:
    def __init__(self, archivo="pedidos.xlsx"):
        # Verificar si el archivo existe, si no, crearlo con la estructura inicial
        if not os.path.exists(archivo):
            self.crear_archivo_inicial(archivo)
        self.archivo = archivo
        self.workbook = openpyxl.load_workbook(archivo)
        self.sheet_pedidos = self.workbook["Pedidos"]
        self.sheet_menu = self.workbook["Menu"]

    def crear_archivo_inicial(self, archivo):
        # Crear un nuevo libro de trabajo y hojas
        wb = openpyxl.Workbook()
        
        # Hoja de pedidos
        sheet_pedidos = wb.active
        sheet_pedidos.title = "Pedidos"
        headers_pedidos = ["Mesa", "Fecha", "Hora Pedido", "Platos", "Total"]
        sheet_pedidos.append(headers_pedidos)
        
        # Hoja de menú
        sheet_menu = wb.create_sheet("Menu")
        headers_menu = ["Plato", "Precio"]
        sheet_menu.append(headers_menu)
        
        # Agregar algunos platos de ejemplo
        platos_ejemplo = [
            ("Pizza Margherita", 10.0),
            ("Hamburguesa", 8.5),
            ("Ensalada César", 6.0)
        ]
        for plato, precio in platos_ejemplo:
            sheet_menu.append([plato, precio])
        
        # Guardar el archivo
        wb.save(archivo)

    def registrar_pedido(self):
        # Cargar el menú desde la hoja "Menu"
        menu = {}
        for row in self.sheet_menu.iter_rows(min_row=2, values_only=True):
            plato, precio = row
            menu[plato] = precio
        
        # Mostrar el menú
        print("Menú disponible:")
        for i, (plato, precio) in enumerate(menu.items(), 1):
            print(f"{i}. {plato} - ${precio}")
        
        # Solicitar número de mesa
        mesa = input("Ingrese el número de mesa: ").strip()
        
        # Seleccionar platos
        platos_seleccionados = []
        while True:
            seleccion = input("Ingrese el número del plato (0 para terminar): ")
            if seleccion == "0":
                break
            try:
                num = int(seleccion)
                if 1 <= num <= len(menu):
                    plato = list(menu.keys())[num - 1]
                    platos_seleccionados.append(plato)
                else:
                    print("Número inválido.")
            except ValueError:
                print("Por favor, ingrese un número.")
        
        if not platos_seleccionados:
            print("No se seleccionaron platos.")
            return
        
        # Calcular total
        total = sum(menu[plato] for plato in platos_seleccionados)
        
        # Registrar en la hoja "Pedidos"
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_pedido = datetime.now().strftime("%H:%M:%S")
        platos_str = ", ".join(platos_seleccionados)
        self.sheet_pedidos.append([mesa, fecha, hora_pedido, platos_str, total])
        self.workbook.save(self.archivo)
        print(f"Pedido registrado para mesa {mesa}. Total: ${total:.2f}")

    