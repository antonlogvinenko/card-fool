'''Containts definition of Table class.
'''

import cards

class Table(list):
    '''Represents a set of pairs [bottom<top].
    '''
    def _card_encl(self, card):
        '''Returns '[cA]' if card is cA.
        '''
        return '[' + str(card) + ']'
    def _cover_encl(self, bottom, top):
        '''Returns a cover pair like '[c6<c7]'.
        '''
        return self._card_encl(str(bottom) + '<' + str(top))
    def clear(self):
        '''Removes all cards from the table.
        '''
        del self[:]
    def take_all(self):
        '''Returns all cards from the table in the form of list.
        '''
        all = []
        for x in self:
            if isinstance(x, list):
                all.extend(x)
            else:
                all.append(x)
        self.clear()
        return all
    def put_on_cards(self, cards):
        '''Adds cards on the table as uncovered.
        '''
        for card in cards:
            self.put_on_card(card)
    def put_on_card(self, card):
        '''Adds card on the table as uncovered.
        '''
        self.append(card)
    def get_bottom_cards(self):
        '''Returns list with all bottom cards.
        '''
        bottom_cards = []
        for smth in self:
            if isinstance(smth, list):
                bottom_cards.append(smth[0])
            else:
                bottom_cards.append(smth)
        return bottom_cards
    def has_same_value(self, value):
        '''Returns True if some card on the table
        has the 'value' value. Returns False otherwise.
        '''
        for card in self.convert_to_cards():
            if value == card.get_value():
                return True
        return False
    def get_covering_cards(self):
        '''Returns a list of all cards covering smth.
        '''
        covering_cards = []
        for smth in self:
            if isinstance(smth, list):
                covering_cards.append(smth[1])
        return covering_cards
    def get_covered_cards(self):
        '''Returns a list of all cards covered with smth.
        '''
        covered_smth = []
        for smth in self:
            if isinstance(smth, list):
                covered_smth.append(smth[0])
        return covered_smth
    def get_uncovered_cards(self):
        '''Returns a list of all not covered cards.
        '''
        uncovered_smth = []
        for smth in self:
            if isinstance(smth, cards.Card):
                uncovered_smth.append(smth)
        return uncovered_smth
    def add_retransfered(self, retransfered_cards):
        '''Returns True and adds retransfered_cards to the
        tabe as uncovered if it is possible to add.
        Returns False if it is not.
        '''
        if not self.possible_to_put_cards(retransfered_cards):
            return False
        for card in retransfered_cards:
            self.put_on_card(card)
        return True
    def cover_card(self, bottom, top):
        '''Returns True and covers card bottom with card
        top if bottom is on the table.
        '''
        if bottom in self:
            self.append([self.pop(self.index(bottom)), top])
            return True
        return False
    def __str__(self):
        '''String representation of the table.
        '''
        string = ''
        for x in self:
            if isinstance(x, list):
                string += self._cover_encl(x[0], x[1])
            else:
                string += self._card_encl(x)
        return string
    def has_uncovered_cards(self):
        '''Returns True if the table has uncovered cards.
        False otherwise.
        '''
        for x in self:
            if isinstance(x, cards.Card):
                return True
        return False
    def has_covered_cards(self):
        '''Returns True if the table has covered cards.
        False otherwise.
        '''
        for x in self:
            if isinstance(x, list):
                return True
        return False
    def cover(self, cover_set):
        '''Perform sa cover operation on the table
        for all pairs in the cover_set.
        '''
        for pair in cover_set:
            self.cover_card(pair[0], pair[1])
    def convert_to_cards(self):
        '''Returns all cards on the table
        in one cards.Cards object.
        '''
        list_of_cards = cards.Cards()
        for x in self:
            if isinstance(x, cards.Card):
                list_of_cards.append(x)
            else:
                list_of_cards.extend(x)
        return list_of_cards
    def possible_to_throw_on(self, card):
        '''Returns True if it is possible to throw on card
        on the table.
        '''
        if not self.is_empty():
            value = card.get_value()
            for on_table in self.convert_to_cards():
                if on_table.get_value() == value:
                    return True
        return False
    def possible_to_put_cards(self, to_put):
        '''Returns True if to_put is possible to put on the table.
        '''
        for i in range(len(to_put) - 1):
            if to_put[i].get_value() != to_put[i + 1].get_value():
                return False
        return True
    def get_number_of_uncovered_cards(self):
        '''Returns number of uncovered cards on the table.
        '''
        num = 0
        for x in self:
            if isinstance(x, cards.Card):
                num = num + 1
        return num
    def get_number_of_items(self):
        '''Returns number of cover pairs and not covered cards.
        '''
        return len(self)
    def get_number_of_cards(self):
        '''Returns number of cards on the table.
        '''
        number = 0
        for elem in self:
            if isinstance(elem, cards.Card):
                number += 1
            else:
                number += 2
        return number
    def has_card(self, card):
        '''Returns True if the table has card.
        Returns False otherwise.
        '''
        for x in self:
            if isinstance(x, list):
                if x[0] == card or x[1] == card:
                    return True
            else:
                if x == card:
                    return True
        return False
    def has_as_covered(self, card):
        '''Return True if the table has card as covered.
        Returns False otherwise.
        '''
        for x in self:
            if isinstance(x, list):
                if x[0] == card:
                    return True                
        return False
    def has_as_covering(self, card):
        '''Return True if the table has card as covering.
        Returns False otherwise.
        '''
        for x in self:
            if isinstance(x, list):
                if x[1] == card:
                    return True                
        return False
    def has_as_not_covered(self, card):
        '''Return True if the table has card as not covered.
        Returns False otherwise.
        '''
        for x in self:
            if isinstance(x, cards.Card):
                if x == card:
                    return True
        return False
    def is_empty(self):
        '''Returns True if the table is empty.
        Returns False otherwise.
        '''
        return self.get_number_of_items() == 0
    def __repr__(self):
        '''Representation of the object.
        '''
        return self.__str__()