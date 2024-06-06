#!/usr/bin/env python3

from bjgame.game import BlackjackGame

def main():
    num_players = int(input('Enter number of players (1-4): '))
    player_names = [input(f'Enter name for player {i+1}: ') for i in range(num_players)]
    game = BlackjackGame(player_names)
    game.start_game()

if __name__ == "__main__":
    main()
