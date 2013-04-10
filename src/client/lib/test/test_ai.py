'''Tests for Players_Cards_Probabilities and Ai classes in ai.py
'''

import tester
import ai
import cards
import table
import requestor
import server_response

class Test(tester.Test):
    def __init__(self):
        self.testing_module = ai
        a = ai.Players_Cards_Probabilities(['Linda', 'John'], 'Linda', ['c6', 'c7', 'hK', 'hQ', 's9', 's8'], 'hA')
        self.class_names = ['Players_Cards_Probabilities', 'Ai']
        artint = ai.Ai(requestor.Requestor, 0)
        s1 = server_response.Server_Response()
        s2 = server_response.Server_Response()
        s1.set_trump_card(cards.Card('s7'))
        s2.set_trump_card(cards.Card('s7'))
        artint.prev_status = s1
        artint.new_status = s2
        c1 = cards.Cards()
        c1.add_card(cards.Card('c6'))
        c1.add_card(cards.Card('s6'))
        c2 = cards.Cards()
        c2.add_card(cards.Card('c7'))
        c2.add_card(cards.Card('s7'))
        t1 = table.Table()
        t1.put_on_cards([cards.Card('s7'), cards.Card('c9')])
        t1.cover_card(cards.Card('s7'), cards.Card('s0'))
        s1.set_table(t1)
        t2 = table.Table()
        t2.put_on_cards([cards.Card('s7'), cards.Card('c9')])
        t2.cover_card(cards.Card('s7'), cards.Card('s0'))
        t2.put_on_cards([cards.Card('c9'), cards.Card('d0')])
        s2.set_table(t2)
        artint._probs = a
        artint.prev_status = s1
        artint.new_status = s2
        self.test_Ai = [
                        [artint, 'generate_attack_set', [[cards.Card('c6'), cards.Card('h6'),  cards.Card('d6') , cards.Card('cQ'), cards.Card('sQ'), cards.Card('s6')], 3], '''[[c6], [h6], [d6], [cQ], [sQ], [s6], [h6, c6], [d6, c6], [s6, c6], [h6, d6], [h6, s6], [d6, s6], [sQ, cQ], [h6, d6, c6], [h6, s6, c6], [d6, s6, c6], [h6, d6, s6]]'''],
                        [artint, 'generate_covering_sets', [[cards.Card('c7'), cards.Card('cJ')], [cards.Card('c8'), cards.Card('c9'), cards.Card('cK')]], '''[[cJ<cK][c7<c8], [cJ<cK][c7<c9]]'''],
                        [artint, 'generate_throw_on_set', [[cards.Card('s7'), cards.Card('c7'), cards.Card('c9')], 3], '''[[s7], [c7], [c9], [s7, c7], [s7, c9], [c7, c9], [s7, c7, c9]]'''],
                        [artint, 'generate_throw_on_set', [[cards.Card('s7'), cards.Card('c7'), cards.Card('c9')], 2], '''[[s7], [c7], [c9], [s7, c7], [s7, c9], [c7, c9]]'''],
                        [artint, 'calc_average_value', [[cards.Card('c6'), cards.Card('s6')]], '''4.5'''],
                        [artint, 'calc_average_value', [[cards.Card('c6'), cards.Card('c7')]], '''0.5'''],
                        [artint, 'calc_average_value', [[cards.Card('c6'), cards.Card('c7')]], '''0.5'''],
                        [artint, 'calc_average_value', [[cards.Card('s7'), cards.Card('s6')]], '''9.5'''],
                        [artint, 'calc_average_value', [[cards.Card('sA'), cards.Card('cA'), cards.Card('cJ')]], '''10.0'''],
                        [artint, 'queue_attack_cards', [[c1, c2]], None],
                        [artint, 'get_str_queue', [], '''['command=attack&uid=0&cards=[c6][s6]', 'command=attack&uid=0&cards=[c7][s7]']'''],
                        [artint, 'clear_queue', [], None],
                        [artint, 'get_str_queue', [], '''[]'''],
                        [artint, 'queue_cover_cards', [[c2, c2], c1], None],
                        [artint, 'get_str_queue', [], '''['command=cover&uid=0&cards=[c7, s7]', 'command=cover&uid=0&cards=[c7, s7]']'''],
                        [artint, 'clear_queue', [], None],
                        [artint, 'queue_retransfer_cards', [c1], None],
                        [artint, 'get_str_queue', [], '''['command=retransfer&uid=0&cards=[c6][s6]']'''],
                        [artint, 'clear_queue', [], None],
                        [artint, 'queue_quit', [], None],
                        [artint, 'get_str_queue', [], '''['command=quit&uid=0']'''],
                        [artint, 'clear_queue', [], None],
                        [artint, 'queue_take', [], None],
                        [artint, 'get_str_queue', [], '''['command=take&uid=0']'''],
                        [artint, 'clear_queue', [], None],
                        [artint, 'queue_skip', [], None],
                        [artint, 'get_str_queue', [], '''['command=skip&uid=0']'''],
                        [artint, 'queue_throw_on_cards', [[c1, c2]], None],
                        [artint, 'get_str_queue', [], '''['command=skip&uid=0', 'command=attack&uid=0&cards=[c6][s6]', 'command=attack&uid=0&cards=[c7][s7]']'''],
                        [artint, 'set_options', [[True, True, False]], None],
                        [artint, 'attack6_restrict', [], True],
                        [artint, 'first_attack5_restrict', [], True],
                        [artint, 'retransfer_allowed', [], False],
                        [artint, 'get_thrown_on_cards', [], '''[c9, d0]'''],
                        [artint, 'same_covering_cards', [], True],
                        [artint, 'is_coverable', [cards.Card('c9'), cards.Card('c8')], False],
                        [artint, 'calc_throw_on_probability', [[cards.Card('c6')], 'John'], 1],
                        [artint, 'calc_retransfer_probability', [[cards.Card('sA'), cards.Card('cA')], 'John'], '''0.620689655172'''],
                        [artint, 'calc_cover_probability', [[cards.Card('c8'), cards.Card('c9')], 'John'], '''0.206896551724'''],
                        ]

        self.test_Players_Cards_Probabilities = []
      
Test().run_tests()