import os
import uuid

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
credential = DefaultAzureCredential()


def upload_to_blob(file):
    storage_url = "https://lenskartsa.blob.core.windows.net/"

    blob_client = BlobClient(
        storage_url,
        container_name="lenskardata",
        blob_name=file,
        credential=credential,
    )

    with open(file, "rb") as data:
        blob_client.upload_blob(data)
        print(f"Uploaded {file} to {blob_client.url}")