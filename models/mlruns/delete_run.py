import os
import shutil
import yaml
import time

# ce script permet de supprimer les dossiers des runs supprimés dans l'interface MLflow 
# car MLfow ne supprime pas les dossiers des runs supprimés en local 
# Il va chercher dans les fichiers meta.yaml des dossiers des runs si le lifecycle_stage est 'deleted', si oui il supprime le dossier
# si non il passe au dossier suivant, il compte le nombre de dossiers supprimés si il y en a sinon il affiche 0

def delete_directory_with_retry(directory, max_attempts=3, delay_between_attempts=1):
    """
    Tente de supprimer le répertoire avec plusieurs tentatives. Cela est utile pour gérer les cas où 
    le système d'exploitation verrouille temporairement des fichiers, empêchant leur suppression immédiate.
    
    Args:
        directory (str): Le chemin du dossier à supprimer.
        max_attempts (int): Nombre maximal de tentatives de suppression.
        delay_between_attempts (int): Délai en secondes entre les tentatives.
    
    Returns:
        bool: True si le dossier a été supprimé, False sinon.
    """
    for attempt in range(max_attempts):
        try:
            shutil.rmtree(directory)  # Tente de supprimer le dossier et tout son contenu.
            print(f"Dossier {directory} supprimé")
            return True  # Retourne True si la suppression est réussie.
        except Exception as e:
            # Affiche un message d'erreur si la suppression échoue et attend avant de réessayer.
            print(f"Tentative {attempt + 1} : Impossible de supprimer {directory}: {e}")
            time.sleep(delay_between_attempts)
    return False  # Retourne False après avoir épuisé toutes les tentatives.

def delete_directories_with_deleted_lifecycle_stage(root_dir):
    """
    Parcourt récursivement le répertoire spécifié à la recherche de fichiers `meta.yaml`.
    Supprime le dossier parent si le `lifecycle_stage` de l'expérience est marqué comme 'deleted'.
    
    Args:
        root_dir (str): Le chemin du répertoire racine à partir duquel commencer la recherche.
    """
    fold_deleted = 0  # Compteur pour le nombre de dossiers supprimés.

    for root, dirs, files in os.walk(root_dir, topdown=False):
        for file in files:
            if file == 'meta.yaml':
                file_path = os.path.join(root, file)
                # Ouverture et lecture du fichier meta.yaml
                try:
                    with open(file_path, 'r') as yaml_file:
                        data = yaml.safe_load(yaml_file)
                        # Fermeture forcée du fichier, normalement inutile avec 'with' mais dans ce contexte 
                        # il m'évite une erreur de type WindowsError32 (The process cannot access the file because it is being used by another process)
                        yaml_file.close()  
                except Exception as e:
                    print(f"Erreur lors de la lecture de {file_path}: {e}")
                    continue
                
                 # Vérifie si le lifecycle_stage est marqué comme 'deleted'.
                if data.get('lifecycle_stage', '') == 'deleted':
                    # Tente de supprimer le dossier et incrémente le compteur si la suppression est réussie.
                    if delete_directory_with_retry(root):
                        fold_deleted += 1
    print(f"Nombre total de dossiers supprimés : {fold_deleted}")


# Spécifie que le script est exécuté depuis le répertoire contenant `mlrusns`.
root_dir = '.'  
delete_directories_with_deleted_lifecycle_stage(root_dir)
