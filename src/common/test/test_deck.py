import tester
import inspect
import deck
import cards


class Test(tester.Test):
    def __init__(self):
        self.testing_module = deck
        a = []
        for s in cards.SUITS:
            for v in cards.VALUES:
                a.append(cards.Card(s + v))
        self.class_names = ['Deck']
        d = deck.Deck()
        self.test_Deck = [
                         [d, 'is_empty', [], False],
                         [d, 'show_trump_card', [], 'cA'],
                         [d, 'take_cards', [3], [cards.Card('h6'), cards.Card('h7'), cards.Card('h8')]],
                         [d, 'get_number_of_cards', [], 33],
                         [d, 'take_cards', [30], a[3:33]],
                         [d, 'take_cards', [4], [cards.Card('cQ'), cards.Card('cK'), cards.Card('cA')]],
                         [d, 'get_number_of_cards', [], 0],
                         [d, 'take_cards', [1], []],
                         [d, 'is_empty', [], True]
                         ]

Test().run_tests()