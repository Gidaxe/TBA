#from game import DEBUG

#Description: the Item module
class Item():

    inventaire_jeu = {}

    @classmethod
    def list_items(cls):
        for id in Item.inventaire_jeu:
            print(f"\n\t-{Item.inventaire_jeu[id]}")

    def __init__(self, name, identifiant, description, weight):
        self.name = name 
        self.id = identifiant
        self.description = description 
        self.weight = weight
        Item.inventaire_jeu[self.id] = self


    def __str__(self):
        return  f"{self.name} : {self.description} ({self.weight} kg)" 
    
