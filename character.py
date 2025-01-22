import random as rd


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
    def __init__(self, name, identifier, description, starting_room, msgs, nomade = True, echange = False, ennemi = False):
        self.id = identifier
        self.name = name
        self.HP = 100
        self.power = 25
        self.description = description
        self.current_room = starting_room
        self.inventory = {}
        self.msgs = msgs
        self.nomade = nomade
        self.echange = echange
        self.ennemi = ennemi
        self.invincible = False
        self.dead = False
        self.leader = None

    # String representation of the PNG
    def __str__(self):
        return self.name + " : " + self.description

    # Define the get_inventory method
    def get_inventory(self):
        if len(self.inventory) > 0:
            print(f"\n{self.name}vous propose:")
            for key in self.inventory.keys():
                if self.inventory[key] != None:
                    print(f"\n\t- {self.inventory[key]}")
        else:
            print(f"\n{self.name} n'a rien a vous offrir !")
    
    # Define the get_response method, it handles the responses of the NPC to the player's prompts
    def get_response(self, prompt):
        if prompt == "Entraine nous !":
            heros = [self.followers[entity] for entity in self.followers]
            if not heros:
                return False
            hero = heros[0].leader
            hero.power += 50
            print(f"\nGrace à l'entrainement fourni par le mage légendaire de la forêt sacrée vous avez reçu +100% de puissance d'attaque !!!")
            return True
        
        return self.name + ": " + self.msgs.get(prompt, "huuummm")

            

    # Define the move method, allows NPC to move randomly between rooms.
    def move(self):
        if self.nomade:
            next_room = rd.choice([room for room in self.current_room.exits.values()])        

            # If there is no next room in that direction
            if next_room is None:
                return True
        else:
            #Ne rien afficher car le joueur n'a pas besoin de savoir si un npc n'a pas pu effectuer son déplacement automatique
            return True
        
        # Set the current room to the next room.
        self.current_room.refresh_room_allies(self, self.current_room, next_room)
        self.current_room = next_room
        return True
    

    # Define the follow player method
    def follow_player(self, player):
        room = self.current_room
        next_room = player.current_room
        character_index = room.get_entity(name=self.name,room_index=True)
        if next_room.solo:
            print(f"{self.name} ne peux pas vous suivre dans ce lieux !")
            return True
        if self.nomade:
            # Set the current room to the next room, remove npc from previous room entities list and add it to the new room's.
            # Difficulty encountered: room = next_room does not impact self.current_room.
            try:
                room.room_entities.pop(character_index)
                self.current_room = next_room
                self.current_room.room_entities.append(self)
                print(f"{self.name} vous suis vers {self.leader.current_room.name}.")
            finally:
                return True

        else:
            print(f"{self.name} ne peut pas se déplacer !")
        return True
    
    # Defines the death method for NPCs
    def death(self):
        if self.invincible:
            return True
        print(f"\n{self.name} a été vaicu !")
        room = self.current_room
        character_index = room.get_entity(name=self.name,room_index=True)
        room.room_entities.pop(character_index)
        self.dead = True
        return True

    