import time
import random
import re

from story_segments import intro_and_char_creation, first_dungeon_jail



def main():
    while True:
        player_character = intro_and_char_creation()

        story_segments = [
            first_dungeon_jail
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


if __name__ == "__main__":
    main()