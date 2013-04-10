import random
import cards

SUITS = ('h', 'd', 's', 'c')
SUITS_COMP = ('s', 'c', 'd', 'h')
VALUES = ('6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A')


class Deck(list):
    def __init__(self, compatibility_test_mode=False):
        '''Fills object with non-shuffled deck.
        '''
        if compatibility_test_mode:
            self.extend(self._str_to_card_deck(self._get_ordered_str_deck_comp()))
        else:
            self.extend(self._str_to_card_deck(self._get_ordered_str_deck()))
    def shuffle(self):
        '''Shuffles the deck.
        '''
        shuffled = []
        while self != []:
            card = random.choice(self)
            self.remove(card)
            shuffled.append(card)
        self.extend(shuffled)
    def _get_ordered_str_deck(self):
        '''Returns non-shuffled deck with cards
        in string representation.
        '''
        deck = []
        i = 0
        for suit in SUITS:
            for value in VALUES:
                deck.append(suit + value)
        return deck
    def _get_ordered_str_deck_comp(self):
        '''Returns non-shuffled deck with cards
        in string representation for compatibility test.
        '''
        deck = []
        for value in VALUES:
            for suit in SUITS_COMP:
                deck.append(suit + value)
        return deck
    def _str_to_card_deck(self, str_deck):
        '''Converts list of string cards to a list
        of cards.Card objects.
        '''
        card_deck = []
        for str_card in str_deck:
            card_deck.append(cards.Card(str_card))
        return card_deck  
    def show_trump_card(self):
        '''Returns the trump.
        '''
        return cards.Card(self[-1].get_suit() + self[-1].get_value())
    def take_cards(self, num):
        '''Returns cards from the top of the deck.
        Number of cards is maximum possible
        but less or equal to num. Returned cards are removed
        from the deck.
        '''
        if len(self) == 0:
            return []
        if len(self) < num:
            num = len(self)
        take = self[:num]
        del self[:num]
        return take
    def is_empty(self):
        '''Returns True if the deck is empty.
        Returns False if not.
        '''
        return self.get_number_of_cards() == 0
    def get_common_repr(self):
        '''Returns deck's representation
        in '[d0][dJ][dQ][dK]' format.
        '''
        return '[' + str(self.get_number_of_cards()) +']'
    def get_number_of_cards(self):
        '''Returns number of cards left in the deck.
        '''
        return len(self)
    def __str__(self):
        '''Conversion to a string.
        '''
        string = ''
        for x in self:
            string += str(x)
        return string
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()