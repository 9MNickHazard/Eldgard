import time
import random
import re


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

# player character
class Character:
    def __init__(self, name, role, pronouns, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.role = role
        self.pronouns = pronouns

        self.character_level = 1

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

######################################


# basic monster
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