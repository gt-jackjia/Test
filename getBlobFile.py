"""
NOTE: 
BlobServiceClient class allows you to manipulate Azure Storage resources and blob containers.
ContainerClient class allows you to manipulate Azure Storage containers and their blobs.
BlobClient class allows you to manipulate Azure Storage blobs.
"""
import os
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from azure.identity import DefaultAzureCredential


blob_service_client = BlobServiceClient(account_url="https://rgcybersecurityprivb443.blob.core.windows.net/eks-privacy-blob", credential=DefaultAzureCredential())

"""
TODO:
Retrieve File from the blob. For now, retrieve any file, just make it work.

"""
def getFileFromBlob(CONTAINERNAME:str, BLOBNAME:str):
    blob_client = blob_service_client.get_blob_client(container=CONTAINERNAME, blob=BLOBNAME, snapshot=None)

    with open(file=os.path.join(os.getcwd(),BLOBNAME), mode='wb') as blob_file:
        download_stream = blob_client.download_blob()
        blob_file.write(download_stream.readall())


"""
def getBlobFile(blobPath: str):
    BLOBNAME = blobPath
    blob_service_client_instance = BlobServiceClient(
        account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
    blob_client_instance = blob_service_client_instance.get_blob_client(
        CONTAINERNAME, BLOBNAME, snapshot=None)
    blob_data = blob_client_instance.download_blob()
    return pd.read_csv(StringIO(str(blob_data.readall(),'utf-8')))


"""






    
