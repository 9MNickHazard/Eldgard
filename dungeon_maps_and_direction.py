import time
import random
import re
import pprint
from dataclasses import dataclass

from mechanics import combat_1v1, roll_1v1_initiative, roll_flee_check, roll_damage_value, monster_turn_1v1, player_turn_1v1, roll_stat, seperator, roll_stat_check_d20, get_modifier_value, initiate_combat, printwait, roll_loot, perform_stat_check
from character_and_monsters import Character, Monster, Weapon

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
    direction_choice = directions_dict[list(directions_dict.keys())[int(direction_choice) - 1]]

    next_room = directions_dict[direction_choice]

    return next_room, direction_choice



class first_dungeon_jail_free_explore:
    


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
        | Special  | Nothing  - Starting - Chest    - Crazy    |
        | Chest    |          | Room     |          | Prisoner |
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
    'room11': {'north:': 'room21'},
    'room12': {'north:': 'room22', 'east:': 'room13'},
    'room13': {'north:': 'room23', 'west:': 'room12', 'east:': 'room14'},
    'room14': {'west:': 'room13', 'east:': 'room15'},
    'room15': {'north:': 'room25', 'west:': 'room14'},
    'room21': {'north:': 'room31', 'south:': 'room11', 'east:': 'room22'},
    'room22': {'north:': 'room32', 'west:': 'room21', 'south:': 'room12', 'east:': 'room23'},
    'room23': {'north:': 'room33', 'west:': 'room22', 'south:': 'room13'},
    'room24': {},
    'room25': {'north:': 'room35', 'south:': 'room15'},
    'room31': {'south:': 'room21', 'east:': 'room32'},
    'room32': {'west:': 'room31', 'south:': 'room22', 'east:': 'room33'},
    'room33': {'north:': 'room43', 'west:': 'room32', 'south:': 'room23', 'east:': 'room34'},
    'room34': {'west:': 'room33', 'east:': 'room35'},
    'room35': {'north:': 'room45', 'west:': 'room34', 'south:': 'room25'},
    'room41': {},
    'room42': {},
    'room43': {'north:': 'room53', 'south:': 'room33'},
    'room44': {},
    'room45': {'boss:': 'exit'},
    'room51': {},
    'room52': {},
    'room53': {'south:': 'room43', 'east:': 'room54'},
    'room54': {'west:': 'room53', 'east:': 'room55'},
    'room55': {'west:': 'room54', 'south:': 'room45'}
    }
    


    def rat_room(self, character: Character, number_of_rats):
        rat_loot = random.randint(1, 10)
        rat_chance_of_nothing = random.randint(15, 30)
        rat = Monster('Putrid Rat', '1d4 - 1', 'Rodent', {'gold_coins': rat_loot, 'chance_of_nothing': rat_chance_of_nothing}, 3, 3, 5, 1, 1, 1)
        printwait("You walk into the room...", 1)
        if number_of_rats == 1:
            printwait("You see a pair of beaty red eyes in the corner and a scuffle of paws. The Rat screeches and lunges at you...", 3)
            battle_result = initiate_combat(character, rat, True)
            loot_result = roll_loot(rat, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else: 
                print('Unkown Loot Error')
        elif number_of_rats == 2:
            printwait("You see two pairs of beaty red eyes in the corner and a scuffle of paws. The Rat closest to you screeches and lunges at you...", 3)
            battle_result = initiate_combat(character, rat, True)
            loot_result = roll_loot(rat, character, battle_result)
            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                printwait("You barely have time to catch your breath. The second Rat lunges at you...", 2)
            elif loot_result == 'death':
                return loot_result
            else: 
                print('Unkown Loot Error')

            battle_result = initiate_combat(character, rat, True)
            loot_result2 = roll_loot(rat, character, battle_result)

            if loot_result2 in ['no_loot', 'yes_loot', 'fled', 'death']:
                return loot_result
            else: 
                print('Unkown Loot Error')

    # starting room visited value
    rooms_visited = ['room13']


    # for chest loot, guarenteed_loot is a dict with keys as what the loot is and values as how much of that item is given
    # for other things, value is a list with 0 index value being number of items and 1 index value is the chance of getting that item
    iron_shortsword = Weapon('Iron Shortsword', '1d4 + 2', 1, 'Sword', 'Common', 1, 'A basic iron shortsword, reliable in close combat.', 5)
    iron_longsword = Weapon('Iron Longsword', '1d5 + 2', 0, 'Sword', 'Common', 1, 'Long iron blade, favored by many warriors.', 8)
    mithril_shortsword = Weapon('Mithril Shortsword', '1d7 + 1', 2, 'Sword', 'Uncommon', 1, 'Lightweight yet durable, this mithril blade cuts with ease.')

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
        'small_health_potion': [2, 35], 
        'small_attack_potion': [1, 10], 
        'small_defense_potion': [1, 5]
    }

    rare_chest_loot = {
        "guarenteed_loot": {iron_longsword: 1, 'gold_coins': 2},
        "nothing": [1, 20],
        "gold_coins": [random_gold_rare_chest(), 30],
        'small_health_potion': [3, 35], 
        'small_attack_potion': [1, 10], 
        'small_defense_potion': [1, 5]
    }

    special_chest_loot = {
        "guarenteed_loot": {mithril_shortsword: 1, 'gold_coins': 5},
        "nothing": [1, 10],
        "gold_coins": [random_gold_special_chest(), 40],
        'small_health_potion': [4, 35], 
        'small_attack_potion': [2, 10], 
        'small_defense_potion': [1, 5]
    }

    def add_loot_to_inv(character, total_loot):
        for item, quantity in total_loot:
            if isinstance(item, Weapon):
                weapon_name = item.name
                if weapon_name in character.inventory['weapons']:
                    character.inventory['weapons'][weapon_name] += 1
                else:
                    character.inventory['weapons'][weapon_name] = 1
            elif item == 'nothing':
                continue
            elif item == 'gold_coins':
                character.inventory['gold_coins'] += quantity
            elif item in ['small_health_potion', 'small_attack_potion', 'small_defense_potion']:
                character.inventory['potions'][item] += quantity
            else:
                if item in character.inventory['misc']:
                    character.inventory['misc'][item] += quantity
                else:
                    character.inventory['misc'][item] = quantity

        

    def loot_chest_roll(self, character: Character, chest_loot: dict, number_of_loots):
        total_probability = 0
        for item, value in list(chest_loot.items())[1:]:
            total_probability += value[1]
        
        if total_probability != 100:
            raise ValueError(f"Probabilities must sum to 100, but they sum to {total_probability}")
        
        printwait("You loot the chest...", 4)

        total_loot = []

        for i in range(1, number_of_loots):
            roll = random.randint(1, 100)
            cumulative_probability = 0
            for item, value in list(chest_loot.items())[1:]:
                probability = value[1]
                cumulative_probability += probability
                if roll <= cumulative_probability:
                    total_loot.append[item, value[0]]
        
        # right now this is only accounting for number_of_loots = 2
        if total_loot[0][0] and total_loot[1][0] == 'nothing':
            printwait("Unfortunate... You find nothing in the chest")
        elif total_loot[0][0] == 'nothing':
            printwait(f"You find {total_loot[1][1]} {total_loot[1][0]} in the chest")
            self.add_loot_to_inv(character, total_loot) 
        elif total_loot[1][0] == 'nothing':
            printwait(f"You find {total_loot[0][1]} {total_loot[0][0]} in the chest")
            self.add_loot_to_inv(character, total_loot)
        elif total_loot[0][0] == total_loot[1][0]:
            printwait(f"You find {(total_loot[0][1] + total_loot[1][1])} {total_loot[0][0]} in the chest")
            self.add_loot_to_inv(character, total_loot)
        else:
            printwait(f"You find {total_loot[0][1]} {total_loot[0][0]} and {total_loot[1][1]} {total_loot[1][0]} in the chest")
            self.add_loot_to_inv(character, total_loot)

        

    # WIP
    def loot_chest(self,character: Character, chest_type, chest_loot=chest_loot, rare_chest_loot=rare_chest_loot, special_chest_loot=special_chest_loot):
        if chest_type == 'chest':
            self.loot_chest_roll(character, chest_loot, 2)
            print(f"---Here is your inventory---")
            pprint.pprint(character.inventory)
            seperator()
        elif chest_type == 'rare_chest':
            self.loot_chest_roll(character, rare_chest_loot, 2)
            print(f"---Here is your inventory---")
            pprint.pprint(character.inventory)
            seperator()
        elif chest_type == 'special_chest':
            self.loot_chest_roll(character, special_chest_loot, 2)
            print(f"---Here is your inventory---")
            pprint.pprint(character.inventory)
            seperator()
        else:
            ValueError("Chest Type Error")

    # WIP
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
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 17, 'strength', 0, 1)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
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
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 18, 'strength', 0, 2)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
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
            else:
                printwait("Your lockpick breaks off in the lock... There's no way to get in there now...", 2)
                printwait("Unless you smash it... But that won't be easy...", 1)
                str_check = perform_stat_check(character, 19, 'strength', 0, 2)
                if str_check:
                    self.loot_chest(character, 'chest')
                    printwait("Which way will you go now...", 2)
                    chest_looted = True
                else:
                    printwait("You smash your weapon on the chest but it bounces off and knocks you in the face. Ouch!!", 2)
                    printwait("'Oh well...' You think, 'which way should I go now...'", 2)
        else:
            ValueError("Chest Type Error")

    # def main(self):
    #     rooms_visited = ['room13']
    #     while self.player_position != 'room45':
    #         next_room, direction = next_room_choice(self.player_position, self.rooms)
    #         printwait(f"You walk through the door to the {direction}...", 2)
    #         self.player_position = next_room
    #         if next_room in rooms_visited:
    #             printwait("You have already been in this room.")
    #         else:
    #             randomized_room = randomize_dungeon_room(self.room_contents) 
    #             if randomized_room == 'rat_1':
    #                 result = self.rat_room(self.character, 1)
    #             elif randomized_room == 'rat_2':
    #                 result = self.rat_room(self.character, 2)
    #             elif randomized_room == 'guard_1':
    #                 pass
    #             elif randomized_room == 'guard_2':
    #                 pass
    #             elif randomized_room == 'goblin_1':
    #                 pass
    #             elif randomized_room == 'goblin_2':
    #                 pass
    #             elif randomized_room == 'nothing':
    #                 pass
    #             elif randomized_room == 'chest':
    #                 pass
    #             elif randomized_room == 'rare_chest':
    #                 pass
    #             elif randomized_room == 'special_chest':
    #                 pass
    #             else:
    #                 printwait("Unknown Room Error", 1)

    #         rooms_visited.append(next_room)

