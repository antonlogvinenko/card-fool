import tester

import players
import cards
import inspect
import deck
import sys
import games
import server_parser
import server_generator
import table



class Test(tester.Test):
    def __init__(self):
        self.testing_module = cards
        a = cards.Card('h0')
        a.set_trump_suit('h')
        b = cards.Card("dK'The_Owner'")
        b.set_trump_suit('h')        
        c = cards.Card('cQ')
        c.set_trump_suit('h')        
        d = cards.Card('hQ')
        d.set_trump_suit('h')        
        cc = cards.Cards()
        cc.add_card(a)
        cc.add_card(b)
        cc.add_card(c)
        cc.add_card(d)
        self.class_names = ['Card', 'Cards']
        self.test_Card = [
                         [a, 'get_suit', [], 'h'],
                         [b, 'get_value', [], 'K'],
                         [b, 'get_owner', [], 'The_Owner'],
                         [c, 'owner_known', [], False],
                         [b,'owner_known', [], True],
                         [a, 'is_trump', [], True],
                         [b, 'is_trump', [], False],
                         [a, '__gt__', [b], True],
                         [a, '__gt__', [d], False],
                         [d, '__gt__', [c], True],
                         [a, '__lt__', [b], False],
                         [a, '__lt__', [d], True],
                         [d, '__lt__', [c], False],
                         [a, '__eq__', [b], False],
                         [b, '__eq__', [b], True],
                         [a, '__ne__', [b], True],
                         [b, '__ne__', [b], False],
                         [a, '__nonzero__', [], True],
                         [b, '__nonzero__', [], False],
                         ]
        self.test_Cards = [
                          [cc, 'has_card', [c], True],
                          [cc, 'has_card', [cards.Card('d8')], False],
                          [cc, 'add_cards', [[cards.Card('d6'), cards.Card('d7')]], None],
                          [cc, 'has_card', [cards.Card('d6')], True],
                          [cc, 'extract_card', [cards.Card('d6')], None],
                          [cc, 'has_card', [cards.Card('d6')], False],
                          [cc, 'extract_cards', [[cards.Card('d8'), cards.Card('d7')]], None],
                          [cc, 'has_card', [cards.Card('d7')], False],
                          [cc, 'has_card', [cards.Card('d8')], False],
                          [cc, 'get_least_trump', [cards.Card('hK')], 'h0'],
                          [cc, 'clear', [], None],
                          [cc, 'has_card', [c], False],
                          ]
Test().run_tests()