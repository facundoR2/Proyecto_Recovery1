import os # Para manejar rutas de archivos y directorios
import shutil   # Para copiar archivos y directorios
from os import walk # Para recorrer directorios
from shutil import copyfile # Para copiar archivos
import psutil # Para detectar unidades USB

def recover_usb_data(usb_path, output_folder_name="USB_RecoveryV1"):
    # Obtener el escritorio del usuario
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_folder = os.path.join(desktop, output_folder_name)

    def detect_usb_drives():
        usb_drives = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if 'removable' in partition.opts:
                usb_drives.append(partition.device)
        return usb_drives

    # Crear la carpeta de destino si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Verificar si el USB existe
    if not os.path.exists(usb_path):
        print(f"El USB en la ruta '{usb_path}' no fue encontrado.")
        print("Por favor, asegúrate de que el USB esté conectado.")
        usb_drives = detect_usb_drives() # Detectar unidades USB
        if usb_drives:
            print("Unidades USB detectadas:")
            for drive in usb_drives:
                print(drive)
        else:
            print("No se detectaron unidades USB.")
        return

    # Copiar los archivos del USB a la carpeta de destino
    try:
        for item in os.listdir(usb_path):
            source = os.path.join(usb_path, item)
            destination = os.path.join(output_folder, item)

            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        print(f"Datos recuperados exitosamente en: {output_folder}")
    except Exception as e:
        print(f"Error al recuperar los datos: {e}")

if __name__ == "__main__":
    # Cambia 'D:\\' por la letra de tu unidad USB
    usb_drive_path = "D:\\"
    output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "USB_Recovery")
    recover_usb_data(usb_drive_path)
    # Intentar recuperar archivos corruptos
    try:

        for root, dirs, files in walk(usb_drive_path):
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(output_folder, os.path.relpath(source_file, usb_drive_path))
                # IDea: convertir los datos del archivo a bytes y luego a string. 
                # Esto puede ayudar a identificar archivos corruptos.
                # el archivo como texto plano.
                # Leer el archivo como texto plano
                # Abrir el archivo en modo binario?
                # investigar en la documentación de Python.
                # intentar abrir el archivo
                # si el archivo no se abre, ver excepción.
                # mostrar peso del archivo.
                

                # Crear directorios necesarios en la carpeta de destino
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)

                try:
                    copyfile(source_file, destination_file)
                except Exception as e:
                    print(f"Error al copiar el archivo corrupto '{source_file}': {e}")

        print("Intento de recuperación de archivos corruptos completado.")
    except Exception as e:
        print(f"Error al intentar recuperar archivos corruptos: {e}")