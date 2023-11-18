import sqlite3
from typing import List
from src.utils.singleton import Singleton
from src.dao.playerDAO import PlayerDAO


class ParticipantDAO(metaclass=Singleton):
    """
    Communicate with the participant table
    """

    def __init__(self, db_file='data/database.db'):

        """
        Initialize the class with the name of the SQLite database file.

        Parameters:
        db_file (str): Name of the SQLite database file.
        """
        self.db_file = db_file


    def find_best_champ(self, critere) -> List[str]:
        """
        Get all champions by a specified criteria and return a list

        :return: A list of statistics for champions
        :rtype: List of str
        """

        """
        Defining the criteria
        Per_game: Returns a list of total games played for champions
        Per_winrate: Returns a list of winrate for champions
        ... 
        """
        critere_affichage = ["Per_game", "Per_winrate", "Per_KDA",  "Per_gold", "Per_lane", "Per_other_stat"]
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if critere==critere_affichage[0]:   
            #List of champions ranked by popularity (total number of games played)
            query=  """ SELECT championName as Champion, COUNT(*) AS total_parties       
                        FROM participant                  
                        GROUP BY championName              
                        ORDER BY total_parties DESC   
                        """ 
            cursor.execute(query)
            results = cursor.fetchall()   # Retrieving query results
            return results

        #List of champions ranked by winrate (number of games won/number of games played)
        elif critere==critere_affichage[1]:
            query=  """SELECT championName, COUNT(*) AS total_parties, SUM(win) AS parties_gagnees, ROUND((SUM(win) * 1.0 / COUNT(*)),2)*100 AS winrate
                    FROM participant                                 
                    GROUP BY championName                             
                    ORDER BY winrate DESC                           
                    """
            cursor.execute(query)
            results = cursor.fetchall()   # Retrieving query results

            return results

        #Champions list in descending order of KDA (kills+assists)/deaths on all their games played
        elif critere==critere_affichage[2]:
            query= """SELECT championName , ROUND(AVG((kills + assists) / deaths), 2) AS kda
                    FROM participant 
                    GROUP BY championName 
                    ORDER BY kda DESC  
                """
            cursor.execute(query)       
            results = cursor.fetchall()   # Retrieving query results

            return results

        #List of champions in descending order of gold per minute per game
        elif critere==critere_affichage[3]:
            query= """ SELECT championName, ROUND(AVG(goldEarned / gameDuration),2) AS golds_per_minute
                    FROM participant
                    GROUP BY championName 
                    ORDER BY golds_per_minute DESC
                """
            cursor.execute(query)       
            results = cursor.fetchall()   # Retrieving query results
            
            return results

        #List of lanes in descending order of total games played per lane
        elif critere==critere_affichage[4]:
            query= """ SELECT lane, COUNT(*) AS total_parties, ROUND((SUM(win) * 1.0 / COUNT(*)),2)*100 AS winrate
                    FROM participant                                    
                    GROUP BY lane                                       
                    ORDER BY total_parties DESC                        
                    """
            cursor.execute(query)        
            results = cursor.fetchall()   # Retrieving query results

            return results
        
        #Champions list and their gold, totalminionkilled and descending order of total_games played
        elif critere==critere_affichage[5]:
            query=  """ SELECT championName, COUNT(*) AS total_parties, SUM(goldEarned) AS total_gold, SUM(totalMinionsKilled) AS total_minions_killed
                        FROM participant                                    
                        GROUP BY championName                               
                        ORDER BY total_parties DESC                      
                    """
            cursor.execute(query)       
            results = cursor.fetchall()   # Retrieving query results

            return results

    
    """
    Requesting the statistics of a champion given his name
    Statistics that are returned are: the champion's name, his total games played, winrate, kda and golds per minute
    """
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
        res = cursor.fetchone()           # Retrieving query results

        return res


    """
    The "getpartie" method displays all the games played by a player with statistics for each game, 
    including the champion's name, lane, game result (won or lost), kills, deaths, assists, 
    totalDamageDone and goldEarned/gameDuration.

    """

    def getpartie(self, player):
        """
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        puuid = PlayerDAO().find_player_by_name(player)._puuid
        print(puuid)
        query = """ SELECT championName, lane, win, kills, deaths, assists,
                            totalDamageDone, goldEarned/gameDuration
                    FROM participant
                    WHERE puuid = ?
                    LIMIT 10;
                    """

        cursor.execute(query, (puuid,))
        res = cursor.fetchall()           # Retrieving query results
        parties = []
        for participant in res:
            parties.append(participant)

        return res

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
print(result)

"""
"""
particip_dao = ParticipantDAO()
result = particip_dao.getpartie("VIVE Serendrip")
print(result)
"""

