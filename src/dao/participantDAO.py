import sqlite3
from typing import List
from src.utils.singleton import Singleton
from tabulate import tabulate
import pandas as pd
from src.dao.playerDAO import PlayerDAO
from src.business.participant.participant import Participant

class ParticipantDAO(metaclass=Singleton):
    """
    Communicate with the participant table
    """

    def __init__(self, db_file='data/database.db'):

        """
        Initialize the class with the name of the SQLite database file.

        Parameters:
        db_name (str): Name of the SQLite database file.
        """
        self.db_file = db_file


    def find_best_champ(self, critere) -> List[str]:
        """
        Get all champions by winrate return a list

        :return: A list of winrate for champions
        :rtype: List of str
        """
        critere_affichage = ["Per_game", "Per_winrate", "Per_KDA",  "Per_gold", "Per_lane", "Per_other_stat"]
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if critere==critere_affichage[0]:   
            #Liste des champions classés par popularité (nombre total de games joués)
            query=  """ SELECT championName as Champion, COUNT(*) AS total_parties       
                        FROM participant                  
                        GROUP BY championName              
                        ORDER BY total_parties DESC   
                        """ 
            cursor.execute(query)
            results = cursor.fetchall()   # Récupérer les résultats de la requête

            return results

        #Liste des champions classés par winrate (nombre de parties gagnées/nombre de parties jouées)
        elif critere==critere_affichage[1]:
            query=  """SELECT championName, COUNT(*) AS total_parties, SUM(win) AS parties_gagnees, ROUND((SUM(win) * 1.0 / COUNT(*)),2)*100 AS winrate
                    FROM participant                                 
                    GROUP BY championName                             
                    ORDER BY winrate DESC                           
                    """
            cursor.execute(query)
            results = cursor.fetchall()   # Récupérer les résultats de la requête

            return results

        #Liste des champions suivant l'ordre décroissant de leur KDA (kills+assists)/deaths sur toutes leurs parties jouées
        elif critere==critere_affichage[2]:
            query= """SELECT championName , ROUND(AVG((kills + assists) / deaths), 2) AS kda
                    FROM participant 
                    GROUP BY championName 
                    ORDER BY kda DESC  
                """
            cursor.execute(query)       
            results = cursor.fetchall()   # Récupérer les résultats de la requête

            return results

        #Liste des champions suivant l'ordre décroissant de leur gold par minute par partie 
        elif critere==critere_affichage[3]:
            query= """ SELECT championName, ROUND(AVG(goldEarned / gameDuration),2) AS golds_per_minute
                    FROM participant
                    GROUP BY championName 
                    ORDER BY golds_per_minute DESC
                """
            cursor.execute(query)       
            results = cursor.fetchall()   # Récupérer les résultats de la requête
            
            return results

        #Liste des lane suivant l'ordre décroissant du winrate par lane
        elif critere==critere_affichage[4]:
            query= """ SELECT lane, COUNT(*) AS total_parties, ROUND((SUM(win) * 1.0 / COUNT(*)),2)*100 AS winrate
                    FROM participant                                    
                    GROUP BY lane                                       
                    ORDER BY total_parties DESC                        
                    """
            cursor.execute(query)        
            results = cursor.fetchall()   # Récupérer les résultats de la requête

            return results
        
        #Liste des champions et leur gold, totalminionkilled et l'ordre décroissant de leur total_games joués
        elif critere==critere_affichage[5]:
            query=  """ SELECT championName, COUNT(*) AS total_parties, SUM(goldEarned) AS total_gold, SUM(totalMinionsKilled) AS total_minions_killed
                        FROM participant                                    
                        GROUP BY championName                               
                        ORDER BY total_parties DESC                      
                    """
            cursor.execute(query)       
            results = cursor.fetchall()   # Récupérer les résultats de la requête

            return results



    def stat_champ_by_name(self, name:str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        query = """SELECT 
                        championName AS name,
                        COUNT(*) AS total_games,
                        ROUND((SUM(win) * 1.0 / COUNT(*)), 3)*100 AS winrate,
                        ROUND(AVG((kills + assists) / deaths),2) AS kda,
                        ROUND(AVG(goldEarned / gameDuration),2) AS golds_per_minute
                    FROM participant
                    WHERE championName = ?
                    """
      
        cursor.execute(query, (name,))
        res = cursor.fetchone()

        return res

    def getpartie(self, player):
        """
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        puuid = PlayerDAO().find_player_by_name(player)._puuid
        #query = """ SELECT championName, lane, win, kills, deaths, assists,
                            #totalDamageDone, goldEarned/gameDuration
                    #FROM participant
                    #WHERE puuid = ?
                    #LIMIT 10;
                    #"""
        query = """ SELECT *
                    FROM participant
                    WHERE puuid = ?
                    LIMIT 10;
                    """

        cursor.execute(query, (puuid,))
        res = cursor.fetchall()
        parties = []
        for participant in res:
            #parties.append(Participant(*participant))
            print("début")
            print(participant[1])
            print(participant[0])
            print(participant[3])
            print(participant[4])
            print(participant[5])
            print(participant[7])
            print(participant[8])
            print(participant[6])
            print(participant[9])
            print(participant[10])
            print(participant[11])
            print(participant[12])
            print(participant[13])
            print(participant[2])
            print("fin")
            P = Participant(id_game=participant[1],
                            puuid=participant[0],
                            teamID=participant[3],
                            totalDamageDealtToChampions=participant[4],
                            win=participant[5],
                            lane=participant[7],
                            role=participant[8],
                            totalMinionsKilled=participant[6],
                            championName=participant[9],
                            goldEarned=participant[10],
                            death=participant[11],
                            assists=participant[12],
                            kills=participant[13],
                            gameDuration=participant[2])
            parties.append(P)
        return parties

#Exemple d'utilisation
"""
particip_dao = ParticipantDAO()
result = particip_dao.find_best_champ("Per_KDA")
print(result)
"""
"""
champion_name = "Sylas"
participant_dao = ParticipantDAO()
result = participant_dao.stat_champ_by_name(champion_name)
"""

particip_dao = ParticipantDAO()
result = particip_dao.getpartie("VIVE Serendrip")
print(result[0]._death)
