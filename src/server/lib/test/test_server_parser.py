import tester
'''Testing module
Tests classes: server_parser.Server_Parser, Command.
It makes me believe... It should work...
'''

import server_parser
import tester

class Test(tester.Test):
    def __init__(self):
        self.testing_module = server_parser
        p = server_parser.Server_Parser()
        self.test_Server_Parser = [
# I Basic tests.
[p, 'parse_command', ['''command=restart&test=true'''],
'''The client command object=
_command = 
restart
_test = 
True'''
],
[p, 'parse_command', ['''command=register&name=Victor'''],
'''The client command object=
_command = 
register
_name = 
Victor'''
],
[p, 'parse_command', ['''command=createGame&uid=7&gameName=GreatBoom&numberOfPlayers=3&retransfer=true&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7
_number_of_players = \n3\n_game_name = \nGreatBoom\n_first_attack_5cards = 
True\n_attack_6cards = \nTrue\n_retransfer = \nTrue''',
],
[p, 'parse_command', ['''command=joinGame&uid=666&gameName=Kolbasa'''],
'''The client command object=\n_command = \njoinGame\n_uid = \n666\n_game_name = \nKolbasa'''
],
[p, 'parse_command', ['''command=getListOfGames'''],
'''The client command object=\n_command = \ngetListOfGames'''
],
[p, 'parse_command', ['''command=getGameStatus&uid=777'''],
'''The client command object=\n_command = \ngetGameStatus\n_uid = \n777'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards=[h6][s6]'''],
'''The client command object=\n_command = \nattack\n_uid = \n555\n_cards = \n[h6, s6]'''
],
[p, 'parse_command', ['''command=cover&uid=565&cards=[h6'Killer'<h7][s6<s7]'''],
'''The client command object=\n_command = \ncover\n_uid = \n565\n_cards = \n[h6'Killer'<h7][s6<s7]'''
],
[p, 'parse_command', ['''command=take&uid=755'''],
'''The client command object=\n_command = \ntake\n_uid = \n755'''
],
[p, 'parse_command', ['''command=retransfer&uid=645&cards=[h6][s6]'''],
'''The client command object=\n_command = \nretransfer\n_uid = \n645\n_cards = \n[h6, s6]'''
],
[p, 'parse_command', ['''command=quit&uid=545'''],
'''The client command object=\n_command = \nquit\n_uid = \n545'''
],
[p, 'parse_command', ['''command=skip&uid=654'''],
'''The client command object=\n_command = \nskip\n_uid = \n654'''
],
[p, 'parse_command', ['''command=restart&test=true'''],
'''The client command object=\n_command = \nrestart\n_test = \nTrue'''
],

# II Tests on fields, fields' order
#Added fields do not influence the result if they have bad, but not VERY bad syntax,
#because such fields are not even parsed (2 test type).
#But because they are in the inside of the string and if they contain smth like '='
#they will corrupt everything for sure.
#Adding some correct fields.
[p, 'parse_command', ['''command=register&name=Victor&uid=78&retransfer=true'''],
'''The client command object=\n_command = \nregister\n_name = \nVictor'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards=[h6][s6]&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \nattack\n_uid = \n555\n_cards = \n[h6, s6]'''
],
#Adding incorrect fields (not too much incorrect).
[p, 'parse_command', ['''command=cover&uid=565&name=wowo,forbidden symbols$#%^!!!^)&cards=[h6'Killer'<h7][s6<s7]'''],
'''The client command object=\n_command = \ncover\n_uid = \n565\n_cards = \n[h6'Killer'<h7][s6<s7]'''
],
[p, 'parse_command', ['''command=skip&uid=654&cards=[VISA VIRTUAL][MASTER CARD]'''],
'''The client command object=\n_command = \nskip\n_uid = \n654'''
],
#Adding incorrect fields (very-very incorect, with many '=' delimiters).
[p, 'parse_command', ['''command=createGame&uid=7&name=G=R=E=A=T=B=o=om&numberOfPlayers=3&retransfer=true&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7\n_error = 
Error type= More than one inner delimiter =
Details= ['name', 'G', 'R', 'E', 'A', 'T', 'B', 'o', 'om']'''
],
[p, 'parse_command', ['''command=skip&uid=6=54'''],
'''The client command object=\n_command = \nskip\n_error = 
Error type= More than one inner delimiter =\nDetails= ['uid', '6', '54']'''
],
#Removed fields influence significantly= an exception is raised ('unfilled fields').
#Removing fields (non command).
[p, 'parse_command', ['''command=retransfer&cards=[h6][s6]'''],
'''The client command object=\n_command = \nretransfer\n_cards = \n[h6, s6]\n_error = 
Error type= Not all required for the command fields are filled\nDetails= ['uid']'''
],
[p, 'parse_command', ['''command=createGame&uid=7&name=GreatBoom&retransfer=true&firstAttack5Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7
_first_attack_5cards = \nTrue\n_retransfer = \nTrue\n_error = 
Error type= Not all required for the command fields are filled
Details= ['gameName', 'numberOfPlayers', 'attack6Cards']''',
],
[p, 'parse_command', ['''command=register'''],
'''The client command object=\n_command = \nregister\n_error = 
Error type= Not all required for the command fields are filled\nDetails= ['name']'''
],
#Removing fields (command).
[p, 'parse_command', ['''name=Victor'''],
'''The client command object=\n_error = 
Error type= Illegal command syntax: command field goes first\nDetails= No info'''
],
#Moving a field to another place does not influence if the field is not command.
#If it is, the exception is raised (we need to know type of message at first)
#Moving a field (not command).
[p, 'parse_command', ['''command=attack&cards=[h6][s6]&uid=555'''],
'''The client command object=\n_command = \nattack\n_uid = \n555\n_cards = \n[h6, s6]'''
],
[p, 'parse_command', ['''command=cover&cards=[h6'Killer'<h7][s6<s7]&uid=565'''],
'''The client command object=\n_command = \ncover\n_uid = \n565\n_cards = \n[h6'Killer'<h7][s6<s7]'''
],
#Moving a command field.
[p, 'parse_command', ['''uid=7&name=GreatBoom&numberOfPlayers=3
retransfer=true\ncommand=createGame\nfirstAttack5Cards=true\nattack6Cards=true'''],
'''The client command object=\n_error = 
Error type= Illegal command syntax: command field goes first\nDetails= No info''',
],
[p, 'parse_command', ['''uid=565&command=cover&cards=[h6'Killer'<h7][s6<s7]'''],
'''The client command object=\n_error = 
Error type= Illegal command syntax: command field goes first\nDetails= No info'''
],
#It is not forbidden to redefine fields. But not a command field - an exeption will raise.
[p, 'parse_command', ['''command=getListOfGames&command=joinGame'''],
'''The client command object=\n_command = \ngetListOfGames\n_error = 
Error type= Command must be set once\nDetails= No info'''
],
[p, 'parse_command', ['''command=getGameStatus&uid=777&command=joinGame'''],
'''The client command object=\n_command = \ngetGameStatus\n_uid = \n777\n_error = 
Error type= Command must be set once\nDetails= No info'''
],

# III Tests to raise all exceptions
[p, 'parse_command', ['''command=joinGame&uid=666&GOGO=(Kolbasa)'''],
'''The client command object=\n_command = \njoinGame\n_uid = \n666\n_error = 
Error type= Unknown field name\nDetails= GOGO'''
],
[p, 'parse_command', ['''command=DROP_TABLE_WORLD'''],
'''The client command object=\n_error = \nError type= Unknown command\nDetails= DROP_TABLE_WORLD'''
],
[p, 'parse_command', ['''command=register&name=Victor'''],
'''The client command object=\n_command = \nregister\n_name = \nVictor'''
],
[p, 'parse_command', ['''command=joinGame&uid=666&gameName=Kol3$%^asa'''],
'''The client command object=\n_command = \njoinGame\n_uid = \n666\n_error = 
Error type= Illegal identificator\nDetails= Kol3$%^asa'''
],
[p, 'parse_command', ['''command=createGame&uid=7&gameName=GreatBoom&numberOfPlayers=3&retransfer=true&firstAttack5Cards=YO&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7
_number_of_players = \n3\n_game_name = \nGreatBoom\n_retransfer = \nTrue\n_error = 
Error type= Non boolean value\nDetails= YO''',
],
[p, 'parse_command', ['''command=getGameStatus&uid=7f7'''],
'''The client command object=\n_command = \ngetGameStatus\n_uid = \n7f7'''
],
[p, 'parse_command', ['''command=cover&uid=565&cards=[h6'Killer'>h7][s6<s7]'''],
'''The client command object=\n_command = \ncover\n_uid = \n565\n_error = 
Error type= Wrong covering set syntax\nDetails= [h6'Killer'>h7][s6<s7]'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards=[ho][s6]'''],
'''The client command object=\n_command = \nattack\n_uid = \n555\n_error = 
Error type= Wrong attack or retransfer set syntax\nDetails= [ho][s6]'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards[h6][s6]'''],
'''The client command object=\n_command = \nattack\n_uid = \n555
_error = \nError type= Command can not be splitted on pairs\nDetails= cards[h6][s6]'''
],
[p, 'parse_command', ['''command=take'''],
'''The client command object=\n_command = \ntake\n_error = 
Error type= Not all required for the command fields are filled\nDetails= ['uid']'''
],
[p, 'parse_command', ['''command=retransfer&uid=645&cards=[h6]=[s6]'''],
'''The client command object=\n_command = \nretransfer
_uid = \n645\n_error = \nError type= More than one inner delimiter =
Details= ['cards', '[h6]', '[s6]']'''
],
[p, 'parse_command', ['''uid=645&command=retransfer&cards=[h6][s6]'''],
'''The client command object=\n_error = 
Error type= Illegal command syntax: command field goes first\nDetails= No info'''
],
[p, 'parse_command', ['''command=quit&uid=545&command=attack'''],
'''The client command object=\n_command = \nquit\n_uid = \n545\n_error = 
Error type= Command must be set once\nDetails= No info'''
],
# IV Corrupting data of different type fields (boolean, numeric etc.)
[p, 'parse_command', ['''command=&name=Victor'''],
'''The client command object=\n_error = \nError type= Unknown command\nDetails= '''
],
[p, 'parse_command', ['''command=joinGame&uid=666&gameName='''],
'''The client command object=\n_command = \njoinGame\n_uid = \n666\n_error = 
Error type= Identificator is missed\nDetails= '''
],
[p, 'parse_command', ['''command=GURGUR&uid=7&name=GreatBoom&numberOfPlayers=3
retransfer=true\nfirstAttack5Cards=true\nattack6Cards=true'''],
'''The client command object=\n_error = \nError type= Unknown command\nDetails= GURGUR''',
],
[p, 'parse_command', ['''command=joinGame&uid=-5&name=Kolbasa'''],
'''The client command object=\n_command = \njoinGame\n_error = \nError type= Illegal identificator\nDetails= -5'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards=[h6][[s6]'''],
'''The client command object=\n_command = \nattack\n_uid = \n555\n_error = 
Error type= Wrong attack or retransfer set syntax\nDetails= [h6][[s6]'''
],
[p, 'parse_command', ['''command=attack&uid=555&cards=[h][[s6]'''],
'''The client command object=\n_command = \nattack\n_uid = \n555
_error = 
Error type= Wrong attack or retransfer set syntax\nDetails= [h][[s6]'''
],
[p, 'parse_command', ['''command=cover&uid=565&cards=[h6'Killer'<h7s6<s7]'''],
'''The client command object=\n_command = \ncover\n_uid = \n565\n_error = 
Error type= Wrong covering set syntax\nDetails= [h6'Killer'<h7s6<s7]'''
],
[p, 'parse_command', ['''command=retransfer&uid=645&cards=[h6]=[s6]'''],
'''The client command object=\n_command = \nretransfer\n_uid = 
645\n_error = \nError type= More than one inner delimiter =
Details= ['cards', '[h6]', '[s6]']'''
],
[p, 'parse_command', ['''command=createGame&uid=7&gameName=GreatBoom&numberOfPlayers=3&retransfer=1&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7
_number_of_players = \n3\n_game_name = \nGreatBoom\n_error = 
Error type= Non boolean value\nDetails= 1''',
],
[p, 'parse_command', ['''command=createGame&uid=7&gameName=GreatBoom&numberOfPlayers=3&retransfer=true&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = 
7\n_number_of_players = \n3\n_game_name = \nGreatBoom\n_first_attack_5cards = 
True\n_attack_6cards = \nTrue\n_retransfer = \nTrue''',
],
[p, 'parse_command', ['''command=createGame&uid=7&gameName=GreatBoom&numberOfPlayers=3&retransfer=true&firstAttack5Cards=true&attack6Cards=true'''],
'''The client command object=\n_command = \ncreateGame\n_uid = \n7
_number_of_players = \n3\n_game_name = \nGreatBoom\n_first_attack_5cards = 
True\n_attack_6cards = \nTrue\n_retransfer = \nTrue''',
],
[p, 'parse_command', ['''command=register&name=Victor'''],
'''The client command object=\n_command = \nregister\n_name = \nVictor'''
],
]
        self.class_names = ['Server_Parser']



test = Test()
test.run_tests()