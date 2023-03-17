import os
from azure.storage.blob import ContainerClient  
from datetime import datetime

"""
Ressource : Azure SDK for Python
https://learn.microsoft.com/fr-fr/python/api/overview/azure/storage-blob-readme?source=recommendations&view=azure-python

Ressource : Azure Blob Storage documentation
https://learn.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
"""

# Point de terminaison du Service Blob du Compte de stockage
account_url = 'https://rgmlstorage.blob.core.windows.net/'
# Clé d'accès du Compte de stockage
credential = 'tRpS1DRzhGd2BGt8HUZAAkxBYnFh+/VFnnKgPla7023f4rs1OF2tTK+tF0qEPzx4e56Twzdyc3H7+AStSeSWBg=='

# chaine de connection au service de storage Azure
connection_string = "DefaultEndpointsProtocol=https;AccountName=rgmlstorage;AccountKey=tRpS1DRzhGd2BGt8HUZAAkxBYnFh+/VFnnKgPla7023f4rs1OF2tTK+tF0qEPzx4e56Twzdyc3H7+AStSeSWBg==;EndpointSuffix=core.windows.net"
# Nom du conteneur
container_name = 'jet-varnish-mgi'


"""Fonction créant un répertoire si il n'existe pas"""
def check_file_path(path):
    local_files = []
    if not os.path.isdir(path):
        os.makedirs(path)
        print("Création du répertoire '"+path+"'.")
    else :
        for root, dirs, files in os.walk(path):
            for name in files:
                local_files.append(name)
    return local_files        


"""Fonction pour télécharger en local tous les fichiers du blob en précisant l'extension"""
def download_blob_files(file_extension, local_path):
    
    # Si le chemin existe on retourne la liste des fichiers existants sinon on crée un répertoire
    files = check_file_path(local_path)

    try:
        # On crée un objet ContainerClient 
        # pour se connecter au conteneur avec url et credential
        #container_client = ContainerClient(account_url, container_name, credential)
        # ou en utilisant la chaine de connection
        container_client = ContainerClient.from_connection_string(connection_string, container_name)

        # On itère dans tous les blobs du conteneur
        for blob in container_client.list_blob_names():
            blob_name = blob.split('/')[-1]
            # pour chaque blob (fichier) du conteneur selon son extension
            if blob[-3:] == file_extension and blob_name not in files :
                # On crée une copie locale du fichier
                with open(file= local_path+blob_name, mode="wb") as download_file:
                    download_file.write(container_client.download_blob(blob).readall())
                    print(blob_name + ' file successfully downloaded!')
            else :
                print(blob_name +' file already in path '+ local_path +'.')

    except Exception as ex:
        print('Exception:')
        print(ex)

"""Fonction pour télécharger en local un fichier du blob"""
def download_blob_file(file_name, local_path):
    
    # Si le chemin existe on retourne la liste des fichiers existants sinon on crée un répertoire
    files = check_file_path(local_path)

    try:
        # On crée un objet ContainerClient 
        # pour se connecter au conteneur avec url et credential
        #container_client = ContainerClient(account_url, container_name, credential)
        # ou en utilisant la chaine de connection
        container_client = ContainerClient.from_connection_string(connection_string, container_name)

        if file_name not in files :
            # On itère tous les blobs du conteneur
            for blob in container_client.list_blob_names():
                blob_name = blob.split('/')[-1]
                # pour chaque blob (fichier) du conteneur selon son extension
                if blob_name == file_name :
                    # On crée une copie locale du fichier
                    with open(file= local_path+blob_name, mode="wb") as download_file:
                        download_file.write(container_client.download_blob(blob).readall())
                        print(file_name + ' successfully downloaded!')
        else :
            print(file_name +' already in path '+ local_path +'.')

    except Exception as ex:
        print('Exception:')
        print(ex)


"""Fonction pour télécharger dans un flux un fichier du blob"""
def stream_blob_files(file_extension):
        
    try:
        # On crée un objet ContainerClient 
        # pour se connecter au conteneur avec url et credential
        #container_client = ContainerClient(account_url, container_name, credential)
        # ou en utilisant la chaine de connection
        container_client = ContainerClient.from_connection_string(connection_string, container_name)

        # On itère dans tous les blobs du conteneur
        for blob in container_client.list_blob_names():
            # pour chaque blobs (fichiers) du conteneur selon son extension
            if blob[-3:] == file_extension :
                # on retourne le contenu texte
                return container_client.download_blob(blob).content_as_text()

    except Exception as ex:
        print('Exception:')
        print(ex)


"""Fonction pour charger un fichier dans le blob"""
def upload_file_to_blob(filepath, filename):
    try:
        # On crée un objet ContainerClient 
        # pour se connecter au conteneur avec url et credential
        container_client = ContainerClient(account_url, container_name, credential)
        # ou en utilisant la chaine de connection
        #container_client = ContainerClient.from_connection_string(connection_string, container_name)

        # getting the timestamp
        ts = int(datetime.timestamp(datetime.now()))

        with open(file=os.path.join(filepath, filename), mode="rb") as data:
            container_client.upload_blob(name=str(ts)+'_'+filename, data=data, overwrite=True)

    except Exception as ex:
        print('Exception:')
        print(ex)


# download_blob_files('csv', 'data/')