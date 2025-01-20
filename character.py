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
    followers = {}

    # Define the constructor.
    def __init__(self, name, identifier, description, starting_room, msgs, nomade = True, echange = False):
        self.id = identifier
        self.name = name
        self.description = description
        self.current_room = starting_room
        self.inventory = {}
        self.msgs = msgs
        self.nomade = nomade
        self.echange = echange
        self.leader = None

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
        return self.name + ": " + self.msgs.get(prompt, "huuummm")

            

    # Define the move method.
    def move(self):
        # Get the next room from the exits dictionary of the current room.
        
        if self.nomade:
            next_room = rd.choice([room for room in self.current_room.exits.values()])        

            # If there is no next room in that direction
            if next_room is None:
                return True
        else:
            #Ne rien afficher car le joueur n'a pas besoin de savoir si un npc n'a pas pu effectuer son déplacement automatique
            return True
        
        # Set the current room to the next room.
        self.current_room.refresh_room_entities(self, self.current_room, next_room)
        self.current_room = next_room
        return True
    

    #Define the follow player function
    def follow_player(self, player):
        room = self.current_room
        character_index = room.get_entity(name=self.name,room_index=True)
        if self.nomade:
            # Set the current room to the next room, remove npc from previous room entities list and add it to the new room's.
            # Dans difficultés rencontrés, ne pas oublier de parler de ce fichu bug qui se passe qd on ne prends pas en compte la diff entre égalité mathématique et référence en progammation.
            try:
                room.room_entities.pop(character_index)
                next_room = player.current_room
                self.current_room = next_room
                self.current_room.room_entities.append(self)
            finally:
                return True

        else:
            print(f"{self.name} ne peut pas se déplacer !")
        return True
        
        

    