from datetime import datetime, timedelta, timezone
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv
import os

load_dotenv()

# Genera una URL segura y temporal para visualizar un archivo privado en Azure Blob Storage
def generate_url_sas(blob_name, expira_en_min=15):
    try:
        # Lee las credenciales para firmar el Token SAS
        account_name = os.getenv('AZURE_ACCOUNT_NAME')
        account_key = os.getenv('AZURE_ACCOUNT_KEY')
        container_name = os.getenv('AZURE_CONTAINER_NAME')

        # Validación de seguridad: Si las credenciales no están presentes no se genera el SAS e informa del error
        if not all([account_name, account_key, container_name]):
            print("Error: Faltan credenciales de Azure")
            return None
        
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True), # Permiso estricto de solo lectura
            expiry=datetime.now(timezone.utc) + timedelta(minutes=expira_en_min)
        )

        url_segura = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
        return url_segura
    
    except Exception as e:
        print(f"Error al generar URL SAS para  '{blob_name}': {e}")
        return None
