import pickle
import os

class Player:
    def __init__(self, name, balance=10000):
        self.name = name
        self.balance = balance
        self.hand = []
        self.bet = 0

    def place_bet(self, amount):
        if amount <= self.balance:
            self.bet = amount
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

    def receive_card(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        value, aces = 0, 0
        for card in self.hand:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(card.rank)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def save(self):
        with open(f'{self.name}.pkl', 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, name):
        if os.path.exists(f'{name}.pkl'):
            with open(f'{name}.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return cls(name)

class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer', balance=float('inf'))
        self.hidden_card = None

    def reveal_hidden_card(self):
        self.hand.append(self.hidden_card)
        self.hidden_card = None
import pickle

class Player:
    def __init__(self, name, balance=10000):
        self.name = name
        self.balance = balance
        self.hand = []
        self.bet = 0

    def place_bet(self, amount):
        if amount <= self.balance:
            self.bet = amount
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")
    
    def receive_card(self, card):
        self.hand.append(card)
    
    def calculate_hand_value(self):
        value, aces = 0, 0
        for card in self.hand:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(card.rank)
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
        
        return value
    
    def save(self):
        with open(f'{self.name}.pkl', 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(name):
        try:
            with open(f'{name}.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return Player(name)

class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer', balance=float('inf'))
        self.hidden_card = None
    
    def reveal_hidden_card(self):
        self.hand.append(self.hidden_card)
        self.hidden_card = None
