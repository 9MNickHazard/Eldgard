import time
import random
import re

from character_and_monsters import Character, Monster


######################################
# COMBAT MECHANICS
######################################

def initiate_combat(player: Character, monster: Monster, can_flee: bool) -> str:
    while True:
        choice = input(f"Are you ready to fight the {monster.name}? Please enter y when ready: ")
        if choice == 'y':
            break
        print("Please enter y when ready.")
        
    printwait("First, initiative will be rolled for both you and your opponent.", 2)
    initiative = roll_1v1_initiative(monster, player)
    battle_result = combat_1v1(monster, player, initiative, can_flee)
    return battle_result

######################################

def parse_monster_effect(monster_effect: str) -> list:
    parsed = monster_effect.split()
    parsed[0] = int(parsed[0])
    # parsed[2] = int(parsed[2])
    return parsed

######################################

def combat_1v1(monster: Monster, character: Character, initiative: str, flee_possibility: bool) -> str:
    effect_duration = 0
    monster_effect = False
    character_abilities = character.special_abilities_dictionary
    seperator()
    printwait(f"---BATTLE START!---", 1)
    printwait(f"{character.name} vs {monster.name}", 1)
    seperator()

    monster_hp = monster.hit_points
    character_hp = character.hit_points

    if initiative == 'character':
        effect_duration_counter = 0
        while monster_hp > 0 and character_hp > 0:
            print("---Your Turn---")
            player_turn_result = player_turn_1v1(monster, character, flee_possibility, character_abilities)

            if player_turn_result == 'fled':
                return 'fled'
            elif player_turn_result == 'trapped':
                print("The battle continues...")
            elif isinstance(player_turn_result, (int, float)):
                monster_hp -= player_turn_result
            elif isinstance(player_turn_result, tuple):
                if len(player_turn_result) >= 1:
                    monster_hp -= player_turn_result[0]
                if len(player_turn_result) >= 2:
                    monster_effect = parse_monster_effect(player_turn_result[1])
                if len(player_turn_result) >= 3:
                    effect_duration = player_turn_result[2]
            else:
                print(f"Unknown Action: {player_turn_result}")

            if monster_hp <= 0:
                break

            # time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            # time.sleep(2)
            ################################################################################ working here
            monster_turn_result = monster_turn_1v1(monster, character, monster_effect)
            character_hp -= monster_turn_result 

            if monster_effect:
                effect_duration_counter += 1

            if effect_duration_counter == effect_duration:
                monster_effect = False

            # time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            # time.sleep(2)

        if monster_hp <= 0:
            return 'player_win'
        if character_hp <= 0:
            return 'monster_win'

    elif initiative == 'monster':
        effect_duration_counter = 0
        while monster_hp > 0 and character_hp > 0:
            monster_turn_result = monster_turn_1v1(monster, character, monster_effect)
            character_hp -= monster_turn_result 

            if monster_effect:
                effect_duration_counter += 1

            if effect_duration_counter == effect_duration:
                monster_effect = False

            if character_hp <= 0:
                break

            # time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            # time.sleep(2)

            print("---Your Turn---")
            player_turn_result = player_turn_1v1(monster, character, flee_possibility, character_abilities)

            if player_turn_result == 'fled':
                return 'fled'
            elif player_turn_result == 'trapped':
                print("The battle continues...")
            elif isinstance(player_turn_result, (int, float)):
                monster_hp -= player_turn_result
            elif isinstance(player_turn_result, tuple):
                if len(player_turn_result) >= 1:
                    monster_hp -= player_turn_result[0]
                if len(player_turn_result) >= 2:
                    monster_effect = parse_monster_effect(player_turn_result[1])
                if len(player_turn_result) >= 3:
                    effect_duration = player_turn_result[2]
            else:
                print(f"Unknown Action: {player_turn_result}")

            # time.sleep(2)
            seperator()
            print(f"---Your Remaining HP: {character_hp}---")
            print(f"---{monster.name}'s Remaining HP: {monster_hp}---")
            seperator()
            # time.sleep(2)

        if monster_hp <= 0:
            return 'player_win'
        if character_hp <= 0:
            return 'monster_win'


    else:
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
        printwait(f"{monster.name} rolled a {monster_flee_check}", 2)
        seperator()
        printwait(f"Rolling {character.name}'s flee check...", 1)
        printwait(f"{character.name} rolled a {character_flee_check}", 2)
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

    print(f"Rolling {damage}...")
    # time.sleep(1)

    for i in range(number_of_dice):
        roll = random.randint(1, dice_type)
        print(f"The roll is a {roll}.")
        # time.sleep(1)
        total_damage += roll

    total_damage_plus_modifier = total_damage + modifier
    # time.sleep(1)
    print(f"The sum of all rolls ({total_damage}) plus the modifier ({modifier}) is: {total_damage_plus_modifier}.")

    return total_damage_plus_modifier

