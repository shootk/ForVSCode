import re


class Card():
    def __init__(self, color, num=-1):
        self.num = num
        self.pred_num = []
        self.color = color
        self.is_open = False
        if num == -1:
            self.is_open = False
        else:
            self.is_open = True

    def set_num(self, num):
        self.num = num

    def set_pred_num(self, max, min):
        for i in range(min, max + 1):
            self.pred_num.append(i)

    def pop_pred_num(self, num):
        self.pred_num.remove(num)

    def open(self):
        self.num = input("Input number")
        self.is_open = True


class Deck():
    def __init__(self):
        self.black_cards = []
        self.white_cards = []
        self.set_cards()

    def set_cards(self):
        for card_num in range(12):
            self.black_cards.append(Card('b', card_num))
            self.white_cards.append(Card('w', card_num))

    def draw_card(self):
        card_color = input("Draw card's color:")
        if card_color == 'b':
            self.num_of_black_card -= 1
        elif card_color == 'w':
            self.num_of_white_card -= 1

    def open_card(self, card):
        if card.color == 'b':
            self.black_cards[card.num].open = True
        elif card.color == 'w':
            self.white_cards[card.num].open = False

    def black_count(self):
        return len(self.black_cards)

    def white_count(self):
        return len(self.white_cards)


class Player():
    def __init__(self, name):
        self.name = name
        self.on_game = True
        self.cards = []

    def insert_card(self, position, color, num=-1):  # カードを入れる
        card = Card(color, num)
        self.cards.insert(position, card)

    def card_open(self, card_position):  # カードを表にする
        self.cards[card_position].open()
        self.is_on_game()

    def game_over(self):  # ゲームオーバーにする
        self.on_game = False

    def is_on_game(self):  # ゲームに参加しているかどうか確認する
        for card in self.cards:
            if not card.is_open:
                return True
        self.game_over()
        return False


class Me(Player):
    def __init__(self, name):
        super().__init__(name)

    def set_card(self, position, num):
        self.cards


class Game():
    def __init__(self, player_num):
        self.deck = Deck()
        self.players = []
        self.myself = Me(input("Please type your name:"))
        self.set_players(player_num)

    def set_players(self, player_num):
        first_num_of_cards = 6 - player_num
        for i in range(first_num_of_cards):
            self.myself.cards[i].set
        self.players.append(self.myself)
        print("Please input your opponent's name from your left.")
        for i in range(player_num):
            name = input("\nPlayer" + str(i) + "'s name:")
            self.players.append(Player(name))
        for player in range

    def attack(self, attacker, target):
        yes_no = input("Attack is compleate? (y/n) : ")
        if yes_no == 'y':
            card_position = input("Card's position from left:") - 1
            self.players[target].card_open(card_position)
            if not self.players[target].is_on_game:
                self.players.pop(target)
            return True
        else:
            card_position = input("Position of attacker's card:") - 1
            self.players[attacker].set_cards(card_position)
            return False
