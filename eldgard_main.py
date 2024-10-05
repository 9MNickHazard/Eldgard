import time
import random
import re
import pprint

from story_segments import intro_and_char_creation, first_dungeon_jail, southwold_1
from character_and_monsters import Character

def main():
    while True:
        player_character = intro_and_char_creation()

        story_segments = [
            first_dungeon_jail,
            southwold_1
        ]

        for story in story_segments:
            result = story(player_character)
            if result == 'death':
                print("---YOU HAVE DIED! GAME OVER!---")
                break
            elif result == 'quit':
                print("You quit the game.")
                break
        else:
            print("---END OF BETA TEST---")
        
        play_again = input("Would you like to play again? (y/n): ").lower()
        if play_again != 'y':
            break





# # FOR TESTING!! MAIN()
# def main():
#     test_character = player_character = Character(name='Nick_test', role='knight', pronouns=1, strength=25, dexterity=25, constitution=25, intelligence=25, wisdom=25, charisma=25)

#     while True:
#         story_segments = [
#             first_dungeon_jail,
#             southwold_1
#         ]

#         for story in story_segments:
#             result = story(test_character)
#             if result == 'death':
#                 print("---YOU HAVE DIED! GAME OVER!---")
#                 break
#             elif result == 'quit':
#                 print("You quit the game.")
#                 break
#         else:
#             print("---END OF BETA TEST---")
        
#         play_again = input("Would you like to play again? (y/n): ").lower()
#         if play_again != 'y':
#             break


if __name__ == "__main__":
    main()