######################################

def monster_turn_1v1(monster: Monster, character: Character, monster_effect) -> int:
    print(f"---{monster.name}'s Turn---")

    if isinstance(monster_effect, list):
        if monster_effect[1] == 'attack_roll':
            monster_attack_roll = random.randint(1, 20)
            monster_attack_roll += monster_effect[0]
        else:
            monster_attack_roll = random.randint(1, 20)
    else:
        monster_attack_roll = random.randint(1, 20)
    # time.sleep(3)
    print(f"{monster.name} rolling vs your AC ({character.armor_class})...")
    # time.sleep(3)

    if monster_attack_roll == 20:
        monster_crit_damage = roll_damage_value(monster.damage)
        monster_crit_damage += monster_crit_damage
        print(f"The {monster.name} rolls a natural 20, critical hit! You take double damage...")
        # time.sleep(3)
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

######################################

def player_attack(monster: Monster, character: Character, damage_multiplier: int | float = 1, additional_damage: int = 0, additional_attack_roll: int = 0):
    attack_roll = random.randint(1, 20)
    if attack_roll == 20:
        if character.role.lower() == 'archer':
            printwait(f"You fire a projectile at the {monster.name}...", 3)
            print(f"You roll a natural 20! Critical hit! Your arrow hits the {monster.name} going straight through it, rips a hole in spacetime, travels through a wormhole in the 5th dimension and plunges itself again deep within the shocked {monster.name}!")
        elif character.role.lower() == 'knight':
            printwait(f"You swing your weapon at the {monster.name}...", 3)
            print(f"You roll a natural 20! Critical hit! Your weapon strikes the {monster.name} with such tremendous force that it creates gravitons, temporarily altering gravity. The {monster.name} is lifted off its feet, spun around by the cosmic disturbance, only to be slammed back down onto your waiting blade!")
        else:
            printwait(f"You cast a spell at the {monster.name}...", 3)
            print(f"You roll a natural 20! Critical hit! Your spell engulfs the {monster.name} in a dazzling vortex of arcane energy, briefly phasing it out of reality. The {monster.name} reappears a second later, looking bewildered and smoking, as if it had been subjected to the heat death and rebirth of several universes in the blink of an eye!")
        crit_damage = roll_damage_value(character.weapon['damage'])
        crit_damage += crit_damage
        crit_damage *= damage_multiplier
        crit_damage += additional_damage
        print(f"You do double damage! You deal {crit_damage} damage to the {monster.name}!")
        return crit_damage
    else:
        attack_roll += character.get_modifier(character.dexterity)
        attack_roll += additional_attack_roll
        if character.role.lower() == 'archer':
            printwait(f"You fire a projectile at the {monster.name}...", 3)
        elif character.role.lower() == 'knight':
            printwait(f"You swing your weapon at the {monster.name}...", 3)
        else:
            printwait(f"You cast a spell at the {monster.name}...", 3)
        
        if attack_roll >= monster.armor_class:
            print("It's a hit!")
            damage = roll_damage_value(character.weapon['damage'])
            damage *= damage_multiplier
            damage += additional_damage
            print(f"You deal {damage} damage to the {monster.name}.")
            return damage
        else:
            if character.role.lower() == 'archer':
                printwait(f"A child would have got closer to the target than that shot... You deal no damage this turn.", 3)
            elif character.role.lower() == 'knight':
                printwait(f"You swing and miss, falling flat on your face... You deal no damage this turn.", 3)
            else:
                printwait(f"Your spell fizzles out pathetically... You deal no damage this turn.", 3)
            return 0 
                    
######################################

