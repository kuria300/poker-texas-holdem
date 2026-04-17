import time
import random
from .deck import Deck
from .player import Player
from treys import Card as TreysCard, Evaluator
from .card import Card

class Game:
    def __init__(self):
        self.pot=0
        self.community_card=[]
        self.state='pre-flop'
        self.current_highest_amount_round=0
        self.deck=Deck()
        self.player1=Player('Eugene')
        self.player2=Player('AI')
        self._turn =self.player1

        self.evaluator=Evaluator()
        
    @property
    def turn(self):
        return self._turn
    @turn.setter
    def turn(self, player):
        if not isinstance(player, Player):
            raise TypeError('player is not an instance of Player class')
        
        self._turn=player
        
    
    def reset_bets(self):
        self.player1.track_bet=0
        self.player2.track_bet=0
        self.current_highest_amount_round=0
        
    def deal_card_to_players(self):
        self.player1.receive_cards(self.deck.deal_cards(), self.deck.deal_cards())
        self.player2.receive_cards(self.deck.deal_cards(), self.deck.deal_cards())
         
        print('p1 cards', self.player1.hand)
        print('p2 cards', self.player2.hand)
         
    def deal_community_cards(self):
        """this is in flop"""
        for _ in range(3):
            self.community_card.append(self.deck.deal_cards())
        return self.community_card
    def deal_turn_card(self):
        """ this is in turn """
        self.community_card.append(self.deck.deal_cards())
        return self.community_card
    def deal_river_card(self):
        """this is in last round riveer"""
        self.community_card.append(self.deck.deal_cards())
        return self.community_card
    
    # this helps convert the card class(a card representation) to treys card format for easy evaluation using the rank_map and suit_map
    def convert_card_to_treys(self, card):
        rank_map = {
           'two':'2','three':'3','four':'4','five':'5','six':'6',
           'seven':'7','eight':'8','nine':'9','ten':'T',
           'jack':'J','queen':'Q','king':'K','ace':'A'
        }

        suit_map = {
            'spades': 's', 'hearts': 'h', 'diamonds': 'd', 'clubs': 'c'
        }
        
        #returns the card in treys format 2 of hearts will be 2h then convert to int representation
        return TreysCard.new(f"{rank_map[card.rank.lower()]}{suit_map[card.suit.lower()]}")
        
    def betting_round(self):
         print(f'\n----ROUND-{self.state.upper()}!----')
         self.turn=self.player1
         self.player1.has_played=False
         self.player2.has_played=False
         while True:
            current_player=self.turn
            print(f'\n-----{current_player.name}"s turn-----')
            print(f"\nPot: {self.pot} | Current highest bet: {self.current_highest_amount_round}")
            print(f"{current_player.name} your Chips: {current_player.chips} | {current_player.name} your Bet: {current_player.track_bet}")
            
            """player action """
            if current_player == self.player1:
                while True:
                    if self.current_highest_amount_round == 0 and self.state != 'pre-flop':
                        # print("Options: bet, check, raise, fold")
                        valid_actions = ['bet', 'check', 'fold']
                    elif self.player1.track_bet == self.current_highest_amount_round:
                        # print("Options: check, raise, fold")
                        valid_actions = ['check', 'fold', 'raise']
                    else:
                        # print("Options: call, raise, fold")
                        valid_actions = ['call', 'fold', 'raise']
                        
                    action = input(f"\nYour turn {valid_actions}: ").lower().strip()
        
                    if action not in valid_actions:
                        print(f'action must be either {valid_actions}')
                        continue
                    else:
                        break
                
            else:
                print(f"{current_player.name} is thinking...")
                time.sleep(2)
                if self.current_highest_amount_round == 0 and self.state != 'pre-flop':
                    action = random.choice(['bet', 'check', 'fold'])
                elif current_player.track_bet == self.current_highest_amount_round:
                    action = random.choice(['check', 'raise'])
                else:
                    action = random.choice(['call', 'raise'])
                print(f'{current_player.name} decided to {action}')
                
             
            if action == 'raise': 
                if current_player == self.player1:
                    while True:
                        amount=int(input(f'Enter amount (amount > {self.current_highest_amount_round}) to raise:'))
                        if not isinstance(amount, int):
                            raise TypeError('value needs to be integer')
                        if amount >  self.current_highest_amount_round:
                            break
                        
                        print('Value must be greater than highest placed bet')
                        continue
                        
                    bet=current_player.raise_amount(amount)
                    self.current_highest_amount_round=amount
                    self.pot+=bet
                else:
                    amount=self.current_highest_amount_round * 2
                    
                    bet=current_player.raise_amount(amount)
                    self.current_highest_amount_round=amount
                    self.pot+=bet
                    
                
                    print(f"\nPot: {self.pot} | Current highest bet: {self.current_highest_amount_round}")
                    print(f"{current_player.name} your Chips: {current_player.chips} | {current_player.name} your Bet: {current_player.track_bet}")
                
            if action == 'call':
                
                bet=current_player.call(self.current_highest_amount_round)
                # self.current_highest_amount_round=bet
                self.pot+=bet
                
                print(f"\nPot: {self.pot} | Current highest bet: {self.current_highest_amount_round}")
                print(f"{current_player.name} your Chips: {current_player.chips} | {current_player.name} your Bet: {current_player.track_bet}")
                
            if action == 'check':
                current_player.check(self.current_highest_amount_round)
            if action == 'bet':
                if current_player == self.player1:
                    while True:
                        amount=int(input(f'enter amount to bet:'))
                        if not isinstance(amount, int):
                            raise TypeError('value needs to be integer')
                        if amount > 0:
                            break
                        
                        print('Value must be greater than 0')
                        continue

                    bet=current_player.bet(amount)
                    self.current_highest_amount_round=amount
                    self.pot+=bet
                else:
                    amount= random.randint(20, 100)
                    bet=current_player.bet(amount)
                    self.current_highest_amount_round=amount
                    self.pot+=bet
                    
                    print(f"\nPot: {self.pot} | Current highest bet: {self.current_highest_amount_round}")
                    print(f"{current_player.name} your Chips: {current_player.chips} | {current_player.name} your Bet: {current_player.track_bet}")
            if action == 'fold':
                if current_player == self.player1:
                    self.player1.fold()
                    self.player2.chips+= self.pot
                    print(f'\n {self.player2.name} has won {self.pot} chips total: {self.player2.chips} chips!!')
        
                else:
                    self.player2.fold()
                    self.player1.chips+= self.pot
                    print(f'{self.player1.name} has won {self.pot} chips total: {self.player1.chips} chips!!')
                self.pot=0
                return 'over'
            
                
            """check condition if bets match"""
            if self.player1.track_bet == self.player2.track_bet and self.player1.has_played and self.player2.has_played:
                print(f"\n--- {self.state} betting finished! ---")
                break
                    
            """"switching players"""
            if self.turn == self.player1:
                self.turn = self.player2
                self.player2.has_played=True
        
            else:
                self.turn = self.player1
                self.player1.has_played=True
                

    def first_betting_round(self):
        print(f'\n------WELCOME TO TEXAS BABY!------')
        
        """initial money before anything"""
        if self.turn == self.player1:
            self.small_blind = 20
            self.big_blind = 40
            
            print('\n--- Posting Blinds ---')
            
            small_b = self.player1.call(self.small_blind)
            big_b = self.player2.call(self.big_blind)
            
            self.pot += small_b + big_b
            self.current_highest_amount_round = self.big_blind
            
            print(f'{self.player1.name} posts small blind: {small_b}')
            print(f'{self.player2.name} posts big blind: {big_b}')
            print('\n------results------')
            print(f'Pot is now {self.pot}')
            print(f'Current highest bet is {self.current_highest_amount_round}')
        
        self.deck.shuffle()
        self.deal_card_to_players()
        # self.turn=self.player2

        return self.betting_round()

    def end_show(self):
        print(f'\n---END OF ROUND CARD EVALUATION - {self.state.upper()} ROUND---')
        print(f'{self.player1.name} hand: {self.player1.hand}')
        print(f'{self.player2.name} hand: {self.player2.hand}')
        print(f'Community cards: {self.community_card}')

        # convert player hands and community cards to treys format 
        player1_hand_treys = [self.convert_card_to_treys(card) for card in self.player1.hand]
        player2_hand_treys = [self.convert_card_to_treys(card) for card in self.player2.hand]
        community_cards_treys = [self.convert_card_to_treys(card) for card in self.community_card]

        print(player1_hand_treys, player2_hand_treys, community_cards_treys)
        
        # evaluate the hands and get the score using evaluator obj method evaluate and returns a score the lower the score the better
        score= self.evaluator.evaluate(community_cards_treys, player1_hand_treys)
        score2= self.evaluator.evaluate(community_cards_treys, player2_hand_treys)

        print(f'{self.player1.name} score: {score}')
        print(f'{self.player2.name} score: {score2}')
        
        # get rank class of score using the method get_rank_class eg score 1 is royal flush and 10 is pair
        score_class1= self.evaluator.get_rank_class(score)
        score_class2= self.evaluator.get_rank_class(score2)

        print(f'{self.player1.name} hand rank: {score_class1}')
        print(f'{self.player2.name} hand rank: {score_class2}')

        if score < score2:
            #convert the score class into a string representation of the hand type  using class_to_string eg 1 becomes royal flush 
            hand_type = self.evaluator.class_to_string(score_class1)
            hand_type2 = self.evaluator.class_to_string(score_class2)

            
            print(f'{self.player1.name} wins {self.pot} chips, total:{self.player1.chips+self.pot} with {hand_type} against {self.player2.name}"s hand {hand_type2}!')
            self.player1.chips+= self.pot

        
        elif score2 < score:
            hand_type = self.evaluator.class_to_string(score_class1)
            hand_type2 = self.evaluator.class_to_string(score_class2)

            print(f'{self.player2.name} wins {self.pot} chips, total:{self.player2.chips+self.pot} with {hand_type2} against {self.player1.name} {hand_type}!')
            self.player2.chips+= self.pot
        else:
            self.player1.chips+= self.pot//2
            self.player2.chips+= self.pot//2
            print(f'It is a tie! {self.player1.name} and {self.player2.name} split the pot, each getting {self.pot//2} chips!')
            
        return 'game_end'

    def play_game(self):
        if self.first_betting_round() == 'over':
            return
        
        self.state='flop'
        self.reset_bets()
        self.deal_community_cards()
        print(f'\n--{self.community_card}--')

        if self.betting_round() == 'over':
            return

        
        self.state='turn'
        self.reset_bets()
        self.deal_turn_card()
        print(f'\n--{self.community_card}--')

        if self.betting_round() == 'over':
            return

        
        self.state='river'
        self.reset_bets()
        self.deal_river_card()
        print(f'\n--{self.community_card}--')

        if self.betting_round() == 'over':
            return

        if self.end_show() == "game_end":
            print('------GAME OVER------')
