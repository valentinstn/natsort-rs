from natsort_rs import natsort
from unittest import TestCase


class NatSortTestCase(TestCase):
    def test_simple_natsorting(self):
        self.assertListEqual(
            natsort(["item 1", "item 10", "item 3"]), ["item 1", "item 3", "item 10"]
        )

    def test_case_unsensitive_natsorting(self):
        self.assertListEqual(
            natsort(["Item 1", "Item 3", "item 2"], ignore_case=True),
            ["Item 1", "item 2", "Item 3"],
        )

    def test_more_complex_object_natsorting(self):
        sorted_objs = natsort(
            [
                {"name": "item 1", "id": 1},
                {"name": "item 3", "id": 3},
                {"name": "item 2", "id": 2},
            ],
            key=lambda d: d["name"],
        )
        self.assertEqual(len(sorted_objs), 3)
        self.assertDictEqual(sorted_objs[0], {"name": "item 1", "id": 1})

        self.assertDictEqual(sorted_objs[1], {"name": "item 2", "id": 2})

        self.assertDictEqual(sorted_objs[2], {"name": "item 3", "id": 3})

    def test_with_numbers_attached_to_string(self):
        self.assertListEqual(
            natsort(
                [
                    "item 0",
                    "item 1b",
                    "Item 5",
                    "Item 50000",
                    "item 3b",
                    "item 3000b",
                    "item 2b",
                ],
                ignore_case=True,
            ),
            [
                "item 0",
                "item 1b",
                "item 2b",
                "item 3b",
                "Item 5",
                "item 3000b",
                "Item 50000",
            ],
        )

    def test_numbers_with_unit(self):
        self.assertListEqual(
            natsort(["Vol: 20L", "Vol: 1L", "Vol: 2L", "Vol: 10L"]),
            ["Vol: 1L", "Vol: 2L", "Vol: 10L", "Vol: 20L"],
        )

    def test_returned_indices(self):
        self.assertEqual(
            natsort(
                ["Vol: 20L", "Vol: 1L", "Vol: 2L", "Vol: 10L"], return_indices=True
            ),
            [1, 2, 3, 0],
        )

    def test_tuple_primary_key_sorting(self):
        """Tuples are sorted by their first element using natural order."""
        self.assertListEqual(
            natsort([("item 10", "a"), ("item 2", "b"), ("item 1", "c")]),
            [("item 1", "c"), ("item 2", "b"), ("item 10", "a")],
        )

    def test_tuple_secondary_key_sorting(self):
        """When the first key is equal, the second key breaks the tie naturally."""
        self.assertListEqual(
            natsort(
                [
                    ("section 1", "part 10"),
                    ("section 1", "part 2"),
                    ("section 1", "part 1"),
                ]
            ),
            [
                ("section 1", "part 1"),
                ("section 1", "part 2"),
                ("section 1", "part 10"),
            ],
        )

    def test_tuple_ignore_case(self):
        """ignore_case applies to every element within each tuple."""
        self.assertListEqual(
            natsort(
                [("B", "item 2"), ("a", "item 10"), ("a", "item 3")], ignore_case=True
            ),
            [("a", "item 3"), ("a", "item 10"), ("B", "item 2")],
        )

    def test_mixed_str_first_tuple_later(self):
        """Strings and tuples in the same list sort by their natural string key."""
        self.assertListEqual(
            natsort(["item 10", ("item 2", "b"), "item 1"]),
            ["item 1", ("item 2", "b"), "item 10"],
        )

    def test_mixed_tuple_first_str_later(self):
        """Tuple-first mixed list: tuples and bare strings sort together naturally."""
        self.assertListEqual(
            natsort([("item 10", "a"), "item 2", ("item 1", "c")]),
            [("item 1", "c"), "item 2", ("item 10", "a")],
        )

    def test_mixed_ignore_case(self):
        """ignore_case is applied correctly across a mixed str/tuple list."""
        self.assertListEqual(
            natsort(["Item 10", ("item 2", "b"), "item 1"], ignore_case=True),
            ["item 1", ("item 2", "b"), "Item 10"],
        )
