"""La classe Item décrit les caractéristiques des objets utilisables dans le jeu."""


class Item:
    """Classe représentant un objet du jeu (nom, identifiant, description, poids).
    Gère également l’inventaire global (inventaire_jeu) de tous les objets instanciés.
    """

    inventaire_jeu = {}

    @classmethod
    def list_items(cls):
        """Affiche dans la console la liste de tous les objets présents dans l’inventaire."""
        for item in Item.inventaire_jeu.values():
            print(f"\n\t-{item}")

    def __init__(self, name, identifiant, description, weight):
        """Défine the constructor"""
        self.name = name
        self.id = identifiant
        self.description = description
        self.weight = weight
        self.nb_utilisations = 0
        Item.inventaire_jeu[self.id] = self

    def __str__(self):
        """Define the string representation of an item."""
        return f"{self.name} : {self.description} ({self.weight} kg)"
