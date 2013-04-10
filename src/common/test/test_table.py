import tester
import table
import inspect
import cards


class Test(tester.Test):
    def __init__(self):
        self.testing_module = table
        self.class_names = ['Table']
        t = table.Table()
        self.test_Table = [
                          [t, 'is_empty', [0], True],
                          [t, 'put_on_card', [cards.Card('hJ')], None],
                          [t, 'put_on_card', [cards.Card('sJ')], None],
                          [t, 'has_as_covered', [cards.Card('cJ')], False],
                          [t, 'has_as_not_covered', [cards.Card('cJ')], False],
                          [t, 'has_as_not_covered', [cards.Card('sJ')], True],
                          [t, 'has_card', [cards.Card('sJ')], True],
                          [t, 'has_card', [cards.Card('sA')], False],
                          [t, 'has_as_covering', [cards.Card('dQ')], False],
                          [t, 'is_empty', [0], False],
                          [t, 'get_number_of_items', [], 2],
                          [t, 'get_number_of_cards', [], 2],
                          [t, 'put_on_card', [cards.Card('sQ')], None],
                          [t, 'has_as_not_covered', [cards.Card('sQ')], True],
                          [t, 'cover_card', [cards.Card('sQ'), cards.Card('sA')], True],
                          [t, 'has_as_not_covered', [cards.Card('sQ')], False],
                          [t, 'has_as_covering', [cards.Card('sA')], True],
                          [t, 'has_as_covered', [cards.Card('sQ')], True],
                          [t, 'has_as_covered', [cards.Card('sA')], False],
                          [t, 'has_as_covering', [cards.Card('c8')], False],
                          [t, 'has_card', [cards.Card('sA')], True],
                          [t, 'cover_card', [cards.Card('sQ'), cards.Card('sK')], False],
                          [t, 'cover_card', [cards.Card('s6'), cards.Card('sK')], False],
                          [t, 'get_number_of_items', [], 3],
                          [t, 'get_number_of_cards', [], 4],
                          [t, 'take_all', [], [cards.Card('hJ'), cards.Card('sJ'), cards.Card('sQ'), cards.Card('sA')]],
                          [t, 'is_empty', [0], True],
                          [t, 'put_on_cards', [[cards.Card('s7'), cards.Card('cQ'), cards.Card('dA')]], None],
                          [t, 'get_number_of_cards', [], 3],
                          [t, 'get_number_of_items', [], 3],
                          [t, 'clear', [], None],
                          [t, 'is_empty', [0], True]
                          ]

Test().run_tests()