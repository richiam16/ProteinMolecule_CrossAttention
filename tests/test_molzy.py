"""
Unit and regression test for the molzy package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import molzy


def test_molzy_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "molzy" in sys.modules
