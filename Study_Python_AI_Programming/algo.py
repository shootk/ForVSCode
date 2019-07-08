import numpy as np

class Card():
    def __init__(self, color, num=-1):
        self.num = num
        self.color = color
        if num == -1:
            self.open = False
        else:
            self.open = True


class Deck():
    def __init__(self):
        self.black_cards = []
        self.white_cards = []
        self.min_card_num = 0
        self.max_card_num = 11
        self.num_of_black_card = 12
        self.num_of_white_card = 12
        self.set_cards()

    def set_cards(self):
        for card_num in range(self.max_card_num + 1):
            self.black_cards.append(Card('b', card_num))
            self.white_cards.append(Card('w', card_num))

    def draw_card(self, card_color):
        if card_color == 'b':
            self.num_of_black_card -= 1
        elif card_color == 'w':
            self.num_of_white_card -= 1

    def open_card(self, card):
        if card.color == 'b':
            self.black_cards[card.num].open = True
        elif card.color == 'w':
            self.white_cards[card.num].open = False


class Player():
    def __init__(self, name):
        self.name = name
        self.on_game = True
        self.cards = []

    def set_card(self, card, card_position):
        self.cards.insert(card_position + 1, card)

    def card_open(self, card_position, card_num):
        self.cards[card_position].open = True
        self.cards[card_position].num = card_num
    
    def game_over(self):
        self.on_game = False

class Game():
    def __init__(self, player_num):
        self.deck = Deck()
        self.opponents = []
        self.myself = Player(input("Please type your name:"))
        set_opponents(player_num - 1)

    def set_opponents(self, opponent_num):
        print("Please input your opponent's name from your left.")
        for i in range(opponent_num):
            name = input("\nPlayer" + str(i) +"'s name:")
            opponent.append(Player(name))

    def attack(self):
        target = input("Target number : ")
