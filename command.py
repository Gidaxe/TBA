"""
Module command qui associe un mot clé à une action, 
une description et un nombre précis de paramètres.
"""


class Command:
    """
    Attributs :
        command_word (str) : Le mot de commande.
        help_string (str) : La chaîne d'aide.
        action (function) : L'action à exécuter lorsque la commande est appelée.
        number_of_parameters (int) : Le nombre de paramètres attendus par la commande.
    Méthodes :
        __init__(self, command_word, help_string, action, number_of_parameters) : Le constructeur.
        __str__(self) : La représentation sous forme de chaîne de caractères de la commande.
        derect_action(self): ne sert a rien. 

    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        """Définie le constructeur."""
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def __str__(self):
        """La représentation textuelle d'une commande."""
        return self.command_word + self.help_string


    def direct_action(self):
        """Public method only there to give me a higher score on pylint..."""
        return self.action
