from __future__ import absolute_import, unicode_literals

import unittest

import quichem.parser


TEST_CASES = {
    "o": ('[Item[Coefficient[1], Compound[[Counter[Element[o], 1]]], '
          'Charge[0, ], State[]]]'),
    "pb": ('[Item[Coefficient[1], Compound[[Counter[Element[pb], 1]]], '
           'Charge[0, ], State[]]]'),
    "uuo": ('[Item[Coefficient[1], Compound[[Counter[Element[uuo], 1]]], '
            'Charge[0, ], State[]]]'),
    "o2": ('[Item[Coefficient[1], Compound[[Counter[Element[o], 2]]], '
           'Charge[0, ], State[]]]'),
    "c60": ('[Item[Coefficient[1], Compound[[Counter[Element[c], 60]]], '
            'Charge[0, ], State[]]]'),
    "h2o": ('[Item[Coefficient[1], Compound[[Counter[Element[h], 2], '
            'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "c6h12o6": ('[Item[Coefficient[1], Compound[[Counter[Element[c], 6], '
                'Counter[Element[h], 12], Counter[Element[o], 6]]], '
                'Charge[0, ], State[]]]'),
    "lioh": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 1], '
             'Counter[Element[o], 1], Counter[Element[h], 1]]], Charge[0, ], '
             'State[]]]'),
    "cmgali": ('[Item[Coefficient[1], Compound[[Counter[Element[cm], 1], '
               'Counter[Element[ga], 1], Counter[Element[li], 1]]], '
               'Charge[0, ], State[]]]'),
    "c.mgali": ('[Item[Coefficient[1], Compound[[Counter[Element[c], 1], '
                'Counter[Element[mg], 1], Counter[Element[al], 1], '
                'Counter[Element[i], 1]]], Charge[0, ], State[]]]'),
    "ge'oh'4": ('[Item[Coefficient[1], Compound[[Counter[Element[ge], 1], '
                'Counter[Group[[Counter[Element[o], 1], '
                'Counter[Element[h], 1]]], 4]]], Charge[0, ], State[]]]'),
    "b'nh4'3'p.o4'2": (
        '[Item[Coefficient[1], Compound[[Counter[Element[b], 1], '
        'Counter[Group[[Counter[Element[n], 1], Counter[Element[h], 4]]], 3], '
        'Counter[Group[[Counter[Element[p], 1], '
        'Counter[Element[o], 4]]], 2]]], Charge[0, ], State[]]]'),
    "h=": ('[Item[Coefficient[1], Compound[[Counter[Element[h], 1]]], '
           'Charge[1, =], State[]]]'),
    "br-": ('[Item[Coefficient[1], Compound[[Counter[Element[br], 1]]], '
            'Charge[1, -], State[]]]'),
    "o2=": ('[Item[Coefficient[1], Compound[[Counter[Element[o], 2]]], '
            'Charge[1, =], State[]]]'),
    "o2.=": ('[Item[Coefficient[1], Compound[[Counter[Element[o], 2]]], '
             'Charge[1, =], State[]]]'),
    "o.2=": ('[Item[Coefficient[1], Compound[[Counter[Element[o], 1]]], '
             'Charge[2, =], State[]]]'),
    "so4.2=": ('[Item[Coefficient[1], Compound[[Counter[Element[s], 1], '
               'Counter[Element[o], 4]]], Charge[2, =], State[]]]'),
    "h2g": ('[Item[Coefficient[1], Compound[[Counter[Element[h], 2]]], '
            'Charge[0, ], State[g]]]'),
    "hp.o4aq": ('[Item[Coefficient[1], Compound[[Counter[Element[h], 1], '
                'Counter[Element[p], 1], Counter[Element[o], 4]]], '
                'Charge[0, ], State[aq]]]'),
    "heg": ('[Item[Coefficient[1], Compound[[Counter[Element[he], 1]]], '
            'Charge[0, ], State[]]]'),
    "he;g": ('[Item[Coefficient[1], Compound[[Counter[Element[he], 1]]], '
             'Charge[0, ], State[g]]]'),
    "li2s": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 2], '
             'Counter[Element[s], 1]]], Charge[0, ], State[]]]'),
    "li2;s": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 2]]], '
              'Charge[0, ], State[s]]]'),
    "li=s": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 1]]], '
             'Charge[1, =], State[s]]]'),
    "li=;s": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 1]]], '
              'Charge[1, =], State[s]]]'),
    "li;=s": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 1]]], '
              'Charge[0, ], State[]], Separator[=], Item[Coefficient[1], '
              'Compound[[Counter[Element[s], 1]]], Charge[0, ], State[]]]'),
    "2h2o": ('[Item[Coefficient[2], Compound[[Counter[Element[h], 2], '
             'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "10he": ('[Item[Coefficient[10], Compound[[Counter[Element[he], 1]]], '
             'Charge[0, ], State[]]]'),
    "cocl2/6h2o": ('[Item[Coefficient[1], Compound[[Counter[Element[co], 1], '
                   'Counter[Element[cl], 2]]], Charge[0, ], State[]], '
                   'Separator[/], Item[Coefficient[6], '
                   'Compound[[Counter[Element[h], 2], '
                   'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "li3=/6h2o": ('[Item[Coefficient[1], Compound[[Counter[Element[li], 3]]], '
                  'Charge[1, =], State[]], Separator[/], Item[Coefficient[6], '
                  'Compound[[Counter[Element[h], 2], '
                  'Counter[Element[o], 1]]], Charge[0, ], State[]]]'),
    "mgo=h2o-mg'oh'2": (
        '[Item[Coefficient[1], Compound[[Counter[Element[mg], 1], '
        'Counter[Element[o], 1]]], Charge[0, ], State[]], Separator[=], '
        'Item[Coefficient[1], Compound[[Counter[Element[h], 2], '
        'Counter[Element[o], 1]]], Charge[0, ], State[]], Separator[-], '
        'Item[Coefficient[1], Compound[[Counter[Element[mg], 1], '
        'Counter[Group[[Counter[Element[o], 1], '
        'Counter[Element[h], 1]]], 2]]], Charge[0, ], State[]]]'),
    "2cl-aq=2ag=aq-2agcl;s": (
        '[Item[Coefficient[2], Compound[[Counter[Element[cl], 1]]], '
        'Charge[1, -], State[aq]], Separator[=], Item[Coefficient[2], '
        'Compound[[Counter[Element[ag], 1]]], Charge[1, =], State[aq]], '
        'Separator[-], Item[Coefficient[2], '
        'Compound[[Counter[Element[ag], 1], Counter[Element[cl], 1]]], '
        'Charge[0, ], State[s]]]'),
}


class TestStringList(unittest.TestCase):

    def setUp(self):
        self.parser = quichem.parser.parser_factory()

    def test_tokens(self):
        for case in TEST_CASES:
            self.assertEqual(TEST_CASES[case],
                             str(self.parser.parseString(case, parseAll=True)))
