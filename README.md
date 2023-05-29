# UltraBAK-3000
Sistema de respaldo de archivos con Batch/Python
PASOS A TENER EN CUENTA

1. Instalar las siguientes dependencias:
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 
   pip install pydrive2
3. Ejecutar el script quickstart.py(solo se ejecuta una vez para hacer la autenticación)
5. En pybak.py: Asignar el id de la carpeta en el método crear_carpeta dentro del main.
6. Asignar un directorio para hacer el backup(no funciona con backslashes)
7. Ejecutar el script
