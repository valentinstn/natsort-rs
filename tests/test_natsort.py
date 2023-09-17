from natsort_rs import natsort 
from unittest import TestCase


class NatSortTestCase(TestCase):

    def test_simple_natsorting(self):
        self.assertListEqual(
            natsort(['item 1', 'item 10', 'item 3']),
            ['item 1', 'item 3', 'item 10']
        )