class Player:
    def __init__(self, name, chips=500, folded= False):
        self.name=name
        self.chips=chips
        self.hand=[]
        self.folded=folded
        self.track_bet=0
       
    def reset(self):
        self.track_bet=0
        self.hand=[] 
    def receive_cards(self, *cards):
        # print(cards)
        for card in cards:
            self.hand.append(card)
    def fold(self):
        self.folded = True
        return self.folded
    def bet(self, amount_of_chips):
        if not isinstance(amount_of_chips, int):
            raise TypeError('value not of type int')
        amount_bet= amount_of_chips - self.track_bet
        if amount_bet > self.chips:
            # go all in
            amount_bet= self.chips
        self.chips-=amount_bet
        self.track_bet+= amount_bet
        return amount_bet
            
    def call(self, amount_of_chips):
        if not isinstance(amount_of_chips, int):
            raise TypeError('value not of type int')
        amount_remain= amount_of_chips - self.track_bet
        if amount_remain > self.chips:
            # go all in
            amount_remain= self.chips
        
        self.chips-=amount_remain
        self.track_bet+= amount_remain
        return amount_remain
    
    def check(self, highest_amount):
        if highest_amount == self.track_bet:
            print(f'{self.name} checks')
        else:
            print(f'{self.name} needs to call')
        
    def raise_amount(self, amount_of_chips):
        """i want total to be amount"""
        if not isinstance(amount_of_chips, int):
            raise TypeError('value id not of type int')
        amount_to_raise= amount_of_chips-self.track_bet
        if amount_to_raise > self.chips:
            # go all in
            amount_to_raise= self.chips
        self.chips-= amount_to_raise
        self.track_bet +=  amount_to_raise
        return amount_to_raise