import random as rd
#from game import DEBUG
# Define the Character class.
class Character():
    """
    Represents an NPC in the game.

    The Character class handles Character attributes such as their name and current location in the game world,
    as well as actions like moving between rooms.

    Attributes:
        name (str): The name of the Character.
        current_room (Room or None): The room where the Character is currently located.

    Methods:
        move(direction): Moves the Character to the room in the given direction, if possible.

    Exceptions:
        None.

    Examples:
        >>> from room import Room  # Assuming a Room class exists
        >>> kitchen = Room("Kitchen", "A cozy kitchen with a fireplace.")
        >>> hallway = Room("Hallway", "A narrow hallway.")
        >>> kitchen.exits = {"north": hallway}
        >>> hallway.exits = {"south": kitchen}

        >>> Character = Character("Alice")
        >>> Character.current_room = kitchen
        >>> Character.move("north")
        A narrow hallway.
        True

        >>> Character.move("west")
        Aucune porte dans cette direction !
        False
    """

    # Define the constructor.
    def __init__(self, name, identifier, description, starting_room, msgs, nomade = True):
        self.id = identifier
        self.name = name
        self.description = description
        self.current_room = starting_room
        self.inventory = {}
        self.msgs = msgs
        self.nomade = nomade

    #String representation of the PNG
    def __str__(self):
        return self.name + " : " + self.description

    #define the get_inventory method
    def get_inventory(self):
        if len(self.inventory) > 0:
            print(f"\n{self.name}vous propose:")
            for key in self.inventory.keys():
                if self.inventory[key] != None:
                    print(f"\n\t- {self.inventory[key]}")
        else:
            print(f"\n{self.name} n'a rien a vous offrir !")
    
    def get_msg(self, prompt):
        return self.msgs.get(prompt, "huuummm")

            

    # Define the move method.
    def move(self, direction = None):
        # Get the next room from the exits dictionary of the current room.
        if direction:
            if self.nomade:
                directions = {"nord":"N", "sud":"S", "est":"E", "ouest":"O", "up": "U", "down":"D", "n":"N", "s":"S", "e":"E", "o":"O", "u":"U", "d": "D"}
                try:
                    direction = directions[direction.lower()]
                except KeyError:
                    pass
                finally:
                    next_room = self.current_room.get_exit(direction)
            else:
                print(f"{self.name} ne peut pas se déplacer !")
                return True
        else:
            if self.nomade:
                next_room = rd.choice([room for room in self.current_room.exits.values()])        

                # If there is no next room in that direction
                if next_room is None:
                    return True
            else:
                return True
        
        # Set the current room to the next room.
        self.current_room.refresh_room_entities(self, self.current_room, next_room)
        self.current_room = next_room
        return True

    