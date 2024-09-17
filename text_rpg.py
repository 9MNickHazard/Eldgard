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
        """Print the character's details."""
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
    def __init__(self, name, role, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.role = role
        
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
        """Print the character's details."""
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




def roll_stat(stat) -> int:
    print(f"Rolling your {stat}...")
    # time.sleep(1)
    stat1 = random.randint(1, 6)
    print(f"Your first d6 roll is {stat1}")
    # time.sleep(1)
    stat2 = random.randint(1, 6)
    print(f"Your second d6 roll is {stat2}")
    # time.sleep(1)
    stat3 = random.randint(1, 6)
    print(f"Your third d6 roll is {stat3}")
    # time.sleep(1)
    stat4 = random.randint(1, 6)
    print(f"Your fourth d6 roll is {stat4}")
    # time.sleep(1)

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
        print(f"Your roll of {check} succeded! You passed the {stat} check!")
        return True
    else:
        print(f"Your roll of {check} was a failure... You failed the {stat} check...")
        return False
    

def roll_1v1_initiative(monster: Monster, character: Character) -> str:
    monster_initiative = random.randint(1, 20)
    monster_initiative += monster.get_modifier(monster.dexterity)
    character_initiative = random.randint(1, 20)
    character_initiative += character.get_modifier(character.dexterity)
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
        roll_1v1_initiative(monster, character)


def roll_flee_check(monster: Monster, character: Character) -> bool:
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
    



def combat_1v1(monster: Monster, character: Character, initiative: str) -> str:
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
            player_turn_result = player_turn_1v1(monster, character)
            if isinstance(player_turn_result, int):
                monster_hp -= player_turn_result
            elif player_turn_result == 'fled':
                return 'fled'
            elif player_turn_result == 'trapped':
                continue
            else:
                print(f"Unknown Action: {player_turn_result}")

            if monster_hp or character_hp < 0:
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

            if monster_hp or character_hp < 0:
                break

            time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            time.sleep(2)

            print("---Your Turn---")
            player_turn_result = player_turn_1v1(monster, character)
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
    print(f"{monster.name} rolling vs your AC ({character.armor_class})...")
    time.sleep(2)

    if monster_attack_roll == 20:
        monster_crit_damage = roll_damage_value(monster.damage)
        monster_crit_damage += monster_crit_damage
        print(f"The {monster.name} rolls a natural 20, critical hit! You take double damage...")
        time.sleep(2)
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


def player_turn_1v1(monster: Monster, character: Character):
    while True:
        choice = input("Choices: 1. Attack, 2. Special Ability, 3. Use an Item, 4. Attempt to Flee. Please pick an action (enter the number of your choice): ")
        if choice == '1':
            attack_roll = random.randint(1, 20)
            if character.role.lower() == 'archer':
                if attack_roll == 20:
                    print(f"You fire a projectile at the {monster.name}...")
                    time.sleep(2)
                    print(f"You roll a natural 20! Critical hit! Your arrow hits the {monster.name} going straight through it, rips a hole in spacetime, travels through a wormhole in the 5th dimension and plunges itself again deep within the shocked {monster.name}!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    print(f"You do double damage! You deal {crit_damage} damage to the {monster.name}!")
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.dexterity)
                    print(f"You fire a projectile at the {monster.name}...")
                    time.sleep(2)
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
                    time.sleep(2)
                    print(f"You roll a natural 20! Critical hit! Your weapon strikes the {monster.name} with such tremendous force that it creates gravitons, temporarily altering gravity. The {monster.name} is lifted off its feet, spun around by the cosmic disturbance, only to be slammed back down onto your waiting blade!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.strength)
                    print(f"You swing your weapon at the {monster.name}...")
                    time.sleep(2)
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
                    time.sleep(2)
                    print(f"You roll a natural 20! Critical hit! Your spell engulfs the {monster.name} in a dazzling vortex of arcane energy, briefly phasing it out of reality. The {monster.name} reappears a second later, looking bewildered and smoking, as if it had been subjected to the heat death and rebirth of several universes in the blink of an eye!")
                    crit_damage = roll_damage_value(character.weapon['damage'])
                    crit_damage += crit_damage
                    return crit_damage
                else:
                    attack_roll += character.get_modifier(character.intelligence)
                    print(f"You cast a spell at the {monster.name}...")
                    time.sleep(2)
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
            flee_check = roll_flee_check(monster, character)
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
        # time.sleep(.7)
        print("EEEEE  L       DDDD     GGGG    AAAAA  RRRRR   DDDD")
        # time.sleep(.7)
        print("E      L       D   D   G        A   A  R   R   D   D")
        # time.sleep(.7)
        print("EEEEE  L       D   D   G  GG    AAAAA  RRRRR   D   D")
        # time.sleep(.7)
        print("E      L       D   D   G   G    A   A  R R     D   D")
        # time.sleep(.7)
        print("EEEEE  LLLLLL  DDDD     GGGG    A   A  R  RR   DDDD")
        seperator()
        # time.sleep(2)

        print("Lets roll your stats!")
        seperator()
        print("On this adventure you will have 6 main stats: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. You will also have the chance to name your character and pick from one of the 3 classes: Archer, Knight, Wizard")
        seperator()
        # time.sleep(1)
        print("Each stat will be randomly generated by rolling 4d6, removing the lowest number and adding the remaining values.")
        seperator()

        while True:
            start_rolling = input("Type y then hit enter when you are ready to roll your stats: ").lower()
            if start_rolling == 'y':
                break
            print("Please type y and hit enter when you are ready to begin rolling your stats!")

        player_starting_str = roll_stat("Strength")
        seperator()
        # time.sleep(.5)
        player_starting_dex = roll_stat("Dexterity")
        seperator()
        # time.sleep(.5)
        player_starting_con = roll_stat("Constitution")
        seperator()
        # time.sleep(.5)
        player_starting_int = roll_stat("Intelligence")
        seperator()
        # time.sleep(.5)
        player_starting_wis = roll_stat("Wisdom")
        seperator()
        # time.sleep(.5)
        player_starting_cha = roll_stat("Charisma")
        seperator()
        # time.sleep(.5)

        print("Now it is time to pick your class!")
        # time.sleep(2)
        seperator()
        print("There are three options for classes: Archer, Knight or Wizard")
        # time.sleep(2)
        seperator()
        print("Here are the bonuses, usable weapons, special abilities and descriptions for each class:")
        # time.sleep(3)
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
        
        # time.sleep(5)

        while True:
            class_choice = input("Which class would you like to be? Please type in the name of the class and hit enter to choose: ").lower()
            if class_choice in ['archer', 'knight', 'wizard']:
                break
            print("Please enter a valid choice.")

        seperator()
        print(f"You chose {class_choice.upper()}!")
        # time.sleep(1)
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

        # time.sleep(1)

        seperator()
        print("Now it is time to pick a name for your brave hero!")
        seperator()
        # time.sleep(1)
            
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


        player_character = Character(name=name_choice, role=class_choice, strength=player_starting_str, dexterity=player_starting_dex, constitution=player_starting_con, intelligence=player_starting_int, wisdom=player_starting_wis, charisma=player_starting_cha)

        seperator()
        # time.sleep(1)

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
        # time.sleep(2)
        print("...")
        # time.sleep(2)
        print("...")
        # time.sleep(2)
        print("You awake with a splitting headache and a groggy feeling. You can still taste the alcohol from the copious amounts of meade you drink the night before.")
        seperator()
        # time.sleep(2)
        print("You wearily look around. You appear to be in a dark jail cell. A few other folks are in there with you, scattered about, all still passed out.")
        seperator()
        # time.sleep(2)
        print("You spy a puddle of puke in the corner of the jail cell, it makes you a bit naseous.")

        while True:
            puke_choice = input("Do you want to throw up? (Please enter y or n): ").lower()
            if puke_choice == 'y':
                seperator()
                # time.sleep(2)
                print("You puke your brains out, and wipe off your mouth. You actually feel a lot better!")
                seperator()
                # time.sleep(2)
                print("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.")
                seperator()
                # time.sleep(2)
                print("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.")
                seperator()
                # time.sleep(2)
                print("---You now need to roll a check to see if you successfully pick the guard's pocket---")
                # time.sleep(2)
                print(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(player_character.dexterity)}) will be applied---")
                # time.sleep(2)
                print("---If you roll above the required value, you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---")
                seperator()
                # time.sleep(2)

                while True:
                    choice = input("Are you ready to roll this Dexterity check? You need a 10 or greater to pass. Please enter y or n: ")
                    if choice == 'y':
                        break
                    print("Please enter y or n")

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
                # time.sleep(2)
                print("You hold it in... You feel quite unsettled...")
                seperator()
                # time.sleep(2)
                print("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.")
                seperator()
                # time.sleep(2)
                print("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.")
                seperator()
                # time.sleep(2)
                print("---You now need to roll a check to see if you successfully pick the guard's pocket---")
                # time.sleep(2)
                print(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(player_character.dexterity)}) will be applied---")
                # time.sleep(2)
                print("---If you roll above the required value, you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---")
                # time.sleep(2)
                print("For this Dexterity check you will recieve an additional -2 modifier for choosing not to throw up and feel better.")
                seperator()
                # time.sleep(2)

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

        # time.sleep(2)
        print("You fumble around with the keys in the dark, but manage to find the correct key to the jail cell.")
        seperator()
        # time.sleep(2)
        print("You quietly unlock the jail cell door and slip out. As you close the door behind you, you hear a small grunt from the guard...")
        seperator()
        # time.sleep(2)
        print("...But it's just him dreaming. You quietly slink down the hallway. You come to an intersection...")
        seperator()
        # time.sleep(2)
        print("...to the left you hear the faint muttering of some guards and the periodic hearty chuckle. To the right you here the scuttle of small claws on the stone floor.")
        seperator()
        # time.sleep(2)


        first_dungeon_rat_loot = random.randint(1, 10)
        first_dungeon_rat_chance_of_nothing = random.randint(15, 30)
        first_dungeon_rat = Monster('Putrid Rat', '1d4 - 1', 'Rodent', {'gold_coins': first_dungeon_rat_loot, 'chance_of_nothing': first_dungeon_rat_chance_of_nothing}, 3, 3, 5, 1, 1, 1)

        while True:
            starting_dungeon_first_choice = input("Which path do you take? Type left or right: ")
            if starting_dungeon_first_choice == 'right':
                seperator()
                # time.sleep(2)
                print("You go right and walk down the dark corridor. You turn around a corner and come face to face with the biggest rat you've ever seen in your life...")
                seperator()
                # time.sleep(2)
                print("---It's time for your first battle!---")
                # time.sleep(2)
                print("---If you die in battle, you will have to restart the entire game! Be careful!---")
                # time.sleep(2)
                print("---You and the rat will take turns doing actions. In a turn you can either decide to Attack, Use a Special Ability, Use an Item, or (in some cases) Attempt to Flee (DEX check)---")
                # time.sleep(2)
                print("---if you attack, you will roll a d20, applying your class's respective modifier (DEX for Archer, STR for Knight, INT for Wizard) against the enemy's Armor Class (AC)---")
                # time.sleep(2)
                print("---If your attack roll is successful, you will do damage based on your weapon (default damage with no weapon is 1d4 + 1)---")
                # time.sleep(2)
                print("---It will then be the enemy's turn. Most monsters will just attack, but some higher level monsters may take other actions---")
                seperator()
                # time.sleep(2)

                while True:
                    choice = input("Are you ready to fight the Rat? Please enter y when ready: ")
                    if choice == 'y':
                        break
                    print("Please enter y when ready.")

                # time.sleep(2)

                print("First, initiative will be rolled for both you and the monster. Your Dexterity modifier is applied to this roll. The one with the highest roll will go first.")
                # time.sleep(2)
                initiative = roll_1v1_initiative(first_dungeon_rat, player_character)
                # time.sleep(2)
                battle_result = combat_1v1(first_dungeon_rat, player_character, initiative)

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
                break

            else:
                print("Please enter left or right.")
                seperator()


        time.sleep(2)
        print("You stumble out of the room, beat up and bruised. You think to yourself, maybe I shouldn't be picking fights while this hungover...")


        print("End of Beta Test")

        play_again = input("Would you like to start a new game? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()



