# Define the Item class
class Item():

    inventaire_jeu = {}

    # Define the list_items class method that lists out all the items in the game.
    @classmethod
    def list_items(cls):
        for id in Item.inventaire_jeu:
            print(f"\n\t-{Item.inventaire_jeu[id]}")

    # Define the constructor.
    def __init__(self, name, identifiant, description, weight):
        self.name = name 
        self.id = identifiant
        self.description = description 
        self.weight = weight
        self.nb_utilisations = 0
        Item.inventaire_jeu[self.id] = self

    # Define the string representation of an item.
    def __str__(self):
        return  f"{self.name} : {self.description} ({self.weight} kg)" 
    