def first_dungeon_function(character: Character):
    player_position = 'room13'
    # rooms_visited = ['room13']
    chest_looted = False
    while True:
        next_room, direction = next_room_choice(player_position, first_dungeon_jail_free_explore.rooms)

        printwait(f"You walk through the door to the {direction}...", 2)

        player_position = next_room

        if player_position == 'room45':
            break

        if player_position in first_dungeon_jail_free_explore.rooms_visited:
            printwait("You have already been in this room.")
        elif player_position == 'room11':
            result = first_dungeon_jail_free_explore.chest_room(character, 'special chest', chest_looted)
        elif player_position == 'room14':
            result = first_dungeon_jail_free_explore.chest_room(character, 'chest', chest_looted)
        elif player_position == 'room54':
            result = first_dungeon_jail_free_explore.chest_room(character, 'rare chest', chest_looted)
        else:
            randomized_room = randomize_dungeon_room(first_dungeon_jail_free_explore.room_contents) 
            if randomized_room == 'rat_1':
                result = first_dungeon_jail_free_explore.rat_room(character, 1)
            elif randomized_room == 'rat_2':
                result = first_dungeon_jail_free_explore.rat_room(character, 2)
            elif randomized_room == 'guard_1':
                pass
            elif randomized_room == 'guard_2':
                pass
            elif randomized_room == 'goblin_1':
                pass
            elif randomized_room == 'goblin_2':
                pass
            elif randomized_room == 'nothing':
                pass
            elif randomized_room == 'chest':
                result = first_dungeon_jail_free_explore.chest_room(character, 'chest', chest_looted)

            elif randomized_room == 'rare_chest':
                result = first_dungeon_jail_free_explore.chest_room(character, 'rare chest', chest_looted)
            elif randomized_room == 'special_chest':
                result = first_dungeon_jail_free_explore.chest_room(character, 'special chest', chest_looted)
            else:
                ValueError("Unknown Room Error")

            if result == 'death':
                return 'death'

            first_dungeon_jail_free_explore.rooms_visited.append(next_room)
            



