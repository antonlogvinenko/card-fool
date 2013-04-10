import tester
import games
import cards
import players
import inspect

class Test(tester.Test):
    def __init__(self):
        g = games.Game(5, True, False, True)
        g._trump_card = cards.Card('cA')
        gs = games.Games()
        gs2 = games.Games()
        p1 = players.Registered_Player('name', 'game')
        p2 = players.Registered_Player('name2', 'game2')
        p3 = players.Registered_Player('name3', 'game3')
        p4 = players.Registered_Player('name4', 'game4')
        p5 = players.Registered_Player('name5', 'game5')
        gs2['12'] = g
        gs2['13'] = g
        self.testing_module = games
        self.test_Game = [
                            [g, 'get_number_of_players', [], 5],
                            [g, 'get_trump', [], cards.Card('cA')],
                            [g, 'get_options', [], '{numberOfPlayers5}{attack6Cards}{canRetransfer}'],
                            [g, 'retransfer_allowed', [], True],
                            [g, 'first_5cards', [], False],
                            [g, 'attack_6cards', [], True],
                            [g, 'add_registered_player', [777, p1], True],
                            [g, 'add_registered_player', [666, p2], True],
                            [g, 'needs_players', [], True],
                            [g, 'add_registered_player', [555, p3], True],
                            [g, 'add_registered_player', [444, p4], True],
                            [g, 'add_registered_player', [333, p5], True],
                            [g, 'add_registered_player', [333, players.Registered_Player('name6', 'game6')], False],
                            [g, 'needs_players', [], False],
                            ]
        self.test_Games = [
                           [gs, 'new_game', ['name', 3, True, False, True, False, False], None],
                           [gs, 'new_game', ['name2', 4, False, True, True, False, False], None],
                           [gs2, 'get_game_objects', [], [g, g]],
                           [gs2, 'get_game_names', [], ['12', '13']]
                           ]
        self.class_names = ['Game',
                            'Games'
                            ]
    
test = Test()
test.run_tests()

