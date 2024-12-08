# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        vide = Command("", "cette commande ne fait rien", Actions.vide, 0)
        self.commands[""] = vide
        connexion = Command("connexion", "accéder au monde virtuel", Actions.connect, 0)
        self.commands["connexion"] = connexion
        
        # Setup rooms

        village_de_DASSA_baobab = Room("Forest", "dans une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        self.rooms.append(village_de_DASSA_baobab)
        labo_du_docteur = Room("Tower", "dans une immense tour en pierre qui s'élève au dessus des nuages.")
        self.rooms.append(labo_du_docteur)
        Grotte   = Room("Cave", "dans une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(Grotte)
        foret_sacrée = Room("Cottage", "dans un petit chalet pittoresque avec un toit de chaume. Une épaisse fumée verte sort de la cheminée.")
        self.rooms.append(foret_sacrée)
        arbre_voyageur = Room("Swamp", "dans un marécage sombre et ténébreux. L'eau bouillonne, les abords sont vaseux.")
        self.rooms.append(arbre_voyageur)
        village_de_Ganvié = Room("Castle", "dans un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(village_de_Ganvié)
        marche_flottant = Room("Tourciel","dans une tour au dessus des nuages.")
        self.rooms.append(marche_flottant)
        saule_pleureur = Room("Mondesouterrain","dans un monde souterrain en dessous du monde des humains.")
        self.rooms.append(saule_pleureur)
        chateau_de_madar = Room("Mondesouterrain","dans un monde souterrain en dessous du monde des humains.")
        self.rooms.append(chateau_de_madar)
        terrain_d_entrainement= Room("Mondesouterrain","dans un monde souterrain en dessous du monde des humains.")
        self.rooms.append(terrain_d_entrainement)
        salle_du_trone = Room("Mondesouterrain","dans un monde souterrain en dessous du monde des humains.")
        self.rooms.append(salle_du_trone)
        chambre_secrete_du_roi = Room("Mondesouterrain","dans un monde souterrain en dessous du monde des humains.")
        self.rooms.append(chambre_secrete_du_roi)
        # Create exits for rooms

        village_de_DASSA_baobab.exits = {"N" : Grotte, "E" : village_de_Ganvié, "S" : chateau_de_madar, "O" : foret_sacréé, "U" : None, "D" : None}
        labo_du_docteur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : None}
        Grotte.exits = {"N" : None, "E" : None, "S" : village_de_Dassa_baobab, "O" : None, "U" : None, "D" : None}
        foret_sacrée.exits = {"N" : None, "E" : village_de_Dassa_baobab, "S" : None, "O" : None, "U" : arbre_voyageur, "D" : None}
        arbre_voyageur.exits = {"N" : None, "E" : None, "S" : chateau_de_madar, "O" : None, "U" : None, "D" : foret_sacréé}
        village_de_Ganvié.exits = {"N" : saule_pleureur, "E" : marche_flottant, "S" : None, "O" : village_de_Dassa_baobab, "U" : None, "D" : None}
        marche_flottant.exits = {"N" : None, "E" : None, "S" : None, "O" : village_de_Ganvié, "U" : None, "D" : None}
        saule_pleureur.exits = {"N" : None, "E" : None, "S" : village_de_Ganvié, "O" : None, "U" : None, "D" : None}
        chateau_de_madar.exits = {"N" : None, "E" : chambre_secrete_du_roi, "S" : salle_du_trone, "O" : terrain_d_entrainement, "U" : None, "D" : None}
        terrain_d_entrainement.exits = {"N" : None, "E" : chateau_de_madar, "S" : None, "O" : None, "U" : None, "D" : None}
        salle_du_trone.exits = {"N" : chateau_de_madar, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        chambre_secrete_du_roi.exits = {"N" : None, "E" : None, "S" : None, "O" : chateau_de_madar, "U" : None, "D" : None}



        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = labo_du_docteur 

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
