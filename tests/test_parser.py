from __future__ import absolute_import, unicode_literals

import unittest

import pyparsing

import quichem.parser


TEST_CASES = {
    # Individual Elements
    "o": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[o], 1]]], '
          'Charge[0, ], State[]]]'),
    "pb": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[pb], 1]]], '
           'Charge[0, ], State[]]]'),
    "uuo": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[uuo], 1]]], '
            'Charge[0, ], State[]]]'),
    # Subscripts
    "o2": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[o], 2]]], '
           'Charge[0, ], State[]]]'),
    "c60": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[c], 60]]], '
            'Charge[0, ], State[]]]'),
    "h2o": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 2], '
            'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "c6h12o6": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[c], 6], '
                'Counter[Element[h], 12], Counter[Element[o], 6]]], '
                'Charge[0, ], State[]]]'),
    # Compounds
    "lioh": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 1], '
             'Counter[Element[o], 1], Counter[Element[h], 1]]], Charge[0, ], '
             'State[]]]'),
    "cmgali": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[cm], 1], '
               'Counter[Element[ga], 1], Counter[Element[li], 1]]], '
               'Charge[0, ], State[]]]'),
    "c.mgali": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[c], 1], '
                'Counter[Element[mg], 1], Counter[Element[al], 1], '
                'Counter[Element[i], 1]]], Charge[0, ], State[]]]'),
    # Parentheses
    "ge'oh'4": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[ge], 1], '
                'Counter[Group[[Counter[Element[o], 1], '
                'Counter[Element[h], 1]]], 4]]], Charge[0, ], State[]]]'),
    "b'nh4'3'p.o4'2": (
        '[Item[Coefficient[1, 1], Compound[[Counter[Element[b], 1], '
        'Counter[Group[[Counter[Element[n], 1], Counter[Element[h], 4]]], 3], '
        'Counter[Group[[Counter[Element[p], 1], '
        'Counter[Element[o], 4]]], 2]]], Charge[0, ], State[]]]'),
    "ge''nh4'2o'4": (
        '[Item[Coefficient[1, 1], Compound[[Counter[Element[ge], 1], '
        'Counter[Group[[Counter[Group[[Counter[Element[n], 1], '
        'Counter[Element[h], 4]]], 2], Counter[Element[o], 1]]], 4]]], '
        'Charge[0, ], State[]]]'),
    # Charges
    "h=": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 1]]], '
           'Charge[1, =], State[]]]'),
    "br-": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[br], 1]]], '
            'Charge[1, -], State[]]]'),
    "o2=": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[o], 2]]], '
            'Charge[1, =], State[]]]'),
    "o2.=": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[o], 2]]], '
             'Charge[1, =], State[]]]'),
    "o.2=": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[o], 1]]], '
             'Charge[2, =], State[]]]'),
    "so4.2=": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[s], 1], '
               'Counter[Element[o], 4]]], Charge[2, =], State[]]]'),
    # States
    "h2g": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 2]]], '
            'Charge[0, ], State[g]]]'),
    "hp.o4aq": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 1], '
                'Counter[Element[p], 1], Counter[Element[o], 4]]], '
                'Charge[0, ], State[aq]]]'),
    "he;g": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[he], 1]]], '
             'Charge[0, ], State[g]]]'),
    "heg": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[he], 1]]], '
            'Charge[0, ], State[g]]]'),
    "hg": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[hg], 1]]], '
           'Charge[0, ], State[]]]'),
    "li2s": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 2], '
             'Counter[Element[s], 1]]], Charge[0, ], State[]]]'),
    "li2;s": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 2]]], '
              'Charge[0, ], State[s]]]'),
    "li=s": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 1]]], '
             'Charge[1, =], State[s]]]'),
    "li=;s": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 1]]], '
              'Charge[1, =], State[s]]]'),
    "li;=s": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 1]]], '
              'Charge[0, ], State[]], Separator[=], Item[Coefficient[1, 1], '
              'Compound[[Counter[Element[s], 1]]], Charge[0, ], State[]]]'),
    "li=s2": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 1]]], '
              'Charge[0, ], State[]], Separator[=], Item[Coefficient[1, 1], '
              'Compound[[Counter[Element[s], 2]]], Charge[0, ], State[]]]'),
    "h=l": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 1]]], '
            'Charge[1, =], State[l]]]'),
    "h=li": ('[Item[Coefficient[1, 1], Compound[[Counter[Element[h], 1]]], '
             'Charge[0, ], State[]], Separator[=], Item[Coefficient[1, 1], '
             'Compound[[Counter[Element[li], 1]]], Charge[0, ], State[]]]'),
    # Coefficients
    "2h2o": ('[Item[Coefficient[2, 1], Compound[[Counter[Element[h], 2], '
             'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "10he": ('[Item[Coefficient[10, 1], Compound[[Counter[Element[he], 1]]], '
             'Charge[0, ], State[]]]'),
    "99/100o": ('[Item[Coefficient[99, 100], '
                'Compound[[Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "99.001o": ('[Item[Coefficient[99.001, 1], '
                'Compound[[Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    # Hydrates
    "cocl2/6h2o": (
        '[Item[Coefficient[1, 1], Compound[[Counter[Element[co], 1], '
        'Counter[Element[cl], 2]]], Charge[0, ], State[]], Separator[/], '
        'Item[Coefficient[6, 1], Compound[[Counter[Element[h], 2], '
        'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "li3=/6h2o": (
        '[Item[Coefficient[1, 1], Compound[[Counter[Element[li], 3]]], '
        'Charge[1, =], State[]], Separator[/], Item[Coefficient[6, 1], '
        'Compound[[Counter[Element[h], 2], Counter[Element[o], 1]]], '
        'Charge[0, ], State[]]]'),
    # Complex
    "mgo=h2o-mg'oh'2": (
        '[Item[Coefficient[1, 1], Compound[[Counter[Element[mg], 1], '
        'Counter[Element[o], 1]]], Charge[0, ], State[]], Separator[=], '
        'Item[Coefficient[1, 1], Compound[[Counter[Element[h], 2], '
        'Counter[Element[o], 1]]], Charge[0, ], State[]], Separator[-], '
        'Item[Coefficient[1, 1], Compound[[Counter[Element[mg], 1], '
        'Counter[Group[[Counter[Element[o], 1], '
        'Counter[Element[h], 1]]], 2]]], Charge[0, ], State[]]]'),
    "2cl-aq=2ag=aq-2agcl;s": (
        '[Item[Coefficient[2, 1], Compound[[Counter[Element[cl], 1]]], '
        'Charge[1, -], State[aq]], Separator[=], Item[Coefficient[2, 1], '
        'Compound[[Counter[Element[ag], 1]]], Charge[1, =], State[aq]], '
        'Separator[-], Item[Coefficient[2, 1], '
        'Compound[[Counter[Element[ag], 1], Counter[Element[cl], 1]]], '
        'Charge[0, ], State[s]]]'),
}

ERROR_CAUSING_TEST_CASES = {'x', 'naq'}


class TestStringList(unittest.TestCase):

    def setUp(self):
        self.parser = quichem.parser.parser_factory()

    def test_tokens(self):
        for case in TEST_CASES:
            self.assertEqual(TEST_CASES[case],
                             str(self.parser.parseString(case, parseAll=True)))

    def test_raises(self):
        for case in ERROR_CAUSING_TEST_CASES:
            with self.assertRaises(pyparsing.ParseException):
                self.parser.parseString(case, parseAll=True)


if __name__ == '__main__':
    unittest.main()
