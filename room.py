import random as rd
import character as chara
#from game import DEBUG
# Define the Room class.

class Room:
    """
    Represents a room in the game.

    A Room object defines a location in the game world, with a name, a description, and exits leading to other rooms.

    Attributes:
        name (str): The name of the room.
        description (str): A brief description of the room.
        exits (dict): A dictionary mapping directions (str) to neighboring rooms (Room or None).

    Methods:
        __init__(name, description):
            Initializes a Room instance with a name, a description, and no exits.
       
        get_exit(direction):
            Returns the room in the given direction if it exists.
       
        get_exit_string():
            Returns a string describing all available exits from the room.
       
        get_long_description():
            Returns a detailed description of the room, including its description and available exits.

    Examples:
        >>> kitchen = Room("Kitchen", "A cozy kitchen with a fireplace.")
        >>> hallway = Room("Hallway", "A narrow hallway.")
        >>> kitchen.exits = {"north": hallway}
        >>> hallway.exits = {"south": kitchen}

        >>> print(kitchen.get_exit_string())
        Exits: north

        >>> kitchen.get_exit("north")
        <Room object representing 'Hallway'>

        >>> print(kitchen.get_long_description())
        A cozy kitchen with a fireplace.
        Exits: north

        >>> kitchen.get_exit("west") is None
        True
    """

    entities = {} #dictionnaire: {nom_de_la_room:[entitées de la room]}

    # Define the method class to update the entities in the room
    @classmethod
    def refresh_room_allies(cls):
        #faire en sorte qu'a chaque déplacement du joueur les npc qui ne le follow ont une chance de se déplacer de façon random
        followers = chara.Character.followers
        for ent in followers:
            entity = followers[ent]
            entity.follow_player(entity.leader)


    @classmethod
    def refresh_room_enemies(cls, player, game):
        room = player.current_room
        ennemis = [entity for entity in room.room_entities if entity.ennemi]
        power = 25
        if not player.invisible:
            for ennemi in ennemis:
                player.HP -= power
                if player.HP < 0:
                    player.HP = 0
                print(f"\nPlayer: {player.name} vient de perdre {power}HP")
                print(f"Il vous reste: {player.HP}HP")
                if player.HP == 0:
                    print(f"\n{player.name} a été vaicu !")
                    player.death(ennemi)
                    game.finished = True
                    return True


    # Define the constructor. 
    def __init__(self, name, description, lacustre = False, solo = False):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.lacustre = lacustre
        self.solo = solo
        Room.entities[self.name] = []
        self.room_entities = Room.entities[self.name]

    #Define the string representation of a room
    def __str__(self):
        return self.name
    
    # Define the get_exit method.
    def get_exit(self, direction):
        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        self.get_entities(True)
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
    
    #Define the get_inventroy method
    def get_inventory(self):
        if len(self.inventory) > 0:
            print("\nLa pièce contient :")
            for key in self.inventory.keys():
                if self.inventory[key] != None:
                    print(f"\n\t- {self.inventory[key]}")
        else:
            print("\nIl n'y a aucun objet ici.")

    #Define the get_entity method returns either the entity's id, their index in the room they are in or the entity itself (Character instance).
    def get_entity(self, name, id=None, room_index=None):
        cmpt = 0
        for i in range(len(self.room_entities)):
            if self.room_entities[i].name == name:
                ent = self.room_entities[i]
                index = i
                cmpt += 1
                break
        if cmpt<1:
            print(f"il n'y a pas de {name} dans cette pièce !")
            return None
        if id:
            return ent.id
        elif room_index:
            return index
        else:
            return ent

    #Define the get_entities method
    def get_entities(self, show = False):
        if show:
            print(f"\nLes entités autour de vous sont:")
            for entity in self.room_entities:
                if entity.id != 1: #identifiant du joueur
                    print(f"\n\t-{entity}")
         