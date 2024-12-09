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
        vide = Command("", " : cette commande ne fait rien", Actions.vide, 0)
        self.commands[""] = vide
        connexion = Command("connexion", " : accéder au monde virtuel", Actions.connexion, 0)
        self.commands["connexion"] = connexion
        back = Command("back", " : cette commande permet au joueur de retourner à sa dernière destination.", Actions.back, 0)
        self.commands["back"] = back
        
        # Setup rooms

        labo_du_docteur = Room("Labo", "dans le laboratoire du docteur madarrrrrrrrrr.")
        self.rooms.append(labo_du_docteur)
        village_de_DASSA_baobab = Room("village de DASSA", "dans le village de DASSA.\n Plus précisement sous le baobab du village, autour de vous des cases en argiles avec des toits en pailles")
        self.rooms.append(village_de_DASSA_baobab)
        Grotte   = Room("Grotte", "dans une grotte sombre avec des chauves souris et des serpents.")
        self.rooms.append(Grotte)
        foret_sacrée = Room("foret sacrée", "dans la foret sacré à l'interieur du temple au python, ce temple etait dans le passé un lieu de culte au dieux, autour de vous des ossements humains et des statues.")
        self.rooms.append(foret_sacrée)
        arbre_voyageur = Room("Arbre voyageur", "sur un arbre particulier qui a la capacité de vous téléporté à des endroits précis .")
        self.rooms.append(arbre_voyageur)
        village_de_Ganvié = Room("village de ganvié", "à l'ambarcadaire du village de ganvié, autour de vous il y a des bes cannots et des femmes qui vendent du poisson.")
        self.rooms.append(village_de_Ganvié)
        marche_flottant = Room("Tourciel","sur le marché flottant du village de ganvié, ce marché est assez particulier il a été crée par les dieux et vous pouvez y trouver des objets magiques.")
        self.rooms.append(marche_flottant)
        saule_pleureur = Room("saule pleureur","sous le saule pleureur.")
        self.rooms.append(saule_pleureur)
        chateau_de_madar = Room("chateau de madar","dans le chateau de madar, un immense chateau peu éclairé.")
        self.rooms.append(chateau_de_madar)
        terrain_d_entrainement= Room("terrain d'entrainement","sur le terrain d'entrainnement des agojié, les soldat d'élites du Roi Madarrrrrr.")
        self.rooms.append(terrain_d_entrainement)
        salle_du_trone = Room("Salle du trone","dans la salle du trone de madar.")
        self.rooms.append(salle_du_trone)
        chambre_secrete_du_roi = Room("chambre secrète","dans la chambre secrète de madar, cette pièce contient de nombreux secrets dont la solution pour sortir du jeu.")
        self.rooms.append(chambre_secrete_du_roi)
        # Create exits for rooms

        village_de_DASSA_baobab.exits = {"N" : Grotte, "E" : village_de_Ganvié, "S" : chateau_de_madar, "O" : foret_sacrée, "U" : None, "D" : None}
        labo_du_docteur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : None}
        Grotte.exits = {"N" : None, "E" : None, "S" : village_de_DASSA_baobab, "O" : None, "U" : None, "D" : None}
        foret_sacrée.exits = {"N" : None, "E" : village_de_DASSA_baobab, "S" : None, "O" : None, "U" : arbre_voyageur, "D" : None}
        arbre_voyageur.exits = {"N" : None, "E" : None, "S" : chateau_de_madar, "O" : None, "U" : None, "D" : foret_sacrée}
        village_de_Ganvié.exits = {"N" : saule_pleureur, "E" : None, "S" : None, "O" : village_de_DASSA_baobab, "U" : marche_flottant, "D" : None}
        marche_flottant.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : village_de_Ganvié}
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
