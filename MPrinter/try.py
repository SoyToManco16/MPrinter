import win32print
import subprocess
import win32api
import tkinter as tk
from tkinter import filedialog
from colorama import Fore

def getos():
    ostype = os.name

    if ostype == 'nt':
        return "windows"
    else:
        return "linux"

system = getos()

def listprinters():
    """Función para mostrar detalles de las impresoras y permitir su selección."""
    # Obtener la impresora principal (por ejemplo, la predeterminada)
    principal = mainprint()  
    printers_list = []  # Cada elemento será una lista con los datos de una impresora

    # Rellenar los datos según el sistema
    if system == "windows" and win32print:
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            for printer in printers:
                printer_name = printer[2]
                handle = win32print.OpenPrinter(printer_name)
                info = win32print.GetPrinter(handle, 2)
                # Se recopilan algunos datos relevantes para Windows
                row = [
                    info.get('pPrinterName', 'Desconocido'),
                    str(info.get('Status', 'Desconocido')),
                    info.get('pDriverName', 'Desconocido'),
                    info.get('pPortName', 'Desconocido')
                ]
                printers_list.append(row)
                win32print.ClosePrinter(handle)
        except Exception as e:
            print(cc(f"Error obteniendo impresoras en Windows: {e}", "r"))
            return
    elif cups:
        try:
            conn = cups.Connection()
            cups_printers = conn.getPrinters()
            for name, info in cups_printers.items():
                # Se recopilan algunos datos relevantes para CUPS
                row = [
                    name,
                    str(info.get('printer-state', 'Desconocido')),
                    info.get('printer-location', 'No especificada'),
                    info.get('printer-make-and-model', 'Desconocido'),
                    info.get('device-uri', 'No especificada'),
                    str(info.get('printer-is-accepting-jobs', 'Desconocido')),
                    str(info.get('printer-type', 'Desconocido')),
                    str(info.get('color-supported', 'Desconocido'))
                ]
                printers_list.append(row)
        except Exception as e:
            print(cc(f"No hemos podido obtener impresoras: {e}", "r"))
            return
    else:
        print(cc("Sistema no compatible !!", "r"))
        return

    # Reordenar la lista para que la impresora principal aparezca primero (si se encuentra)
    principal_row = None
    others = []
    for row in printers_list:
        if row[0] == principal:
            principal_row = row
        else:
            others.append(row)
    final_list = [principal_row] + others if principal_row is not None else printers_list

    # Mostrar la lista de impresoras de forma simple con numeración
    print("Impresoras disponibles:")
    for idx, row in enumerate(final_list, start=1):
        # Se muestran algunos datos básicos; se pueden ajustar según convenga
        # Aquí se muestran: Nombre, Estado y Ubicación
        print(f"{idx}. {row[0]} - Estado: {row[1]}, Ubicación: {row[2]}")

    # Solicitar al usuario que seleccione una impresora por su número
    option = input(cc("Seleccione una impresora (número): ", color))
    try:
        option_num = int(option)
        if 1 <= option_num <= len(final_list):
            selected_printer = final_list[option_num - 1][0]
            print(cc(f"Seleccionaste: {selected_printer}", "v"))
            return selected_printer
        else:
            print(cc("Número fuera de rango.", "r"))
    except ValueError:
        print(cc("Entrada no válida.", "r"))

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

def select_archive():
    """Abre un cuadro de diálogo para seleccionar un archivo PDF."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*"))
    )
    root.destroy()  # Cierra la ventana de selección
    return archivo

def print_archive(archivo):

    defprinter = listprinters()
    set_default_printer(defprinter)

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