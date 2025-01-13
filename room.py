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

    entities = {}

    # Define the method class to update the entities in the room
    @classmethod
    def refresh_room_entities(cls, entity, old_room, new_room):
        ents =Room.entities[old_room.name]
        n = len(ents)
        for i in range(n):
            if ents[i] == entity:
                ents.pop(i)
                break
        Room.entities[new_room.name].append(entity)

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        Room.entities[self.name] = []
    
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
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
    
    #Define the get_inventroy method
    def get_inventory(self):
        if len(self.inventory) > 0:
            print("\nLa pièce contient :")
            for key in self.inventory.keys():
                if self.inventory[key] != None:
                    print(f"\n\t- {self.inventory[key]}")
        else:
            print("\nIl n'y a rien ici.")

    #Define the get_entities method
    def get_entities(self, show = False):
        if show:
            print(f"\nLes entités autour de vous sont:")
            for entity in Room.entities[self.name]:
                if entity.id != 1: #identifiant du joueur
                    print(f"\n\t-{entity}")
        return self.entities
         