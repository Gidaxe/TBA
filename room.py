"""Module gérant la classe Room et ses interactions avec les entités du jeu."""

import character as chara


# Define the Room class.
class Room:
    """
    Represents a room in the game.

    A Room object defines a location in the game world, with a name, a description, and exits.

    Attributes:
        name (str): The name of the room.
        description (str): A brief description of the room.
        exits (dict): A dictionary mapping directions (str) to neighboring rooms (Room or None).

    Methods:
        __init__(name, description, lacustre=False, solo=False):
            Initializes a Room instance with a name, a description, and specific flags
            indicating if it's a lacustre or a solo room.

        get_exit(direction):
            Returns the room in the given direction if it exists.

        get_exit_string():
            Returns a string describing all available exits from the room.

        get_long_description():
            Returns a detailed description of the room, including its description
            and available exits.

        get_inventory():
            Displays items in the current room's inventory.

        get_entity(name, id=None, room_index=None):
            Retrieves a specific entity in the room by name (and optionally by ID or index).

        get_entities(show=False):
            Returns a list of all entities in the room, optionally displaying them.
    """

    entities = {}  # dictionnaire: {nom_de_la_room:[entitées de la room]}

    # Define the class class to update the allies in the room
    @classmethod
    def refresh_room_allies(cls):
        """Met à jour la position des alliés en les faisant suivre leur leader, s’il y en a."""
        followers = chara.Character.followers
        for follower in followers.values():
            follower.follow_player(follower.leader)

    # Define class method to get ennemies attacks
    @classmethod
    def refresh_room_enemies(cls, game):
        """Gère l’attaque des ennemis dans la salle et vérifie l’état de la partie.

        Args:
            game (Game): L’instance de la classe Game en cours, qui contient
                les informations sur le joueur et l’état général du jeu.

        Returns:
            bool: True si aucune autre action d’ennemi n’est nécessaire ou si le joueur
            est rendu invisible ou si la salle est vide d’ennemis. Sinon, gère la défaite
            du joueur.
        """
        player = game.player
        room = player.current_room
        ennemis = [entity for entity in room.room_entities if entity.ennemi]
        if game.antagoniste.dead:
            game.win = True
            game.finished = True
        if not ennemis:
            return True
        if player.invisible and not room.solo:
            return True
        power = ennemis[0].power
        for ennemi in ennemis:
            player.hp -= power
            player.hp = max(player.hp, 0)
            print(f"\nPlayer: {player.name} vient de perdre {power}HP")
            print(f"Il vous reste: {player.hp}HP")
            if player.hp == 0:
                print(f"\n{player.name} a été vaicu !")
                player.death(ennemi)
                game.finished = True
        return True

    # Define the constructor.
    def __init__(self, name, description, lacustre=False, solo=False):
        """Initialise une nouvelle salle avec un nom, une description et des drapeaux spéciaux."""
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.lacustre = lacustre
        self.solo = solo
        Room.entities[self.name] = []
        self.room_entities = Room.entities[self.name]

    # Define the string representation of a room
    def __str__(self):
        """Retourne le nom de la salle lorsqu’elle est convertie en chaîne de caractères."""
        return self.name

    # Define the get_exit method.
    def get_exit(self, direction):
        """Retourne la salle située dans la direction spécifiée.

        Args:
            direction (str): La direction dans laquelle chercher la prochaine salle.

        Returns:
            Room or None: La salle correspondante si elle existe, sinon None.
        """
        # Return the room in the given direction if it exists.
        if direction in self.exits:
            return self.exits[direction]

        return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        """Retourne une chaîne de caractères listant toutes les sorties disponibles de la salle.

        Returns:
            str: Les directions disponibles (ex: "Sorties: N, E, S").
        """
        exit_string = "Sorties: "
        for sortie in self.exits:
            if self.exits.get(sortie) is not None:
                exit_string += sortie + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        """Retourne la description complète de la salle, incluant ses sorties et entités.

        Returns:
            str: La description détaillée de la salle et la liste de ses sorties.
        """
        self.get_entities(True)
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    # Define the get_inventroy method
    def get_inventory(self):
        """Affiche les objets disponibles dans l’inventaire de la salle, s’il y en a."""
        if len(self.inventory) > 0:
            print("\nLa pièce contient :")
            for value in self.inventory.values():
                if value is not None:
                    print(f"\n\t- {value}")
        else:
            print("\nIl n'y a aucun objet ici.")

    # Define the get_entity method returns either the entity's id,
    # their index in the room they are in or the entity itself (Character instance).
    def get_entity(self, name, identifiant=None, room_index=None):
        """Recherche et retourne l’entité correspondant au nom dans la salle.

        Args:
            name (str): Le nom de l’entité à chercher.
            id (bool, optional): Si True, retourne seulement l’identifiant de l’entité.
            room_index (bool, optional): Si True, retourne l’index de l’entité dans la liste.

        Returns:
            Character or int or None: L’instance de l’entité, son ID, ou son index selon
            les paramètres. Retourne None si l’entité n’est pas trouvée.
        """
        cmpt = 0
        for i in range(len(self.room_entities)):
            if self.room_entities[i].name == name:
                ent = self.room_entities[i]
                index = i
                cmpt += 1
                break
        if cmpt < 1:
            print(f"il n'y a pas de {name} dans cette pièce !")
            return None
        if identifiant:
            return ent.identifiant
        if room_index:
            return index

        return ent

    # Define the get_entities method
    def get_entities(self, show=False):
        """Retourne la liste des entités se trouvant dans la salle, avec option d’affichage.

        Args:
            show (bool, optional): Si True, affiche les entités non-joueur présentes.

        Returns:
            list: Liste des entités présentes dans la salle.
        """
        if show:
            print("\nLes entités autour de vous sont:")
            for entity in self.room_entities:
                if entity.id != 1:  # identifiant du joueur
                    print(f"\n\t-{entity}")
        return self.room_entities
