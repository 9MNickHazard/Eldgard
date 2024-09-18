import time
import random
import re

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

def get_modifier_value(stat):
        for stat_range, modifier in modifiers.items():
            if stat in stat_range:
                return f"+{modifier}" if modifier > 0 else str(modifier)
            

            
class Monster:
    def __init__(self, name, damage, monster_type, loot_drops, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name

        self.damage = damage

        self.monster_type = monster_type

        self.loot_drops = loot_drops
        
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

    
            
    



class Character:
    def __init__(self, name, role, pronouns, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.role = role
        self.pronouns = pronouns
        
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
        for stat_range, modifier in modifiers.items():
            if stat in stat_range:
                return modifier
    


    def display_character(self):
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Strength: {self.strength} (Modifier: {get_modifier_value(self.strength)})")
        print(f"Dexterity: {self.dexterity} (Modifier: {get_modifier_value(self.dexterity)})")
        print(f"Constitution: {self.constitution} (Modifier: {get_modifier_value(self.constitution)})")
        print(f"Intelligence: {self.intelligence} (Modifier: {get_modifier_value(self.intelligence)})")
        print(f"Wisdom: {self.wisdom} (Modifier: {get_modifier_value(self.wisdom)})")
        print(f"Charisma: {self.charisma} (Modifier: {get_modifier_value(self.charisma)})")
        print(f"Hit Points (HP): {self.hit_points}")
        print(f"Armor Class (AC): {self.armor_class}")


    weapon = {
        'name': 'none',
        'damage': '1d4 + 1',
        'type': 'none',
        'rarity': 'none',
        'required_level': 'none',
        'description': 'none',
        'value': 'none',
    }

    inventory = {
        'gold_coins': 0,
        'potions': {'small_health_potion': 0, 'small_attack_potion': 0, 'small_defense_potion': 0},
        'weapons': {}
    }

    character_level = 1

    evil_rating = 0

    good_rating = 0




def roll_stat(stat) -> int:
    print(f"Rolling your {stat}...")
    time.sleep(1)
    stat1 = random.randint(1, 6)
    print(f"Your first d6 roll is {stat1}")
    time.sleep(1)
    stat2 = random.randint(1, 6)
    print(f"Your second d6 roll is {stat2}")
    time.sleep(1)
    stat3 = random.randint(1, 6)
    print(f"Your third d6 roll is {stat3}")
    time.sleep(1)
    stat4 = random.randint(1, 6)
    print(f"Your fourth d6 roll is {stat4}")
    time.sleep(1)

    rolls = [stat1, stat2, stat3, stat4]
    lowest_stat_roll = min(rolls)
    rolls.remove(lowest_stat_roll)
    total_stat_roll = sum(rolls)
    print(f"Your final combined roll for {stat} is {total_stat_roll}.")

    return total_stat_roll


def seperator():
    print("------------------------------------")


def roll_stat_check_d20(character: Character, target: int, stat: str, additional_modifier: int) -> bool:
    stat_value = getattr(character, stat)
    modifier = character.get_modifier(stat_value)

    check = random.randint(1, 20)
    print(f"You rolled a {check} ({get_modifier_value(stat_value)} from your {stat}).")
    seperator()
    check += modifier
    check += additional_modifier

    if check >= target:
        print(f"Your total roll of {check} succeded! You passed the {stat} check!")
        return True
    else:
        print(f"Your total roll of {check} was a failure... You failed the {stat} check...")
        return False
    

def roll_1v1_initiative(monster: Monster, character: Character) -> str:
    while True:
        monster_initiative = random.randint(1, 20)
        monster_initiative += monster.get_modifier(monster.dexterity)
        character_initiative = random.randint(1, 20)
        character_initiative += character.get_modifier(character.dexterity)

        if monster_initiative < 0:
            monster_initiative = 0

        if character_initiative < 0:
            character_initiative = 0

        seperator()
        print(f"Rolling {monster.name}'s initiative...")
        time.sleep(1)
        print(f"{monster.name} rolled a {monster_initiative}")
        seperator()
        time.sleep(2)
        print(f"Rolling {character.name}'s initiative...")
        time.sleep(1)
        print(f"{character.name} rolled a {character_initiative}")
        seperator()
        time.sleep(2)

        if character_initiative > monster_initiative:
            print(f"Congrats! {character.name} gets to go first!")
            return 'character'
        elif monster_initiative > character_initiative:
            print(f"Unlucky... {monster.name} gets to go first.")
            return 'monster'
        else:
            print("It's a tie! Rerolling...")
            time.sleep(2)


def roll_flee_check(monster: Monster, character: Character, is_fleeing_possible: bool) -> bool:
    if is_fleeing_possible:
        monster_flee_check = random.randint(1, 20)
        monster_flee_check += monster.get_modifier(monster.dexterity)
        character_flee_check = random.randint(1, 20)
        character_flee_check += character.get_modifier(character.dexterity)
        seperator()
        print(f"Rolling {monster.name}'s flee check...")
        time.sleep(1)
        print(f"{monster.name} rolled a {monster_flee_check}")
        seperator()
        time.sleep(2)
        print(f"Rolling {character.name}'s flee check...")
        time.sleep(1)
        print(f"{character.name} rolled a {character_flee_check}")
        seperator()
        time.sleep(2)

        if character_flee_check > monster_flee_check:
            print(f"You succesfully slip away from the {monster.name}.")
            return True
        elif monster_flee_check > character_flee_check:
            print(f"Unlucky... The {monster.name} prevents you from escaping.")
            return False
        else:
            print("It's a tie! Rerolling...")
            time.sleep(2)
            roll_1v1_initiative(monster, character)

    else:
        print("You cannot run from this battle.")
        return False



def roll_damage_value(damage: str) -> int:
    pattern = r'(\d+)d(\d+)\s*([-+])?\s*(\d+)?'

    match = re.match(pattern, damage)

    number_of_dice = int(match.group(1))
    dice_type = int(match.group(2))
        
    if match.group(3) and match.group(4):
        modifier = int(match.group(4))
        if match.group(3) == '-':
            modifier = -modifier
    else:
        modifier = 0

    total_damage = 0

    print(f"Rolling {damage}...")
    time.sleep(1)

    for i in range(number_of_dice):
        roll = random.randint(1, dice_type)
        print(f"The roll is a {roll}.")
        time.sleep(1)
        total_damage += roll

    total_damage_plus_modifier = total_damage + modifier
    time.sleep(1)
    print(f"The sum of all rolls ({total_damage}) plus the modifier ({modifier}) is: {total_damage_plus_modifier}.")

    return total_damage_plus_modifier


archer_special_abilities = ['Blinding Shot', 'Armor Piercing Arrow', 'Nimble Steps']
knight_special_abilities = ['Heavy Armor', 'Resilience', 'Big Swing']
wizard_special_abilities = ['Spellcasting', 'Magic Shield', 'Polymorph']

# Blinding Shot: Fire a special arrow that reduces the enemy's attack roll by 3 for the next 3 turns
# Armor Piercing Arrow: Ignore enemy's Armor Class for an attack
# Nimble Steps: Periodically succeed 100 percent on Dexterity checks
# Heavy Armor: Reduced damage from non-magical damage sources
# Resilience: Recover a certain amount of hitpoints
# Big Swing: Deal double damage, but add +3 to your enemy's next attack roll
# Spellcasting: Access to various help spells
# Magic Shield: Increased Armor Class for a turn
# Polymorph: Ability to change an enemy/npc into a harmless creature       
    



def combat_1v1(monster: Monster, character: Character, initiative: str, flee_possibility: bool) -> str:
    seperator()
    print(f"---BATTLE START!---")
    time.sleep(1)
    print(f"{character.name} vs {monster.name}")
    seperator()
    time.sleep(1)

    monster_hp = monster.hit_points
    character_hp = character.hit_points

    if initiative == 'character':
        while monster_hp > 0 and character_hp > 0:
            print("---Your Turn---")
            player_turn_result = player_turn_1v1(monster, character, flee_possibility)
            if isinstance(player_turn_result, int):
                monster_hp -= player_turn_result
            elif player_turn_result == 'fled':
                return 'fled'
            elif player_turn_result == 'trapped':
                continue
            else:
                print(f"Unknown Action: {player_turn_result}")

            if monster_hp <= 0:
                break

            time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            time.sleep(2)
            
            monster_turn_result = monster_turn_1v1(monster, character)
            character_hp -= monster_turn_result 

            time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            time.sleep(2)

        if monster_hp <= 0:
            return 'player_win'
        if character_hp <= 0:
            return 'monster_win'

    elif initiative == 'monster':
        while monster_hp > 0 and character_hp > 0:
            monster_turn_result = monster_turn_1v1(monster, character)
            character_hp -= monster_turn_result 

            if character_hp <= 0:
                break

            time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            time.sleep(2)

            print("---Your Turn---")
            player_turn_result = player_turn_1v1(monster, character, flee_possibility)
            if isinstance(player_turn_result, int):
                monster_hp -= player_turn_result
            elif player_turn_result == 'fled':
                return 'fled'
            elif player_turn_result == 'trapped':
                continue
            else:
                print(f"Unknown Action: {player_turn_result}")

            time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            time.sleep(2)

        if monster_hp <= 0:
            return 'player_win'
        if character_hp <= 0:
            return 'monster_win'


    else:
        print(f"Unknown Initiative Value: {initiative}")


            
def monster_turn_1v1(monster: Monster, character: Character) -> int:
    print(f"---{monster.name}'s Turn---")
    monster_attack_roll = random.randint(1, 20)
    time.sleep(3)
    print(f"{monster.name} rolling vs your AC ({character.armor_class})...")
    time.sleep(3)

    if monster_attack_roll == 20:
        monster_crit_damage = roll_damage_value(monster.damage)
        monster_crit_damage += monster_crit_damage
        print(f"The {monster.name} rolls a natural 20, critical hit! You take double damage...")
        time.sleep(3)
        print(f"The {monster.name} deals {monster_crit_damage} damage to you.")
        return monster_crit_damage
    
    monster_attack_roll += monster.get_modifier(monster.strength)

    if monster_attack_roll >= character.armor_class:
        print(f"The {monster.name} successfully hits you.")
        monster_damage = roll_damage_value(monster.damage)
        print(f"The {monster.name} deals {monster_damage} to you. Ouch!")
        return monster_damage
    else:
        print(f"The {monster.name} strikes at you, but you parry it expertly. You take no damage this turn!")
        return 0


def player_turn_1v1(monster: Monster, character: Character, flee_possibility: bool):
    while True:
        choice = input("Choices: 1. Attack, 2. Special Ability, 3. Use an Item, 4. Attempt to Flee. Please pick an action (enter the number of your choice): ")
        if choice == '1':
            attack_roll = random.randint(1, 20)
            if character.role.lower() == 'archer':
                if attack_roll == 20:
                    print(f"You fire a projectile at the {monster.name}...")
                    time.sleep(3)
                    print(f"You roll a natural 20! Critical hit! Your arrow hits the {monster.name} going straight through it, rips a hole in spacetime, travels through a wormhole in the 5th dimension and plunges itself again deep within the shocked {monster.name}!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    print(f"You do double damage! You deal {crit_damage} damage to the {monster.name}!")
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.dexterity)
                    print(f"You fire a projectile at the {monster.name}...")
                    time.sleep(3)
                    if attack_roll >= monster.armor_class:
                        print("It's a hit!")
                        damage = roll_damage_value(character.weapon['damage'])
                        print(f"You deal {damage} damage to the {monster.name}.")
                        return damage
                    else:
                        print("A child would have got closer to the target than that shot... You deal no damage this turn.")
                        return 0
            elif character.role.lower() == 'knight':
                if attack_roll == 20:
                    print(f"You swing your weapon at the {monster.name}...")
                    time.sleep(3)
                    print(f"You roll a natural 20! Critical hit! Your weapon strikes the {monster.name} with such tremendous force that it creates gravitons, temporarily altering gravity. The {monster.name} is lifted off its feet, spun around by the cosmic disturbance, only to be slammed back down onto your waiting blade!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.strength)
                    print(f"You swing your weapon at the {monster.name}...")
                    time.sleep(3)
                    if attack_roll >= monster.armor_class:
                        print("It's a hit!")
                        damage = roll_damage_value(character.weapon['damage'])
                        print(f"You deal {damage} damage to the {monster.name}.")
                        return damage
                    else:
                        print("You swing and miss, falling flat on your face... You deal no damage this turn.")
                        return 0
            elif character.role.lower() == 'wizard':
                if attack_roll == 20:
                    print(f"You cast a spell at the {monster.name}...")
                    time.sleep(3)
                    print(f"You roll a natural 20! Critical hit! Your spell engulfs the {monster.name} in a dazzling vortex of arcane energy, briefly phasing it out of reality. The {monster.name} reappears a second later, looking bewildered and smoking, as if it had been subjected to the heat death and rebirth of several universes in the blink of an eye!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.intelligence)
                    print(f"You cast a spell at the {monster.name}...")
                    time.sleep(3)
                    if attack_roll >= monster.armor_class:
                        print("It's a hit!")
                        damage = roll_damage_value(character.weapon['damage'])
                        print(f"You deal {damage} damage to the {monster.name}.")
                        return damage
                    else:
                        print("Your spell fizzles out pathetically... You deal no damage this turn.")
                        return 0
            else:
                print(f"Unknown Class: {character.role}")

            
        elif choice == '2':
            if character.role.lower() == 'archer':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({archer_special_abilities[0]}, {archer_special_abilities[1]}, {archer_special_abilities[2]}): ").lower()
                    if spec_ability in [archer_special_abilities[0].lower(), archer_special_abilities[1].lower(), archer_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'blinding shot':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'blinding shot':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'nimble steps':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    player_turn_1v1(monster, character)
                else:
                    print("Unknown Special Ability")
            
            if character.role.lower() == 'knight':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({knight_special_abilities[0]}, {knight_special_abilities[1]}, {knight_special_abilities[2]}): ").lower()
                    if spec_ability in [knight_special_abilities[0].lower(), knight_special_abilities[1].lower(), knight_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'heavy armor':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'resilience':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'big swing':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                else:
                    print("Unknown Special Ability")

            if character.role.lower() == 'wizard':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({wizard_special_abilities[0]}, {wizard_special_abilities[1]}, {wizard_special_abilities[2]}): ").lower()
                    if spec_ability in [wizard_special_abilities[0].lower(), wizard_special_abilities[1].lower(), wizard_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'spellcasting':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'magic shield':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                elif spec_ability == 'polymorph':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    player_turn_1v1(monster, character)
                else:
                    print("Unknown Special Ability")

            else:
                print(f"Unknown Class: {character.role}")

        elif choice == '3':
            print(character.inventory)
            seperator()
            time.sleep(1)
            print("Use Item not yet implemented...")
            seperator()
            player_turn_1v1(monster, character)
        
        elif choice == '4':
            print("Flee checks are based on the Dexterity modifier of the monster and the player.")
            flee_check = roll_flee_check(monster, character, flee_possibility)
            if flee_check == True:
                return 'fled'
            else:
                return 'trapped'

        
        else:
            print("Please enter a valid response.")
            



def main():
    death_status = False
    
    while not death_status:
        print("Welcome to Eldgard! You will be embarking on a text rpg journey through this fantasy medieval land!")
        seperator()
        time.sleep(.7)
        print("EEEEE  L       DDDD     GGGG    AAAAA  RRRRR   DDDD")
        time.sleep(.7)
        print("E      L       D   D   G        A   A  R   R   D   D")
        time.sleep(.7)
        print("EEEEE  L       D   D   G  GG    AAAAA  RRRRR   D   D")
        time.sleep(.7)
        print("E      L       D   D   G   G    A   A  R R     D   D")
        time.sleep(.7)
        print("EEEEE  LLLLLL  DDDD     GGGG    A   A  R  RR   DDDD")
        seperator()
        time.sleep(2)

        print("Lets roll your stats!")
        seperator()
        print("On this adventure you will have 6 main stats: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. You will also have the chance to name your character and pick from one of the 3 classes: Archer, Knight, Wizard")
        seperator()
        time.sleep(1)
        print("Each stat will be randomly generated by rolling 4d6, removing the lowest number and adding the remaining values.")
        seperator()

        while True:
            start_rolling = input("Type y then hit enter when you are ready to roll your stats: ").lower()
            if start_rolling == 'y':
                break
            print("Please type y and hit enter when you are ready to begin rolling your stats!")

        player_starting_str = roll_stat("Strength")
        seperator()
        time.sleep(.5)
        player_starting_dex = roll_stat("Dexterity")
        seperator()
        time.sleep(.5)
        player_starting_con = roll_stat("Constitution")
        seperator()
        time.sleep(.5)
        player_starting_int = roll_stat("Intelligence")
        seperator()
        time.sleep(.5)
        player_starting_wis = roll_stat("Wisdom")
        seperator()
        time.sleep(.5)
        player_starting_cha = roll_stat("Charisma")
        seperator()
        time.sleep(.5)

        print("Now it is time to pick your class!")
        time.sleep(2)
        seperator()
        print("There are three options for classes: Archer, Knight or Wizard")
        time.sleep(2)
        seperator()
        print("Here are the bonuses, usable weapons, special abilities and descriptions for each class:")
        time.sleep(3)
        seperator()

        print("Archer:")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        print("| Stat Bonuses:            Special Abilities:                                                                                    |")
        print("| Strength: -2             - Blinding Shot: Fire a special arrow that reduces the enemy's attack roll by 3 for the next 3 turns  |")
        print("| Dexterity: +3            - Armor Piercing Arrow: Ignore enemy's Armor Class for an attack                                      |")
        print("| Constitution: -1         - Nimble Steps: Periodically succeed 100 percent on Dexterity checks                                  |")
        print("| Intelligence: +0                                                                                                               |")
        print("| Wisdom: +2               Description:                                                                                          |")
        print("| Charisma: +1             A nimble and precise ranged fighter, the Archer excels at striking enemies from afar                  |")
        print("|                          with deadly accuracy. Light on defense, but unmatched in Dexterity and keen awareness.                |")
        print("| Usable Weapons:                                                                                                                |")
        print("| - Longbow                                                                                                                      |")
        print("| - Crossbow                                                                                                                     |")
        print("|                                                                                                                                |")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        

        print("Knight:")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        print("| Stat Bonuses:            Special Abilities:                                                                                    |")
        print("| Strength: +3             - Heavy Armor: Reduced damage from non-magical damage sources                                         |")
        print("| Dexterity: -2            - Resilience: Recover a certain amount of hitpoints                                                   |")
        print("| Constitution: +3         - Big Swing: Deal double damage, but add +3 to your enemy's next attack roll                          |")
        print("| Intelligence: -2                                                                                                               |")
        print("| Wisdom: +0               Description:                                                                                          |")
        print("| Charisma: +3             A powerful, heavily-armored warrior with unmatched strength and endurance. The Knight                 |")
        print("|                          thrives in close combat, absorbing damage while delivering devastating blows.                         |")
        print("| Usable Weapons:                                                                                                                |")
        print("| - Longsword                                                                                                                    |")
        print("| - Great Axe                                                                                                                    |")
        print("|                                                                                                                                |")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        

        print("Wizard:")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        print("| Stat Bonuses:            Special Abilities:                                                                                    |")
        print("| Strength: -3             - Spellcasting: Access to various help spells                                                         |")
        print("| Dexterity: +0            - Magic Shield: Increased Armor Class for a turn                                                      |")
        print("| Constitution: -2         - Polymorph: Ability to change an enemy/npc into a harmless creature                                  |")
        print("| Intelligence: +4                                                                                                               |")
        print("| Wisdom: +3               Description:                                                                                          |")
        print("| Charisma: +0             A master of arcane magic, the Wizard wields powerful spells to control the battlefield.               |")
        print("|                          Physically weak but capable of devastating magical attacks and versatile enchantments.                |")
        print("| Usable Weapons:                                                                                                                |")
        print("| - Staff                                                                                                                        |")
        print("| - Wand                                                                                                                         |")
        print("|                                                                                                                                |")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        
        time.sleep(5)

        while True:
            class_choice = input("Which class would you like to be? Please type in the name of the class and hit enter to choose: ").lower()
            if class_choice in ['archer', 'knight', 'wizard']:
                break
            print("Please enter a valid choice.")

        seperator()
        print(f"You chose {class_choice.upper()}!")
        time.sleep(1)
        seperator()

        while True:
            class_confirmation = input(f"Are you sure you want to stick with {class_choice.upper()}? Please enter y to continue or n to re-pick your class: ").lower()
            if class_confirmation == 'y':
                break
            elif class_confirmation == 'n':
                seperator()
                print("Please enter Archer, Knight or Wizard.")
                while True:
                    class_choice = input("Which class would you like to be? Please type in the name of the class and hit enter to choose: ").lower()
                    if class_choice in ['archer', 'knight', 'wizard']:
                        break
                    print("Please enter a valid choice.")
            else:
                print("Please enter y or n")

        time.sleep(1)

        seperator()
        print("What are your pronouns?")
        while True:
            pronoun_choice = input("Choices: 1. He/Him, 2. She/Her, 3. They/Them. Please input the number associated with your choice: ")
            if pronoun_choice in ['1', '2', '3']:
                break

        print("Now it is time to pick a name for your brave hero!")
        seperator()
        time.sleep(1)
            
        name_choice = str(input("Please enter your character's name: "))
        seperator()

        while True:
            name_confirmation = input(f"Are you sure you want to stick with {name_choice} as your character's name? Please enter y to continue or n to re-name your character: ").lower()
            if name_confirmation == 'y':
                break
            elif name_confirmation == 'n':
                seperator()
                name_choice = str(input("Please enter your character's name: "))
                break
            else:
                print("Please enter y or n")


        player_character = Character(name=name_choice, role=class_choice, pronouns=pronoun_choice, strength=player_starting_str, dexterity=player_starting_dex, constitution=player_starting_con, intelligence=player_starting_int, wisdom=player_starting_wis, charisma=player_starting_cha)

        seperator()
        time.sleep(1)

        print("Now lets take a look at your character!")
        player_character.display_character()
        seperator()

        while True:
            end_character_creation_choice = input("When you are ready to begin your adventure in Eldgard, type y: ").lower()
            if end_character_creation_choice == 'y':
                break
            print("Please enter y when you are ready to continue!")

        # START OF STORY

        # First Dungeon (A jail in Southwold)

        print("The Adventure Begins...")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("You awake with a splitting headache and a groggy feeling. You can still taste the alcohol from the copious amounts of meade you drink the night before.")
        seperator()
        time.sleep(2)
        print("You wearily look around. You appear to be in a dark jail cell. A few other folks are in there with you, scattered about, all still passed out.")
        seperator()
        time.sleep(2)
        print("You spy a puddle of puke in the corner of the jail cell, it makes you a bit naseous.")

        while True:
            puke_choice = input("Do you want to throw up? (Please enter y or n): ").lower()
            if puke_choice == 'y':
                seperator()
                time.sleep(2)
                print("You puke your brains out, and wipe off your mouth. You actually feel a lot better!")
                seperator()
                time.sleep(2)
                print("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.")
                seperator()
                time.sleep(2)
                print("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.")
                seperator()
                time.sleep(2)
                print("---You now need to roll a check to see if you successfully pick the guard's pocket---")
                time.sleep(2)
                print(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(player_character.dexterity)}) will be applied---")
                time.sleep(2)
                print("---If you roll above the required value, you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---")
                seperator()
                time.sleep(2)

                while True:
                    choice = input("Are you ready to roll this Dexterity check? You need a 10 or greater to pass. Please enter y when ready: ")
                    if choice == 'y':
                        break
                    print("Please enter y when ready.")

                seperator()

                while True:
                    jail_key_pickpocket_check = roll_stat_check_d20(player_character, 10, 'dexterity', 0)
                    if jail_key_pickpocket_check == True:
                        break
                    else:
                        while True:
                            choice = input("Try again? Enter y when ready: ")
                            if choice == 'y':
                                break
                            print("Please enter y when ready.")

                print("You carefully reach into the guard's pocket and snatch the cell keys. He snorts, but remains asleep.")
                break

            elif puke_choice == 'n':
                seperator()
                time.sleep(2)
                print("You hold it in... You feel quite unsettled...")
                seperator()
                time.sleep(2)
                print("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.")
                seperator()
                time.sleep(2)
                print("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.")
                seperator()
                time.sleep(2)
                print("---You now need to roll a check to see if you successfully pick the guard's pocket---")
                time.sleep(2)
                print(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(player_character.dexterity)}) will be applied---")
                time.sleep(2)
                print("---If you roll above the required value, you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---")
                time.sleep(2)
                print("For this Dexterity check you will recieve an additional -2 modifier for choosing not to throw up and feel better.")
                seperator()
                time.sleep(2)

                while True:
                    choice = input("Are you ready to roll this Dexterity check? You need a 10 or greater to pass. Please enter y or n: ")
                    if choice == 'y':
                        break
                    print("Please enter y or n")

                while True:
                    jail_key_pickpocket_check = roll_stat_check_d20(player_character, 10, 'dexterity', -2)
                    if jail_key_pickpocket_check == True:
                        break
                    else:
                        while True:
                            choice = input("Try again? Enter y when ready: ")
                            if choice == 'y':
                                break
                            print("Please enter y when ready.")

                print("You carefully reach into the guard's pocket and snatch the cell keys. He snorts, but remains asleep.")
                break
            else:
                print("Please enter y or n")

        time.sleep(2)
        print("You fumble around with the keys in the dark, but manage to find the correct key to the jail cell.")
        seperator()
        time.sleep(2)
        print("You quietly unlock the jail cell door and slip out. As you close the door behind you, you hear a small grunt from the guard...")
        seperator()
        time.sleep(2)
        print("...But it's just him dreaming. You quietly slink down the hallway. You come to an intersection...")
        seperator()
        time.sleep(2)
        print("...to the left you hear the faint muttering of some guards and the periodic hearty chuckle. To the right you here the scuttle of small claws on the stone floor.")
        seperator()
        time.sleep(2)


        first_dungeon_rat_loot = random.randint(1, 10)
        first_dungeon_rat_chance_of_nothing = random.randint(15, 30)
        first_dungeon_rat = Monster('Putrid Rat', '1d4 - 1', 'Rodent', {'gold_coins': first_dungeon_rat_loot, 'chance_of_nothing': first_dungeon_rat_chance_of_nothing}, 3, 3, 5, 1, 1, 1)

        while True:
            starting_dungeon_first_choice = input("Which path do you take? Type left or right: ")
            if starting_dungeon_first_choice == 'right':
                seperator()
                time.sleep(2)
                print("You go right and walk down the dark corridor. You turn around a corner and come face to face with the biggest rat you've ever seen in your life...")
                seperator()
                time.sleep(2)
                print("---It's time for your first battle!---")
                time.sleep(2)
                print("---If you die in battle, you will have to restart the entire game! Be careful!---")
                time.sleep(2)
                print("---You and the rat will take turns doing actions. In a turn you can either decide to Attack, Use a Special Ability, Use an Item, or (in some cases) Attempt to Flee (DEX check)---")
                time.sleep(2)
                print("---if you attack, you will roll a d20, applying your class's respective modifier (DEX for Archer, STR for Knight, INT for Wizard) against the enemy's Armor Class (AC)---")
                time.sleep(2)
                print("---If your attack roll is successful, you will do damage based on your weapon (default damage with no weapon is 1d4 + 1)---")
                time.sleep(2)
                print("---It will then be the enemy's turn. Most monsters will just attack, but some higher level monsters may take other actions---")
                seperator()
                time.sleep(2)

                while True:
                    choice = input("Are you ready to fight the Rat? Please enter y when ready: ")
                    if choice == 'y':
                        break
                    print("Please enter y when ready.")

                time.sleep(2)

                print("First, initiative will be rolled for both you and the monster. Your Dexterity modifier is applied to this roll. The one with the highest roll will go first.")
                time.sleep(2)
                initiative = roll_1v1_initiative(first_dungeon_rat, player_character)
                time.sleep(2)
                battle_result = combat_1v1(first_dungeon_rat, player_character, initiative, True)

                seperator()
                time.sleep(2)

                if battle_result == 'player_win':
                    loot_roll = random.randint(1, 100)
                    if loot_roll in range(1, first_dungeon_rat.loot_drops['chance_of_nothing'] + 1):
                        print(f"You slay the {first_dungeon_rat.name}! You look around the corpse, but unfortunately find no loot worth keeping...")
                        time.sleep(3)
                        print(f"---Here is your inventory---")
                        print(player_character.inventory)
                        seperator()
                        break
                    else:
                        print(f"You slay the {first_dungeon_rat.name}! Your loot the body and find {first_dungeon_rat.loot_drops['gold_coins']} Gold Coins! You put the gold in your pocket.")
                        player_character.inventory["gold_coins"] += first_dungeon_rat.loot_drops["gold_coins"]
                        time.sleep(3)
                        print(f"---Here is your inventory---")
                        print(player_character.inventory)
                        seperator()
                        break

                elif battle_result == 'monster_win':
                    death_status = True
                    print("---You have died. GAME OVER---")
                    break

                elif battle_result == 'fled':
                    break




            elif starting_dungeon_first_choice =='left':
                seperator()
                print("You go left and walk down the dark corridor. The muffled voices become louder and you can just barely make out what they are saying...")
                time.sleep(3)
                print(f"Guard 1: Ohhhh you should have seen this crazy {player_character.role} last night at the White Goose Tavern! They were deep in their cups, prancing on tables and bellowing some bawdy tune as if they were a drunken bard.")
                time.sleep(4)
                seperator()
                print("Guard 2: *laughs* By the gods, the state they were in last night! Half-dressed and declaring themselves ‘Champion of the White Goose,’ dancing atop the tables like they'd been crowned in a court of fools!")
                seperator()
                time.sleep(4)
                print("Guard 1: And did you notice what they had on 'em? That odd piece... Looked like a carved gem with light swirling inside, as if a small universe were trapped within. Small, but 'twas heavy as a wet hog. And I swear, it whispered when I confiscated it from him.")
                seperator()
                time.sleep(4)
                print("Guard 2: Aye, was a curious object. Luckily, it's safely locked away in the chest. *gestures to a chest sitting on the ground behind the guards*")
                seperator()
                time.sleep(3)

                print("You think to yourself, 'hmmmm I must get my gem back, I still need to deliver it to the king...'")
                while True:
                    choice = input(f"what do you want to do? 1. Attack the guards, 2. Attempt to sneak by and steal back your gem, 3. Attempt to convince them into giving back your gem. Please choose the number associated with your choice: ")
                    seperator()
                    if choice == '1':
                        player_character.evil_rating += 1
                        if player_character.role == 'archer':
                            print("You quietly knock an arrow, draw your bow and let it fly. It strikes the closer guard and he crumples to the floor.")
                            print("The other guard screams in rage, looking around frantically. He spots you lurking and the shadows and charges, drawing his sword. 'YOU BASTARD!' he cries out...")
                            seperator()
                            break
                        elif player_character.role == 'knight':
                            print("You quietly draw your sword, and stealthily creep up to the closer guard. You shove your blade in his back, he crumples to the floor.")
                            print("The other guard, who was deep in his goblet, sputters up meade as he sees his friend all of the sudden on the ground. He tosses his drink, drawing his sword. 'YOU BASTARD!' he shouts, as he charges you...")
                            seperator()
                            break
                        elif player_character.role == 'wizard':
                            print("You quietly raise your staff, and loose a potent magic dart. It strikes the closer guard and he crumples to the floor.")
                            print("The other guard screams in rage, looking around frantically. He spots you lurking and the shadows and charges, drawing his sword. 'YOU BASTARD!' he cries out...")
                            seperator()
                            break
                        else:
                            print("Unknown Class")

                    elif choice == '2':
                        print("You attempt to sneak around the edge of the room in the shadows, but immediately knock into some iron armor strewn on the floor. 'Shit...' you mutter under your breath, but it's too late, the guards spot you...")
                        time.sleep(4)
                        print(f"Guard 1: Oi! It's {player_character.name} the {player_character.role} from last night! What're ya doing out your cell?! Come here...")
                        break

                    elif choice == '3':
                        print("---For some options, you will roll a Charisma (CHA) check, based on your Charisma modifier---")
                        time.sleep(3)
                        print("---In this instance, you will gain an additional modifier depending on your answer to the earlier puke option, when you first awoke in your cell---")
                        time.sleep(4)
                        print("---You must beat a 12 to succeed on this check (note that this threshold for success will not always be displayed)---")
                        time.sleep(3)

                        while True:
                            cha_check_choice = input("Are you ready to roll the Charisma check? Please enter y when ready: ")
                            if cha_check_choice == 'y':
                                break
                            print("Please enter y when ready.")

                        if puke_choice =='y':
                            cha_check = roll_stat_check_d20(player_character, 12, 'charisma', 2)
                        elif puke_choice =='n':
                            cha_check = roll_stat_check_d20(player_character, 12, 'charisma', -2)
                        else:
                            cha_check = roll_stat_check_d20(player_character, 12, 'charisma', 0)

                        if cha_check == True:
                            player_character.good_rating += 1
                            print("You brush off the stone dust on your clothes, stand up straight and walk into the light.")
                            time.sleep(3)
                            print("You say with confidence, 'Ahhh my good fellows, Olgur just let me out, I've come to collect my personal belongings and be on my merry way!'")
                            time.sleep(3)
                            print(f"Guard 1: Ayee, that time already? Gloevar, grab {player_character.name}'s belongs out the chest behind ye. {player_character.name}, maybe lay off the meade next time. Trot on now.")
                            time.sleep(3)
                            print("Gloevar hands you your belongings, including your gem.")
                            time.sleep(3)
                            print("You do a slight bow and walk briskly to the door on the other side of the room.")
                            time.sleep(2)
                            print(f"As you put your hand on door handle, you hear a yell from near where you came from, 'Oi!! Stop that {player_character.role}! They stole my keys!!'")
                            time.sleep(3)
                            print("Before you are able to slip out the door, you feel a rough hand grab your collar and whip you around. 'Think we're stupid or something?!' Gloevar says mockingly...")
                            break

                        else:
                            print("You brush off the stone dust on your clothes, stand up straight and walk into the light.")
                            time.sleep(3)
                            print("You say with confidence, 'Ahhh my good fellows, Olgur just let me out, I've come to collect my personal belongings and be on my merry way!'")
                            time.sleep(3)
                            print(f"Guard 1: 'Oi! {player_character.name}, you shouldn't be out yer cell yet! Get over here...'")
                            break

                            
                    else:
                        print("Please input 1, 2 or 3.")

                seperator()
                print("---It's time for your first battle!---")
                time.sleep(3)
                print("---If you die in battle, you will have to restart the entire game! Be careful!---")
                time.sleep(3)
                print("---You and the rat will take turns doing actions. In a turn you can either decide to Attack, Use a Special Ability, Use an Item, or (in some cases) Attempt to Flee (DEX check)---")
                time.sleep(3)
                print("---if you attack, you will roll a d20, applying your class's respective modifier (DEX for Archer, STR for Knight, INT for Wizard) against the enemy's Armor Class (AC)---")
                time.sleep(3)
                print("---If your attack roll is successful, you will do damage based on your weapon (default damage with no weapon is 1d4 + 1)---")
                time.sleep(3)
                print("---It will then be the enemy's turn. Most monsters will just attack, but some higher level monsters may take other actions---")
                seperator()
                time.sleep(3)

                # generating guard's monster class
                first_dungeon_guard_loot = random.randint(5, 20)
                first_dungeon_guard_chance_of_nothing = random.randint(10, 25)

                while True:
                    choice = input("Are you ready to fight the Guard? Please enter y when ready: ")
                    if choice == 'y':
                        break
                    print("Please enter y when ready.")

                time.sleep(2)

                if choice == '1':
                    first_dungeon_enraged_guard = Monster('Enraged Guard', '1d4 + 1', 'Human', {'gold_coins': first_dungeon_guard_loot, 'chance_of_nothing': first_dungeon_guard_chance_of_nothing}, 8, 4, 8, 1, 1, 1)
                    print("First, initiative will be rolled for both you and your opponent. Your Dexterity modifier is applied to this roll. The one with the highest roll will go first.")
                    time.sleep(2)
                    initiative = roll_1v1_initiative(first_dungeon_enraged_guard, player_character)
                    time.sleep(2)
                    battle_result = combat_1v1(first_dungeon_enraged_guard, player_character, initiative, False)

                    if battle_result == 'player_win':
                        loot_roll = random.randint(1, 100)
                        if loot_roll in range(1, first_dungeon_enraged_guard.loot_drops['chance_of_nothing'] + 1):
                            print(f"You slay the {first_dungeon_enraged_guard.name}! You look around the corpse, but unfortunately find no loot worth keeping...")
                            time.sleep(3)
                            print(f"---Here is your inventory---")
                            print(player_character.inventory)
                            seperator()
                            break
                        else:
                            print(f"You slay the {first_dungeon_enraged_guard.name}! Your loot the body and find {first_dungeon_enraged_guard.loot_drops['gold_coins']} Gold Coins! You put the gold in your pocket.")
                            player_character.inventory["gold_coins"] += first_dungeon_enraged_guard.loot_drops["gold_coins"]
                            time.sleep(3)
                            print("You defeat the first guard so handedly, that the other guard drops his weapon, shaking. As he flees, you can see a wet spot forming in his pants...")
                            time.sleep(3)
                            print(f"---Here is your inventory---")
                            print(player_character.inventory)
                            seperator()
                            break

                    elif battle_result == 'monster_win':
                        death_status = True
                        print("---You have died. GAME OVER---")
                        break
                else:
                    first_dungeon_guard = Monster('Enraged Guard', '1d4 + 1', 'Human', {'gold_coins': first_dungeon_guard_loot, 'chance_of_nothing': first_dungeon_guard_chance_of_nothing}, 6, 3, 6, 1, 1, 1)
                    print("First, initiative will be rolled for both you and your opponent. Your Dexterity modifier is applied to this roll. The one with the highest roll will go first.")
                    time.sleep(2)
                    initiative = roll_1v1_initiative(first_dungeon_guard, player_character)
                    time.sleep(2)
                    battle_result = combat_1v1(first_dungeon_guard, player_character, initiative, False)

                    if battle_result == 'player_win':
                        loot_roll = random.randint(1, 100)
                        if loot_roll in range(1, first_dungeon_guard.loot_drops['chance_of_nothing'] + 1):
                            print(f"You slay the {first_dungeon_guard.name}! You look around the corpse, but unfortunately find no loot worth keeping...")
                            time.sleep(3)
                            print("You defeat the first guard so handedly, that the other guard drops his weapon, shaking. As he flees, you can see a wet spot forming in his pants...")
                            time.sleep(3)
                            print(f"---Here is your inventory---")
                            print(player_character.inventory)
                            seperator()
                            break
                        else:
                            print(f"You slay the {first_dungeon_guard.name}! Your loot the body and find {first_dungeon_guard.loot_drops['gold_coins']} Gold Coins! You put the gold in your pocket.")
                            player_character.inventory["gold_coins"] += first_dungeon_guard.loot_drops["gold_coins"]
                            time.sleep(3)
                            print(f"---Here is your inventory---")
                            print(player_character.inventory)
                            seperator()
                            break

                    elif battle_result == 'monster_win':
                        death_status = True
                        print("---You have died. GAME OVER---")
                        break

                seperator()
                time.sleep(2)

            else:
                print("Please enter left or right.")
                seperator()

        if death_status == True:
            break

        time.sleep(2)
        print("You walk out of the room, a bit bruised and hungover still, but alive. You think to yourself, maybe I shouldn't be picking fights in this state...")


        print("End of Beta Test")

        play_again = input("Would you like to start a new game? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()



