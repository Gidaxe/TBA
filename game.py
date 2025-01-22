# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

DEBUG = False

WIN = '''

 _       _______   ___   ____________     __
| |     / /  _/ | / / | / / ____/ __ \   / /
| | /| / // //  |/ /  |/ / __/ / /_/ /  / / 
| |/ |/ // // /|  / /|  / /___/ _, _/  /_/  
|__/|__/___/_/ |_/_/ |_/_____/_/ |_|  (_)   
                                            
'''

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.win = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.antagoniste = None
    
    # Setup the game
    def setup(self):


        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D, NE, NO, SE, SO)", Actions.go, 1)
        vide = Command("", " : cette commande ne fait rien", Actions.vide, 0)
        connexion = Command("connexion", " : accéder au monde virtuel", Actions.connexion, 0)
        back = Command("back", " : cette commande permet au joueur de retourner à sa dernière destination.", Actions.back, 0)
        look = Command("look", " : regarder quels objets sont dans la salle", Actions.look, 0)
        take = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        drop = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        check = Command("check", " : observer son inventaire", Actions.check, 0)
        history = Command("history", " : observer son historique", Actions.history, 0)
        items = Command("items", " : lister tous les objets presents dans le jeu", Actions.items, 0)
        beam = Command("beam", " : se téléporter dans un endroit déjà visité au moins une fois.", Actions.beam, 0)
        lead = Command("lead", " <direction> <PNJ> || <lock/unlock> <PNJ> : se déplacer d'une salle a l'autre avec un npc", Actions.lead, 2)
        talk = Command("talk", " <PNJ> : parler avec une personne", Actions.talk, 1)
        use = Command("use", " <objet> : utiliser un objet", Actions.use, 1)


        self.commands["help"] = help
        self.commands["quit"] = quit
        self.commands["connexion"] = connexion
        self.commands["look"] = look
        self.commands["talk"] = talk
        self.commands["lead"] = lead
        self.commands["take"] = take
        self.commands["use"] = use
        self.commands["drop"] = drop
        self.commands["check"] = check
        self.commands["go"] = go
        self.commands["back"] = back
        self.commands["history"] = history
        self.commands["beam"] = beam
        self.commands["items"] = items
        self.commands[""] = vide
        
        
        # Setup rooms
        labo_du_docteur = Room("Labo", "dans le laboratoire du docteur madar, il revient bientot. Vite connectez-vous à son jeu si vous voulez survivre !.")
        Grotte   = Room("Grotte", "dans une grotte sombre avec des chauves souris et des serpents.")
        village_de_DASSA_baobab = Room("village de DASSA", "dans le village de DASSA, le lieu où repose l'épée ancestrale de votre clan et où vivent vos frères. Sans leur soutien, vous ne pourrez accomplir votre destinée. \nC'est ici que tout commence !")
        
        chateau_de_madar = Room("chateau de madar","dans le chateau de madar, un immense chateau peu éclairé.")
        terrain_d_entrainement= Room("terrain d'entrainement","sur le terrain d'entrainnement des agojié, les soldat d'élites du Roi Madarrrrrr.")
        salle_du_trone = Room("Salle du trone","dans la salle du trone de madar.", solo=True)
        chambre_secrete_du_roi = Room("chambre secrète","dans la chambre secrète de madar, cette pièce contient de nombreux secrets dont la solution pour sortir du jeu.", solo=True)

        village_de_Ganvié = Room("village de ganvié", "à l'ambarcadaire du village de ganvié, autour de vous il y a des bes cannots et des femmes qui vendent du poisson. \nMais ne baissez surtout pas votre garde, les sbires de Madar sont partout !", True)
        marche_flottant = Room("Marché flottant","sur le marché flottant du village de ganvié, ce marché est assez particulier il a été crée par les dieux et vous pouvez y trouver des objets magiques.", True)
        saule_pleureur = Room("saule pleureur","sous le saule pleureur, en plein dans le repere de Mami Wata", True)

        foret_sacrée = Room("foret sacrée", "dans la foret sacré à l'interieur du temple au python", True)
        arbre_voyageur = Room("Arbre voyageur", "sur un arbre particulier qui a la capacité de vous téléporté (beam) n'importe quel endroit dans ce monde pourvu que vous l'ayez déjà visité au moins une fois.")
        
        self.rooms.append(labo_du_docteur)
        self.rooms.append(Grotte)
        self.rooms.append(village_de_DASSA_baobab)

        self.rooms.append(chateau_de_madar)
        self.rooms.append(terrain_d_entrainement)
        self.rooms.append(salle_du_trone)
        self.rooms.append(chambre_secrete_du_roi)
        
        self.rooms.append(village_de_Ganvié)
        self.rooms.append(marche_flottant)
        self.rooms.append(saule_pleureur)

        self.rooms.append(foret_sacrée)
        self.rooms.append(arbre_voyageur)
        

        # Create exits for rooms
        labo_du_docteur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : None}
        Grotte.exits = {"N" : None, "E" : None, "S" : village_de_DASSA_baobab, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        village_de_DASSA_baobab.exits = {"N" : Grotte, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None, "NE": None,"NO": None, "SE": village_de_Ganvié, "SO": chateau_de_madar}
        
        chateau_de_madar.exits = {"N" : None, "E" : None, "S" : None, "O" : terrain_d_entrainement, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        terrain_d_entrainement.exits = {"N" : None, "E" : chateau_de_madar, "S" : salle_du_trone, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        salle_du_trone.exits = {"N" : None, "E" : None, "S" : chambre_secrete_du_roi, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        chambre_secrete_du_roi.exits = {"N" : salle_du_trone, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}

        village_de_Ganvié.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": village_de_DASSA_baobab, "SE": None, "SO": None}
        marche_flottant.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None, "D" : None, "NE": None,"NO": None, "SE": None, "SO": None}
        saule_pleureur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None,  "NE": None,"NO": None, "SE": None, "SO": None}

        foret_sacrée.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : arbre_voyageur, "D" : None, "D" : None, "NE": None ,"NO": None, "SE": None, "SO": None}
        arbre_voyageur.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : foret_sacrée,"NE": None,"NO": None, "SE": None, "SO": None}
        
        

        # Setup room entities
        Atchede = Character("Atchede", 9, "votre frère ainé", village_de_DASSA_baobab, {"salut":"Salut mon frère", "j'ai besoin de ton aide":"Tout pour toi mon frère, que dois-je faire?","Accompagne moi dans ma quête pour vaicre le maléfique Mansa Madar !":"Biensur !", "Saurais-tu où trouver de puissants artefactes ?":"Tu devrais prendre l'épée du clan avec toi, elle te sera très utile ! Pour le reste on peut aller a Ganvier au Sud Est (SE) d'ici afin de demander plus d'informations."})
        Kacou = Character("Kacou", 5, "votre frère cadet", village_de_DASSA_baobab, {"salut":"Salut mon frère", "j'ai besoin de ton aide":"Tout pour toi mon frère, que dois-je faire?","Accompagne moi dans ma quête pour vaicre le maléfique Mansa Madar !":"Biensur ! ", "Saurais-tu où trouver de puissants artefactes ?":"Tu devrais prendre l'épée du clan avec toi, elle te sera très utile ! Pour le reste on peut aller a Ganvier au Sud Est (SE) d'ici afin de demander plus d'informations."})
        mami_watta = Character("mami_watta", 7, "esprit des eaux", saule_pleureur, {"salut":"qui es tu humain?", "Asnaem":"Qu'avons nous là ? \nL'élu est enfin arrivé, \net il s'est enfin décidé à me rendre visite ? \nDis moi 'Asnaem' que désires tu vraiment?", "retourner dans mon monde":"Alors tu sais ce qui t'attends, tu vas devoir devenir assez fort pour vaincre Madar et ses soldat mais saches que bien de vaillants guerriers et rois ont déjà essayé, sans succès. Ce démon à réussi à vaincre une alliance formée par tous les Obas du YOROUBA-LAND et à même tué des Orishas dont mes chers amis Anansi et Ogun...","Ais-je vraiment une chance de le vaincre ?":"\nJe ne sais pas mais en attendant tu peux t'entrainer avec le sorcier de la forêt sacrée pour te préparer... J'ai aussi un cadeau pour toi","Que peux-tu m'apporter ?": "Pour le bon prix je peux t'offrir l'oeil magique qui te permettra de trouver la faiblesse de Madar"}, False, True)
        pecheur = Character("pecheur", 21, "un simple pecheur",village_de_Ganvié, {"salut": "salut", "je cherche où acheter des objets magiques":"Vous en trouverez surement au marché flottant, pour vous y rendre, vous devez embarquer sur un bateau magique et lui dire où vous souhaitez aller.","Où trouver un bateau magique ?": "J'en vent justement !","merci !": " de rien"}, False, True)
        marchand = Character("marchand", 19, " vendeur d'objets magique",marche_flottant, {"salut": "salut jeune homme", "je veux un objet magique puissant": "j'ai plusieurs objets dont une potion magique, un menteau d'invisibilité, des gants et un sac à dos ma foi vachement stylé !"}, False, True)
        Madar = Character("Madar", 13, "version virtuelle du concepteur de ce monde", salle_du_trone, {"c'est toi madar?": "oui", "je vais te vaincre pour retrouver mon monde":"essaie pour voir enfant !"}, False, False, True)
        le_sage_du_village = Character("le_sage",12,"du haut de ses 120 ans il connait tout les secrets de ce monde", Grotte, {"salut":"Bienvenu mon enfant, tu es le héro de la légende, celui qui prendra le nom d'Asnaem et délivrera le ROYAUME DU DAHOMEY tout entier des griffes de Mansa Madar !", "Comment puis-je sortir de ce monde ?": "Pour sortir de ce monde tu va devoir vaincre madar qui est celui qui l'a crée, et le dirige d'une main de fer !", "Comment faire ?":"Constitue toi une équipe de puissants et fidèles alliés, trouves les artefactes les plus puissants de ce monde. \nMais surtout garde un coeur pur et résiliant face à l'adversité, c'est seulement ainsi que tu viendras à bout du puissant Mansa Madarrrr !!!"}, False)
        le_sorcier= Character("le_sorcier",23, "sorcier chargé de la formation des gueriers dans le temple",foret_sacrée, {"salut":"salut les jeunes !","Entraine nous !":"Biensur !","Merci beaucoup":"Ce fut un plaisir jeune Asnaem, je te souhaite bonne fortune pour ta bataille finale !", "Connais-tu un raccourci pour aller au chateau de Madar ?":"Monte (U) l'escalier des Orishas et tu arriveras à l'arbre du voyageur, il te donnera accès à tous les coins de ce monde."}, False)        
        sbire_de_madar1 = Character("Guerrier_de_Madar", 38, "Guerrier masqué venu vous éliminé sous les ordres de son roi Mansa Madar !", village_de_Ganvié, {"salut":"MEUURRRRRRTTT !!!!!"}, False, False, True)
        sbire_de_madar2 = Character("Assassin_de_Madar", 40, "Assassin masqué venu vous éliminé sous les ordres de son roi Mansa Madar !", village_de_Ganvié, {"salut":"MEUURRRRRRTTT !!!!!"}, False, False, True)
        agojié1 = Character("Agojié1", 51, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)
        agojié2 = Character("Agojié2", 54, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)
        agojié3 = Character("Agojié3", 56, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)
        agojié4 = Character("Agojié4", 58, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)
        agojié5 = Character("Agojié5", 60, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)
        agojié6 = Character("Agojié6", 63, "Guerrière féroce férocement loyale à Madar !", terrain_d_entrainement, {"salut":"Pour sa majestéééééé !!!!!"}, False, False, True)


        Room.entities[village_de_DASSA_baobab.name].append(Atchede)
        Room.entities[village_de_DASSA_baobab.name].append(Kacou)
        Room.entities[saule_pleureur.name].append(mami_watta)
        Room.entities[village_de_Ganvié.name].append(pecheur)
        Room.entities[marche_flottant.name].append(marchand)
        Room.entities[salle_du_trone.name].append(Madar)
        Room.entities[Grotte.name].append(le_sage_du_village)
        Room.entities[foret_sacrée.name].append(le_sorcier)
        Room.entities[village_de_Ganvié.name].append(sbire_de_madar1)
        Room.entities[village_de_Ganvié.name].append(sbire_de_madar2)
        Room.entities[terrain_d_entrainement.name].append(agojié1)
        Room.entities[terrain_d_entrainement.name].append(agojié2)
        Room.entities[terrain_d_entrainement.name].append(agojié3)
        Room.entities[terrain_d_entrainement.name].append(agojié4)
        Room.entities[terrain_d_entrainement.name].append(agojié5)
        Room.entities[terrain_d_entrainement.name].append(agojié6)


        # Setup room inventories
        sword = Item("sword", 0, "Une épée au fil tranchant comme un rasoir:\n\t\t_-50HP de dégats +50% par alliés qui décident de vous suivre !", 4)
        shield = Item("shield", 1, "Bouclier pouvant parrer n'importe quelle attaque:\n\t\t_+250HP", 6)
        map = Item("map", 2, "Carte magique permettant de vous repérer dans le monde et meme sous certaines conditions de vous téléporter !!!", 2)
        boat = Item("boat", 4, "Bateau pour traverser n'importe quelle étendu d'eau", 15)
        oeil_magique = Item("oeil", 11, "Oeil magique ayant une fois appartenu a l'épervier de ganvié, il peut tout voir, nul mystere ne lui échappe !", 1)
        menteau_d_invisibilité = Item("menteau_d_invisibilité", 13, "Menteau mythique fait par le grand marabou du nord lui-même !", 4)
        gants = Item("gants", 7, "Ce gants augmente la puissance de son utilisateur", 3)
        potion_magique = Item("potion_magique", 8, "Potions permettant de retrouver sa vigueur:\n\t\t_+100HP par utilisation\n\t\t_x25 Utilisations", 2)
        sac_a_dos = Item("Sac", 17,"Sac à dos en peau de lion, ultra résistant esthétique !:\n\t\t_+50kg de capacité de charge", -50)

        village_de_DASSA_baobab.inventory["sword"] = sword
        foret_sacrée.inventory["shield"] = shield 
        pecheur.inventory["boat"] = boat
        arbre_voyageur.inventory["map"] = map
        mami_watta.inventory["oeil"] = oeil_magique
        marchand.inventory["menteau_d_invisibilité"] = menteau_d_invisibilité
        marchand.inventory["gants"] = gants
        marchand.inventory["potion_magique"] = potion_magique
        marchand.inventory["sac_a_dos"] = sac_a_dos


        # Setup player et de l'antagoniste
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = labo_du_docteur 
        Madar.invincible = False
        Madar.power = 75
        Madar.HP = 555
        self.antagoniste = Madar

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            Room.refresh_room_enemies(self)
        if self.win:
            print(WIN)
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
