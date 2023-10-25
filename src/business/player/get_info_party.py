import sqlite3
import pandas as pd
import json


with open('src/business/joueur/infos_partie.json', 'r') as fichier_json:
    infos_partie = json.load(fichier_json)
    
def extract_participant_info(json_data) -> None :
    """ Obtenir les informations d'une partie à partir d'un JSON

    Parameters :
    
        json_data : JSON 

    Return :

        None
    """
    info = json_data.get("info")

    # Vérifie si json_data est un dictionnaire
    if not isinstance(json_data, dict):
        raise ValueError("json_data n'est pas un dictionnaire JSON valide")

    # Accéder aux informations spécifiques pour chaque participant
    participants = info.get("participants", [])

    # Créer une liste pour stocker les informations de tous les participants
    participant_info = []
    participant_info.append(participants["metadata"])
    participant_info.append(info["gameDuration"])
    

    for participant in participants:
        # Créer une liste avec les informations spécifiques pour ce participant
        participant_data = [
            participant["puuid"],
            participant["assists"],
            participant["championName"],
            participant["champLevel"],
            participant["deaths"],
            participant["goldEarned"],
            participant["kills"],
            participant["neutralMinionsKilled"],
            participant["role"],
            participant["lane"],
            participant["totalDamageDealt"],
            participant["win"],
            participant["teamId"]
        ]

        # Étendre la liste d'informations à la liste des participants
        participant_info.extend(participant_data)

    return participant_info
    

test = extract_participant_info(infos_partie)
print(test)
