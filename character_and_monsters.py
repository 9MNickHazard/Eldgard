import time
import random
import re

def printwait(what_to_print: str = "*Missing printwait string input*", wait_time: int = 1):
    print(what_to_print)
    # time.sleep(wait_time)

def seperator():
    print("------------------------------------")


def get_modifier_value(stat):
    modifiers = {
        range(1, 2): -5,
        range(2, 4): -4,
        range(4, 6): -3,
        range(6, 8): -2,
        range(8, 10): -1,
        range(10, 12): 0,
        range(12, 14): 1,
        range(14, 16): 2,
        range(16, 18): 3,
        range(18, 20): 4,
        range(20, 22): 5,
        range(22, 24): 6,
        range(24, 26): 7,
        range(26, 28): 8,
        range(28, 30): 9,
        range(30, 31): 10
        }    
    for stat_range, modifier in modifiers.items():
        if stat in stat_range:
            return f"+{modifier}" if modifier > 0 else str(modifier)
        
archer_special_abilities = ['Blinding Shot', 'Double Shot', 'Nimble Steps']
knight_special_abilities = ['Heavy Armor', 'Resilience', 'Big Swing']
wizard_special_abilities = ['Fire Storm', 'Magic Shield', 'Polymorph']

class Weapon:
    def __init__(self, name, damage, accuracy_bonus, weapon_type, rarity, required_level, description, value) -> None:
        self.name = name
        self.damage = damage
        self.accuracy_bonus = accuracy_bonus
        self.type = weapon_type
        self.rarity = rarity
        self.required_level = required_level
        self.description = description
        self.value = value

class Named_Weapons:
    maple_staff = Weapon('Maple Staff', '1d4 + 1', 0, 'Staff', 'common', 1, 'none', 0)
    bronze_longsword = Weapon('Bronze Longsword', '1d4 + 1', 0, 'Sword', 'common', 1, 'none', 0)
    wooden_bow = Weapon('Wooden Bow', '1d4 + 1', 0, 'Bow', 'common', 1, 'none', 0)
    tormunds_greatsword = Weapon("Tormund's Greatsword", '2d4 + 2', 2, 'Sword', 'Rare', 1, "The ornate and massive Greatsword of Tormund, the Reaper's Herald.", 40)


class Potion:
    """Potion Types: Self Heal, Attack Bonus, Damage Bonus, Defense Bonus
    each value is the bonus each turn so effect_duration of 2 and self_heal_amount of 4 would heal 8 over 2 turns"""
    def __init__(self, name, type, required_level: int = 1, description: str = 'none', effect_duration: int = 1, self_heal_amount: int = 0, attack_roll_bonus: int = 0, additional_damage: int = 0, damage_multiplier: int = 0, bonus_armor_class: int = 0):
        self.name = name
        self.type = type
        self.required_level = required_level
        self.description = description
        self.effect_duration = effect_duration
        self.self_heal_amount = self_heal_amount
        self.attack_roll_bonus = attack_roll_bonus
        self.additional_damage = additional_damage
        self.damage_multiplier = damage_multiplier
        self.bonus_armor_class = bonus_armor_class

class Named_Potions:
    small_health_potion = Potion('Small Health Potion', 'Self Heal', 1, "An oozing green brew that restores a few Hit Points. Doesn't look very appetizing...", 2, 4)
    small_attack_potion = Potion('Small Attack Potion', 'Attack Bonus', 1, "A white, almost glistening potion. One sip and your reflexes quicken.", 3, 0, 4)
    small_defense_potion = Potion('Small Defense Potion', 'Defense Bonus', 1, "A dark brown muddy potion. But it'll make your skin tough as leather.", 3, 0, 0, 0, 0, 5)

