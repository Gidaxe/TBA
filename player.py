Game_over = '''
   _________    __  _________   ____ _    ____________ 
  / ____/   |  /  |/  / ____/  / __ \ |  / / ____/ __ \ 
 / / __/ /| | / /|_/ / __/    / / / / | / / __/ / /_/ /
/ /_/ / ___ |/ /  / / /___   / /_/ /| |/ / /___/ _, _/ 
\____/_/  |_/_/  /_/_____/   \____/ |___/_____/_/ |_|  
                                                       '''

# Define the Player class.
class Player():
    """
    Represents a player in the game.

    The Player class handles player attributes such as their name and current location in the game world,
    as well as actions like moving between rooms.

    Attributes:
        name (str): The name of the player.
        current_room (Room or None): The room where the player is currently located.

    Methods:
        move(direction): Moves the player to the room in the given direction, if possible.

    Exceptions:
        None.

    Examples:
        >>> from room import Room  # Assuming a Room class exists
        >>> kitchen = Room("Kitchen", "A cozy kitchen with a fireplace.")
        >>> hallway = Room("Hallway", "A narrow hallway.")
        >>> kitchen.exits = {"north": hallway}
        >>> hallway.exits = {"south": kitchen}

        >>> player = Player("Alice")
        >>> player.current_room = kitchen
        >>> player.move("north")
        A narrow hallway.
        True

        >>> player.move("west")
        Aucune porte dans cette direction !
        False
    """

    # Define the constructor.
    def __init__(self, name):
        self.id = 1
        self.name = name
        self.HP = 100
        self.power = 50
        self.max_weight = 25
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.carte = {}
        self.invisible = False


    # Define the get_history method.
    def get_history(self):
        print("\nVous avez déja visité les pièces suivantes:")
        for i in range(len(self.history)):
            print(f"\n\t_{self.history[i].name}")
            if self.history[i].name not in self.carte.keys():
                self.carte[self.history[i].name] = self.history[i]

    #Define the limit_history method
    def limit_history(self):
        if len(self.history) > 10:
           self.history.pop(0)

    #Define the limit_inventory method
    def limit_inventory(self, new_item):
        if sum([self.inventory[item].weight for item in self.inventory]) + new_item.weight > self.max_weight:
           return True
    
        return False

    #define the get_inventory method
    def get_inventory(self):
        if len(self.inventory) > 0:
            print("\nVous disposez des items suivants :")
            for key in self.inventory.keys():
                if self.inventory[key] != None:
                    print(f"\n\t- {self.inventory[key]}")
        else:
            print("\nVotre inventaire est vide.")


    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        directions = {"nord":"N", "sud":"S", "est":"E", "ouest":"O", "up": "U", "down":"D", "n":"N", "s":"S", "e":"E", "o":"O", "u":"U", "d": "D","sudest":"SE","sudouest":"SO","nordest":"NE","nordouest":"NO", "se":"SE","so":"SO","ne":"NE","no":"NO"}
        try:
            direction = directions[direction.lower()]
        except KeyError:
            pass
        finally:
            next_room = self.current_room.get_exit(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        self.current_room.refresh_room_allies()
        self.history.append(self.current_room)
        self.limit_history()
        return True


    def death(self, ennemi):
        print(f"Vous avez été tué par: {ennemi.name}")
        print(Game_over)
        return True
    