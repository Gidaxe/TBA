# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

DEBUG = False

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
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D, NE, NO, SE, SO)", Actions.go, 1)
        self.commands["go"] = go
        vide = Command("", " : cette commande ne fait rien", Actions.vide, 0)
        self.commands[""] = vide
        connexion = Command("connexion", " : accéder au monde virtuel", Actions.connexion, 0)
        self.commands["connexion"] = connexion
        back = Command("back", " : cette commande permet au joueur de retourner à sa dernière destination.", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder quels objets sont dans la salle", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : observer son inventaire", Actions.check, 0)
        self.commands["check"] = check
        items = Command("items", " : lister tous les objets presents dans le jeu", Actions.items, 0)
        self.commands["items"] = items
        beam = Command("beam", " : se téléporter dans un endroit déjà visité au moins une fois.", Actions.beam, 0)
        self.commands["beam"] = beam
        lead = Command("lead", " <direction> <PNJ> || <lock/unlock> <PNJ> : se déplacer d'une salle a l'autre avec un npc", Actions.lead, 2)
        self.commands["lead"] = lead
        talk = Command("talk", " <PNJ> : parler avec une personne", Actions.talk, 1)
        self.commands["talk"] = talk
        use = Command("use", " <objet> : utiliser un objet", Actions.use, 1)
        self.commands["use"] = use

        
        # Setup rooms

        labo_du_docteur = Room("Labo", "dans le laboratoire du docteur madarrrrrrrrrr.")
        self.rooms.append(labo_du_docteur)
        village_de_DASSA_baobab = Room("village de DASSA", "dans le village de DASSA.")
        self.rooms.append(village_de_DASSA_baobab)
        Grotte   = Room("Grotte", "dans une grotte sombre avec des chauves souris et des serpents.")
        self.rooms.append(Grotte)
        foret_sacrée = Room("foret sacrée", "dans la foret sacré à l'interieur du temple au python")
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

        village_de_DASSA_baobab.exits = {"N" : Grotte, "E" : None, "S" : chateau_de_madar, "O" : None, "U" : None, "D" : None, "NE": None,"NO": None, "SE": village_de_Ganvié, "SO": None}
        labo_du_docteur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : None}
        Grotte.exits = {"N" : None, "E" : None, "S" : village_de_DASSA_baobab, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        foret_sacrée.exits = {"N" : None, "E" : village_de_Ganvié, "S" : None, "O" : None, "U" : arbre_voyageur, "D" : None, "D" : None, "NE": None ,"NO": None, "SE": None, "SO": None}
        arbre_voyageur.exits = {"N" : None, "E" : None, "S" : chateau_de_madar, "O" : None, "U" : None, "D" : foret_sacrée,"NE": None,"NO": None, "SE": None, "SO": None}
        village_de_Ganvié.exits = {"N" : saule_pleureur, "E" : None, "S" : None, "O" : None, "U" : marche_flottant, "D" : None, "D" : None, "NE": None,"NO": village_de_DASSA_baobab, "SE": None, "SO": None}
        marche_flottant.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : village_de_Ganvié, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        saule_pleureur.exits = {"N" : None, "E" : None, "S" : village_de_Ganvié, "O" : None, "U" : None, "D" : None,  "NE": None,"NO": None, "SE": None, "SO": None}
        chateau_de_madar.exits = {"N" : None, "E" : chambre_secrete_du_roi, "S" : salle_du_trone, "O" : terrain_d_entrainement, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        terrain_d_entrainement.exits = {"N" : None, "E" : chateau_de_madar, "S" : None, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        salle_du_trone.exits = {"N" : chateau_de_madar, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        chambre_secrete_du_roi.exits = {"N" : None, "E" : None, "S" : None, "O" : chateau_de_madar, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}

        # Setup room inventories
        sword = Item("sword", 0, "une épée au fil tranchant comme un rasoir", 4)
        shield = Item("shield", 1, "bouclier pouvant parrer n'importe quelle attaque", 6)
        map = Item("map", 2, "carte magique permettant de vous repérer dans le monde et meme sous certaines conditions de vous téléporter !!!", 2)
        boat = Item("boat", 4, "bateau pour traverser n'importe quelle étendu d'eau", 3)
        oeil_magique = Item("oeil", 11, "Oeil magique ayant une fois appartenu a l'épervier de ganvié, il peut tout voir, nul mystere ne lui échappe !", 1)
        menteau_d_invisibilité = Item("menteau_d_invisibilité", 13, "menteau mythique fait de peau de lion", 4)
        gants = Item("gants", 7, "ce gants augmente la puissance de son utilisateur", 3)


        marche_flottant.inventory["sword"] = sword
        marche_flottant.inventory["shield"] = shield
        village_de_Ganvié.inventory["boat"] = boat
        arbre_voyageur.inventory["map"] = map
        saule_pleureur.inventory["oeil"] = oeil_magique
        foret_sacrée.inventory["menteau_d_invisibilité"]=menteau_d_invisibilité
        foret_sacrée.inventory["gants"]=gants 

        # Setup room entities
        Atchede = Character("Atchede", 9, "votre frère ainé", village_de_DASSA_baobab, {"salut":"Salut mon frère", "vous allez m'aider dans ma quete":"que devons nous faire?","vaincre madaar":"d'accord !"})
        Kacou = Character("Kacou", 5, "votre frère cadet", village_de_DASSA_baobab, {"salut":"Salut mon frère","vous allez m'aider dans ma quete":"que devons nous faire?","vaincre madaar":"d'accord !"})
        mami_watta = Character("mami watta", 7, "esprit des eaux", saule_pleureur,{"salut":"qui es tu humain?", "Asnaem":"et que veux tu ?", "retourner dans mon monde":"pour ce faire cela ne sera pas simple, tu vas devoir etre assez fort pour vaincre madar et ses soldat mais pas que il te faudras aussi des objets magique que tu pourras trouver dans la foret sacrée...en attendant j'ai un cadeau pour toi"})
        
         
        Room.entities[village_de_DASSA_baobab.name].append(Atchede)
        Room.entities[village_de_DASSA_baobab.name].append(Kacou)
        Room.entities[saule_pleureur.name].append(mami_watta)

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
            #self.player.current_room.refresh_room_entities()
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
    #npc powered by chatgpt
    #interace graphique
    #carte en ascii
    #Nom du jeu en ascii
    #mouvements aléatoire des npc
    #fonction attaque et défense
    

if __name__ == "__main__":
    main()
