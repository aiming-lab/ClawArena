"""
Test suite for requests/structures.py data structures.

Tests cover CaseInsensitiveDict and LookupDict behaviour.
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.structures import CaseInsensitiveDict, LookupDict


class TestCaseInsensitiveDict:
    def test_basic_set_get(self):
        d = CaseInsensitiveDict()
        d["Content-Type"] = "application/json"
        assert d["content-type"] == "application/json"
        assert d["CONTENT-TYPE"] == "application/json"

    def test_equality(self):
        d1 = CaseInsensitiveDict({"Accept": "text/html"})
        d2 = CaseInsensitiveDict({"accept": "text/html"})
        assert d1 == d2

    def test_length(self):
        d = CaseInsensitiveDict({"a": 1, "b": 2})
        assert len(d) == 2

    def test_lower_items(self):
        d = CaseInsensitiveDict({"X-Custom": "value"})
        items = dict(d.lower_items())
        assert "x-custom" in items
        assert items["x-custom"] == "value"

    def test_copy(self):
        d = CaseInsensitiveDict({"Key": "val"})
        d2 = d.copy()
        assert d2["key"] == "val"

    def test_delete(self):
        d = CaseInsensitiveDict({"Key": "val"})
        del d["key"]
        assert "Key" not in d


class TestLookupDict:
    def test_lookup_dict(self):
        d = LookupDict(name="test")
        d.ok = 200
        assert d["ok"] == 200
        assert d.get("ok") == 200
        assert d.get("missing") is None

    def test_repr(self):
        d = LookupDict(name="mydict")
        assert "mydict" in repr(d)
