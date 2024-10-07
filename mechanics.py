import time
import random
import re
import copy
import math

from character_and_monsters import Character, Monster, Weapon, Potion, Named_Potions


######################################
# COMBAT MECHANICS
######################################

def initiate_combat(character: Character, monster: Monster, can_flee: bool) -> str:
    while True:
        choice = input(f"Are you ready to fight {monster.name}? Please enter y when ready: ")
        if choice == 'y':
            break
        print("Please enter y when ready.")
        
    printwait("First, initiative will be rolled for both you and your opponent.", 1)
    initiative = roll_1v1_initiative(monster, character)
    battle_result = combat_1v1(monster, character, initiative, can_flee)
    if battle_result == 'player_win':
        character.add_experience(monster.experience_given)
    return battle_result

######################################

def parse_effect(effect: str) -> list:
    parsed = effect.split()
    parsed[0] = int(parsed[0])
    # parsed[2] = int(parsed[2])
    return parsed

######################################

def combat_1v1(monster: Monster, character: Character, initiative: str, flee_possibility: bool) -> str:
    monster_effect_duration = 0
    monster_effect = False
    self_shield_duration = 0
    self_shield = False
    potion_effect_duration = 0


    # deep copy of the dictionary using import copy, so that we dont alter the instanced dictionary
    character_abilities = copy.deepcopy(character.special_abilities_dictionary)

    seperator()
    printwait(f"---BATTLE START!---", 1)
    printwait(f"{character.name} (HP: {character.hit_points}) vs {monster.name} (HP: {monster.hit_points})", 1)
    seperator()

    monster_hp = monster.hit_points
    character_hp = character.hit_points

    self_shield_duration_counter = 0
    monster_effect_duration_counter = 0
    potion_effect_duration_counter = 0

    # Potion Effects
    health_potion_bonus = False
    attack_potion_bonus = False

    damage_potion_bonus = False
    additional_damage_potion_bonus = 0
    damage_multiplier_potion_bonus = 0

    defense_potion_bonus = False

    def apply_shield(monster_turn_result):
        nonlocal self_shield
        shield_result = self_shield - monster_turn_result
        if shield_result <= 0:
            printwait(f"Your shield absorbed {self_shield} damage.\nShield depleted...", 2)
            self_shield = 0
            return abs(shield_result)
        else:
            self_shield = shield_result
            printwait(f"Your shield absorbed {monster_turn_result} damage.\nDamage absorption remaining: {self_shield}\nShield duration remaining: {self_shield_duration - self_shield_duration_counter - 1} Turn(s)", 2)
            return 0

    def process_turn(entity: str):
        nonlocal character_hp, monster_hp, monster_effect_duration_counter, self_shield_duration_counter, monster_effect, self_shield, potion_effect_duration, potion_effect_duration_counter, self_shield_duration, monster_effect_duration, health_potion_bonus
        
        if entity == 'monster':
            if monster_effect:
                monster_effect_duration_counter += 1
                if monster_effect[1] == 'firestorm':
                    monster_hp -= monster_effect[0]
                    printwait(f"{monster.name} takes {monster_effect[0]} damage from your Fire Storm.\n{monster_effect_duration - monster_effect_duration_counter} turn(s) of Fire Storm remain.")

            if monster_effect_duration_counter == monster_effect_duration:
                monster_effect = False
                monster_effect_duration_counter = 0

            if self_shield:
                self_shield_duration_counter += 1

            if self_shield_duration_counter == self_shield_duration and self_shield_duration_counter != 0:
                self_shield = False
                self_shield_duration_counter = 0
                printwait("Your shield's duration runs out... You're vulnerable again.", 1)

            if self_shield <= 0:
                self_shield = False
                self_shield_duration_counter = 0
        elif entity == 'character':
            if health_potion_bonus:
                character_hp += health_potion_bonus
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    health_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Health Potion wears off...")
        else:
            print(f"Unkown Entity: {entity}")

    def character_defense(monster_turn_result):
        nonlocal character_hp, self_shield, character_abilities
        if self_shield:
            monster_turn_result = apply_shield(monster_turn_result)

        if character.role.lower() == 'knight':
            if character_abilities['heavy armor'][1] == 1:
                monster_turn_result *= .95
            elif character_abilities['heavy armor'][1] == 2:
                monster_turn_result *= .90
            elif character_abilities['heavy armor'][1] == 3:
                monster_turn_result *= .85
            monster_turn_result = math.ceil(monster_turn_result)

        character_hp -= monster_turn_result

    def player_turn_sequence(damage_multiplier: int = 1, additional_damage: int = 0, additional_attack_roll: int = 0):
        nonlocal character_hp, monster_hp, monster_effect, monster_effect_duration, self_shield, self_shield_duration, potion_effect_duration, health_potion_bonus, attack_potion_bonus, additional_damage_potion_bonus, damage_multiplier_potion_bonus, defense_potion_bonus, damage_potion_bonus

        player_turn_result = player_turn_1v1(monster, character, flee_possibility, character_abilities, additional_attack_roll, additional_damage, damage_multiplier)

        if isinstance(player_turn_result, Potion):
            potion_effect_duration = player_turn_result.effect_duration
            if player_turn_result.type == 'Self Heal':
                health_potion_bonus = player_turn_result.self_heal_amount
            elif player_turn_result.type == 'Attack Bonus':
                attack_potion_bonus = player_turn_result.attack_roll_bonus
            elif player_turn_result.type == 'Damage Bonus':
                damage_potion_bonus = True
                additional_damage_potion_bonus = player_turn_result.additional_damage
                damage_multiplier_potion_bonus = player_turn_result.damage_multiplier
            elif player_turn_result.type == 'Defense Bonus':
                defense_potion_bonus = player_turn_result.bonus_armor_class
            

        elif isinstance(player_turn_result, tuple):
            if player_turn_result[0] == 'self heal':
                character_hp += player_turn_result[1]
                if character_hp > character.hit_points:
                    printwait(f"You heal {player_turn_result[1] - character_hp + character.hit_points} hitpoints", 1)
                    character_hp = character.hit_points
                else:
                    printwait(f"You heal {player_turn_result[1]} hitpoints", 1)
            elif player_turn_result[0] == 'monster effect':
                monster_hp -= player_turn_result[1]
                monster_effect = parse_effect(player_turn_result[2])
                monster_effect_duration = player_turn_result[3]
            elif player_turn_result[0] == 'self shield':
                self_shield = player_turn_result[1]
                self_shield_duration = player_turn_result[2]
        elif player_turn_result == 'fled':
            return 'fled'
        elif player_turn_result == 'trapped':
            print("The battle continues...")
        elif isinstance(player_turn_result, (int, float)):
            monster_hp -= player_turn_result
        else:
            print(f"Unknown Action: {player_turn_result}")

        return None

    while monster_hp > 0 and character_hp > 0:
        if initiative == 'character':
            printwait("--- Your Turn ---", 0.5)

            if attack_potion_bonus:
                result = player_turn_sequence(1, 0, attack_potion_bonus)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    attack_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Attack Potion wears off...")
            elif damage_potion_bonus:
                result = player_turn_sequence(damage_multiplier_potion_bonus, additional_damage_potion_bonus, 0)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    damage_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Damage Potion wears off...")
            else:
                result = player_turn_sequence()
            if result:
                return result

            process_turn('character')

            if monster_hp <= 0:
                printwait(f"{monster.name} defeated!! You are victorious!")
                return 'player_win'

            seperator()
            printwait(f"--- Your Remaining HP: {character_hp} ---")
            printwait(f"--- {monster.name}'s Remaining HP: {monster_hp} ---")
            seperator()
            printwait(f"--- {monster.name}'s Turn ---", 0.5)

            if defense_potion_bonus:
                monster_turn_result = monster_turn_1v1(monster, character, monster_effect, defense_potion_bonus)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    defense_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Defense Potion wears off...")
            else:
                monster_turn_result = monster_turn_1v1(monster, character, monster_effect)

            character_defense(monster_turn_result)

            process_turn('monster')

        elif initiative == 'monster':
            printwait(f"--- {monster.name}'s Turn ---", 0.5)
            if defense_potion_bonus:
                monster_turn_result = monster_turn_1v1(monster, character, monster_effect, defense_potion_bonus)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    defense_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Defense Potion wears off...")
            else:
                monster_turn_result = monster_turn_1v1(monster, character, monster_effect)
            
            character_defense(monster_turn_result)

            process_turn('monster')

            if character_hp <= 0:
                return 'monster_win'

            seperator()
            printwait(f"---Your Remaining HP: {character_hp}---")
            printwait(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()

            printwait("--- Your Turn ---", 0.5)

            if attack_potion_bonus:
                result = player_turn_sequence(1, 0, attack_potion_bonus)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    attack_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Attack Potion wears off...")
            elif damage_potion_bonus:
                result = player_turn_sequence(damage_multiplier_potion_bonus, additional_damage_potion_bonus, 0)
                potion_effect_duration_counter += 1
                if potion_effect_duration_counter == potion_effect_duration:
                    damage_potion_bonus = False
                    potion_effect_duration = 0
                    potion_effect_duration_counter = 0
                    printwait("Your Damage Potion wears off...")
            else:
                result = player_turn_sequence()

            if result:
                return result
            
            process_turn('character')

        if monster_hp <= 0:
            printwait(f"{monster.name} defeated!! You are victorious!")
            return 'player_win'
        if character_hp <= 0:
            return 'monster_win'
        
        seperator()
        printwait(f"--- Your Remaining HP: {character_hp} ---")
        printwait(f"--- {monster.name}'s Remaining HP: {monster_hp} ---")
        seperator()

    print(f"Unknown Initiative Value: {initiative}")

######################################

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
        printwait(f"Rolling {monster.name}'s initiative...", 1)
        printwait(f"{monster.name} rolled a {monster_initiative}", 1)
        seperator()
        printwait(f"Rolling {character.name}'s initiative...", 1)
        printwait(f"{character.name} rolled a {character_initiative}", 1)
        seperator()

        if character_initiative > monster_initiative:
            print(f"Congrats! {character.name} gets to go first!")
            return 'character'
        elif monster_initiative > character_initiative:
            print(f"Unlucky... {monster.name} gets to go first.")
            return 'monster'
        else:
            printwait("It's a tie! Rerolling...", 2)

######################################

def roll_flee_check(monster: Monster, character: Character) -> bool:
        printwait("Flee checks are based on the Dexterity modifier of the monster and the player.", 1)
        monster_flee_check = random.randint(1, 20)
        monster_flee_check += monster.get_modifier(monster.dexterity)
        character_flee_check = random.randint(1, 20)
        character_flee_check += character.get_modifier(character.dexterity)
        seperator()
        printwait(f"Rolling {monster.name}'s flee check...", 1)
        printwait(f"{monster.name} rolled a {monster_flee_check}", 1)
        seperator()
        printwait(f"Rolling {character.name}'s flee check...", 1)
        printwait(f"{character.name} rolled a {character_flee_check}", 1)
        seperator()

        if character_flee_check > monster_flee_check:
            print(f"You succesfully slip away from the {monster.name}.")
            return True
        elif monster_flee_check > character_flee_check:
            print(f"Unlucky... The {monster.name} prevents you from escaping.")
            return False
        else:
            printwait("It's a tie! Rerolling...", 2)
            roll_1v1_initiative(monster, character)

######################################

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

    printwait(f"Rolling {damage}...")

    for i in range(number_of_dice):
        roll = random.randint(1, dice_type)
        printwait(f"The roll is a {roll}.")
        total_damage += roll

    total_damage_plus_modifier = total_damage + modifier
    printwait(f"The sum of all rolls ({total_damage}) plus the modifier ({modifier}) is: {total_damage_plus_modifier}.")
    seperator()

    return total_damage_plus_modifier

######################################

def monster_turn_1v1(monster: Monster, character: Character, monster_effect, player_ac_bonus: int = 0) -> int:
    print(f"---{monster.name}'s Turn---")

    if isinstance(monster_effect, list):
        if monster_effect[1] == 'attack roll':
            monster_attack_roll = random.randint(1, 20)
            monster_attack_roll += monster_effect[0]
        else:
            monster_attack_roll = random.randint(1, 20)
    else:
        monster_attack_roll = random.randint(1, 20)

    if player_ac_bonus:
        printwait(f"{monster.name} rolling vs your AC: {character.armor_class} (+{player_ac_bonus} Bonus AC)...", 3)
    else:
        printwait(f"{monster.name} rolling vs your AC: {character.armor_class}...", 3)

    if monster_attack_roll == 20:
        monster_crit_damage = roll_damage_value(monster.damage)
        monster_crit_damage += monster_crit_damage
        printwait(f"The {monster.name} rolls a natural 20, critical hit! You take double damage...", 1)
        printwait(f"The {monster.name} deals {monster_crit_damage} damage to you.", 1)
        monster_crit_damage = math.ceil(monster_crit_damage)
        return monster_crit_damage
    
    if monster.monster_type == 'Dark Wizard':
        monster_attack_roll += monster.get_modifier(monster.intelligence)
    else:
        monster_attack_roll += monster.get_modifier(monster.strength)

    player_armor_class = character.armor_class
    player_armor_class += player_ac_bonus

    if monster_attack_roll >= player_armor_class:
        print(f"The {monster.name} successfully hits you.")
        monster_damage = roll_damage_value(monster.damage)
        print(f"The {monster.name} deals {monster_damage} damage to you. Ouch!")
        monster_damage = math.ceil(monster_damage)
        return monster_damage
    else:
        print(f"The {monster.name} strikes at you, but you parry it expertly. You take no damage this turn!")
        return 0

######################################

def player_attack(monster: Monster, character: Character, damage_multiplier: int = 1, additional_damage: int = 0, additional_attack_roll: int = 0, custom_print: bool = False):
    attack_roll = random.randint(1, 20)
    if attack_roll == 20:
        if character.role.lower() == 'archer':
            if not custom_print:
                printwait(f"You fire a projectile at the {monster.name}...", 2)
            print(f"You roll a natural 20! Critical hit! Your arrow hits the {monster.name} going straight through it, rips a hole in spacetime, travels through a wormhole in the 5th dimension and plunges itself again deep within the shocked {monster.name}!")
        elif character.role.lower() == 'knight':
            if not custom_print:
                printwait(f"You swing your weapon at the {monster.name}...", 2)
            print(f"You roll a natural 20! Critical hit! Your weapon strikes the {monster.name} with such tremendous force that it creates gravitons, temporarily altering gravity. The {monster.name} is lifted off its feet, spun around by the cosmic disturbance, only to be slammed back down onto your waiting blade!")
        elif character.role.lower() == 'wizard':
            if not custom_print:
                printwait(f"You cast a spell at the {monster.name}...", 2)
            print(f"You roll a natural 20! Critical hit! Your spell engulfs the {monster.name} in a dazzling vortex of arcane energy, briefly phasing it out of reality. The {monster.name} reappears a second later, looking bewildered and smoking, as if it had been subjected to the heat death and rebirth of several universes in the blink of an eye!")
        crit_damage = roll_damage_value(character.equipped_items['weapon'].damage)
        crit_damage += crit_damage
        crit_damage *= damage_multiplier
        crit_damage += additional_damage
        crit_damage = math.ceil(crit_damage)
        print(f"You do double damage! You deal {crit_damage} damage to the {monster.name}!")
        return crit_damage
    else:
        if character.role.lower() == 'archer':
            attack_roll += character.get_modifier(character.dexterity)
        elif character.role.lower() == 'knight':
            attack_roll += character.get_modifier(character.strength)
        elif character.role.lower() == 'wizard':
            attack_roll += character.get_modifier(character.intelligence)

        
        attack_roll += additional_attack_roll
        if character.role.lower() == 'archer':
            if not custom_print:
                printwait(f"You fire a projectile at the {monster.name}...", 2)
        elif character.role.lower() == 'knight':
            if not custom_print:
                printwait(f"You swing your weapon at the {monster.name}...", 2)
        elif character.role.lower() == 'wizard':
            if not custom_print:
                printwait(f"You cast a spell at the {monster.name}...", 2)
        
        if attack_roll >= monster.armor_class:
            print("It's a hit!")
            damage = roll_damage_value(character.equipped_items['weapon'].damage)
            damage *= damage_multiplier
            damage += additional_damage
            damage = math.ceil(damage)
            print(f"You deal {damage} damage to the {monster.name}.")
            return damage
        else:
            if character.role.lower() == 'archer':
                printwait(f"A child would have got closer to the target than that shot... You deal no damage this turn.", 1)
            elif character.role.lower() == 'knight':
                printwait(f"You swing and miss, falling flat on your face... You deal no damage this turn.", 1)
            elif character.role.lower() == 'wizard':
                printwait(f"Your spell fizzles out pathetically... You deal no damage this turn.", 1)
            return 0 
                    
######################################

def player_turn_1v1(monster: Monster, character: Character, flee_possibility: bool, character_abilities: dict, attack_roll_bonus: int = 0, additional_damage: int = 0, damage_multiplier: int = 1):
    while True:
        choice = input("Choices: 1. Attack, 2. Special Ability, 3. Use an Item, 4. Attempt to Flee. Please pick an action (enter the number of your choice): ")
        if choice == '1':
            if character.role.lower() in ['archer', 'knight', 'wizard']:
                damage = player_attack(monster, character, damage_multiplier, additional_damage, attack_roll_bonus)
                return damage
            else:
                print(f"Unknown Class: {character.role}")
                continue

            
        elif choice == '2':
            if character.role.lower() == 'archer':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities (1. {character.special_abilities[0]}, 2. {character.special_abilities[1]}, 3. {character.special_abilities[2]}): ").lower()
                    if spec_ability in ['1', '2', '3']:
                        break
                    print("Please enter a valid response.")
                if spec_ability == '1':
                    if character_abilities['blinding shot'][0] < character_abilities['blinding shot'][2]:
                        character_abilities['blinding shot'][0] += 1
                        if character_abilities['blinding shot'][1] == 1:
                            printwait("Drawing your bow, you fire a brilliant arrow...", 1)
                            damage = player_attack(monster, character, 1.4, 0, 5, True)
                            effect ='-3 attack roll'
                            duration = 2
                        elif character_abilities['blinding shot'][1] == 2:
                            printwait("Drawing your bow, you fire a stunningly bright arrow...", 1)
                            damage = player_attack(monster, character, 1.6, 0, 7, True)
                            effect ='-5 attack roll'
                            duration = 3
                        elif character_abilities['blinding shot'][1] == 3:
                            printwait("Drawing your bow, you fire an arrow made of pure light...", 1)
                            damage = player_attack(monster, character, 2, 0, 10, True)
                            effect ='-8 attack roll'
                            duration = 4

                        if damage > 0:
                            printwait(f"It strikes the {monster.name}, bursting on impact, temporarily blinding your target.", 1)
                        else:
                            printwait(f"It's light fades as it sores to the side of the {monster.name}. Unfortunate...", 1)
                        
                        seperator()
                        # returning type of effect, damage, what is effected and by how much, # of turns the effect applies for
                        return ('monster effect', damage, effect, duration)
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue
                    
                elif spec_ability == '2':
                    if character_abilities['double shot'][0] < character_abilities['double shot'][2]:
                        character_abilities['double shot'][0] += 1
                        # checking which level the SA is
                        if character_abilities['double shot'][1] == 1:
                            printwait("You knock two arrows and let them fly...", 2)
                            damage1 = player_attack(monster, character, 0.9, 0, -4, True)
                            damage2 = player_attack(monster, character, 0.9, 0, -4, True)
                            damage = damage1 + damage2

                            if damage == 0:
                                return damage
                            elif damage1 == 0 or damage2 == 0:
                                printwait(f"A single arrow strikes the {monster.name}, the other flying wide.", 1)
                            else:
                                printwait(f"Both arrows hit the {monster.name}.", 1)

                        elif character_abilities['double shot'][1] == 2:
                            printwait("You knock two arrows and release them with practiced precision...", 1)
                            damage1 = player_attack(monster, character, 1, 0, -2, True)
                            damage2 = player_attack(monster, character, 1, 0, -2, True)
                            damage = damage1 + damage2

                            if damage == 0:
                                return damage
                            elif damage1 == 0 or damage2 == 0:
                                printwait("One arrow hits true, while the other barely misses its mark.", 1)
                            else:
                                printwait(f"The arrows strike in rapid succession, the {monster.name} stumbles backwards.", 1)
                            
                        elif character_abilities['double shot'][1] == 3:
                            printwait("You knock two arrows, imbuing them with power before unleashing...", 1)
                            damage1 = player_attack(monster, character, 1.2, 0, 1, True)
                            damage2 = player_attack(monster, character, 1.2, 0, 1, True)
                            damage = damage1 + damage2

                            if damage == 0:
                                return damage
                            elif damage1 == 0 or damage2 == 0:
                                printwait(f"One of your charged arrows finds its target, delivering a potent blow to the {monster.name}.", 1)
                            else:
                                printwait(f"The arrows whistle through the air, striking the {monster.name} with pinpoint accuracy.", 1)

                        seperator()
                        return damage

                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue

                elif spec_ability == '3':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    continue
                else:
                    print("Unknown Special Ability")
            
            elif character.role.lower() == 'knight':
                while True:
                    spec_ability = input(f"Please enter the number associated with one of your character's special abilities (1. {character.special_abilities[0]}, 2. {character.special_abilities[1]}, 3. {character.special_abilities[2]}): ").lower()
                    if spec_ability in ['1', '2', '3']:
                        break
                    print("Please enter a valid response.")

                if spec_ability == '1':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    continue

                elif spec_ability == '2':
                    if character_abilities['resilience'][0] < character_abilities['resilience'][2]:
                        character_abilities['resilience'][0] += 1
                        if character_abilities['resilience'][1] == 1:
                            printwait("Your determination manifests as a pulse of healing energy, knitting flesh and bolstering spirit.", 1)
                            seperator()
                            return ('self heal', 3)
                        elif character_abilities['resilience'][1] == 2:
                            printwait("Your determination manifests as a pulse of healing energy, flooding your body, knitting flesh and bolstering spirit.", 1)
                            seperator()
                            return ('self heal', 6)
                        elif character_abilities['resilience'][1] == 3:
                            printwait("Your determination manifests as radiant healing energy, coursing through your body like a river, knitting flesh, mending bone and bolstering spirit.", 1)
                            seperator()
                            return ('self heal', 10)
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue

                elif spec_ability == '3':
                    # checking if the SA's number of uses are used up for this combat
                    if character_abilities['big swing'][0] < character_abilities['big swing'][2]:
                        character_abilities['big swing'][0] += 1
                        if character_abilities['big swing'][1] == 1:
                            printwait(f"You wind up and swing your weapon as hard as you can muster...", 1)
                            damage = player_attack(monster, character, 2, 0, 0, True)
                            seperator()
                            return ('monster effect', damage, '3 attack roll', 1)
                        
                        elif character_abilities['big swing'][1] == 2:
                            printwait(f"Channeling your strength, you execute a mighty sweep, your weapon cutting through the air with fearsome momentum...", 1)
                            damage = player_attack(monster, character, 3, 2, 0, True)
                            seperator()
                            return ('monster effect', damage, '4 attack roll', 2)
                        
                        elif character_abilities['big swing'][1] == 3:
                            printwait(f"Time seems to slow as you focus your entire being into a single, monumental strike; your weapon becomes an extension of your will, ready to unleash untold devastation...", 1)
                            damage = player_attack(monster, character, 4, 4, 0, True)
                            seperator()
                            return ('monster effect', damage, '5 attack roll', 3)
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue

                else:
                    print("Unknown Special Ability")
                    continue

            elif character.role.lower() == 'wizard':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities (1. {character.special_abilities[0]}, 2. {character.special_abilities[1]}, 3. {character.special_abilities[2]}): ").lower()
                    if spec_ability in ['1', '2', '3']:
                        break
                    print("Please enter a valid response.")
                if spec_ability == '1':
                    if character_abilities['fire storm'][0] < character_abilities['fire storm'][2]:
                        character_abilities['fire storm'][0] += 1
                        if character_abilities['fire storm'][1] == 1:
                            printwait(f"", 2)
                            damage = player_attack(monster, character, 0.5, 0, 3, True)
                            seperator()
                            effect = '2 firestorm'
                            duration = 3
                        
                        elif character_abilities['fire storm'][1] == 2:
                            printwait(f"", 2)
                            damage = player_attack(monster, character, 0.5, 0, 5, True)
                            seperator()
                            effect = '3 firestorm'
                            duration = 4
                        
                        elif character_abilities['fire storm'][1] == 3:
                            printwait(f"", 2)
                            damage = player_attack(monster, character, 0.6, 0, 8, True)
                            seperator()
                            effect = '4 firestorm'
                            duration = 5

                        if damage > 0:
                            printwait(f"Your Fire Storm rains down upon the {monster.name}.", 1)
                        return ('monster effect', damage, effect, duration)
                    
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue
                # magic shield returns str that is checked for being self shield, 2nd number is amount that can be absorbed, 3rd number is duration of shield (if not used up by the 2nd number going to 0)
                elif spec_ability == '2':
                    if character_abilities['magic shield'][0] < character_abilities['magic shield'][2]:
                        character_abilities['magic shield'][0] += 1
                        if character_abilities['magic shield'][1] == 1:
                            printwait("You conjure a shimmering and powerful forcefield around yourself.", 1)
                            seperator()
                            return ('self shield', 4, 2)
                        elif character_abilities['magic shield'][1] == 2:
                            printwait("Arcane sigils flare to life as you weave a robust barrier of iridescent energy, encasing yourself in a dome of protective magic.", 1)
                            seperator()
                            return ('self shield', 9, 3)
                        elif character_abilities['magic shield'][1] == 3:
                            printwait("The very air crackles with power as you manifest a grand bulwark of arcane might; prismatic energies swirl and solidify into an awe-inspiring spherical shield.", 1)
                            seperator()
                            return ('self shield', 14, 4)
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue
                elif spec_ability == '3':
                    print("This Special Ability not yet implemented...")
                    seperator()
                    continue
                else:
                    print("Unknown Special Ability")
                    continue

            else:
                print(f"Unknown Class: {character.role}")

        elif choice == '3':
            potion = use_potion(character)
            if potion:
                return potion
            else:
                continue

        
        elif choice == '4':
            if not flee_possibility:
                print("You cannot run from this battle.")
                continue
            flee_check = roll_flee_check(monster, character)
            if flee_check == True:
                return 'fled'
            else:
                return 'trapped'

        else:
            print("Please enter a valid response.")

######################################

def use_potion(character):
    potions_in_inv = list(character.inventory['potions'].keys())
    print("Which Potion would you like to use? Enter 'n' to cancel.")
    for index, (potion, quantity) in enumerate(character.inventory['potions'].items()):
        print(f"{index + 1}. {potion.name} (x{quantity})")
    while True:
        potion_choice = input("Enter the number associated with your choice: ")
        if potion_choice == 'n':
            return False
        elif potion_choice.isdigit():
            potion_choice = int(potion_choice)
            if 1 <= potion_choice <= len(potions_in_inv):
                chosen_potion = potions_in_inv[potion_choice - 1]
                if character.character_level >= chosen_potion.required_level:
                    character.inventory['potions'][chosen_potion] -= 1
                    if character.inventory['potions'][chosen_potion] <= 0:
                        del character.inventory['potions'][chosen_potion]
                    return chosen_potion
                else:
                    print("You are not a high enough level to use this potion.")
            else:
                print("Please enter a valid option.")
        else:
            print("Please enter a valid option.")

######################################

def add_loot_to_inv(character, total_loot):
    if isinstance(total_loot, tuple):
        total_loot = [total_loot]

    for item, quantity in total_loot:
        if isinstance(item, Weapon):
            if item in list(character.inventory['weapons'].keys()):
                character.inventory['weapons'][item] += quantity
            else:
                character.inventory['weapons'][item] = quantity
            printwait(f"You loot {quantity} {item.name}(s)!", 1)
        elif item == 'nothing':
            printwait(f"You find nothing...", 1)
            continue
        elif item == 'gold_coins':
            character.inventory['gold_coins'] += quantity
            printwait(f"You loot {quantity} Gold Coins!", 1)
        elif isinstance(item, Potion):
            if item in list(character.inventory['potions'].keys()):
                character.inventory['potions'][item] += quantity   
            else:
                character.inventory['potions'][item] = quantity
            printwait(f"You loot {quantity} {item.name}(s)!", 1)
        else:
            if item in list(character.inventory['misc'].keys()):
                character.inventory['misc'][item] += quantity
            else:
                character.inventory['misc'][item] = quantity
            printwait(f"You loot {quantity} {item}(s)!", 1)
    

######################################

def roll_monster_loot(monster: Monster, character: Character, battle_result: str):
    loot = monster.loot_drops
    if battle_result == 'player_win':
        printwait("You loot the body...", 4)
        
        guarenteed_loot = loot['guarenteed_loot']
        guarenteed_loot = list(guarenteed_loot.items())

        if guarenteed_loot:
            add_loot_to_inv(character, guarenteed_loot)

        total_probability = 0
        for item, value in list(loot.items())[1:]:
            total_probability += value[1]
        
        if total_probability != 100:
            raise ValueError(f"Probabilities must sum to 100, but they sum to {total_probability}")

        roll = random.randint(1, 100)
        cumulative_probability = 0
        for item, value in list(loot.items())[1:]:
            probability = value[1]
            cumulative_probability += probability
            if roll <= cumulative_probability:
                total_loot = [(item, value[0])]
                add_loot_to_inv(character, total_loot)
                print(f"---Here is your inventory---")
                character.print_inventory()
                seperator()
                if item == 'nothing':
                    return 'no_loot'
                else:
                    return 'yes_loot'

    elif battle_result == 'monster_win':
        return 'death'

    elif battle_result == 'fled':
        return 'fled'
    
    else:
        printwait("battle_result error in roll_monster_loot()", 1)



######################################
# ROLL STAT/CHECK MECHANICS
######################################

def roll_stat(stat) -> int:
    printwait(f"Rolling your {stat}...", 1)
    stat1 = random.randint(1, 6)
    printwait(f"Your first d6 roll is {stat1}", 1)
    stat2 = random.randint(1, 6)
    printwait(f"Your second d6 roll is {stat2}", 1)
    stat3 = random.randint(1, 6)
    printwait(f"Your third d6 roll is {stat3}", 1)
    stat4 = random.randint(1, 6)
    printwait(f"Your fourth d6 roll is {stat4}", 1)

    rolls = [stat1, stat2, stat3, stat4]
    lowest_stat_roll = min(rolls)
    rolls.remove(lowest_stat_roll)
    total_stat_roll = sum(rolls)
    print(f"Your final combined roll for {stat} is {total_stat_roll}.")

    return total_stat_roll

######################################

def seperator():
    print("------------------------------------")

######################################

def roll_stat_check_d20(character: Character, target: int, stat: str, additional_modifier: int) -> bool:
    stat_value = getattr(character, stat)
    modifier = character.get_modifier(stat_value)

    check = random.randint(1, 20)
    print(f"You rolled a {check} ({get_modifier_value(stat_value)} from your {stat}).")
    seperator()
    check += modifier
    check += additional_modifier

    if check >= target:
        print(f"Your total roll of {check} succeded! You passed the {stat.capitalize()} check!")
        return True
    else:
        print(f"Your total roll of {check} was a failure... You failed the {stat.capitalize()} check...")
        return False
    
######################################

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
        
######################################

def printwait(what_to_print: str = "*Missing printwait string input*", wait_time: int = 1):
    print(what_to_print)
    time.sleep(wait_time) 

######################################

def perform_stat_check(character: Character, target: int, stat: str, modifier: int, number_of_attempts: int) -> bool:
    while True:
        choice = input(f"Are you ready to roll the {stat.capitalize()} check? Enter y when ready: ").lower()
        if choice == 'y':
            break
        else:
            print("Please enter y when ready.")

    tries = 0        
    while tries < number_of_attempts:
        result = roll_stat_check_d20(character, target, stat, modifier)
        seperator()
        if result:
            return True
        
        tries += 1

        while True:
            choice = input("Try again? (y/n): ")
            if choice == 'y':
                break
            elif choice == 'n':
                return False
            print("Please enter a valid option.")

        printwait(f"Rerolling... (Attempt {tries + 1} of {number_of_attempts})", 2)

    return False