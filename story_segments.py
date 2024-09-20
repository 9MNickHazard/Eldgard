import time
import random
import re

from mechanics import combat_1v1, roll_1v1_initiative, roll_flee_check, roll_damage_value, monster_turn_1v1, player_turn_1v1, roll_stat, seperator, roll_stat_check_d20, get_modifier_value, initiate_combat, printwait, roll_loot, perform_stat_check
from character_and_monsters import Character, Monster




def intro_and_char_creation():
    printwait("Welcome to Eldgard! You will be embarking on a text rpg journey through this fantasy medieval land!", 3)
    seperator()
    printwait("EEEEE  L       DDDD     GGGG    AAAAA  RRRRR   DDDD", .8)
    printwait("E      L       D   D   G        A   A  R   R   D   D", .8)
    printwait("EEEEE  L       D   D   G  GG    AAAAA  RRRRR   D   D", .8)
    printwait("E      L       D   D   G   G    A   A  R R     D   D", .8)
    printwait("EEEEE  LLLLLL  DDDD     GGGG    A   A  R  RR   DDDD", 3)
    seperator()

    printwait("Lets roll your stats!", 2)
    seperator()
    printwait("On this adventure you will have 6 main stats: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. You will also have the chance to name your character and pick from one of the 3 classes: Archer, Knight, Wizard", 5)
    seperator()
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

    printwait("Now it is time to pick your class!", 2)
    seperator()
    printwait("There are three options for classes: Archer, Knight or Wizard", 2)
    seperator()
    printwait("Here are the bonuses, usable weapons, special abilities and descriptions for each class:", 5)
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
    print("What are your pronouns?")
    while True:
        pronoun_choice = input("Choices: 1. He/Him, 2. She/Her, 3. They/Them. Please input the number associated with your choice: ")
        if pronoun_choice in ['1', '2', '3']:
            break
        print("Please enter a valid option.")

    

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


    player_character = Character(name=name_choice, role=class_choice, pronouns=pronoun_choice, strength=player_starting_str, dexterity=player_starting_dex, constitution=player_starting_con, intelligence=player_starting_int, wisdom=player_starting_wis, charisma=player_starting_cha)

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

    return player_character


