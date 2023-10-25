from InquirerPy import prompt

from view.abstract_view import AbstractView
from view.session import Session


class ConnectionView(AbstractView):
    def __init__(self):
        self.__questions = [
            {
                "type": "input",
                "Identifiant": "login",
                "Mot de passe":"password"
                "message": "Enter your login and password",
            }
        ]

    def display_info(self):
        print(f"Hello, please enter your login and password")

    def make_choice(self):
        answers = prompt(self.__questions)
        Session().user_identifiant = answers["login"]
        Session().user_mdp = answers["password"]

        from view.start_view import StartView

        return memberView()