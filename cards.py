import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])

class Deck:
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suit_emojis = {
        'Clubs': '♣️',
        'Diamonds': '♦️',
        'Hearts': '♥️',
        'Spades': '♠️'
    }
    
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks] * 8
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
        self.cut_card_position = random.randint(60, 80)

    def place_cut_card(self):
        self.cut_card_position = random.randint(60, 80)
    
    def deal_card(self):
        if len(self.cards) == 0:
            self.__init__()
        return self.cards.pop(0)
    
    def format_card(self, card):
        return f"{card.rank}{self.suit_emojis[card.suit]}"
