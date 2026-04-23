import pandas as pd
import os
import flet as ft

def main(page: ft.Page):
    # 1. Cargar el DataFrame
    try:
        carpeta = os.getcwd()
        os.chdir(carpeta)
        archivo = "Resultados.csv"
        df = pd.read_csv(archivo, encoding='latin1')
        df = df.astype(str) 
    except FileNotFoundError:
        page.add(ft.Text("Error: No se encontró el archivo Excel."))
        return

    # 2. Crear las Columnas dinámicamente
    # Usamos comprensión de listas para generar las cabeceras
    my_columns = [
        ft.DataColumn(ft.Text(col_name)) 
        for col_name in df.columns
    ]

    # 3. Crear las Filas dinámicamente
    # Iteramos sobre los valores del dataframe para crear las celdas
    my_rows = []
    for row in df.values:
        # Creamos una lista de celdas para esta fila
        cells = [ft.DataCell(ft.Text(value)) for value in row]
        my_rows.append(ft.DataRow(cells=cells))

    # 4. Ensamblar el DataTable
    # Es importante meterlo en un Row/Column con scroll, o la tabla se cortará
    datatable = ft.DataTable(
        columns=my_columns,
        rows=my_rows,
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.BorderSide(1, "grey"),
        horizontal_lines=ft.border.BorderSide(1, "grey"),
    )

    # Agregamos scroll para poder ver tablas grandes
    page.add(
        ft.Column(
            [datatable],
            scroll=ft.ScrollMode.ADAPTIVE, 
            expand=True
        )
    )

ft.app(target=main)