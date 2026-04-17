import random 
from .card import Card
# this class contains all the cards insisde a deck box 52
class Deck:
    def __init__(self):
        self.rank=['two', 'three', 'four', 'five','six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'Ace']
        self.suit=['Hearts', 'Diamonds', 'Clubs', 'spades']
        self.cards=[]
    
        for rank in self.rank:
            for suit in self.suit:
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_cards(self):
        return self.cards.pop()