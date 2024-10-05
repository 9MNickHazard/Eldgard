import time
import random
import re
import pprint

from mechanics import combat_1v1, roll_1v1_initiative, roll_flee_check, roll_damage_value, monster_turn_1v1, player_turn_1v1, roll_stat, seperator, roll_stat_check_d20, get_modifier_value, initiate_combat, printwait, perform_stat_check, add_loot_to_inv, roll_monster_loot
from character_and_monsters import Character, Monster, Weapon, Named_Monsters

def randomize_dungeon_room(room_possibilities: dict):
    total_probability = sum(room_possibilities.values())
    if total_probability != 100:
        raise ValueError(f"Probabilities must sum to 100, but they sum to {total_probability}")

    roll = random.randint(1, 100)

    cumulative_probability = 0
    for room, probability in room_possibilities.items():
        cumulative_probability += probability
        if roll <= cumulative_probability:
            return room
        
# access a value in a dict using key index value:
    # directions_dict[list(directions_dict.keys())[0]]

def next_room_choice(player_position: str, rooms: dict): 
    '''rooms needs to be a dictionary with sub-dictionaries, where each key/value pair is a valid direction out of that room and the next room that is in that direction'''
    number_of_directions = len(rooms[player_position])
    directions_dict = rooms[player_position]

    if number_of_directions == 1:
        while True:
            direction_choice = input(f"Options: 1. {list(directions_dict.keys())[0]}\nWhich way would you like to go: ")
            if direction_choice == '1':
                break
            else:
                printwait("Please enter a valid option.", 1)
    elif number_of_directions == 2:
        while True:
            direction_choice = input(f"Options: 1. {list(directions_dict.keys())[0]} 2. {list(directions_dict.keys())[1]}\nWhich way would you like to go: ")
            if direction_choice in ['1', '2']:
                break
            else:
                printwait("Please enter a valid option.", 1)
    elif number_of_directions == 3:
        while True:
            direction_choice = input(f"Options: 1. {list(directions_dict.keys())[0]} 2. {list(directions_dict.keys())[1]} 3. {list(directions_dict.keys())[2]}\nWhich way would you like to go: ")
            if direction_choice in ['1', '2', '3']:
                break
            else:
                printwait("Please enter a valid option.", 1)
    else:
        while True:
            direction_choice = input(f"Options: 1. {list(directions_dict.keys())[0]} 2. {list(directions_dict.keys())[1]} 3. {list(directions_dict.keys())[2]} 4. {list(directions_dict.keys())[3]}\nWhich way would you like to go: ")
            if direction_choice in ['1', '2', '3', '4']:
                break
            else:
                printwait("Please enter a valid option.", 1)

    # changing direction_choice back from a str of (1,2,3,4) to north/west/south/east
    direction_choice = list(directions_dict.keys())[int(direction_choice) - 1]

    next_room = directions_dict[direction_choice]

    return next_room, direction_choice



