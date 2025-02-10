# Librerías
import os
from Interface.ascii import stewie
from colorama import Fore, init
from tabulate import tabulate
import subprocess
import tempfile

# Variable global para almacenar la impresora predeterminada
mainprinter = None 

# Inicializar colorama
init(autoreset=True)

# Funciones
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

def create_table(data, header=None, formato="grid", border_color=color):
    """
    Genera una tabla con bordes coloreados.
    
    Args:
        data: Lista de listas con los datos.
        header: Lista con encabezados (opcional).
        formato: Formato de tabla (por defecto "grid").
        border_color: Color de los bordes (por defecto "c" para cyan).
    """
    table = tabulate(data, headers=header, tablefmt=formato)
    
    # Dividir la tabla en líneas
    table_lines = table.splitlines()
    colored_table = ""
    for line in table_lines:
        colored_line = ""
        # Colorear caracteres de borde: "+", "|" y "-"
        for char in line:
            if char in ("+", "|", "-"):
                colored_line += cc(char, border_color)
            else:
                colored_line += char
        colored_table += colored_line + "\n"
    return colored_table

# Funciones para las impresoras

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

# ------------------------- FUNCIONES PARA ADMINISTRAR IMPRESORAS -------------------------

def set_default_printer(printer_name):
    """Establece la impresora como predeterminada."""
    try:
        if os.name == "nt":  # Windows
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
        if os.name == "nt":  # Windows
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
    print("\nOpciones para la impresora seleccionada:")
    print("1. Hacerla predeterminada")
    print("2. Imprimir página de prueba")
    print("3. Cancelar")

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


def listprinters():
    """Función para mostrar detalles de las impresoras y permitir su administración."""
    # Obtener la impresora principal
    principal = mainprint()
    table_data = []  # Aquí se almacenarán las filas (cada fila es una lista)
    headers = []     # Se asignarán según el sistema

    # Rellenar los datos según el sistema
    if os.name == "nt" and win32print:
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            for printer in printers:
                printer_name = printer[2]
                printer_handle = win32print.OpenPrinter(printer_name)
                printer_info = win32print.GetPrinter(printer_handle, 2)
                # Cada fila con los datos relevantes para Windows
                row = [
                    printer_info['pPrinterName'],
                    printer_info['Status'],
                    printer_info['pLocation'] or "No especificada",
                    printer_info['pDriverName'],
                    printer_info['pPortName'],
                    printer_info.get('pPrintProcessor', 'Desconocido'),
                    printer_info.get('pComment', 'No disponible')
                ]
                table_data.append(row)
                win32print.ClosePrinter(printer_handle)
            headers = ["Nombre", "Estado", "Ubicación", "Controlador", "Puerto", "Procesador", "Comentario"]
        except Exception as e:
            print(cc(f"Error obteniendo impresoras en Windows: {e}", "r"))
            return

    elif cups:
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            for name, info in printers.items():
                # Cada fila con los datos relevantes para CUPS
                row = [
                    name,
                    info.get('printer-state', 'Desconocido'),
                    info.get('printer-location', 'No especificada'),
                    info.get('printer-make-and-model', 'Desconocido'),
                    info.get('device-uri', 'No especificada'),
                    info.get('printer-is-accepting-jobs', 'Desconocido'),
                    info.get('printer-type', 'Desconocido'),
                    info.get('color-supported', 'Desconocido')
                ]
                table_data.append(row)
            headers = ["Nombre", "Estado", "Ubicación", "Modelo", "URI", "Acepta trabajos", "Tipo", "Soporta color"]
        except Exception as e:
            print(cc(f"No hemos podido obtener impresoras: {e}", "r"))
            return
    else:
        print(cc("Sistema no compatible !!", "r"))
        return

    # Reordenar la lista para que la impresora principal aparezca primero (si se encuentra)
    main_row = None
    other_rows = []
    for row in table_data:
        if row[0] == principal:
            main_row = row
        else:
            other_rows.append(row)
    final_table = [main_row] + other_rows if main_row is not None else table_data

    # Añadir numeración: se inserta una columna a la izquierda
    numbered_table = []
    for i, row in enumerate(final_table, start=1):
        numbered_table.append([i] + row)

    # Preparar los encabezados agregando "N°" al principio
    full_headers = ["N°"] + headers

    # Mostrar la tabla
    print(create_table(numbered_table, full_headers, border_color=color))

    # Solicitar al usuario que seleccione la impresora (por número)
    option = input(cc("Selecciona la impresora que quieres administrar (número): ", color))
    try:
        option_num = int(option)
        if 1 <= option_num <= len(numbered_table):
            selected_printer = numbered_table[option_num - 1][1]  # El nombre está en la segunda columna
            print(cc(f"Seleccionaste: {selected_printer}", "v"))
            manage_printers_submenu(selected_printer)
        else:
            print(cc("Número fuera de rango.", "r"))
    except ValueError:
        print(cc("Entrada no válida.", "r"))

# ------------------------- FUNCIONES PARA COLA DE IMPRESIÓN -------------------------

def list_jobs(printer_name):
    """Lista los trabajos de impresión pendientes."""
    if os.name == "nt":  # Windows
        jobs = win32print.EnumJobs(0, 0, -1, 1)
        for job in jobs:
            print(f"Job ID: {job['JobId']}, Document: {job['Document']}")    
    else:  # Linux (CUPS)
        result = subprocess.run(["lpstat", "-o", printer_name], capture_output=True, text=True)
        print(result.stdout)

def cancel_job(printer_name, job_id):
    """Cancela un trabajo de impresión específico."""
    if os.name == "nt":  # Windows
        win32print.SetJob(0, job_id, 3, None, 0x00000400)
    else:  # Linux (CUPS)
        subprocess.run(["cancel", f"{printer_name}-{job_id}"])

def pause_job(printer_name, job_id):
    """Pausa un trabajo de impresión específico."""
    if os.name == "nt":  # Windows
        win32print.SetJob(0, job_id, 3, None, 0x00000002)
    else:  # Linux (CUPS)
        subprocess.run(["cupsdisable", f"{printer_name}-{job_id}"])

def resume_job(printer_name, job_id):
    """Reanuda un trabajo de impresión específico."""
    if os.name == "nt":  # Windows
        win32print.SetJob(0, job_id, 3, None, 0x00000008)
    else:  # Linux (CUPS)
        subprocess.run(["cupsenable", f"{printer_name}-{job_id}"])

def prioritize_job(printer_name, job_id):
    """Prioriza un trabajo de impresión, moviéndolo a la primera posición."""
    if os.name == "nt":  # Windows
        win32print.SetJob(0, job_id, 3, None, 0x00000010)
    else:  # Linux (CUPS)
        subprocess.run(["lp", "-i", f"{printer_name}-{job_id}", "-H", "immediate"])

def manage_printer_jobs(mainprinter):
    list_jobs(mainprinter)
