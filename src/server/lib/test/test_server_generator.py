import tester
import players
import cards
import inspect
import deck
import sys
import games
import server_generator

class Test(tester.Test):
    def __init__(self):
        s = server_generator.Server_Generator()
        gs = games.Games()
        gs.new_game('game1', 5, True, False, False, True)
        gs.new_game('game2', 3, False, True, True, True)
        gs['game1'].add_registered_player('32', players.Registered_Player('Teddy'))
        gs['game1'].add_registered_player('33', players.Registered_Player('Yahel'))
        gs['game1'].add_registered_player('34', players.Registered_Player('Riva'))
        gs['game2'].add_registered_player('36', players.Registered_Player('Teddy'))
        gs['game2'].add_registered_player('37', players.Registered_Player('Yahel'))
        gs['game2'].add_registered_player('38', players.Registered_Player('Riva'))


        g = games.Game(4, True, False, True, True)
        g._out.add_card(cards.Card('h8'))
        g._table.put_on_card(cards.Card('h0'))
        p1 = players.Registered_Player('Teddy')
        p2 = players.Registered_Player('Yahel')
        p3 = players.Registered_Player('Riva')
        g.add_registered_player('123', p1)
        g.add_registered_player('33', p2)
        g.add_registered_player('34', p3)
        x = g.get_players_hash()
        x['123'].give_card(cards.Card('h8'))
        x['123'].give_card(cards.Card('h7'))
        x['123'].make_defender()
        x['33'].make_defender()
        x['34'].make_attacker()
        self.testing_module = server_generator
        self.test_Server_Generator = [
                                      [s, 'skip_response', ['OK', 'No message'], 'status:ok\nmessage:No message'],
                                      [s, 'quit_response', ['OK', 'Missed game'], 'status:ok\nmessage:Missed game'],
                                      [s, 'retransfer_response', ['OK', 'Bla'], 'status:ok\nmessage:Bla'],
                                      [s, 'take_response', ['OK', 'Bla2'], 'status:ok\nmessage:Bla2'],
                                      [s, 'cover_response', ['OK', 'Bla3'], 'status:ok\nmessage:Bla3'],
                                      [s, 'attack_response', ['OK', 'Bla4'], 'status:ok\nmessage:Bla4'],
                                      [s, 'join_game_response', ['OK', 'Bla5'], 'status:ok\nmessage:Bla5'],
                                      [s, 'create_game_response', ['OK', 'Bla6'], 'status:ok\nmessage:Bla6'],
                                      [s, 'register_response', ['OK', 'Bla7', '738'], 'status:ok\nmessage:Bla7\nuid:738'],
                                      [s, 'list_of_games_response', [gs],
                                       '''game:"game1"(Riva)(Teddy)(Yahel){numberOfPlayers5}{attack6Cards}\ngame:"game2"(Riva)(Teddy)(Yahel){numberOfPlayers3}{firstAttack5Cards}{canRetransfer}'''],
                                      [s, 'get_game_status_response', ['ok', 'mes', 'game', g, '123'],
                                       '''status:ok\nmessage:mes\ngame:game\ntable:[h0]\ndeck:[36]\ntrump:[cA]\nout:[h8]\noptions:{numberOfPlayers4}{attack6Cards}{canRetransfer}\nplayer:1(Teddy)_defender_[h8][h7]\nplayer:2(Yahel)_defender_[0]\nplayer:3(Riva)_attacker_[0]\nactive:1'''
                                       ]
                                      ]
        self.class_names = ['Server_Generator']

tester = Test()
tester.run_tests()