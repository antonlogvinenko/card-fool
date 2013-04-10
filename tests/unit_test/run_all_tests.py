import sys

server_libs = "..\\..\\src\\server\\lib\\test\\"
server_tests = ['test_games',
                'test_players',
                'test_server_generator',
                'test_server_parser',
                'test_client_command'
                ]
server_tests.sort()

common_libs = "..\\..\\src\\common\\test\\"
common_tests = ['test_cards',
                'test_deck',
                'test_table',
                ] 

client_libs = "..\\..\\src\\client\\lib\\test\\"
client_tests = ['test_client_generator',
                'test_server_response',
                'test_client_parser',
		'test_ai',
                ]

print 'Common libraries:'
for test in common_tests:
    exec open(common_libs + test + '.py').read()

print 'Server libraries:'
for test in server_tests:
    exec open(server_libs + test + '.py').read()

print 'Client libraries:'
for test in client_tests:
    exec open(client_libs + test + '.py').read()
