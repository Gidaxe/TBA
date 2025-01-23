"""Module gérant la classe Player et les fonctions associées."""

from ascii import Game_over


# Define the Player class.
class Player:
    """
    Represents a player in the game.

    The Player class handles player attributes such as
    their name and current location in the game world,
    as well as actions like moving between rooms.

    Attributes:
        name (str): The name of the player.

        current_room (Room or None): The room where
        the player is currently located.

    Methods:
        move(direction): Moves the player to the room
        in the given direction, if possible.

    Exceptions:
        None.
    """

    # Define the constructor.
    def __init__(self, name):
        """Initialise le joueur avec un nom, ses attributs par défaut et son inventaire."""
        self.id = 1
        self.name = name
        self.hp = 100
        self.power = 50
        self.max_weight = 25
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.carte = {}
        self.invisible = False

    # Define the get_history method.
    def get_history(self):
        """Affiche et met à jour l’historique des pièces déjà visitées par le joueur."""
        print("\nVous avez déja visité les pièces suivantes:")
        for i in range(len(self.history)):
            print(f"\n\t_{self.history[i].name}")
            if self.history[i].name not in self.carte:
                self.carte[self.history[i].name] = self.history[
                    i
                ]  # carte did not turn out to be very useful in the end

    # Define the limit_history method
    def limit_history(self):
        """Limite l’historique des pièces à 10 entrées maximum en supprimant la plus ancienne."""
        if len(self.history) > 10:
            self.history.pop(0)

    # Define the limit_inventory method,
    # returns True if adding the new item would overload player capacity.
    def limit_inventory(self, new_item):
        """Vérifie si l’ajout d’un nouvel objet surcharge la capacité de portage du joueur.

        Args:
            new_item (Item): L’objet que l’on souhaite ajouter à l’inventaire.

        Returns:
            bool: True si l’inventaire dépasserait la limite de poids, False sinon.
        """
        if (
            sum([item.weight for item in self.inventory.values()]) + new_item.weight
            > self.max_weight
        ):
            return True

        return False

    # define the get_inventory method
    def get_inventory(self):
        """Affiche la liste des objets dans l’inventaire du joueur ou indique qu’il est vide."""
        if len(self.inventory) > 0:
            print("\nVous disposez des items suivants :")
            for value in self.inventory.values():
                if value is not None:
                    print(f"\n\t- {value}")
        else:
            print("\nVotre inventaire est vide.")

    # Define the move method.
    def move(self, direction):
        """Déplace le joueur dans la direction indiquée, si une sortie existe dans cette direction.

        Args:
            direction (str): La direction dans laquelle le joueur souhaite se déplacer.

        Returns:
            bool: True si le déplacement a réussi, False sinon.
        """
        # Get the next room from the exits dictionary of the current room.
        directions = {
            "nord": "N",
            "sud": "S",
            "est": "E",
            "ouest": "O",
            "up": "U",
            "down": "D",
            "n": "N",
            "s": "S",
            "e": "E",
            "o": "O",
            "u": "U",
            "d": "D",
            "sudest": "SE",
            "sudouest": "SO",
            "nordest": "NE",
            "nordouest": "NO",
            "se": "SE",
            "so": "SO",
            "ne": "NE",
            "no": "NO",
        }
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

    # Define the death method for the player.
    def death(self, ennemi):
        """Informe le jouer sur sa mort dans le jeu."""
        print(f"Vous avez été tué par: {ennemi.name}")
        print(Game_over)
        return True
