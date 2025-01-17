import item as obj
#from game import DEBUG
# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"
# The MSG2 variable is used when the command takes 2 parameters.
MSG2 = "\nLa commande '{command_word}' prend 2 paramètres.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
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
        player.get_history()
        print(player.current_room.get_long_description())
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
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
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

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
        
        # Print the list of available commands.
        game.process_command(input("> "))
        return True
    

    def connexion(game, list_of_words, number_of_parameters):
        player = game.player

                # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
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
        
        try:
            player.current_room.refresh_room_entities(player, player.current_room, player.history[-2])
            player.current_room = player.history[-2]
            history.pop()
            player.limit_history()
            player.get_history()
        except IndexError:
            pass
        finally:
            print(player.current_room.get_long_description())
            return True
        

    def look(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        room.get_inventory()
        room.get_entities(show=True)
        return True


    def take(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

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
        
        player.inventory[item] = room.inventory.pop(item, None)
        return True
    

    def drop(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        item = list_of_words[1]
        room.inventory[item] = player.inventory.pop(item, None)
        return True
    

    def check(game, list_of_words, number_of_parameters):
        player = game.player

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player.get_inventory()
        return True
    
    def items(game, list_of_words, number_of_parameters):

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        obj.Item.list_items()
        return True
    
    def beam(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        carte = player.carte
        #verification du nombre d'arguments
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        #vérification des conditions de téléportation
        if room.name != "Arbre voyageur":
            print("vous ne pouvez vous téléporter qu'a proximité de l'arbre du voyageur !")
            return True
        elif "map" not in player.inventory.keys():
            print("Vous ne pouvez pas vous téléporter sans la carte magique")
            return True
        print('vous ne pouvez vous téléporter que dans les pièces enregistré dans votre carte magique.')
        print([ i for i in carte.keys()])
        #choix de la destination et téléportation
        destination = input("portail magique>")
        if destination not in carte.keys():
            print(f"vous ne pouvez pas vous téléporter à {destination}")
        elif destination == "quit":
            return True
        else:
            player.current_room.refresh_room_entities(player, player.current_room, carte[destination])
            player.current_room = carte[destination]
            player.history.append(player.current_room)
            player.limit_history()
            player.get_history()
            print("téléportation réussie !! \n")
            print(player.current_room.get_long_description())
        
        return True
    
    def lead(game, list_of_words, number_of_parameters):
        player = game.player

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG2.format(command_word=command_word))
            return False
        
        direction = list_of_words[1]
        npc = player.current_room.get_entity(list_of_words[2])

        if npc == None:
            return True
        
        if list_of_words[1] == "lock":
            if npc.nomade:
                npc.following = True
                npc.leader = player
                print(f'{npc.name} vous suis !')
                return True
            print(f'{npc.name} ne peut pas se déplacer !')
            return True
        
        if list_of_words[1] == "unlock":
            npc.following = False
            npc.leader = None
            print(f'{npc.name} ne vous suis plus !')
            return True
        
        if npc.nomade:
            player.move(direction)
            npc.follow_player(player)
            player.get_history()
            print(player.current_room.get_long_description())
            return True
        else:
            print(f"{npc.name} ne peut pas se déplacer !")
            return True
            
    
    def talk(game, list_of_words, number_of_parameters):
        player = game.player

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        npc = list_of_words[1]
        entities = player.current_room.entities[player.current_room.name]
        
        for ent in entities:
            if ent.name == npc:
                while True:
                    msg = input(f"\ntappez 'bye' pour arreter de parler avec {ent.name} \nDiscussion>")
                    if msg == "bye":
                        print("Au revoir jeune aventurier !")
                        return True
                    print(ent.get_msg(msg))

        print("Il n'y a personne de ce nom ici !")
        return True
    ##écrire une commande beam