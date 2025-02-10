# Librerías
from Interface.ascii import mp_main
from Modules.Mainfuncs import clear, getos, cc, mainprint, listprinters, manage_printer_jobs

# Obtener datos de funciones 
system = getos() # Sistema
mainprinter = mainprint() # Impresora principal
 
# Definir color menús según SO
if system == "windows":
    color = "c"
else:
    color = "y"

# Desplegar opciones
def options():

    """ Función para mostrar opciones en el menú principal 
        y no repetir código """

    if system == "win":
        print(cc("\n1. Administrar impresoras", color))
        print(cc("2. Gestionar trabajos de impresión", color))
        print(cc("3. Imprimir archivos", color))
        print(cc("4. Monitorizar impresión", color))
        print(cc("5. Configurar impresoras", color))
        print(cc("Exit para salir", color))

    else:
        print(cc("\n1. Administrar impresoras", color))
        print(cc("2. Gestionar trabajos de impresión", color))
        print(cc("3. Imprimir archivos", color))
        print(cc("4. Monitorizar impresión", color))
        print(cc("5. Configurar impresoras", color))
        print(cc("Exit para salir", color))
        


# Menú principal
def main_menu():
    clear()
    if system == "win":
        print(cc(mp_main, "c"))
        print(cc(f"Sistema en uso: {cc(system, "g")}", "c"))
        print(cc(f"Impresora principal: {cc(mainprinter, "g")}", "c"))
    else:
        print(cc(mp_main, "y"))
        print(cc(f"Sistema en uso: {cc(system, "g")}", "y"))
        print(cc(f"Impresora principal: {cc(mainprinter, "g")}", "y"))


   

if __name__ == "__main__":
    # Flujo principal
    main_menu()
    options()

    try:
        option = input(cc("Introduce una opción (1/5): ", color))
        clear()

        if option == "1":
            print(cc("\nADMINISTRACIÓN DE IMPRESORAS\n", color))
            listprinters() # Esta función lista todas las impresoras y nos permite manejarlas

        elif option == "2":
            print(cc("\nGESTIONAR TRABAJOS DE IMPRESIÓN\n", color))
            manage_printer_jobs(mainprinter)

        elif option == "3":
            print(cc("\nIMPRIMIR ARCHIVOS\n", color))


        elif option == "4":
            print(cc("\nMONITORIZAR IMPRESIÓN\n", color))


        elif option == "5":
            print(cc("\nCONFIGURACIÓN DE IMPRESORAS\n", color))

        elif option == "exit":
            print(cc("\nByeee !!", "v"))

        else:
            print(cc("\nOpción no válida", "r"))


    except KeyboardInterrupt:
        print("Byee !!")

    
    
        
