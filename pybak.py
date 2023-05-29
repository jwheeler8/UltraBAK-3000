import os
import datetime
from concurrent.futures import ThreadPoolExecutor
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


directorio_credenciales = 'credentials_module.json'


# INICIAR SESION
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)



# Subir un archivo
def subir_archivo(ruta_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{'id': id_folder['id']}]})
    archivo['title'] = ruta_archivo.split('/')[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()


# subir directorio
def subir_directorio(ruta_directorio, parent_folder_id=None):
    folder_name = os.path.basename(ruta_directorio)
    folder = crear_carpeta(folder_name, parent_folder_id)
    with ThreadPoolExecutor() as executor:
        for item in os.listdir(ruta_directorio):
            ruta_item = os.path.join(ruta_directorio, item)
            if os.path.isfile(ruta_item):
                executor.submit(subir_archivo, ruta_item, folder)

            elif os.path.isdir(ruta_item):
                executor.submit(subir_directorio, ruta_item, folder['id'])
               

# CREACIÓN DE CARPETAS
def crear_carpeta(nombre_carpeta, parent_id=None):
    credenciales = login()
    metadata = {'title': nombre_carpeta, 'mimeType': 'application/vnd.google-apps.folder',
                }
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]
    carpeta = credenciales.CreateFile(metadata)
    carpeta.Upload()

    return carpeta

def main():
    fecha = 'BAK'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # CARPETA EN DONDE SE VAN A GUARDAR TODOS LOS BACKUPS,M CUENTA CON SU ID ÚNICO.
    carpeta = crear_carpeta(fecha,'1YygmxHnRyCNEW6JmtaWbK7AyYdvvnxKg')
    print(f'Carpeta creada: {fecha}')

    # DIRECTORIO EN EL QUE SE REALIZARÁ EL BACKUP
    # NO FUNCIONA CON BACKSLASHES
    ruta_directorio = 'D:/WebWorks/pybak'

    subir_directorio(ruta_directorio,carpeta['id'])
    print('Directorio subido correctamente.')


if __name__ == "__main__":
    main()