def player_turn_1v1(monster: Monster, character: Character, flee_possibility: bool, character_abilities: dict):
    while True:
        choice = input("Choices: 1. Attack, 2. Special Ability, 3. Use an Item, 4. Attempt to Flee. Please pick an action (enter the number of your choice): ")
        if choice == '1':
            if character.role.lower() in ['archer', 'knight', 'wizard']:
                damage = player_attack(monster, character)
                return damage
            else:
                print(f"Unknown Class: {character.role}")
                continue

            
        elif choice == '2':
            if character.role.lower() == 'archer':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({Character.archer_special_abilities[0]}, {Character.archer_special_abilities[1]}, {Character.archer_special_abilities[2]}): ").lower()
                    if spec_ability in [Character.archer_special_abilities[0].lower(), Character.archer_special_abilities[1].lower(), Character.archer_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'blinding shot':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                elif spec_ability == 'armor piercing arrow':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                elif spec_ability == 'nimble steps':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    continue
                else:
                    print("Unknown Special Ability")
            
            elif character.role.lower() == 'knight':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({Character.knight_special_abilities[0]}, {Character.knight_special_abilities[1]}, {Character.knight_special_abilities[2]}): ").lower()
                    if spec_ability in [Character.knight_special_abilities[0].lower(), Character.knight_special_abilities[1].lower(), Character.knight_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'heavy armor':
                    print("You cannot use that ability in battle...")
                    seperator()
                    print("Please choose a valid option for your turn.")
                    seperator()
                    continue
                elif spec_ability == 'resilience':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                elif spec_ability == 'big swing':
                    # checking if the SA's number of uses are used up for this combat
                    if character_abilities['big swing'][0] < character_abilities['big swing'][2]:
                        printwait(f"You wind up and swing your weapon as hard as you can muster...", 3)
                        character_abilities['big swing'][0] += 1
                        damage = player_attack(monster, character, 2)
                        return (damage, '3 attack_roll', 1)
                    else:
                        printwait("You have run out of uses of that ability in this combat.", 1)
                        seperator()
                        continue
                else:
                    print("Unknown Special Ability")
                    continue

            elif character.role.lower() == 'wizard':
                while True:
                    spec_ability = input(f"Please enter one of your character's special abilities ({Character.wizard_special_abilities[0]}, {Character.wizard_special_abilities[1]}, {Character.wizard_special_abilities[2]}): ").lower()
                    if spec_ability in [Character.wizard_special_abilities[0].lower(), Character.wizard_special_abilities[1].lower(), Character.wizard_special_abilities[2].lower()]:
                        break
                    print("Please enter a valid response.")
                if spec_ability == 'spellcasting':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                elif spec_ability == 'magic shield':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                elif spec_ability == 'polymorph':
                    print("Special Abilities not yet implemented...")
                    seperator()
                    continue
                else:
                    print("Unknown Special Ability")
                    continue

            else:
                print(f"Unknown Class: {character.role}")

        elif choice == '3':
            print(character.inventory)
            seperator()
            # time.sleep(1)
            print("Use Item not yet implemented...")
            seperator()
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

def roll_loot(monster: Monster, character: Character, battle_result: str):
    if battle_result == 'player_win':
        roll = random.randint(1, 100)
        if roll in range(1, monster.loot_drops['chance_of_nothing'] + 1):
            printwait(f"You slay the {monster.name}! You look around the corpse, but unfortunately find no loot worth keeping...", 3)
            print(f"---Here is your inventory---")
            print(character.inventory)
            seperator()
            return 'no_loot'
        else:
            printwait(f"You slay the {monster.name}! You loot the body and find {monster.loot_drops['gold_coins']} Gold Coins! You put the gold in your pocket.", 3)
            character.inventory["gold_coins"] += monster.loot_drops["gold_coins"]
            print(f"---Here is your inventory---")
            print(character.inventory)
            seperator()
            return 'yes_loot'

    elif battle_result == 'monster_win':
        print("---You have died. GAME OVER---")
        return 'death'

    elif battle_result == 'fled':
        return 'fled'
    
    else:
        printwait("battle_result error", 2)


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

def printwait(what_to_print: str, wait_time: int):
    print(what_to_print)
    # time.sleep(wait_time)

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
        # time.sleep(1.5)
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