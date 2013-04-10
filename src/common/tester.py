'''Contains Test class definition.
'''

import inspect

class Test:
    def __init__(self):
        self.testing_module = games
        self.test_Game = []
        self.test_Games = []
        self.class_names = []
    def run_tests(self):
        '''Run tests for each specified class.
        '''
        for name in self.class_names:
            self.test(name)
    def test(self, name):
        '''Run rests for class 'name'.
        '''
        class_ref = self.testing_module.__dict__[name]
        test_data = self.__dict__['test_' + name]
        failed = []
        for x in test_data:
            func = class_ref.__dict__[x[1]]
            args_num = len(inspect.getargspec(func)[0]) - 1
            if args_num == 0: f = func(x[0])
            elif args_num == 1: f = func(x[0], x[2][0])
            elif args_num == 2: f = func(x[0], x[2][0], x[2][1])
            elif args_num == 3: f = func(x[0], x[2][0], x[2][1], x[2][2])
            elif args_num == 4: f = func(x[0], x[2][0], x[2][1], x[2][2], x[2][3])
            elif args_num == 5: f = func(x[0], x[2][0], x[2][1], x[2][2], x[2][3], x[2][4])
            elif args_num == 6: f = func(x[0], x[2][0], x[2][1], x[2][2], x[2][3], x[2][4], x[2][5])
            elif args_num == 7: f = func(x[0], x[2][0], x[2][1], x[2][2], x[2][3], x[2][4], x[2][5], x[2][6])
            if str(f) != str(x[3]):
                failed.append([test_data.index(x), "expected: " + str(x[3]), 'got: ' + str(f)])
        result = '[' + str(self.testing_module.__name__) + '.' + name + ' testing]'
        if failed == []:
            result = 'OK  ' + result
        else:
            result = 'FAILED  ' + result
            result += '\n\tFailures: ' + str(len(failed)) + '/' + str(len(test_data))
        for x in failed:
            result += '\n\t' + str(x)
        print result