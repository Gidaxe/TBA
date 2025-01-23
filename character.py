"""
Module character pour les PNG.
"""

import random as rd


# Define the Character class.
class Character:
    """
    Représente un PNJ dans le jeu.
    La classe Character gère les attributs des personnages tels que
    leur nom et leur emplacement actuel dans le monde du jeu, ainsi que 
    des actions comme se déplacer entre les pièces.
    """

    followers = {}

    def __init__(
        self,
        name,
        identifier,
        description,
        starting_room,
        msgs,
        nomade=True,
        echange=False,
        ennemi=False,
    ):
        """Define the constructor."""
        self.id = identifier
        self.name = name
        self.hp = 100
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

    def __str__(self):
        """La representation textuelle de la classe"""
        return self.name + " : " + self.description

    def get_inventory(self):
        """Définie la méthode get_inventory pour un PNG"""
        if len(self.inventory) > 0:
            print(f"\n{self.name}vous propose:")
            for value in self.inventory.values():
                if value is not None:
                    print(f"\n\t- {value}")
        else:
            print(f"\n{self.name} n'a rien a vous offrir !")

    def get_response(self, prompt):
        """Défini la méthode get_response method,
        elle se charge de gerer les réponses du PNG
        aux requetes du joueur."""
        if prompt == "Entraine nous !":
            heros = list(self.followers.values())
            if not heros:
                return False
            hero = heros[0].leader
            hero.power += 50
            print(
                "\nGrace à l'entrainement fourni par le mage légendaire de la forêt sacrée vous avez reçu '+100%' de puissance d'attaque !!!"
            )
            return True

        return self.name + ": " + self.msgs.get(prompt, "huuummm")

    def move(self):
        """Définie la méthode move, permet au PNG de se déplacer aléatoirement entre les rooms."""
        if self.nomade:
            next_room = rd.choice(list(self.current_room.exits.values()))

            # If there is no next room in that direction
            if next_room is None:
                return True
        else:
            # Ne rien afficher car le joueur n'a pas besoin de
            # savoir si un npc n'a pas pu effectuer son déplacement automatique
            return True

        # Set the current room to the next room.
        self.current_room.refresh_room_allies(self, self.current_room, next_room)
        self.current_room = next_room
        return True

    def follow_player(self, player):
        """Définie la méthode follow_player"""
        room = self.current_room
        next_room = player.current_room
        character_index = room.get_entity(name=self.name, room_index=True)
        if next_room.solo:
            print(f"{self.name} ne peux pas vous suivre dans ce lieux !")
            return True
        if self.nomade:
            # Set the current room to the next room, remove npc from previous room entities list
            # and add it to the new room's.
            # Difficulty encountered: room = next_room does not impact self.current_room.
            try:
                room.room_entities.pop(character_index)
                self.current_room = next_room
                self.current_room.room_entities.append(self)
                print(f"{self.name} vous suis vers {self.leader.current_room.name}.")
            finally:
                pass

        else:
            print(f"{self.name} ne peut pas se déplacer !")
        return True

    def death(self):
        """Définie la mort d'un NPC"""
        if self.invincible:
            return True
        print(f"\n{self.name} a été vaicu !")
        room = self.current_room
        character_index = room.get_entity(name=self.name, room_index=True)
        room.room_entities.pop(character_index)
        self.dead = True
        return True
