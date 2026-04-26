from storages.backends.azure_storage import AzureStorage
from dotenv import load_dotenv
import os

load_dotenv()

# Storage_backend : Es el backend de almacenamiento personalizado para subir archivos multimedias (imagenes) a Azure.
# Se utiliza la cadena de conexión para permisos de escritura.

class AzureMediaStorage(AzureStorage):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    expiration_secs = None 

    def _save(self, name, content):
        print(f"Intentando subir archivo a Azure Storage: {name}")

        try:
            result = super()._save(name, content)
            print(f"Archivo '{name}' subido exitosamente a Azure Storage.")
            return result

        except Exception as e:
            print(f"Error al subir archivo '{name}' a Azure Storage: {e}")
            raise e
