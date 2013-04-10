'''Tests for Client_Generator class in client_generator.py
'''

import tester
import client_generator
import cards
import table


class Test(tester.Test):
    def __init__(self):
        self.testing_module = client_generator
        self.class_names = ['Client_Generator']
        g = client_generator.Client_Generator()
        cc = cards.Cards()
        t = table.Table()
        t.put_on_card(cards.Card('c7'))
        t.put_on_card(cards.Card('c9'))
        t.cover_card(cards.Card('c7'), cards.Card('c8'))
        t.cover_card(cards.Card('c9'), cards.Card('c0'))
        cc.add_cards([cards.Card('c8\'Owner\''), cards.Card('c7')])
        t2 = table.Table()
        t2.put_on_card(cards.Card('c7'))
        t2.put_on_card(cards.Card('c9'))
        self.test_Client_Generator = [
                                      [g, 'register', ['Ford'], 'command=register&name=Ford'],
                                      [g, 'create_game', [34, 'Life', 4, True, False, True],
                                       'command=createGame&uid=34&gameName=Life&numberOfPlayers=4&retransfer=true&firstAttack5Cards=false&attack6Cards=true'],
                                      [g, 'create_game', ['37', 'Life', '8', False, True, False],
                                       'command=createGame&uid=37&gameName=Life&numberOfPlayers=8&retransfer=false&firstAttack5Cards=true&attack6Cards=false'],
                                      [g, 'join_game', ['78', 'TheName'], 'command=joinGame&uid=78&gameName=TheName'],
                                      [g, 'get_games_list', [], 'command=getListOfGames'],
                                      [g, 'get_game_status', ['468456'], 'command=getGameStatus&uid=468456'],
                                      [g, 'attack', ['123', cc], '''command=attack&uid=123&cards=[c8'Owner'][c7]'''],
                                      [g, 'cover', ['sdf', t], 'command=cover&uid=sdf&cards=[c7<c8][c9<c0]'],
                                      [g, 'take', ['132'], 'command=take&uid=132'],
                                      [g, 'retransfer', ['456', cc], '''command=retransfer&uid=456&cards=[c8'Owner'][c7]'''],
                                      [g, 'quit', ['654'], 'command=quit&uid=654'],
                                      [g, 'skip', ['54'], 'command=skip&uid=54'],
                                      ]

Test().run_tests()