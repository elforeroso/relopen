import flet as ft
import pandas as pd
import os
import sys
import subprocess

def main(page: ft.Page):
    page.title = "Sistema Centralizado - Pronovejez"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # --- Componente para mostrar logs ---
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Resultado de la Ejecución"),
        content=ft.Text("Cargando..."),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # --- Lógica para ejecutar scripts externos ---
    def ejecutar_script(nombre_script):
        try:
            if not os.path.exists(nombre_script):
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: No se encuentra {nombre_script}"))
                page.snack_bar.open = True
                page.update()
                return

            page.snack_bar = ft.SnackBar(ft.Text(f"Ejecutando {nombre_script}... Espere por favor."))
            page.snack_bar.open = True
            page.update()

            # Ejecutamos capturando la salida (stdout y stderr)
            # text=True hace que la salida sea string en lugar de bytes
            resultado = subprocess.run(
                [sys.executable, nombre_script], 
                capture_output=True, 
                text=True,
                encoding='utf-8' # Forzamos utf-8 para evitar problemas con tildes
            )
            
            # Preparamos el mensaje de salida
            salida_texto = ""
            if resultado.stdout:
                salida_texto += f"--- SALIDA ---\n{resultado.stdout}\n"
            if resultado.stderr:
                salida_texto += f"\n--- ERRORES/AVISOS ---\n{resultado.stderr}"
            
            if not salida_texto:
                salida_texto = "El script se ejecutó correctamente pero no generó salida en consola."

            # Mostramos el resultado en el diálogo
            dlg_modal.content = ft.Column(
                [
                    ft.Text(f"Script: {nombre_script}", weight="bold"),
                    ft.Container(
                        content=ft.Text(salida_texto, font_family="Consolas", size=12),
                        bgcolor=ft.colors.GREY_100,
                        padding=10,
                        border_radius=5,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        expand=True, # Para que ocupe espacio si es grande
                    )
                ],
                height=400, # Altura fija para que aparezca scroll si es mucho texto
                width=600,
                scroll=ft.ScrollMode.AUTO
            )
            page.open(dlg_modal)
            page.update()

        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error crítico al ejecutar: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    # --- Lógica para cargar datos (Igual que antes) ---
    def obtener_vista_datos():
        archivo = "out_diabetes.csv"
        if not os.path.exists(archivo):
             return ft.Text(f"No se encontró el archivo {archivo}", color="red")

        try:
            df = pd.read_csv(archivo, encoding='latin1')
            df = df.astype(str)
            df_preview = df.head(50)

            my_columns = [ft.DataColumn(ft.Text(col)) for col in df_preview.columns]
            my_rows = []
            for row in df_preview.values:
                cells = [ft.DataCell(ft.Text(val)) for val in row]
                my_rows.append(ft.DataRow(cells=cells))

            return ft.Column(
                [
                    ft.Text(f"Vista Previa: {archivo} (Primeras 50 filas)", size=20, weight="bold"),
                    ft.Container(
                        content=ft.DataTable(
                            columns=my_columns,
                            rows=my_rows,
                            border=ft.border.all(1, "grey"),
                            vertical_lines=ft.border.BorderSide(1, "grey"),
                            horizontal_lines=ft.border.BorderSide(1, "grey"),
                        ),
                        expand=True,
                        padding=10
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        except Exception as e:
            return ft.Text(f"Error leyendo CSV: {e}", color="red")

    # --- Componentes de la UI ---
    
    # 1. Bienvenida
    container_inicio = ft.Container(
        content=ft.Column([
            ft.Icon(name=ft.Icons.HEALTH_AND_SAFETY, size=100, color="blue"),
            ft.Text("Bienvenido al Sistema de Análisis", size=30, weight="bold"),
            ft.Text("Selecciona una opción del menú lateral para comenzar.", size=16),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        expand=True
    )

    # 2. Panel de Gráficos
    container_graficos = ft.Column([
        ft.Text("Visualización de Datos", size=25, weight="bold"),
        ft.Divider(),
        ft.Row(
            spacing=20,
            run_spacing=20,
            controls=[
                ft.ElevatedButton(
                    "Mapa de Calor Diabetes", 
                    icon=ft.Icons.MAP, 
                    on_click=lambda _: ejecutar_script("graf_calor_diabetes.py"),
                    height=50
                ),
                ft.ElevatedButton(
                    "Neuropatía Diabética", 
                    icon=ft.Icons.MEDICAL_SERVICES, 
                    on_click=lambda _: ejecutar_script("neuropatia_diabetica.py"),
                    height=50
                ),
                ft.ElevatedButton(
                    "Histograma Edades", 
                    icon=ft.Icons.BAR_CHART, 
                    on_click=lambda _: ejecutar_script("graf_histo_edades.py"),
                    height=50
                ),
                ft.ElevatedButton(
                    "Gráficos Generales (SNS)", 
                    icon=ft.Icons.SHOW_CHART, 
                    on_click=lambda _: ejecutar_script("graf_sns.py"),
                    height=50
                ),
            ]
        )
    ], expand=True, scroll=ft.ScrollMode.AUTO)

    # 3. Panel de Modelos
    container_modelos = ft.Column([
        ft.Text("Modelos de Regresión Logística", size=25, weight="bold"),
        ft.Divider(),
        ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ANALYTICS),
                    title=ft.Text("Regresión Diabetes V1"),
                    subtitle=ft.Text("Ejecuta el modelo v1 de predicción"),
                    on_click=lambda _: ejecutar_script("regrelogi_diabetes v1.py")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ANALYTICS),
                    title=ft.Text("Regresión Diabetes V2"),
                    subtitle=ft.Text("Ejecuta el modelo v2 de predicción"),
                    on_click=lambda _: ejecutar_script("regrelogi_diabetes v2.py")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PSYCHOLOGY),
                    title=ft.Text("Regresión Estrés"),
                    subtitle=ft.Text("Análisis de factores de estrés"),
                    on_click=lambda _: ejecutar_script("regrelogi_estres.py")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.FAMILY_RESTROOM),
                    title=ft.Text("Dinámica Familiar"),
                    subtitle=ft.Text("Modelo sobre dinámica familiar"),
                    on_click=lambda _: ejecutar_script("regrelogi_dinafami.py")
                ),
            ]
        )
    ], expand=True)

    # --- Navegación ---
    def cambiar_tab(e):
        indice = e.control.selected_index
        contenido_principal.controls.clear()
        
        if indice == 0: # Inicio
            contenido_principal.controls.append(container_inicio)
        elif indice == 1: # Datos
            contenido_principal.controls.append(ft.ProgressBar())
            page.update()
            tabla = obtener_vista_datos()
            contenido_principal.controls.clear()
            contenido_principal.controls.append(tabla)
        elif indice == 2: # Gráficos
            contenido_principal.controls.append(container_graficos)
        elif indice == 3: # Modelos
            contenido_principal.controls.append(container_modelos)
        
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED, 
                selected_icon=ft.Icons.HOME, 
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TABLE_CHART_OUTLINED, 
                selected_icon=ft.Icons.TABLE_CHART, 
                label="Datos"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.INSERT_CHART_OUTLINED, 
                selected_icon=ft.Icons.INSERT_CHART, 
                label="Gráficos"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MODEL_TRAINING, 
                selected_icon=ft.Icons.MODEL_TRAINING, 
                label="Modelos"
            ),
        ],
        on_change=cambiar_tab,
    )

    contenido_principal = ft.Column([container_inicio], expand=True)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                contenido_principal,
            ],
            expand=True,
        )
    )

ft.app(target=main)