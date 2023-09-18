from natsort_rs import natsort 
from unittest import TestCase


class NatSortTestCase(TestCase):

    def test_simple_natsorting(self):
        self.assertListEqual(
            natsort(['item 1', 'item 10', 'item 3']),
            ['item 1', 'item 3', 'item 10']
        )

    def test_case_unsensitive_natsorting(self):
        self.assertListEqual(
            natsort(['Item 1', 'Item 3', 'item 2'], ignore_case=True),
            ['Item 1', 'item 2', 'Item 3']
        )

    def test_more_complex_object_natsorting(self):
        sorted_objs = natsort(
            [
                {'name': 'item 1', 'id': 1},
                {'name': 'item 3', 'id': 3},
                {'name': 'item 2', 'id': 2}
            ],
            key=lambda d: d['name']
        )
        self.assertEqual(len(sorted_objs), 3)
        self.assertDictEqual(
            sorted_objs[0], 
            {'name': 'item 1', 'id': 1}
        )

        self.assertDictEqual(
            sorted_objs[1], 
            {'name': 'item 2', 'id': 2}
        )

        self.assertDictEqual(
            sorted_objs[2], 
            {'name': 'item 3', 'id': 3}
        )
    
    def test_with_numbers_attached_to_string(self):
        self.assertListEqual(
            natsort(
                ['item 0', 'item 1b', 'Item 5', 'Item 50000', 
                 'item 3b', 'item 3000b', 'item 2b'], 
                ignore_case=True
            ),
            ['item 0', 'item 1b', 'item 2b', 'item 3b', 
             'Item 5', 'item 3000b', 'Item 50000']
        )