def first_dungeon_jail(character: Character):
    death_status = False
    printwait("The Adventure Begins...", 2)
    printwait("...", 2)
    printwait("...", 2)
    printwait("You awake with a splitting headache and a groggy feeling. You can still taste the alcohol from the copious amounts of meade you drink the night before.", 2)
    seperator()
    printwait("You wearily look around. You appear to be in a dark jail cell. A few other folks are in there with you, scattered about, all still passed out.", 2)
    seperator()
    printwait("You spy a puddle of puke in the corner of the jail cell, it makes you a bit naseous.", 2)

    while True:
        puke_choice = input("Do you want to throw up? (Please enter y or n): ").lower()
        if puke_choice == 'y':
            seperator()
            printwait("You puke your brains out, and wipe off your mouth. You actually feel a lot better!", 2)
            seperator()
            printwait("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.", 2)
            seperator()
            printwait("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.", 2)
            seperator()
            printwait("---You now need to roll a check to see if you successfully pick the guard's pocket---", 2)
            printwait(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(character.dexterity)}) will be applied---", 2)
            printwait("---If you roll above the required value (10 for this check, although this value will not always be given to you), you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---", 2)
            seperator()

            jail_key_pickpocket_check = perform_stat_check(character, 10, 'dexterity', 0, 1000)

            print("You carefully reach into the guard's pocket and snatch the cell keys. He snorts, but remains asleep.")
            break

        elif puke_choice == 'n':
            seperator()
            # time.sleep(2)
            printwait("You hold it in... You feel quite unsettled...", 2)
            seperator()
            printwait("You pick up your head and notice that a guard is fast asleep in a chair just within arms reach.", 2)
            seperator()
            printwait("You think to yourself: Hmmm I reckon I could get the cell keys from the guard's back pocket if I'm really careful.", 2)
            seperator()
            printwait("---You now need to roll a check to see if you successfully pick the guard's pocket---", 2)
            printwait(f"---This is a Dexterity check. A d20 will be rolled and your Dexterity modifier ({get_modifier_value(character.dexterity)}) will be applied---", 2)
            printwait("---If you roll above the required value (10 for this check, although this value will not always be given to you), you will pass the check. If you roll below, various things can happen, but in this instance you will be allowed to try again---", 2)
            printwait("For this Dexterity check you will recieve an additional -2 modifier for choosing not to throw up and feel better.", 2)
            seperator()

            jail_key_pickpocket_check = perform_stat_check(character, 10, 'dexterity', -2, 1000)

            print("You carefully reach into the guard's pocket and snatch the cell keys. He snorts, but remains asleep.")
            break
        else:
            print("Please enter y or n")

    printwait("You fumble around with the keys in the dark, but manage to find the correct key to the jail cell.", 2)
    seperator()
    printwait("You quietly unlock the jail cell door and slip out. As you close the door behind you, you hear a small grunt from the guard...", 2)
    seperator()
    printwait("...But it's just him dreaming. You quietly slink down the hallway. You come to an intersection...", 2)
    seperator()
    printwait("...to the left you hear the faint muttering of some guards and the periodic hearty chuckle. To the right you here the scuttle of small claws on the stone floor.", 2)
    seperator()


    first_dungeon_rat_loot = random.randint(1, 10)
    first_dungeon_rat_chance_of_nothing = random.randint(15, 30)
    first_dungeon_rat = Monster('Putrid Rat', '1d4 - 1', 'Rodent', {'gold_coins': first_dungeon_rat_loot, 'chance_of_nothing': first_dungeon_rat_chance_of_nothing}, 3, 3, 5, 1, 1, 1)

    while True:
        starting_dungeon_first_choice = input("Which path do you take? Type left or right: ")
        if starting_dungeon_first_choice == 'right':
            seperator()
            printwait("You go right and walk down the dark corridor. You turn around a corner and come face to face with the biggest rat you've ever seen in your life...", 2)
            seperator()
            printwait("---It's time for your first battle!---", 2)
            printwait("---If you die in battle, you will have to restart the entire game! Be careful!---", 2)
            printwait("---You and the rat will take turns doing actions. In a turn you can either decide to Attack, Use a Special Ability, Use an Item, or (in some cases) Attempt to Flee (DEX check)---", 2)
            printwait("---if you attack, you will roll a d20, applying your class's respective modifier (DEX for Archer, STR for Knight, INT for Wizard) against the enemy's Armor Class (AC)---", 2)
            printwait("---If your attack roll is successful, you will do damage based on your weapon (default damage with no weapon is 1d4 + 1)---", 2)
            printwait("---It will then be the enemy's turn. Most monsters will just attack, but some higher level monsters may take other actions---", 2)
            seperator()

            battle_result = initiate_combat(character, first_dungeon_rat, False) 
            seperator()
            # time.sleep(2)
            
            loot_result = roll_loot(first_dungeon_rat, character, battle_result)

            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                break
            elif loot_result == 'death':
                death_status = True
                break
            else: 
                print('Unkown Error')




        elif starting_dungeon_first_choice =='left':
            seperator()
            printwait("You go left and walk down the dark corridor. The muffled voices become louder and you can just barely make out what they are saying...", 3)
            printwait(f"Guard 1: Ohhhh you should have seen this crazy {character.role} last night at the White Goose Tavern! They were deep in their cups, prancing on tables and bellowing some bawdy tune as if they were a drunken bard.", 4)
            seperator()
            printwait("Guard 2: *laughs* By the gods, the state they were in last night! Half-dressed and declaring themselves 'Champion of the White Goose,' dancing atop the tables like they'd been crowned in a court of fools!", 4)
            seperator()
            printwait("Guard 1: And did you notice what they had on 'em? That odd piece... Looked like a carved gem with light swirling inside, as if a small universe were trapped within. Small, but 'twas heavy as a wet hog. And I swear, it whispered when I confiscated it from him.", 4)
            seperator()
            printwait("Guard 2: Aye, was a curious object. Luckily, it's safely locked away in the chest. *gestures to a chest sitting on the ground behind the guards*", 3)
            seperator()

            print("You think to yourself, 'hmmmm I must get my gem back, I still need to deliver it to the king...'")
            while True:
                choice = input(f"what do you want to do? 1. Attack the guards, 2. Attempt to sneak by and steal back your gem, 3. Attempt to convince them into giving back your gem. Please choose the number associated with your choice: ")
                seperator()
                if choice == '1':
                    character.evil_rating += 1
                    if character.role == 'archer':
                        printwait("You quietly knock an arrow, draw your bow and let it fly. It strikes the closer guard and he crumples to the floor.", 3)
                        printwait("The other guard screams in rage, looking around frantically. He spots you lurking and the shadows and charges, drawing his sword. 'YOU BASTARD!' he cries out...", 4)
                        seperator()
                        break
                    elif character.role == 'knight':
                        printwait("You quietly draw your sword, and stealthily creep up to the closer guard. You shove your blade in his back, he crumples to the floor.", 3)
                        printwait("The other guard, who was deep in his goblet, sputters up meade as he sees his friend all of the sudden on the ground. He tosses his drink, drawing his sword. 'YOU BASTARD!' he shouts, as he charges you...", 4)
                        seperator()
                        break
                    elif character.role == 'wizard':
                        printwait("You quietly raise your staff, and loose a potent magic dart. It strikes the closer guard and he crumples to the floor.", 3)
                        printwait("The other guard screams in rage, looking around frantically. He spots you lurking and the shadows and charges, drawing his sword. 'YOU BASTARD!' he cries out...", 4)
                        seperator()
                        break
                    else:
                        print("Unknown Class")

                elif choice == '2':
                    print("You attempt to sneak around the edge of the room in the shadows, but immediately knock into some iron armor strewn on the floor. 'Shit...' you mutter under your breath, but it's too late, the guards spot you...")
                    # time.sleep(4)
                    print(f"Guard 1: Oi! It's {character.name} the {character.role} from last night! What're ya doing out your cell?! Come here...")
                    break

                elif choice == '3':
                    printwait("---For some options, you will roll a Charisma (CHA) check, based on your Charisma modifier---", 3)
                    printwait("---In this instance, you will gain an additional modifier depending on your answer to the earlier puke option, when you first awoke in your cell---", 4)
                    printwait("---You must beat a 12 to succeed on this check (note that this threshold for success will not always be displayed)---", 3)

                    if puke_choice =='y':
                        cha_check = perform_stat_check(character, 12, 'charisma', 2, 1)
                    elif puke_choice =='n':
                        cha_check = perform_stat_check(character, 12, 'charisma', -2, 1)
                    else:
                        print('Unknown Error')

                    if cha_check == True:
                        character.good_rating += 1
                        printwait("You brush off the stone dust on your clothes, stand up straight and walk into the light.", 3)
                        printwait("You say with confidence, 'Ahhh my good fellows, Olgur just let me out, I've come to collect my personal belongings and be on my merry way!'", 3)
                        printwait(f"Guard 1: Ayee, that time already? Gloevar, grab {character.name}'s belongs out the chest behind ye. {character.name}, maybe lay off the meade next time. Trot on now.", 3)
                        printwait("Gloevar hands you your belongings, including your gem.", 3)
                        printwait("You do a slight bow and walk briskly to the door on the other side of the room.", 2)
                        printwait(f"As you put your hand on door handle, you hear a yell from near where you came from, 'Oi!! Stop that {character.role}! They stole my keys!!'", 3)
                        printwait("Before you are able to slip out the door, you feel a rough hand grab your collar and whip you around. 'Think we're stupid or something?!' Gloevar says mockingly...", 3)
                        break

                    else:
                        printwait("You brush off the stone dust on your clothes, stand up straight and walk into the light.", 3)
                        printwait("You say with confidence, 'Ahhh my good fellows, Olgur just let me out, I've come to collect my personal belongings and be on my merry way!'", 3)
                        printwait(f"Guard 1: 'Oi! {character.name}, you shouldn't be out yer cell yet! Get over here...'", 3)
                        break

                        
                else:
                    print("Please input 1, 2 or 3.")

            seperator()
            printwait("---It's time for your first battle!---", 3)
            printwait("---If you die in battle, you will have to restart the entire game! Be careful!---", 3)
            printwait("---You and the rat will take turns doing actions. In a turn you can either decide to Attack, Use a Special Ability, Use an Item, or (in some cases) Attempt to Flee (DEX check)---", 3)
            printwait("---if you attack, you will roll a d20, applying your class's respective modifier (DEX for Archer, STR for Knight, INT for Wizard) against the enemy's Armor Class (AC)---", 3)
            printwait("---If your attack roll is successful, you will do damage based on your weapon (default damage with no weapon is 1d4 + 1)---", 3)
            printwait("---It will then be the enemy's turn. Most monsters will just attack, but some higher level monsters may take other actions---", 3)
            seperator()

            first_dungeon_guard_loot = random.randint(5, 20)
            first_dungeon_guard_chance_of_nothing = random.randint(10, 25)

            # time.sleep(2)

            if choice == '1':
                first_dungeon_enraged_guard = Monster('Enraged Guard', '1d4 + 1', 'Human', {'gold_coins': first_dungeon_guard_loot, 'chance_of_nothing': first_dungeon_guard_chance_of_nothing}, 8, 4, 8, 1, 1, 1)
                battle_result = initiate_combat(character, first_dungeon_enraged_guard, False)
                loot_result = roll_loot(first_dungeon_enraged_guard, character, battle_result)
            else:
                first_dungeon_guard = Monster('Guard', '1d4 + 1', 'Human', {'gold_coins': first_dungeon_guard_loot, 'chance_of_nothing': first_dungeon_guard_chance_of_nothing}, 6, 3, 6, 1, 1, 1)
                battle_result = initiate_combat(character, first_dungeon_guard, False)
                loot_result = roll_loot(first_dungeon_guard, character, battle_result)

            if loot_result in ['no_loot', 'yes_loot', 'fled']:
                break
            elif loot_result == 'death':
                death_status = True
                break
            else: 
                print('Unkown Error')

            seperator()
            # time.sleep(2)

        else:
            print("Please enter left or right.")
            seperator()

    if death_status == True:
        return 'death'

    # time.sleep(2)
    print("You walk out of the room, a bit bruised and hungover still, but alive. You think to yourself, maybe I shouldn't be picking fights in this state...")