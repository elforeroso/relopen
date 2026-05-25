import os
import leer_datos
import analisis_neuropatia_diabetica
import analisis_estres
import analisis_dinafamiliar
import regrelogi_diabetes_v2
import regrelogi_estres
import regrelogi_dinafami

def mostrar_menu():
    print("\n" + "*"*40)
    print("               MENÚ RELOPEN")
    print("         Modelo de Regresion Logica")
    print("           Pronostico de la Vejez ")
    print("*"*40)
    print("1. Cargar y Preprocesar Datos")
    print("")
    print("2. Analisis Datos Neuropatía Diabética")
    print("3. Analisis Datos Estrés")
    print("4. Analisis Datos Dinámica Familiar")
    print("")
    print("5. Regresión Logistica Neuropatía Diabética")
    print("6. Regresión Logistica Estrés")
    print("7. Regresión Logistica Dinámica Familiar")
    print("0. Salir")
    print("*"*40)

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-7): ")

        if opcion == "1":
            print("\n>>> Ejecutando lectura de datos...")
            df = leer_datos.leer_csv()
            # df_trabajo = crear_df_trabajo(df)
            # # df_trabajo_sinpuntos = crear_df_trabajo_sinpuntos(df)
 
        elif opcion == "2":
            print("\n>>> Iniciando análisis de neuropatía...")
            df_largo = analisis_neuropatia_diabetica.crea_df_neuropatia()
            analisis_neuropatia_diabetica.graf_boxplot_neuropatia(df_largo)

        elif opcion == "3":
            print("\n>>> Iniciando análisis de Estrés...")
            df_largo = analisis_estres.crea_df()
            analisis_estres.graf_boxplot(df_largo)

        elif opcion == "4":
            print("\n>>> Iniciando análisis de Dinámica Familiar...")
            df_largo = analisis_dinafamiliar.crea_df()
            analisis_dinafamiliar.graf_boxplot(df_largo)
        
        elif opcion == "5":
            print("\n>>> Iniciando Regresion Logistica Neuropatica Diabética...")
            regrelogi_diabetes_v2.calculo_regrelogis_diabetes()
            regrelogi_diabetes_v2.grafica_regrelogis_diabetes()
            # df_largo = regrelogi_diabetes_v2.crea_df()
            # regrelogi_diabetes_v2.graf_boxplot(df_largo)
        
        elif opcion == "6":
            print("\n>>> Iniciando Regresion Logistica Estrés...")
            regrelogi_estres.calculo_regrelogis_estres()
            regrelogi_estres.grafica_regrelogis_estres()
            # df_largo = regrelogi_estres.crea_df()
            # regrelogi_estres.graf_boxplot(df_largo)

        elif opcion == "6":
            print("\n>>> Iniciando Regresion Logistica Dinámica Familiar...")
            regrelogi_estres.calculo_regrelogis_estres()
            regrelogi_estres.grafica_regrelogis_estres()

        elif opcion == "7":
            print("\n>>> Iniciando Regresion Dinámica Familiar...")
            regrelogi_dinafami.calculo_regrelogis_dinafamiliar()
            regrelogi_dinafami.grafica_regrelogis_dinafamiliar()

        elif opcion == "0":
            print("\nSaliendo de RELOPEN...")
            break
        else:
            print("\n[!] Opción no válida. Por favor, intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
