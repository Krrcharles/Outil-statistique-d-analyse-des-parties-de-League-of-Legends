import os
import dotenv
from src.view.start_view import StartView
from data.creer_db import creer_database
from data.fill_database import fill

# This script is the entry point of your application

if __name__ == "__main__":
    dotenv.load_dotenv(override=True)
    
    #si l'utilisateur lance l'application pour la première fois
    #il n'a pas de DB de constitué et donc il faut l'initaliser
    #pour le moment j'admet que ca marche psk ca marche quand je teste a la main
    if not os.path.exists(os.path.exists(os.path.join(os.getcwd(),'databse.db'))):
        creer_database()
        fill()
    
    # run the Start View
    current_view = StartView()

    # while current_view is not none, the application is still running
    while current_view:
        # a border between view
        with open("src/graphical_assets/border.txt", "r", encoding="utf-8") as asset:
            print(asset.read())
        # Display the info of the view
        current_view.display_info()
        # ask user for a choice
        current_view = current_view.make_choice()

    with open(
        "src/graphical_assets/defeat.txt", "r", encoding="utf-8"
    ) as asset:
        print(asset.read())
