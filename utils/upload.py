import os
import uuid
import pandas as pd

from azure.storage.blob import ContainerClient


def upload_to_blob(file):
    container_client = ContainerClient.from_connection_string(conn_str="", container_name="lenskardata")
    with open(file, "rb") as data:
        container_client.upload_blob(name=file, data=data)
    