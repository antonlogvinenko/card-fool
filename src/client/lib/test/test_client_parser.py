'''Tests for Client_Parser class in client_parser.py
'''

import tester
import server_response
import client_parser
import cards
import table

class Test(tester.Test):
    def __init__(self):
        self.testing_module = client_parser
        self.class_names = ['Client_Parser']
        p = client_parser.Client_Parser()
        self.test_Client_Parser = [

[p, 'parse_response',
['''game:"MyGame"(Viktor)(Fedor){numberOfPlayers2}{attack6Cards}{firstAttack5Cards}{canRetransfer}
game:"AnotherGame"(Viktor){numberOfPlayers2}{canRetransfer}
game:"AnotherGame"(Tricky1)(Tricky2){numberOfPlayers5}{attack6Cards}{firstAttack5Cards}'''],
'''status:True
message:
uid:0
game_name:
game_options:[]
trump_card:None
out:None
table:None
cards_in_deck:0
games_list:[
Game_info
name:MyGame
players:['Viktor', 'Fedor']
required numbers:2
options:[True, True, True], 
Game_info
name:AnotherGame
players:['Viktor']
required numbers:2
options:[False, False, True], 
Game_info
name:AnotherGame
players:['Tricky1', 'Tricky2']
required numbers:5
options:[True, True, False]]
other_players_info:[]
me:None
error:None'''
],

[p, 'parse_response',
['''status:ok
message:message22
game:BUZZZ
table:[h6<h7][sA]
deck:[12]
trump:[s6]
out:[d7][c8]
options:{attack6Cards}{firstAttack5Cards}{canRetransfer}
player:1(Fedor)_defendant_[7]
player:2(Cool)_attacker_[h6][s0]
player:3(Tricky)_attacker_[5]
active:2'''],
'''status:True
message:message22
uid:0
game_name:BUZZZ
game_options:[True, True, True]
trump_card:s6
out:[d7, c8]
table:[h6<h7][sA]
cards_in_deck:12
games_list:[]
other_players_info:[
Player_info
name:Fedor
order:1
status:_defendant_
active:False
number of cards:7
cards:[], 
Player_info
name:Tricky
order:3
status:_attacker_
active:False
number of cards:5
cards:[]]
me:
Player_info
name:Cool
order:2
status:_attacker_
active:True
number of cards:0
cards:[h6, s0]
error:None''']
]



Test().run_tests()