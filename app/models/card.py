class Card:
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank
        
        if not isinstance(suit, str) or not isinstance(rank, str):
            raise TypeError('Suit and rank must be string!')
    
    def __repr__(self):
        return f'{self.rank} of {self.suit}'