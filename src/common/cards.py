CLIENT_COMMANDS = ['register', 'createGame', 'joinGame', 'getListOfGames', 'getGameStatus',
                   'attack', 'cover', 'take', 'retransfer', 'quit', 'skip', 'restart']
SUITS = ['h', 'd', 's', 'c']
VALUES = ['6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']


import client_command

class Card:
    '''Presents cards and some operations on them: >, <, ==, !=.
    '''
    def __init__(self, str):
        self._trump_suit = None
        self._suit = str[0]
        self._value = str[1]
        owner = str[2:]
        self._owner = None
        if owner != '':
            self._owner = owner[1:len(owner)-1]
    def set_owner(self, name):
        '''Change the owner of the card.
        '''
        self._owner = name
    def forget_owner(self):
        '''Reset the value of the card's owner.
        '''
        self._owner = None
    def set_trump_suit(self, trump):
        '''Set the current trump. Function will be removed.
        '''
        if trump not in SUITS:
            self._trump_suit = 'd'
        self._trump_suit = trump
    def get_suit(self):
        '''Get the suit of this card.
        '''
        return self._suit
    def get_value(self):
        '''Get the value of this card.
        '''
        return self._value
    def get_owner(self):
        '''Get card owner's name.
        '''
        return self._owner
    def owner_known(self):
        '''Returns True if the owner of this
        card is known. Returns False otherwise.
        '''
        return self._owner != None
    def is_trump(self):
        '''Checks if this card is a trump?
        '''
        return self.get_suit() == self._trump_suit
    def get_str_repr(self):
        '''Get card's representation in fromat '[cA]'.
        '''
        return '[' + str(self) + ']'
    def __gt__(self, other):
        '''Checks if self-card can cover other-card
        '''
        if isinstance(other, str):
            if len(other) < 2:
                return False
            if self.is_trump() and self._trump_suit != other[0]:
                return True
            if not self.is_trump() and self._trump_suit == other[0]:
                return False
            if self.get_suit() == other[0]:
                return VALUES.index(self.get_value()) > VALUES.index(other[1])
        if isinstance(other, Card):
            if self.is_trump() and not other.is_trump():
                return True
            if not self.is_trump() and other.is_trump():
                return False
            if self.get_suit() == other.get_suit():
                return VALUES.index(self.get_value()) > VALUES.index(other.get_value())
        return False
    def __lt__(self, other):
        '''Checks if other-card can cover self-card.
        '''
        return other > self
    def __eq__(self, other):
        '''Checks if self-card and other-card are the same card
        '''
        if isinstance(other, str):
            if len(other) < 2:
                return False
            return self.get_suit() == other[0] and self.get_value() == other[1]
        if isinstance(other, Card):
            return self.get_suit() == other.get_suit() and self.get_value() == other.get_value()
        return False
    def __ne__(self, other):
        '''Checks if self-card and other-card are different cards.
        '''
        return not self == other
    def __nonzero__(self):
        '''For converting to boolean in conditional context.
        Returns true if card has a trump suit, false otherwise.
        '''
        return self.is_trump()
    def get_card_str(self):
        '''Returns card's string representation without owner.
        '''
        return self.get_suit() + self.get_value()
    def __str__(self):
        '''String representation of the card.
        Is used when the Card instance is used in a string context.
        '''
        str = self.get_suit() + self.get_value()
        if self.owner_known():
            str += '\''+self.get_owner()+'\''
        return str
    def __repr__(self):
        '''Returns full string representation of the card.
        '''
        return self.__str__()


class Cards(list):
    '''Presents a list of cards of Card class.
    '''
    def add_card(self, card):
        '''Adds a card to the list.
        '''
        self.append(card)
    def add_cards(self, cards):
        '''Add cards (instances of Cards class) to the list.
        '''
        for card in cards:
            self.add_card(card)
    def extract_card(self, card):
        '''Returns and removes the card.
        '''
        for c in self:
            if c == card:
                self.remove(c)
    def extract_cards(self, cards):
        '''Returns and removes specified cards.
        '''
        for card in cards:
            self.extract_card(card)
    def has_card(self, card):
        '''Returns True if list contains the card.
        False otherwise.
        '''
        for x in self:
            if x == card:
                return True
        return False
    def get_number_of_cards(self):
        '''Returns number of cards.
        '''
        return len(self)
    def get_least_trump(self, trump_card):
        '''Gets least trump value in the list.
        '''
        trumps = []
        for x in self:
            if x.get_suit() == trump_card.get_suit():
                trumps.append(x)
        def min(card1, card2):
            if card1 < card2:
                return card1
            return card2
        return reduce(min, trumps)
    def all_different(self):
        '''Checks if all cards in the list are different.
        '''
        for i in range(len(self) - 1):
            test1 = self[i]
            for j in range(i + 1,len(self)):
                test2 = self[j]
                if test1 == test2:
                    return False
        return True
    def get_str_repr(self):
        '''Returns cards' string representation
        in the format [c0][cJ][cQ]
        '''
        return ''.join([x.get_str_repr() for x in self])
    def clear(self):
        '''Remove all cards from the list.
        '''
        del self[:]

def is_card(str):
    '''Checks if string str is a card.
    '''
    return len(str) == 2 and str[0] in SUITS and str[1] in VALUES