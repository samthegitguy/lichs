import sys
import os
import berserk
import chess
from pathlib import Path
from getpass import getpass

from Game import Game
from lichs.api_key import set_api

token_file = Path(__file__).parent.absolute() / "token.key"

def set_token(key):
    token_file.write_text(key)
    print("The API-token was entered and saved.")

def get_token():
    return getpass("Please enter your token: ")
# def get_opt(opt):
    # TODO Get option function
    

def main():
    
    if len(sys.argv) == 2:
            set_token(sys.argv[1])

    if not token_file.exists():
        print("Please provide a token key")
        print("See the instructions in the Github README:")
        print("https://github.com/Cqsi/lichs#how-to-generate-a-personal-api-token")
        set_token(get_token())


    token = token_file.read_text()
    session = berserk.TokenSession(token)
    client = berserk.clients.Client(session)
    board = berserk.clients.Board(session)

    # Gets your account data, e.g ["id"], ["username"]
    errOccurring = True
    while errOccurring:
        try:
            account_data = client.account.get()
            player_id = account_data["id"]
            errOccurring = False
        except berserk.exceptions.ResponseError as e:
            print("Error ", e, "occurred.")
            print("Unable to connect to Lichess")
            print("Check if your token key is right")
            print("Or try again later")
            set_token(get_token())

    # Welcome text
    print("Welcome to Lichess in the Terminal (lichs)\n")
    print("Type either\nP to play\nH for help\nQ to quit ")
    optFlag = True # Flag for options menu
    while optFlag == True:
        choice = input("Choose your option: ")
        if choice.lower() == "h":
            print("You will find help on the website that's opening")
            os.system("start https://github.com/Cqsi/lichs/blob/master/README.md#usage")
        elif choice.lower() == "q":
            print("Quitting...")
            sys.exit(0)
        elif choice.lower() == "p": 
            optFlag = False
        else: print("Please choose from either P to play, H for help, or Q to quit")
        
    print("What kind of chess would you like to play? \n1. Rapid (10+0)\n2. Classical (30+0)\n")
    num = input("Please choose from either 1 (Rapid, 10+0) or 2 (Classical, 30+0): ")
    typeFlag = True # Flag for gametype validation
    while typeFlag == True:
        if num=="1":
            time=10
            typeFlag = False
        elif num=="2":
            time=30
            typeFlag = False
        else:
            num = input("Please choose from either 1 (Rapid, 10+0) or 2 (Classical, 30+0): ")

    print("Searching after opponent...")
    board.seek(time, 0)

    for event in board.stream_incoming_events():
        if event['type'] == 'gameStart':
            print("An opponent was found!")

            isWhite = True
            color = "Black" # We set the color to the opposite color of the player

            if player_id != client.games.export(event['game']['id'])['players']['white']['user']['id']:
                isWhite = False
                color = "White"
                print("You're playing as black!")
                print("White's turn...")
            else:
                print("You're playing as white!")
            game = Game(board, event['game']['id'], player_id, isWhite, color, time)
            game.start()

if __name__ == "__main__":
    main()
