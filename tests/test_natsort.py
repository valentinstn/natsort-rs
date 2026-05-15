from natsort_rs import natsort
from unittest import TestCase
from typing import assert_type


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

    # ------------------------------------------------------------------
    # None handling
    # ------------------------------------------------------------------

    def test_none_last_by_default(self):
        """None values are placed after all non-None values by default."""
        self.assertListEqual(
            natsort(["item 3", None, "item 1", "item 2"]),
            ["item 1", "item 2", "item 3", None],
        )

    def test_none_first(self):
        """none_last=False places None values before all non-None values."""
        self.assertListEqual(
            natsort(["item 3", None, "item 1", "item 2"], none_last=False),
            [None, "item 1", "item 2", "item 3"],
        )

    def test_multiple_nones_last(self):
        """Multiple None values are all placed at the end, preserving stable order."""
        result = natsort(["item 2", None, "item 1", None])
        self.assertListEqual(result[:2], ["item 1", "item 2"])
        self.assertEqual(result[2], None)
        self.assertEqual(result[3], None)

    def test_multiple_nones_first(self):
        """Multiple None values are all placed at the start with none_last=False."""
        result = natsort(["item 2", None, "item 1", None], none_last=False)
        self.assertEqual(result[0], None)
        self.assertEqual(result[1], None)
        self.assertListEqual(result[2:], ["item 1", "item 2"])

    def test_all_nones(self):
        """A list of only None values is returned unchanged."""
        self.assertListEqual(natsort([None, None, None]), [None, None, None])

    def test_none_with_return_indices(self):
        """return_indices=True works correctly when None values are present."""
        # "item 1"->idx 2, "item 2"->idx 0, None->idx 1 (last)
        self.assertEqual(
            natsort(["item 2", None, "item 1"], return_indices=True),
            [2, 0, 1],
        )

    def test_none_with_ignore_case(self):
        """None values sort correctly alongside ignore_case=True."""
        self.assertListEqual(
            natsort(["Item 3", None, "item 1", "ITEM 2"], ignore_case=True),
            ["item 1", "ITEM 2", "Item 3", None],
        )

    def test_none_with_key(self):
        """key function may return None; those entries are sorted last."""
        data = [
            {"name": "item 3", "id": 3},
            {"name": None, "id": 99},
            {"name": "item 1", "id": 1},
        ]
        result = natsort(data, key=lambda d: d["name"])
        self.assertDictEqual(result[0], {"name": "item 1", "id": 1})
        self.assertDictEqual(result[1], {"name": "item 3", "id": 3})
        self.assertDictEqual(result[2], {"name": None, "id": 99})

    def test_none_with_tuple_rows(self):
        """None values sort last when mixed with tuple rows."""
        self.assertListEqual(
            natsort([("item 2", "b"), None, ("item 1", "a")]),
            [("item 1", "a"), ("item 2", "b"), None],
        )

    def test_none_first_with_tuple_rows(self):
        """none_last=False places None before tuple rows."""
        self.assertListEqual(
            natsort([("item 2", "b"), None, ("item 1", "a")], none_last=False),
            [None, ("item 1", "a"), ("item 2", "b")],
        )

    # ------------------------------------------------------------------
    # None inside tuples/lists
    # ------------------------------------------------------------------

    def test_none_inside_tuple_secondary_key(self):
        """None as a secondary key in a tuple sorts last by default."""
        self.assertListEqual(
            natsort(
                [("section 1", "part 2"), ("section 1", None), ("section 1", "part 1")]
            ),
            [("section 1", "part 1"), ("section 1", "part 2"), ("section 1", None)],
        )

    def test_none_inside_tuple_secondary_key_first(self):
        """None as a secondary key sorts first with none_last=False."""
        self.assertListEqual(
            natsort(
                [("section 1", "part 2"), ("section 1", None), ("section 1", "part 1")],
                none_last=False,
            ),
            [("section 1", None), ("section 1", "part 1"), ("section 1", "part 2")],
        )

    def test_none_inside_tuple_primary_key(self):
        """None as a primary key in a tuple sorts last by default."""
        self.assertListEqual(
            natsort([(None, "b"), ("item 2", "a"), ("item 1", "c")]),
            [("item 1", "c"), ("item 2", "a"), (None, "b")],
        )

    def test_none_inside_tuple_primary_key_first(self):
        """None as a primary key sorts first with none_last=False."""
        self.assertListEqual(
            natsort([(None, "b"), ("item 2", "a"), ("item 1", "c")], none_last=False),
            [(None, "b"), ("item 1", "c"), ("item 2", "a")],
        )

    def test_none_inside_tuple_mixed_with_toplevel_none(self):
        """None elements inside tuples and top-level None both respect none_last."""
        self.assertListEqual(
            natsort([("section 1", None), None, ("section 1", "part 1")]),
            [("section 1", "part 1"), ("section 1", None), None],
        )

    def test_none_inside_tuple_ignore_case(self):
        """ignore_case still works when tuple elements contain None."""
        self.assertListEqual(
            natsort(
                [("B", "item 2"), ("a", None), ("a", "item 1")],
                ignore_case=True,
            ),
            [("a", "item 1"), ("a", None), ("B", "item 2")],
        )

    # ------------------------------------------------------------------
    # Numeric handling (ints and floats)
    # ------------------------------------------------------------------

    def test_ints_in_flat_list(self):
        """Integers in a flat list are converted to strings for comparison."""
        self.assertListEqual(natsort([10, 2, 1]), [1, 2, 10])

    def test_floats_in_flat_list(self):
        """Floats in a flat list are converted to strings for comparison."""
        self.assertListEqual(natsort([1.0, 1.02, 1.1]), [1.0, 1.02, 1.1])

    def test_numbers_inside_tuples(self):
        """Numeric elements inside tuples/lists are handled like strings."""
        self.assertListEqual(
            natsort([("item", 10), ("item", 2), ("item", 1)]),
            [("item", 1), ("item", 2), ("item", 10)],
        )

    # ------------------------------------------------------------------
    # Type hint tests
    # ------------------------------------------------------------------

    def test_return_type_is_list_of_input_type(self):
        """Without return_indices, the return type matches the input list element type."""
        str_result = natsort(["b", "a", "c"])
        assert_type(str_result, list[str])

        int_result = natsort([3, 1, 2])
        assert_type(int_result, list[int])

    def test_return_indices_gives_list_of_int(self):
        """With return_indices=True, the return type is always list[int]."""
        indices = natsort(["b", "a", "c"], return_indices=True)
        assert_type(indices, list[int])
