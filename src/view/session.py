from src.utils.singleton import Singleton


class Session(metaclass=Singleton):
    def __init__(self):
        """
        Définition des variables que l'on stocke en session
        Le syntaxe
        ref:type = valeur
        permet de donner le type des variables. Utile pour l'autocompletion.
        """
        self.user_identifiant: str = "unknown"
        self.user_mdp: str = "unknown"
        self.not_admin: str = "yes"