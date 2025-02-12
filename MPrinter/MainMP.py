# Librerías
from Interface.ascii import mp_main
from Modules.Mainfuncs import *

# Obtener datos de funciones 
system = getos() # Sistema
mainprinter = mainprint() # Impresora principal
 
# Variable menu
option = "0"

if system == "windows":
    color = "c"
else:
    color = "y"

# Desplegar opciones
def options():

    """ Función para mostrar opciones en el menú principal 
        y no repetir código """
    
    print(cc("\n1. Administrar impresoras", color))
    print(cc("2. Gestionar trabajos de impresión", color))
    print(cc("3. Imprimir archivos", color))
    print(cc("Exit para salir y clear para limpiar la pantalla", color))


# Menú principal
def main_menu():
    if system == "windows":
        print(cc(mp_main, color))
        print(cc(f"Sistema en uso: {cc(system, "g")}", color))
        print(cc(f"Impresora principal: {cc(mainprinter, "g")}", color))
    else:
        print(cc(mp_main, color))
        print(cc(f"Sistema en uso: {cc(system, "g")}", color))
        print(cc(f"Impresora principal: {cc(mainprinter, "g")}", color))
   

if __name__ == "__main__":
    # Flujo principal
    try:
        while option != "exit":

            main_menu()
            options()

            option = input(cc("Introduce una opción (1-4): ", color))

            if option == "1":
                print(cc("\nADMINISTRACIÓN DE IMPRESORAS\n", color))
                selectprinter = list_printers() # Esta función lista todas las impresoras y nos permite manejarlas
                manage_printers_submenu(selectprinter)

            elif option == "2":
                print(cc("\nGESTIONAR TRABAJOS DE IMPRESIÓN\n", color))
                list_queue()
                

            elif option == "3":
                print(cc("\nIMPRIMIR ARCHIVOS\n", color))
                archivo = select_archive()
                printerrr = list_printers()
                set_default_printer(printerrr)
                print_document(printerrr, archivo)

            elif option == "clear":
                clear()

            elif option == "exit":
                print(cc("\nByeee !!", "v"))

            else:
                print(cc("\nOpción no válida", "r"))

    except KeyboardInterrupt:
        print("Byee !!")        

    
    
        
