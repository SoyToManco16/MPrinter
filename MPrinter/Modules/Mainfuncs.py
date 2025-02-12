# Librerías
import os
from Interface.ascii import stewie
from colorama import Fore, init
from tabulate import tabulate
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog



# Variable global para almacenar la impresora predeterminada
mainprinter = None 

# Inicializar colorama
init(autoreset=True)

# ------------------------- FUNCIONES PARA SISTEMA -------------------------
def getos():
    ostype = os.name

    if ostype == 'nt':
        return "windows"
    else:
        return "linux"

system = getos()

if system == "windows":
    try:
        import win32print
        import win32api
        color = "c"
    except ImportError:
        win32print = None
else:
    try:
        import cups
        color = "y"
    except ImportError:
        cups = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def cc(text, color):

    """ Función para colorear texto"""

    colors = {
        "r": Fore.RED,
        "a": Fore.BLUE,
        "v": Fore.GREEN,
        "y": Fore.YELLOW,
        "c": Fore.CYAN,
        "m": Fore.MAGENTA,
        "ly": Fore.LIGHTYELLOW_EX,
        "lr": Fore.LIGHTRED_EX,
        "lm": Fore.LIGHTMAGENTA_EX,
        "lc": Fore.LIGHTCYAN_EX,
        "la": Fore.LIGHTBLUE_EX,
        "g": Fore.RESET  # Color por defecto (gris/blanco según terminal)
    }

    return f"{colors.get(color, Fore.RESET)}{text}{Fore.RESET}"

# ------------------------- FUNCIONES BÁSICAS IMPRESORAS -------------------------

def mainprint():

    """Obtener impresora principal (solo una vez al inicio)"""

    if os.name == "nt" and win32print:
        mainprinter = win32print.GetDefaultPrinter()
    elif cups:
        conn = cups.Connection()
        mainprinter = conn.getDefault()
    else:
        mainprinter = None

    return mainprinter

def list_printers():
    """Función para mostrar las impresoras disponibles y permitir su selección."""
    printers_list = []

    # Detectar sistema operativo y obtener lista de impresoras
    if system == "windows":
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printers_list = [printer[2] for printer in printers]
    else:
        result = subprocess.run(['lpstat', '-a'], capture_output=True, text=True)
        printers_list = [line.split()[0] for line in result.stdout.splitlines()]
    
    # Mostrar la lista de impresoras
    print(cc("IMPRESORAS DISPONIBLES", color))
    for idx, printer in enumerate(printers_list, start=1):
        print(f"{idx}. {printer}")

    # Solicitar al usuario que seleccione una impresora
    option = input(cc("Seleccione una impresora (número): ", color))
    try:
        option_num = int(option)
        if 1 <= option_num <= len(printers_list):
            selected_printer = printers_list[option_num - 1]
            print(f"Seleccionaste: {selected_printer}")
            return selected_printer
        else:
            print(cc("Número fuera de rango.", "y"))
    except ValueError:
        print(cc("Entrada no válida", "r"))
# ------------------------- FUNCIONES PARA ADMINISTRAR IMPRESORAS -------------------------

def set_default_printer(printer_name):
    """Establece la impresora como predeterminada."""
    try:
        if system == "windows":  # Windows
            win32print.SetDefaultPrinter(printer_name)
        else:  # Linux (CUPS)
            subprocess.run(["lpadmin", "-d", printer_name], check=True)
        
        print(cc(f"La impresora '{printer_name}' ha sido establecida como predeterminada.", "v"))
    
    except Exception as e:
        print(cc(f"Error al cambiar la impresora predeterminada: {e}", "r"))

def print_test_page(printer_name):
    """Imprime una página de prueba con un mensaje personalizado."""
    print(f"Imprimiendo página de prueba en '{printer_name}'...")

    # Crear archivo de texto temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(stewie)
        test_file = temp_file.name  # Guardar el nombre del archivo

    try:
        if system == "windows":  # Windows
            subprocess.run(["notepad.exe", "/p", test_file], check=True)
        else:  # Linux (CUPS)
            subprocess.run(["lp", "-d", printer_name, test_file], check=True)
        
        print("Página de prueba enviada a la impresora.")

    except Exception as e:
        print(f"Error al imprimir página de prueba: {e}")

    finally:
        os.remove(test_file)  # Eliminar archivo temporal después de imprimir

def manage_printers_submenu(printer_name):
    """Menú de administración de la impresora."""
    print(cc("\nOpciones para la impresora seleccionada", color))
    print(cc("1. Hacerla predeterminada", color))
    print(cc("2. Imprimir página de prueba", color))
    print(cc("3. Cancelar", color))

    try:
        option = int(input("Selecciona una opción: "))

        if option == 1:
            set_default_printer(printer_name)
        elif option == 2:
            print_test_page(printer_name)
        elif option == 3:
            print("Operación cancelada.")
        else:
            print("Opción no válida.")

    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")

# ------------------------- FUNCIONES PARA COLA DE IMPRESIÓN -------------------------
def list_queue():
    if system == "windows":
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(hprinter, 0, -1, 1)
        win32print.ClosePrinter(hprinter)
        return [{"Job ID": job["JobId"], "Document": job["Document"], "Status": job["Status"]} for job in jobs]
    
    else:
        conn = cups.Connection()
        jobs = conn.getJobs()
        return [{"Job ID": job, "Title": jobs[job]["title"], "Status": jobs[job]["job-state"]} for job in jobs]


# ------------------------- FUNCIONES PARA IMPRESIÓN DE ARCHIVOS -------------------------

def select_archive():
    """Abre un cuadro de diálogo para seleccionar un archivo PDF."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos PDF", "*.pdf"),("Todos los archivos", "*.*"))
    )
    root.destroy()  # Cierra la ventana de selección
    return archivo

def print_document(defprinter, archivo):

    if system == "windows":
        print(f"Impresora predeterminada: {defprinter}")

        # Enviar el archivo PDF a la impresora utilizando win32api
        win32api.ShellExecute(
            0,
            "print",
            archivo,
            None,
            ".",
            0
        )
    else:
        # Enviar el archivo PDF a la impresora utilizando lp
        subprocess.run(['lp', '-d', defprinter, archivo], capture_output=True, text=True)
        print("Archivo enviado a la impresora en Linux.")
    