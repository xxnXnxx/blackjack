from bjgame.cards import Deck
from bjgame.player import Player, Dealer

class BlackjackGame:
    def __init__(self, player_names):
        self.players = [Player.load(name) for name in player_names]
        self.dealer = Dealer()
        self.deck = Deck()

    def start_game(self):
        while True:
            self.deck.shuffle()
            self.deck.place_cut_card()
            self.collect_bets()
            self.deal_initial_cards()
            self.play_rounds()
            self.settle_bets()
            self.remove_bankrupt_players()
            for player in self.players:
                player.save()
            self.display_balances()
            if not self.ask_to_continue() or not self.players:
                break

    def collect_bets(self):
        for player in self.players:
            while True:
                try:
                    bet = int(input(f'{player.name}, place your bet: '))
                    player.place_bet(bet)
                    break
                except ValueError as e:
                    print(e)

    def deal_initial_cards(self):
        for player in self.players:
            player.clear_hand()
        self.dealer.clear_hand()

        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.deal_card())
            self.dealer.receive_card(self.deck.deal_card())

        self.dealer.hidden_card = self.dealer.hand.pop()
        self.display_hands(initial=True)

    def display_hands(self, initial=False):
        for player in self.players:
            print(f'{player.name}\'s hand: {self.format_hand(player.hand)} (Value: {player.calculate_hand_value()})')
        print(f'Dealer\'s hand: {self.format_hand(self.dealer.hand)} {"[Hidden]" if initial else ""}')

    def format_hand(self, hand):
        return ', '.join([self.deck.format_card(card) for card in hand])

    def play_rounds(self):
        for player in self.players:
            while player.calculate_hand_value() < 21:
                action = input(f'{player.name}, do you want to hit or stand? ').strip().lower()
                if action == 'hit':
                    player.receive_card(self.deck.deal_card())
                    self.display_hands()
                elif action == 'stand':
                    break

        self.dealer.reveal_hidden_card()
        while self.dealer.calculate_hand_value() < 17:
            self.dealer.receive_card(self.deck.deal_card())
        self.display_hands()

    def settle_bets(self):
        dealer_value = self.dealer.calculate_hand_value()
        for player in self.players:
            player_value = player.calculate_hand_value()
            if player_value > 21:
                print(f'{player.name} busted')
                player.balance -= player.bet
            elif dealer_value > 21 or player_value > dealer_value:
                winnings = player.bet * 2
                player.balance += winnings
                print(f'{player.name} win')
            elif player_value == dealer_value:
                player.balance += player.bet
                print(f'{player.name} push')
            else:
                print(f'{player.name} lose')
                player.balance -= player.bet
            #print(f"{player.name}'s balance: ${player.balance}")
    
    def remove_bankrupt_players(self):
        bankrupt_players = [player for player in self.players if player.balance <= 0]
        for player in bankrupt_players:
            print(f'{player.name} has run out of funds and is removed from the game.')
            self.players.remove(player)

    def display_balances(self):
        for player in self.players:
            print(f'{player.name}\'s balance: ${player.balance}')
            
    def ask_to_continue(self):
        response = input('Do you want to play again? (yes/no): ').strip().lower()
        return response == 'yes'
