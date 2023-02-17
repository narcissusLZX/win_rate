from collections import Counter
import random
import copy

class Card():
    def __init__(self, number=2, suit=0):
        if (number == 'A'):
            number = 14
        elif (number == 'K'):
            number = 13
        elif (number == 'Q'):
            number = 12
        elif (number == 'J'):
            number = 11
        if (suit == 's'):
            suit = 0
        elif (suit == 'h'):
            suit = 1
        elif (suit == 'c'):
            suit = 2
        elif (suit == 'd'):
            suit = 3
        self.number = int(number)
        self.suit = int(suit)

    def __eq__(self, obj):
        return self.number == obj.number and self.suit == obj.suit

    def __lt__(self, obj):
        return self.number < obj.number or (self.number == obj.number and self.suit < obj.suit)


class Five():
    def __init__(self, five_cards):
    #print(len(five_cards))
        assert len(five_cards) == 5
        self.flush = True
        for i in range(5):
            self.flush = self.flush and (five_cards[i].suit == five_cards[0].suit)
        self.cards = sorted(five_cards)
        flag = True
        for i in range(3):
            flag = flag and (self.cards[i].number == self.cards[i+1].number-1)
        if (flag):
            if (self.cards[4].number == self.cards[3].number+1):
                self.straight = self.cards[4].number
            elif (self.cards[4].number == 14 and self.cards[3].number == 5):
                self.straight = 5
            else:
                self.straight = -1
        else:
            self.straight = -1

        self.numbers = Counter([card.number for card in five_cards])
        numbers = sorted(list(self.numbers.values()))
        if (self.flush and self.straight > 0):
            self.value = 8
        elif (numbers[-1] == 4):
            self.value = 7
        elif (numbers[-1] == 3 and numbers[-2] == 2):
            self.value = 6
        elif (self.flush):
            self.value = 5
        elif (self.straight > 0):
            self.value = 4
        elif (numbers[-1] == 3):
            self.value = 3
        elif (numbers[-1] == 2 and numbers[-2] == 2):
            self.value = 2
        elif (numbers[-1] == 2):
            self.value = 1
        else:
            self.value = 0

    def __eq__(self, obj):
        if (obj == None):
                return False
        if (self.value != obj.value or self.straight != obj.straight):
            return False
        number1 = sorted(self.numbers.items(), key=lambda x:(-x[1], -x[0]))
        number2 = sorted(obj.numbers.items(), key=lambda x:(-x[1], -x[0]))
        for i in range(len(number1)):
            if (number1[i] != number2[i]):
                return False
        return True

    def __lt__(self, obj):
        if (obj == None):
            return False
        if (self.value < obj.value):
            return True
        elif (self.value > obj.value):
            return False
        if (self.straight < obj.straight):
            return True
        elif (self.straight > obj.straight):
            return False
        number1 = sorted(self.numbers.items(), key=lambda x:(-x[1], -x[0]))
        number2 = sorted(obj.numbers.items(), key=lambda x:(-x[1], -x[0]))
        for i in range(len(number1)):
            if (number1[i][0] < number2[i][0]):
                return True
            elif (number1[i][0] > number2[i][0]):
                return False
        return False

class Player():
    def __init__(self, card1, card2):
        self.cards = [card1, card2]
        self.best = None

    def calc_best(self, common):
        self.best = None
        for abandom1 in range(7):
            for abandom2 in range(abandom1+1, 7):
        #print(common, self.cards, all)
                all = self.cards+common
                all.pop(abandom2)
                all.pop(abandom1)
                now_five = Five(all)
                if (self.best == None or self.best < now_five):
                    self.best = Five(all)

    def __eq__(self, obj):
        return self.best == obj.best

    def __lt__(self, obj):
        return self.best < obj.best


def calc_winner(common, players):
    ret = [0]*len(players)
    for player in players:
        player.calc_best(common)
    for i in range(len(players)):
        flag = True
        for player in players:
            flag = flag and (player < players[i] or player == players[i])
        if (flag):
            ret[i] = 1

    return ret


if __name__ == "__main__":
    players = [Player(Card('K',0), Card('9',1)), Player(Card('Q', 1), Card('A', 0))]
    common = [Card(9,2),Card(7,3),Card(4,0)]
    mode =5 - len(common)
    win_times = [0]*len(players)
    total_times = 1000
    all_cards = []
    for number in range(2, 15):
        for suit in range(4):
            card = Card(str(number), str(suit))
            flag = True
            for player in players:
                if card == player.cards[0] or card == player.cards[1]:
                    flag = False
                    break
            for ccard in common:
                if card == ccard:
                    flag = False
                    break
            if (flag):
                all_cards.append(card)
    for i in range(total_times):
        s_common = random.sample(all_cards, mode)
        win = calc_winner(common+s_common, players)
        for i in range(len(players)):
            win_times[i] += win[i]
    print(win_times, total_times)
    print([win_time / total_times for win_time in win_times])
