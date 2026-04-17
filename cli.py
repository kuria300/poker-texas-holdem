from app.models.card import Card
from app.models.deck import Deck
from app.models.player import Player
from app.models.game import Game

def play_rounds():
    game=Game()

    # game.deck.shuffle()
    # game.deal_card_to_players()
    # game.deal_community_cards()
    # game.deal_turn_card()
    # game.deal_river_card()
    # data=game.convert_card_to_treys(game.player1.hand[0])
    # print(data)
    
    # game.end_show()

    game.play_game()

    
play_rounds()
    