class first_dungeon_jail_free_explore:
    def __init__(self) -> None:
        self.rooms_visited = ['room13']


    dungeon_map = """
        +----------+----------+----------+----------+----------+
        |          |          |          |          |          |
        |    X     |    X     | Random   - Rare     - Random   |
        |          |          |          | Chest    |          |
        +----------+----------+----|-----+----------+----|-----+
        |          |          |          |          |          |
        |    X     |    X     | Random   |    X     | Boss     > Exit
        |          |          |          |          |          |
        +----------+----------+----|-----+----------+----|-----+
        |          |          |          |          |          |
        | Random   - Random   - Random   - Random   - Random   |
        |          |          |          |          |          |
        +----|-----+----|-----+----|-----+----------+----|-----+
        |          |          |          |          |          |
        | Random   - Random   - Random   |    X     | Random   |
        |          |          |          |          |          |
        +----|-----+----|-----+----|-----+----------+----|-----+
        |          |          |          |          |          |
        | Special  | Nothing  - Starting - Chest    - Random   |
        | Chest    |          | Room     |          |          |
        +----------+----------+----------+----------+----------+
    """

    room_contents = {
        "rat_1": 14,
        "rat_2": 8,
        "guard_1": 14,
        "guard_2": 8,
        "goblin_1": 14,
        "goblin_2": 8,
        "nothing": 20,
        "chest": 9,
        "rare_chest": 4,
        "special_chest": 1
    }

    # rooms denoted by room(row)(collumn). From bottom left, to right and then the next row up.
    rooms = {
    'room11': {'north': 'room21'},
    'room12': {'north': 'room22', 'east': 'room13'},
    'room13': {'north': 'room23', 'west': 'room12', 'east': 'room14'},
    'room14': {'west': 'room13', 'east': 'room15'},
    'room15': {'north': 'room25', 'west': 'room14'},
    'room21': {'north': 'room31', 'south': 'room11', 'east': 'room22'},
    'room22': {'north': 'room32', 'west': 'room21', 'south': 'room12', 'east': 'room23'},
    'room23': {'north': 'room33', 'west': 'room22', 'south': 'room13'},
    'room24': {},
    'room25': {'north': 'room35', 'south': 'room15'},
    'room31': {'south': 'room21', 'east': 'room32'},
    'room32': {'west': 'room31', 'south': 'room22', 'east': 'room33'},
    'room33': {'north': 'room43', 'west': 'room32', 'south': 'room23', 'east': 'room34'},
    'room34': {'west': 'room33', 'east': 'room35'},
    'room35': {'north': 'room45', 'west': 'room34', 'south': 'room25'},
    'room41': {},
    'room42': {},
    'room43': {'north': 'room53', 'south': 'room33'},
    'room44': {},
    'room45': {'boss': 'exit'},
    'room51': {},
    'room52': {},
    'room53': {'south': 'room43', 'east': 'room54'},
    'room54': {'west': 'room53', 'east': 'room55'},
    'room55': {'west': 'room54', 'south': 'room45'}
    }

    


    def rat_room(self, character: Character, number_of_rats):
        rat = Named_Monsters.level_1_rat()

        printwait("You walk into the room...", 1)
        if number_of_rats == 1:
            printwait("You see a pair of beaty red eyes in the corner and a scuffle of paws. The Rat screeches and lunges at you...", 3)
            battle_result = initiate_combat(character, rat, True)
            loot_result = roll_monster_loot(rat, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else: 
                print('Unkown Loot Error')
        elif number_of_rats == 2:
            printwait("You see two pairs of beaty red eyes in the corner and a scuffle of paws. The Rat closest to you screeches and lunges at you...", 3)
            battle_result = initiate_combat(character, rat, True)
            loot_result = roll_monster_loot(rat, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                printwait("You barely have time to catch your breath. The second Rat lunges at you...", 2)
            elif loot_result == 'death':
                return loot_result
            else: 
                print('Unkown Loot Error')

            battle_result = initiate_combat(character, rat, True)
            loot_result2 = roll_monster_loot(rat, character, battle_result)

            if loot_result2 in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else: 
                print('Unkown Loot Error')

    def guard_room(self, character: Character, number_of_guards):
        guard = Named_Monsters.level_1_guard()

        printwait("You enter the room cautiously...", 1)
        
        if number_of_guards == 1:
            printwait("You spot a guard standing alert. They notice you and draw their weapon. 'What are you doing out of your cell!' they exclaim.", 3)
            battle_result = initiate_combat(character, guard, True)
            loot_result = roll_monster_loot(guard, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else:
                print('Unknown Loot Error')
        
        elif number_of_guards == 2:
            printwait("You see two guards patrolling the room. The first one notices you and exclaims, 'Oi! You there! Get over here!'", 3)
            battle_result = initiate_combat(character, guard, True)
            loot_result = roll_monster_loot(guard, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                printwait("Just as you finish dealing with the first guard, the second one charges at you...", 2)
            elif loot_result == 'death':
                return loot_result
            else:
                print('Unknown Loot Error')

            battle_result = initiate_combat(character, guard, True)
            loot_result2 = roll_monster_loot(guard, character, battle_result)

            if loot_result2 in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result2
            else:
                print('Unknown Loot Error')

    def goblin_room(self, character: Character, number_of_goblins):
        goblin = Named_Monsters.level_1_goblin()

        printwait("You enter the room, your senses on high alert...", 2)
        
        if number_of_goblins == 1:
            printwait("You hear a cackle and spot a goblin lurking in the shadows. It grins wickedly and attacks!", 3)
            battle_result = initiate_combat(character, goblin, True)
            loot_result = roll_monster_loot(goblin, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else:
                print('Unknown Loot Error')
        
        elif number_of_goblins == 2:
            printwait("You see two goblins arguing over some trinket. They stop abruptly when they notice you, and the first one charges with a shriek!", 3)
            battle_result = initiate_combat(character, goblin, True)
            loot_result = roll_monster_loot(goblin, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                printwait("As the first goblin falls to the floor, defeated, the second one sneaks up behind you...", 2)
            elif loot_result == 'death':
                return loot_result
            else:
                print('Unknown Loot Error')

            battle_result = initiate_combat(character, goblin, False)
            loot_result2 = roll_monster_loot(goblin, character, battle_result)

            if loot_result2 in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result2
            else:
                print('Unknown Loot Error')

    def boss_room(self, character: Character):
        tormunds_greatsword = Weapon("Tormund's Greatsword", '2d4 + 2', 2, 'Sword', 'Rare', 1, "The ornate and massive Greatsword of Tormund, the Reaper's Herald.", 40)
        if 'Mysterious Gem' in character.inventory['misc']:
            no_gem = False
            tormund_loot = {
            "guarenteed_loot": {'gold_coins': 40, 'Small Health Potion': 2, 'Small Attack Potion': 2, 'Small Defense Potion': 2},
            "nothing": [1, 0],
            "gold_coins": [25, 30],
            'Small Health Potion': [2, 30], 
            'Small Attack Potion': [2, 15], 
            'Small Defense Potion': [2, 5],
            tormunds_greatsword: [1, 20]
            }
        else:
            no_gem = True
            tormund_loot = {
            "guarenteed_loot": {'Mysterious Gem': 1, 'gold_coins': 40, 'Small Health Potion': 2, 'Small Attack Potion': 2, 'Small Defense Potion': 2},
            "nothing": [1, 0],
            "gold_coins": [25, 30],
            'Small Health Potion': [2, 30], 
            'Small Attack Potion': [2, 15], 
            'Small Defense Potion': [2, 5],
            tormunds_greatsword: [1, 20]
            }
        guard_boss = Monster("Tormund, the Reaper's Herald", '1d6 + 2', 'Human', tormund_loot, 1, 10, 1, 8, 8, 8, 300) # CHANGE THIS BACK TO 14, 10, 14, 8, 8, 8
        printwait("You walk into the room but this room is different... No cobwebs in the corners and no mice or rats running around the floor.", 3)
        printwait("On the other side of the room is a large wooden door, clearly the way out of this dreadful place.", 3)
        printwait("Standing directly in front of that door is one of the largest men you've ever seen... A guard with ornate armor and a horned helmet.", 3)
        printwait("He stands with both hands resting on the pummel of his enormous Greatsword.", 3)
        printwait("'Prisoner!' The enormous guard booms. 'You go no further. Your punishment is no longer time in a cell, now, for you, the Reapers draw near...'", 4)
        printwait("His Greatsword leaves a trail of sparks as he walks toward you, each heavily armored footstep echoing loudly in the small room...", 3)

        battle_result = initiate_combat(character, guard_boss, False)
        loot_result = roll_monster_loot(guard_boss, character, battle_result)


        if loot_result in ['no_loot', 'yes_loot', 'fled', 'death']:
            return loot_result, no_gem
        else:
            print('Unknown Loot Error')
    


    # for chest loot, guarenteed_loot is a dict with keys as what the loot is and values as how much of that item is given
    # for other things, value is a list with 0 index value being number of items and 1 index value is the chance of getting that item
    iron_shortsword = Weapon('Iron Shortsword', '1d4 + 2', 1, 'Sword', 'Common', 1, 'A basic iron shortsword, reliable in close combat.', 5)
    iron_longsword = Weapon('Iron Longsword', '1d5 + 2', 0, 'Sword', 'Common', 1, 'Long iron blade, favored by many warriors.', 8)
    mithril_shortsword = Weapon('Mithril Shortsword', '1d7 + 1', 2, 'Sword', 'Uncommon', 1, 'Lightweight yet durable, this mithril blade cuts with ease.', 15)

    def random_gold_chest():
        return random.randint(2, 10)
    
    def random_gold_rare_chest():
        return random.randint(4, 14)
        
    def random_gold_special_chest():
        return random.randint(6, 18)

    chest_loot = {
        "guarenteed_loot": {iron_shortsword: 1, 'gold_coins': 2},
        "nothing": [1, 30],
        "gold_coins": [random_gold_chest(), 20],
        'Small Health Potion': [2, 35], 
        'Small Attack Potion': [1, 10], 
        'Small Defense Potion': [1, 5]
    }

    rare_chest_loot = {
        "guarenteed_loot": {iron_longsword: 1, 'gold_coins': 2},
        "nothing": [1, 20],
        "gold_coins": [random_gold_rare_chest(), 30],
        'Small Health Potion': [3, 35], 
        'Small Attack Potion': [1, 10], 
        'Small Defense Potion': [1, 5]
    }

    special_chest_loot = {
        "guarenteed_loot": {mithril_shortsword: 1, 'gold_coins': 5},
        "nothing": [1, 10],
        "gold_coins": [random_gold_special_chest(), 40],
        'Small Health Potion': [4, 35], 
        'Small Attack Potion': [2, 10], 
        'Small Defense Potion': [1, 5]
    }

        

    def loot_chest_roll(self, character: Character, chest_loot: dict, number_of_loots):
        guarenteed_loot = chest_loot['guarenteed_loot']
        guarenteed_loot = list(guarenteed_loot.items())

        total_probability = 0
        for item, value in list(chest_loot.items())[1:]:
            total_probability += value[1]
        
        if total_probability != 100:
            raise ValueError(f"Probabilities must sum to 100, but they sum to {total_probability}")
        
        printwait(f"You loot the chest {number_of_loots} time(s)...", 4)

        total_loot = []

        for i in range(number_of_loots):
            roll = random.randint(1, 100)
            cumulative_probability = 0
            for item, value in list(chest_loot.items())[1:]:
                probability = value[1]
                cumulative_probability += probability
                if roll <= cumulative_probability:
                    total_loot.append((item, value[0]))
                    break
        
        if guarenteed_loot:
            add_loot_to_inv(character, guarenteed_loot)

        add_loot_to_inv(character, total_loot)

        # if len(total_loot) >= 2:
        #     if total_loot[0][0] == 'nothing' and total_loot[1][0] == 'nothing':
        #         printwait("Unfortunate... You find nothing in the chest", 3)
        #     elif total_loot[0][0] == 'nothing':
        #         printwait(f"You find {total_loot[1][1]} {total_loot[1][0]} in the chest", 3)
        #         add_loot_to_inv(character, [total_loot[1]])
        #     elif total_loot[1][0] == 'nothing':
        #         printwait(f"You find {total_loot[0][1]} {total_loot[0][0]} in the chest", 3)
        #         add_loot_to_inv(character, [total_loot[0]])
        #     elif total_loot[0][0] == total_loot[1][0]:
        #         combined_amount = total_loot[0][1] + total_loot[1][1]
        #         printwait(f"You find {combined_amount} {total_loot[0][0]} in the chest", 3)
        #         add_loot_to_inv(character, [(total_loot[0][0], combined_amount)])
        #     else:
        #         printwait(f"You find {total_loot[0][1]} {total_loot[0][0]} and {total_loot[1][1]} {total_loot[1][0]} in the chest", 3)
        #         add_loot_to_inv(character, [total_loot[0], total_loot[1]])
        # elif len(total_loot) == 1:
        #     if total_loot[0][0] == 'nothing':
        #         if not guarenteed_loot:
        #             printwait("Unfortunate... You find nothing in the chest", 3)
        #         else:
        #             pass
        #     else:
        #         printwait(f"You find {total_loot[0][1]} {total_loot[0][0]} in the chest", 3)
        #         add_loot_to_inv(character, [total_loot[0]])
        # else:
        #     if not guarenteed_loot:
        #         printwait("Unfortunate... You find nothing in the chest", 3)
        #     else:
        #         pass


        


    def loot_chest(self,character: Character, chest_type, chest_loot=chest_loot, rare_chest_loot=rare_chest_loot, special_chest_loot=special_chest_loot):
        if chest_type == 'chest':
            self.loot_chest_roll(character, chest_loot, 2)
            seperator()
        elif chest_type == 'rare_chest':
            self.loot_chest_roll(character, rare_chest_loot, 2)
            seperator()
        elif chest_type == 'special_chest':
            self.loot_chest_roll(character, special_chest_loot, 2)
            seperator()
        else:
            ValueError("Chest Type Error")


    def chest_room(self, character: Character, type_of_chest, chest_looted):
        if chest_looted:
            printwait("You see a chest in the middle of the dark and musty room. You approach it and realize the chest has already been looted... Unfortunate...", 2)
        elif type_of_chest == 'chest':
            printwait("You see a chest in the middle of the dark and musty room. You approach it and find it locked.", 2)
            printwait("You may just be able to pick the lock...", 1)
            check = perform_stat_check(character, 10, 'dexterity', 0, 6)
            if check:
                self.loot_chest(character, 'chest')
                printwait("Which way will you go now...", 2)
                chest_looted = True
                return chest_looted
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 17, 'strength', 0, 1)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
                    return chest_looted
                else:
                    printwait("You smash your weapon on the chest but it bounces off and knocks you in the face. Ouch!!", 2)
                    printwait("'Oh well...' You think, 'which way should I go now...'", 2)
        elif type_of_chest == 'rare_chest':
            printwait("Your eyes are drawn to a chest in the center of the room with a reinforced lid. It seems this one was built to protect something valuable.", 2)
            printwait("You may just be able to pick the lock, although it won't be easy...", 1)
            check = perform_stat_check(character, 12, 'dexterity', 0, 5)
            if check:
                self.loot_chest(character, 'rare_chest')
                printwait("Which way will you go now...", 2)
                chest_looted = True
                return chest_looted
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 18, 'strength', 0, 2)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
                    return chest_looted
                else:
                    printwait("You smash your weapon on the chest but it bounces off and knocks you in the face. Ouch!!", 2)
                    printwait("'Oh well...' You think, 'which way should I go now...'", 2)
        elif type_of_chest == 'special_chest':
            printwait("In the center of the room stands a chest with a sturdy iron lock. It's clear that extra care was taken to secure this one.", 2)
            printwait("I may be able to pick this lock if I'm lucky...", 1)
            check = perform_stat_check(character, 15, 'dexterity', 0, 4)
            if check:
                self.loot_chest(character, 'special_chest')
                printwait("Which way will you go now...", 2)
                chest_looted = True
                return chest_looted
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 19, 'strength', 0, 2)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
                    return chest_looted
                else:
                    printwait("You smash your weapon on the chest but it bounces off and knocks you in the face. Ouch!!", 2)
                    printwait("'Oh well...' You think, 'which way should I go now...'", 2)
        else:
            ValueError("Chest Type Error")


########################################################################

def first_dungeon_function(character: Character):
    dungeon_instance = first_dungeon_jail_free_explore()
    player_position = 'room13'
    # rooms_visited = ['room13']
    chest_looted = False
    while True:
        next_room, direction = next_room_choice(player_position, dungeon_instance.rooms)

        printwait(f"You walk through the door to the {direction}...", 2)

        player_position = next_room

        if player_position == 'room45':
            result, no_gem = dungeon_instance.boss_room(character)
            if result == 'death':
                break
            else:
                player_position = 'exit'

        if player_position == 'exit':
            if no_gem:
                printwait("You find your Mysterious Gem on the body of Tormund. He must have had it all along...")
                seperator()
            printwait("You vanquish Tormund, the Reaper's Herald and successfully escape the jail!", 2)
            seperator()
            return 'dungeon complete'
        
        if player_position in dungeon_instance.rooms_visited:
            printwait("You have already been in this room.", 2)
            seperator()
        elif player_position == 'room11':
            result = dungeon_instance.chest_room(character, 'special_chest', chest_looted)
            if result == True:
                chest_looted = True
        elif player_position == 'room14':
            result = dungeon_instance.chest_room(character, 'chest', chest_looted)
            if result == True:
                chest_looted = True
        elif player_position == 'room34':
            result = dungeon_instance.chest_room(character, 'chest', chest_looted)
            if result == True:
                chest_looted = True
        elif player_position == 'room54':
            result = dungeon_instance.chest_room(character, 'rare_chest', chest_looted)
            if result == True:
                chest_looted = True
        else:
            randomized_room = randomize_dungeon_room(dungeon_instance.room_contents) 
            if randomized_room == 'rat_1':
                result = dungeon_instance.rat_room(character, 1)
                if result == 'death':
                    break
            elif randomized_room == 'rat_2':
                result = dungeon_instance.rat_room(character, 2)
                if result == 'death':
                    break
            elif randomized_room == 'guard_1':
                result = dungeon_instance.guard_room(character, 1)
                if result == 'death':
                    break
            elif randomized_room == 'guard_2':
                result = dungeon_instance.guard_room(character, 2)
                if result == 'death':
                    break
            elif randomized_room == 'goblin_1':
                result = dungeon_instance.goblin_room(character, 1)
                if result == 'death':
                    break
            elif randomized_room == 'goblin_2':
                result = dungeon_instance.goblin_room(character, 2)
                if result == 'death':
                    break
            elif randomized_room == 'nothing':
                printwait("You walk into the cold, dark room but see nothing of interest except cobwebs and mice scuttling around on the dank floor...", 2)
                seperator()
            elif randomized_room == 'chest':
                result = dungeon_instance.chest_room(character, 'chest', chest_looted)
                if result == True:
                    chest_looted = True
            elif randomized_room == 'rare_chest':
                result = dungeon_instance.chest_room(character, 'rare_chest', chest_looted)
                if result == True:
                    chest_looted = True
            elif randomized_room == 'special_chest':
                result = dungeon_instance.chest_room(character, 'special_chest', chest_looted)
                if result == True:
                    chest_looted = True
            else:
                ValueError("Unknown Room Error")

        dungeon_instance.rooms_visited.append(next_room)

    if result == 'death':
        return 'death'

        
            



