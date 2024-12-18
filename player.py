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
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}


    # Define the get_history method.
    def get_history(self):
        print("\nVous avez déja visité les pièces suivantes:")
        for i in range(len(self.history)-1):
            print(f"\n\t_{self.history[i].name}")

    #Define the limit_history method
    def limit_history(self):
        if len(self.history) > 10:
           self.history.pop(0)

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
        directions = {"nord":"N", "sud":"S", "est":"E", "ouest":"O", "up": "U", "down":"D", "n":"N", "s":"S", "e":"E", "o":"O", "u":"U", "d": "D"}
        try:
            direction = directions[direction.lower()]
        except KeyError:
            next_room = None
        finally:
            next_room = self.current_room.get_exit(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        self.history.append(self.current_room)
        self.limit_history()
        return True

    