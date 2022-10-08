from twl import check
from random import shuffle

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

# Create dictionary of each letter and its value
letters_to_points = {letters:points for letters, points in zip(letters, points)}
letters_to_points[" "] = 0

tile_list = []
# Create available letter list
def tile_shuffle():
    for i in range(12):
        tile_list.append("E")
    for i in range(9):
        tile_list.append("A")
        tile_list.append("I")
    for i in range(8):
        tile_list.append("O")
    for i in range(6):
        tile_list.append("N")
        tile_list.append("R")
        tile_list.append("T")
    for i in range(4):
        tile_list.append("L")
        tile_list.append("S")
        tile_list.append("U")
        tile_list.append("D")
    for i in range(3):
        tile_list.append("G")
    for i in range(2):
        tile_list.append(" ")
        tile_list.append("B")
        tile_list.append("C")
        tile_list.append("M")
        tile_list.append("P")
        tile_list.append("F")
        tile_list.append("H")
        tile_list.append("V")
        tile_list.append("W")
        tile_list.append("Y")
    for i in range(1):
        tile_list.append("K")
        tile_list.append("J")
        tile_list.append("X")
        tile_list.append("Q")
        tile_list.append("Z")
    shuffle(tile_list)

# Calculate score of a played word
def score_word(word):   
    point_total = 0
    for letter in word:
        point_total += letters_to_points.get(letter.upper(), 0)
    return point_total

# Create dictionaries of who has played which words and how many points each player has
player_to_words = {"player1": ["BLUE", "TENNIS","EXIT"], "wordNerd": ["EARTH", "EYES", "MACHINE"], "Lexi Con": ["ERASER", "BELLY", "HUSKY"], "Prof Reader": ["ZAP", "COMA", "PERIOD"]}
player_tiles = {}
player_to_points = {}

# Checks if word is playable from player's tiles
def tile_checker(player, word):
    temp_tiles = player_tiles[player].copy()
    for letter in word:
        if temp_tiles.count(letter.upper()) > 0:
            temp_tiles.remove(letter.upper())
        else:
            print("Word is not possible with the tiles in your hand!")
            return False
    return True

# Add newly-played word to player's list
def play_word(player):
    tiles_in_hand = False
    while not tiles_in_hand:
        print("Please enter your word below. If no words are available, press Enter to pass your turn.")
        word = input()
        if word == "":
            return 1
        # Checks if word is valid Scrabble word.
        while not check(word.lower()):
            print("Invalid word, please try another word. If no words are available, press Enter to pass your turn.")
            word = input()
            if word == "":
                return 1
        tiles_in_hand = tile_checker(player, word)
    for letter in word:
        player_tiles[player].remove(letter.upper())
    try:
        player_to_words[player].append(word)
    except:
        print("Player entered is not currently playing!")
        return 0
    return 0

# Calculate points for currently-played words
def update_point_totals():
    for player, words in player_to_words.items():
        player_points = 0
        for word in words:
            player_points += score_word(word)
        player_to_points[player] = player_points

# Returns individual player's score
def player_score(player):
    update_point_totals()
    return player_to_points[player]

# Allows multiple words to be inputted and returns the point total for all words entered.
def point_counter():
    point_count = 0
    print("Enter words to be totaled. When finished, press enter again to calculate the total.")
    word = input()
    while word != '':
        point_count += score_word(word)
        word = input()
    return point_count

# print(point_counter())

#  Adds player to game
def add_player(player):
    player_to_words[player] = []
    player_tiles[player] = []

def tile_swapper(player):
    swap_response = 'YES'
    while swap_response != '':
        print("Enter the letter you would like to remove and press Enter. If you are done swapping out letters, press enter again.")
        swap_response = input()
        if swap_response == '':
            break
        if player_tiles[player].count(swap_response.upper()) > 0:
            tile_list.append(player_tiles[player].pop(player_tiles[player].index(swap_response.upper())))
        else:
            print("Entry not found in player's hand. Please try again.")

# Simulates one round of gameplay. Loops until player indicates game is over.
def game_round():
    round = 1
    exit = ''
    while exit != 'YES':
        print(f"Round {round}:")
        pass_count = 0
        for player in player_to_words:
            if len(player_tiles[player]) < 7:
                for i in range(7 - len(player_tiles[player])):
                    player_tiles[player].append(tile_list.pop(0))
            print(f"{player}'s turn!")
            print("Your tiles are:")
            print(list(player_tiles[player]))
            print("Do you wish to swap your tiles out and pass your turn?")
            swap_tiles = ""
            while swap_tiles.upper() != "YES":
                swap_tiles = input()
                if swap_tiles.upper() == 'NO':
                    pass_count += play_word(player)
                    break
                elif swap_tiles.upper() != "YES":
                    print("Please enter 'Yes' or 'No'")
            if swap_tiles.upper() == "YES":
                tile_swapper(player)
        round += 1
        if len(tile_list) == 0:
            for player in player_tiles:
                if len(player_tiles[player]) == 0:
                    return
            if pass_count == player_count:
                return
        print(f"Round {round - 1} complete. Do you want to quit here?")
        exit = input().upper()

player_to_words.clear()
tile_shuffle()

print("How many players will be playing?")
try:
    player_count = int(input())
except:
    print("You did not enter a number, please try again.")

for i in range(player_count):
    print(f"Please enter the name for player {i + 1}:")
    add_player(input())

for i in range(7):
    for player in player_tiles:
        player_tiles[player].append(tile_list.pop(0))


game_round()


# print("Enter player name to view score.")
# print("Current players are:")
# print(list(player_to_words.keys()))
# print(player_score(input()))

update_point_totals()
input("Press enter to see the final score.")
print(player_to_points)