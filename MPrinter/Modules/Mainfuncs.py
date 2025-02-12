# Librerías
import os
from Interface.ascii import stewie
from colorama import Fore, init
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

def start_printer(printer_name):

    if system == "windows":
        print("Luego")

    else:

        try:
            conn = cups.Connection()
            conn.enablePrinter(printer_name)
            print(cc(f"Impresora habilitada correctamente", "v"))
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def stop_printer(printer_name):

    if system == "windows":
        print("Luego")

    else:
        try:
            conn = cups.Connection()
            conn.disablePrinter(printer_name)
            print(cc(f"Impresora deshabilitada correctamente", "v"))
            
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def remove_printer(printer_name):

    if system == "windows":
        print("Luego")

    else:
        try:
            conn = cups.Connection()
            conn.deletePrinter(printer_name)
            print(cc(f"Impresora deshabilitada correctamente", "v"))
            
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def manage_printers_submenu(printer_name):
    """Menú de administración de la impresora."""
    print(cc("\nOpciones para la impresora seleccionada", color))
    print(cc("1. Hacerla predeterminada", color))
    print(cc("2. Imprimir página de prueba", color))
    print(cc("3. Iniciar impresora", color))
    print(cc("4. Pausar impresora", color))
    print(cc("5. Eliminar impresora", color))
    print(cc("6. Cancelar", color))

    try:
        option = int(input("Selecciona una opción: "))

        if option == 1:
            set_default_printer(printer_name)
        elif option == 2:
            print_test_page(printer_name)
        elif option == 3:
            start_printer(printer_name)
        elif option == 4:
            stop_printer(printer_name)
        elif option == 5:
            remove_printer(printer_name)
        elif option == 6:
            print("Operación cancelada.")
        else:
            print("Opción no válida.")

    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")

# ------------------------- FUNCIONES PARA COLA DE IMPRESIÓN -------------------------
def list_queue():
    if system == "windows":
        printer_name = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(handle, 0, 10, 1)
        if len(jobs) == 0:
            return "empty"
        else:
            for job in jobs:
                print(f"Job ID: {job['JobId']}, Estado: {job['Status']}, Usuario: {job['UserName']}, Documento: {job['pDocument']}")
    
    else:
        try: 
            conn = cups.Connection()
            jobs = conn.getJobs()

            if len(jobs) == 0:
                return "empty"
            else: 
                for job_id, job in jobs.items():
                    print(f"Job ID: {job_id}")
                    print(f"Usuario: {job.get('job-originating-user-name', 'Desconocido')}")
                    print(f"Nombre del trabajo: {job.get('title', 'Sin nombre')}")
                    print(f"Estado del trabajo: {job.get('job-state', 'Desconocido')}")
                    print(f"Impresora: {job.get('printer-uri', 'Desconocida')}")
                    print(f"Fecha: {job.get('time-at-creation', 'Desconocida')}")
                    print("---" * 40)

        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def start_job(job_id):

    if system == "windows":
        print("Por implementar")
    else:
        conn = cups.Connection()
        try:
            conn.restartJob(job_id)
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def cancel_job(job_id):

    if system == "windows":
        print("Por implementar")
    else:
        conn = cups.Connection()
        try:
            conn.cancelJob(job_id)
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def cancel_all_jobs():

    if system == "windows":
        print("Por implementar")
    else:
        conn = cups.Connection()
        try:
            conn.cancelAllJobs()
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def move_job_to_first_place(job_id, printer_name):

    if system == "windows":
        print("Por implementar")
    else:
        conn = cups.Connection()
        # Obtener información del trabajo antes de cancelarlo
        job_info = conn.getJobAttributes(job_id)
        file_path = job_info['file']
        try:
            conn.cancelJob(job_id)
            add_job(printer_name, file_path, f"Trabajo {job_id} reenviado a el principio de la cola")
        except Exception as e:
            print(cc(f"Error: {e}", "r"))

def manage_job_list_submenu(job_id, mainprinter):
    """ Submenú para trabajar con la cola de impresión """
    print(cc("\nOpciones para el trabajo seleccionado", color))
    print(cc("1. Reanudar trabajo", color))
    print(cc("2. Cancelar trabajo", color))
    print(cc("3. Cancelar todos los trabajos", color))
    print(cc("4. Mover trabajo al principio de la cola", color))
    print(cc("5. Cancelar", color))

    option = input(cc("Introduce una opción: ", color))

    if option == "1":
        start_job(job_id)
    elif option == "2":
        cancel_job(job_id)
    elif option == "3":
        cancel_all_jobs()
    elif option == "4":
        move_job_to_first_place(job_id, mainprinter)
    elif option == "5":
        return
    else:
        print(cc("Opción no válida", "r"))
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
