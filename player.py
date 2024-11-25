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
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    