# player character
class Character:
    def __init__(self, name, role, pronouns, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.role = role
        self.pronouns = pronouns

        self.character_level = 1

        self.experience = 0

        self.evil_rating = 0

        self.good_rating = 0

        
        # core stats
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        # apply class (role) modifiers
        self.apply_role_modifiers()
        
        # hit points and armor class calculations
        self.hit_points = 10 + self.get_modifier(self.constitution)
        self.armor_class = 10 + self.get_modifier(self.dexterity)

        # special abilities, first value in each value's list is how many times the Special Ability has been used in the combat (when assigning this to a value 
        # inside player_turn_1v1), second value is the abilities' level and should not be changed inside the combat function.
        # third value is the number of times it can be used in a single combat.
        self.special_abilities_dictionary = {
            'blinding shot': [0, 1, 1],
            'double shot': [0, 1, 1],
            'nimble steps': [0, 1, 1],
            'heavy armor': [0, 1, 1],
            'resilience': [0, 1, 1],
            'big swing': [0, 1, 1],
            'fire storm': [0, 1, 1],
            'magic shield': [0, 1, 1],
            'polymorph': [0, 1, 1],
        }
        if role == 'archer':
            self.inventory = {
                'gold_coins': 0,
                'potions': {Named_Potions.small_health_potion: 1},
                'weapons': {Named_Weapons.wooden_bow: 1},
                'misc': {}
            }
        elif role == 'knight':
            self.inventory = {
                'gold_coins': 0,
                'potions': {Named_Potions.small_health_potion: 1},
                'weapons': {Named_Weapons.bronze_longsword: 1},
                'misc': {}
            }
        elif role == 'wizard':
            self.inventory = {
                'gold_coins': 0,
                'potions': {Named_Potions.small_health_potion: 1},
                'weapons': {Named_Weapons.maple_staff: 1},
                'misc': {}
            }
        

        self.equipped_items = {
            'weapon': next(iter(self.inventory['weapons'].keys())),
            'armor': None,
            'amulet': None,
            'ring': None
        }

        if role == 'archer':
            self.special_abilities = archer_special_abilities
        elif role == 'knight':
            self.special_abilities = knight_special_abilities
        elif role == 'wizard':
            self.special_abilities = wizard_special_abilities

    # Blinding Shot: Fire a special arrow that reduces the enemy's attack roll by 3 for the next 3 turns
    # Double shot: fire two arrows with lower accuracy
    # Nimble Steps: Periodically succeed 100 percent on Dexterity checks
    # Heavy Armor: Reduced damage from non-magical damage sources
    # Resilience: Recover a certain amount of hitpoints
    # Big Swing: Deal double damage, but add +3 to your enemy's next attack roll
    # Fire Storm: a damaging spell that burns the opponent for some amount of turns
    # Magic Shield: Increased Armor Class for a turn
    # Polymorph: Ability to change an enemy/npc into a harmless creature  

    # THIS IS MAYBE WORKING
    def equip_weapon(self):
        weapons_in_inv = list(self.inventory['weapons'].keys())
        weapon_names = [weapon.name for weapon in weapons_in_inv]

        weapon_choices = "\n".join([f"{i+1}. {weapon}" for i, weapon in enumerate(weapon_names)])
        while True:
            choice = input(f"Which weapon would you like to equip?\n{weapon_choices}\nChoice (type 'n' to cancel): ")
            if choice == 'n':
                break
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(weapons_in_inv):
                    weapon = weapons_in_inv[choice - 1]
                    if self.character_level >= weapon.required_level:
                        if self.equipped_items['weapon'] == weapon:
                            print("You already have that weapon equipped!")
                        else:
                            self.equipped_items['weapon'] = weapon
                            printwait(f"{weapon.name} equipped!", 1)
                            self.print_equipped_items()
                            break
                    else:
                        print("You are not a high enough level to equip this weapon!")
                else:
                    print("Please enter a valid option.")
            else:
                print("Please enter a valid option.")


    def apply_role_modifiers(self):
            if self.role == 'archer':
                self.strength -= 2
                self.dexterity += 3
                self.constitution -= 1
                self.wisdom += 2
                self.charisma += 1
            elif self.role == 'knight':
                self.strength += 3
                self.dexterity -= 2
                self.constitution += 3
                self.intelligence -= 2
                self.charisma += 3
            elif self.role == 'wizard':
                self.strength -= 3
                self.constitution -= 2
                self.intelligence += 4
                self.wisdom += 3
            else:
                print("Not a valid class, no modifiers applied")


    def get_modifier(self, stat):
        modifiers = {
            range(1, 2): -5,
            range(2, 4): -4,
            range(4, 6): -3,
            range(6, 8): -2,
            range(8, 10): -1,
            range(10, 12): 0,
            range(12, 14): 1,
            range(14, 16): 2,
            range(16, 18): 3,
            range(18, 20): 4,
            range(20, 22): 5,
            range(22, 24): 6,
            range(24, 26): 7,
            range(26, 28): 8,
            range(28, 30): 9,
            range(30, 31): 10
            }
        for stat_range, modifier in modifiers.items():
            if stat in stat_range:
                return modifier
    


    def display_character(self):
        print(f"Name: {self.name}")
        print(f"Pronouns: {self.pronouns}")
        print(f"Level: {self.character_level}")
        print(f"Experience: {self.experience}/{self.experience_for_levels[self.character_level + 1]}")
        print(f"Class: {self.role}")
        print(f"Strength: {self.strength} (Modifier: {get_modifier_value(self.strength)})")
        print(f"Dexterity: {self.dexterity} (Modifier: {get_modifier_value(self.dexterity)})")
        print(f"Constitution: {self.constitution} (Modifier: {get_modifier_value(self.constitution)})")
        print(f"Intelligence: {self.intelligence} (Modifier: {get_modifier_value(self.intelligence)})")
        print(f"Wisdom: {self.wisdom} (Modifier: {get_modifier_value(self.wisdom)})")
        print(f"Charisma: {self.charisma} (Modifier: {get_modifier_value(self.charisma)})")
        print(f"Hit Points (HP): {self.hit_points}")
        print(f"Armor Class (AC): {self.armor_class}")



    # each value is how much experience it takes to get to that level (the key). after each level up, experience goes back to 0
    experience_for_levels = {
        1: 0,
        2: 300,
        3: 900,
        4: 2700,
        5: 6500,
        6: 14000,
        7: 23000,
        8: 34000,
        9: 48000,
        10: 64000
    }

    def add_experience(self, amount):
        self.experience += amount

        if self.character_level < 10:
            next_level_exp = self.experience_for_levels[self.character_level + 1]
            if self.experience >= next_level_exp:
                overlap_exp = self.experience - next_level_exp
                self.character_level += 1
                print(f"You gained {amount} experience!")
                print(f"You leveled up!! You are now Level {self.character_level}.")
                self.experience = overlap_exp
                self.level_up()
                
            else:
                print(f"You gained {amount} experience!")
                print(f"Current Level: {self.character_level} | Next Level: {self.experience}/{self.experience_for_levels[self.character_level + 1]}")

        else:
            print("You are Max Level")

    stat_choice = {
        '1': 'strength',
        '2': 'dexterity',
        '3': 'constitution',
        '4': 'intelligence',
        '5': 'wisdom',
        '6': 'charisma'
    }

    def level_up(self):
        if self.character_level % 2 == 0:
            while True:
                print("Time to level up your stats! Choose 1 stat to level up twice or 2 stats to level up once.\n1. STR,  2. DEX,  3. CON,  4. INT,  5. WIS,  6. CHA")
                choice = input("Input either 1 number or 2 numbers separated by a space, associated with your choice above: ")
                if re.match(r'^[1-6]$', choice): 
                    choice = self.stat_choice[choice]
                    stat_value = getattr(self, choice)
                    setattr(self, choice, stat_value + 2)
                    break          
                elif re.match(r'^[1-6] [1-6]$', choice):
                    split_choice = choice.split(' ')
                    choice1 = split_choice[0]
                    choice2 = split_choice[1]

                    choice1 = self.stat_choice[choice1]
                    stat_value1 = getattr(self, choice1)
                    setattr(self, choice1, stat_value1 + 1)

                    choice2 = self.stat_choice[choice2]
                    stat_value2 = getattr(self, choice2)
                    setattr(self, choice2, stat_value2 + 1)
                    break
                else:
                    printwait("Please enter a valid choice.", 1)
                

        if self.character_level % 2 == 1:
            while True:
                choice = input(f"Choose a Special Ability to level up!\n1. {self.special_abilities[0]}, 2. {self.special_abilities[1]}, 3. {self.special_abilities[2]}")
                if choice in ['1', '2', '3']:
                    if self.special_abilities_dictionary[self.special_abilities[int(choice) - 1]][1] <= 2:
                        self.special_abilities_dictionary[self.special_abilities[int(choice) - 1]][1] += 1
                        break
                    else:
                        print("That Special Ability is already at max level. Please pick a different one.")
                else:
                    printwait("Please enter a valid choice.", 1)

        seperator()
        printwait("Rolling d8 hit dice...", 2)
        hp_roll = random.randint(1, 8)
        printwait(f"Rolled a {hp_roll} {get_modifier_value(self.constitution)} (CON Modifier)", 1)
        hp_roll += self.get_modifier(self.constitution)
        if hp_roll < 1:
            hp_roll = 1
        self.hit_points += hp_roll
        printwait(f"You gained {hp_roll} to your max Hit Points!\nNew Max Hit Points: {self.hit_points}")
        self.armor_class = 10 + self.get_modifier(self.dexterity)

        seperator()
        print("Character Page:")
        self.display_character()
        seperator()

    def print_inventory(self):
        start_line = f"\n===== {self.name}'s Inventory ====="
        print(start_line)
        
        # Gold Coins
        print(f"\nGold Coins: {self.inventory['gold_coins']}")
        
        # Potions
        print("\nPotions:")
        if self.inventory['potions']:
            for potion, quantity in self.inventory['potions'].items():
                if quantity > 0:
                    print(f"  {potion.name}: {quantity}")
        else:
            print("  No potions")
        
        # Weapons
        print("\nWeapons:")
        if self.inventory['weapons']:
            for weapon, quantity in self.inventory['weapons'].items():
                print(f"  {weapon.name} (x{quantity}):")
                print(f"    Damage: {weapon.damage}")
                print(f"    Type: {weapon.type}")
                print(f"    Rarity: {weapon.rarity}")
                print(f"    Required Level: {weapon.required_level}")
                print(f"    Description: {weapon.description}")
        else:
            print("  No weapons")
        
        # Misc Items
        print("\nMiscellaneous Items:")
        if self.inventory['misc']:
            for item, quantity in self.inventory['misc'].items():
                print(f"  {item}: {quantity}")
        else:
            print("  No miscellaneous items")
        end_line = ""
        for character in start_line:
            end_line += "="
        end_line = end_line[1:]
        print(f"\n{end_line}")

    def print_equipped_items(self):
        print("\n===== EQUIPPED ITEMS =====")
        
        for slot, item in self.equipped_items.items():
            print(f"\n{slot.capitalize()}:")
            if item is None:
                print("  Nothing equipped")
            elif isinstance(item, Weapon):
                print(f"  {item.name}")
                print(f"    Damage: {item.damage}")
                print(f"    Type: {item.type}")
                print(f"    Rarity: {item.rarity}")
                print(f"    Required Level: {item.required_level}")
                print(f"    Description: {item.description}")
        
        print("\n==========================")

######################################


# basic monster
class Monster:
    def __init__(self, name, damage, monster_type, loot_drops, strength, dexterity, constitution, intelligence, wisdom, charisma, experience_given: int = 0):
        self.name = name

        self.damage = damage

        self.monster_type = monster_type

        self.loot_drops = loot_drops

        self.experience_given = experience_given
        
        # core stats
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        # hit points and armor class calculations
        self.hit_points = 10 + self.get_modifier(self.constitution)
        self.armor_class = 10 + self.get_modifier(self.dexterity)

    def get_modifier(self, stat):
        modifiers = {
            range(1, 2): -5,
            range(2, 4): -4,
            range(4, 6): -3,
            range(6, 8): -2,
            range(8, 10): -1,
            range(10, 12): 0,
            range(12, 14): 1,
            range(14, 16): 2,
            range(16, 18): 3,
            range(18, 20): 4,
            range(20, 22): 5,
            range(22, 24): 6,
            range(24, 26): 7,
            range(26, 28): 8,
            range(28, 30): 9,
            range(30, 31): 10
            }
        for stat_range, modifier in modifiers.items():
            if stat in stat_range:
                return modifier
            
    def display_monster(self):
        print(f"Name: {self.name}")
        print(f"Monster Type: {self.monster_type}")
        print(f"Damage: {self.damage}")
        print(f"Strength: {self.strength} (Modifier: {get_modifier_value(self.strength)})")
        print(f"Dexterity: {self.dexterity} (Modifier: {get_modifier_value(self.dexterity)})")
        print(f"Constitution: {self.constitution} (Modifier: {get_modifier_value(self.constitution)})")
        print(f"Intelligence: {self.intelligence} (Modifier: {get_modifier_value(self.intelligence)})")
        print(f"Wisdom: {self.wisdom} (Modifier: {get_modifier_value(self.wisdom)})")
        print(f"Charisma: {self.charisma} (Modifier: {get_modifier_value(self.charisma)})")
        print(f"Hit Points (HP): {self.hit_points}")
        print(f"Armor Class (AC): {self.armor_class}")

#####################################




####################################

class Named_Monsters:
    def level_1_rat():
        randomized_gold = random.randint(1, 10)

        loot = {
            "guarenteed_loot": {'gold_coins': 5, Named_Potions.small_health_potion: 1},
            "nothing": [1, 30],
            "gold_coins": [randomized_gold, 55],
            Named_Potions.small_health_potion: [1, 15] 
        }
        
        level_1_rat = Monster('Putrid Rat', '1d4 - 1', 'Rodent', loot, 3, 3, 5, 1, 1, 1, 25)
        return level_1_rat
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    def level_1_guard(enraged: bool = False):
        randomized_gold = random.randint(5, 20)

        loot = {
            "guarenteed_loot": {'gold_coins': 10, Named_Potions.small_defense_potion: 1},
            "nothing": [1, 20],
            "gold_coins": [randomized_gold, 60],
            Named_Potions.small_defense_potion: [1, 20]
        }

        if enraged:
            level_1_guard = Monster('Enraged Guard', '1d4 + 1', 'Human', loot, 8, 4, 8, 1, 1, 1, 50)
        else:
            level_1_guard = Monster('Guard', '1d4 + 1', 'Human', loot, 6, 3, 6, 1, 1, 1, 40)
        return level_1_guard
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    def level_1_goblin():
        randomized_gold = random.randint(2, 25)

        loot = {
            "guarenteed_loot": {'gold_coins': 10, Named_Potions.small_attack_potion: 1},
            "nothing": [1, 25],
            "gold_coins": [randomized_gold, 65],
            Named_Potions.small_attack_potion: [1, 10]
        }

        goblin = Monster('Mischievous Goblin', '1d6', 'Goblin', loot, 7, 4, 6, 2, 1, 1, 35)
        return goblin
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    def tormund_the_repears_herald(gem_in_inv: bool = True):
        tormunds_greatsword = Named_Weapons.tormunds_greatsword
        randomized_gold = random.randint(35, 65)
        
        if gem_in_inv:
            loot = {
                "guarenteed_loot": {'gold_coins': 40, Named_Potions.small_health_potion: 2, Named_Potions.small_attack_potion: 2, Named_Potions.small_defense_potion: 2},
                "nothing": [1, 0],
                "gold_coins": [randomized_gold, 30],
                Named_Potions.small_health_potion: [2, 30], 
                Named_Potions.small_attack_potion: [2, 15], 
                Named_Potions.small_defense_potion: [2, 5],
                Named_Weapons.tormunds_greatsword: [1, 20]
            }
        else:
            loot = {
                "guarenteed_loot": {'Mysterious Gem': 1, 'gold_coins': 40, Named_Potions.small_health_potion: 2, Named_Potions.small_attack_potion: 2, Named_Potions.small_defense_potion: 2},
                "nothing": [1, 0],
                "gold_coins": [randomized_gold, 30],
                Named_Potions.small_health_potion: [2, 30], 
                Named_Potions.small_attack_potion: [2, 15], 
                Named_Potions.small_defense_potion: [2, 5],
                Named_Weapons.tormunds_greatsword: [1, 20]
            }

        tormund = Monster("Tormund, the Reaper's Herald", '1d6 + 2', 'Human', loot, 14, 10, 14, 8, 8, 8, 300)
        return tormund
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    