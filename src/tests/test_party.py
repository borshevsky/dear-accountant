# encoding: utf-8

import unittest

from party import Party, _to_money, IncorrectMoney


class TestParty(unittest.TestCase):
    def test_payoff1(self):
        party = Party('party', ['@A', '@B', '@C'])
        party.waste('@A', 150)
        party.waste('@B', 150)
        expected = [('@C', '@A', 50), ('@C', '@B', 50)]

        self.assertEqual(party.payoff(), expected)

    def test_payoff2(self):
        party = Party('party', ['@A', '@B', '@C'])
        party.waste('@A', 100)
        party.waste('@B', 20)
        party.waste('@C', 30)
        expected = [('@B', '@A', 30), ('@C', '@A', 20)]

        self.assertEqual(party.payoff(), expected)

    def test_payoff3(self):
        party = Party('party', ['@A', '@B', '@C', '@D'])
        party.waste('@A', 2000)
        party.waste('@B', 1000)
        party.waste('@C', 1000)
        expected = [('@D', '@A', 1000.0)]

        self.assertEqual(party.payoff(), expected)

    def test_payoff4(self):
        party = Party('party', ['@A', '@B', '@C', '@D', '@E', '@F', '@G', '@H'])
        party.waste('@A', 11000)
        party.waste('@B', 11000)
        party.waste('@C', 1000)
        party.waste('@D', 1500)
        expected = [('@E', '@A', 3062.5), ('@F', '@A', 3062.5), ('@G', '@A', 1812.5),
                    ('@G', '@B', 1250.0), ('@H', '@B', 3062.5), ('@C', '@B', 2062.5),
                    ('@D', '@B', 1562.5)]

        self.assertEqual(party.payoff(), expected)

    def test_payoff5(self):
        party = Party('party', ['@A', '@B', '@C', '@D'])
        party.waste('@A', 1000)
        party.waste('@B', 500)
        party.waste('@C', 250)
        party.waste('@D', 100)
        expected = [('@D', '@A', 362.5), ('@C', '@A', 175.0), ('@C', '@B', 37.5)]
        self.assertEqual(party.payoff(), expected)

    def test_payoff_not_dividable(self):
        party = Party('party', ['@A', '@B', '@C'])
        party.waste('@A', 100)
        expected = [('@B', '@A', 33.3), ('@C', '@A', 33.3)]

        self.assertEqual(party.payoff(), expected)

    def test_members(self):
        party = Party('party', ['@A', '@B', '@C'])
        self.assertEqual(party.members_list(), ['@A', '@B', '@C'])

    def test_to_money(self):
        self.assertEqual(_to_money('100'), 100)
        self.assertEqual(_to_money('100.0'), 100)
        self.assertEqual(_to_money('1k'), 1000)
        self.assertEqual(_to_money('1.5к'), 1500)

        self.assertException(lambda: _to_money('1.5.5'), IncorrectMoney)
        self.assertException(lambda: _to_money('1k5'), IncorrectMoney)
        self.assertException(lambda: _to_money('1.5kk'), IncorrectMoney)
        self.assertException(lambda: _to_money('-1.5k'), IncorrectMoney)

    def assertException(self, f, exception_class):
        with self.assertRaises(exception_class):
            f()


if __name__ == '__main__':
    unittest.main()
