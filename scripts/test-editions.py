#!/usr/bin/env python3
"""Check archive navigation and collection windows without writing test editions."""
import copy
import importlib.util
import unittest
from pathlib import Path
from typing import Any, cast

SPEC = importlib.util.spec_from_file_location("watch_build", Path(__file__).with_name("build.py"))
assert SPEC and SPEC.loader
build = cast(Any, importlib.util.module_from_spec(SPEC))
SPEC.loader.exec_module(build)


class EditionTests(unittest.TestCase):
    def setUp(self):
        self.original = build.EDITIONS
        self.previous = copy.deepcopy(min(self.original, key=lambda item: item["date"]))
        self.current = copy.deepcopy(self.previous)
        self.current.update({
            "id": "2099-10-26",
            "date": "2099-10-26",
            "dateLabel": "26 octobre 2099",
            "periodStart": "2099-10-19",
            "periodEnd": "2099-10-25",
        })
        for signal in self.current["signals"]:
            signal["timing"] = "context"
            signal["publicationDate"] = "2099-10-18"
        self.current["signals"][0]["timing"] = "week"
        self.current["signals"][0]["publicationDate"] = "2099-10-19"
        build.EDITIONS = [self.current, self.previous]

    def tearDown(self):
        build.EDITIONS = self.original

    def test_previous_only_in_archives(self):
        page = build.archives_body()
        self.assertIn(f'../editions/{self.previous["id"]}/', page)
        self.assertNotIn(f'../editions/{self.current["id"]}/', page)
        self.assertIn("1 édition antérieure disponible", page)

    def test_current_permalink_not_labelled_archive(self):
        self.assertNotIn("ARCHIVE · ", build.edition_body(self.current, True))
        self.assertIn("ARCHIVE · ", build.edition_body(self.previous, True))

    def test_complete_previous_seven_days(self):
        build.validate_data()
        self.current["signals"][0]["publicationDate"] = "2099-10-25"
        build.validate_data()

    def test_execution_day_outside_explicit_window(self):
        self.current["signals"][0]["publicationDate"] = "2099-10-26"
        with self.assertRaises(ValueError):
            build.validate_data()

    def test_incomplete_window_rejected(self):
        del self.current["periodEnd"]
        with self.assertRaises(ValueError):
            build.validate_data()

    def test_invalid_window_rejected(self):
        self.current["periodEnd"] = "2099-10-27"
        with self.assertRaises(ValueError):
            build.validate_data()
        self.current["periodEnd"] = "2099-10-25"
        self.current["periodStart"] = "2099-10-18"
        with self.assertRaises(ValueError):
            build.validate_data()

    def test_historical_data_unchanged(self):
        build.EDITIONS = copy.deepcopy(self.original)
        build.validate_data()

    def test_duplicate_edition_rejected(self):
        build.EDITIONS.append(copy.deepcopy(self.previous))
        with self.assertRaises(ValueError):
            build.validate_data()


if __name__ == "__main__":
    unittest.main()
