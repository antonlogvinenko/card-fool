'''Tests for Server_Response, Player_Info, Game_Info classes in server_response.py
'''

import tester
import server_response
import client_parser
import cards
import table

class Test(tester.Test):
    def __init__(self):
        self.testing_module = server_response
        self.class_names = ['Server_Response', 'Player_Info', 'Game_Info']
        s = server_response.Server_Response(True, 'good_response')
        cc = cards.Cards()
        cc.add_cards([cards.Card('c8'), cards.Card('h0')])
        p1 = server_response.Player_Info(1, 'Avel', '_attacker_', True)
        p2 = server_response.Player_Info(2, 'Brad', '_defendant_', False)
        t = table.Table()
        t.put_on_card(cards.Card('h7'))
        g = server_response.Game_Info('Just_game', ['P1', 'P2', 'P3'], 4, [True, False, True])

        self.test_Server_Response = [
                                     [s, 'get_status', [], True],
                                     [s, 'set_status', [False], None],
                                     [s, 'set_uid', [7], None],
                                     [s, 'get_uid', [], 7],
                                     [s, 'get_status', [], False],
                                     [s, 'get_message', [], 'good_response'],
                                     [s, 'set_message', ['better_response'], None],
                                     [s, 'get_message', [], 'better_response'],
                                     [s, 'set_game_name', ['good_game'], None],
                                     [s, 'get_game_name', [], 'good_game'],
                                     [s, 'set_options_list', [[False, False, False]], None],
                                     [s, 'get_game_options', [], [False, False, False]],
                                     [s, 'set_game_options', [True, False, True], None],
                                     [s, 'get_game_options', [], [True, False, True]],
                                     [s, 'retransfer_allowed', [], True],
                                     [s, 'first_attack5_restrict', [], False],
                                     [s, 'attack6_restrict', [], True],
                                     [s, 'set_trump_card', [cards.Card('h8')], None],
                                     [s, 'get_trump_card', [], cards.Card('h8')],
                                     [s, 'add_other_player_info', [p1], None],
                                     [s, 'add_other_player_info', [p1], None],
                                     [s, 'add_other_players_info', [[p1, p2]], None],
                                     [s, 'get_other_players_info', [], [p1, p1, p1, p2]],
                                     [s, 'set_my_info', [p2], None],
                                     [s, 'get_my_info', [], p2],
                                     [s, 'set_out', [cc], None],
                                     [s, 'get_out', [], cc],
                                     [s, 'set_table', [t], None],
                                     [s, 'get_table', [], t],
                                     [s, 'set_cards_in_deck', [3], None],
                                     [s, 'get_cards_in_deck', [], 3],
                                     ]
        self.test_Player_Info = [
                                 [p1, 'get_name', [], 'Avel'],
                                 [p1, 'get_status', [], '_attacker_'],
                                 [p1, 'get_order', [], 1],
                                 [p1, 'set_number_of_cards', [5], None],
                                 [p1, 'get_number_of_cards', [], 5],
                                 [p2, 'set_cards', [cc], None],
                                 [p2, 'get_cards', [], cc],
                                 [p1, 'is_active', [], True],
                                 [p2, 'is_active', [], False],
                                 [p2, 'make_active', [], None],
                                 [p2, 'is_active', [], True],
                                 ]
        self.test_Game_Info = [
                               [g, 'get_name', [], 'Just_game'],
                               [g, 'get_list_of_players', [], ['P1', 'P2', 'P3']],
                               [g, 'get_required_number', [], 4],
                               [g, 'get_options', [], [True, False, True]],
                               [g, 'retransfer_allowed', [], True],
                               [g, 'first_attack5_restrict', [], False],
                               [g, 'attack6_restrict', [], True],
                               ]

Test().run_tests()