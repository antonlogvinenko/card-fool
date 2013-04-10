import tester
import players
import cards
import inspect
import deck
import sys



class Test(tester.Test):
    def __init__(self):
        reg_pl = players.Registered_Player('user', 'game')
        in_game = players.Player_In_Game(reg_pl, 3)
        reg_pls = players.Registered_Players()
        in_games = players.Players_In_Game()
        self.testing_module = players
        self.test_Player = [
                            [players.Player('Pl'), 'get_name', [], 'Pl'],
                            [players.Player(), 'get_name', [], '']
                            ]
        self.test_Registered_Player = [
                                       [reg_pl, 'get_playing_game', [], 'game'],
                                       [reg_pl, 'stops_playing', [], None],
                                       [reg_pl, 'starts_playing', ['new_game'], None],
                                       [reg_pl, 'get_playing_game', [], 'new_game'],
                                       ]
        self.test_Player_In_Game = [
                                    [in_game, 'get_order', [], 3],
                                    [in_game, 'get_status', [], ''],
                                    [in_game, 'make_attacker', [], None],
                                    [in_game, 'get_status', [], '_attacker_'],
                                    [in_game, 'make_defender', [], None],
                                    [in_game, 'get_status', [], '_defender_'],
                                    [in_game, 'make_fool', [], None],
                                    [in_game, 'get_status', [], '_fool_'],
                                    [in_game, 'make_winner', [], None],
                                    [in_game, 'get_status', [], '_winner_'],
                                    [in_game, 'has_card', [cards.Card('h0')], False],
                                    [in_game, 'give_card', [cards.Card('c8')], None],
                                    [in_game, 'has_card', [cards.Card('c8')], True],
                                    [in_game, 'get_cards', [], [cards.Card('c8')]],
                                    [in_game, 'give_card', [cards.Card('c7')], None],
                                    [in_game, 'give_card', [cards.Card('c6')], None],
                                    [in_game, 'give_cards', [[cards.Card('c9'), cards.Card('c0')]], None],
                                    [in_game, 'get_cards', [], [cards.Card('c8'),cards.Card('c7'),cards.Card('c6'),cards.Card('c9'),cards.Card('c0')]],
                                    [in_game, 'take_away_card', [cards.Card('c8')], None],
                                    [in_game, 'get_cards', [], [cards.Card('c7'),cards.Card('c6'),cards.Card('c9'),cards.Card('c0')]],
                                    [in_game, 'take_away_cards', [[cards.Card('c8'),cards.Card('c7')]], None],
                                    [in_game, 'get_cards', [], [cards.Card('c6'),cards.Card('c9'),cards.Card('c0')]],
                                    ]
        self.test_Registered_Players = [
                                        [reg_pls, 'new_player', [323, 'buba'], None],
                                        [reg_pls, 'new_player', [777, 'angel'], None],
                                        [reg_pls, 'name_exists', ['buba'], True],
                                        [reg_pls, 'name_exists', ['buba222'], False],
                                        ]
        self.test_Players_In_Game = [
                                     [in_games, 'new_player', [323, players.Registered_Player('buba')], None],
                                     [in_games, 'new_player', [777, players.Registered_Player('angel')], None],
                                     [in_games, 'get_number_of_players', [], 2],
                                     ]
        self.class_names = ['Player',
                            'Registered_Player',
                            'Player_In_Game',
                            'Registered_Players',
                            'Players_In_Game']
    
test = Test()
test.run_tests()

