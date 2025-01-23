import item as obj
from ascii import carte_monde
from ascii import Titre

"""# Description: The actions module.

 The actions module contains the functions that are called when a command is executed.
 Each function takes 3 parameters:
 - game: the game object
 - list_of_words: the list of words in the command
 - number_of_parameters: the number of parameters expected by the command
 The functions return True if the command was executed successfully, False otherwise.
 The functions print an error message if the number of parameters is incorrect.
 The error message is different depending on the number of parameters expected by the command."""


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"
# The MSG2 variable is used when the command takes 2 parameters.
MSG2 = "\nLa commande '{command_word}' prend 2 paramètres.\n"


class Actions:
    """La classe Actions n’est pas instanciable. Elle regroupe les fonctions qui permettent au joueur d’interagir avec le jeu. 
    Il y a deux types de fonctions, celles qui sont appelées lors de l’exécution d’une commande par le joueur, 
    et celles qui sont appelées lors de l’utilisation d’un objet par le joueur. Ainsi on a les fonctions"""

    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        print(player.current_room.get_long_description())
        return True

    def quit(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def vide(game, list_of_words, number_of_parameters):
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Does nothing
        return True

    def connexion(game, list_of_words, number_of_parameters):
        player = game.player

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Connects the player to the virtual world.
        print("Bienvenue dans:")
        print(Titre)
        player.current_room = game.rooms[1]
        player.history.append(player.current_room)
        print(player.current_room.get_long_description())
        return True

    def back(game, list_of_words, number_of_parameters):
        player = game.player
        history = player.history

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Prevents the player from going back once he is in one of the final rooms.
        if player.current_room.solo:
            print("Vous ne pouvez plus faire marche arrière jeune héro !!!")
            return True

        try:
            player.current_room = player.history[-2]
            player.current_room.refresh_room_allies()
            history.pop()
            player.limit_history()
        except IndexError:
            pass
        finally:
            print(player.current_room.get_long_description())
            return True

    def look(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Prints out the Player's current room, it's description, what items and entities are inside.
        print(f"\n{room.name}")
        print(f"\n{room.get_exit_string()}")
        room.get_inventory()
        room.get_entities(show=True)
        return True

    def take(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item = list_of_words[1]

        if item not in room.inventory:
            print("cet objet n'est pas présent dans cette salle")
            return True

        if player.limit_inventory(room.inventory[item]):
            print("votre inventaire est trop plein !!!")
            return True

        # Takes an item from the room's inventory to the player's
        player.inventory[item] = room.inventory.pop(item, None)
        print(f"\nVous venez d'aquérir: {player.inventory[item].name}")
        return True

    def drop(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Takes an item from the player's inventory to the Room's
        item = list_of_words[1]
        room.inventory[item] = player.inventory.pop(item, None)
        print(f"\nVous venez de déposer: {item}")
        return True

    def check(game, list_of_words, number_of_parameters):
        player = game.player

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Prints out the player's HP, attack power and the content of his inventory.
        print(f"Vous avez: {player.hp}HP,  {player.power}ATK")
        player.get_inventory()
        return True

    def history(game, list_of_words, number_of_parameters):
        player = game.player

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Prints out the player's travel history.
        player.get_history()

    def items(game, list_of_words, number_of_parameters):

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Lists out all the items present in the game.
        obj.Item.list_items()
        return True

    def beam(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Verification of the teleportation conditions.
        if room.name != "Arbre voyageur":
            print(
                "vous ne pouvez vous téléporter qu'a proximité de l'arbre du voyageur !"
            )
            return True
        elif "map" not in player.inventory.keys():
            print("Vous ne pouvez pas vous téléporter sans la carte magique")
            return True
        room_names = [room.name for room in game.rooms]
        print("Vous ne pouvez vous téléporter n'importe où dans le monde !.")
        print(room_names)

        # Choose a destination
        destination = input("portail magique>")
        if destination not in room_names:
            print(f"vous ne pouvez pas vous téléporter à {destination}")
        else:
            # Teleports the player to his desired location
            player.current_room = [
                dest for dest in game.rooms if dest.name == destination
            ].pop()
            print("téléportation réussie !! \n")
            player.current_room.refresh_room_allies()
            player.history.append(player.current_room)
            player.limit_history()
            print(player.current_room.get_long_description())

        return True

    def lead(game, list_of_words, number_of_parameters):
        player = game.player

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG2.format(command_word=command_word))
            return False

        direction = list_of_words[1]
        npc = player.current_room.get_entity(list_of_words[2])

        if npc == None:
            return True

        # Binds the NPC to the player
        if list_of_words[1] == "lock":
            if npc.nomade:
                npc.followers[npc.name] = npc
                npc.leader = player
                print(f"{npc.name} vous suis !")
                return True
            print(f"{npc.name} ne peut pas se déplacer !")
            return True

        # Unbinds the NPC from the player
        if list_of_words[1] == "unlock":
            del npc.followers[npc.name]
            npc.leader = None
            print(f"{npc.name} ne vous suis plus !")
            return True

        # Teleport the NPC with the player without binding it.
        if npc.nomade:
            player.move(direction)
            npc.follow_player(player)
            print(player.current_room.get_long_description())
            return True
        else:
            print(f"{npc.name} ne peut pas se déplacer !")
            return True

    def talk(game, list_of_words, number_of_parameters):
        player = game.player

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        npc = list_of_words[1]
        entity = player.current_room.get_entity(npc)
        if not entity:
            return True
        # list of all the promps the npc knows how to answer.
        msgs = [msg for msg in entity.msgs]

        # Talk with the entity, you can either trade or dialogue with them.
        while True:
            if entity.echange:
                print(f"\nTappez 'commerce' pour commercer avec {entity.name}")
            for i in range(len(msgs)):
                print(f"\n{i}: {msgs[i]}")
            print(f"\nTappez 'bye' pour arreter de parler avec {entity.name}")

            choix = input(f"\nChoix>")
            if choix == "bye":
                print(f"{entity.name}: Au revoir jeune aventurier !")
                return True
            elif choix == "commerce":
                Actions.echanger(player, entity)
                return True

            try:
                msg = msgs[int(choix)]
                msg = entity.get_response(msg)
                if not msg:
                    return True
                print(msg)
            except:
                print(
                    f"Veillez saisir un choix valide: {[i for i in range(len(msgs))]}"
                )

    def echanger(player, merchant):
        # Trade Menu, you can either either buy, sell or directly trade items.
        print(f"{merchant.name}: Que veux-tu faire ? acheter, vendre ou echanger ?")
        choix = input(f"\nOption>")
        if choix not in ("acheter", "vendre", "echanger"):
            print(f"\n{merchant.name}: Désolé, mais je ne peux pas vous aider !")
            return True

        if choix == "acheter":
            Actions.acheter(player, merchant)
            return True
        elif choix == "vendre":
            Actions.vendre(player, merchant)
            return True
        else:
            pass

    def acheter(player, merchant):
        # buy Items
        stock = [item for item in merchant.inventory]
        print(f"\n{merchant.name}: Que veux-tu acheter ?")
        print(stock)
        while True:
            print(f"Tappez 'bye' pour arreter de parler avec {merchant.name}")
            msg = input(f"\nAcheter>")
            if msg == "bye":
                print(
                    f"{merchant.name}: Ravi de faire affaire avec toi !!!\nAu revoir jeune aventurier !"
                )
                return True
            elif msg in stock:
                if not player.limit_inventory(merchant.inventory[msg]):
                    player.inventory[msg] = merchant.inventory[msg]
                    del merchant.inventory[msg]
                    print(f"{merchant.name}: Très bon choix !")
                    print(f"\nVous venez d'acquérir {msg} !")
                    Actions.acheter(player, merchant)
                    return True
                else:
                    print("votre inventaire est trop plein !!!")
            else:
                print(f"{merchant.name}: Je ne possède pas de {msg} !")

    def vendre(player, merchant):
        # sell Items
        stock = [item for item in player.inventory]
        print(f"\n{merchant.name}: Que veux-tu me vendre ?")
        print("Inventaire:")
        print(stock)
        while True:
            print(f"Tappez 'bye' pour arrêter de parler avec {merchant.name}")
            msg = input(f"\nVendre>")
            if msg == "bye":
                print(
                    f"{merchant.name}: Ravi de faire affaire avec toi !!!\nAu revoir jeune aventurier !"
                )
                return True
            elif msg in stock:
                merchant.inventory[msg] = player.inventory[msg]
                del player.inventory[msg]
                print(f"{merchant.name}: Très interessant !")
                print(f"\nVous venez de vendre {msg} à {merchant.name} !")
                Actions.vendre(player, merchant)
                return True
            else:
                print(f"{merchant.name}: Je ne possède pas de {msg} !")

    def use(game, list_of_words, number_of_parameters):
        player = game.player
        actions = {
            "map": (Actions.look_map, game),
            "boat": (Actions.naviger, game),
            "sword": (Actions.attaquer, game),
            "shield": (Actions.defence, game),
            "potion_magique": (Actions.regeneration, game),
            "menteau_d_invisibilité": (Actions.invisibilite, game),
            "oeil": (Actions.vision_magique, game),
        }

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item = list_of_words[1]

        if item not in player.inventory.keys():
            print(f"L'objet {item} n'est pas dans votre inventaire")
            return True

        # Use an Item
        action = actions.get(item, (Actions.innexistant, item))
        action[0](action[1])
        return True

    def innexistant(item):
        # Handles fringe cases where the item either runs out or does nothing.
        print(f"L'objet {item} ne fais rien ou n'est pas dans votre inventaire !")
        return True

    def look_map(game):
        # Display the world's map
        print(carte_monde)
        return True

    def naviger(game):
        # Use boat.
        player = game.player
        room = player.current_room
        destinations = [room for room in game.rooms if room.lacustre]
        destination_names = [
            room.name for room in destinations if room != player.current_room
        ]

        # Cannot use the boat when not near a body of water.
        if room not in destinations:
            print("Vous ne pouvez pas utiliser le bateau ici !")
            return True

        try:
            # Navigation menu to go to one of the islands on boat.
            print("\nOù voulez vous aller matelot ?")
            print(f"\n{destination_names}")
            destination = input("\nDestination>")
            next_room = [
                room for room in destinations if room.name == destination
            ].pop()
            player.current_room = next_room
            player.current_room.refresh_room_allies()
            player.history.append(player.current_room)
            player.limit_history()
            print(player.current_room.get_long_description())
        except:
            print(f"\nLa destination {destination} n'existe pas !")
        finally:
            return True

    def attaquer(game):
        # Attack ennemies and apply damage bonuses.
        player = game.player
        room = player.current_room
        ennemis = [entity for entity in room.room_entities if entity.ennemi]
        power = player.power
        bonus = 0
        try:
            followers = len(ennemis[0].followers)
            bonus += (
                followers * power * 0.5
            )  # Bonus de 50% pour chaque allié qui accompagne le héro.
            print(f"+{followers*100*0.5}% de dégats en plus")
        # If there are no enemies in the room, only prints out a message telling the player to chill out.
        except IndexError:
            print("\nRangez donc votre épée jeune héro ! Il n'y a pas d'énnemis ici !")
            return True
        finally:
            for ennemi in ennemis:
                ennemi.hp -= power + bonus
                if ennemi.hp < 0:
                    ennemi.hp = 0
                print(f"\n{ennemi.name}: {ennemi.hp} HP")
                if ennemi.hp == 0:
                    ennemi.death()

    def defence(game):
        # The shield item adds HP to the player's total HP. It is a lesser version of the cheat item that is the magic potion
        player = game.player
        player.hp += 250
        print("+250HP")
        del player.inventory["shield"]

    def regeneration(game):
        # The magic potion increases the Player's HP by 100 and can be used 25 times !
        player = game.player
        potion = player.inventory["potion_magique"]
        potion.nb_utilisations += 1
        player.hp += 100
        print("+100HP")
        if potion.nb_utilisations >= 25:
            del player.inventory["potion_magique"]

    def invisibilite(game):
        # Makes the player invisible.
        player = game.player
        player.invisible = not player.invisible
        if player.invisible:
            print(
                "Vous êtes maintenant invisible aux yeux de tous vous énnemis (à part Madar)."
            )
        else:
            print("Vous n'êtes plus invisible aux yeux de vos énnemis.")

    def vision_magique(game):
        # Turns off Madar's invincibility.
        player = game.player
        room = player.current_room
        Madar = game.antagoniste
        Madar.invincible = False
        print(
            "Vous pouvez désormais voir le point faible du tout puissant Mansa Madar.\nSon immortalité ne sert plus à rien !!!"
        )
